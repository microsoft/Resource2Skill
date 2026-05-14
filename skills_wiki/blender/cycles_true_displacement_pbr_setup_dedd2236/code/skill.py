def create_object(
    scene_name: str = "Scene",
    object_name: str = "Procedural_Displaced_Terrain",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.22, 0.16, 0.11),
    **kwargs,
) -> str:
    """
    Create a highly displaced procedural terrain patch in Cycles.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = 5x5 meter patch).
        material_color: (R, G, B) base rock color in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Render Engine Setup ===
    # True displacement requires Cycles to function
    scene.render.engine = 'CYCLES'

    # === Step 2: Create Base Geometry ===
    mesh = bpy.data.meshes.new(name=f"{object_name}_Mesh")
    obj = bpy.data.objects.new(name=object_name, object_data=mesh)
    scene.collection.objects.link(obj)

    # Create a simple plane using bmesh
    bm = bmesh.new()
    s = 2.5  # 5x5m plane baseline
    v1 = bm.verts.new((-s, -s, 0))
    v2 = bm.verts.new((s, -s, 0))
    v3 = bm.verts.new((s, s, 0))
    v4 = bm.verts.new((-s, s, 0))
    bm.faces.new((v1, v2, v3, v4))
    bm.to_mesh(mesh)
    bm.free()

    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface modifier for dense topology required for displacement
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 6       # High density for viewport
    subsurf.render_levels = 7  # Maximum density for render

    # === Step 3: Build Material with True Displacement ===
    mat = bpy.data.materials.new(name=f"{object_name}_Material")
    mat.use_nodes = True
    obj.data.materials.append(mat)

    # The Core Technique: Enable True Displacement in Cycles material settings
    mat.cycles.displacement_method = 'DISPLACEMENT'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create Nodes
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (1000, 0)

    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf_node.location = (600, 200)

    disp_node = nodes.new(type='ShaderNodeDisplacement')
    disp_node.location = (600, -200)
    disp_node.inputs['Midlevel'].default_value = 0.0
    disp_node.inputs['Scale'].default_value = 0.8 * scale  # Scale displacement intensity

    # Procedural Noise to act as our downloaded heightmap
    noise_node = nodes.new(type='ShaderNodeTexNoise')
    noise_node.location = (0, 0)
    noise_node.inputs['Scale'].default_value = 2.0
    # Use index 2 for 'Detail' to ensure cross-version compatibility
    noise_node.inputs[2].default_value = 15.0  

    # Color mapping
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (300, 200)
    color_ramp.color_ramp.elements[0].position = 0.3
    color_ramp.color_ramp.elements[0].color = (*material_color, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.8
    color_ramp.color_ramp.elements[1].color = (0.55, 0.5, 0.45, 1.0) # Lighter highlights

    # Roughness mapping
    rough_ramp = nodes.new(type='ShaderNodeValToRGB')
    rough_ramp.location = (300, -50)
    rough_ramp.color_ramp.elements[0].position = 0.0
    rough_ramp.color_ramp.elements[0].color = (0.6, 0.6, 0.6, 1.0)
    rough_ramp.color_ramp.elements[1].position = 1.0
    rough_ramp.color_ramp.elements[1].color = (0.95, 0.95, 0.95, 1.0)

    # Connect Node Tree
    links.new(noise_node.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf_node.inputs['Base Color'])

    links.new(noise_node.outputs['Fac'], rough_ramp.inputs['Fac'])
    links.new(rough_ramp.outputs['Color'], bsdf_node.inputs['Roughness'])

    links.new(noise_node.outputs['Fac'], disp_node.inputs['Height'])

    links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])

    # === Step 4: Add Tutorial Lighting ===
    sun_name = f"{object_name}_Sun"
    sun_data = bpy.data.lights.new(name=sun_name, type='SUN')
    sun_data.energy = 5.0
    sun_data.angle = math.radians(11.4)  # Specific angle from the tutorial
    
    sun_obj = bpy.data.objects.new(name=sun_name, object_data=sun_data)
    scene.collection.objects.link(sun_obj)
    
    sun_obj.location = (location[0] + 5, location[1] - 5, location[2] + 10)
    sun_obj.rotation_euler = (math.radians(45), 0, math.radians(45))

    return f"Created '{object_name}' utilizing Cycles True Displacement and generated a complementary Sun light at {location}."
