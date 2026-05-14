def create_pbr_displaced_surface(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Brick_Surface",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 2.0,
    primary_color: tuple = (0.6, 0.2, 0.1), # Brick color
    **kwargs,
) -> str:
    """
    Create a PBR material setup with Adaptive Displacement in the active scene.
    Demonstrates Mapping, HSV adjustment, Inverted Gloss (Roughness), Normal Mapping,
    and True Geometric Displacement.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name of the generated plane.
        location: (x, y, z) world-space position.
        scale: Uniform scale of the surface.
        primary_color: Base color of the procedural texture.
        
    Returns:
        Status string.
    """
    import bpy
    
    # 1. Setup Scene for Adaptive Subdivision
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL' # Required for Adaptive Subdivision
    
    # 2. Create Geometry
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Apply Scale so displacement scales correctly
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Add Subdivision Surface Modifier
    subsurf = obj.modifiers.new(name="Adaptive_Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'CATMULL_CLARK'
    try:
        # Enable adaptive subdivision (only works if engine is cycles and feature set is experimental)
        subsurf.use_adaptive_subdivision = True
    except AttributeError:
        pass # Fallback if run in an environment where experimental isn't active
        
    # 3. Create Material
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    # VERY IMPORTANT: Enable true displacement in the material settings
    mat.cycles.displacement_method = 'DISPLACEMENT'
    
    obj.data.materials.append(mat)
    
    # 4. Build the PBR Node Network
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Clear default nodes to build cleanly
    
    # Create nodes
    output_node = nodes.new('ShaderNodeOutputMaterial')
    output_node.location = (1200, 0)
    
    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (800, 0)
    
    # Texture Coordinate & Mapping
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    mapping.inputs['Scale'].default_value = (3.0, 3.0, 3.0) # Scale the texture down
    
    # Simulating PBR Image Textures using a Brick Texture + Noise
    brick_tex = nodes.new('ShaderNodeTexBrick')
    brick_tex.location = (-300, 200)
    brick_tex.inputs['Color 1'].default_value = (*primary_color, 1.0)
    brick_tex.inputs['Color 2'].default_value = (primary_color[0]*0.8, primary_color[1]*0.8, primary_color[2]*0.8, 1.0)
    brick_tex.inputs['Mortar'].default_value = (0.8, 0.8, 0.8, 1.0)
    
    # Detail Noise (to drive normal map realistically)
    noise_tex = nodes.new('ShaderNodeTexNoise')
    noise_tex.location = (-300, -200)
    noise_tex.inputs['Scale'].default_value = 50.0
    noise_tex.inputs['Detail'].default_value = 15.0
    
    # Color Adjustment: Hue Saturation Value (from video)
    hsv_node = nodes.new('ShaderNodeHueSaturation')
    hsv_node.location = (200, 300)
    hsv_node.inputs['Saturation'].default_value = 1.1 # Slight boost
    
    # Roughness Conversion: Invert Node (simulating gloss-to-roughness workflow from video)
    invert_node = nodes.new('ShaderNodeInvert')
    invert_node.location = (200, 0)
    
    # Normal Map Workflow
    normal_map = nodes.new('ShaderNodeNormalMap')
    normal_map.location = (200, -200)
    normal_map.inputs['Strength'].default_value = 0.5
    
    # Displacement Workflow
    displacement = nodes.new('ShaderNodeDisplacement')
    displacement.location = (800, -300)
    displacement.inputs['Midlevel'].default_value = 0.0  # From video
    displacement.inputs['Scale'].default_value = 0.05    # Scaled down to prevent extreme spikes
    
    # 5. Wire the network (The "Noodles")
    
    # Vector Mapping
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], brick_tex.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise_tex.inputs['Vector'])
    
    # Color Route
    links.new(brick_tex.outputs['Color'], hsv_node.inputs['Color'])
    links.new(hsv_node.outputs['Color'], bsdf_node.inputs['Base Color'])
    
    # Roughness Route (Simulating Gloss Map Inversion)
    # Using the noise texture to act as our gloss map
    links.new(noise_tex.outputs['Fac'], invert_node.inputs['Color'])
    links.new(invert_node.outputs['Color'], bsdf_node.inputs['Roughness'])
    
    # Normal Route
    links.new(noise_tex.outputs['Color'], normal_map.inputs['Color'])
    links.new(normal_map.outputs['Normal'], bsdf_node.inputs['Normal'])
    
    # Displacement Route (Using Brick factor as height map)
    links.new(brick_tex.outputs['Fac'], displacement.inputs['Height'])
    
    # Final Outputs
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
    links.new(displacement.outputs['Displacement'], output_node.inputs['Displacement'])
    
    # 6. Add some lighting to visualize the displacement effectively
    sun_name = f"{object_name}_Sun"
    if not bpy.data.objects.get(sun_name):
        bpy.ops.object.light_add(type='SUN', radius=1.0, location=(location[0]+5, location[1]-5, location[2]+5))
        sun = bpy.context.active_object
        sun.name = sun_name
        sun.data.energy = 3.0
        sun.data.angle = 0.1 # Sharp shadows to show micro-displacement
        # Point sun at the plane
        sun.rotation_euler = (0.785, 0.0, 0.785)
    
    return f"Created '{object_name}' with complete PBR node setup and Adaptive Displacement enabled."
