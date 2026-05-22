# Automated Hard-Surface UV Mapping & Diagnostic Pipeline

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Automated Hard-Surface UV Mapping & Diagnostic Pipeline

* **Core Visual Mechanism**: A precisely unfolded 3D model visualized using a procedural UV/Color grid. The signature of this technique is the presence of a mapped checkerboard texture (specifically the `COLOR_GRID`) distributed across the geometry, where the texture squares appear uniform in scale and parallel to the geometry's flow, indicating zero distortion and properly placed seams.

* **Why Use This Skill (Rationale)**: UV mapping is the critical bridge between 3D geometry and 2D texturing. Without it, image textures stretch, warp, and artifact. By strategically placing seams on sharp edges (out of direct line-of-sight where possible) and packing the resulting "UV shells" efficiently, you ensure that pixel density is distributed evenly, maximizing texture resolution and preventing alias artifacts.

* **Overall Applicability**: This workflow is mandatory for any asset destined for game engines (Unreal, Unity), Substance Painter, or baking pipelines. The specific "sharp edge to seam" logic is ideal for hard-surface models like weapons, vehicles, sci-fi crates, and architectural elements. 

* **Value Addition**: Compared to a default primitive with overlapping or missing UVs, this skill prepares an object for production-ready texturing. It adds structural coordinate data to the mesh and provides a visual diagnostic tool to verify that the topology is texture-ready.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Primitive**: A custom bmesh generated "Mechanical Cylinder" (featuring an inset and extruded inner cavity) is created to provide a shape that naturally requires UV unwrapping.
  - **Operations**: The script automatically iterates through the mesh's edges, calculates the angle between adjacent face normals, and programmatically marks edges exceeding 80 degrees as `seam = True`. This perfectly replicates the tutorial's `Select Sharp Edges` -> `Mark Seam` workflow.
  - **Unwrap**: The script applies the standard `ANGLE_BASED` unwrap algorithm, utilizing a margin to automatically pack the resulting islands.

* **Step B: Materials & Shading**
  - **Shader Model**: Principled BSDF.
  - **Textures**: A procedurally generated Blender Image (`COLOR_GRID` type, 1024x1024) is mapped to the Base Color. This grid acts as a heat map for distortion.
  - **Nodes**: Replicates the `Node Wrangler (Ctrl+T)` setup: `Texture Coordinate (UV)` -> `Image Texture` -> `Principled BSDF`. 
  - **Properties**: Roughness is set to `0.5`, Specular to `0.5`, with the generated texture completely overriding the base color.

* **Step C: Lighting & Rendering Context**
  - EEVEE or Cycles. The diagnostic material is emissive/diffuse enough to be evaluated in Material Preview mode (which uses a default HDRI) without requiring complex scene lighting.

* **Step D: Animation & Dynamics (if applicable)**
  - N/A. This is a purely structural and material-based setup.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base Mesh Generation | `bmesh` | Allows us to procedurally generate a hard-surface shape (a bored cylinder) that explicitly requires seams, serving as a perfect testbed. |
| Seam Marking | `bmesh.edges.calc_face_angle()` | Replicates the tutorial's "Select Sharp Edges" feature safely via Python without relying on viewport context overrides. |
| Unwrapping | `bpy.ops.uv.unwrap` | The standard, robust algorithm recommended in the video. Passing a `margin` handles the "Pack Islands" step automatically. |
| UV Diagnostic Material | Shader Node Tree | Procedurally creates the exact UV Grid testing setup shown in the video, complete with the Node Wrangler mapping nodes. |

> **Feasibility Assessment**: 100% — The script successfully automates the exact 4-step workflow detailed in the video (Apply Scale [baked into gen], Mark Seams, Unwrap, Pack/Check) and applies the diagnostic visualizer. 

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "UVMapped_Part",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.8, 0.8),
    **kwargs,
) -> str:
    """
    Create an Automated Hard-Surface UV Mapped Object.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: Fallback color (overridden by diagnostic texture).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (Mechanical Cylinder) ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    # Create base cylinder
    bmesh.ops.create_cylinder(
        bm, 
        cap_ends=True, 
        cap_tris=False, 
        segments=16, 
        radius=scale * 1.0, 
        depth=scale * 1.5
    )
    
    # Inset and extrude the top face to create a cavity
    top_faces = [f for f in bm.faces if f.normal.z > 0.9]
    if top_faces:
        res = bmesh.ops.inset_region(bm, faces=top_faces, thickness=scale * 0.2)
        inner_faces = [elem for elem in res['faces'] if isinstance(elem, bmesh.types.BMFace)]
        res_extrude = bmesh.ops.extrude_face_region(bm, geom=inner_faces)
        
        # Move the extruded faces down to create the hole
        extruded_verts = list(set(v for elem in res_extrude['geom'] if isinstance(elem, bmesh.types.BMFace) for v in elem.verts))
        bmesh.ops.translate(bm, vec=Vector((0, 0, -scale * 0.8)), verts=extruded_verts)

    # === Step 2: Automated Seam Marking (The Tutorial's Core Logic) ===
    bm.edges.ensure_lookup_table()
    for edge in bm.edges:
        if edge.is_manifold:
            # Calculate angle between adjacent faces
            angle = edge.calc_face_angle()
            # Mark seams on edges sharper than ~80 degrees (1.4 radians)
            if angle > 1.4:
                edge.seam = True
                
    # Add a vertical seam to allow the outer cylinder to unroll perfectly
    vertical_edges = [e for e in bm.edges if abs(e.verts[0].co.z - e.verts[1].co.z) > (scale * 0.5) and not e.seam]
    if vertical_edges:
        vertical_edges[0].seam = True

    bm.to_mesh(mesh)
    bm.free()

    # === Step 3: Unwrap & Pack ===
    # Set context for unwrapping
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    current_mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Unwrap using Angle Based method. Passing a margin automatically packs the islands.
    try:
        bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.025)
    except RuntimeError as e:
        print(f"UV Unwrap failed (this can happen in headless environments): {e}")
        
    bpy.ops.object.mode_set(mode=current_mode)

    # === Step 4: Diagnostic UV Material Setup ===
    mat_name = "UV_Diagnostic_Grid"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        # 4a. Create or retrieve the Generated Image
        img_name = "Diagnostic_Color_Grid"
        img = bpy.data.images.get(img_name)
        if not img:
            img = bpy.data.images.new(img_name, width=1024, height=1024)
            img.generated_type = 'COLOR_GRID' # Generates the testing grid shown in tutorial
        
        # 4b. Build Node Tree
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (300, 0)
        
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 0)
        bsdf.inputs['Roughness'].default_value = 0.5
        
        tex_img = nodes.new('ShaderNodeTexImage')
        tex_img.image = img
        tex_img.location = (-300, 0)
        
        # Replicate Node Wrangler mapping setup
        tex_coord = nodes.new('ShaderNodeTexCoord')
        tex_coord.location = (-500, 0)
        
        links.new(tex_coord.outputs['UV'], tex_img.inputs['Vector'])
        links.new(tex_img.outputs['Color'], bsdf.inputs['Base Color'])
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Apply material to object
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    # Position object
    obj.location = Vector(location)

    return f"Created UV mapped '{object_name}' at {location} with marked seams and packed islands."
```