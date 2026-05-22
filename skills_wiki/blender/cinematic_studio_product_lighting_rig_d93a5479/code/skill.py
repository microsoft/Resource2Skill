def create_object(
    scene_name: str = "Scene",
    object_name: str = "StudioRig",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.4, 0.8), # Used here as the Background Gradient Color
    **kwargs,
) -> str:
    """
    Creates a complete Cinematic Studio Lighting Rig with a Key Light, Bounce Fill, 
    Gradient Backdrop, and an 85mm Depth-of-Field Camera.
    
    Note: Changes render engine to CYCLES, as the bounce fill requires path-tracing.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the rig hierarchy.
        location: (x, y, z) world-space position for the rig center/subject focus.
        scale: Uniform scale factor for the rig spread.
        material_color: (R, G, B) used to tint the background gradient spotlight.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # The tutorial's bounce-plane technique REQUIRES a path tracer to work.
    scene.render.engine = 'CYCLES'

    # --- 1. Set pure black environment ---
    if not scene.world:
        scene.world = bpy.data.worlds.new("World")
    scene.world.use_nodes = True
    bg_node = scene.world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0) # Pure black

    # --- 2. Master Rig Parent ---
    master_empty = bpy.data.objects.new(object_name, None)
    master_empty.location = location
    scene.collection.objects.link(master_empty)

    # Focus Target
    target_empty = bpy.data.objects.new(f"{object_name}_FocusTarget", None)
    target_empty.location = (0.0, 0.0, 0.5 * scale)
    scene.collection.objects.link(target_empty)
    target_empty.parent = master_empty

    # --- 3. Key Light (Area Light) ---
    key_data = bpy.data.lights.new(name=f"{object_name}_KeyLight", type='AREA')
    key_data.shape = 'RECTANGLE'
    key_data.size = 0.5 * scale
    key_data.size_y = 2.0 * scale
    key_data.energy = 1000.0 * (scale ** 2)
    key_data.color = (1.0, 0.96, 0.9) # Slightly warm daylight
    
    key_obj = bpy.data.objects.new(name=f"{object_name}_KeyLight", object_data=key_data)
    key_obj.location = (-1.5 * scale, -1.5 * scale, 1.5 * scale)
    scene.collection.objects.link(key_obj)
    key_obj.parent = master_empty

    track_key = key_obj.constraints.new(type='TRACK_TO')
    track_key.target = target_empty
    track_key.track_axis = 'TRACK_NEGATIVE_Z'
    track_key.up_axis = 'UP_Y'

    # --- 4. Bounce Fill (Passive Mesh Plane) ---
    bpy.ops.mesh.primitive_plane_add(size=3.0 * scale, location=(0,0,0))
    fill_obj = bpy.context.active_object
    fill_obj.name = f"{object_name}_BounceFill"
    fill_obj.location = (1.5 * scale, 1.0 * scale, 0.5 * scale)
    fill_obj.parent = master_empty

    track_fill = fill_obj.constraints.new(type='TRACK_TO')
    track_fill.target = target_empty
    track_fill.track_axis = 'TRACK_Z'  # +Z normal faces subject
    track_fill.up_axis = 'UP_Y'

    fill_mat = bpy.data.materials.new(name=f"{object_name}_BounceMat")
    fill_mat.use_nodes = True
    bsdf_fill = fill_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf_fill:
        bsdf_fill.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0) # Pure white
        bsdf_fill.inputs["Roughness"].default_value = 1.0
    fill_obj.data.materials.append(fill_mat)

    # --- 5. Gradient Backdrop ---
    bpy.ops.mesh.primitive_plane_add(size=15.0 * scale, location=(0,0,0))
    bg_obj = bpy.context.active_object
    bg_obj.name = f"{object_name}_Backdrop"
    bg_obj.location = (0.0, 3.0 * scale, 0.0)
    bg_obj.rotation_euler = (math.radians(90), 0, 0)
    bg_obj.parent = master_empty

    bg_mat = bpy.data.materials.new(name=f"{object_name}_BgMat")
    bg_mat.use_nodes = True
    bsdf_bg = bg_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf_bg:
        bsdf_bg.inputs["Base Color"].default_value = (0.02, 0.02, 0.02, 1.0) # Dark grey
        bsdf_bg.inputs["Roughness"].default_value = 0.8
        if "Specular IOR Level" in bsdf_bg.inputs:
            bsdf_bg.inputs["Specular IOR Level"].default_value = 0.1
    bg_obj.data.materials.append(bg_mat)

    # --- 6. Background Spot Light ---
    bg_target = bpy.data.objects.new(f"{object_name}_BgTarget", None)
    bg_target.location = (0.0, 3.0 * scale, 1.5 * scale)
    scene.collection.objects.link(bg_target)
    bg_target.parent = master_empty

    spot_data = bpy.data.lights.new(name=f"{object_name}_BgSpot", type='SPOT')
    spot_data.spot_blend = 0.85
    spot_data.spot_size = math.radians(75)
    spot_data.energy = 2500.0 * (scale ** 2)
    spot_data.color = (material_color[0], material_color[1], material_color[2]) # Custom gradient color
    
    spot_obj = bpy.data.objects.new(name=f"{object_name}_BgSpot", object_data=spot_data)
    spot_obj.location = (0.0, 1.0 * scale, 0.5 * scale)
    scene.collection.objects.link(spot_obj)
    spot_obj.parent = master_empty

    track_spot = spot_obj.constraints.new(type='TRACK_TO')
    track_spot.target = bg_target
    track_spot.track_axis = 'TRACK_NEGATIVE_Z'
    track_spot.up_axis = 'UP_Y'

    # --- 7. Pedestal ---
    bpy.ops.mesh.primitive_cylinder_add(radius=0.8 * scale, depth=0.1 * scale, location=(0,0,0))
    pedestal = bpy.context.active_object
    pedestal.name = f"{object_name}_Pedestal"
    pedestal.location = (0.0, 0.0, -0.05 * scale)
    pedestal.parent = master_empty

    ped_mat = bpy.data.materials.new(name=f"{object_name}_PedestalMat")
    ped_mat.use_nodes = True
    bsdf_ped = ped_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf_ped:
        bsdf_ped.inputs["Base Color"].default_value = (0.01, 0.01, 0.01, 1.0)
        bsdf_ped.inputs["Roughness"].default_value = 0.3
    pedestal.data.materials.append(ped_mat)

    # --- 8. Studio Camera ---
    cam_data = bpy.data.cameras.new(f"{object_name}_Camera")
    cam_data.lens = 85 # Telephoto compression
    cam_data.dof.use_dof = True
    cam_data.dof.focus_object = target_empty
    cam_data.dof.aperture_fstop = 2.8

    cam_obj = bpy.data.objects.new(f"{object_name}_Camera", cam_data)
    cam_obj.location = (0.0, -4.5 * scale, 1.0 * scale)
    scene.collection.objects.link(cam_obj)
    cam_obj.parent = master_empty

    cam_track = cam_obj.constraints.new(type='TRACK_TO')
    cam_track.target = target_empty
    cam_track.track_axis = 'TRACK_NEGATIVE_Z'
    cam_track.up_axis = 'UP_Y'

    scene.camera = cam_obj

    # Force view layer update so constraints resolve correctly
    bpy.context.view_layer.update()

    return f"Created '{object_name}' Studio Rig at {location}. Engine set to Cycles for passive bounce fill. Place a subject inside the rig."
