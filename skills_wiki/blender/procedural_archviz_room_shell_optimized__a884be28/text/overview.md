# Procedural Archviz Room Shell & Optimized Glass

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Archviz Room Shell & Optimized Glass

* **Core Visual Mechanism**: This skill uses the "inverted hull" technique—taking a standard primitive cube, scaling it to realistic human dimensions, and flipping its normals inward to instantly create a room interior. It pairs this geometry with a Light Path-optimized glass shader that prevents Cycles from calculating expensive caustics, drastically reducing interior render noise.

* **Why Use This Skill (Rationale)**: The creator emphasizes overcoming "blank canvas syndrome" by immediately establishing a bounded, human-scaled space. Standard glass shaders in enclosed rooms create immense noise because rays get trapped trying to calculate caustics through the glass. Mixing a Glass and Transparent shader using a Light Path node allows direct light to enter the room freely while maintaining reflections on the window surface.

* **Overall Applicability**: This is the foundational starting point for any architectural visualization (Archviz) interior. It establishes the physical bounds, functional camera placement, discrete material zones (walls vs. floor), and the environmental lighting gateway (the window).

* **Value Addition**: Instead of manually pushing vertices, this skill parametrically generates a room of any size, automatically separating the floor material from the walls via normal-direction scripting, cuts a window procedurally, and implements an advanced noise-reduction shader that standard primitives lack.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A standard cube, scaled to architectural dimensions (e.g., 5m x 6m x 2.6m ceiling height).
  - **Inversion**: The scale is applied, and normals are flipped inward (`bmesh.ops.reverse_faces`).
  - **Window Cutout**: A secondary cube is used as a Boolean `DIFFERENCE` cutter to non-destructively punch a hole in the wall.
  - **Window Pane**: A simple plane placed inside the cutout to hold the glass material.

* **Step B: Materials & Shading**
  - **Wall Material**: Simple Principled BSDF, slightly off-white, high roughness.
  - **Floor Material**: Procedurally assigned by iterating through the BMesh and finding the face whose normal points straight up (`Z == 1.0`).
  - **Optimized Archviz Glass**: A node tree mixing a `Glass BSDF` and `Transparent BSDF`. The `Factor` is driven by a `Light Path` node (combining `Is Shadow Ray` and `Is Diffuse Ray`). This allows environment light to pass through the window without triggering complex caustic noise calculations inside the room.

* **Step C: Lighting & Rendering Context**
  - **Render Engine**: Forced to Cycles. Viewport denoising is activated to allow rapid iterative design without visual static.
  - **World Environment**: A `Sky Texture` (Nishita) is instantiated to simulate realistic sun and sky lighting pouring through the newly cut window, mimicking the HDRI setup from the tutorial.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Room Shell | `bpy.ops.mesh.primitive_cube_add` + Normal Flipping | Easiest way to establish a perfectly sealed rectangular boundary. |
