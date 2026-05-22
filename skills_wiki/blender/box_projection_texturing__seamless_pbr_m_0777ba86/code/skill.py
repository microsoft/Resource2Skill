def create_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjected_Part",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.3, 0.6, 0.7),
    **kwargs,
) -> str:
    """
    Create a complex tiered mechanical part textured with Box Projection mapping.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color tint for the projection map.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (Surface of Revolution) ===
    # Profile coordinates (x, z) for the tiered part
    profile = [
        (0.0, 0.0),    # Bottom center
        (1.5, 0.0),    # Bottom outer edge
        (1.5, 0.4),    # Base tier height
        (1.0, 0.4),    # Inset for middle tier
        (1.0, 1.2),    # Middle tier height
        (0.5, 1.2),    # Top flat surface
        (0.5, 0.7),    # Inner hole depth
        (0.0, 0.7)     # Inner hole center
    ]

    verts = []
    faces = []
    segments = 48

    # Generate vertices by revolving the profile
    for i in range(segments):
        angle = (i / segments) * 2 * math.pi
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        for px, pz in profile:
            verts.append((px * cos_a, px * sin_a, pz))

    num_p = len(profile)
    # Generate quad faces connecting the segments
    for i in range(segments):
        next_i = (i + 1) % segments
        for j in range(num_p - 1):
            v1 = i * num_p + j
            v2 = i * num_p + j + 1
            v3 = next_i * num_p + j + 1
            v4 = next_i * num_p + j
            # Reverse winding order to ensure normals face outward
            faces.append((v4, v3, v2, v1))

    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    # Clean up degenerate center poles and recalculate normals
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # === Step 2: Modifiers for Procedural Edge Flow ===
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.segments = 2
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(35)
    bevel.width = 0.03

    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 3
    subsurf.render_levels = 3

    for poly in mesh.polygons:
        poly.use_smooth = True

    # === Step 3: Box Projection Material Setup ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Dummy images to represent external PBR textures
    # We use COLOR_GRID to easily visualize the lack of stretching and seam blending
    dummy_color = bpy.data.images.new(name=f"{object_name}_ColorGrid", width=1024, height=1024)
    dummy_color.generated_type = 'COLOR_GRID'
    
    dummy_noncolor = bpy.data.images.new(name=f"{object_name}_NonColorGrid", width=1024, height=1024)
    dummy_noncolor.generated_type = 'COLOR_GRID'
    dummy_noncolor.colorspace_settings.name = 'Non-Color'

    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1200, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (900, 0)
    bsdf.inputs['Metallic'].default_value = 0.8  # Make it look like worn metal

    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (0, 0)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (200, 0)
    # Scale the texture slightly so it repeats beautifully
    mapping.inputs['Scale'].default_value = (2.0, 2.0, 2.0)

    def create_box_tex(name, loc, img):
        node = nodes.new('ShaderNodeTexImage')
        node.name = name
        node.location = loc
        node.image = img
        # THIS IS THE CORE SKILL: Box projection with blending
        node.projection = 'BOX'
        node.projection_blend = 0.25
        return node

    # Base Color Texture
    tex_color = create_box_tex("Tex_Color", (400, 300), dummy_color)
    
    # MixRGB to tint the generated grid with the requested material_color
    mix_node = nodes.new('ShaderNodeMixRGB')
    mix_node.location = (650, 300)
    mix_node.blend_type = 'MULTIPLY'
    mix_node.inputs['Fac'].default_value = 1.0
    mix_node.inputs['Color2'].default_value = (*material_color, 1.0)

    # Roughness Texture (Uses a ramp to convert the grid into roughness variance)
    tex_rough = create_box_tex("Tex_Roughness", (400, 0), dummy_noncolor)
    ramp_rough = nodes.new('ShaderNodeValToRGB')
    ramp_rough.location = (650, 0)
    ramp_rough.color_ramp.elements[0].color = (0.2, 0.2, 0.2, 1.0)
    ramp_rough.color_ramp.elements[1].color = (0.7, 0.7, 0.7, 1.0)

    # Bump/Normal Texture
    tex_bump = create_box_tex("Tex_Bump", (400, -300), dummy_noncolor)
    bump_node = nodes.new('ShaderNodeBump')
    bump_node.location = (650, -300)
    bump_node.inputs['Distance'].default_value = 0.05

    # Connect Coordinates
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], tex_color.inputs['Vector'])
    links.new(mapping.outputs['Vector'], tex_rough.inputs['Vector'])
    links.new(mapping.outputs['Vector'], tex_bump.inputs['Vector'])

    # Connect Shader Flow
    links.new(tex_color.outputs['Color'], mix_node.inputs['Color1'])
    links.new(mix_node.outputs['Color'], bsdf.inputs['Base Color'])
    
    links.new(tex_rough.outputs['Color'], ramp_rough.inputs['Fac'])
    links.new(ramp_rough.outputs['Color'], bsdf.inputs['Roughness'])
    
    links.new(tex_bump.outputs['Color'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], bsdf.inputs['Normal'])

    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    obj.data.materials.append(mat)

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' with Box Projected material at {location}"
