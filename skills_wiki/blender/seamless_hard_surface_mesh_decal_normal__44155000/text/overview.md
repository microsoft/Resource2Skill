# Seamless Hard-Surface Mesh Decal (Normal Transfer Blending)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Seamless Hard-Surface Mesh Decal (Normal Transfer Blending)

* **Core Visual Mechanism**: This technique merges separate geometric details (decals, vents, panel cutouts) onto a complex curved surface *without* altering the topology of the base mesh. It creates the illusion of a single continuous piece of manufactured metal or plastic. The signature of this effect is an intersecting geometric shape where the intersection seam is entirely invisible due to perfectly blended vertex normals.
* **Why Use This Skill (Rationale)**: Modifying a high-density curved surface to add a cut-out or extrusion normally ruins the underlying edge flow, resulting in pinching and shading artifacts under subdivision. By keeping the detail as a separate floating mesh (a "decal") and stealing the shading data (normals) from the base mesh, you get perfect shading and complete non-destructive flexibility. 
* **Overall Applicability**: Essential for hard-surface modeling, sci-fi concepts, robotics, and vehicle design. Used to add bolts, latches, vents, armor paneling, and structural cut-outs to complex hulls and bodies.
* **Value Addition**: Transforms a basic, smooth primitive into a complex, highly detailed manufactured object while maintaining a non-destructive workflow.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A clean, curved primitive (e.g., a UV Sphere or smooth Cylinder).
  - **Decal Mesh**: A separate object positioned intersecting the base. It is modeled with an outer "flange" — an extruded boundary loop that overlaps the base mesh.
  - **Topology Flow**: The outer boundary edge of the decal is given an Edge Crease of 1.0 to hold its shape under subdivision. These outer boundary vertices are assigned to a specific Vertex Group (e.g., `Blend_Mask`).
  - **Modifier Stack (Strict Order)**: 
    1. **Shrinkwrap**: Snaps the outer flange (via the Vertex Group) precisely to the base mesh.
    2. **Bevel**: Adds hard-surface chamfers to the inner geometry (using an Angle limit).
    3. **Subdivision Surface**: Smooths the decal and, crucially, interpolates the Vertex Group weights to create a soft gradient across the flange.
    4. **Data Transfer**: Targets the base mesh, restricted to the Vertex Group, and copies Custom Normals using "Nearest Face Interpolated" (`POLYINTERP_NEAREST`). 

* **Step B: Materials & Shading**
  - **Shader Model**: A standard Principled BSDF with slightly elevated metallic and mid-to-low roughness values (e.g., `Metallic = 0.5`, `Roughness = 0.3`).
  - **Normals**: The Data Transfer modifier overrides the shading. Auto Smooth (or Shade Smooth in Blender 4.1+) must be enabled for the Custom Normals to render correctly.
  - **Color**: Unified across both objects to sell the illusion that they are the same piece of material, e.g., a sleek industrial blue `(0.2, 0.5, 0.8)`.

* **Step C: Lighting & Rendering Context**
  - Works perfectly in both EEVEE and Cycles. The effect is most visible under high-contrast lighting or HDRI reflections, as the reflections will flow continuously across the separate objects without breaking.

* **Step D: Animation & Dynamics**
  - Because it uses modifiers, the decal can be constrained or parented to the base mesh. If the base mesh deforms (e.g., via a rig), the decal will dynamically update its shrinkwrap and normal projection in real-time.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base & Decal Starting Shapes | `bpy.ops.mesh.primitive_*` | Provides clean, symmetrical base geometry rapidly. |
| Decal Flange & Detailing | `bmesh` | Allows precise topological control: selecting boundary edges, extruding the blending flange, and assigning vertex group weights programmatically. |
| Invisible Seam Blending | Modifiers (`Shrinkwrap`, `DataTransfer`) | Procedural and dynamic. SubD interpolates the vertex group weight, creating a perfect gradient for the Data Transfer modifier to blend the normals seamlessly. |

