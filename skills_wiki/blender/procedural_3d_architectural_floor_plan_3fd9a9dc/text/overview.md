# Procedural 3D Architectural Floor Plan

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural 3D Architectural Floor Plan

* **Core Visual Mechanism**: Generating an architectural "cutaway" or top-down 3D layout by constructing vertical planes from a defined set of 2D line segments (including gaps for doors) and dynamically adding thickness via a Solidify modifier. A corresponding floor plane is generated to ground the structure.
* **Why Use This Skill (Rationale)**: The tutorial demonstrates using generative AI to hallucinate 3D architectural renders from flat 2D blueprints. In a native 3D environment like Blender, the equivalent workflow is procedural generation. By defining walls as mathematical segments, you can instantly generate precise, customizable, and iteration-friendly interior layouts without tedious manual extrusion and edge-loop cutting.
* **Overall Applicability**: Ideal for architectural visualization, interior design pre-visualization, top-down RPG game level design, or generating structured environments for other props to be placed within. 
* **Value Addition**: This skill replaces the manual, error-prone process of modeling a house layout. It provides a programmatic foundation that guarantees straight walls, uniform thickness, and clean distinct materials for walls versus floors, matching the crisp aesthetic of professional real estate 3D renders.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: Created entirely via Python using the `bmesh` module.
  - **Wall Construction**: 2D coordinate pairs dictate the start and end points of walls. Vertical quads are generated between these points up to a specified `wall_height`.
  - **Modifiers**: A `Solidify` modifier is applied with an offset of 0 (centered) to give the infinitely thin planes realistic wall thickness.
  - **Floor Construction**: A simple polygonal plane that bounds the outer dimensions of the wall segments.

* **Step B: Materials & Shading**
  - **Wall Material**: A clean, bright Principled BSDF (e.g., `(0.9, 0.9, 0.9)`) with a slight roughness to simulate matte plaster or drywall, which catches soft shadows well.
  - **Floor Material**: A contrasting warm color (e.g., `(0.5, 0.35, 0.2)`) to simulate wood or neutral concrete, providing visual separation from the walls.

* **Step C: Lighting & Rendering Context**
  - **Lighting setup**: Works exceptionally well with an isometric orthographic camera and soft sun lighting or a high-contrast HDRI to emulate the "dollhouse" rendering style shown in the tutorial.
  - **Render Engine**: Compatible with both EEVEE and Cycles. Cycles will provide realistic bounce lighting inside the rooms.

* **Step D: Animation & Dynamics**
  - Static structural mesh. Can be animated by keyframing the `wall_height` or using a Build modifier for an "assembly" presentation effect.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Wall Layout Generation | `bmesh` planar quads | Allows defining a floor plan simply as a list of 2D line segments, natively handling gaps for doorways. |
| Wall Thickness | `Solidify` Modifier | Keeps the base geometry lightweight (just 2D lines) while ensuring perfectly uniform, non-destructive thickness. |
| Floor Generation | `bmesh` flat plane | Easily bounds the structure and allows for a separate material slot from the walls. |

