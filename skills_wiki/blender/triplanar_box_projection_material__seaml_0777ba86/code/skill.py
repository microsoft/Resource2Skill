def create_object(
    scene_name: str = "Scene",
    object_name: str = "Triplanar_Prop",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a mechanical shape with a Triplanar (Box-Projected) Material setup.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color tint for the projected texture.
        **kwargs: Additional parameters.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry using BMesh ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    
    # 1. Base Disc
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=32,
        radius1=1.0,
        radius2=1.0,
        depth=0.2
    )

    # Find the top facing polygon
    top_face = None
    for f in bm.faces:
        if f.normal.z > 0.9:
            top_face = f
            break

    if top_face:
        # 2. Inset and Extrude UP (Creates the middle tier)
        bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3)
        ext1 = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
        extruded_top1 = ext1['faces'][0]
        bmesh.ops.translate(bm, verts=extruded_top1.verts, vec=Vector((0, 0, 0.5)))
        
        # 3. Inset and Extrude DOWN (Creates the inner cavity)
        bmesh.ops.inset_region(bm, faces=[extruded_top1], thickness=0.2)
        ext2 = bmesh.ops.extrude_discrete_faces(bm, faces=[extruded_top1])
        extruded_top2 = ext2['faces'][0]
        bmesh.ops.translate(bm, verts=extruded_top2.verts, vec=Vector((0, 0, -0.4)))

    # Apply smooth shading to all faces
    for f in bm.faces:
        f.smooth = True

    bm.to_mesh(mesh)
    bm.free()

    # === Step 2: Add Modifiers ===
    # Bevel to hold corners during subdivision
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.segments = 3
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = 0.52  # ~30 degrees
    bevel.width = 0.05

    # Subdivision Surface for organic smoothing
    subsurf = obj.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2


    # === Step 3: Build Triplanar / Box-Projection Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_TriplanarMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for n in nodes:
        nodes.remove(n)

    # Material Outputs & Shader
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (800, 0)

    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.location = (500, 0)
    principled.inputs['Roughness'].default_value = 0.7

    # Setup the Triplanar Mapping Nodes
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)

    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-400, 0)
    mapping.inputs['Scale'].default_value = (2.0, 2.0, 2.0) # Scale texture for better visibility

    # The core technique: Box Projection Image Node
    tex_image = nodes.new(type='ShaderNodeTexImage')
    tex_image.location = (-200, 0)
    tex_image.projection = 'BOX'
    tex_image.projection_blend = 0.25  # Blends the seams between the X, Y, Z axes

    # Generate a Grid texture to visualize the seamless projection perfectly
    img_name = "Triplanar_Demo_Grid"
    img = bpy.data.images.get(img_name)
    if not img:
        img = bpy.data.images.new(name=img_name, width=1024, height=1024, alpha=False)
        img.source = 'GENERATED'
        img.generated_type = 'COLOR_GRID'
    tex_image.image = img

    # Tint the grid with the requested material color
    mix_color = nodes.new(type='ShaderNodeMixRGB')
    mix_color.location = (150, 0)
    mix_color.blend_type = 'MULTIPLY'
    mix_color.inputs['Fac'].default_value = 1.0
    mix_color.inputs['Color2'].default_value = (*material_color, 1.0)

    # Connect the graph: Object Space -> Mapping -> Box Image -> Color Tint -> Principled BSDF
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], tex_image.inputs['Vector'])
    links.new(tex_image.outputs['Color'], mix_color.inputs['Color1'])
    links.new(mix_color.outputs['Color'], principled.inputs['Base Color'])
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])

    # Assign material
    obj.data.materials.append(mat)

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' using Box-Projection Triplanar setup at {location}."
