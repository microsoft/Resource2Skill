def create_object(
    scene_name: str = "Scene",
    object_name: str = "SeamlessBoxProjectedPart",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.25, 0.1),
    **kwargs,
) -> str:
    """
    Creates a complex mechanical shape and applies a seamless material 
    using Object Coordinates and Box Projection blending.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color tint for the procedural rust/paint.
        
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    # Create base cylinder (radius 1, depth 0.5)
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, 
        segments=32, radius1=1.0, radius2=1.0, depth=0.5
    )

    # Ensure lookup tables are updated before iterating
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()

    # Find the top face (highest Z axis)
    top_face = max(bm.faces, key=lambda f: f.calc_center_median().z)

    # Inset 1
    ret = bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3)
    top_face = ret['faces'][0]

    # Extrude up
    ret = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    top_face = ret['faces'][0]
    bmesh.ops.translate(bm, verts=top_face.verts, vec=(0, 0, 0.4))

    # Inset 2
    ret = bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.2)
    top_face = ret['faces'][0]

    # Extrude down (creating a central hole)
    ret = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    top_face = ret['faces'][0]
    bmesh.ops.translate(bm, verts=top_face.verts, vec=(0, 0, -0.3))

    # Bevel sharp edges to catch light
    bm.edges.ensure_lookup_table()
    sharp_edges = [e for e in bm.edges if len(e.link_faces) == 2 and e.calc_face_angle() > 0.5]
    if sharp_edges:
        bmesh.ops.bevel(bm, geom=sharp_edges, offset=0.03, segments=3, profile=0.5)

    bm.to_mesh(mesh)
    bm.free()

    # Shade smooth
    for f in mesh.polygons:
        f.use_smooth = True

    # Add Subdivision Surface Modifier
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 3

    # === Step 2: Build Seamless Material ===
    mat_name = f"{object_name}_SeamlessMaterial"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(mat_name)
        mat.use_nodes = True
    
    tree = mat.node_tree
    tree.nodes.clear()

    # Core Shader Nodes
    output = tree.nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)

    principled = tree.nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (400, 0)
    tree.links.new(principled.outputs[0], output.inputs[0])

    # Coordinate setup (The core of the tutorial)
    tex_coord = tree.nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)

    mapping = tree.nodes.new('ShaderNodeMapping')
    mapping.location = (-400, 0)
    mapping.inputs['Scale'].default_value = (2.0, 2.0, 2.0)
    tree.links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # Procedural Base Color (Seamless 3D projection)
    noise = tree.nodes.new('ShaderNodeTexNoise')
    noise.location = (-200, 200)
    noise.inputs['Scale'].default_value = 8.0
    tree.links.new(mapping.outputs['Vector'], noise.inputs['Vector'])

    ramp = tree.nodes.new('ShaderNodeValToRGB')
    ramp.location = (0, 200)
    ramp.color_ramp.elements[0].color = (0.05, 0.05, 0.05, 1.0) # Dark dirt
    ramp.color_ramp.elements[1].color = (*material_color, 1.0)  # User defined color
    tree.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    tree.links.new(ramp.outputs['Color'], principled.inputs['Base Color'])

    # Box Projected Image Texture (Demonstrating the exact video technique)
    img_name = "Generated_BoxProjection_Demo"
    img = bpy.data.images.get(img_name)
    if not img:
        img = bpy.data.images.new(name=img_name, width=1024, height=1024)
        img.generated_type = 'COLOR_GRID' # Highly visible pattern to show off the blending
        
    tex_img = tree.nodes.new('ShaderNodeTexImage')
    tex_img.image = img
    tex_img.location = (-200, -100)
    
    # CRITICAL: Box projection setup
    tex_img.projection = 'BOX'
    tex_img.projection_blend = 0.3  # This blends the seams at 90 degree corners
    tree.links.new(mapping.outputs['Vector'], tex_img.inputs['Vector'])

    # Pass the box-projected image into a bump node
    bump = tree.nodes.new('ShaderNodeBump')
    bump.location = (100, -100)
    bump.inputs['Distance'].default_value = 0.05
    tree.links.new(tex_img.outputs['Color'], bump.inputs['Height'])
    tree.links.new(bump.outputs['Normal'], principled.inputs['Normal'])

    # Assign material to object
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    # === Step 3: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' with Box Projected material at {location}"
