def create_pbr_displacement_plane(
    scene_name: str = "Scene",
    object_name: str = "PBR_RockPlane",
    location: tuple = (0, 0, 0),
    scale: float = 2.0,
    base_color_rock: tuple = (0.25, 0.20, 0.15), 
    base_color_crevice: tuple = (0.02, 0.02, 0.02),
    displacement_scale: float = 0.2,
    subdivision_level: int = 6,
    **kwargs
) -> str:
    """
    Creates a highly subdivided plane with a procedural PBR rock material that uses 
    true geometric displacement in Cycles.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name of the plane object.
        location: (x, y, z) coordinates.
        scale: Size of the plane.
        base_color_rock: RGB tuple for the high points.
        base_color_crevice: RGB tuple for the deep cracks.
        displacement_scale: Height modifier for the geometric displacement.
        subdivision_level: Density of the mesh (higher = more detail, slower render).
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Geometry Setup ===
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Apply scale to ensure displacement height is uniform
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Add Subdivision Surface Modifier to generate geometry for displacement
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = subdivision_level
    subsurf.render_levels = subdivision_level
    
    # === Step 2: Material & Node Setup ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    # CRITICAL: Tell Cycles to actually move the vertices
    mat.cycles.displacement_method = 'DISPLACEMENT'
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Clean slate
    
    # Outputs
    mat_out = nodes.new('ShaderNodeOutputMaterial')
    mat_out.location = (800, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (400, 0)
    links.new(bsdf.outputs['BSDF'], mat_out.inputs['Surface'])
    
    # Coordinates
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)
    
    # Macro Detail: Voronoi Cracks (Used for Displacement and Base Color)
    voronoi_cracks = nodes.new('ShaderNodeTexVoronoi')
    voronoi_cracks.feature = 'DISTANCE_TO_EDGE' # Creates a cracked plate pattern
    voronoi_cracks.inputs['Scale'].default_value = 3.5
    voronoi_cracks.location = (-800, 200)
    links.new(tex_coord.outputs['Object'], voronoi_cracks.inputs['Vector'])
    
    # Sharpen cracks via ColorRamp
    crack_ramp = nodes.new('ShaderNodeValToRGB')
    crack_ramp.location = (-500, 200)
    crack_ramp.color_ramp.elements[0].position = 0.00
    crack_ramp.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0) # High flat plates
    crack_ramp.color_ramp.elements[1].position = 0.15
    crack_ramp.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1.0) # Deep black cracks
    links.new(voronoi_cracks.outputs['Distance'], crack_ramp.inputs['Fac'])
    
    # Micro Detail: Noise (Used for Bump and Roughness)
    noise_detail = nodes.new('ShaderNodeTexNoise')
    noise_detail.inputs['Scale'].default_value = 25.0
    noise_detail.inputs['Detail'].default_value = 15.0
    noise_detail.location = (-800, -200)
    links.new(tex_coord.outputs['Object'], noise_detail.inputs['Vector'])
    
    # --- Connect Channels ---
    
    # 1. Base Color
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-200, 300)
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (*base_color_crevice, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.5
    color_ramp.color_ramp.elements[1].color = (*base_color_rock, 1.0)
    links.new(crack_ramp.outputs['Color'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
    
    # 2. Roughness
    rough_ramp = nodes.new('ShaderNodeValToRGB')
    rough_ramp.location = (-200, -100)
    rough_ramp.color_ramp.elements[0].position = 0.2
    rough_ramp.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1.0)
    rough_ramp.color_ramp.elements[1].position = 0.8
    rough_ramp.color_ramp.elements[1].color = (0.9, 0.9, 0.9, 1.0)
    links.new(noise_detail.outputs['Fac'], rough_ramp.inputs['Fac'])
    links.new(rough_ramp.outputs['Color'], bsdf.inputs['Roughness'])
    
    # 3. Normal (Micro Bump)
    bump = nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.4
    bump.location = (100, -300)
    links.new(noise_detail.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    
    # 4. Displacement (Macro Height)
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.inputs['Midlevel'].default_value = 0.5
    disp_node.inputs['Scale'].default_value = displacement_scale
    disp_node.location = (400, -400)
    links.new(crack_ramp.outputs['Color'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], mat_out.inputs['Displacement'])
    
    # === Step 3: Scene Context Setup ===
    # Switch to Cycles to activate the displacement
    scene.render.engine = 'CYCLES'
    
    # Add dramatic angled lighting as shown in the video
    sun_name = f"{object_name}_Sun"
    if sun_name not in bpy.data.objects:
        light_data = bpy.data.lights.new(name=sun_name, type='SUN')
        light_data.energy = 5.0
        light_data.angle = math.radians(10.0) # Slight shadow softening
        sun_obj = bpy.data.objects.new(name=sun_name, object_data=light_data)
        scene.collection.objects.link(sun_obj)
        
        sun_obj.location = (location[0] + 5, location[1] - 5, location[2] + 10)
        # Point the sun towards the plane with a raking angle
        sun_obj.rotation_euler = (math.radians(45), math.radians(30), math.radians(45))
    
    return f"Created PBR Displacement Plane '{object_name}' with sub-div level {subdivision_level}. Render engine switched to Cycles."
