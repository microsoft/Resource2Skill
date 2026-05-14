def create_object(
    scene_name: str = "Scene",
    object_name: str = "VolumetricGodRays",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.8, 0.8),
    **kwargs,
) -> str:
    """
    Create Procedural Volumetric God Rays in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created setup.
        location: (x, y, z) world-space origin position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the volume scatter.
        **kwargs: Overrides for volume_density, volume_anisotropy, sun_elevation.

    Returns:
        Status string.
    """
    import bpy
    import math
    import random
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Force object mode if needed
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # === Engine Setup ===
    # Cycles is required for accurate volumetric light scattering
    scene.render.engine = 'CYCLES'
    scene.view_settings.exposure = 0.1  # Darken global exposure to make rays pop

    # === Step 1: Create Base Geometry ===
    loc = Vector(location)
    
    # Create an empty as the master parent
    root_empty = bpy.data.objects.new(object_name, None)
    root_empty.location = loc
    bpy.context.collection.objects.link(root_empty)

    # Floor plane
    bpy.ops.mesh.primitive_plane_add(size=40*scale, location=loc)
    floor = bpy.context.active_object
    floor.name = f"{object_name}_Floor"
    floor.parent = root_empty

    # Main Subject Cube (Focal point)
    bpy.ops.mesh.primitive_cube_add(size=2*scale, location=loc + Vector((0, 0, 1*scale)))
    main_cube = bpy.context.active_object
    main_cube.name = f"{object_name}_Subject"
    main_cube.parent = root_empty

    # Occluders (Scattered cubes to break up light and cast shadows)
    random.seed(42)  # Fixed seed for reproducible scattering
    for i in range(35):
        # Cluster them higher up in the air
        pos_offset = Vector((
            random.uniform(-6, 6) * scale,
            random.uniform(-6, 6) * scale,
            random.uniform(4, 10) * scale
        ))
        bpy.ops.mesh.primitive_cube_add(
            size=random.uniform(0.2, 0.8) * scale, 
            location=loc + pos_offset
        )
        occ = bpy.context.active_object
        occ.name = f"{object_name}_Occluder_{i}"
        occ.rotation_euler = (
            random.uniform(0, 3.14), 
            random.uniform(0, 3.14), 
            random.uniform(0, 3.14)
        )
        occ.parent = root_empty

    # Volume Domain (Large box enclosing everything)
    bpy.ops.mesh.primitive_cube_add(size=40*scale, location=loc + Vector((0, 0, 15*scale)))
    vol_cube = bpy.context.active_object
    vol_cube.name = f"{object_name}_VolumeDomain"
    vol_cube.parent = root_empty
    vol_cube.display_type = 'BOUNDS'  # Do not block viewport visibility

    # === Step 2: Build Volume Material ===
    vol_mat = bpy.data.materials.new(name=f"{object_name}_VolMat")
    vol_mat.use_nodes = True
    v_nodes = vol_mat.node_tree.nodes
    v_links = vol_mat.node_tree.links

    # Clear default Surface node setup
    for n in v_nodes:
        v_nodes.remove(n)

    # Create Volume Shader
    v_out = v_nodes.new(type='ShaderNodeOutputMaterial')
    v_out.location = (300, 0)
    
    v_scatter = v_nodes.new(type='ShaderNodeVolumeScatter')
    v_scatter.location = (0, 0)
    v_scatter.inputs['Density'].default_value = kwargs.get('volume_density', 0.1)
    v_scatter.inputs['Anisotropy'].default_value = kwargs.get('volume_anisotropy', 0.9)
    v_scatter.inputs['Color'].default_value = (material_color[0], material_color[1], material_color[2], 1.0)

    # Plug into Volume, NOT Surface
    v_links.new(v_scatter.outputs['Volume'], v_out.inputs['Volume'])
    vol_cube.data.materials.append(vol_mat)

    # === Step 3: Setup World Lighting (Sky Texture) ===
    # Create a new world additively so we don't destroy existing user worlds
    new_world = bpy.data.worlds.new(f"{object_name}_SkyWorld")
    scene.world = new_world
    new_world.use_nodes = True
    w_nodes = new_world.node_tree.nodes
    w_links = new_world.node_tree.links

    w_out = w_nodes.get("World Output")
    if not w_out:
        w_out = w_nodes.new(type='ShaderNodeOutputWorld')
    
    w_bg = w_nodes.get("Background")
    if not w_bg:
        w_bg = w_nodes.new(type='ShaderNodeBackground')

    w_sky = w_nodes.new(type='ShaderNodeTexSky')
    w_sky.sky_type = 'NISHITA'
    # Extremely low sun elevation (5 degrees) for long, raking crepuscular rays
    w_sky.sun_elevation = math.radians(kwargs.get('sun_elevation', 5.0))
    w_sky.sun_rotation = math.radians(kwargs.get('sun_rotation', 135.0))

    w_links.new(w_sky.outputs['Color'], w_bg.inputs['Color'])
    w_links.new(w_bg.outputs['Background'], w_out.inputs['Surface'])

    # === Step 4: Finalize ===
    bpy.ops.object.select_all(action='DESELECT')
    root_empty.select_set(True)
    bpy.context.view_layer.objects.active = root_empty

    return f"Created '{object_name}' volumetric setup at {location} with {len(root_empty.children)} objects and custom Sky World."
