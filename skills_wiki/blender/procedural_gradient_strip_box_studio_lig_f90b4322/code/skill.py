def create_gradient_light(
    scene_name: str = "Scene",
    object_name: str = "GradientStripBox",
    location: tuple = (0.0, -2.0, 0.0),
    rotation: tuple = (1.5708, 0, 0), # 90 degrees on X
    scale: tuple = (1.0, 4.0, 1.0),
    light_color: tuple = (1.0, 1.0, 1.0),
    intensity: float = 10.0,
    double_gradient: bool = True,
    axis: str = 'X',
    falloff: float = 2.0,
    **kwargs
) -> str:
    """
    Creates a procedural gradient emission plane (Strip Box) for studio lighting.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name of the created light plane.
        location: (x, y, z) position.
        rotation: (x, y, z) rotation in radians.
        scale: Scale factor (non-uniform scale creates strip lights).
        light_color: (R, G, B) color of the emission.
        intensity: Brightness multiplier.
        double_gradient: If True, gradient peaks in the center and fades to both edges. 
                         If False, fades linearly from one edge to the other.
        axis: 'X' or 'Y' - the local axis the gradient flows along.
        falloff: Controls the sharpness of the gradient (higher = sharper, thinner strip).
        
    Returns:
        Status string.
    """
    import bpy
    import math
    
    # 1. Create Base Geometry (Plane)
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = scale
    
    # Hide from camera so it acts as an off-screen light/reflection source
    obj.visible_camera = False 
    if hasattr(obj, 'cycles'):
        obj.cycles.is_camera_visible = False
    
    # 2. Build Procedural Gradient Material
    mat = bpy.data.materials.new(name=f"{object_name}_GradientMat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Remove default Principled BSDF setup
    
    # Add Core Nodes
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    
    sep_xyz = nodes.new('ShaderNodeSeparateXYZ')
    sep_xyz.location = (-400, 0)
    
    math_power = nodes.new('ShaderNodeMath')
    math_power.operation = 'POWER'
    math_power.inputs[1].default_value = falloff
    math_power.location = (200, 0)
    
    math_intensity = nodes.new('ShaderNodeMath')
    math_intensity.operation = 'MULTIPLY'
    math_intensity.inputs[1].default_value = intensity
    math_intensity.location = (400, 0)
    
    emission = nodes.new('ShaderNodeEmission')
    emission.inputs['Color'].default_value = (*light_color, 1.0)
    emission.location = (600, 0)
    
    out = nodes.new('ShaderNodeOutputMaterial')
    out.location = (800, 0)
    
    # 3. Connect the basic coordinate flow
    links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], sep_xyz.inputs['Vector'])
    
    # Select target axis
    axis_socket = sep_xyz.outputs[0] if axis.upper() == 'X' else sep_xyz.outputs[1]
    current_output = axis_socket
    
    # 4. Math Logic for Gradient Types
    if double_gradient:
        # Center the generated coordinates (-0.5 to 0.5)
        mapping.inputs['Location'].default_value = (-0.5, -0.5, 0.0)
        
        # Absolute (-0.5 -> 0.5 becomes 0.5 -> 0 -> 0.5)
        math_abs = nodes.new('ShaderNodeMath')
        math_abs.operation = 'ABSOLUTE'
        math_abs.location = (-200, 100)
        
        # Multiply by 2 (0.5 -> 0 -> 0.5 becomes 1.0 -> 0 -> 1.0)
        math_mul = nodes.new('ShaderNodeMath')
        math_mul.operation = 'MULTIPLY'
        math_mul.inputs[1].default_value = 2.0
        math_mul.location = (0, 100)
        
        # Subtract from 1 (1.0 -> 0 -> 1.0 becomes 0.0 -> 1.0 -> 0.0)
        math_sub = nodes.new('ShaderNodeMath')
        math_sub.operation = 'SUBTRACT'
        math_sub.inputs[0].default_value = 1.0
        math_sub.location = (0, -100)
        
        links.new(current_output, math_abs.inputs[0])
        links.new(math_abs.outputs[0], math_mul.inputs[0])
        links.new(math_mul.outputs[0], math_sub.inputs[1])
        
        current_output = math_sub.outputs[0]
        
    # 5. Connect Final Falloff and Emission
    links.new(current_output, math_power.inputs[0])
    links.new(math_power.outputs[0], math_intensity.inputs[0])
    links.new(math_intensity.outputs[0], emission.inputs['Strength'])
    links.new(emission.outputs['Emission'], out.inputs['Surface'])
    
    # Deselect all and select the newly created light plane
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    grad_type = "Double" if double_gradient else "Single"
    return f"Created '{object_name}' (Procedural {grad_type} Gradient Strip Light) at {location} with intensity {intensity}."
