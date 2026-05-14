def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Surface",
    location: tuple = (0, 0, 0),
    scale: float = 5.0,
    material_color: tuple = (0.5, 0.4, 0.3),
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with a true PBR displacement material.
    Switches to Cycles to enable physical vertex displacement at render time.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created mesh.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (size of the surface).
        material_color: (R, G, B) base color for the top surface of the rocks.
        **kwargs: Can include 'subdivisions' (default 100).

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Switch Render Engine to Cycles ===
    # True displacement is a Cycles-specific feature
    scene.render.engine = 'CYCLES'

    # === Step 2: Create Dense Geometry ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    # Use bmesh to create a dense grid (100x100 = 10,000 faces)
    # Required for the displacement map to have enough vertices to push around
    bm = bmesh.new()
    subdivs = kwargs.get('subdivisions', 100)
    bmesh.ops.create_grid(bm, x_segments=subdivs, y_segments=subdivs, size=scale)
    bm.to_mesh(mesh)
    bm.free()
    
    obj.location = Vector(location)
    
    # Smooth shading
    for poly in mesh.polygons:
        poly.use_smooth = True

    # === Step 3: Configure Material for True Displacement ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    # THE MOST CRITICAL SETTING: Change from 'BUMP' to 'DISPLACEMENT'
    mat.cycles.displacement_method = 'DISPLACEMENT'
    
    # === Step 4: Build Procedural PBR Node Tree ===
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1000, 0)
    
    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (600, 200)
    links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])
    
    # Texture Coordinates
    coord_node = nodes.new('ShaderNodeTexCoord')
    coord_node.location = (-800, 200)
    mapping_node = nodes.new('ShaderNodeMapping')
    mapping_node.location = (-600, 200)
    links.new(coord_node.outputs['UV'], mapping_node.inputs['Vector'])
    
    # Macro shape: Voronoi (Simulates rocks / cracked wall structure)
    voronoi_node = nodes.new('ShaderNodeTexVoronoi')
    voronoi_node.location = (-400, 200)
    voronoi_node.feature = 'DISTANCE_TO_EDGE'
    voronoi_node.inputs['Scale'].default_value = 5.0
    links.new(mapping_node.outputs['Vector'], voronoi_node.inputs['Vector'])
    
    # Micro detail: Noise (Simulates surface grit / bump)
    noise_node = nodes.new('ShaderNodeTexNoise')
    noise_node.location = (-400, -100)
    noise_node.inputs['Scale'].default_value = 20.0
    noise_node.inputs['Detail'].default_value = 15.0
    links.new(mapping_node.outputs['Vector'], noise_node.inputs['Vector'])
    
    # --> Base Color
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-100, 300)
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (0.02, 0.015, 0.01, 1.0) # Deep dark cracks
    color_ramp.color_ramp.elements[1].position = 0.1
    color_ramp.color_ramp.elements[1].color = (*material_color, 1.0) # Surface rock color
    links.new(voronoi_node.outputs['Distance'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf_node.inputs['Base Color'])
    
    # --> Roughness
    math_roughness = nodes.new('ShaderNodeMath')
    math_roughness.operation = 'ADD'
    math_roughness.location = (-100, 100)
    links.new(voronoi_node.outputs['Distance'], math_roughness.inputs[0])
    links.new(noise_node.outputs['Fac'], math_roughness.inputs[1])
    
    roughness_ramp = nodes.new('ShaderNodeValToRGB')
    roughness_ramp.location = (100, 100)
    roughness_ramp.color_ramp.elements[0].position = 0.0
    roughness_ramp.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1.0)
    roughness_ramp.color_ramp.elements[1].position = 1.0
    roughness_ramp.color_ramp.elements[1].color = (0.95, 0.95, 0.95, 1.0)
    links.new(math_roughness.outputs['Value'], roughness_ramp.inputs['Fac'])
    links.new(roughness_ramp.outputs['Color'], bsdf_node.inputs['Roughness'])
    
    # --> Normal/Bump
    bump_node = nodes.new('ShaderNodeBump')
    bump_node.location = (200, -100)
    bump_node.inputs['Strength'].default_value = 0.5
    bump_node.inputs['Distance'].default_value = 0.1
    links.new(noise_node.outputs['Fac'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], bsdf_node.inputs['Normal'])
    
    # --> True Displacement Mapping
    math_add_noise = nodes.new('ShaderNodeMath')
    math_add_noise.operation = 'ADD'
    math_add_noise.location = (100, -300)
    links.new(voronoi_node.outputs['Distance'], math_add_noise.inputs[0])
    
    math_scale_noise = nodes.new('ShaderNodeMath')
    math_scale_noise.operation = 'MULTIPLY'
    math_scale_noise.inputs[1].default_value = 0.1
    math_scale_noise.location = (-100, -400)
    links.new(noise_node.outputs['Fac'], math_scale_noise.inputs[0])
    links.new(math_scale_noise.outputs['Value'], math_add_noise.inputs[1])

    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (300, -300)
    disp_node.inputs['Midlevel'].default_value = 0.0
    disp_node.inputs['Scale'].default_value = 0.2 * scale 
    links.new(math_add_noise.outputs['Value'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])
    
    # === Step 5: Add Sun Light to highlight Displacement ===
    light_name = "Displacement_SunLight"
    if light_name not in bpy.data.objects:
        light_data = bpy.data.lights.new(name=light_name, type='SUN')
        light_data.energy = 5.0
        light_data.angle = math.radians(10.0) # Sharp shadows to accentuate rock crevices
        light_obj = bpy.data.objects.new(name=light_name, object_data=light_data)
        scene.collection.objects.link(light_obj)
        light_obj.location = (location[0], location[1], location[2] + 10)
        # Angled dramatically to catch the displaced edges
        light_obj.rotation_euler = (math.radians(60), math.radians(0), math.radians(45))

    return f"Created PBR Displaced Surface '{object_name}' with {len(mesh.polygons)} faces at {location}. Cycles engine enabled."
