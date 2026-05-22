def create_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjectedPart",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a mechanical part textured via Triplanar/Box Projection in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color tint.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Material Setup (Triplanar / Box Projection) ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Outputs and Shaders
    node_out = nodes.new("ShaderNodeOutputMaterial")
    node_out.location = (800, 0)

    node_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    node_bsdf.location = (500, 0)
    node_bsdf.inputs['Metallic'].default_value = 0.7
    node_bsdf.inputs['Roughness'].default_value = 0.4
    links.new(node_bsdf.outputs[0], node_out.inputs[0])

    # Coordinate Mapping
    node_tex_coord = nodes.new("ShaderNodeTexCoord")
    node_tex_coord.location = (-600, 0)

    node_mapping = nodes.new("ShaderNodeMapping")
    node_mapping.location = (-400, 0)
    links.new(node_tex_coord.outputs['Object'], node_mapping.inputs['Vector'])

    # Internal Image Generation (Proves the seamless projection without external files)
    img_name = "BoxProj_TestGrid"
    if img_name in bpy.data.images:
        img = bpy.data.images[img_name]
    else:
        img = bpy.data.images.new(name=img_name, width=1024, height=1024)
        img.generated_type = 'COLOR_GRID'

    # The Core Technique: Box Projection Image Texture
    node_img = nodes.new("ShaderNodeTexImage")
    node_img.location = (-200, 0)
    node_img.image = img
    node_img.projection = 'BOX'
    node_img.projection_blend = 0.25  # Smooths the seams at sharp corners
    links.new(node_mapping.outputs['Vector'], node_img.inputs['Vector'])

    # Colorize the grid
    node_ramp = nodes.new("ShaderNodeValToRGB")
    node_ramp.location = (100, 0)
    node_ramp.color_ramp.elements[0].color = (0.1, 0.1, 0.1, 1.0) # Dark Iron
    node_ramp.color_ramp.elements[1].color = (*material_color, 1.0) # Paint/Rust Tint
    links.new(node_img.outputs['Color'], node_ramp.inputs['Fac'])
    links.new(node_ramp.outputs['Color'], node_bsdf.inputs['Base Color'])

    # Procedural Surface Bump
    node_noise = nodes.new("ShaderNodeTexNoise")
    node_noise.location = (-200, -300)
    node_noise.inputs['Scale'].default_value = 15.0
    node_noise.inputs['Detail'].default_value = 5.0
    links.new(node_mapping.outputs['Vector'], node_noise.inputs['Vector'])

    node_bump = nodes.new("ShaderNodeBump")
    node_bump.location = (100, -300)
    node_bump.inputs['Distance'].default_value = 0.05
    links.new(node_noise.outputs['Fac'], node_bump.inputs['Height'])
    links.new(node_bump.outputs['Normal'], node_bsdf.inputs['Normal'])

    # === Step 2: Mesh Generation ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()

    # Base cylinder
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=32,
        radius1=1.0,
        radius2=1.0,
        depth=0.5
    )

    # Find top face (normal pointing up)
    top_face = next(f for f in bm.faces if f.normal.z > 0.9)

    # First Tier (Inset & Extrude)
    bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3)
    ret = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    top_face = ret["faces"][0]
    bmesh.ops.translate(bm, vec=(0, 0, 0.4), verts=top_face.verts)

    # Second Tier (Inset & Extrude)
    bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.2)
    ret = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    top_face = ret["faces"][0]
    bmesh.ops.translate(bm, vec=(0, 0, 0.4), verts=top_face.verts)

    # Sharpen 90-degree edges using procedural bevel
    # Filter edges connected to exactly 2 faces with a sharp angle (> ~28 degrees)
    edges_to_bevel = [e for e in bm.edges if len(e.link_faces) == 2 and e.calc_face_angle() > 0.5]
    bmesh.ops.bevel(
        bm,
        geom=edges_to_bevel,
        offset=0.03,
        segments=3,
        profile=0.5
    )

    bm.to_mesh(mesh)
    bm.free()

    # === Step 3: Refinement & Positioning ===
    for poly in mesh.polygons:
        poly.use_smooth = True

    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 3
    subsurf.render_levels = 3

    obj.data.materials.append(mat)
    
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{obj.name}' mapped with Box Projection at {location}"
