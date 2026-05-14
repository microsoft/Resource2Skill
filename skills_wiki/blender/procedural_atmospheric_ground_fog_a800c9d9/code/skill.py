def create_object(
    scene_name: str = "Scene",
    object_name: str = "Procedural_Ground_Fog",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 10.0,
    material_color: tuple = (0.7, 0.75, 0.8),
    **kwargs,
) -> str:
    """
    Create a procedural volumetric ground fog domain.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created fog volume.
        location: (x, y, z) world-space position of the volume center.
        scale: Uniform scale factor defining the size of the fog domain.
        material_color: (R, G, B) color of the fog (base and ambient emission).
        **kwargs: 
            density_multiplier (float): Overall thickness of the fog (default: 0.05).
            noise_scale (float): Scale of the clumping noise (default: 2.0).

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Extract kwargs with defaults
    density_mult_val = kwargs.get('density_multiplier', 0.05)
    noise_scale_val = kwargs.get('noise_scale', 2.0)

    # === Step 1: Create Bounding Geometry ===
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    fog_domain = bpy.context.active_object
    fog_domain.name = object_name
    
    # Scale to cover a large area (X/Y are large, Z is half height)
    fog_domain.scale = (scale * 2.0, scale * 2.0, scale)
    fog_domain.location = Vector(location)
    
    # Set to bounding box display so it doesn't obstruct viewport modeling
    fog_domain.display_type = 'BOUNDS'

    # === Step 2: Build Procedural Volume Material ===
    mat_name = f"Mat_{object_name}"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    fog_domain.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output and Core Volume Nodes
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (800, 0)

    vol_node = nodes.new('ShaderNodeVolumePrincipled')
    vol_node.location = (500, 0)
    # Set color and anisotropy
    vol_node.inputs['Color'].default_value = (*material_color, 1.0)
    vol_node.inputs['Emission Color'].default_value = (*material_color, 1.0)
    vol_node.inputs['Anisotropy'].default_value = 0.2
    
    # Ambient emission is a tiny fraction of density to simulate scattered light
    vol_node.inputs['Emission Strength'].default_value = density_mult_val * 0.02

    # Coordinate & Gradient Logic
    coord_node = nodes.new('ShaderNodeTexCoord')
    coord_node.location = (-800, 0)

    sep_xyz = nodes.new('ShaderNodeSeparateXYZ')
    sep_xyz.location = (-600, 0)

    # Invert Generated Z (0=bottom, 1=top -> 1=bottom, 0=top)
    inv_z = nodes.new('ShaderNodeMath')
    inv_z.operation = 'SUBTRACT'
    inv_z.inputs[0].default_value = 1.0
    inv_z.location = (-400, 0)

    # Power curves the gradient to hug the ground
    power_node = nodes.new('ShaderNodeMath')
    power_node.operation = 'POWER'
    power_node.inputs[1].default_value = 2.0
    power_node.location = (-200, 0)

    # Noise Logic for Breakup
    noise_node = nodes.new('ShaderNodeTexNoise')
    noise_node.inputs['Scale'].default_value = noise_scale_val
    noise_node.inputs['Detail'].default_value = 4.0
    noise_node.location = (-400, 300)
    
    # Increase contrast of the noise
    noise_ramp = nodes.new('ShaderNodeMapRange')
    noise_ramp.inputs[1].default_value = 0.3 # From Min
    noise_ramp.inputs[2].default_value = 0.7 # From Max
    noise_ramp.location = (-200, 300)

    # Math Logic: Gradient * Noise * Overall Density
    mix_noise = nodes.new('ShaderNodeMath')
    mix_noise.operation = 'MULTIPLY'
    mix_noise.location = (100, 150)

    final_density = nodes.new('ShaderNodeMath')
    final_density.operation = 'MULTIPLY'
    final_density.inputs[1].default_value = density_mult_val
    final_density.location = (300, 150)

    # === Step 3: Connect the Node Tree ===
    # Surface out -> empty. Volume out -> Principled Volume
    links.new(vol_node.outputs['Volume'], out_node.inputs['Volume'])
    
    # Setup Z-Gradient
    links.new(coord_node.outputs['Generated'], sep_xyz.inputs['Vector'])
    links.new(sep_xyz.outputs['Z'], inv_z.inputs[1])
    links.new(inv_z.outputs['Value'], power_node.inputs[0])
    
    # Setup Noise (Use object coords so scale doesn't stretch noise)
    links.new(coord_node.outputs['Object'], noise_node.inputs['Vector'])
    links.new(noise_node.outputs['Fac'], noise_ramp.inputs[0])
    
    # Mix and apply density
    links.new(power_node.outputs['Value'], mix_noise.inputs[0])
    links.new(noise_ramp.outputs['Result'], mix_noise.inputs[1])
    
    links.new(mix_noise.outputs['Value'], final_density.inputs[0])
    links.new(final_density.outputs['Value'], vol_node.inputs['Density'])

    return f"Created '{object_name}' (Procedural Volumetric Fog) at {location} with bounding scale {scale}."
