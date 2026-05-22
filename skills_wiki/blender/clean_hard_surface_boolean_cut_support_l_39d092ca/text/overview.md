# Clean Hard-Surface Boolean Cut (Support Loop Technique)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Clean Hard-Surface Boolean Cut (Support Loop Technique)

* **Core Visual Mechanism**: Performing a non-destructive Difference Boolean operation on a curved surface using a high-density "cutter" object. By adding perpendicular loop cuts along the cutter's geometry, the resulting intersection creates a dense, localized perimeter of vertices. This bounds the inevitable N-gons, preventing them from stretching across the curved base geometry and breaking the shading.
* **Why Use This Skill (Rationale)**: Booleans on curved surfaces (like cylinders or spheres) natively produce long, stretched N-gons. Because standard rendering calculates vertex normals based on face data, these stretched N-gons cause ugly black gradients and artifacts (pinching). Adding support loops to both the base mesh and the cutter forces the Boolean solver to generate smaller, confined polygons at the intersection, preserving perfect curved surface normals.
* **Overall Applicability**: This is a fundamental workflow for hard-surface concept art, sci-fi props, mechs, weapons, and vehicle panels. It allows for complex, non-destructive detailing (cutouts, panel lines, ports) without requiring manual retopology.
* **Value Addition**: Transforms a messy, artifact-ridden boolean cut into a production-ready hard-surface detail. Coupled with a Bevel modifier and Weighted Normals, it produces a high-fidelity, CAD-like appearance purely procedurally within Blender.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A 64-segment cylinder. Extra edge loops are bisected along its height to increase density and contain N-gons.
  - **Cutter Mesh**: A thinner, longer 64-segment cylinder. Crucially, it has multiple loop cuts along its length. It is rotated 90 degrees to intersect the base mesh laterally.
  - **Modifiers (Base Mesh)**: 
    1. **Boolean (Difference)**: Set to `EXACT` solver to cleanly process the dense intersection.
    2. **Bevel**: Angle-limited (30 degrees) to catch the sharp boolean edges, creating a micro-bevel that catches light. `Harden Normals` is enabled.
    3. **Weighted Normal**: Set to `Keep Sharp`. This is the final polish step that corrects any remaining slight shading deviations, forcing the normals of the curved surface to remain parallel.

* **Step B: Materials & Shading**
  - **Shader Model**: Principled BSDF designed for a clean, milled metal or hard-surface plastic look.
  - **Colors & Values**: Base Color `(0.5, 0.6, 0.7)`, Metallic `0.8` (highly reflective), Roughness `0.3` (tight, sharp specular highlights to expose shading quality).
  - Smooth shading is enabled on all polygons to ensure the Boolean boundaries evaluate the vertex normals smoothly.

* **Step C: Lighting & Rendering Context**
  - **Lighting**: Best showcased with high-contrast studio lighting or an HDRI to reflect sharp light strips across the curve, validating that the boolean did not warp the surface reflections.
  - **Render Engine**: EEVEE or Cycles. The modifier stack resolves the shading at the geometry level, so it looks perfect in both.

* **Step D: Animation & Dynamics (if applicable)**
  - Since it is non-destructive, the cutter object is parented to the base object. The cutter can be animated (moving laterally or scaling) to create real-time animated mechanical cutaways.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base & Cutter Generation | `bmesh` with `bisect_plane` | Native primitives lack a "length segments" parameter. Using `bmesh` to programmatically slice the cylinder guarantees the support loops required for clean booleans. |
| The Cut | Boolean Modifier (Exact Solver) | Non-destructive, allowing the cutter to be hidden/moved. The Exact solver prevents coplanar artifacting. |
| Shading Correction | Bevel + Weighted Normal Modifiers | The standard combination for perfect hard-surface shading without destructive manual retopology. |

> **Feasibility Assessment**: 100% reproduction of the core principle. The code automatically generates the support geometry described in the video and sets up the complete non-destructive modifier stack to output artifact-free shading.

#### 3b. Complete Reproduction Code

