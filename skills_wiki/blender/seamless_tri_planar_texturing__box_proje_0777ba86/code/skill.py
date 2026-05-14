def create_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjectedProp",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a complex stepped cylinder textured seamlessly using Box Projection Blending.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color tint in 0-1 range.
        **kwargs: Optional override for 'blend_amount' (default 0.2).

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    blend_amount = kwargs.get("blend_amount", 0.25)

    # === Step 1: Create Base Geometry using BMesh ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    
    # Create base cylinder (depth 0.5, radius 2.0)
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=32, radius1=2.0, radius2=2.0, depth=0.5)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, 0.25))

    # -- Create First Step --
    # Find the top-facing face
    top_face = next(f for f in bm.faces if f.normal.z > 0.9)
    # Inset inwards
    bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.8)
    
    # Extrude the inset face upwards
    ext1 = bmesh.ops.extrude_face_region(bm, geom=[top_face])
    ext1_faces = [e for e in ext1['geom'] if isinstance(e, bmesh.types.BMFace)]
    new_top1 = next(f for f in ext1_faces if f.normal.z > 0.5)
    bmesh.ops.translate(bm, verts=new_top1.verts, vec=(0, 0, 1.0))

    # -- Create Second Step --
    # Inset the new top face
    bmesh.ops.inset_region(bm, faces=[new_top1], thickness=0.5)
    
    # Extrude again
    ext2 = bmesh.ops.extrude_face_region(bm, geom=[new_top1])
    ext2_faces = [e for e in ext2['geom'] if isinstance(e, bmesh.types.BMFace)]
    new_top2 = next(f for f in ext2_faces if f.normal.z > 0.5)
    bmesh.ops.translate(bm, verts=new_top2.verts, vec=(0, 0, 1.0))

    # Finalize BMesh
    bm.to_mesh(mesh)
    bm.free()

    # Shade smooth
    for poly in mesh.polygons:
        poly.use_smooth = True

    # === Step 2: Modifiers for Hard Surface Detailing ===
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.segments = 3
    bevel.width = 0.05
    bevel.limit_method = 'ANGLE'

    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # === Step 3: Build Box Projection Material ===
    mat_name = object_name + "_Mat"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create mapping nodes
    tex_coord = nodes.new(type="ShaderNodeTexCoord")
    tex_coord.location = (-800, 0)

    mapping = nodes.new(type="ShaderNodeMapping")
    mapping.location = (-600, 0)
    mapping.inputs['Scale'].default_value = (4.0, 4.0, 4.0)

    # Generate a visible test grid image to demonstrate the projection
    tex_image = nodes.new(type="ShaderNodeTexImage")
    tex_image.location = (-400, 0)
    
    img_name = "BoxProjGrid_Demo"
    if img_name in bpy.data.images:
        img = bpy.data.images[img_name]
    else:
        img = bpy.data.images.new(img_name, width=1024, height=1024)
        img.generated_type = 'COLOR_GRID'
    tex_image.image = img

    # *** CORE SKILL: Set Projection to BOX and configure Blend ***
    tex_image.projection = 'BOX'
    tex_image.projection_blend = blend_amount

    # Mix node to tint the grid with the parameterized material_color
    mix_tint = nodes.new(type="ShaderNodeMixRGB")
    mix_tint.blend_type = 'MULTIPLY'
    mix_tint.location = (-150, 150)
    mix_tint.inputs[0].default_value = 1.0  # Factor
    mix_tint.inputs[2].default_value = (*material_color, 1.0)

    # Main Shader
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.location = (50, 0)
    bsdf.inputs['Metallic'].default_value = 0.7
    bsdf.inputs['Roughness'].default_value = 0.35

    output = nodes.new(type="ShaderNodeOutputMaterial")
    output.location = (300, 0)

    # Connect nodes
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], tex_image.inputs['Vector'])
    links.new(tex_image.outputs['Color'], mix_tint.inputs[1])
    links.new(mix_tint.outputs[0], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    obj.data.materials.append(mat)

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' with Box Projection Texturing at {location}. Adjust mapping node to scale texture."
