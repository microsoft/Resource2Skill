def create_box_projected_prop(
    scene_name: str = "Scene",
    object_name: str = "BoxProjectedProp",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.4, 0.1),
    blend_amount: float = 0.25,
    **kwargs,
) -> str:
    """
    Create a complex hard-surface prop textured seamlessly without UVs using Box Projection.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) tint multiplied over the projected texture.
        blend_amount: How much the X, Y, Z box projection planes blend at the seams.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    bm = bmesh.new()
    # Create base disc
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=32, radius1=1.5, radius2=1.5, depth=0.2)
    bmesh.ops.translate(bm, vec=(0, 0, 0.1), verts=bm.verts) # Set base at Z=0

    # Step 1: First extrusion
    top_faces = [f for f in bm.faces if f.normal.z > 0.9]
    bmesh.ops.inset_region(bm, faces=top_faces, thickness=0.5)
    ret_ext = bmesh.ops.extrude_face_region(bm, geom=top_faces)
    verts = [e for e in ret_ext['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, 0.4), verts=verts) 

    # Step 2: Second extrusion
    bm.faces.ensure_lookup_table()
    top_faces = [f for f in bm.faces if f.calc_center_median().z > 0.4 and f.normal.z > 0.9]
    bmesh.ops.inset_region(bm, faces=top_faces, thickness=0.4)
    ret_ext2 = bmesh.ops.extrude_face_region(bm, geom=top_faces)
    verts2 = [e for e in ret_ext2['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, 0.5), verts=verts2)

    # Step 3: Inner inset hole (extruding down)
    bm.faces.ensure_lookup_table()
    top_faces = [f for f in bm.faces if f.calc_center_median().z > 0.9 and f.normal.z > 0.9]
    bmesh.ops.inset_region(bm, faces=top_faces, thickness=0.2)
    ret_ext3 = bmesh.ops.extrude_face_region(bm, geom=top_faces)
    verts3 = [e for e in ret_ext3['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, -0.6), verts=verts3) 

    # Write bmesh to object
    mesh = bpy.data.meshes.new(object_name)
    bm.to_mesh(mesh)
    bm.free()

    # Shade Smooth
    for p in mesh.polygons:
        p.use_smooth = True

    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # Add Modifiers
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.segments = 3
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = 0.5 # approx 28 degrees
    bevel.width = 0.05

    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 3

    # === Step 2: Build Box-Projected Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (800, 0)

    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (500, 0)
    bsdf_node.inputs['Roughness'].default_value = 0.65

    mix_node = nodes.new('ShaderNodeMixRGB')
    mix_node.location = (250, 0)
    mix_node.blend_type = 'MULTIPLY'
    mix_node.inputs[0].default_value = 1.0
    mix_node.inputs[2].default_value = (*material_color, 1.0)

    tex_node = nodes.new('ShaderNodeTexImage')
    tex_node.location = (0, 0)
    tex_node.projection = 'BOX'
    tex_node.projection_blend = blend_amount

    # Generate a dummy grid texture to clearly demonstrate the Box Projection
    img_name = f"{object_name}_GeneratedGrid"
    if img_name in bpy.data.images:
        img = bpy.data.images[img_name]
    else:
        img = bpy.data.images.new(img_name, 1024, 1024, alpha=False)
        img.generated_type = 'COLOR_GRID'
    tex_node.image = img

    map_node = nodes.new('ShaderNodeMapping')
    map_node.location = (-200, 0)
    map_node.inputs['Scale'].default_value = (2.0, 2.0, 2.0)

    tc_node = nodes.new('ShaderNodeTexCoord')
    tc_node.location = (-400, 0)

    # Connect Nodes
    links.new(tc_node.outputs['Object'], map_node.inputs['Vector'])
    links.new(map_node.outputs['Vector'], tex_node.inputs['Vector'])
    links.new(tex_node.outputs['Color'], mix_node.inputs[1])
    links.new(mix_node.outputs['Color'], bsdf_node.inputs['Base Color'])
    links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])

    obj.data.materials.append(mat)

    # === Step 3: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' with seamlessly blended Box Projected materials at {location}"
