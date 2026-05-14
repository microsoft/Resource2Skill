def create_cinematic_flight_camera(
    scene_name: str = "Scene",
    object_name: str = "CinematicCamera",
    start_loc: tuple = (0.0, -10.0, 2.0),
    end_loc: tuple = (0.0, 5.0, 2.0),
    start_rot: tuple = (1.396, 0.0, 0.0),      # ~80 deg X
    end_rot: tuple = (1.396, 0.0, 0.785),      # ~80 deg X, 45 deg Z
    duration_frames: int = 150,
    padding_frames: int = 40,
    smoothing_iterations: int = 50,
    jitter_amount: float = 0.5,
    lens_mm: float = 20.0,
    **kwargs
) -> str:
    """
    Creates a cinematic, organic camera flight path mimicking a smoothed Walk Navigation recording.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created camera object.
        start_loc: (x, y, z) starting position.
        end_loc: (x, y, z) ending position.
        start_rot: (x, y, z) starting rotation in radians.
        end_rot: (x, y, z) ending rotation in radians.
        duration_frames: How many frames the core movement takes.
        padding_frames: Number of static hold frames at the start and end (crucial for ease-in/out).
        smoothing_iterations: Number of times to apply the Boxcar moving average filter.
        jitter_amount: Intensity of the random operator drift applied before smoothing.
        lens_mm: Camera focal length (default 20mm for a wide cinematic look).

    Returns:
        Status string describing the creation.
    """
    import bpy
    from mathutils import Vector
    import random
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Camera Object ===
    cam_data = bpy.data.cameras.new(name=object_name + "_Data")
    cam_data.lens = lens_mm
    cam_obj = bpy.data.objects.new(object_name, cam_data)
    scene.collection.objects.link(cam_obj)
    
    # === Step 2: Initialize Animation Data ===
    cam_obj.animation_data_create()
    action = bpy.data.actions.new(name=object_name + "_Action")
    cam_obj.animation_data.action = action
    cam_obj.rotation_mode = 'XYZ'
    
    # Create F-Curves for Location (0,1,2) and Rotation Euler (0,1,2)
    fcurves_loc = [action.fcurves.new(data_path="location", index=i) for i in range(3)]
    fcurves_rot = [action.fcurves.new(data_path="rotation_euler", index=i) for i in range(3)]
    all_fcurves = fcurves_loc + fcurves_rot
        
    start_v = Vector(start_loc)
    end_v = Vector(end_loc)
    start_r = Vector(start_rot)
    end_r = Vector(end_rot)
    
    loc_drift = Vector((0.0, 0.0, 0.0))
    rot_drift = Vector((0.0, 0.0, 0.0))
    
    total_frames = padding_frames * 2 + duration_frames
    
    # === Step 3: Generate Dense, Organic Raw Data ===
    for frame in range(1, total_frames + 1):
        if frame <= padding_frames:
            # Static Hold Start (boundary condition for ease-in)
            pos = start_v
            rot = start_r
            loc_drift = Vector((0.0, 0.0, 0.0))
            rot_drift = Vector((0.0, 0.0, 0.0))
        elif frame > padding_frames + duration_frames:
            # Static Hold End (boundary condition for ease-out)
            pos = end_v
            rot = end_r
        else:
            # Moving Phase
            t = (frame - padding_frames) / duration_frames
            base_pos = start_v.lerp(end_v, t)
            base_rot = start_r.lerp(end_r, t)
            
            # Sine wave fading ensures the drift perfectly resolves to 0 at the start and end points
            fade = math.sin(t * math.pi) 
            
            # Add Brownian drift to simulate Walk Navigation over-correction
            loc_noise = Vector((random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)))
            rot_noise = Vector((random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)))
            
            loc_drift += loc_noise * (jitter_amount * fade)
            rot_drift += rot_noise * (jitter_amount * 0.05 * fade)
            
            # Dampen drift to stay loosely anchored to the primary vector
            loc_drift *= 0.85
            rot_drift *= 0.85
            
            pos = base_pos + loc_drift
            rot = base_rot + rot_drift
            
        # Insert dense keyframes (one per frame)
        fcurves_loc[0].keyframe_points.insert(frame, pos.x)
        fcurves_loc[1].keyframe_points.insert(frame, pos.y)
        fcurves_loc[2].keyframe_points.insert(frame, pos.z)
        fcurves_rot[0].keyframe_points.insert(frame, rot.x)
        fcurves_rot[1].keyframe_points.insert(frame, rot.y)
        fcurves_rot[2].keyframe_points.insert(frame, rot.z)
        
    # === Step 4: Programmatic Iterative Smoothing ===
    # Mathematically mimicking the user holding down `Alt + O` (Smooth Keys)
    for fc in all_fcurves:
        for _ in range(smoothing_iterations):
            vals = [kp.co[1] for kp in fc.keyframe_points]
            for i in range(1, len(vals) - 1):
                # 3-tap moving average
                fc.keyframe_points[i].co[1] = (vals[i-1] + vals[i] + vals[i+1]) / 3.0
                
        # Set handles to AUTO for perfectly smooth Bezier transitions
        for kp in fc.keyframe_points:
            kp.interpolation = 'BEZIER'
            kp.handle_left_type = 'AUTO'
            kp.handle_right_type = 'AUTO'

    # === Step 5: Add Subtle High-Frequency "Breathing" ===
    # Adds a tiny amount of F-Curve noise to rotation to keep it feeling handheld after smoothing
    for i in range(3):
        mod = fcurves_rot[i].modifiers.new(type='NOISE')
        mod.scale = 25.0
        mod.strength = 0.005
        mod.phase = random.uniform(0, 100)
            
    # === Step 6: Finalize Context ===
    scene.camera = cam_obj
    scene.frame_start = 1
    scene.frame_end = total_frames
    
    return f"Created Cinematic Camera '{cam_obj.name}' with {total_frames} smoothed frames, providing perfect organic easing."
