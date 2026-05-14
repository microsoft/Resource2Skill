def create_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjected_Part",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.3, 0.1),
    **kwargs,
) -> str:
    """
    Create a complex stepped hard-surface part textured procedurally using 
    Box (Tri-Planar) Projection without UV unwrapping.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color tint for the projected grid.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (Stepped Cylinder Profile) ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # 2D Profile vertices (X = Radius, Z = Height)
    verts = [
        (0.0, 0.0, 0.0),    # Center bottom (on axis)
        (1.0, 0.0, 0.0),    # Outer bottom edge
        (1.0, 0.0, 0.4),    # Outer top edge
        (0.6, 0.0, 0.4),    # Inner step horizontal
        (0.6, 0.0, 0.8),    # Middle top edge
        (0.3, 0.0, 0.8),    # Top step horizontal
        (0.3, 0.0, 0.5),    # Inner hole wall
        (0.0, 0.0, 0.5)     # Center hole bottom (on axis)
    ]
    edges = [(i, i+1) for i in range(len(verts)-1)]
    mesh.from_pydata(verts, edges, [])

    # === Step 2: Apply Non-Destructive Modeling Modifiers ===
    screw = obj.modifiers.new(name="Screw", type='SCREW')
    screw.steps = 32
    screw.render_steps = 64
    screw.angle = math.radians(360)
    screw.use_smooth_shade = True
    screw.use_merge_vertices = True
    screw.merge_threshold = 0.01

    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.05
    bevel.segments = 3
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(45) # Catches the 90 degree steps

    subsurf = obj.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 3

    # === Step 3: Build Box-Projected Material ===
    mat = bpy.data.materials.new(name=object_name + "_Material")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output & BSDF
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1100, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (800, 0)
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    # Coordinates & Mapping
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-400, 0)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-200, 0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # Image Texture (Box Projected)
    tex_image = nodes.new('ShaderNodeTexImage')
    tex_image.location = (0, 0)
    tex_image.projection = 'BOX'
    tex_image.projection_blend = 0.25  # <-- The core technique to hide seams

    # Generate an internal Color Grid to demonstrate the projection without external files
    img_name = "Box_Projection_Grid_Debug"
    img = bpy.data.images.get(img_name)
    if not img:
        img = bpy.data.images.new(img_name, width=1024, height=1024)
        img.generated_type = 'COLOR_GRID'
    tex_image.image = img
    links.new(mapping.outputs['Vector'], tex_image.inputs['Vector'])

    # Multiply grid with parameter color
    if bpy.app.version >= (3, 4, 0):
        mix = nodes.new('ShaderNodeMix')
        mix.data_type = 'RGBA'
        mix.blend_type = 'MULTIPLY'
        mix.inputs['Factor'].default_value = 1.0
        mix.inputs['B'].default_value = (*material_color, 1.0)
        links.new(tex_image.outputs['Color'], mix.inputs['A'])
        color_out = mix.outputs['Result']
    else:
        mix = nodes.new('ShaderNodeMixRGB')
        mix.blend_type = 'MULTIPLY'
        mix.inputs['Fac'].default_value = 1.0
        mix.inputs['Color2'].default_value = (*material_color, 1.0)
        links.new(tex_image.outputs['Color'], mix.inputs['Color1'])
        color_out = mix.outputs['Color']
    
    mix.location = (300, 100)
    links.new(color_out, bsdf.inputs['Base Color'])

    # Derive Roughness from the texture grid to demonstrate PBR mapping coherence
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (300, -200)
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (0.3, 0.3, 0.3, 1.0)
    ramp.color_ramp.elements[1].position = 1.0
    ramp.color_ramp.elements[1].color = (0.7, 0.7, 0.7, 1.0)
    links.new(tex_image.outputs['Color'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], bsdf.inputs['Roughness'])

    # Assign material
    obj.data.materials.append(mat)

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' with Box Projected Material at {location}"
