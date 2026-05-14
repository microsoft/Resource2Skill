def create_pbr_displacement_plane(
    scene_name: str = "Scene",
    object_name: str = "PBR_Rock_Plane",
    location: tuple = (0, 0, 0),
    scale: float = 2.0,
    material_color: tuple = (0.2, 0.15, 0.1),
    **kwargs,
) -> str:
    """
    Create a procedural PBR rock material with true displacement on a subdivided plane.
    Recreates the core workflow of applying true displacement in Cycles.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created plane.
        location: (x, y, z) world-space position.
        scale: Size scale of the plane.
        material_color: (R, G, B) base color for the top surface of the rock.
        **kwargs: Additional overrides.

    Returns:
        Status string confirming creation.
    """
    import bpy
    import math

    # Get scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Enforce Cycles Engine ===
    # True material displacement relies heavily on Cycles
    scene.render.engine = 'CYCLES'
    
    # === Step 2: Create Dense Base Geometry ===
    # Multiply size by scale directly to avoid needing to apply transforms later
    bpy.ops.mesh.primitive_plane_add(size=2.0 * scale, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    
    # Add Subdivision Surface modifier for heavy geometry (replacing manual edit-mode sub-D)
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 6        # High density for viewport preview
    subsurf.render_levels = 8 # Extremely dense for final Cycles render
    
    # === Step 3: Create Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    # THE MOST CRITICAL STEP: Tell Cycles to actually move the mesh, not just fake bump
    mat.cycles.displacement_method = 'DISPLACEMENT'
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear unnecessary default nodes
    for node in nodes:
        if node.type not in {'BSDF_PRINCIPLED', 'OUTPUT_MATERIAL'}:
            nodes.remove(node)
            
    principled = nodes.get("Principled BSDF")
    if not principled: 
        principled = nodes.new('ShaderNodeBsdfPrincipled')
    output = nodes.get("Material Output")
    
    # --- Procedural PBR Texture Generation ---
    # 1. Voronoi for structural cracks (simulating stone blocks)
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.feature = 'DISTANCE_TO_EDGE'
    voronoi.inputs['Scale'].default_value = 3.0
    
    # 2. Noise for fine surface grit
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 10.0
    noise.inputs['Detail'].default_value = 15.0
    
    # 3. Combine Voronoi and Noise to form the master Height Map
    math_mult = nodes.new('ShaderNodeMath')
    math_mult.operation = 'MULTIPLY'
    math_mult.inputs[1].default_value = 0.3
    links.new(noise.outputs['Fac'], math_mult.inputs[0])
    
    math_add = nodes.new('ShaderNodeMath')
    math_add.operation = 'ADD'
    links.new(voronoi.outputs['Distance'], math_add.inputs[0])
    links.new(math_mult.outputs['Value'], math_add.inputs[1])
    
    # 4. Base Color Ramp (Dark cracks, colored surface)
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.color_ramp.elements[0].color = (0.01, 0.01, 0.01, 1.0) 
    color_ramp.color_ramp.elements[1].color = material_color + (1.0,) 
    links.new(math_add.outputs['Value'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
    
    # 5. Roughness Ramp
    rough_ramp = nodes.new('ShaderNodeValToRGB')
    rough_ramp.color_ramp.elements[0].color = (0.7, 0.7, 0.7, 1.0)
    rough_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    links.new(math_add.outputs['Value'], rough_ramp.inputs['Fac'])
    links.new(rough_ramp.outputs['Color'], principled.inputs['Roughness'])
    
    # 6. Normal (Bump) Map
    bump = nodes.new('ShaderNodeBump')
    bump.inputs['Distance'].default_value = 0.2
    links.new(math_add.outputs['Value'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], principled.inputs['Normal'])
    
    # 7. True Displacement Node
    disp = nodes.new('ShaderNodeDisplacement')
    disp.inputs['Midlevel'].default_value = 0.0
    disp.inputs['Scale'].default_value = 0.5 * scale # Extrusion amount relative to scale
    links.new(math_add.outputs['Value'], disp.inputs['Height'])
    links.new(disp.outputs['Displacement'], output.inputs['Displacement'])
    
    # Assign material to object
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat
    
    # === Step 4: Add Angled Lighting ===
    # True displacement is invisible without sharp shadows. We add a sun if one isn't present.
    sun_exists = False
    for obj_lit in scene.objects:
        if obj_lit.type == 'LIGHT' and obj_lit.data.type == 'SUN':
            sun_exists = True
            break
            
    if not sun_exists:
        sun_data = bpy.data.lights.new(name="Sun_Displacement_Light", type='SUN')
        sun_data.energy = 5.0 # High strength to match tutorial
        sun_data.angle = 0.1  # Sharp shadows
        sun = bpy.data.objects.new(name="Sun_Displacement_Light", object_data=sun_data)
        scene.collection.objects.link(sun)
        
        # Position slightly above and angle to rake across the surface
        sun.location = (location[0], location[1], location[2] + 5)
        sun.rotation_euler = (math.radians(45), math.radians(45), 0)
        
    return f"Created '{object_name}' (PBR True Displaced Plane) with Cycles displacement at {location}"
