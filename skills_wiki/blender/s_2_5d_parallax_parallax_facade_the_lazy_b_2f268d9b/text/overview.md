# 2.5D Parallax Parallax Facade (The "Lazy" Building Generator)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: 2.5D Parallax Parallax Facade (The "Lazy" Building Generator)

* **Core Visual Mechanism**: The core technique relies on transforming a flat 2D plane into a "2.5D" surface by subdividing it into a grid, extruding the "window frames" outward (or recessing the window panes inward), and assigning a transparent/glossy material to the panes. A separate box with an emission material is placed behind the transparent panes to fake a deep, complex interior room. 
* **Why Use This Skill (Rationale)**: This is a cornerstone technique for creating massive, highly-detailed cityscapes with almost zero modeling effort (popularized by Ian Hubert's "Lazy Tutorials"). By faking the interior geometry using a simple emissive backdrop behind glossy glass, you achieve realistic parallax effects when the camera moves, creating the illusion of fully modeled rooms at a fraction of the polygon cost.
* **Overall Applicability**: Perfect for background assets in cyberpunk, urban, or night-time environments where hundreds of buildings are needed. It provides high visual impact for mid-to-background architectural elements without ballooning render times.
* **Value Addition**: Replaces heavy, fully modeled interior sets with extremely lightweight, procedural "hollow shells" that react correctly to lighting and camera movement.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Facade**: A flat plane subdivided into a uniform grid (e.g., 3x4). 
  - **Operation**: `bmesh.ops.inset_individual` is used to procedurally generate window frames and recess the inner window faces.
  - **Interior Box**: A simple primitive cube scaled to match the dimensions of the facade, positioned directly behind the recessed windows. 
  - **Polygon Budget**: Extremely low (under 50 faces per building module).

* **Step B: Materials & Shading**
  - **Wall Material**: A Principled BSDF with high roughness, representing brick or concrete. (Default: dark reddish-brown `(0.4, 0.15, 0.1)`).
  - **Glass Material**: A Mix Shader combining a `Glossy BSDF` (Roughness ~0.1) and a `Transparent BSDF`. The mix factor dictates how much of the interior light bleeds through. EEVEE requires `blend_method = 'HASHED'` for the transparency to work correctly.
  - **Interior Material**: An `Emission` shader applied to the interior box (Default: warm yellow `(1.0, 0.8, 0.4)` with a strength of 5.0) to simulate room lighting.

* **Step C: Lighting & Rendering Context**
  - Shines brightest in low-light/night environments where the emissive interiors provide the primary illumination (high contrast).
  - Works excellently in both EEVEE (fast viewport) and Cycles.
  - To enhance the illusion, adding an image texture of a room to the emission shader (instead of a flat color) creates hyper-realistic fake interiors.

* **Step D: Animation & Dynamics**
  - N/A for the base object, though flickering noise modifiers can be added to the interior Emission strength to simulate broken neon or TV lights.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Facade Grid & Recesses | `bmesh` with `inset_individual` | Programmatically creates frames and recessed panes in one operation, easily allowing separation of materials by tracking face indices. |
| Window Transparency | Mix Shader Node Tree (Glossy + Transp) | Perfectly mimics the video's custom shader setup, ensuring the emissive box behind it is visible while still catching world reflections. |
| Interior Depth | Separate Cube Object with Emission | Using a dedicated background geometry allows the parallax effect to work correctly as the camera moves past the building. |

> **Feasibility Assessment**: 90% reproduction. The script procedurally generates the 3D depth, material separation, and interior glowing box exactly as shown in the tutorial. The missing 10% is the reliance on a specific photographic texture (which requires external files), but the script uses procedural colors that can be instantly swapped for an image texture by the user.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "LazyBuilding",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.35, 0.15, 0.1),
    **kwargs,
) -> str:
    """
    Create a 2.5D Parallax Building Facade in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created building hierarchy.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the exterior wall.
        **kwargs: 
            grid_columns (int): Number of windows horizontally (default: 3)
            grid_rows (int): Number of windows vertically (default: 4)
            interior_color (tuple): RGB color for the interior emission (default: warm light)

    Returns:
        Status string confirming creation.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    # Extract kwargs
    grid_columns = kwargs.get('grid_columns', 3)
    grid_rows = kwargs.get('grid_rows', 4)
    interior_color = kwargs.get('interior_color', (1.0, 0.7, 0.3))

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    collection = scene.collection

    # ==========================================
    # Step 1: Create Materials
    # ==========================================
    
    # 1A. Wall Material
    mat_wall = bpy.data.materials.new(name=f"{object_name}_Wall")
    mat_wall.use_nodes = True
    wall_bsdf = mat_wall.node_tree.nodes.get("Principled BSDF")
    if wall_bsdf:
        wall_bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        wall_bsdf.inputs["Roughness"].default_value = 0.9

    # 1B. Glass Material (Mix of Glossy and Transparent)
    mat_glass = bpy.data.materials.new(name=f"{object_name}_Glass")
    mat_glass.use_nodes = True
    mat_glass.blend_method = 'HASHED'  # Crucial for EEVEE transparency
    mat_glass.shadow_method = 'NONE'
    
    nodes = mat_glass.node_tree.nodes
    links = mat_glass.node_tree.links
    nodes.clear()
    
    node_out = nodes.new(type='ShaderNodeOutputMaterial')
    node_mix = nodes.new(type='ShaderNodeMixShader')
    node_glossy = nodes.new(type='ShaderNodeBsdfGlossy')
    node_transp = nodes.new(type='ShaderNodeBsdfTransparent')
    
    node_glossy.inputs["Roughness"].default_value = 0.05
    node_mix.inputs["Fac"].default_value = 0.15 # 15% Glossy, 85% Transparent
    
    links.new(node_transp.outputs[0], node_mix.inputs[1])
    links.new(node_glossy.outputs[0], node_mix.inputs[2])
    links.new(node_mix.outputs[0], node_out.inputs[0])

    # 1C. Interior Emission Material
    mat_interior = bpy.data.materials.new(name=f"{object_name}_Interior")
    mat_interior.use_nodes = True
    int_nodes = mat_interior.node_tree.nodes
    int_links = mat_interior.node_tree.links
    int_nodes.clear()
    
    int_out = int_nodes.new(type='ShaderNodeOutputMaterial')
    int_emit = int_nodes.new(type='ShaderNodeEmission')
    int_emit.inputs["Color"].default_value = (*interior_color, 1.0)
    int_emit.inputs["Strength"].default_value = 5.0
    int_links.new(int_emit.outputs[0], int_out.inputs[0])

    # ==========================================
    # Step 2: Build Facade Geometry
    # ==========================================
    mesh_facade = bpy.data.meshes.new(f"{object_name}_Facade_Mesh")
    obj_facade = bpy.data.objects.new(f"{object_name}_Facade", mesh_facade)
    
    # Assign materials (Index 0: Wall, Index 1: Glass)
    mesh_facade.materials.append(mat_wall)
    mesh_facade.materials.append(mat_glass)

    bm = bmesh.new()
    
    # Generate Grid Vertices centered at origin
    for y in range(grid_rows + 1):
        for x in range(grid_columns + 1):
            cx = x - (grid_columns / 2.0)
            cy = y - (grid_rows / 2.0)
            bm.verts.new((cx, cy, 0))
    
    bm.verts.ensure_lookup_table()
    
    # Generate Grid Faces
    window_faces = []
    for y in range(grid_rows):
        for x in range(grid_columns):
            v1 = bm.verts[y * (grid_columns + 1) + x]
            v2 = bm.verts[y * (grid_columns + 1) + x + 1]
            v3 = bm.verts[(y + 1) * (grid_columns + 1) + x + 1]
            v4 = bm.verts[(y + 1) * (grid_columns + 1) + x]
            f = bm.faces.new((v1, v2, v3, v4))
            window_faces.append(f)
            
    # Inset to create frames and recessed windows
    # depth=-0.1 pushes the inner face along -Z relative to normal
    bmesh.ops.inset_individual(bm, faces=window_faces, thickness=0.15, depth=-0.15)
    
    # Assign material indices
    for f in bm.faces:
        if f in window_faces:
            f.material_index = 1  # The shrunken original faces become Glass
        else:
            f.material_index = 0  # The newly generated frames become Wall
            
    bm.to_mesh(mesh_facade)
    bm.free()

    # Rotate upright (Z becomes -Y, so facade faces forward (-Y))
    obj_facade.rotation_euler = (math.radians(90), 0, 0)

    # ==========================================
    # Step 3: Build Interior Emissive Box
    # ==========================================
    mesh_box = bpy.data.meshes.new(f"{object_name}_Interior_Mesh")
    obj_box = bpy.data.objects.new(f"{object_name}_Interior", mesh_box)
    mesh_box.materials.append(mat_interior)
    
    bm_box = bmesh.new()
    bmesh.ops.create_cube(bm_box, size=1.0)
    
    # Scale cube to match the back of the facade
    bmesh.ops.scale(bm_box, vec=(grid_columns, grid_rows, 1.0), verts=bm_box.verts)
    # Translate behind the recessed windows (Local Z = -0.7)
    bmesh.ops.translate(bm_box, vec=(0, 0, -0.7), verts=bm_box.verts)
    
    bm_box.to_mesh(mesh_box)
    bm_box.free()
    
    # Rotate upright to match facade
    obj_box.rotation_euler = (math.radians(90), 0, 0)

    # ==========================================
    # Step 4: Finalize Hierarchy
    # ==========================================
    parent_empty = bpy.data.objects.new(object_name, None)
    parent_empty.empty_display_type = 'ARROWS'
    parent_empty.empty_display_size = 2.0
    
    collection.objects.link(parent_empty)
    collection.objects.link(obj_facade)
    collection.objects.link(obj_box)
    
    obj_facade.parent = parent_empty
    obj_box.parent = parent_empty
    
    # Apply global transforms to the parent Empty
    parent_empty.location = Vector(location)
    parent_empty.scale = (scale, scale, scale)

    return f"Created '{object_name}' (Lazy Building) at {location} with {grid_columns}x{grid_rows} windows."
```

#### 3c. Verification Checklist

- [x] Does the code import all required modules INSIDE the function body?
- [x] Is it purely ADDITIVE (no scene clearing, no deleting existing objects)?
- [x] Does it set `obj.name = object_name` so the object is identifiable?
- [x] Are all color values explicit numeric tuples (not referencing undefined variables)?
- [x] Does it respect the `location` and `scale` parameters?
- [x] Does the function return a descriptive status string?
- [x] Would someone looking at the viewport say "yes, that is the technique from the tutorial"?
- [x] Does it avoid hardcoded file paths or external image dependencies?
- [x] Does it handle the case where an object with the same name already exists? (Yes, Blender's `.new()` automatically handles numerical appending without crashing).