# Procedural Hard Surface Panel Splitting

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Hard Surface Panel Splitting

* **Core Visual Mechanism**: Creating intricate, perfectly flush panel cutouts and access hatches on curved 3D surfaces. The signature of this technique is the identical curvature continuity between the base object and the inset panel piece, separated by a crisp, uniform bevel gap that catches edge highlights. 
* **Why Use This Skill (Rationale)**: Traditional modeling of panel cuts on curved surfaces requires complex retopology and carefully matching edge flow to avoid pinching when subdivided. This non-destructive Boolean approach bypasses topology issues completely. By using the exact same cutter shape for both a `Difference` cut (on the main hull) and an `Intersect` cut (on a duplicate hull), the resulting pieces physically interlock like real-world manufactured parts with guaranteed 100% surface curvature continuity.
* **Overall Applicability**: Essential for Hard Surface, Sci-Fi, and mechanical modeling. Perfect for detailing spaceship hulls, mech armor plates, weapon chassis, and industrial product casings where modular panels conform to an aerodynamic or ergonomic outer shell.
* **Value Addition**: Transforms a basic primitive into a manufactured, engineered object. The procedural gap created by the opposing bevels adds micro-shadows (ambient occlusion) and specular highlights, instantly increasing the perceived polygon scale and realism of the model without manual vertex pushing.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A standard high-segment cylinder (e.g., 64 sides to represent a smooth curve). 
  - **Cutter Mesh**: A distinct object (often a cube or union of cubes) positioned so it penetrates the outer surface of the base mesh.
  - **Modifiers**: 
    - The Base Object receives a `Boolean (Difference)` to hollow out the panel cavity.
    - A Duplicate Object receives a `Boolean (Intersect)` to become the physical panel itself.
    - Both receive a `Bevel` modifier limited by Angle (approx 30°). This rounds the sharp Boolean cuts while leaving the flat faces untouched, creating a realistic mechanical gap.
* **Step B: Materials & Shading**
  - Smooth shading is enabled on the meshes.
  - `Harden Normals` is enabled within the Bevel modifiers to prevent the procedural boolean geometry from creating bad shading gradients on the curved faces.
  - A metallic Principled BSDF shader (High metallic, mid-roughness) to accentuate the edge highlights caught by the bevel gaps.
* **Step C: Lighting & Rendering Context**
  - High-contrast studio lighting or HDRI environments heavily complement this technique, as the small bevel gaps thrive on catching harsh glints of light against shadow. EEVEE or Cycles both handle the geometry perfectly.
* **Step D: Animation & Dynamics**
  - Because the workflow relies on live Modifiers, the Cutter object can be animated (moving across the surface), and the panel cut will procedurally update and slide along the hull in real-time.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Geometry Base & Cutters | `bmesh` primitives | Bypasses `bpy.ops` context reliance; ensures clean, mathematically precise geometry generation. |
| Curvature Matching | Object Duplication + Boolean Modifiers | Non-destructive. A Difference on the base and an Intersect on the duplicate perfectly creates matching puzzle pieces. |
| Panel Gaps & Shading | Bevel Modifier + Harden Normals | Automatically catches sharp boolean edges and bevels them to create a realistic manufactured seam without manual retopology. |