> **Feasibility Assessment**: 100% of the *geometric structural* concept from the video is reproduced. While the script does not call external AI APIs to hallucinate furniture or textures, it provides the exact underlying 3D architectural shell required to build the scenes depicted in the video natively in Blender.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "3DFloorPlan",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.9, 0.9, 0.9),
    **kwargs,
) -> str:
    """
    Create a Procedural 3D Architectural Floor Plan in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created wall object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the walls in 0-1 range.
        **kwargs: 
            floor_color: (R, G, B) color for the floor.
            wall_height: Vertical height of the walls.
            wall_thickness: Thickness applied via Solidify.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Configurable parameters
    floor_color = kwargs.get("floor_color", (0.5, 0.35, 0.2))
    wall_height = kwargs.get("wall_height", 2.5)
    wall_thickness = kwargs.get("wall_thickness", 0.2)

    # Define the floor plan layout as a list of line segments (x1, y1, x2, y2)
    # Gaps in the lines represent doorways
    wall_segments = [
        # Exterior Bottom (with front door gap)
        (0, 0, 4.5, 0), (5.5, 0, 10, 0),
        # Exterior Right
        (10, 0, 10, 8),
        # Exterior Top
        (10, 8, 0, 8),
        # Exterior Left
        (0, 8, 0, 0),
        # Interior vertical wall separating left rooms from right hall
        (4, 0, 4, 3.5), (4, 4.5, 4, 8), 
        # Interior horizontal wall separating top left and bottom left rooms
        (0, 4, 1.5, 4), (2.5, 4, 4, 4), 
        # Interior small bathroom wall
        (7, 8, 7, 5), (7, 5, 8.5, 5), (9.5, 5, 10, 5)
    ]

    # === Step 1: Create Wall Geometry ===
    mesh_walls = bpy.data.meshes.new(object_name + "_Mesh")
    obj_walls = bpy.data.objects.new(object_name, mesh_walls)
    scene.collection.objects.link(obj_walls)

    bm = bmesh.new()
    for seg in wall_segments:
        x1, y1, x2, y2 = seg
        v1 = bm.verts.new((x1, y1, 0))
        v2 = bm.verts.new((x2, y2, 0))
        v3 = bm.verts.new((x2, y2, wall_height))
        v4 = bm.verts.new((x1, y1, wall_height))
        bm.faces.new((v1, v2, v3, v4))

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh_walls)
    bm.free()

    # Apply Solidify for thickness
    mod_solidify = obj_walls.modifiers.new(name="Wall_Thickness", type='SOLIDIFY')
    mod_solidify.thickness = wall_thickness
    mod_solidify.offset = 0  # Center thickness to align corners better

    # === Step 2: Create Floor Geometry ===
    mesh_floor = bpy.data.meshes.new(object_name + "_Floor_Mesh")
    obj_floor = bpy.data.objects.new(object_name + "_Floor", mesh_floor)
    scene.collection.objects.link(obj_floor)

    bm_floor = bmesh.new()
    # Create a boundary floor that covers the 10x8 footprint
    v1 = bm_floor.verts.new((0, 0, 0))
    v2 = bm_floor.verts.new((10, 0, 0))
    v3 = bm_floor.verts.new((10, 8, 0))
    v4 = bm_floor.verts.new((0, 8, 0))
    bm_floor.faces.new((v1, v2, v3, v4))
    bm_floor.to_mesh(mesh_floor)
    bm_floor.free()

    # Parent floor to walls for easy transformation
    obj_floor.parent = obj_walls

    # === Step 3: Build Materials ===
    # Wall Material
    mat_wall = bpy.data.materials.new(name=f"{object_name}_Wall_Mat")
    mat_wall.use_nodes = True
    bsdf_wall = mat_wall.node_tree.nodes.get("Principled BSDF")
    if bsdf_wall:
        bsdf_wall.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf_wall.inputs['Roughness'].default_value = 0.8
    obj_walls.data.materials.append(mat_wall)

    # Floor Material
    mat_floor = bpy.data.materials.new(name=f"{object_name}_Floor_Mat")
    mat_floor.use_nodes = True
    bsdf_floor = mat_floor.node_tree.nodes.get("Principled BSDF")
    if bsdf_floor:
        bsdf_floor.inputs['Base Color'].default_value = (*floor_color, 1.0)
        bsdf_floor.inputs['Roughness'].default_value = 0.3
    obj_floor.data.materials.append(mat_floor)

    # === Step 4: Position & Scale ===
    obj_walls.location = Vector(location)
    
    # We apply scale cautiously. Since Solidify thickness is affected by object scale,
    # we usually want to apply scale if we scale the object.
    obj_walls.scale = (scale, scale, scale)
    
    # Ensure view layer updates
    bpy.context.view_layer.update()

    return f"Created procedural 3D floor plan '{object_name}' (Walls + Floor) at {location} scaled by {scale}."
```