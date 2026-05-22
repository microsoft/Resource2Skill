def create_object(
    scene_name: str = "Scene",
    object_name: str = "Displaced_PBR_Surface",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 2.0,
    material_color: tuple = (0.35, 0.25, 0.20),
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with true PBR Micro-Displacement in Cycles.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the plane and displacement depth.
        material_color: (R, G, B) base color mapping for the procedural texture.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created setup.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Switch Render Engine to Cycles ===
    # True material displacement is a Cycles-exclusive feature.
    scene.render.engine = 'CYCLES'

    # === Step 2: Create Geometry ===
    # Using bmesh to create a dense base grid to support displacement
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=50, y_segments=50, size=scale)
    me = bpy.data.meshes.new(object_name + "_Mesh")
    bm.to_mesh(me)
    bm.free()

    obj = bpy.data.objects.new(object_name, me)
    scene.collection.objects.link(obj)
    obj.location = Vector(location)

    # Add Subdivision Surface Modifier for micro-polygon density
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 3

    # === Step 3: Material & PBR Setup ===
    mat = bpy.data.materials.new(name=object_name + "_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)

    # CRITICAL: Tell Cycles to use true physical displacement, not just bump maps.
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for n in nodes:
        nodes.remove(n)

    # Material Output
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (400, 0)

    # Principled BSDF
    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (0, 0)
    links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])

    # Displacement Node
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (0, -300)
    disp_node.inputs['Scale'].default_value = 0.2 * scale
    disp_node.inputs['Midlevel'].default_value = 0.5
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])

    # Procedural Texture (Mimicking the downloaded PBR Maps from the tutorial)
    noise_node = nodes.new('ShaderNodeTexNoise')
    noise_node.location = (-600, 0)
    noise_node.inputs['Scale'].default_value = 4.0
    noise_node.inputs['Detail'].default_value = 15.0
    noise_node.inputs['Roughness'].default_value = 0.6

    # Color Ramp for Base Color (Simulating Albedo map)
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-300, 100)
    color_ramp.color_ramp.elements[0].position = 0.3
    color_ramp.color_ramp.elements[1].position = 0.7
    color_ramp.color_ramp.elements[0].color = (material_color[0]*0.3, material_color[1]*0.3, material_color[2]*0.3, 1.0)
    color_ramp.color_ramp.elements[1].color = (material_color[0], material_color[1], material_color[2], 1.0)
    links.new(noise_node.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf_node.inputs['Base Color'])

    # Color Ramp for Roughness (Simulating Roughness map)
    rough_ramp = nodes.new('ShaderNodeValToRGB')
    rough_ramp.location = (-300, -100)
    rough_ramp.color_ramp.elements[0].position = 0.4
    rough_ramp.color_ramp.elements[1].position = 0.6
    rough_ramp.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1.0)
    rough_ramp.color_ramp.elements[1].color = (0.9, 0.9, 0.9, 1.0)
    links.new(noise_node.outputs['Fac'], rough_ramp.inputs['Fac'])
    links.new(rough_ramp.outputs['Color'], bsdf_node.inputs['Roughness'])

    # Map connection: Raw map to Height (Simulating Displacement map)
    links.new(noise_node.outputs['Fac'], disp_node.inputs['Height'])

    # === Step 4: Lighting (Sun) ===
    # Hard lighting is necessary to cast shadows over the displaced geometry
    light_data = bpy.data.lights.new(name=object_name + "_Sun", type='SUN')
    light_data.energy = 3.0
    light_data.angle = math.radians(5.0) # Keeps shadows relatively sharp
    light_obj = bpy.data.objects.new(name=object_name + "_Sun_Obj", object_data=light_data)
    scene.collection.objects.link(light_obj)
    
    light_obj.location = Vector((location[0], location[1], location[2] + 5.0))
    light_obj.rotation_euler = (math.radians(45), math.radians(30), 0)

    return f"Created Displaced PBR Surface '{object_name}' with high-density mesh, procedural node mapping, and Sun light."
