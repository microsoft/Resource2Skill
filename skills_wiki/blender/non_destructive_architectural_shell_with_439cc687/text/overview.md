# Non-Destructive Architectural Shell with Collection Booleans

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Non-Destructive Architectural Shell with Collection Booleans

* **Core Visual Mechanism**: This technique builds the primary structure of an interior scene using a procedural modifier stack. A base cube with flipped normals acts as the interior volume. A `Solidify` modifier pushes geometry outward to create wall thickness. Openings (windows/doors) are carved dynamically using a `Boolean` modifier tied to a hidden Collection. Finally, a `Bevel` modifier catches highlights on the freshly cut window sills and room corners, a hallmark of photorealism.
* **Why Use This Skill (Rationale)**: Architectural layouts require constant iteration. Destructive modeling (manually cutting edge loops and deleting faces for windows) ruins topology and makes moving elements tedious. By using Collection-based Booleans, you can shift, scale, or add windows simply by moving proxy cubes around the scene. 
* **Overall Applicability**: Essential for any interior rendering, ArchViz (Architectural Visualization), or level design block-out. It provides a watertight, physically thick shell that interacts correctly with path-traced lighting (Cycles) and prevents light leaks.
* **Value Addition**: Compared to just adding a cube and removing a face, this creates a realistic, thick-walled structure with properly rounded edges and multi-material slots (floor vs. walls) assigned dynamically.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A standard Cube, scaled to room dimensions.
  - **Normals**: Mesh normals are flipped to point *inward* (toward the camera).
  - **Modifiers**:
    1. `Solidify`: `offset` set to `-1.0` (expands outward from the flipped normals), generating physical wall thickness without cluttering interior workspace.
    2. `Boolean` (Difference): Operates on an entire target Collection (e.g., "Booleans") rather than a single object.
    3. `Bevel`: Applied last. Uses `Angle` limit. This ensures the 90-degree cuts made by the Boolean modifier get a slight rounding, which is crucial for edge highlights in rendering.
* **Step B: Materials & Shading**
  - Utilizes two distinct `Principled BSDF` materials on a single mesh (Walls and Floor).
  - Material assignment is handled programmatically via `bmesh` by evaluating the Z-axis of face normals.
  - To mimic the video's Ambient Occlusion (AO) PBR layering, an `Ambient Occlusion` node is multiplied into the Base Color using a Mix node, grounding the corners with procedural contact shadows.
* **Step C: Lighting & Rendering Context**
  - Designed for **Cycles** (Path Tracing). Physically accurate lighting requires actual wall thickness to bounce light naturally and prevent HDRI sky light from leaking through infinitely thin planes.
  - Best paired with an HDRI environment map and a window spanning the Boolean cutout.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Room Shell & Thickness | `bpy.ops.mesh.primitive` + `Solidify` | Clean bounding box manipulation; non-destructive wall generation. |
| Windows/Doors | `Boolean` (Collection mode) | Allows infinite, movable cutouts without breaking base mesh topology. |
| Edge Highlights | `Bevel` Modifier | Added after Booleans to procedurally round the sharp cut edges. |
| Material Assignment | `bmesh` normal evaluation | Automatically maps the floor material to the bottom face, regardless of room scale. |

