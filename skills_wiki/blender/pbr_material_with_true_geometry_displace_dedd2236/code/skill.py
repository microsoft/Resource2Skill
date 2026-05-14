def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Rock_Plane",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.45, 0.38, 0.32),
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with a true-displacement PBR rock material 
    and a Sun light to showcase the shadows, set to the Cycles engine.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created mesh.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the plane and displacement depth.
        material_color: (R, G, B) base color of the rock surface.

    Returns:
        Status string describing the creation.
    """
    import bpy
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Render Engine Setup ===
    # Cycles is required for true material displacement to be visible
    scene.render.engine = 'CYCLES'
    
    # === Step 2: Create Subdivided Geometry ===
    # A 200x200 grid provides 40,000 faces, giving plenty of vertices for displacement
    bpy.ops.mesh.primitive_grid_add(
        x_subdivisions=200, 
        y_subdivisions=200, 
        size=2.0 * scale, 
        location=location
    )
    obj = bpy.context.active_object
    obj.name = object_name
    bpy.ops.object.shade_smooth()
    
    # === Step 3: Lighting Setup ===
    # A directional Sun light at an angle accentuates the physical bumps and cracks
    light_name = f"{object_name}_Sun"
    light_data = bpy.data.lights.new(name=light_name, type='SUN')
    light_data.energy = 5.0
    light_data.angle = math.radians(11.4)  # Slight softness to the shadows
    
    light_obj = bpy.data.objects.new(name=light_name, object_data=light_data)
    scene.collection.objects.link(light_obj)
    
    light_obj.location = (location[0], location[1], location[2] + (5.0 * scale))
    # Angle the sun at 45 degrees
    light_obj.rotation_euler = (math.radians(45), math.radians(15), math.radians(45))
    
    # === Step 4: PBR Material Setup ===
    mat_name = f"{object_name}_PBR_Mat"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    
    # CRITICAL: Tell Cycles to use actual geometric displacement, not just bump
    mat.cycles.displacement_method = 'DISPLACEMENT'
    
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
        
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Core Shader Nodes
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = (800, 0)
    
    node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_principled.location = (500, 0)
    
    node_disp = nodes.new(type='ShaderNodeDisplacement')
    node_disp.location = (500, -300)
    node_disp.inputs['Scale'].default_value = 0.25 * scale
    node_disp.inputs['Midlevel'].default_value = 0.0
    
    # Texture Coordinates
    node_tc = nodes.new(type='ShaderNodeTexCoord')
    node_tc.location = (-700, 0)
    
    node_mapping = nodes.new(type='ShaderNodeMapping')
    node_mapping.location = (-500, 0)
    node_mapping.inputs['Scale'].default_value = (3.0, 3.0, 3.0)
    
    # Procedural Base Color
    node_noise_col = nodes.new(type='ShaderNodeTexNoise')
    node_noise_col.location = (-200, 200)
    node_noise_col.inputs['Scale'].default_value = 10.0
    node_noise_col.inputs['Detail'].default_value = 15.0
    
    node_ramp_col = nodes.new(type='ShaderNodeValToRGB')
    node_ramp_col.location = (100, 200)
    node_ramp_col.color_ramp.elements[0].color = (material_color[0]*0.3, material_color[1]*0.3, material_color[2]*0.3, 1.0)
    node_ramp_col.color_ramp.elements[1].color = (material_color[0], material_color[1], material_color[2], 1.0)
    
    # Procedural Roughness
    node_noise_rough = nodes.new(type='ShaderNodeTexNoise')
    node_noise_rough.location = (-200, -100)
    node_noise_rough.inputs['Scale'].default_value = 5.0
    
    node_ramp_rough = nodes.new(type='ShaderNodeValToRGB')
    node_ramp_rough.location = (100, -100)
    node_ramp_rough.color_ramp.elements[0].position = 0.4
    node_ramp_rough.color_ramp.elements[0].color = (0.6, 0.6, 0.6, 1.0)
    node_ramp_rough.color_ramp.elements[1].position = 0.8
    node_ramp_rough.color_ramp.elements[1].color = (0.9, 0.9, 0.9, 1.0)
    
    # Procedural Displacement (Rock Wall Simulation via Voronoi Distance to Edge)
    node_voronoi = nodes.new(type='ShaderNodeTexVoronoi')
    node_voronoi.location = (-200, -400)
    node_voronoi.feature = 'DISTANCE_TO_EDGE'
    node_voronoi.inputs['Scale'].default_value = 4.0
    
    # Shape the cracks so the stones have flat, elevated tops with deep crevices
    node_ramp_disp = nodes.new(type='ShaderNodeValToRGB')
    node_ramp_disp.location = (100, -400)
    node_ramp_disp.color_ramp.elements[0].position = 0.05
    node_ramp_disp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    node_ramp_disp.color_ramp.elements[1].position = 0.2
    node_ramp_disp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    
    # Normal Bump map to support the macro-displacement
    node_bump = nodes.new(type='ShaderNodeBump')
    node_bump.location = (100, -700)
    node_bump.inputs['Distance'].default_value = 0.5
    
    # === Step 5: Wire the Node Tree ===
    links.new(node_tc.outputs['Object'], node_mapping.inputs['Vector'])
    
    # Wiring Color
    links.new(node_mapping.outputs['Vector'], node_noise_col.inputs['Vector'])
    links.new(node_noise_col.outputs['Fac'], node_ramp_col.inputs['Fac'])
    links.new(node_ramp_col.outputs['Color'], node_principled.inputs['Base Color'])
    
    # Wiring Roughness
    links.new(node_mapping.outputs['Vector'], node_noise_rough.inputs['Vector'])
    links.new(node_noise_rough.outputs['Fac'], node_ramp_rough.inputs['Fac'])
    links.new(node_ramp_rough.outputs['Color'], node_principled.inputs['Roughness'])
    
    # Wiring Displacement and Bump
    links.new(node_mapping.outputs['Vector'], node_voronoi.inputs['Vector'])
    links.new(node_voronoi.outputs['Distance'], node_ramp_disp.inputs['Fac'])
    
    links.new(node_ramp_disp.outputs['Color'], node_disp.inputs['Height'])
    links.new(node_ramp_disp.outputs['Color'], node_bump.inputs['Height'])
    links.new(node_bump.outputs['Normal'], node_principled.inputs['Normal'])
    
    # Final Output Wiring
    links.new(node_principled.outputs['BSDF'], node_output.inputs['Surface'])
    links.new(node_disp.outputs['Displacement'], node_output.inputs['Displacement'])
    
    return f"Created '{object_name}' with PBR true displacement and '{light_name}' Sun light. Engine set to CYCLES."
