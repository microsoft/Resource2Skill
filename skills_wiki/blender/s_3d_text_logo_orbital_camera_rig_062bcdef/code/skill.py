def create_object(
    scene_name: str = "Scene",
    object_name: str = "OrbitalLogo",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.7, 0.75),
    **kwargs,
) -> str:
    """
    Create an animated 3D text logo with an orbital camera rig and dynamic metallic material.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created text object and rig components.
        location: (x, y, z) world-space position for the center of the rig.
        scale: Uniform scale factor for the text size, camera orbit radius, and light distance.
        material_color: (R, G, B) base metallic color.
        **kwargs: Can include 'text_string' (default "3D LOGO") and 'anim_duration' (default 250).

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    text_string = kwargs.get("text_string", "3D LOGO")
    anim_duration = kwargs.get("anim_duration", 250)

    # ==========================================
    # 1. CREATE 3D TEXT & MATERIAL
    # ==========================================
    
    # Create text curve
    font_curve = bpy.data.curves.new(type="FONT", name=f"{object_name}_Font")
    font_curve.body = text_string
    font_curve.extrude = 0.15 * scale
    font_curve.bevel_depth = 0.015 * scale
    font_curve.align_x = 'CENTER'
    font_curve.align_y = 'CENTER'
    
    text_obj = bpy.data.objects.new(name=object_name, object_data=font_curve)
    text_obj.location = Vector(location)
    scene.collection.objects.link(text_obj)

    # Create Metallic Edge-Roughness Material
    mat = bpy.data.materials.new(name=f"{object_name}_Metallic")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
    bsdf.inputs['Metallic'].default_value = 1.0
    
    # Procedural Roughness driven by Layer Weight
    layer_weight = nodes.new("ShaderNodeLayerWeight")
    layer_weight.inputs['Blend'].default_value = 0.5
    
    color_ramp = nodes.new("ShaderNodeValToRGB")
    color_ramp.color_ramp.elements[0].position = 0.2
    color_ramp.color_ramp.elements[0].color = (0.15, 0.15, 0.15, 1.0) # Shiny edges
    color_ramp.color_ramp.elements[1].position = 0.8
    color_ramp.color_ramp.elements[1].color = (0.5, 0.5, 0.5, 1.0)   # Rougher front faces
    
    links.new(layer_weight.outputs['Facing'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Roughness'])
    
    text_obj.data.materials.append(mat)

    # ==========================================
    # 2. CREATE ORBITAL CAMERA RIG
    # ==========================================
    
    # A: The Focal Target (Empty)
    target_obj = bpy.data.objects.new(name=f"{object_name}_Target", object_data=None)
    target_obj.empty_display_type = 'PLAIN_AXES'
    target_obj.location = Vector(location)
    scene.collection.objects.link(target_obj)

    # B: The Orbit Path (Bezier Circle)
    # Using ops here for the complex primitive generation, then capturing it
    bpy.ops.curve.primitive_bezier_circle_add(radius=5.0 * scale, location=Vector(location))
    path_obj = bpy.context.active_object
    path_obj.name = f"{object_name}_Track"
    
    # C: The Camera
    cam_data = bpy.data.cameras.new(name=f"{object_name}_CamData")
    cam_data.lens = 35.0  # Slightly wider angle for dramatic logo feel
    cam_obj = bpy.data.objects.new(name=f"{object_name}_Cam", object_data=cam_data)
    cam_obj.location = Vector(location)
    scene.collection.objects.link(cam_obj)
    
    # Add Follow Path Constraint
    follow_path = cam_obj.constraints.new(type='FOLLOW_PATH')
    follow_path.target = path_obj
    follow_path.use_curve_follow = False # Handled by Track To instead
    
    # Animate the Follow Path offset factor from 0.0 to 1.0 (Full 360 rotation)
    follow_path.offset_factor = 0.0
    cam_obj.keyframe_insert(data_path=f'constraints["{follow_path.name}"].offset_factor', frame=1)
    
    follow_path.offset_factor = 1.0
    cam_obj.keyframe_insert(data_path=f'constraints["{follow_path.name}"].offset_factor', frame=anim_duration)

    # Add Track To Constraint
    track_to = cam_obj.constraints.new(type='TRACK_TO')
    track_to.target = target_obj
    track_to.track_axis = 'TRACK_NEGATIVE_Z'
    track_to.up_axis = 'UP_Y'

    # ==========================================
    # 3. CREATE TRACKING SPOTLIGHTS
    # ==========================================
    
    # Create a dramatic backlight spot
    spot_data = bpy.data.lights.new(name=f"{object_name}_Spot", type='SPOT')
    spot_data.energy = 5000.0 * (scale ** 2)
    spot_data.spot_size = math.radians(45)
    spot_data.spot_blend = 0.8
    spot_data.color = (0.8, 0.9, 1.0)
    
    spot_obj = bpy.data.objects.new(name=f"{object_name}_Spot", object_data=spot_data)
    spot_obj.location = (location[0], location[1] - (4.0 * scale), location[2] + (3.0 * scale))
    scene.collection.objects.link(spot_obj)
    
    # Track light to the text target
    spot_track = spot_obj.constraints.new(type='TRACK_TO')
    spot_track.target = target_obj
    spot_track.track_axis = 'TRACK_NEGATIVE_Z'
    spot_track.up_axis = 'UP_Y'

    return f"Created Orbital Text '{object_name}' ('{text_string}') at {location} with Camera Rig, Target, and Tracking Spotlight."
