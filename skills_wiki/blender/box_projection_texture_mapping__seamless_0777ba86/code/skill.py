def create_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjectedFlange",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.3, 0.1),
    **kwargs,
) -> str:
    """
    Create a stepped mechanical flange featuring a Box-Projected material.
    This demonstrates seamless texturing without UV mapping.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color tint for the pattern.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (Stepped Flange) ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    
    # Base cylinder tier
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=32, radius1=1.0, radius2=1.0, depth=0.4)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, 0.2))
    
    # Inset and extrude middle tier
    top_faces = [f for f in bm.faces if f.normal.z > 0.9]
    ret = bmesh.ops.inset_region(bm, faces=top_faces, thickness=0.3)
    new_top = [f for f in ret['faces'] if f.normal.z > 0.9]
    ret_ext = bmesh.ops.extrude_face_region(bm, geom=new_top)
    ext_verts = [e for e in ret_ext['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=ext_verts, vec=(0, 0, 0.4))
    
    # Inset and extrude top tier
    top_faces = [f for f in bm.faces if f.normal.z > 0.9 and f.calc_center_bounds().z > 0.5]
    ret = bmesh.ops.inset_region(bm, faces=top_faces, thickness=0.3)
    new_top = [f for f in ret['faces'] if f.normal.z > 0.9]
    ret_ext = bmesh.ops.extrude_face_region(bm, geom=new_top)
    ext_verts = [e for e in ret_ext['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=ext_verts, vec=(0, 0, 0.4))

    # Apply smooth shading to the mesh
    for f in bm.faces:
        f.smooth = True

    bm.to_mesh(mesh)
    bm.free()

    # Modifiers to achieve the hard-surface blocky-but-smooth look
    bevel = obj.modifiers.new("Bevel", 'BEVEL')
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(30)
    bevel.width = 0.03
    bevel.segments = 2

    subdiv = obj.modifiers.new("Subdivision", 'SUBSURF')
    subdiv.levels = 2
    subdiv.render_levels = 2

    # === Step 2: Build Box-Projected Material ===
    mat = bpy.data.materials.new(name=object_name + "_Material")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (800, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (500, 0)
    bsdf.inputs['Roughness'].default_value = 0.6
    bsdf.inputs['Metallic'].default_value = 0.8
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    # The mapping setup bypassing UVs
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-400, 0)
    # Scale up the mapping so the pattern is dense enough to see the seams blend
    mapping.inputs['Scale'].default_value = (3.0, 3.0, 3.0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # Image Texture - THE CORE SKILL
    tex_image = nodes.new('ShaderNodeTexImage')
    tex_image.location = (-100, 0)
    tex_image.projection = 'BOX'           # Switch from Flat to Box Projection
    tex_image.projection_blend = 0.35      # Feather the seams between X, Y, Z axes
    
    # Generate a built-in grid image to visualize the box projection clearly
    img_name = "Box_Proj_Demo_Grid"
    img = bpy.data.images.get(img_name)
    if not img:
        img = bpy.data.images.new(img_name, width=1024, height=1024, alpha=False)
        img.generated_type = 'COLOR_GRID'
    tex_image.image = img

    links.new(mapping.outputs['Vector'], tex_image.inputs['Vector'])

    # Tint the generated pattern using the provided material_color parameter
    # Uses a fallback structure to support both older and newer Blender versions
    try:
        mix = nodes.new('ShaderNodeMix')
        mix.location = (200, 0)
        mix.data_type = 'RGBA'
        mix.blend_type = 'MULTIPLY'
        mix.inputs['Factor'].default_value = 0.85
        mix.inputs['A'].default_value = (material_color[0], material_color[1], material_color[2], 1.0)
        links.new(tex_image.outputs['Color'], mix.inputs['B'])
        links.new(mix.outputs['Result'], bsdf.inputs['Base Color'])
    except Exception:
        mix = nodes.new('ShaderNodeMixRGB')
        mix.location = (200, 0)
        mix.blend_type = 'MULTIPLY'
        mix.inputs['Fac'].default_value = 0.85
        mix.inputs['Color1'].default_value = (material_color[0], material_color[1], material_color[2], 1.0)
        links.new(tex_image.outputs['Color'], mix.inputs['Color2'])
        links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])

    # === Step 3: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' with Box Projection Material at {location}"
