def create_architectural_window_rig(
    scene_name: str = "Scene",
    object_name: str = "ArchWindowRig",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    wall_color: tuple = (0.8, 0.8, 0.8),
    sun_color: tuple = (1.0, 0.85, 0.7),
    sky_color: tuple = (0.6, 0.8, 1.0),
    sun_intensity: float = 5.0,
    **kwargs,
) -> str:
    """
    Creates an optimized architectural window with a noise-free glass shader, 
    paired with a realistic Sun and Sky Area light setup.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created rig.
        location: (x, y, z) world-space position of the wall center.
        scale: Uniform scale factor.
        wall_color: (R, G, B) color of the wall.
        sun_color: (R, G, B) color of the direct sunlight.
        sky_color: (R, G, B) color of the ambient sky fill light.
        sun_intensity: Strength of the sun light.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector, Euler

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection

    # 1. Create Control Empty (Parent)
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    rig_root = bpy.context.active_object
    rig_root.name = f"{object_name}_Root"
    rig_root.scale = (scale, scale, scale)

    # 2. Create the Wall
    bpy.ops.mesh.primitive_cube_add(size=1)
    wall = bpy.context.active_object
    wall.name = f"{object_name}_Wall"
    wall.scale = (6.0, 0.4, 4.0) # Wide, thin, tall
    wall.location = (0, 0, 2.0)
    wall.parent = rig_root
    
    # Wall Material
    wall_mat = bpy.data.materials.new(name=f"{object_name}_WallMat")
    wall_mat.use_nodes = True
    bsdf = wall_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*wall_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.9
    wall.data.materials.append(wall_mat)

    # 3. Create the Boolean Cutter for the Window Hole
    bpy.ops.mesh.primitive_cube_add(size=1)
    cutter = bpy.context.active_object
    cutter.name = f"{object_name}_Cutter"
    cutter.scale = (2.0, 1.0, 2.0)
    cutter.location = (0, 0, 2.0) # Centered in wall
    cutter.parent = rig_root
    cutter.display_type = 'WIRE'
    cutter.hide_render = True

    # Apply Boolean to Wall
    bool_mod = wall.modifiers.new(name="WindowCut", type='BOOLEAN')
    bool_mod.object = cutter
    bool_mod.operation = 'DIFFERENCE'

    # 4. Create the Noise-Free Glass Pane
    bpy.ops.mesh.primitive_cube_add(size=1)
    glass = bpy.context.active_object
    glass.name = f"{object_name}_GlassPane"
    glass.scale = (1.9, 0.05, 1.9) # Slightly smaller than hole, very thin
    glass.location = (0, 0, 2.0)
    glass.parent = rig_root

    # Noise-Free Glass Shader Logic
    glass_mat = bpy.data.materials.new(name=f"{object_name}_SmartGlass")
    glass_mat.use_nodes = True
    tree = glass_mat.node_tree
    tree.nodes.clear() # Clear default nodes

    out_node = tree.nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (400, 0)

    mix_node = tree.nodes.new('ShaderNodeMixShader')
    mix_node.location = (200, 0)

    glass_bsdf = tree.nodes.new('ShaderNodeBsdfGlass')
    glass_bsdf.location = (0, 100)
    glass_bsdf.inputs['Roughness'].default_value = 0.05
    glass_bsdf.inputs['IOR'].default_value = 1.45

    trans_bsdf = tree.nodes.new('ShaderNodeBsdfTransparent')
    trans_bsdf.location = (0, -100)
    trans_bsdf.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)

    light_path = tree.nodes.new('ShaderNodeLightPath')
    light_path.location = (-400, 300)

    math_add = tree.nodes.new('ShaderNodeMath')
    math_add.operation = 'ADD'
    math_add.location = (-200, 300)

    # Link Nodes
    tree.links.new(light_path.outputs['Is Shadow Ray'], math_add.inputs[0])
    tree.links.new(light_path.outputs['Is Diffuse Ray'], math_add.inputs[1])
    tree.links.new(math_add.outputs['Value'], mix_node.inputs['Fac'])
    
    tree.links.new(glass_bsdf.outputs['BSDF'], mix_node.inputs[1])
    tree.links.new(trans_bsdf.outputs['BSDF'], mix_node.inputs[2])
    tree.links.new(mix_node.outputs['Shader'], out_node.inputs['Surface'])

    glass.data.materials.append(glass_mat)

    # 5. Lighting Setup: Sun Light
    sun_data = bpy.data.lights.new(name=f"{object_name}_SunLight", type='SUN')
    sun_data.energy = sun_intensity
    sun_data.color = sun_color
    sun_data.angle = math.radians(1.5) # Sharp shadows
    
    sun_obj = bpy.data.objects.new(name=f"{object_name}_Sun", object_data=sun_data)
    collection.objects.link(sun_obj)
    sun_obj.parent = rig_root
    # Position outside and point down through the window
    sun_obj.location = (3.0, 5.0, 5.0) 
    # Aiming towards the center (0,0,1)
    sun_obj.rotation_euler = Euler((math.radians(60), 0, math.radians(150)), 'XYZ')

    # 6. Lighting Setup: Area Light (Sky Portal / Fill)
    area_data = bpy.data.lights.new(name=f"{object_name}_SkyFillData", type='AREA')
    area_data.energy = sun_intensity * 100.0 # Area lights need significantly higher energy
    area_data.color = sky_color
    area_data.shape = 'RECTANGLE'
    area_data.size = 3.0
    area_data.size_y = 3.0

    area_obj = bpy.data.objects.new(name=f"{object_name}_SkyFill", object_data=area_data)
    collection.objects.link(area_obj)
    area_obj.parent = rig_root
    # Position just outside the window, pointing inside
    area_obj.location = (0, 0.5, 2.0)
    area_obj.rotation_euler = Euler((math.radians(90), 0, math.radians(180)), 'XYZ')

    # Deselect all and select the root empty
    bpy.ops.object.select_all(action='DESELECT')
    rig_root.select_set(True)
    bpy.context.view_layer.objects.active = rig_root

    return f"Created '{object_name}' Architectural Rig at {location} with optimized glass and lighting."
