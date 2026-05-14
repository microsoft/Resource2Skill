def create_object(
    scene_name: str = "Scene",
    object_name: str = "VolumetricFogDomain",
    location: tuple = (0, 0, 0),
    scale: float = 10.0,
    material_color: tuple = (1.0, 1.0, 1.0),
    **kwargs,
) -> str:
    """
    Create a procedural volumetric fog domain in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the fog domain cube.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (size of the fog box).
        material_color: (R, G, B) color of the fog scattering.
        **kwargs: 
            - base_density (float): Density of the uniform volume (default: 0.04)
            - anisotropy (float): Directional scattering factor (default: 0.65)
            - noise_detail (float): Detail level of the noise texture (default: 5.0)
            - noise_scale (float): Scale of the noise texture (default: 5.0)

    Returns:
        Status string describing the created object.
    """
    import bpy
    from mathutils import Vector

    # Get scene
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # Extract kwargs with defaults based on the tutorial
    base_density = kwargs.get('base_density', 0.04)
    anisotropy = kwargs.get('anisotropy', 0.65)
    noise_detail = kwargs.get('noise_detail', 5.0)
    noise_scale = kwargs.get('noise_scale', 5.0)

    # === Step 1: Create Domain Geometry ===
    bpy.ops.mesh.primitive_cube_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Set display type to wireframe so it doesn't block the viewport
    obj.display_type = 'WIRE'

    # === Step 2: Build Volumetric Material ===
    mat_name = f"{object_name}_Mat"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Clear default Principled BSDF

    # Add necessary nodes
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (800, 0)

    mix_node = nodes.new('ShaderNodeMixShader')
    mix_node.location = (600, 0)
    mix_node.inputs['Fac'].default_value = 0.5

    prin_vol = nodes.new('ShaderNodeVolumePrincipled')
    prin_vol.location = (300, 150)
    prin_vol.inputs['Density'].default_value = base_density
    prin_vol.inputs['Anisotropy'].default_value = anisotropy
    # Apply requested material color to the fog
    prin_vol.inputs['Color'].default_value = (*material_color, 1.0) 

    vol_scat = nodes.new('ShaderNodeVolumeScatter')
    vol_scat.location = (300, -150)
    vol_scat.inputs['Anisotropy'].default_value = anisotropy
    vol_scat.inputs['Color'].default_value = (*material_color, 1.0)

    ramp_node = nodes.new('ShaderNodeValToRGB')
    ramp_node.location = (0, -150)
    # Configure ColorRamp to crush blacks and limit whites to grey
    ramp_node.color_ramp.elements[0].position = 0.2
    ramp_node.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    ramp_node.color_ramp.elements[1].position = 0.8
    # Gray color to limit maximum scatter density
    ramp_node.color_ramp.elements[1].color = (0.2, 0.2, 0.2, 1.0) 

    noise_node = nodes.new('ShaderNodeTexNoise')
    noise_node.location = (-300, -150)
    noise_node.inputs['Scale'].default_value = noise_scale
    noise_node.inputs['Detail'].default_value = noise_detail

    map_node = nodes.new('ShaderNodeMapping')
    map_node.location = (-500, -150)

    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-700, -150)

    # === Step 3: Link the Node Tree ===
    # Important: Plug into Volume input, not Surface
    links.new(mix_node.outputs[0], out_node.inputs['Volume']) 
    links.new(prin_vol.outputs[0], mix_node.inputs[1])
    links.new(vol_scat.outputs[0], mix_node.inputs[2])
    
    # Texture logic
    links.new(ramp_node.outputs['Color'], vol_scat.inputs['Density'])
    links.new(noise_node.outputs['Fac'], ramp_node.inputs['Fac'])
    links.new(map_node.outputs['Vector'], noise_node.inputs['Vector'])
    links.new(tex_coord.outputs['Generated'], map_node.inputs['Vector'])

    return f"Created procedural volumetric fog domain '{object_name}' at {location} with scale {scale}. Base density: {base_density}, Anisotropy: {anisotropy}."