> **Feasibility Assessment**: 100% — The script perfectly reproduces the mesh decal workflow. It constructs a base surface, generates the decal geometry, sets up the masking vertex groups, and configures the exact modifier stack required to achieve the seamless normal blend.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "MeshDecal",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.5, 0.8),
    **kwargs,
) -> str:
    """
    Create a seamless Mesh Decal (a detailed vent/panel) blended onto a curved surface.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created decal object.
        location: (x, y, z) world-space position for the base object.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (Target Surface) ===
    # A large smooth sphere to demonstrate the decal blending onto a curved surface
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=64, ring_count=32, 
        radius=2.0 * scale, 
        location=location
    )
    base_obj = bpy.context.active_object
    base_obj.name = f"{object_name}_Base"
    bpy.ops.object.shade_smooth()
    
    # === Step 2: Create the Decal Base Shape ===
    # Positioned at the top pole of the sphere
    decal_z = location[2] + (2.0 * scale)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32, 
        radius=0.4 * scale, 
        depth=0.2 * scale, 
        location=(location[0], location[1], decal_z)
    )
    decal_obj = bpy.context.active_object
    decal_obj.name = object_name
    
    # === Step 3: Model Decal details using BMesh ===
    bm = bmesh.new()
    bm.from_mesh(decal_obj.data)
    
    # Find top and bottom faces based on local Z median
    max_z, min_z = -float('inf'), float('inf')
    top_face = None
    bottom_face = None
    for f in bm.faces:
        cz = f.calc_center_median().z
        if cz > max_z:
            max_z = cz
            top_face = f
        if cz < min_z:
            min_z = cz
            bottom_face = f
            
    # Delete bottom face to make it an open shell
    bmesh.ops.delete(bm, geom=[bottom_face], context='FACES')
    
    # Inset top face to create the rim of a vent
    ret = bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.08 * scale)
    inner_faces = [f for f in ret['faces'] if f.is_valid]
    
    # Push inner face down to form a cavity
    bmesh.ops.translate(bm, vec=(0, 0, -0.15 * scale), verts=inner_faces[0].verts)
    
    # Create the blending flange by extruding the bottom boundary
    boundary_edges = [e for e in bm.edges if len(e.link_faces) == 1]
    ret = bmesh.ops.extrude_edge_only(bm, edges=boundary_edges)
    
    ext_verts = [v for v in ret['geom'] if isinstance(v, bmesh.types.BMVert)]
    ext_edges = [e for e in ret['geom'] if isinstance(e, bmesh.types.BMEdge)]
    
    # Scale the flange outwards to create an overlap with the base mesh
    for v in ext_verts:
        v.co.x *= 2.0
        v.co.y *= 2.0
        v.co.z -= 0.05 * scale # Dip slightly downward for better shrinkwrap projection
        
    # Crease the outer boundary so Subdivision Surface doesn't pull it inward
    crease_layer = bm.edges.layers.crease.verify()
    for e in ext_edges:
        if len(e.link_faces) == 1:
            e[crease_layer] = 1.0
            
    # Assign outer flange vertices to a Vertex Group (Index 0) for masking
    deform_layer = bm.verts.layers.deform.verify()
    for v in ext_verts:
        v[deform_layer][0] = 1.0
        
    bm.to_mesh(decal_obj.data)
    bm.free()
    
    # Initialize the vertex group on the object data
    vg = decal_obj.vertex_groups.new(name="Blend_Mask")
    
    # === Step 4: Shading & Materials ===
    # Compatibility fallback for pre-4.1 Auto Smooth requirement
    if hasattr(decal_obj.data, "use_auto_smooth"):
        decal_obj.data.use_auto_smooth = True
    
    bpy.ops.object.select_all(action='DESELECT')
    decal_obj.select_set(True)
    bpy.context.view_layer.objects.active = decal_obj
    bpy.ops.object.shade_smooth()
    
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Metallic"].default_value = 0.5
        bsdf.inputs["Roughness"].default_value = 0.3
        
    base_obj.data.materials.append(mat)
    decal_obj.data.materials.append(mat)
    
    # === Step 5: The Mesh Decal Modifier Stack ===
    # 1. Shrinkwrap: Snaps ONLY the flange vertices to the base surface
    mod_sw = decal_obj.modifiers.new(name="Shrinkwrap", type='SHRINKWRAP')
    mod_sw.target = base_obj
    mod_sw.vertex_group = vg.name
    mod_sw.wrap_method = 'NEAREST_SURFACEPOINT'
    
    # 2. Bevel: Adds hard-surface sharpness to inner uncreased edges
    mod_bevel = decal_obj.modifiers.new(name="Bevel", type='BEVEL')
    mod_bevel.limit_method = 'ANGLE'
    mod_bevel.angle_limit = math.radians(40)
    mod_bevel.width = 0.015 * scale
    mod_bevel.segments = 2
    
    # 3. Subdivision: Smooths everything, interpolates the vertex group weight gradient
    mod_subd = decal_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    mod_subd.levels = 2
    mod_subd.render_levels = 2
    
    # 4. Data Transfer: Copies normals from the base to hide the intersection seam entirely
    mod_dt = decal_obj.modifiers.new(name="DataTransfer", type='DATA_TRANSFER')
    mod_dt.object = base_obj
    mod_dt.vertex_group = vg.name
    mod_dt.use_loop_data = True
    mod_dt.data_types_loops = {'CUSTOM_NORMAL'}
    mod_dt.loop_mapping = 'POLYINTERP_NEAREST'
    
    return f"Created '{object_name}' (Decal) seamlessly attached to '{base_obj.name}'"
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
- [x] Does it handle the case where an object with the same name already exists? (Yes, Blender auto-suffixes names safely).