def create_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjected_Part",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.25, 0.1),
    **kwargs,
) -> str:
    """
    Create a mechanical part mapped with seamless Box Projection texturing.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color multiplier for the material.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Create Base Geometry ===
    mesh = bpy.data.meshes.new(name=f"{object_name}_mesh")
    obj = bpy.data.objects.new(name=object_name, object_data=mesh)
    scene.collection.objects.link(obj)

    # Use bmesh to procedurally construct the stepped cylinder
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=32, radius1=1.0, radius2=1.0, depth=0.5)
    bmesh.ops.translate(bm, vec=(0, 0, 0.25), verts=bm.verts) # Rest on floor

    # Level 1 Inset & Extrude
    top_face = max(bm.faces, key=lambda f: f.calc_center_median().z)
    bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3, use_even_offset=True)
    res = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    extruded_face = res['faces'][0]
    bmesh.ops.translate(bm, vec=(0, 0, 0.4), verts=extruded_face.verts)

    # Level 2 Inset & Extrude
    bmesh.ops.inset_region(bm, faces=[extruded_face], thickness=0.2, use_even_offset=True)
    res = bmesh.ops.extrude_discrete_faces(bm, faces=[extruded_face])
    extruded_face2 = res['faces'][0]
    bmesh.ops.translate(bm, vec=(0, 0, 0.3), verts=extruded_face2.verts)

    bm.to_mesh(mesh)
    bm.free()

    # Shade smooth
    for p in mesh.polygons:
        p.use_smooth = True

    # Procedural edge rounding modifiers
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = 0.5  # Approx 28 degrees; catches 90-degree edges
    bevel.width = 0.05
    bevel.segments = 3

    subsurf = obj.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 3

    # === Step 2: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Material")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (800, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (500, 0)
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    # Create an internal generated image to visualize the 2D projection
    img_name = "Box_Projection_Demo_Grid"
    img = bpy.data.images.get(img_name)
    if not img:
        img = bpy.data.images.new(img_name, width=1024, height=1024, alpha=False)
        img.generated_type = 'COLOR_GRID'

    # The Core Technique: Box Projection Image Node
    tex_img = nodes.new('ShaderNodeTexImage')
    tex_img.location = (100, 100)
    tex_img.image = img
    tex_img.projection = 'BOX'
    tex_img.projection_blend = 0.25  # Blends the seams at object corners

    # Tint the grid with the parameterized material color
    mix = nodes.new('ShaderNodeMixRGB')
    mix.location = (350, 100)
    mix.blend_type = 'MULTIPLY'
    mix.inputs[0].default_value = 0.8 # Factor
    mix.inputs[2].default_value = (*material_color, 1.0)
    links.new(tex_img.outputs['Color'], mix.inputs[1])
    links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])

    # Mapping based on local object space
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-100, 0)
    links.new(mapping.outputs['Vector'], tex_img.inputs['Vector'])

    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-300, 0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # Add 3D Procedural noise for PBR wear/bump (mimics tutorial visual fidelity)
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (100, -200)
    noise.inputs['Scale'].default_value = 4.0
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])

    bump = nodes.new('ShaderNodeBump')
    bump.location = (300, -200)
    bump.inputs['Distance'].default_value = 0.05
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    
    links.new(noise.outputs['Fac'], bsdf.inputs['Roughness'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    obj.data.materials.append(mat)

    # === Step 3: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))

    return f"Created '{object_name}' utilizing seamless Box Projection texturing at {location}."
