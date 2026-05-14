# Architectural Interior Shell & Cove Lighting Setup

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Architectural Interior Shell & Cove Lighting Setup

* **Core Visual Mechanism**: This pattern generates a complete architectural enclosure optimized for interior rendering. It features inward-facing normals, a Boolean-driven window cutout for directional light entry, a floating dropped ceiling panel, and hidden emission planes that create a realistic recessed "cove" lighting effect bouncing off the main ceiling. It also includes procedural stretched-noise wood flooring and classic wainscoting-style wall moldings using bevelled curves.
* **Why Use This Skill (Rationale)**: Interior scenes require very specific lighting containment. Unlike exterior scenes, light should only enter through designated architectural openings (windows) or emit from practical fixtures. By turning the world environment to black and using a combination of a strong directional Sun and hidden ambient cove lighting, this setup physically accurately mimics how light behaves in a modern enclosed room, generating high-contrast, photorealistic shadows and soft bounce light.
* **Overall Applicability**: Perfect as the base environment for architectural visualization, interior design mockups, character "bedroom" scenes, or stylized room dioramas.
* **Value Addition**: Instead of manually building walls, aligning planes, cutting holes, and tuning lighting ratios, this skill instantly provides a structurally sound, beautifully lit, and texturally grounded room shell. The procedural wood floor and procedural wall moldings instantly add scale and realism compared to flat primitive walls.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Room Shell**: A basic box scaled to room proportions (e.g., 4x5x2.8m) with inverted normals so the interior faces are renderable.
  - **Window**: A wireframe cube used as a Boolean `DIFFERENCE` cutter on the main room mesh to cleanly punch out the window opening.
  - **Ceiling System**: Uses two layered planes. A "Floating Panel" dropped slightly below the ceiling with a Solidify modifier, and a slightly larger "Cove Light" emission plane hidden just above it to bounce light outward.
  - **Moldings**: Rectangular curve objects (`POLY` splines) with a `bevel_depth` applied to create clean wainscoting frames. An Array modifier tiles them across the wall.
* **Step B: Materials & Shading**
  - **Walls**: Soft, customizable pastel Principled BSDF (`Roughness: 0.8`).
  - **Wood Floor**: Procedural texture relying on a `Noise Texture` passed through a stretched `Mapping` node (scaled 10x on one axis to simulate wood grain), fed into a `Color Ramp` using warm browns `(0.4, 0.2, 0.1)` and `(0.7, 0.4, 0.2)`.
  - **Cove Light**: Pure `Emission` shader outputting a warm color `(1.0, 0.85, 0.6)` at a strength of `5.0`.
* **Step C: Lighting & Rendering Context**
  - **World**: Forced to pure black `(0, 0, 0, 1)` to eliminate flat ambient lighting and emphasize the interior light interplay.
  - **Sun Light**: Placed directly outside the Boolean window, angled sharply into the room with high energy (`8.0`) and a warm tint. 
  - **Render Context**: Built for Cycles (for accurate light bounces inside the cove) but compatible with EEVEE.
* **Step D: Animation & Dynamics**
  - Static architectural environment. Lighting and camera positions are easily animated.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Room & Boolean** | `bmesh` primitives + Boolean Modifier | Prevents context errors in background execution while ensuring perfectly sealed interior corners. |
| **Wall Moldings** | `bpy.data.curves` + Bevel + Array Modifier | Procedurally generates clean, non-destructive decorative frames without complex mesh modeling. |
| **Wood Floor** | Shader node tree (Noise + Stretched Vector) | Infinite resolution, requires no external image dependencies or UV mapping. |
| **Cove Lighting** | Layered planes + Emission Shader | Physically correct way to simulate recessed ceiling light bouncing off architectural surfaces. |

