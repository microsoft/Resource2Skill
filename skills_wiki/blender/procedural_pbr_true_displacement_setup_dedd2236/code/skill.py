def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Terrain",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 2.0,
    material_color: tuple = (0.35, 0.25, 0.18),
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with true procedural PBR displacement in Cycles.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the terrain plane.
        material_color: (R, G, B) primary color for the displaced material.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Engine Setup ===
    # True displacement requires Cycles to render properly
    scene.render.engine = 'CYCLES'
    
    # === Step 2: Create Base Geometry ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    bm = bmesh.new()
    v1 = bm.verts.new((-1.0, -1.0, 0.0))
    v2 = bm.verts.new((1.0, -1.0, 0.0))
    v3 = bm.verts.new((1.0, 1.0, 0.0))
    v4 = bm.verts.new((-1.0, 1.0, 0.0))
    bm.faces.new((v1, v2, v3, v4))
    bm.to_mesh(mesh)
    bm.free()
    
    # Add heavy subdivision for physical displacement (Level 8 = 65,536 faces)
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE' # Keeps boundaries square
    subsurf.levels = 8
    subsurf.render_levels = 8
    
    # === Step 3: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    # CRITICAL: Tell Cycles to actually displace the geometry, not just bump map it
    mat.cycles.displacement_method = 'DISPLACEMENT'
    
    obj.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Base nodes
    node_output = nodes.new('ShaderNodeOutputMaterial')
    node_output.location = (800, 0)
    
    node_principled = nodes.new('ShaderNodeBsdfPrincipled')
    node_principled.location = (400, 0)
    
    node_disp = nodes.new('ShaderNodeDisplacement')
    node_disp.location = (400, -300)
    node_disp.inputs['Midlevel'].default_value = 0.5
    node_disp.inputs['Scale'].default_value = 0.3
    
    # Procedural Noise Engine
    node_noise = nodes.new('ShaderNodeTexNoise')
    node_noise.location = (-200, 0)
    node_noise.inputs['Scale'].default_value = 3.5
    node_noise.inputs['Detail'].default_value = 15.0
    node_noise.inputs['Roughness'].default_value = 0.65
    
    # Color mapping
    node_colorramp = nodes.new('ShaderNodeValToRGB')
    node_colorramp.location = (100, 150)
    node_colorramp.color_ramp.elements[0].color = (0.02, 0.02, 0.02, 1.0)
    node_colorramp.color_ramp.elements[1].color = (material_color[0], material_color[1], material_color[2], 1.0)
    
    # Roughness mapping (recesses are rough, peaks are slightly less rough)
    node_roughramp = nodes.new('ShaderNodeValToRGB')
    node_roughramp.location = (100, -100)
    node_roughramp.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1.0)
    node_roughramp.color_ramp.elements[1].color = (0.9, 0.9, 0.9, 1.0)
    
    # Wiring
    links.new(node_noise.outputs['Fac'], node_colorramp.inputs['Fac'])
    links.new(node_noise.outputs['Fac'], node_roughramp.inputs['Fac'])
    links.new(node_noise.outputs['Fac'], node_disp.inputs['Height'])
    
    links.new(node_colorramp.outputs['Color'], node_principled.inputs['Base Color'])
    links.new(node_roughramp.outputs['Color'], node_principled.inputs['Roughness'])
    
    links.new(node_principled.outputs['BSDF'], node_output.inputs['Surface'])
    links.new(node_disp.outputs['Displacement'], node_output.inputs['Displacement'])
    
    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    # === Step 5: Setup Lighting to Showcase Displacement ===
    sun_data = bpy.data.lights.new(name=f"{object_name}_Sun", type='SUN')
    sun_data.energy = 5.0
    sun_data.angle = 0.1 # Sharp shadows to accentuate depth
    sun_obj = bpy.data.objects.new(name=f"{object_name}_Sun", object_data=sun_data)
    scene.collection.objects.link(sun_obj)
    
    sun_loc = Vector(location) + Vector((5.0, -5.0, 7.0))
    sun_obj.location = sun_loc
    
    # Orient the sun to point directly at the terrain center
    direction = Vector(location) - sun_loc
    sun_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    return f"Created '{object_name}' with True Displacement (Cycles enabled) and directional Sun light at {location}"
