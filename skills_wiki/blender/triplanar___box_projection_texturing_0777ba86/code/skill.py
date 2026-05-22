def create_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjected_Asset",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a Box-Projected textured asset in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color tint.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (Stepped Cylinder) ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    
    # Base cylinder tier
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=32, radius1=1.5, radius2=1.5, depth=0.5)
    bmesh.ops.translate(bm, vec=(0, 0, 0.25), verts=bm.verts)

    # Inset & Extrude Tier 2
    top_face = next(f for f in bm.faces if f.normal.z > 0.9)
    bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.4)
    
    ret = bmesh.ops.extrude_face_region(bm, geom=[top_face])
    ext_verts = [v for v in ret['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, 0.6), verts=ext_verts)
    
    # Inset & Extrude Tier 3
    new_top = next(f for f in ret['geom'] if isinstance(f, bmesh.types.BMFace) and f.normal.z > 0.9)
    bmesh.ops.inset_region(bm, faces=[new_top], thickness=0.3)
    
    ret = bmesh.ops.extrude_face_region(bm, geom=[new_top])
    ext_verts = [v for v in ret['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, 0.4), verts=ext_verts)
    
    bm.to_mesh(mesh)
    bm.free()

    # Smooth shading
    for poly in mesh.polygons:
        poly.use_smooth = True

    # Add Bevel Modifier to round off harsh edges
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.segments = 3
    bevel.width = 0.05
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(30)

    # === Step 2: Build Material (Box Projection Setup) ===
    mat = bpy.data.materials.new(name=f"{object_name}_BoxMapMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Nodes
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (400, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (100, 0)
    bsdf.inputs['Roughness'].default_value = 0.4
    bsdf.inputs['Metallic'].default_value = 0.1

    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-700, 0)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-500, 0)
    mapping.inputs['Scale'].default_value = (3.0, 3.0, 3.0) 

    # Key node: Image Texture set to BOX projection
    img_tex = nodes.new('ShaderNodeTexImage')
    img_tex.location = (-300, 0)
    img_tex.projection = 'BOX'
    img_tex.projection_blend = 0.25  # Blends the projection seams
    
    # Create an internal generated image to visualize the projection mapping
    grid_img = bpy.data.images.new(name=f"{object_name}_Grid", width=1024, height=1024, alpha=False)
    grid_img.generated_type = 'COLOR_GRID'
    img_tex.image = grid_img

    # Blend the Grid with the requested material color
    try:
        # Blender 3.4+ Mix Node
        mix = nodes.new('ShaderNodeMix')
        mix.data_type = 'RGBA'
        mix.blend_type = 'MULTIPLY'
        mix.location = (-100, 0)
        mix.inputs['A'].default_value = (*material_color, 1.0)
        mix.inputs['Factor'].default_value = 1.0
        color_input = mix.inputs['B']
        mix_out = mix.outputs['Result']
    except Exception:
        # Legacy MixRGB Node fallback
        mix = nodes.new('ShaderNodeMixRGB')
        mix.blend_type = 'MULTIPLY'
        mix.location = (-100, 0)
        mix.inputs['Color1'].default_value = (*material_color, 1.0)
        mix.inputs['Fac'].default_value = 1.0
        color_input = mix.inputs['Color2']
        mix_out = mix.outputs['Color']

    # Link the Box Projection network
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], img_tex.inputs['Vector'])
    links.new(img_tex.outputs['Color'], color_input)
    links.new(mix_out, bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    obj.data.materials.append(mat)

    # === Step 3: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' with Triplanar Box Projection texturing at {location}"
