# Procedural Architectural Siding via Proxy-Volume Booleans

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Architectural Siding via Proxy-Volume Booleans

* **Core Visual Mechanism**: This technique uses a layered, non-destructive modifier stack to create complex architectural detailing. It relies on generating an infinite, uniform pattern (using an `Array` modifier on a simple batten/plank) and then trimming that array to a precise architectural boundary (like a sloped gable roof) using a `Boolean` modifier set to **Intersect**. The target of the intersect is a hidden, thickened proxy volume of the wall.
* **Why Use This Skill (Rationale)**: Manually cutting individual planks or battens to match a sloped roofline is destructive and tedious. If the roof pitch changes, manual cuts must be redone. By using a proxy volume intersection, the siding geometry is entirely procedural. Moving a single vertex on the proxy wall automatically updates the angles of every intersecting batten in real-time.
* **Overall Applicability**: Essential for architectural visualization, house exteriors, stylized cabins, sci-fi paneling, or any scenario where repeating linear elements must perfectly conform to a non-square boundary.
* **Value Addition**: Transforms a basic flat plane into rich, highly detailed 3D siding that casts realistic micro-shadows, complete with synchronized window/door cutouts across multiple separate objects.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Wall**: A flat planar mesh mapping out the profile of the wall (e.g., a 5-sided pentagon for a gable wall). Given a `Solidify` modifier to provide realistic thickness.
  - **Proxy Cutter**: A duplicate of the base wall mesh. Given an aggressively thick `Solidify` modifier to encapsulate the entire siding area. Hidden from render, displayed as wire bounds.
  - **Batten Siding**: A simple elongated cube representing a single vertical wood strip. Given an `Array` modifier for horizontal spacing, followed by a `Boolean (Intersect)` targeting the Proxy Cutter to shape the top.
  - **Window Cutouts**: A separate cube used as a Boolean (Difference) cutter applied to *both* the wall and the batten array simultaneously, ensuring perfectly aligned holes.

* **Step B: Materials & Shading**
  - Uses the `Principled BSDF`.
  - **Base Wall**: Painted wood finish. Slightly higher roughness (`0.9`), base color `(0.85, 0.85, 0.83)`.
  - **Battens**: Uses a subtly darker tint of the base wall `(0.8, 0.8, 0.78)` and slightly lower roughness (`0.8`) to create subtle visual separation and highlight the ambient occlusion between the boards.

* **Step C: Lighting & Rendering Context**
  - EEVEE or Cycles.
  - Works best with strong directional lighting (like a Sun light at a steep angle) to cast sharp shadows from the vertical battens across the flat wall surface, emphasizing the 3D geometry.

* **Step D: Animation & Dynamics**
  - N/A for animation, but highly parametric. Changing the `Array` spacing or modifying the base mesh vertices will update the entire facade procedurally.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Gable Wall Profile | `bmesh` creation | Allows exact parametric control over width and roof pitch (eaves/ridge height) |
| Wall Thickness | `Solidify` Modifier | Keeps the base mesh flat and easy to edit while providing realistic wall depth |
| Board & Batten Pattern | `Array` Modifier | Procedurally generates infinite instances without duplicating mesh data |
| Roofline Sloped Cuts | `Boolean` (Intersect) | Perfectly crops the rectangular array to the complex architectural shape of the proxy wall |
| Window Holes | `Boolean` (Difference) | Non-destructively punches aligned holes through multiple distinct objects at once |

