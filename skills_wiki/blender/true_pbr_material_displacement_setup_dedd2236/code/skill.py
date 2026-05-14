def create_pbr_displaced_ground(
    scene_name: str = "Scene",
    object_name: str = "DisplacedGround",
    location: tuple = (0, 0, 0),
    scale: float = 5.0,
    base_color_dark: tuple = (0.05, 0.03, 0.02),
    base_color_light: tuple = (0.25, 0.18, 0.12),
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with true PBR material displacement.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the ground plane.
        base_color_dark: (R, G, B) dark tone for the procedural texture.
        base_color_light: (R, G, B) light tone for the procedural texture.
        **kwargs: Optional 'subdiv_levels' (int, default=6), 'displacement_strength' (float, default=0.5).
        
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector, Euler
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    
    # Extract kwargs
    subdiv_levels = kwargs.get('subdiv_levels', 6)
    displacement_strength = kwargs.get('displacement_strength', 0.5)

    # === Step 1: Engine Setup ===
    # True material displacement requires the Cycles render engine
    scene.render.engine = 'CYCLES'
    if hasattr(scene, 'cycles'):
        scene.cycles.feature_set = 'SUPPORTED'

    # === Step 2: Create Base Geometry ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    # Construct a default plane (size 2x2) using bmesh
    bm = bmesh.new()
    verts = [
        bm.verts.new((-1.0, -1.0, 0.0)),
        bm.verts.new((1.0, -1.0, 0.0)),
        bm.verts.new((1.0, 1.0, 0.0)),
        bm.verts.new((-1.0, 1.0, 0.0))
    ]
    bm.faces.new(verts)
    bm.to_mesh(mesh)
    bm.free()
    
    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))
    
    # Add Subdivision Modifier to provide the density required for displacement
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = subdiv_levels
    subsurf.render_levels = subdiv_levels

    # === Step 3: Build Material & Shader Node Tree ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    # **CRITICAL STEP**: Tell Cycles to physically displace the mesh, not just bump map it
    mat.cycles.displacement_method = 'DISPLACEMENT_ONLY'
    obj.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Output & BSDF
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (1000, 0)
    
    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf_node.location = (600, 0)
    
    # Texture Coordinates
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    
    # Procedural Noise (Acting as our downloaded height map)
    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.location = (-200, 0)
    noise.inputs['Scale'].default_value = 3.0
    noise.inputs['Detail'].default_value = 15.0
    noise.inputs['Roughness'].default_value = 0.65
    noise.inputs['Distortion'].default_value = 0.1
    
    # Color Ramp for Base Color
    ramp_color = nodes.new(type='ShaderNodeValToRGB')
    ramp_color.location = (200, 200)
    ramp_color.color_ramp.elements[0].color = (*base_color_dark, 1.0)
    ramp_color.color_ramp.elements[1].color = (*base_color_light, 1.0)
    
    # Color Ramp for Roughness (High values to simulate dry rock/dirt)
    ramp_rough = nodes.new(type='ShaderNodeValToRGB')
    ramp_rough.location = (200, -100)
    ramp_rough.color_ramp.elements[0].color = (0.6, 0.6, 0.6, 1.0)
    ramp_rough.color_ramp.elements[1].color = (0.9, 0.9, 0.9, 1.0)
    
    # Displacement Node (Translating noise values into physical height)
    disp_node = nodes.new(type='ShaderNodeDisplacement')
    disp_node.location = (600, -300)
    disp_node.inputs['Scale'].default_value = displacement_strength
    
    # Connect everything
    links.new(tex_coord.outputs['Generated'], noise.inputs['Vector'])
    
    links.new(noise.outputs['Fac'], ramp_color.inputs['Fac'])
    links.new(ramp_color.outputs['Color'], bsdf_node.inputs['Base Color'])
    
    links.new(noise.outputs['Fac'], ramp_rough.inputs['Fac'])
    links.new(ramp_rough.outputs['Color'], bsdf_node.inputs['Roughness'])
    
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
    
    # Drive the displacement output using the same noise map
    links.new(noise.outputs['Fac'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], output_node.inputs['Displacement'])

    # === Step 4: Lighting (To reveal the displacement) ===
    # Ensure there's a light source to cast shadows on the micro-geometry
    sun_data = bpy.data.lights.new(name=f"{object_name}_Sun", type='SUN')
    sun_data.energy = 5.0
    sun_obj = bpy.data.objects.new(f"{object_name}_SunObj", sun_data)
    scene.collection.objects.link(sun_obj)
    
    sun_obj.location = Vector((location[0] + 5, location[1] - 5, location[2] + 10))
    sun_obj.rotation_euler = Euler((math.radians(45), 0, math.radians(45)), 'XYZ')

    return f"Created procedural PBR displaced plane '{object_name}' and accompanying sun light. Switch viewport to Cycles Render to view."
