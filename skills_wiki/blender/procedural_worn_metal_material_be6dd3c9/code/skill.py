def create_object(
    scene_name: str = "Scene",
    object_name: str = "WornMetalSphere",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    base_color: tuple = (0.15, 0.15, 0.15),
    dirt_color: tuple = (0.3, 0.15, 0.05),
    **kwargs,
) -> str:
    """
    Create a sphere with a procedural worn metal material.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        base_color: (R, G, B) color for the clean metal areas.
        dirt_color: (R, G, B) color for the dirty/rusted areas.
        **kwargs: Optional overrides (noise_scale, roughness_offset).

    Returns:
        Status string.
    """
    import bpy

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=64, 
        ring_count=32, 
        radius=1.0, 
        location=location
    )
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Smooth shading for clean reflections
    bpy.ops.object.shade_smooth()

    # === Step 2: Build Procedural Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes to start fresh
    for node in nodes:
        nodes.remove(node)

    # Material Output
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (600, 0)

    # Principled BSDF
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (300, 0)
    # Set to fully metallic
    bsdf.inputs['Metallic'].default_value = 1.0

    # Noise Texture (The core procedural mask)
    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.location = (-400, 0)
    noise.inputs['Scale'].default_value = kwargs.get('noise_scale', 10.0)
    noise.inputs['Detail'].default_value = 15.0  # Max detail for realistic wear
    noise.inputs['Roughness'].default_value = 0.6

    # ColorRamp (Drives Base Color)
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (-50, 200)
    
    # Clean metal color (Dark Gray)
    color_ramp.color_ramp.elements[0].position = 0.2
    color_ramp.color_ramp.elements[0].color = (*base_color, 1.0)
    
    # Dirt/Rust color (Brownish)
    color_ramp.color_ramp.elements[1].position = 0.7
    color_ramp.color_ramp.elements[1].color = (*dirt_color, 1.0)

    # Hue/Saturation/Value (Drives Roughness)
    # Acts as a multiplier to make the overall noise pattern shinier or rougher
    hsv = nodes.new(type='ShaderNodeHueSaturation')
    hsv.location = (-50, -100)
    hsv.inputs['Value'].default_value = kwargs.get('roughness_offset', 0.7)

    # === Step 3: Link the Node Tree ===
    # Noise -> ColorRamp -> Base Color
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
    
    # Noise -> HSV -> Roughness
    links.new(noise.outputs['Fac'], hsv.inputs['Color'])
    links.new(hsv.outputs['Color'], bsdf.inputs['Roughness'])

    # BSDF -> Output
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Assign material to the object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    return f"Created '{object_name}' with procedural worn metal material at {location}"