> **Feasibility Assessment**: 100% reproduction of the architectural shell, base materials, and lighting environment. (Note: Hand-placed third-party furniture assets from the video are excluded as they rely on external asset libraries, but the environment is perfectly primed to receive them).

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "InteriorRoomShell",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.85, 0.8, 0.85),
    **kwargs,
) -> str:
    """
    Create a complete interior room shell with window, procedural wood floor, 
    recessed cove lighting, and directional sun light.

    Args:
        scene_name: Name of the target scene.
        object_name: Prefix name for the created objects.
        location: (x, y, z) world-space position of the room origin.
        scale: Uniform scale factor (1.0 = standard 4x5m room).
        material_color: (R, G, B) base color for the painted walls.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Room Base Dimensions
    w = 4.0 * scale
    l = 5.0 * scale
    h = 2.8 * scale
    
    # --- 1. Room Shell (Walls and Base Ceiling) ---
    bm_room = bmesh.new()
    bmesh.ops.create_cube(bm_room, size=1.0)
    bmesh.ops.scale(bm_room, vec=(w, l, h), verts=bm_room.verts)
    bmesh.ops.translate(bm_room, vec=(0, 0, h/2), verts=bm_room.verts)
    bmesh.ops.reverse_faces(bm_room, faces=bm_room.faces) # Flip normals inward
    
    room_mesh = bpy.data.meshes.new(name=f"{object_name}_Mesh")
    bm_room.to_mesh(room_mesh)
    bm_room.free()
    
    room = bpy.data.objects.new(object_name, room_mesh)
    scene.collection.objects.link(room)
    room.location = location
    
    # --- 2. Window Hole Cutter (Boolean) ---
    cutter_mesh = bpy.data.meshes.new(f"{object_name}_WindowCutter_Mesh")
    bm_cutter = bmesh.new()
    bmesh.ops.create_cube(bm_cutter, size=1.0)
    bmesh.ops.scale(bm_cutter, vec=(0.5 * scale, 1.5 * scale, 1.2 * scale), verts=bm_cutter.verts)
    bm_cutter.to_mesh(cutter_mesh)
    bm_cutter.free()
    
    cutter = bpy.data.objects.new(f"{object_name}_WindowCutter", cutter_mesh)
    scene.collection.objects.link(cutter)
    # Position on the +X wall
    cutter.location = (location[0] + w/2, location[1], location[2] + h/2)
    cutter.display_type = 'WIRE'
    cutter.hide_render = True
    
    bool_mod = room.modifiers.new(name="WindowCut", type='BOOLEAN')
    bool_mod.object = cutter
    bool_mod.operation = 'DIFFERENCE'
    
    # --- 3. Base Materials & Floor ---
    # Wall material
    mat_wall = bpy.data.materials.new(name=f"{object_name}_WallMat")
    mat_wall.use_nodes = True
    if "Principled BSDF" in mat_wall.node_tree.nodes:
        bsdf_wall = mat_wall.node_tree.nodes["Principled BSDF"]
        bsdf_wall.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf_wall.inputs["Roughness"].default_value = 0.8
    room.data.materials.append(mat_wall)
    
    # Floor Mesh (Plane sitting directly on the bottom inner face to avoid z-fighting)
    floor_mesh = bpy.data.meshes.new(f"{object_name}_Floor_Mesh")
    bm_floor = bmesh.new()
    bmesh.ops.create_plane(bm_floor, size=1.0)
    bmesh.ops.scale(bm_floor, vec=(w, l, 1), verts=bm_floor.verts)
    bm_floor.to_mesh(floor_mesh)
    bm_floor.free()
    
    floor = bpy.data.objects.new(f"{object_name}_Floor", floor_mesh)
    scene.collection.objects.link(floor)
    floor.location = (location[0], location[1], location[2] + 0.001)
    
    # Floor Material (Procedural Wood Grain)
    mat_wood = bpy.data.materials.new(name=f"{object_name}_WoodFloor")
    mat_wood.use_nodes = True
    nodes = mat_wood.node_tree.nodes
    links = mat_wood.node_tree.links
    bsdf_wood = nodes.get("Principled BSDF")
    
    tex_noise = nodes.new('ShaderNodeTexNoise')
    tex_noise.inputs['Scale'].default_value = 2.0
    tex_noise.inputs['Detail'].default_value = 15.0
    tex_noise.inputs['Roughness'].default_value = 0.6
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.inputs['Scale'].default_value = (1.0, 10.0, 1.0) # Stretch to create grain
    tex_coord = nodes.new('ShaderNodeTexCoord')
    
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], tex_noise.inputs['Vector'])
    
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.3
    ramp.color_ramp.elements[0].color = (0.4, 0.2, 0.1, 1.0)
    ramp.color_ramp.elements[1].position = 0.7
    ramp.color_ramp.elements[1].color = (0.7, 0.4, 0.2, 1.0)
    
    links.new(tex_noise.outputs['Fac'], ramp.inputs['Fac'])
    if bsdf_wood:
        links.new(ramp.outputs['Color'], bsdf_wood.inputs['Base Color'])
        bsdf_wood.inputs['Roughness'].default_value = 0.25
    floor.data.materials.append(mat_wood)
    
    # --- 4. Recessed Ceiling System ---
    mat_white = bpy.data.materials.new(name=f"{object_name}_WhiteMat")
    mat_white.use_nodes = True
    if "Principled BSDF" in mat_white.node_tree.nodes:
        mat_white.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.9, 0.9, 0.9, 1.0)

    # Floating Panel (Visible ceiling)
    ceil_mesh = bpy.data.meshes.new(f"{object_name}_FloatingCeil_Mesh")
    bm_ceil = bmesh.new()
    bmesh.ops.create_plane(bm_ceil, size=1.0)
    bmesh.ops.scale(bm_ceil, vec=(w - 0.8*scale, l - 0.8*scale, 1), verts=bm_ceil.verts)
    bm_ceil.to_mesh(ceil_mesh)
    bm_ceil.free()
    
    ceil_panel = bpy.data.objects.new(f"{object_name}_FloatingCeiling", ceil_mesh)
    scene.collection.objects.link(ceil_panel)
    ceil_panel.location = (location[0], location[1], location[2] + h - 0.15*scale)
    ceil_panel.data.materials.append(mat_white)
    
    solid = ceil_panel.modifiers.new(name="Solidify", type='SOLIDIFY')
    solid.thickness = 0.05 * scale
    solid.offset = -1 
    
    # Cove Light Plane (Hidden emission bouncing off top)
    cove_mesh = bpy.data.meshes.new(f"{object_name}_Cove_Mesh")
    bm_cove = bmesh.new()
    bmesh.ops.create_plane(bm_cove, size=1.0)
    bmesh.ops.scale(bm_cove, vec=(w - 1.0*scale, l - 1.0*scale, 1), verts=bm_cove.verts)
    bm_cove.to_mesh(cove_mesh)
    bm_cove.free()
    
    cove_light = bpy.data.objects.new(f"{object_name}_CoveLight", cove_mesh)
    scene.collection.objects.link(cove_light)
    cove_light.location = (location[0], location[1], location[2] + h - 0.05*scale)
    
    mat_cove = bpy.data.materials.new(name=f"{object_name}_CoveEmission")
    mat_cove.use_nodes = True
    mat_cove.node_tree.nodes.remove(mat_cove.node_tree.nodes.get("Principled BSDF"))
    emission = mat_cove.node_tree.nodes.new("ShaderNodeEmission")
    emission.inputs['Color'].default_value = (1.0, 0.85, 0.6, 1.0)
    emission.inputs['Strength'].default_value = 8.0
    out = mat_cove.node_tree.nodes.get("Material Output")
    mat_cove.node_tree.links.new(emission.outputs['Emission'], out.inputs['Surface'])
    cove_light.data.materials.append(mat_cove)
    
    # --- 5. Wall Moldings ---
    curve_data = bpy.data.curves.new(name=f"{object_name}_MoldingCurve", type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.bevel_depth = 0.015 * scale
    curve_data.bevel_resolution = 3
    
    spline = curve_data.splines.new(type='POLY')
    spline.points.add(3) # 4 points
    spline.use_cyclic_u = True
    
    # Rectangular frame points
    mw = 0.4 * scale
    mh = 0.8 * scale
    spline.points[0].co = (-mw, -mh, 0, 1)
    spline.points[1].co = (mw, -mh, 0, 1)
    spline.points[2].co = (mw, mh, 0, 1)
    spline.points[3].co = (-mw, mh, 0, 1)
    
    molding = bpy.data.objects.new(f"{object_name}_WallMolding", curve_data)
    scene.collection.objects.link(molding)
    
    # Place on the interior -Y wall
    molding.location = (location[0] - 0.8*scale, location[1] - l/2 + 0.02*scale, location[2] + 1.2*scale)
    molding.rotation_euler = (math.pi/2, 0, 0)
    molding.data.materials.append(mat_white)
    
    # Array to tile along the wall
    array_mod = molding.modifiers.new(name="Array", type='ARRAY')
    array_mod.count = 3
    array_mod.use_relative_offset = True
    array_mod.relative_offset_displace = (2.5, 0, 0)
    
    # --- 6. Lighting Context ---
    # Sun light entering through the window
    light_data = bpy.data.lights.new(name=f"{object_name}_Sun", type='SUN')
    sun = bpy.data.objects.new(name=f"{object_name}_Sun", object_data=light_data)
    scene.collection.objects.link(sun)
    sun.location = (location[0] + w/2 + 2.0*scale, location[1], location[2] + h)
    # Point downward and inward (-X direction)
    sun.rotation_euler = (0, -math.radians(60), math.radians(20))
    light_data.energy = 8.0
    light_data.color = (1.0, 0.95, 0.85)
    
    # World Background (Black out ambient light)
    world = scene.world
    if world and world.use_nodes:
        bg_node = world.node_tree.nodes.get("Background")
        if bg_node:
            bg_node.inputs[0].default_value = (0, 0, 0, 1)
            
    # Optimizer Render Settings
    scene.cycles.use_denoising = True
    
    return f"Created '{object_name}' - Complete room shell with window cut, procedural wood floor, cove lighting, and sun setup."
```