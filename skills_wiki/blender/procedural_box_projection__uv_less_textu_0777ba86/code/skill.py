def create_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjected_Part",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.3, 0.1),
    **kwargs
) -> str:
    """
    Creates a complex mechanical shape demonstrating UV-less Box Projection texturing.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base tint color to mix with the projection grid.

    Returns:
        Status string.
    """
    import bpy
    import bmesh

    # 1. Get Target Scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # 2. Build the Geometry using BMesh
    bm = bmesh.new()
    
    # Create base cylinder
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=32,
        radius1=1.0, radius2=1.0, depth=0.5
    )
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, 0.25)) # Rest on the floor (z=0)

    # Grab the top face for extrusions
    top_face = next(f for f in bm.faces if f.normal.z > 0.9)

    # First Extrude & Inset
    ret1 = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    ext_face1 = ret1['faces'][0]
    bmesh.ops.scale(bm, vec=(0.6, 0.6, 1.0), verts=ext_face1.verts)
    bmesh.ops.translate(bm, verts=ext_face1.verts, vec=(0, 0, 0.4))

    # Second Extrude & Inset
    ret2 = bmesh.ops.extrude_discrete_faces(bm, faces=[ext_face1])
    ext_face2 = ret2['faces'][0]
    bmesh.ops.scale(bm, vec=(0.5, 0.5, 1.0), verts=ext_face2.verts)
    bmesh.ops.translate(bm, verts=ext_face2.verts, vec=(0, 0, 0.3))

    # Finalize Mesh
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    bm.to_mesh(mesh)
    bm.free()

    for poly in mesh.polygons:
        poly.use_smooth = True

    # 3. Create Object & Add to Scene
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    obj.location = location
    obj.scale = (scale, scale, scale)

    # 4. Apply Modifiers (Bevel for sharp edges, Subdiv for overall smoothness)
    mod_bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    mod_bevel.limit_method = 'ANGLE'
    mod_bevel.angle_limit = 0.5  # ~30 degrees
    mod_bevel.segments = 3
    mod_bevel.width = 0.03
    
    mod_subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    mod_subdiv.levels = 2
    mod_subdiv.render_levels = 2

    # 5. Build the Box Projection Material
    mat = bpy.data.materials.new(name=object_name + "_BoxProj_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Nodes
    node_out = nodes.new('ShaderNodeOutputMaterial')
    node_out.location = (600, 0)

    node_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    node_bsdf.location = (300, 0)
    node_bsdf.inputs['Roughness'].default_value = 0.35
    node_bsdf.inputs['Metallic'].default_value = 0.7
    links.new(node_bsdf.outputs['BSDF'], node_out.inputs['Surface'])

    # Texture Mapping (Using Object Coordinates = UV-less)
    node_tex_coord = nodes.new('ShaderNodeTexCoord')
    node_tex_coord.location = (-600, 0)

    node_mapping = nodes.new('ShaderNodeMapping')
    node_mapping.location = (-400, 0)
    links.new(node_tex_coord.outputs['Object'], node_mapping.inputs['Vector'])

    # Create an internal test image to visualize the projection
    img_name = "Generated_UV_Grid"
    img = bpy.data.images.get(img_name)
    if not img:
        img = bpy.data.images.new(name=img_name, width=1024, height=1024, alpha=False, generated_type='COLOR_GRID')

    # Image Node Setup (The core of the skill)
    node_img = nodes.new('ShaderNodeTexImage')
    node_img.location = (-200, 0)
    node_img.image = img
    
    # >>> CORE SKILL SETTINGS <<<
    node_img.projection = 'BOX'         # Project from all sides
    node_img.projection_blend = 0.2     # Soften/blur the seams together
    
    links.new(node_mapping.outputs['Vector'], node_img.inputs['Vector'])

    # Tint node to incorporate parameterized color
    node_mix = nodes.new('ShaderNodeMixRGB')
    node_mix.location = (50, 0)
    node_mix.blend_type = 'MULTIPLY'
    node_mix.inputs[0].default_value = 0.8  # Mix Factor
    node_mix.inputs[2].default_value = (*material_color, 1.0)
    
    links.new(node_img.outputs['Color'], node_mix.inputs[1])
    links.new(node_mix.outputs['Color'], node_bsdf.inputs['Base Color'])

    # Assign Material
    obj.data.materials.append(mat)

    return f"Created '{object_name}' with procedural Box Projection material at {location}."