> **Feasibility Assessment**: 100% reproducible. The tutorial's core workflow relies entirely on Blender's modifier stack, which translates perfectly into the Python API.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralSiding",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.85, 0.85, 0.83),  # Off-white house paint
    **kwargs,
) -> str:
    """
    Create a procedural Board and Batten wall using Proxy-Volume Boolean intersections.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) color of the wall.
        **kwargs: 
            wall_width (float): Total width of the wall.
            eave_height (float): Height of the wall at the edges.
            ridge_height (float): Peak height of the roof.
            batten_width (float): Width of vertical siding strips.
            batten_spacing (float): Distance between siding strips.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection

    # --- Parameters ---
    width = kwargs.get('wall_width', 6.0)
    eave_height = kwargs.get('eave_height', 3.0)
    ridge_height = kwargs.get('ridge_height', 5.0)
    batten_width = kwargs.get('batten_width', 0.06)
    batten_depth = kwargs.get('batten_depth', 0.03)
    batten_spacing = kwargs.get('batten_spacing', 0.4)
    
    window_size = kwargs.get('window_size', (1.2, 1.0, 1.5))
    window_loc = kwargs.get('window_loc', (width / 2.0, 0.0, eave_height * 0.5))

    # --- Materials ---
    mat_wall = bpy.data.materials.new(name=f"{object_name}_WallMat")
    mat_wall.use_nodes = True
    bsdf_wall = mat_wall.node_tree.nodes.get("Principled BSDF")
    if bsdf_wall:
        bsdf_wall.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf_wall.inputs["Roughness"].default_value = 0.9

    mat_batten = bpy.data.materials.new(name=f"{object_name}_BattenMat")
    mat_batten.use_nodes = True
    bsdf_batten = mat_batten.node_tree.nodes.get("Principled BSDF")
    if bsdf_batten:
        # Slightly darker for the battens to enhance ambient occlusion visually
        darker_tint = (material_color[0]*0.95, material_color[1]*0.95, material_color[2]*0.95)
        bsdf_batten.inputs["Base Color"].default_value = (*darker_tint, 1.0)
        bsdf_batten.inputs["Roughness"].default_value = 0.8

    # --- Master Empty ---
    master_empty = bpy.data.objects.new(object_name, None)
    master_empty.empty_display_type = 'ARROWS'
    master_empty.empty_display_size = 2.0
    collection.objects.link(master_empty)

    # --- Step 1: Base Wall Geometry (Flat Gable Profile) ---
    bm_wall = bmesh.new()
    v1 = bm_wall.verts.new((0, 0, 0))
    v2 = bm_wall.verts.new((width, 0, 0))
    v3 = bm_wall.verts.new((width, 0, eave_height))
    v4 = bm_wall.verts.new((width / 2.0, 0, ridge_height))
    v5 = bm_wall.verts.new((0, 0, eave_height))
    bm_wall.faces.new((v1, v2, v3, v4, v5))
    
    mesh_wall = bpy.data.meshes.new(f"{object_name}_ProfileMesh")
    bm_wall.to_mesh(mesh_wall)
    bm_wall.free()

    # --- Step 2: The Visual Background Wall ---
    wall_obj = bpy.data.objects.new(f"{object_name}_BackgroundWall", mesh_wall)
    wall_obj.data.materials.append(mat_wall)
    wall_obj.parent = master_empty
    collection.objects.link(wall_obj)
    
    mod_wall_solidify = wall_obj.modifiers.new(name="Thickness", type='SOLIDIFY')
    mod_wall_solidify.thickness = 0.1
    mod_wall_solidify.offset = 1.0  # Extrude backwards (positive Y) so front stays at Y=0

    # --- Step 3: The Proxy Cutter Volume ---
    # This acts as the boundary bounding box that crops the tall battens to the roofline
    proxy_cutter_obj = bpy.data.objects.new(f"{object_name}_ProxyCutter", mesh_wall)
    proxy_cutter_obj.parent = master_empty
    collection.objects.link(proxy_cutter_obj)
    
    mod_proxy_solidify = proxy_cutter_obj.modifiers.new(name="IntersectionVolume", type='SOLIDIFY')
    mod_proxy_solidify.thickness = batten_depth * 10.0  # Make it extremely thick
    mod_proxy_solidify.offset = 0.0  # Center it over Y=0 so it fully encapsulates the battens
    
    proxy_cutter_obj.display_type = 'WIRE'
    proxy_cutter_obj.hide_render = True

    # --- Step 4: The Batten Array ---
    bm_batten = bmesh.new()
    bmesh.ops.create_cube(bm_batten, size=1.0)
    # Scale to dimensions. Height is made taller than the ridge so it spans the whole proxy volume
    total_batten_height = ridge_height + 1.0
    bmesh.ops.scale(bm_batten, vec=(batten_width, batten_depth, total_batten_height), verts=bm_batten.verts)
    # Translate so bottom is at Z=0, and the back face sits against the wall (Y=0)
    bmesh.ops.translate(bm_batten, vec=(batten_width/2, -batten_depth/2, total_batten_height/2), verts=bm_batten.verts)
    
    mesh_batten = bpy.data.meshes.new(f"{object_name}_BattenMesh")
    bm_batten.to_mesh(mesh_batten)
    bm_batten.free()
    
    batten_obj = bpy.data.objects.new(f"{object_name}_Battens", mesh_batten)
    batten_obj.data.materials.append(mat_batten)
    batten_obj.parent = master_empty
    collection.objects.link(batten_obj)

    # Batten Modifier 1: Array horizontally
    mod_array = batten_obj.modifiers.new(name="HorizontalArray", type='ARRAY')
    mod_array.use_relative_offset = False
    mod_array.use_constant_offset = True
    mod_array.constant_offset_displace = (batten_spacing, 0, 0)
    mod_array.count = int(width / batten_spacing) + 1
    
    # Batten Modifier 2: Intersect with Proxy Volume (Cropping to Roofline)
    mod_bool_int = batten_obj.modifiers.new(name="CropToRoofline", type='BOOLEAN')
    mod_bool_int.operation = 'INTERSECT'
    mod_bool_int.object = proxy_cutter_obj
    mod_bool_int.solver = 'EXACT'

    # --- Step 5: Window Hole Cutter ---
    bm_win = bmesh.new()
    bmesh.ops.create_cube(bm_win, size=1.0)
    bmesh.ops.scale(bm_win, vec=window_size, verts=bm_win.verts)
    bmesh.ops.translate(bm_win, vec=window_loc, verts=bm_win.verts)
    
    mesh_win = bpy.data.meshes.new(f"{object_name}_WindowCutterMesh")
    bm_win.to_mesh(mesh_win)
    bm_win.free()
    
    win_cutter_obj = bpy.data.objects.new(f"{object_name}_WindowCutter", mesh_win)
    win_cutter_obj.parent = master_empty
    collection.objects.link(win_cutter_obj)
    
    win_cutter_obj.display_type = 'WIRE'
    win_cutter_obj.hide_render = True
    
    # Punch hole in the background wall
    mod_wall_diff = wall_obj.modifiers.new(name="CutWindow", type='BOOLEAN')
    mod_wall_diff.operation = 'DIFFERENCE'
    mod_wall_diff.object = win_cutter_obj
    mod_wall_diff.solver = 'EXACT'
    
    # Punch hole in the battens
    mod_batten_diff = batten_obj.modifiers.new(name="CutWindow", type='BOOLEAN')
    mod_batten_diff.operation = 'DIFFERENCE'
    mod_batten_diff.object = win_cutter_obj
    mod_batten_diff.solver = 'EXACT'

    # --- Finalize Transforms ---
    master_empty.location = Vector(location)
    master_empty.scale = (scale, scale, scale)

    return f"Created Procedural Siding System '{object_name}' at {location} (Includes Wall, Battens, Proxy Volume, and Window Cutter)"
```