```python
def create_clean_boolean_cut(
    scene_name: str = "Scene",
    object_name: str = "HS_Boolean_Part",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.5, 0.6, 0.7),
    cutter_loops: int = 20,
    **kwargs
) -> str:
    """
    Create a clean hard-surface boolean cut on a curved surface.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created base object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the hard-surface material.
        cutter_loops: Number of support loops added to the cutter to fix shading.
        
    Returns:
        Status string confirming creation.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    def create_looped_cylinder(name, radius, depth, segments, loop_cuts):
        """Helper function to create a cylinder with perpendicular loop cuts."""
        mesh = bpy.data.meshes.new(name)
        bm = bmesh.new()
        bmesh.ops.create_cone(
            bm, cap_ends=True, cap_tris=False, 
            segments=segments, diameter1=radius*2, diameter2=radius*2, depth=depth
        )
        
        # Iteratively slice the mesh to create support loops
        if loop_cuts > 0:
            step = depth / (loop_cuts + 1)
            for i in range(1, loop_cuts + 1):
                z_pos = -depth/2 + i * step
                # Re-query geometry each iteration to ensure we slice the newly created faces
                geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
                bmesh.ops.bisect_plane(bm, geom=geom, plane_co=(0, 0, z_pos), plane_no=(0, 0, 1))
                
        bm.to_mesh(mesh)
        bm.free()
        
        # Enable smooth shading on all faces
        for poly in mesh.polygons:
            poly.use_smooth = True
            
        obj = bpy.data.objects.new(name, mesh)
        return obj

    # === Step 1: Create Base Geometry (with support loops) ===
    base_obj = create_looped_cylinder(object_name, radius=1.0, depth=2.0, segments=64, loop_cuts=10)
    scene.collection.objects.link(base_obj)

    # === Step 2: Create Cutter Geometry (with dense support loops) ===
    cutter_obj = create_looped_cylinder(f"{object_name}_Cutter", radius=0.4, depth=3.0, segments=64, loop_cuts=cutter_loops)
    
    # Organize Cutter into a dedicated, hidden collection to keep the viewport clean
    cutters_coll = bpy.data.collections.get("Cutters")
    if not cutters_coll:
        cutters_coll = bpy.data.collections.new("Cutters")
        scene.collection.children.link(cutters_coll)
        cutters_coll.hide_viewport = True
        cutters_coll.hide_render = True
    cutters_coll.objects.link(cutter_obj)

    # === Step 3: Position and Parent Cutter ===
    # Rotate 90 degrees on X to punch through the side of the base cylinder
    cutter_obj.rotation_euler = (math.pi / 2, 0, 0)
    cutter_obj.parent = base_obj # Parent ensures cutter moves if the base is moved

    # === Step 4: Apply Modifier Stack ===
    # 4a. Boolean Cut
    bool_mod = base_obj.modifiers.new(name="Boolean", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = cutter_obj
    bool_mod.solver = 'EXACT'

    # Handle Auto Smooth deprecation safely for older vs newer Blender versions
    if hasattr(base_obj.data, "use_auto_smooth"):
        base_obj.data.use_auto_smooth = True
        base_obj.data.auto_smooth_angle = math.radians(60)

    # 4b. Hard Surface Micro-Bevel
    bevel_mod = base_obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel_mod.limit_method = 'ANGLE'
    bevel_mod.angle_limit = math.radians(30)
    bevel_mod.width = 0.02
    bevel_mod.segments = 3
    if hasattr(bevel_mod, "harden_normals"):
        bevel_mod.harden_normals = True

    # 4c. Weighted Normal to perfectly flatten shading on the curved surface
    wn_mod = base_obj.modifiers.new(name="WeightedNormal", type='WEIGHTED_NORMAL')
    wn_mod.keep_sharp = True

    # === Step 5: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = material_color + (1.0,) # RGBA
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = 0.8
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = 0.3
    base_obj.data.materials.append(mat)

    # === Step 6: Finalize Transform ===
    base_obj.location = Vector(location)
    base_obj.scale = (scale, scale, scale)

    return f"Created clean boolean object '{object_name}' at {location} utilizing non-destructive loop-cut cutter."
```