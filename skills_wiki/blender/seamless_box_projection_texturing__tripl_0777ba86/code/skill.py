def create_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjectedPart",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.4, 0.1),
    **kwargs,
) -> str:
    """
    Create a mechanical part mapped with seamless Box Projection (Triplanar Mapping).

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry using BMesh ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    
    # 1. Base Cylinder
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=32, 
        radius1=1.0, radius2=1.0, depth=0.5
    )
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, 0.25))

    # Find the top face (pointing up along Z)
    top_face = next(f for f in bm.faces if f.normal.z > 0.9)

    # 2. Inset the top face
    bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3)

    # 3. Extrude the inset region upwards
    ret = bmesh.ops.extrude_face_region(bm, geom=[top_face])
    ext_verts = [e for e in ret['geom'] if isinstance(e, bmesh.types.BMVert)]
    ext_faces = [e for e in ret['geom'] if isinstance(e, bmesh.types.BMFace)]
    bmesh.ops.translate(bm, verts=ext_verts, vec=(0, 0, 0.4))

    # Find the newly extruded top face
    top_face_2 = next(f for f in ext_faces if f.normal.z > 0.9)

    # 4. Inset again
    bmesh.ops.inset_region(bm, faces=[top_face_2], thickness=0.3)

    # 5. Extrude downwards to create a hollow core
    ret2 = bmesh.ops.extrude_face_region(bm, geom=[top_face_2])
    ext_verts2 = [e for e in ret2['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=ext_verts2, vec=(0, 0, -0.3))

    bm.to_mesh(mesh)
    bm.free()

    # Shade smooth
    for poly in mesh.polygons:
        poly.use_smooth = True

    # === Step 2: Apply Modifiers ===
    # Bevel modifier to hold the sharp edges
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = 0.52  # ~30 degrees
    bevel.width = 0.03
    bevel.segments = 3

    # Subdivision modifier to round out the cylinder
    subsurf = obj.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # === Step 3: Build Box Projection Material ===
    mat = bpy.data.materials.new(name=object_name + "_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create Core Material Nodes
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.8
    
    out = nodes.new('ShaderNodeOutputMaterial')
    out.location = (300, 0)
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])

    # Generate an internal grid image to demonstrate the Box Projection
    img_name = "Box_Proj_Grid_Tex"
    img = bpy.data.images.get(img_name)
    if not img:
        img = bpy.data.images.new(name=img_name, width=1024, height=1024, alpha=False, generated_type='COLOR_GRID')

    # The Skill: Box Projected Image Texture
    tex_node = nodes.new('ShaderNodeTexImage')
    tex_node.image = img
    tex_node.projection = 'BOX'           # <-- Key concept
    tex_node.projection_blend = 0.25      # <-- Feathers the seams
    tex_node.location = (-600, 0)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-800, 0)
    mapping.inputs['Scale'].default_value = (3.0, 3.0, 3.0)

    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)

    # Use the grid as a Bump map and Roughness map to make the material look like manufactured metal
    cramp = nodes.new('ShaderNodeValToRGB')
    cramp.location = (-300, 100)
    cramp.color_ramp.elements[0].color = (0.2, 0.2, 0.2, 1.0)
    cramp.color_ramp.elements[1].color = (0.6, 0.6, 0.6, 1.0)

    bump = nodes.new('ShaderNodeBump')
    bump.location = (-300, -200)
    bump.inputs['Distance'].default_value = 0.05

    # Wire up the Triplanar Box Projection
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])  # <-- Object coordinates
    links.new(mapping.outputs['Vector'], tex_node.inputs['Vector'])
    
    links.new(tex_node.outputs['Color'], cramp.inputs['Fac'])
    links.new(cramp.outputs['Color'], bsdf.inputs['Roughness'])
    
    links.new(tex_node.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' demonstrating seamless Box Projection mapping at {location}"