| Floor/Wall Masking | `bmesh` normal evaluation | Procedurally finds the floor face regardless of room dimensions by checking normal vectors. |
| Window Cutout | `BOOLEAN` Modifier | Keeps the room mesh procedural and allows the window to be moved easily later. |
| Noise-free Glass | Custom Shader Node Tree | Direct implementation of the tutorial's specific warning about default glass causing viewport noise. |

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "ArchvizRoom",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    room_dimensions: tuple = (5.0, 6.0, 2.6),
    floor_color: tuple = (0.4, 0.2, 0.05, 1.0),
    **kwargs,
) -> str:
    """
    Creates a parametric interior room shell with a window cutout and noise-optimized glass.
    
    Args:
        scene_name: Name of the scene.
        object_name: Base name for the generated objects.
        location: World-space base location (floor center).
        scale: Master scale multiplier.
        room_dimensions: (Width X, Depth Y, Height Z) in meters.
        floor_color: RGBA color for the floor material placeholder.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Enable Cycles and Viewport Denoising
    scene.render.engine = 'CYCLES'
    try:
        scene.cycles.use_preview_denoising = True
    except AttributeError:
        pass # Handle API differences in older/newer Blender versions

    # === 1. Create Materials ===
    
    # Wall Material
    mat_wall = bpy.data.materials.new(name=f"{object_name}_Wall")
    mat_wall.use_nodes = True
    bsdf_wall = mat_wall.node_tree.nodes.get("Principled BSDF")
    if bsdf_wall:
        bsdf_wall.inputs["Base Color"].default_value = (0.9, 0.9, 0.9, 1.0)
        bsdf_wall.inputs["Roughness"].default_value = 0.8

    # Floor Material
    mat_floor = bpy.data.materials.new(name=f"{object_name}_Floor")
    mat_floor.use_nodes = True
    bsdf_floor = mat_floor.node_tree.nodes.get("Principled BSDF")
    if bsdf_floor:
        bsdf_floor.inputs["Base Color"].default_value = floor_color
        bsdf_floor.inputs["Roughness"].default_value = 0.3

    # Optimized Archviz Glass Material (Light Path Trick)
    mat_glass = bpy.data.materials.new(name=f"{object_name}_OptiGlass")
    mat_glass.use_nodes = True
    nodes = mat_glass.node_tree.nodes
    links = mat_glass.node_tree.links
    nodes.clear() # Clear default

    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = (400, 0)
    
    node_mix = nodes.new(type='ShaderNodeMixShader')
    node_mix.location = (200, 0)
    
    node_glass = nodes.new(type='ShaderNodeBsdfGlass')
    node_glass.location = (0, 100)
    node_glass.inputs['Roughness'].default_value = 0.05
    node_glass.inputs['IOR'].default_value = 1.45
    
    node_trans = nodes.new(type='ShaderNodeBsdfTransparent')
    node_trans.location = (0, -100)
    
    node_lightpath = nodes.new(type='ShaderNodeLightPath')
    node_lightpath.location = (-200, 300)
    
    node_math = nodes.new(type='ShaderNodeMath')
    node_math.operation = 'MAXIMUM'
    node_math.location = (0, 300)

    # Link logic: If ray is shadow or diffuse, use transparent (let light in). Otherwise, use glass (reflections).
    links.new(node_lightpath.outputs['Is Shadow Ray'], node_math.inputs[0])
    links.new(node_lightpath.outputs['Is Diffuse Ray'], node_math.inputs[1])
    links.new(node_math.outputs[0], node_mix.inputs[0])
    links.new(node_glass.outputs['BSDF'], node_mix.inputs[1])
    links.new(node_trans.outputs['BSDF'], node_mix.inputs[2])
    links.new(node_mix.outputs['Shader'], node_output.inputs['Surface'])

    # === 2. Create Room Shell Geometry ===
    
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    room = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(room)
    
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    
    # Scale cube to room dimensions
    bmesh.ops.scale(bm, vec=Vector(room_dimensions), verts=bm.verts)
    
    # Move so the floor is at Z = 0
    bmesh.ops.translate(bm, vec=Vector((0, 0, room_dimensions[2] / 2.0)), verts=bm.verts)
    
    # Flip normals inward to create a room
    bmesh.ops.reverse_faces(bm, faces=bm.faces)
    
    # Assign materials to slots
    room.data.materials.append(mat_wall)  # Index 0
    room.data.materials.append(mat_floor) # Index 1
    
    # Find floor face (Normal pointing UP +Z in local space) and assign floor material
    for face in bm.faces:
        if face.normal.z > 0.9:
            face.material_index = 1
        else:
            face.material_index = 0
            
    bm.to_mesh(mesh)
    bm.free()

    # === 3. Create Window Cutout ===
    
    cutter_mesh = bpy.data.meshes.new(f"{object_name}_Cutter_Mesh")
    cutter = bpy.data.objects.new(f"{object_name}_Cutter", cutter_mesh)
    scene.collection.objects.link(cutter)
    
    bm_cutter = bmesh.new()
    bmesh.ops.create_cube(bm_cutter, size=1.0)
    bm_cutter.to_mesh(cutter_mesh)
    bm_cutter.free()
    
    # Position cutter on the front wall (-Y axis)
    window_width = 3.0
    window_height = 2.0
    cutter.scale = (window_width, 1.0, window_height)
    cutter.location = (0, -room_dimensions[1] / 2.0, window_height / 2.0 + 0.2)
    cutter.display_type = 'WIRE'
    cutter.hide_render = True

    # Apply Boolean to room
    bool_mod = room.modifiers.new(name="WindowCut", type='BOOLEAN')
    bool_mod.object = cutter
    bool_mod.operation = 'DIFFERENCE'

    # === 4. Add Window Glass Pane ===
    
    pane_mesh = bpy.data.meshes.new(f"{object_name}_Pane_Mesh")
    pane = bpy.data.objects.new(f"{object_name}_Glass", pane_mesh)
    scene.collection.objects.link(pane)
    
    bm_pane = bmesh.new()
    bmesh.ops.create_grid(bm_pane, x_segments=1, y_segments=1, size=0.5)
    
    # Stand pane upright and scale
    bmesh.ops.rotate(bm_pane, cent=(0,0,0), matrix=mathutils.Matrix.Rotation(math.radians(90), 3, 'X'), verts=bm_pane.verts)
    bmesh.ops.scale(bm_pane, vec=(window_width, 1.0, window_height), verts=bm_pane.verts)
    bm_pane.to_mesh(pane_mesh)
    bm_pane.free()
    
    pane.location = cutter.location
    pane.data.materials.append(mat_glass)

    # === 5. Setup Camera & World Environment ===
    
    # Add Camera inside room
    cam_data = bpy.data.cameras.new(f"{object_name}_Camera")
    cam_obj = bpy.data.objects.new(f"{object_name}_Camera", cam_data)
    scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    # Place at average eye height, looking at the window
    cam_obj.location = (0, room_dimensions[1] / 2.0 - 1.0, 1.6)
    cam_obj.rotation_euler = (math.radians(90), 0, math.radians(180))

    # Setup Sky Texture
    world = scene.world
    if not world:
        world = bpy.data.worlds.new("World")
        scene.world = world
    world.use_nodes = True
    wnodes = world.node_tree.nodes
    wlinks = world.node_tree.links
    
    bg_node = wnodes.get("Background")
    sky_node = wnodes.new("ShaderNodeTexSky")
    sky_node.sky_type = 'NISHITA'
    sky_node.sun_elevation = math.radians(25)
    sky_node.sun_rotation = math.radians(-45) # Angle sun into the window
    
    if bg_node:
        wlinks.new(sky_node.outputs['Color'], bg_node.inputs['Color'])

    # Apply Master Transformations
    master_loc = Vector(location)
    for obj in [room, cutter, pane, cam_obj]:
        obj.location += master_loc
        obj.scale = (scale, scale, scale)

    return f"Created Archviz Room '{object_name}' ({room_dimensions[0]}x{room_dimensions[1]}m) with optimized glass window and camera setup."
```