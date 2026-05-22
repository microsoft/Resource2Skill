# Advanced Hard Surface Edge Control (Bevel Weight vs. Sharp vs. Crease)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Advanced Hard Surface Edge Control (Bevel Weight vs. Sharp vs. Crease)

* **Core Visual Mechanism**: This pattern defines how Blender calculates shading across surface transitions using explicit edge metadata (`Bevel Weight`, `Sharp`, and `Crease`). The signature technique involves creating a continuous, smooth bent surface by using **Bevel Weight** (to force a procedural bevel on a shallow geometric angle) while explicitly *omitting* **Mark Sharp**. This allows a downstream Weighted Normal modifier to calculate a seamless, mathematically smooth gradient across the bevel, rather than artificially splitting it.
* **Why Use This Skill (Rationale)**: 
  - **Bevel Weight vs Angle**: Relying purely on global Bevel Angle thresholds often misses shallow curves or accidentally bevels faceted details. `Bevel Weight` provides surgical control over exactly which edges receive fillets.
  - **Omitting Mark Sharp on Curves**: Marking an edge "Sharp" forces Blender to split the vertex normals at that edge. On a continuous, flowing curve, this creates an ugly "flexed" or stretched shading artifact when combined with a Weighted Normal modifier. Removing the Sharp mark restores a pristine, unified reflection.
  - **Crease Isolation**: It clarifies that edge `Crease` is exclusively used to tension the geometry of a Subdivision Surface modifier and has zero direct effect on normal calculations or auto-smoothing.
* **Overall Applicability**: Essential for hard surface modeling, mecha design, weapons, and industrial product visualization where objects feature a complex mix of sharp 90-degree cuts and shallow, continuous stamped/molded bends.
* **Value Addition**: Transforms shading from artifact-ridden to photorealistic, mimicking real-world stamped metal or molded plastic by perfectly controlling light falloff across fillets.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A low-poly solid block featuring a shallow geometric "ridge" (approx 22-degree angle) on the top surface.
  - **Edge Metadata**: 
    - *All* outer boundary edges (90 degrees) are marked `Sharp` and assigned `Bevel Weight = 1.0`.
    - The shallow ridge edge is assigned `Bevel Weight = 1.0` but is explicitly set to `Smooth` (Not Sharp).
  - **Modifiers**: 
    - `Bevel` (Limit Method: WEIGHT) generates fillets only on the edges explicitly tagged, allowing the shallow ridge to be beveled without lowering global angle thresholds.
    - `Weighted Normal` (Keep Sharp: True) fixes large flat Ngon shading and respects the sharp/smooth boundaries defined by the edge metadata.

* **Step B: Materials & Shading**
  - **Shader**: Principled BSDF dialed for highly reflective metal to expose any flaws in surface normal calculations.
  - **Properties**: Roughness `0.15`, Metallic `0.9`. 
  - The demo uses specific colors to denote workflow: User Color (Correct), Red (Incorrect Sharp Artifact), Blue (SubD Crease comparison).

* **Step C: Lighting & Rendering Context**
  - Shading artifacts are most visible in environments with clear reflections. High-contrast HDRIs or dramatic point lighting will immediately highlight the difference between a split normal and a continuous one. Works natively in both EEVEE and Cycles.

* **Step D: Animation & Dynamics**
  - N/A. This is a static topological and shading foundation.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Geometry Base | `bmesh` primitive construction | Allows exact placement of vertices to create the specific shallow angles required to demonstrate the edge limits. |
| Edge Tagging | `bmesh.edges` layers (`bevel_weight`, `crease`, `smooth`) | Programmatic assignment of metadata is the only way to independently control Bevel limits, Normal splitting, and SubD tension. |
| Shading Correction | `WeightedNormal` Modifier | Replicates the industry-standard HardOps/BoxCutter shading workflow for resolving Ngons on hard surface meshes. |

