def create_object(
    scene_name: str = "Scene",
    object_name: str = "SeamlessBoxProjectedProp",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.4, 0.1),
    **kwargs,
) -> str:
    """
    Creates a complex mechanical shape textured with a seamless Box-Projected 
    pattern, bypassing the need for UV unwrapping.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) color multiplier.
        
    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Complex Base Geometry ===
    # Define a complex stepped profile (half-slice) that would normally stretch UVs
    profile_verts = [
        (0.0, 0.0, 0.0),
        (1.2, 0.0, 0.0),
        (1.2, 0.0, 0.3),  # base flange
        (0.8, 0.0, 0.3),  # step in
        (0.8, 0.0, 0.8),  # middle cylinder
        (0.6, 0.0, 0.8),  # step in
        (0.6, 0.0, 0.5),  # deep inset
        (0.3, 0.0, 0.5),  # inner floor
        (0.3, 0.0, 1.2),  # top knob
        (0.0, 0.0, 1.2)   # center top
    ]
    profile_edges = [(i, i+1) for i in range(len(profile_verts)-1)]
    
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    mesh.from_pydata(profile_verts, profile_edges, [])
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # Revolve profile to create a 3D solid
    screw = obj.modifiers.new(name="Screw", type='SCREW')
    screw.steps = 32
    screw.render_steps = 32
    screw.angle = math.radians(360)
    screw.use_smooth_shade = True
    screw.use_normal_calculate = True # Fixes inside-out normals

    # Merge center vertices from revolution
    obj.modifiers.new(name="Weld", type='WELD')

    # Add bevels for realism on 90-degree edges
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.segments = 3
    bevel.width = 0.03
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(30)

    # Smooth the curves
    subsurf = obj.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # === Step 2: Build The Box-Projected Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1000, 0)

    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (700, 0)
    links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])

    # 1. Texture Coordinate (Using Object coords, NOT UVs)
    coord_node = nodes.new('ShaderNodeTexCoord')
    coord_node.location = (-400, 0)

    # 2. Mapping
    map_node = nodes.new('ShaderNodeMapping')
    map_node.location = (-200, 0)
    map_node.inputs['Scale'].default_value = (2.0, 2.0, 2.0)
    links.new(coord_node.outputs['Object'], map_node.inputs['Vector'])

    # Generate an internal grid image to vividly demonstrate lack of stretching
    img_name = "Procedural_Box_Grid"
    img = bpy.data.images.get(img_name)
    if not img:
        img = bpy.data.images.new(img_name, width=1024, height=1024, alpha=False)
        img.generated_type = 'COLOR_GRID'

    # 3. Image Texture Node (THE CORE TECHNIQUE)
    tex_node = nodes.new('ShaderNodeTexImage')
    tex_node.location = (100, 0)
    tex_node.image = img
    tex_node.projection = 'BOX'           # <--- Prevents side stretching
    tex_node.projection_blend = 0.25      # <--- Blends the 90-degree seams
    links.new(map_node.outputs['Vector'], tex_node.inputs['Vector'])

    # 4. Color Multiplication (Applying the parameter safely across versions)
    try:
        # Blender 3.4+ / 4.0+
        mix_node = nodes.new('ShaderNodeMix')
        mix_node.data_type = 'RGBA'
        mix_node.blend_type = 'MULTIPLY'
        mix_node.location = (400, 0)
        mix_node.inputs['Factor'].default_value = 1.0
        mix_node.inputs['A'].default_value = (*material_color, 1.0)
        links.new(tex_node.outputs['Color'], mix_node.inputs['B'])
        color_out = mix_node.outputs['Result']
    except Exception:
        # Legacy fallback (Blender 3.3 and below)
        mix_node = nodes.new('ShaderNodeMixRGB')
        mix_node.blend_type = 'MULTIPLY'
        mix_node.location = (400, 0)
        mix_node.inputs['Fac'].default_value = 1.0
        mix_node.inputs['Color1'].default_value = (*material_color, 1.0)
        links.new(tex_node.outputs['Color'], mix_node.inputs['Color2'])
        color_out = mix_node.outputs['Color']

    links.new(color_out, bsdf_node.inputs['Base Color'])
    
    # Use the grid luminance as a roughness map to add surface variation
    links.new(tex_node.outputs['Color'], bsdf_node.inputs['Roughness'])

    obj.data.materials.append(mat)

    # === Step 3: Finalize Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' with seamless Box Projection mapping at {location}"
