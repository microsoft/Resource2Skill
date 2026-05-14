def create_object(
    scene_name: str = "Scene",
    object_name: str = "CinematicCamera",
    location: tuple = (0, -25, 10),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.1, 0.1),
    **kwargs,
) -> str:
    """
    Create an animated cinematic camera rig and optionally a stylized procedural city.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created camera object.
        location: (x, y, z) world-space starting position.
        scale: Uniform scale factor (applied to camera object, doesn't affect lens).
        material_color: Unused for camera (standard signature).
        **kwargs: 
            shot_type (str): "DOLLY", "TRUCK", "PEDESTAL", "PAN", "TILT", or "ROLL".
            amount (float): Distance for translation (meters) or degrees for rotation.
            duration (int): Number of frames for the animation.
            start_frame (int): Frame where animation starts.
            create_environment (bool): Generate a stylized procedural city block.

    Returns:
        Status string describing the generated rig.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector, Matrix

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Kwargs parsing & Smart Defaults
    shot_type = kwargs.get("shot_type", "DOLLY").upper()
    duration = kwargs.get("duration", 150)
    start_frame = kwargs.get("start_frame", 1)
    end_frame = start_frame + duration
    create_env = kwargs.get("create_environment", True)

    if "amount" in kwargs:
        amount = kwargs["amount"]
    else:
        # Smart defaults based on shot type
        if shot_type in ["PAN", "TILT", "ROLL"]:
            amount = 45.0  # degrees
        elif shot_type == "PEDESTAL":
            amount = 10.0  # meters
        else: # DOLLY, TRUCK
            amount = 20.0  # meters

    # Update scene frame range to fit the animation
    scene.frame_start = 1
    scene.frame_end = max(scene.frame_end, end_frame + 24)

    # === Step 1: Create Optional City Environment ===
    if create_env:
        # Only create the city once per session to avoid additive clutter
        env_col = bpy.data.collections.get("Environment_City")
        if not env_col:
            env_col = bpy.data.collections.new("Environment_City")
            scene.collection.children.link(env_col)
            
            mat = bpy.data.materials.new("CityBuildingMat")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = (0.02, 0.08, 0.15, 1.0)
                bsdf.inputs["Roughness"].default_value = 0.8
                # Compatibility for Blender 3.x vs 4.x emission
                if "Emission Color" in bsdf.inputs:
                    bsdf.inputs["Emission Color"].default_value = (0.0, 0.1, 0.3, 1.0)
                    bsdf.inputs["Emission Strength"].default_value = 0.5
                elif "Emission" in bsdf.inputs:
                    bsdf.inputs["Emission"].default_value = (0.0, 0.05, 0.15, 1.0)
                    
            bm = bmesh.new()
            grid_size = 12
            spacing = 2.5
            random.seed(42) # Deterministic placement
            
            for x in range(-grid_size, grid_size):
                for y in range(-grid_size, grid_size):
                    if random.random() > 0.4:
                        height = random.uniform(1.0, 12.0)
                        if random.random() > 0.95: # Hero buildings
                            height = random.uniform(18.0, 30.0)
                            
                        ret = bmesh.ops.create_cube(bm, size=1.0)
                        verts = ret['verts']
                        bmesh.ops.scale(bm, verts=verts, vec=(1.8, 1.8, height))
                        bmesh.ops.translate(bm, verts=verts, vec=(x * spacing, y * spacing, height/2))
            
            env_mesh = bpy.data.meshes.new("ProceduralCity")
            bm.to_mesh(env_mesh)
            bm.free()
            env_obj = bpy.data.objects.new("ProceduralCity", env_mesh)
            env_obj.data.materials.append(mat)
            env_col.objects.link(env_obj)

    # === Step 2: Create Camera & Setup Optics ===
    cam_data = bpy.data.cameras.new(name=f"{object_name}_Data")
    cam_data.lens = 35 # Wide angle
    cam_data.dof.use_dof = True
    cam_data.dof.focus_distance = abs(location[1]) if location[1] != 0 else 10.0
    cam_data.dof.aperture_fstop = 2.8

    cam_obj = bpy.data.objects.new(object_name, cam_data)
    scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj # Make it the active view

    # === Step 3: Setup Initial Transform & Keyframe ===
    cam_obj.location = Vector(location)
    cam_obj.scale = (scale, scale, scale)
    
    # Default rotation pointing somewhat forward and slightly down
    start_rot = kwargs.get("rotation", (math.radians(75), 0, 0)) 
    cam_obj.rotation_mode = 'XYZ'
    cam_obj.rotation_euler = start_rot

    # MUST update view layer to compute correct initial matrix_world
    bpy.context.view_layer.update()

    cam_obj.keyframe_insert(data_path="location", frame=start_frame)
    cam_obj.keyframe_insert(data_path="rotation_euler", frame=start_frame)

    # === Step 4: Calculate & Apply Cinematic Move ===
    if shot_type == "DOLLY":
        # Move along local -Z (Push in/out)
        local_vec = Vector((0, 0, -amount))
        cam_obj.location = cam_obj.matrix_world @ local_vec
        
    elif shot_type == "TRUCK":
        # Move along local X (Slide left/right)
        local_vec = Vector((amount, 0, 0))
        cam_obj.location = cam_obj.matrix_world @ local_vec
        
    elif shot_type == "PEDESTAL":
        # Move along global Z (Crane up/down)
        cam_obj.location.z += amount
        
    elif shot_type == "PAN":
        # Rotate around global Z (Look left/right)
        cam_obj.rotation_euler.z += math.radians(amount)
        
    elif shot_type == "TILT":
        # Rotate around local X (Pitch up/down)
        rot_mat = Matrix.Rotation(math.radians(amount), 4, 'X')
        cam_obj.matrix_world = cam_obj.matrix_world @ rot_mat
        
    elif shot_type == "ROLL":
        # Rotate around local Z (Dutch angle)
        rot_mat = Matrix.Rotation(math.radians(amount), 4, 'Z')
        cam_obj.matrix_world = cam_obj.matrix_world @ rot_mat

    # Update again before reading final values for keyframing
    bpy.context.view_layer.update()

    cam_obj.keyframe_insert(data_path="location", frame=end_frame)
    cam_obj.keyframe_insert(data_path="rotation_euler", frame=end_frame)

    # === Step 5: Polish Animation Curves (Linear Interpolation) ===
    # Real cameras on motorized tracks move at a constant speed
    if cam_obj.animation_data and cam_obj.animation_data.action:
        for fcurve in cam_obj.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'
                
    return f"Created '{object_name}' with a {shot_type} shot from frame {start_frame} to {end_frame}"
