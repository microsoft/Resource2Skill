def create_object(
    scene_name: str = "Scene",
    object_name: str = "Displaced_PBR_Surface",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.35, 0.25, 0.20),
    **kwargs,
) -> str:
    """
    Create a heavily displaced surface using Cycles true material displacement.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created plane.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the procedural rock (0-1 range).
        **kwargs: Optional overrides (e.g., 'displacement_scale').
        
    Returns:
        Status string describing the creation.
    """
    import bpy
    import math
    from mathutils import Vector, Euler
    
    # 1. Setup Scene for True Displacement
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    scene.render.engine = 'CYCLES'
    # Optional: Enable experimental feature set for adaptive subdivision (not strictly required if subdivided heavily)
    scene.cycles.feature_set = 'SUPPORTED'
    
    # 2. Create Base Plane
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    plane = bpy.context.active_object
    plane.name = object_name
    plane.scale = (scale, scale, scale)
    
    # Add geometry density via Subdivision Surface modifier (Simple mode to keep edges square)
    subsurf = plane.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 6        # High subdivision for viewport preview
    subsurf.render_levels = 7 # Even higher for rendering
    
    # 3. Create the Material & Shader Node Tree
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    plane.data.materials.append(mat)
    
    # CRITICAL: Enable True Displacement in material settings
    mat.cycles.displacement_method = 'DISPLACEMENT'
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Clear default to build clean
    
    # Add Output
    node_output = nodes.new('ShaderNodeOutputMaterial')
    node_output.location = (400, 0)
    
    # Add Principled BSDF
    node_principled = nodes.new('ShaderNodeBsdfPrincipled')
    node_principled.location = (100, 0)
    node_principled.inputs['Roughness'].default_value = 0.85 # Rocky surfaces are rough
    
    # Add Displacement Node
    node_disp = nodes.new('ShaderNodeDisplacement')
    node_disp.location = (100, -300)
    disp_scale = kwargs.get('displacement_scale', 0.25)
    node_disp.inputs['Scale'].default_value = disp_scale * scale
    node_disp.inputs['Midlevel'].default_value = 0.5
    
    # Add Procedural Noise (to act as our downloaded texture)
    node_noise = nodes.new('ShaderNodeTexNoise')
    node_noise.location = (-400, -150)
    node_noise.inputs['Scale'].default_value = 4.0
    node_noise.inputs['Detail'].default_value = 15.0
    node_noise.inputs['Roughness'].default_value = 0.65
    
    # Color Ramp for Base Color
    node_color_ramp = nodes.new('ShaderNodeValToRGB')
    node_color_ramp.location = (-150, 100)
    
    # Set the ramp colors using the provided material_color argument
    color_elements = node_color_ramp.color_ramp.elements
    # Darker version of base color for crevices
    dark_color = (material_color[0]*0.2, material_color[1]*0.2, material_color[2]*0.2, 1.0)
    base_color = (material_color[0], material_color[1], material_color[2], 1.0)
    
    color_elements[0].position = 0.3
    color_elements[0].color = dark_color
    color_elements[1].position = 0.7
    color_elements[1].color = base_color
    
    # Make Connections
    links.new(node_noise.outputs['Color'], node_color_ramp.inputs['Fac'])
    links.new(node_color_ramp.outputs['Color'], node_principled.inputs['Base Color'])
    
    # Use Noise Color as Height data for displacement
    links.new(node_noise.outputs['Color'], node_disp.inputs['Height'])
    
    # Connect Principled & Displacement to Output
    links.new(node_principled.outputs['BSDF'], node_output.inputs['Surface'])
    links.new(node_disp.outputs['Displacement'], node_output.inputs['Displacement'])
    
    # 4. Add Sunlight for shadow emphasis (crucial for showing off displacement)
    sun_name = f"{object_name}_Sun"
    sun_data = bpy.data.lights.new(name=sun_name, type='SUN')
    sun_data.energy = 5.0
    sun_data.angle = 0.087 # ~5 degrees for relatively sharp shadows
    
    sun_obj = bpy.data.objects.new(name=sun_name, object_data=sun_data)
    bpy.context.collection.objects.link(sun_obj)
    
    # Position sun above the plane and rotate it to a low angle
    sun_obj.location = (location[0], location[1], location[2] + 5.0)
    # Pitch ~45 deg, Yaw ~30 deg to cast dynamic diagonal shadows
    sun_obj.rotation_euler = Euler((math.radians(45), math.radians(30), 0), 'XYZ')
    
    return f"Created highly subdivided plane '{object_name}' with True Shader Displacement. Switched engine to Cycles."
