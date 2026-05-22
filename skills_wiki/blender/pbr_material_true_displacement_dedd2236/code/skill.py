def create_pbr_displacement_surface(
    scene_name: str = "Scene",
    object_name: str = "DisplacedRockWall",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 2.0,
    subdivision_level: int = 4,
    displacement_scale: float = 0.25,
    base_color_dark: tuple = (0.02, 0.015, 0.01),
    base_color_light: tuple = (0.4, 0.3, 0.25),
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with a procedural PBR displacement material.
    Replicates the true-displacement technique using the Cycles render engine.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the plane.
        subdivision_level: Density of the subdivision modifier (higher = more detail, slower).
        displacement_scale: Height multiplier for the surface displacement.
        base_color_dark: (R, G, B) color for the deep cracks.
        base_color_light: (R, G, B) color for the high rock faces.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 0: Ensure Cycles is Active ===
    # True displacement requires the Cycles render engine
    scene.render.engine = 'CYCLES'
    
    # === Step 1: Base Geometry & Subdivision ===
    mesh = bpy.data.meshes.new(object_name + "_mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    # Create a pre-subdivided grid (20x20 = 400 faces)
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=20, y_segments=20, size=2.0)
    bm.to_mesh(mesh)
    bm.free()
    
    # Add a Subdivision Surface modifier set to SIMPLE to multiply geometry density
    # Level 4 on a 400 face grid yields ~102,400 faces (perfect for displacement)
    subsurf = obj.modifiers.new("Subdivision", 'SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = subdivision_level
    subsurf.render_levels = subdivision_level
    
    # === Step 2: Procedural PBR Material Setup ===
    mat = bpy.data.materials.new(name=object_name + "_Material")
    mat.use_nodes = True
    
    # CRITICAL: Tell Cycles to use actual geometry displacement, not just bump
    if hasattr(mat, 'cycles'):
        mat.cycles.displacement_method = 'DISPLACEMENT'
        
    obj.data.materials.append(mat)
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Output & BSDF Nodes
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1000, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (600, 0)
    bsdf.inputs['Roughness'].default_value = 0.85
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])
    
    # Displacement Node
    disp = nodes.new('ShaderNodeDisplacement')
    disp.location = (600, -300)
    disp.inputs['Scale'].default_value = displacement_scale
    disp.inputs['Midlevel'].default_value = 0.0
    links.new(disp.outputs['Displacement'], out_node.inputs['Displacement'])
    
    # Texture Generation: Voronoi for the primary cracked rock structure
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-400, 0)
    voronoi.feature = 'DISTANCE_TO_EDGE'
    voronoi.inputs['Scale'].default_value = 4.0
    
    # Base Color Ramp
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (0, 100)
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (*base_color_dark, 1.0)
    
    # Calculate a mid-tone color
    mid_color = (
        (base_color_dark[0] + base_color_light[0]) / 2, 
        (base_color_dark[1] + base_color_light[1]) / 2, 
        (base_color_dark[2] + base_color_light[2]) / 2
    )
    
    color_ramp.color_ramp.elements[1].position = 0.15
    color_ramp.color_ramp.elements[1].color = (*mid_color, 1.0)
    
    el = color_ramp.color_ramp.elements.new(0.6)
    el.color = (*base_color_light, 1.0)
    
    links.new(voronoi.outputs['Distance'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
    
    # Height Shaping Ramp (Plateaus the rocks, keeps deep cracks)
    height_ramp = nodes.new('ShaderNodeValToRGB')
    height_ramp.location = (0, -200)
    height_ramp.color_ramp.elements[0].position = 0.02
    height_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    height_ramp.color_ramp.elements[1].position = 0.3
    height_ramp.color_ramp.elements[1].color = (0.8, 0.8, 0.8, 1.0)
    links.new(voronoi.outputs['Distance'], height_ramp.inputs['Fac'])
    
    # Surface Noise (Grittiness)
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-200, -450)
    noise.inputs['Scale'].default_value = 25.0
    
    noise_scale = nodes.new('ShaderNodeMath')
    noise_scale.operation = 'MULTIPLY'
    noise_scale.inputs[1].default_value = 0.05
    noise_scale.location = (0, -450)
    links.new(noise.outputs['Fac'], noise_scale.inputs[0])
    
    # Combine Height Shapes and Noise Detail
    add_height = nodes.new('ShaderNodeMath')
    add_height.operation = 'ADD'
    add_height.location = (300, -300)
    links.new(height_ramp.outputs['Color'], add_height.inputs[0])
    links.new(noise_scale.outputs['Value'], add_height.inputs[1])
    links.new(add_height.outputs['Value'], disp.inputs['Height'])
    
    # === Step 3: Hard-Shadow Lighting ===
    # A Sun light with low angle size to cast distinct shadows in the displacement
    light_data = bpy.data.lights.new(name=object_name + "_Sun", type='SUN')
    light_data.energy = 5.0
    light_data.angle = math.radians(11.4) # Exact angle from tutorial
    
    light_obj = bpy.data.objects.new(name=object_name + "_SunObj", object_data=light_data)
    scene.collection.objects.link(light_obj)
    
    light_obj.location = (location[0], location[1], location[2] + 5.0)
    light_obj.rotation_euler = (math.radians(45), math.radians(30), 0)
    
    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    return f"Created '{object_name}' with procedural true displacement. Render engine set to Cycles."
