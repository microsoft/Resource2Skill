def create_object(
    scene_name: str = "Scene",
    object_name: str = "TrackingCamRig",
    location: tuple = (0, 0, 0),
    scale: float = 5.0,
    material_color: tuple = (0.2, 0.6, 0.8),
    **kwargs,
) -> str:
    """
    Create a Constraint-Based Tracking Camera Rig around a target location.
    Generates a placeholder subject, a tracking target, a circular path, and a camera.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the rig's components.
        location: (x, y, z) center point of the orbit and subject.
        scale: Radius of the camera's circular orbit.
        material_color: (R, G, B) color for the placeholder subject.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created rig.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection

    # === Step 1: Create Placeholder Subject ===
    # Adding a subject so the camera has something to look at
    subject_name = f"{object_name}_Subject"
    bpy.ops.mesh.primitive_monkey_add(size=2.0, location=location)
    subject = bpy.context.active_object
    subject.name = subject_name
    
    # Smooth subject
    subsurf = subject.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    bpy.ops.object.shade_smooth()

    # Material for subject
    mat = bpy.data.materials.new(name=f"{subject_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.4
    subject.data.materials.append(mat)

    # === Step 2: Create Track Target Empty ===
    track_empty = bpy.data.objects.new(f"{object_name}_TrackTarget", None)
    track_empty.empty_display_type = 'SPHERE'
    track_empty.empty_display_size = 0.5
    # Place target slightly above the subject's center
    target_loc = Vector(location) + Vector((0, 0, 0.5))
    track_empty.location = target_loc
    collection.objects.link(track_empty)

    # === Step 3: Create Camera Path ===
    bpy.ops.curve.primitive_bezier_circle_add(radius=scale, location=location)
    path_obj = bpy.context.active_object
    path_obj.name = f"{object_name}_Path"
    # Tilt path slightly for a dynamic orbital angle
    path_obj.rotation_euler = (math.radians(15), 0, 0)

    # === Step 4: Create Camera Container ===
    container_empty = bpy.data.objects.new(f"{object_name}_Container", None)
    container_empty.empty_display_type = 'CUBE'
    container_empty.empty_display_size = 0.2
    collection.objects.link(container_empty)

    # Follow Path Constraint
    follow_const = container_empty.constraints.new(type='FOLLOW_PATH')
    follow_const.target = path_obj
    follow_const.use_fixed_location = True  # Enable 0.0 to 1.0 offset factor
    follow_const.use_curve_follow = False   # Keep empty axis-aligned (prevents camera roll)
    
    # Animate the path offset
    anim_length = 250
    follow_const.offset_factor = 0.0
    follow_const.keyframe_insert(data_path="offset_factor", frame=1)
    follow_const.offset_factor = 1.0
    follow_const.keyframe_insert(data_path="offset_factor", frame=anim_length)

    # Set interpolation to LINEAR for a seamless infinite loop
    if container_empty.animation_data and container_empty.animation_data.action:
        for fcurve in container_empty.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'

    # === Step 5: Create Camera & Final Constraints ===
    cam_data = bpy.data.cameras.new(f"{object_name}_CamData")
    cam_data.lens = 50
    cam_obj = bpy.data.objects.new(f"{object_name}_Cam", cam_data)
    collection.objects.link(cam_obj)

    # Child Of constraint (Add FIRST: moves camera to container)
    child_const = cam_obj.constraints.new(type='CHILD_OF')
    child_const.target = container_empty
    # Snap camera exactly to container's zero coordinate
    cam_obj.location = (0, 0, 0)
    cam_obj.rotation_euler = (0, 0, 0)

    # Track To constraint (Add SECOND: overwrites rotation to face subject)
    track_const = cam_obj.constraints.new(type='TRACK_TO')
    track_const.target = track_empty
    track_const.track_axis = 'TRACK_NEGATIVE_Z'
    track_const.up_axis = 'UP_Y'
    
    # Optional: Make this the active scene camera
    scene.camera = cam_obj

    return f"Created camera rig '{object_name}' looping around {location} (Radius: {scale}) over {anim_length} frames."
