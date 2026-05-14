def create_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjectedProp",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a mechanical stepped prop demonstrating Seamless Box Projection Shading.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base tint applied over the projected grid.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated object and material.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry using bmesh Profile Spin ===
    mesh = bpy.data.meshes.new(name=object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()

    # Define a stepped profile resembling a mechanical flange
    verts_loc = [
        (0.0, 0.0, 0.0),
        (1.2, 0.0, 0.0),
        (1.2, 0.0, 0.2),
        (0.8, 0.0, 0.2),
        (0.8, 0.0, 0.5),
        (0.4, 0.0, 0.5),
        (0.4, 0.0, 0.9),
        (0.0, 0.0, 0.9)
    ]

    verts = [bm.verts.new(v) for v in verts_loc]
    edges = [bm.edges.new((verts[i], verts[i+1])) for i in range(len(verts)-1)]

    # Spin the profile 360 degrees around the Z axis
    bmesh.ops.spin(
        bm,
        geom=verts + edges,
        cent=(0.0, 0.0, 0.0),
        axis=(0.0, 0.0, 1.0),
        angle=2 * math.pi,
        steps=32,
        use_duplicate=False
    )

    # Clean up spin geometry (merge pole vertices and fix normals)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    # Apply smooth shading to all faces
    for face in bm.faces:
        face.smooth = True

    bm.to_mesh(mesh)
    bm.free()

    # === Step 2: Add Smoothing Modifiers ===
    # Bevel catches the 90-degree steps to protect them from subdivision collapse
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(30)
    bevel.segments = 3
    bevel.width = 0.05

    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # === Step 3: Setup Box Projected Material ===
    mat = bpy.data.materials.new(name=object_name + "_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out_node = nodes.new(type="ShaderNodeOutputMaterial")
    out_node.location = (800, 0)

    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.location = (500, 0)
    bsdf.inputs['Roughness'].default_value = 0.6
    bsdf.inputs['Metallic'].default_value = 0.5
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    # Generate an internal test image to visualize the seamless wrapping
    img_name = "BoxProj_TestPattern"
    tex_img = bpy.data.images.get(img_name)
    if not tex_img:
        tex_img = bpy.data.images.new(img_name, width=1024, height=1024, alpha=False)
        tex_img.generated_type = 'COLOR_GRID'

    img_node = nodes.new(type="ShaderNodeTexImage")
    img_node.location = (0, 0)
    img_node.image = tex_img
    
    # THE CORE TECHNIQUE: Change projection to 'BOX' and increase 'Blend'
    img_node.projection = 'BOX'
    img_node.projection_blend = 0.25

    # Object Texture Coordinates ensure scale/rotation consistency without UVs
    mapping = nodes.new(type="ShaderNodeMapping")
    mapping.location = (-200, 0)
    mapping.inputs['Scale'].default_value = (3.0, 3.0, 3.0)
    links.new(mapping.outputs['Vector'], img_node.inputs['Vector'])

    tex_coord = nodes.new(type="ShaderNodeTexCoord")
    tex_coord.location = (-400, 0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # Tint the grid with the provided material_color using Vector Math (Multiply)
    # This avoids API breaking changes between MixRGB and Mix nodes across Blender versions
    tint_node = nodes.new(type="ShaderNodeVectorMath")
    tint_node.operation = 'MULTIPLY'
    tint_node.location = (250, 0)
    tint_node.inputs[1].default_value = material_color
    links.new(img_node.outputs['Color'], tint_node.inputs[0])
    links.new(tint_node.outputs['Vector'], bsdf.inputs['Base Color'])

    # Add localized bump based on the texture for extra realistic feel
    bump = nodes.new(type="ShaderNodeBump")
    bump.location = (250, -200)
    bump.inputs['Distance'].default_value = 0.05
    bump.inputs['Strength'].default_value = 0.6
    links.new(img_node.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    # Assign material to the object
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    # === Step 4: Position & Finalize ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # Set as active and selected
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    return f"Created '{obj.name}' utilizing Seamless Box Projection texturing at {location}."