> **Feasibility Assessment**: 100% reproduction. The code generates a highly educational "Demo Kit" consisting of three objects that perfectly replicate the visual artifacts and solutions discussed in the tutorial regarding edge data types.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "HardSurface_EdgeControl",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.05, 0.8, 0.1),  # Default to Green for the "Correct" object
    **kwargs,
) -> str:
    """
    Create an Edge Control Demo Kit showcasing Bevel Weight, Sharp, and Crease.
    Generates 3 objects side-by-side to demonstrate correct vs incorrect shading workflows.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: Center world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) color for the correctly modeled central object.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    def assign_material(obj, color, name_suffix):
        mat_name = f"Mat_GlossyMetal_{name_suffix}"
        mat = bpy.data.materials.get(mat_name)
        if not mat:
            mat = bpy.data.materials.new(mat_name)
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                if "Base Color" in bsdf.inputs:
                    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
                bsdf.inputs["Roughness"].default_value = 0.15
                bsdf.inputs["Metallic"].default_value = 0.9
        
        if len(obj.data.materials) == 0:
            obj.data.materials.append(mat)
        else:
            obj.data.materials[0] = mat

    def create_bent_block(name, pos, obj_scale, mark_ridge_sharp=False):
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        scene.collection.objects.link(obj)

        bm = bmesh.new()
        
        # 1. Define Vertices for a thick block with a shallow top ridge
        verts = [
            bm.verts.new((-2, -1, 0)),    # 0: Front Bottom Left
            bm.verts.new(( 0, -1, 0.4)),  # 1: Front Ridge (Shallow Angle)
            bm.verts.new(( 2, -1, 0)),    # 2: Front Bottom Right
            bm.verts.new((-2,  1, 0)),    # 3: Back Bottom Left
            bm.verts.new(( 0,  1, 0.4)),  # 4: Back Ridge
            bm.verts.new(( 2,  1, 0)),    # 5: Back Bottom Right
            bm.verts.new((-2, -1, -1)),   # 6: Base Front Left
            bm.verts.new(( 2, -1, -1)),   # 7: Base Front Right
            bm.verts.new((-2,  1, -1)),   # 8: Base Back Left
            bm.verts.new(( 2,  1, -1))    # 9: Base Back Right
        ]
        
        # 2. Define Faces with correct counter-clockwise winding
        bm.faces.new([verts[0], verts[1], verts[4], verts[3]]) # Top Left
        bm.faces.new([verts[1], verts[2], verts[5], verts[4]]) # Top Right
        bm.faces.new([verts[0], verts[3], verts[8], verts[6]]) # Left
        bm.faces.new([verts[2], verts[7], verts[9], verts[5]]) # Right
        bm.faces.new([verts[6], verts[8], verts[9], verts[7]]) # Bottom
        bm.faces.new([verts[0], verts[6], verts[7], verts[2], verts[1]]) # Front Ngon
        bm.faces.new([verts[3], verts[4], verts[5], verts[9], verts[8]]) # Back Ngon

        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        bm.faces.ensure_lookup_table()

        # Set smooth shading for all faces
        for f in bm.faces:
            f.smooth = True

        bw_layer = bm.edges.layers.bevel_weight.verify()

        # Identify the shallow ridge edge
        ridge_edge = None
        for e in bm.edges:
            v_idx = {v.index for v in e.verts}
            if v_idx == {1, 4}:
                ridge_edge = e
                break

        # 3. Assign Edge Metadata based on topology
        for e in bm.edges:
            if len(e.link_faces) == 2:
                angle = e.calc_face_angle()
                
                # Assign Bevel Weight to ALL hard/semi-hard edges
                if angle > 0.05:
                    e[bw_layer] = 1.0

                if e == ridge_edge:
                    # THE CORE LESSON: Sharp on a continuous bevel causes shading artifacts.
                    e.smooth = not mark_ridge_sharp
                else:
                    # Outer boundary edges are ~90 degrees, they SHOULD be marked sharp
                    if angle > 1.0:
                        e.smooth = False
                    else:
                        e.smooth = True

        bm.to_mesh(mesh)
        bm.free()

        # 4. Modifiers
        bevel = obj.modifiers.new(name="Weight Bevel", type='BEVEL')
        bevel.limit_method = 'WEIGHT' # Drives bevel entirely by the bmesh weight layer
        bevel.width = 0.15
        bevel.segments = 4

        wnorm = obj.modifiers.new(name="WeightedNormal", type='WEIGHTED_NORMAL')
        wnorm.keep_sharp = True

        # Ensure explicit sharp edges are recognized (Standard fallback for various Blender versions)
        if hasattr(mesh, "use_auto_smooth"):
            mesh.use_auto_smooth = True
            mesh.auto_smooth_angle = math.radians(180) # Let explicit bmesh smooth=False handle splits

        obj.location = pos
        obj.scale = (obj_scale, obj_scale, obj_scale)
        return obj

    def create_crease_demo(name, pos, obj_scale, color):
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        scene.collection.objects.link(obj)

        bm = bmesh.new()
        bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False, segments=16, radius=1.5, depth=2.0)
        
        # THE CORE LESSON: Crease is exclusively for Subdivision Surface tension
        cr_layer = bm.edges.layers.crease.verify()
        for e in bm.edges:
            z0 = e.verts[0].co.z
            z1 = e.verts[1].co.z
            if (z0 > 0.9 and z1 > 0.9) or (z0 < -0.9 and z1 < -0.9):
                e[cr_layer] = 1.0

        for f in bm.faces:
            f.smooth = True

        bm.to_mesh(mesh)
        bm.free()

        subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
        subsurf.levels = 3
        subsurf.render_levels = 3

        if hasattr(mesh, "use_auto_smooth"):
            mesh.use_auto_smooth = True
            mesh.auto_smooth_angle = math.radians(180)

        obj.location = pos
        obj.scale = (obj_scale, obj_scale, obj_scale)
        assign_material(obj, color, "Crease")
        return obj

    # Execute and compose the demo kit
    loc = Vector(location)
    offset_dist = 5.0 * scale

    # Object 1: Correct Continuous Bevel Workflow (Center, Green)
    obj_correct = create_bent_block(f"{object_name}_Correct_Continuous", loc, scale, mark_ridge_sharp=False)
    assign_material(obj_correct, material_color, "Correct")

    # Object 2: Incorrect Artifact Workflow (Left, Red) - Shows the "flexing" artifact from the video
    obj_incorrect = create_bent_block(f"{object_name}_Incorrect_Artifact", loc + Vector((-offset_dist, 0, 0)), scale, mark_ridge_sharp=True)
    assign_material(obj_incorrect, (0.8, 0.05, 0.05), "Incorrect")

    # Object 3: SubD Crease Demonstration (Right, Blue)
    obj_crease = create_crease_demo(f"{object_name}_SubD_Crease", loc + Vector((offset_dist, 0, 0)), scale, (0.05, 0.1, 0.8))

    return f"Created Edge Control Demo Kit centered at {location}. Look at the specular reflections on the central ridge to see the workflow difference."
```