# Procedural 3D Floor Plan Generation

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural 3D Floor Plan Generation

* **Core Visual Mechanism**: The core mechanism involves generating continuous vertical boundary surfaces (walls) and using Boolean subtractive operations to punch out precise negative spaces for architectural features like doors and windows. This mimics the manual "trace, extrude, and bridge" workflow shown in the video, but applies it procedurally.
* **Why Use This Skill (Rationale)**: Manually tracing 2D floor plans, adding loop cuts, and bridging faces for every single window and door is highly tedious and prone to topological errors (like non-manifold geometry). Using a solid-modeling Boolean approach allows for non-destructive, mathematically precise architectural shells that can be rapidly iterated upon.
* **Overall Applicability**: Essential for architectural visualization, interior design mockups, real estate rendering, and creating base environments for game levels or indoor cinematic scenes.
* **Value Addition**: Instead of manually plotting vertices over an image, this skill instantly generates a clean, parameterized 3D room shell (walls, floor, door cutout, window cutout) ready for lighting and asset population.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: Solid cube primitives scaled to exact architectural dimensions (e.g., 6m x 5m x 2.8m).
  - **Operations**: A slightly smaller cube is subtracted from the main block to hollow it out, leaving walls of uniform thickness. Additional scaled cubes act as cutters for doors (intersecting the floor) and windows (elevated by a sill height).
  - **Topology**: Using the `EXACT` Boolean solver in Blender yields clean, flat n-gons for the walls, which is optimal for flat architectural surfaces.

* **Step B: Materials & Shading**
  - **Walls**: Principled BSDF with a matte, lightly textured finish. Base color defaults to an off-white/beige `(0.9, 0.9, 0.88)` with high Roughness `(0.9)` to simulate painted drywall.
  - **Floor**: Principled BSDF with a darker, semi-reflective finish `(0.2, 0.15, 0.1)` and lower Roughness `(0.4)` to simulate polished wood or tiling.

* **Step C: Lighting & Rendering Context**
  - Best paired with an environmental HDRI or a Sun lamp angled to cast strong directional shadows through the cutouts, highlighting the volumetric depth of the room.
  - Works exceptionally well in Cycles for accurate interior light bounces.

* **Step D: Animation & Dynamics**
  - Static architectural mesh. Can be used as a static collision object for fluid or cloth simulations (e.g., curtains blowing in the window).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base Wall Construction | `bmesh` primitive creation | Allows for mathematically precise bounding boxes without relying on viewport scaling operations. |
| Door/Window Cutouts | Boolean Modifiers | The most robust way to procedurally recreate the manual "loop cut and delete" workflow without complex vertex math. |
| Object Organization | Parenting | Parents the floor to the walls so the entire room can be moved or scaled as a single unit by the agent. |

> **Feasibility Assessment**: 90%. While the tutorial relies on manually tracing a *specific* image, this code reproduces the exact *structural output* of that workflow (hollowed walls with precise topological cutouts for windows/doors) parametrically, which is much more useful for an automated AI agent. 

#### 3b. Complete Reproduction Code

```python
def create_floorplan(
    scene_name: str = "Scene",
    object_name: str = "ProceduralRoom",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.9, 0.9, 0.88),
    width: float = 6.0,
    depth: float = 5.0,
    height: float = 2.8,
    wall_thickness: float = 0.2,
    **kwargs
) -> str:
    """
    Creates a parameterized 3D room with walls, a floor, and precise boolean 
    cutouts for a door and a window, mimicking architectural drafting workflows.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) color for the interior/exterior walls.
        width: Total width of the room (X-axis).
        depth: Total depth of the room (Y-axis).
        height: Ceiling height (Z-axis).
        wall_thickness: Thickness of the structural walls.

    Returns:
        Status string confirming creation.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Helper to create parameterized solid boxes ===
    def create_box(name, dim, loc):
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        scene.collection.objects.link(obj)
        
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        
        for v in bm.verts:
            v.co.x *= dim[0]
            v.co.y *= dim[1]
            v.co.z *= dim[2]
            v.co += Vector(loc)
            
        bm.to_mesh(mesh)
        bm.free()
        return obj

    # === Helper to cleanly apply boolean operations ===
    def apply_bool(target, cutter, op='DIFFERENCE'):
        mod = target.modifiers.new(name="ArchCut", type='BOOLEAN')
        mod.object = cutter
        mod.operation = op
        mod.solver = 'EXACT'
        
        bpy.context.view_layer.objects.active = target
        bpy.ops.object.modifier_apply(modifier=mod.name)

    loc_offset = Vector(location)

    # === Step 1: Create Main Structural Volumes ===
    # Center the walls so the bottom rests at Z=0
    walls = create_box(f"{object_name}_Walls", (width, depth, height), (0, 0, height / 2))
    
    # Create the negative space to hollow out the room
    hollow = create_box("Temp_Hollow", 
                        (width - wall_thickness * 2, depth - wall_thickness * 2, height + 0.2), 
                        (0, 0, height / 2))
    
    # Door cutter (1m wide, 2.1m tall, intersecting the front wall)
    door_cutter = create_box("Temp_DoorCutter", 
                             (1.0, wall_thickness * 4, 2.1), 
                             (0, -depth / 2, 2.1 / 2))
    
    # Window cutter (2m wide, 1.2m tall, elevated 1m off the floor on the side wall)
    window_cutter = create_box("Temp_WindowCutter", 
                               (wall_thickness * 4, 2.0, 1.2), 
                               (width / 2, 0, 1.0 + 1.2 / 2))

    # === Step 2: Execute Booleans ===
    apply_bool(walls, hollow, 'DIFFERENCE')
    apply_bool(walls, door_cutter, 'DIFFERENCE')
    apply_bool(walls, window_cutter, 'DIFFERENCE')
    
    # Cleanup temporary cutter objects and meshes
    for cutter in [hollow, door_cutter, window_cutter]:
        cutter_mesh = cutter.data
        bpy.data.objects.remove(cutter)
        bpy.data.meshes.remove(cutter_mesh)

    # === Step 3: Create Floor ===
    floor = create_box(f"{object_name}_Floor", (width, depth, 0.1), (0, 0, -0.05))

    # === Step 4: Materials & Shading ===
    # Wall Material (Matte Paint)
    mat_walls = bpy.data.materials.new(name=f"{object_name}_WallMat")
    mat_walls.use_nodes = True
    bsdf_walls = mat_walls.node_tree.nodes.get("Principled BSDF")
    if bsdf_walls:
        bsdf_walls.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf_walls.inputs['Roughness'].default_value = 0.9

    # Floor Material (Polished Wood/Tile)
    mat_floor = bpy.data.materials.new(name=f"{object_name}_FloorMat")
    mat_floor.use_nodes = True
    bsdf_floor = mat_floor.node_tree.nodes.get("Principled BSDF")
    if bsdf_floor:
        bsdf_floor.inputs['Base Color'].default_value = (0.15, 0.1, 0.08, 1.0)
        bsdf_floor.inputs['Roughness'].default_value = 0.35

    walls.data.materials.append(mat_walls)
    floor.data.materials.append(mat_floor)

    # === Step 5: Positioning & Hierarchy ===
    floor.parent = walls
    walls.location = loc_offset
    walls.scale = (scale, scale, scale)

    # Ensure visibility updates
    bpy.context.view_layer.update()

    return f"Created architectural shell '{object_name}' (Dimensions: {width}x{depth}m) at {location}."
```