> **Feasibility Assessment**: 100% reproduction. The procedural modifier stack perfectly recreates the workflow demonstrated in the video natively via Python.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralPanelCut",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.3, 0.35, 0.4),
    **kwargs,
) -> str:
    """
    Creates a perfectly curved, non-destructive panel cut on a cylinder using boolean intersections.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created object hierarchy.
        location: (x, y, z) position of the assembly.
        scale: Uniform scale of the entire assembly.
        material_color: (R, G, B) color for the metallic hull.
        
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    # Get target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # 1. Create Parent Empty
    parent_empty = bpy.data.objects.new(object_name, None)
    scene.collection.objects.link(parent_empty)
    parent_empty.location = Vector(location)
    parent_empty.scale = (scale, scale, scale)

    # 2. Build Base Cylinder Mesh (64 segments for smooth curvature)
    base_mesh = bpy.data.meshes.new(f"{object_name}_Base_Mesh")
    bm_base = bmesh.new()
    bmesh.ops.create_cone(
        bm_base, cap_ends=True, cap_tris=False, 
        segments=64, radius1=1.0, radius2=1.0, depth=2.0
    )
    bm_base.to_mesh(base_mesh)
    bm_base.free()

    # Apply smooth shading configuration
    for poly in base_mesh.polygons:
        poly.use_smooth = True
    if hasattr(base_mesh, "use_auto_smooth"):
        base_mesh.use_auto_smooth = True
        base_mesh.auto_smooth_angle = 1.047 # 60 degrees

    # 3. Create the Main Hull Object and Panel Object
    base_obj = bpy.data.objects.new(f"{object_name}_Hull", base_mesh)
    scene.collection.objects.link(base_obj)
    base_obj.parent = parent_empty

    # The panel piece uses a direct copy of the base mesh to guarantee identical starting curvature
    panel_mesh = base_mesh.copy()
    panel_mesh.name = f"{object_name}_Panel_Mesh"
    panel_obj = bpy.data.objects.new(f"{object_name}_Panel", panel_mesh)
    scene.collection.objects.link(panel_obj)
    panel_obj.parent = parent_empty

    # 4. Build the Cutter Mesh (A T-shaped composite block)
    cutter_mesh = bpy.data.meshes.new(f"{object_name}_Cutter_Mesh")
    bm_cutter = bmesh.new()
    
    # First intersecting block
    ret1 = bmesh.ops.create_cube(bm_cutter, size=1.0)
    for v in ret1['verts']:
        v.co.x *= 0.8   # Width
        v.co.y *= 0.6   # Depth
        v.co.z *= 0.8   # Height
        v.co.y -= 0.8   # Push forward to intersect outer cylinder wall
        v.co.z += 0.2   # Offset vertically
        
    # Second intersecting block (creates a more complex T-shaped cut)
    ret2 = bmesh.ops.create_cube(bm_cutter, size=1.0)
    for v in ret2['verts']:
        v.co.x *= 0.5   
        v.co.y *= 0.6   
        v.co.z *= 0.4   
        v.co.y -= 0.8   
        v.co.z += 0.8   
        
    bm_cutter.to_mesh(cutter_mesh)
    bm_cutter.free()
    
    cutter_obj = bpy.data.objects.new(f"{object_name}_Cutter", cutter_mesh)
    scene.collection.objects.link(cutter_obj)
    cutter_obj.parent = parent_empty
    
    # Hide the cutter from normal view
    cutter_obj.display_type = 'WIRE'
    cutter_obj.hide_render = True
    cutter_obj.hide_viewport = True

    # 5. Apply Non-Destructive Modifiers
    # Cut a hole in the Main Hull
    mod_diff = base_obj.modifiers.new(name="Cutout", type='BOOLEAN')
    mod_diff.operation = 'DIFFERENCE'
    mod_diff.object = cutter_obj
    mod_diff.solver = 'EXACT'

    # Extract the matching panel piece from the Duplicate Hull
    mod_int = panel_obj.modifiers.new(name="PanelPiece", type='BOOLEAN')
    mod_int.operation = 'INTERSECT'
    mod_int.object = cutter_obj
    mod_int.solver = 'EXACT'

    # Add Bevel to the base to create the outer edge of the panel gap
    bev_base = base_obj.modifiers.new(name="PanelGap", type='BEVEL')
    bev_base.segments = 3
    bev_base.width = 0.015
    bev_base.limit_method = 'ANGLE'
    bev_base.angle_limit = 0.523 # 30 degrees
    bev_base.harden_normals = True

    # Add Bevel to the panel piece to create the inner edge of the panel gap
    bev_panel = panel_obj.modifiers.new(name="PanelGap", type='BEVEL')
    bev_panel.segments = 3
    bev_panel.width = 0.015
    bev_panel.limit_method = 'ANGLE'
    bev_panel.angle_limit = 0.523
    bev_panel.harden_normals = True

    # 6. Create Material
    mat = bpy.data.materials.new(name=f"{object_name}_Metal")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = 0.85
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = 0.35

    base_obj.data.materials.append(mat)
    panel_obj.data.materials.append(mat)

    return f"Created '{object_name}' assembly at {location} utilizing 3 objects (Base, Panel, Cutter)."
```