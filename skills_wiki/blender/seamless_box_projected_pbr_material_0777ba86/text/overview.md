# Agent_Skill_Distiller: 3D Modeling & Scene Design Pattern Extraction

### 1. High-level Design Pattern Extraction

> **Skill Name**: Seamless Box Projected PBR Material

* **Core Visual Mechanism**: Utilizing "Box Projection" (tri-planar mapping) within an Image Texture node, combined with a projection "Blend" value. This technique maps a 2D image seamlessly across a complex 3D shape from all six orthographic directions simultaneously, smoothing out the seams where the projections intersect, entirely bypassing the need for UV unwrapping.

* **Why Use This Skill (Rationale)**: Manually UV unwrapping complex, multi-tiered hard-surface objects with bevels and indentations is incredibly time-consuming and often results in texture stretching or visible seams. Box projection allows for instantaneous, seamless texturing. Furthermore, it is completely non-destructive—you can freely model, extrude, and alter the mesh geometry after the material is applied, and the texture will automatically adapt and re-project perfectly onto the new surfaces.

* **Overall Applicability**: Essential for rapid iteration workflows, environment design (architectural walls, ruins, sci-fi corridors), background props, and texturing complex hard-surface geometry where physical accuracy of UV seams is less important than speed and overall visual texture density.

* **Value Addition**: Transforms flat, untextured geometry into high-fidelity PBR objects instantly. It replaces hours of tedious UV unwrapping with a completely procedural, robust, and adaptable shading solution.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A dynamically generated multi-tiered cylindrical pedestal (created programmatically via BMesh to simulate the complex shape from the tutorial).
  - **Modifiers**: A Bevel modifier (set to Angle limit) is applied to sharpen specific edge transitions, followed by a Subdivision Surface modifier to create a high-quality, smooth hard-surface look. This exact stack simulates the high-res hard-surface workflow demonstrated in the video.

* **Step B: Materials & Shading**
  - **Shader Model**: Principled BSDF.
  - **Coordinates**: Uses `Texture Coordinate (Object)` to ensure the texture scales and moves with the object in 3D space, bypassing UVs.
  - **Core Technique**: The `ShaderNodeTexImage` is set to `BOX` projection instead of `FLAT`. The `projection_blend` value is set to `0.2` to feather the edges where the six projection planes meet.
  - **Textures**: To make this standalone and reproducible without external files, a Blender-generated `COLOR_GRID` image is automatically created to clearly visualize the projection mechanism. Procedural noise is layered into the Roughness and Normal (Bump) channels to mimic the worn, rough metal seen in the tutorial.

* **Step C: Lighting & Rendering Context**
  - Works equally well in EEVEE and Cycles. An HDRI or standard 3-point lighting setup is recommended to catch the procedural bump map and specular highlights.

* **Step D: Animation & Dynamics**
  - This is a static shading and modeling technique. However, because it uses Object coordinates, moving or deforming the object in an animation will cause the texture to "stick" perfectly to the surface, proving its robustness.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Complex Base Shape | `bmesh` with sequential extrusion/scaling | Allows procedural generation of a multi-tiered hard-surface shape specifically designed to be difficult to UV unwrap. |
| Edge Sharpening | Modifiers (Bevel + Subsurf) | Non-destructive way to recreate the sharp bevels shown in the tutorial. |
| Texture Projection | Shader Nodes (`ShaderNodeTexImage` Box Projection) | This is the exact core skill taught in the tutorial. A generated `COLOR_GRID` image visually proves the projection is working without needing external downloads. |

> **Feasibility Assessment**: 100% reproduction of the technique. While we use a generated grid and procedural bump instead of an external rusty metal texture file, the core skill—seamless Box Projection mapping on complex, un-unwrapped geometry—is perfectly implemented.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjectedProp",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a complex multi-tiered object with a Seamless Box Projected Material.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) color used (Note: Box projection overrides color with a grid pattern).
        **kwargs: blend_amount (float) - controls the edge blending of the box projection (default: 0.2).

    Returns:
        Status string describing the operation.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    blend_amount = kwargs.get("blend_amount", 0.2)

    # === Step 1: Create Complex Base Geometry via BMesh ===
    bm = bmesh.new()
    
    # Base Ring
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=32, radius1=1.0, radius2=1.0, depth=0.3)
    for v in bm.verts: 
        v.co.z += 0.15 # Rest on Z=0
        
    def extrude_and_transform(face, scale_vec=(1,1,1), translate_vec=(0,0,0)):
        """Helper to inset/extrude and grab the new top face."""
        ext = bmesh.ops.extrude_face_region(bm, geom=[face])
        new_faces = [f for f in ext['geom'] if isinstance(f, bmesh.types.BMFace)]
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        new_top = next(f for f in new_faces if f.normal.z > 0.5)
        
        if scale_vec != (1,1,1):
            bmesh.ops.scale(bm, vec=scale_vec, verts=new_top.verts)
        if translate_vec != (0,0,0):
            bmesh.ops.translate(bm, vec=translate_vec, verts=new_top.verts)
        return new_top

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    top_face = next(f for f in bm.faces if f.normal.z > 0.5)
    
    # Tier 2 (Raised platform)
    top_face = extrude_and_transform(top_face, scale_vec=(0.7, 0.7, 1.0)) # Inset
    top_face = extrude_and_transform(top_face, translate_vec=(0, 0, 0.3)) # Extrude Up
    
    # Tier 3 (Indent / Trench)
    top_face = extrude_and_transform(top_face, scale_vec=(0.6, 0.6, 1.0)) # Inset
    top_face = extrude_and_transform(top_face, translate_vec=(0, 0, -0.2)) # Extrude Down
    
    # Tier 4 (Center Post)
    top_face = extrude_and_transform(top_face, scale_vec=(0.5, 0.5, 1.0)) # Inset
    top_face = extrude_and_transform(top_face, translate_vec=(0, 0, 0.5)) # Extrude Up

    for f in bm.faces:
        f.smooth = True

    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # Apply Modifiers for hard-surface look
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(45)
    bevel.segments = 2
    bevel.width = 0.03

    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # === Step 2: Build Box Projected Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    for n in nodes: 
        nodes.remove(n)

    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1000, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (700, 0)
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (0, 0)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (200, 0)
    mapping.inputs['Scale'].default_value = (2.0, 2.0, 2.0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # Create a generated grid image to visualize the projection
    img_name = "BoxProjTexture_Generated"
    img = bpy.data.images.get(img_name)
    if not img:
        img = bpy.data.images.new(name=img_name, width=1024, height=1024, alpha=False, generated_type='COLOR_GRID')

    img_tex = nodes.new('ShaderNodeTexImage')
    img_tex.location = (400, 100)
    img_tex.image = img
    # THE CORE SKILL: Box projection and blending
    img_tex.projection = 'BOX'
    img_tex.projection_blend = blend_amount
    links.new(mapping.outputs['Vector'], img_tex.inputs['Vector'])
    
    # Layer procedural noise for surface wear/bump
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (200, -250)
    noise.inputs['Scale'].default_value = 20.0
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])

    bump = nodes.new('ShaderNodeBump')
    bump.location = (450, -250)
    bump.inputs['Distance'].default_value = 0.05
    links.new(noise.outputs['Fac'], bump.inputs['Height'])

    # Connect to Principled BSDF
    links.new(img_tex.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(noise.outputs['Fac'], bsdf.inputs['Roughness'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    # Assign material
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    # === Step 3: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created complex mesh '{obj.name}' at {location} utilizing Box Projection with {blend_amount} blend amount."
```