> **Feasibility Assessment**: 100% of the non-destructive room construction technique from the tutorial is reproduced here. (Note: Specific external assets like Quixel Megascans textures or 3D furniture models from the video are omitted to keep the code self-contained and purely procedural).

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "InteriorRoomShell",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.85, 0.82, 0.78),
    **kwargs,
) -> str:
    """
    Create a non-destructive interior room shell with wall thickness, beveled edges, 
    and a dynamic Boolean cutter collection for windows.

    Args:
        scene_name: Name of the active scene.
        object_name: Name of the generated room object.
        location: Base floor location (x, y, z).
        scale: General scale multiplier.
        material_color: RGB tuple for the Wall material.
        **kwargs: Overrides for 'room_width', 'room_length', 'room_height', 'wall_thickness'.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Dimensions
    room_x = kwargs.get('room_width', 4.0) * scale
    room_y = kwargs.get('room_length', 5.0) * scale
    room_z = kwargs.get('room_height', 2.8) * scale
    thickness = kwargs.get('wall_thickness', 0.2) * scale

    # Ensure we are in Object mode
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    # === Step 1: Base Room Mesh ===
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    room = bpy.context.active_object
    room.name = object_name
    
    # Scale and apply to preserve modifier uniformity
    room.scale = (room_x, room_y, room_z)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Offset so the origin is vertically centered, placing the floor exactly at location.z
    room.location.z += room_z / 2.0
    
    # Flip normals inward (we are viewing from the inside)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.flip_normals()
    bpy.ops.object.mode_set(mode='OBJECT')

    # === Step 2: Modifiers ===
    # Solidify: Negative offset pushes walls OUTWARD relative to the inward normals
    mod_solidify = room.modifiers.new(name="WallThickness", type='SOLIDIFY')
    mod_solidify.thickness = thickness
    mod_solidify.offset = -1.0 
    
    # Boolean: Setup for windows/doors
    bool_col_name = f"{object_name}_Cutters"
    if bool_col_name not in bpy.data.collections:
        bool_col = bpy.data.collections.new(bool_col_name)
        scene.collection.children.link(bool_col)
    else:
        bool_col = bpy.data.collections[bool_col_name]
    
    # Hide cutter collection from viewport and render
    bool_col.hide_viewport = True
    bool_col.hide_render = True

    mod_bool = room.modifiers.new(name="WindowCuts", type='BOOLEAN')
    mod_bool.operation = 'DIFFERENCE'
    mod_bool.operand_type = 'COLLECTION'
    mod_bool.collection = bool_col

    # Bevel: Round edges for photorealism (Must be AFTER boolean to affect cuts)
    mod_bevel = room.modifiers.new(name="EdgeHighlight", type='BEVEL')
    mod_bevel.width = 0.015 * scale
    mod_bevel.segments = 3
    mod_bevel.limit_method = 'ANGLE'

    # === Step 3: Populate Boolean Cutters ===
    # Create a default window cutter on the positive Y wall
    cutter_z = location[2] + 1.2 * scale
    cutter_y = location[1] + (room_y / 2.0)
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(location[0], cutter_y, cutter_z))
    cutter = bpy.context.active_object
    cutter.name = f"{object_name}_Window_01"
    cutter.scale = (1.5 * scale, thickness * 4, 1.2 * scale)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Move cutter into the boolean collection
    for col in cutter.users_collection:
        col.objects.unlink(cutter)
    bool_col.objects.link(cutter)

    # === Step 4: Procedural Materials ===
    def create_ao_material(mat_name, color):
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (300, 0)
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 0)
        bsdf.inputs["Roughness"].default_value = 0.8
        ao = nodes.new(type='ShaderNodeAmbientOcclusion')
        ao.location = (-400, 0)
        
        # Cross-version compatibility for Mix Node
        try:
            mix = nodes.new(type='ShaderNodeMix') # Blender 3.4+
            mix.data_type = 'RGBA'
            mix.blend_type = 'MULTIPLY'
            mix.inputs[0].default_value = 0.6
            mix.inputs[2].default_value = (*color, 1.0)
            links.new(ao.outputs["Color"], mix.inputs[1])
            links.new(mix.outputs[2], bsdf.inputs["Base Color"])
        except RuntimeError:
            mix = nodes.new(type='ShaderNodeMixRGB') # Blender < 3.4
            mix.blend_type = 'MULTIPLY'
            mix.inputs[0].default_value = 0.6
            mix.inputs[2].default_value = (*color, 1.0)
            links.new(ao.outputs["Color"], mix.inputs[1])
            links.new(mix.outputs[0], bsdf.inputs["Base Color"])
            
        mix.location = (-200, 0)
        links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
        return mat

    mat_walls = create_ao_material(f"{object_name}_Walls", material_color)
    mat_floor = create_ao_material(f"{object_name}_Floor", (0.15, 0.1, 0.08)) # Dark wood tone

    room.data.materials.append(mat_walls) # Index 0
    room.data.materials.append(mat_floor) # Index 1

    # Assign Floor material dynamically based on face normals
    bm = bmesh.new()
    bm.from_mesh(room.data)
    for face in bm.faces:
        # Since normals point inward, the floor face normal points straight UP (Z > 0.5)
        if face.normal.z > 0.5:
            face.material_index = 1
        else:
            face.material_index = 0
    bm.to_mesh(room.data)
    bm.free()

    # Finalize Context
    bpy.ops.object.select_all(action='DESELECT')
    room.select_set(True)
    bpy.context.view_layer.objects.active = room

    return f"Created room shell '{object_name}' (Dims: {room_x}x{room_y}x{room_z}) with Booleans, Solidify, and AO Materials."
```