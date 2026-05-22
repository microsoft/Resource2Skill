def create_pbr_displacement_surface(
    scene_name: str = "Scene",
    object_name: str = "DisplacedRockWall",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.43, 0.31, 0.22),
    subdivision_level: int = 6,
    displacement_scale: float = 0.3,
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with true physical displacement in Cycles.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created plane.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the rock surface.
        subdivision_level: Density of the mesh (higher = more detailed displacement).
        displacement_scale: Intensity of the depth extrusion.

    Returns:
        Status string confirming creation.
    """
    import bpy
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Force Render Engine Context ===
    # True material displacement ONLY works in Cycles
    scene.render.engine = 'CYCLES'
    
    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Add Subdivision Surface Modifier to provide geometry for displacement
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = subdivision_level
    subsurf.render_levels = subdivision_level

    # === Step 3: Build Procedural PBR Displacement Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    # CRITICAL: Set material to actually displace geometry, not just bump
    mat.cycles.displacement_method = 'DISPLACEMENT'
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes if necessary
    for node in nodes:
        nodes.remove(node)
        
    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (400, 0)
    
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (100, 100)
    bsdf.inputs['Roughness'].default_value = 0.85 # High roughness for rock
    bsdf.inputs['Metallic'].default_value = 0.0
    
    # Create Procedural "Height/Color" Map (Replaces external image dependency)
    noise = nodes.new("ShaderNodeTexNoise")
    noise.location = (-500, 0)
    noise.inputs['Scale'].default_value = 4.0
    noise.inputs['Detail'].default_value = 15.0
    noise.inputs['Roughness'].default_value = 0.7
    
    # Color mapping
    color_ramp = nodes.new("ShaderNodeValToRGB")
    color_ramp.location = (-200, 100)
    color_ramp.color_ramp.elements[0].position = 0.35
    color_ramp.color_ramp.elements[0].color = (0.05, 0.04, 0.03, 1.0) # Deep shadow color
    color_ramp.color_ramp.elements[1].position = 0.65
    color_ramp.color_ramp.elements[1].color = (*material_color, 1.0)  # Base rock color
    
    # Displacement Node Setup
    disp = nodes.new("ShaderNodeDisplacement")
    disp.location = (100, -200)
    disp.inputs['Midlevel'].default_value = 0.5
    disp.inputs['Scale'].default_value = displacement_scale
    
    # Link everything together
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
    
    links.new(noise.outputs['Fac'], disp.inputs['Height'])
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    links.new(disp.outputs['Displacement'], output.inputs['Displacement'])
    
    # Assign material to object
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    # === Step 4: Add Complementary Lighting (from tutorial) ===
    # Add a Sun light to cast shadows across the newly displaced geometry
    light_data = bpy.data.lights.new(name=f"{object_name}_Sun", type='SUN')
    light_data.energy = 5.0
    light_data.angle = 0.1989 # ~11.4 degrees for slightly soft shadows
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_Sun", object_data=light_data)
    scene.collection.objects.link(light_obj)
    light_obj.location = (location[0], location[1] - 3.0, location[2] + 4.0)
    
    # Angle the sun to scrape across the surface
    light_obj.rotation_euler = (math.radians(60), 0, math.radians(20))

    return f"Created '{object_name}' with True Displacement material at {location}. Cycles engine enabled."
