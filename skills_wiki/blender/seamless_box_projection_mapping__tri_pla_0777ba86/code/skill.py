def create_object(
    scene_name: str = "Scene",
    object_name: str = "SeamlessBoxProjected_Part",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.25, 0.1),
    **kwargs,
) -> str:
    """
    Create a complex mechanical shape using Seamless Box Projection mapping.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color to tint the texture (default is a rust color).
        **kwargs: projection_blend (float) to adjust the texture seam blending.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    # Get scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Complex Base Geometry ===
    mesh = bpy.data.meshes.new(object_name)
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    
    # 1. Base flange
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=32, radius1=1.5, radius2=1.5, depth=0.4)
    top_face = next(f for f in bm.faces if f.normal.z > 0.9)

    # 2. Inset and Extrude UP (Inner Ring)
    bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.4)
    ret = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    top_face = ret['faces'][0]
    bmesh.ops.translate(bm, verts=top_face.verts, vec=(0, 0, 0.8))

    # 3. Inset and Extrude DOWN (Hollow center)
    bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3)
    ret = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    top_face = ret['faces'][0]
    bmesh.ops.translate(bm, verts=top_face.verts, vec=(0, 0, -0.6))

    # Shift geometry up so the origin sits at the bottom of the base
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, 0.2))

    for f in bm.faces:
        f.smooth = True

    bm.to_mesh(mesh)
    bm.free()

    # === Step 2: Modifiers for Hard Surface Polish ===
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(35)
    bevel.width = 0.04
    bevel.segments = 3

    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 3
    subsurf.render_levels = 3

    # === Step 3: Seamless Box Projection Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_BoxProjectMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create Core Nodes
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (400, 0)
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (700, 0)
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    texcoord = nodes.new('ShaderNodeTexCoord')
    texcoord.location = (-600, 0)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-400, 0)
    links.new(texcoord.outputs['Object'], mapping.inputs['Vector'])

    # Create a generated grid image to vividly demonstrate the box projection blending
    img_name = "BoxProject_Demonstrator_Grid"
    img = bpy.data.images.get(img_name)
    if not img:
        img = bpy.data.images.new(name=img_name, width=1024, height=1024, alpha=False, generated_type='COLOR_GRID')

    img_tex = nodes.new('ShaderNodeTexImage')
    img_tex.location = (-200, 0)
    img_tex.image = img
    
    # THE CORE SKILL: Box Projection & Blend
    img_tex.projection = 'BOX'
    img_tex.projection_blend = kwargs.get('projection_blend', 0.25)
    links.new(mapping.outputs['Vector'], img_tex.inputs['Vector'])

    # Tint the grid with the requested material_color
    if bpy.app.version >= (3, 4, 0):
        mix = nodes.new('ShaderNodeMix')
        mix.data_type = 'RGBA'
        mix.blend_type = 'MULTIPLY'
        mix.inputs['Factor'].default_value = 1.0
        mix.inputs['A'].default_value = (*material_color, 1.0)
        links.new(img_tex.outputs['Color'], mix.inputs['B'])
        links.new(mix.outputs['Result'], bsdf.inputs['Base Color'])
    else:
        mix = nodes.new('ShaderNodeMixRGB')
        mix.blend_type = 'MULTIPLY'
        mix.inputs['Fac'].default_value = 1.0
        mix.inputs['Color1'].default_value = (*material_color, 1.0)
        links.new(img_tex.outputs['Color'], mix.inputs['Color2'])
        links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])

    # Add some bump based on the texture to prove 3D mapping stability
    bump = nodes.new('ShaderNodeBump')
    bump.location = (100, -200)
    bump.inputs['Distance'].default_value = 0.05
    links.new(img_tex.outputs['Color'], bump.inputs['Height'])
    if 'Normal' in bsdf.inputs:
        links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    # Assign Material
    obj.data.materials.append(mat)

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' using Box Projection material mapping at {location}."
