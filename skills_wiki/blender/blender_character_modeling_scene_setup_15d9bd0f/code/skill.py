def setup_blender_character_modeling_scene(
    scene_name: str = "Scene",
    object_prefix: str = "LoveChan",
    ref_image_front_path: str = "", # Full path to the front reference image file
    ref_image_side_path: str = "",  # Full path to the side reference image file
    ref_image_opacity: float = 0.5,
    metarig_scale: float = 1.0,
    metarig_location: tuple = (0, 0, 0),
    ref_image_distance_from_rig: float = 1.5, # Distance of ref planes from the metarig along their respective axes
    **kwargs,
) -> str:
    """
    Sets up a Blender scene for character modeling, including color management,
    reference images, and a Rigify Human Metarig for scale reference.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_prefix: Prefix for created objects (e.g., 'LoveChan_Ref_Front').
        ref_image_front_path: Full path to the front reference image file (e.g., "C:/Users/User/Downloads/LoveChan_Front.png").
        ref_image_side_path: Full path to the side reference image file (e.g., "C:/Users/User/Downloads/LoveChan_Side.png").
        ref_image_opacity: Opacity for the reference images (0.0-1.0).
        metarig_scale: Uniform scale factor for the Human Metarig.
        metarig_location: (x, y, z) world-space position for the Human Metarig.
        ref_image_distance_from_rig: Distance (in Blender units) that reference planes
                                      are placed from the metarig along their respective axes.
        **kwargs: Additional overrides (not used in this specific implementation but kept for API consistency).

    Returns:
        Status string, eg., "Set up character modeling scene for 'LoveChan'"
    """
    import bpy
    from mathutils import Vector
    import math
    import os

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # --- 1. Scene Render & Color Management Settings ---
    scene.render.engine = 'BLENDER_EEVEE'
    scene.eevee.use_bloom = False
    scene.eevee.use_ambient_occlusion = False
    scene.eevee.use_screen_space_reflections = False
    scene.render.use_motion_blur = False
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None' # Ensure no extra color grading is applied

    # --- 2. Enable Rigify Add-on ---
    try:
        if 'rigify' not in bpy.context.preferences.addons or not bpy.context.preferences.addons['rigify'].bl_info.get('enabled', False):
            bpy.ops.preferences.addon_enable(module='rigify')
    except Exception as e:
        print(f"Warning: Could not enable rigify add-on: {e}. Metarig might not be available.")
        # Proceeding without rigify if it cannot be enabled.

    # --- 3. Add Human Metarig for Scale Reference ---
    bpy.ops.object.select_all(action='DESELECT') # Deselect everything before adding new object
    metarig_obj = None
    if 'rigify' in bpy.context.preferences.addons and bpy.context.preferences.addons['rigify'].bl_info.get('enabled', False):
        bpy.ops.object.armature_human_add(enter_editmode=False)
        metarig_obj = bpy.context.active_object
        metarig_obj.name = f"{object_prefix}_HumanMetarig"
        metarig_obj.location = Vector(metarig_location)
        metarig_obj.scale = (metarig_scale, metarig_scale, metarig_scale)
        metarig_obj.show_in_front = True # Always show metarig in front
    else:
        print("Rigify add-on not enabled or available. Metarig creation skipped.")

    # --- 4. Add and Position Reference Images ---
    ref_images_created = []
    
    # Calculate target height for images based on metarig (if exists) or a default (2 Blender units)
    # The default Metarig height is approx 2 units at scale 1.0.
    target_height_units = (metarig_obj.dimensions.z if metarig_obj else 2.0) * metarig_scale

    # Front Reference Image
    if ref_image_front_path and os.path.exists(ref_image_front_path):
        bpy.ops.object.empty_image_add(filepath=ref_image_front_path, align='WORLD')
        ref_front = bpy.context.active_object
        ref_front.name = f"{object_prefix}_Ref_Front"
        ref_front.empty_display_type = 'IMAGE'
        ref_front.data.display_dop = ref_image_opacity # Set opacity in viewport
        ref_front.data.alpha = ref_image_opacity # Set alpha for render
        ref_front.data.use_depth = False # Display in front of other objects

        # Scale image to match target height
        if ref_front.data.image:
            image_width, image_height = ref_front.data.image.size
            aspect_ratio = image_width / image_height
            
            ref_front.scale.z = target_height_units # Set height directly
            ref_front.scale.x = ref_front.scale.z * aspect_ratio # Maintain aspect ratio
            ref_front.scale.y = 1.0 # Keep y scale as 1 for image planes

        # Rotate to stand upright and face forward (+Y direction)
        ref_front.rotation_euler[0] = math.radians(90) # Rotate along X to be vertical
        ref_front.rotation_euler[2] = math.radians(0)  # Face along +Y axis

        # Position relative to metarig location (centered on X,Z, placed behind metarig on Y)
        ref_front.location.x = metarig_location[0]
        ref_front.location.y = metarig_location[1] - ref_image_distance_from_rig
        ref_front.location.z = metarig_location[2] + (ref_front.dimensions.z / 2) # Lift to align bottom with ground

        ref_images_created.append(ref_front)
    elif ref_image_front_path:
        print(f"Warning: Front reference image not found at '{ref_image_front_path}'. Skipping.")

    # Side Reference Image
    if ref_image_side_path and os.path.exists(ref_image_side_path):
        bpy.ops.object.empty_image_add(filepath=ref_image_side_path, align='WORLD')
        ref_side = bpy.context.active_object
        ref_side.name = f"{object_prefix}_Ref_Side"
        ref_side.empty_display_type = 'IMAGE'
        ref_side.data.display_dop = ref_image_opacity
        ref_side.data.alpha = ref_image_opacity
        ref_side.data.use_depth = False # Display in front of other objects

        # Scale image to match target height
        if ref_side.data.image:
            image_width, image_height = ref_side.data.image.size
            aspect_ratio = image_width / image_height
            
            ref_side.scale.z = target_height_units
            ref_side.scale.x = ref_side.scale.z * aspect_ratio
            ref_side.scale.y = 1.0 # Keep y scale as 1 for image planes

        # Rotate to stand upright and face side (+X direction)
        ref_side.rotation_euler[0] = math.radians(90) # Rotate along X to be vertical
        ref_side.rotation_euler[2] = math.radians(90) # Rotate along Z to face along +X axis

        # Position relative to metarig location (centered on Y,Z, placed to the side of metarig on X)
        ref_side.location.x = metarig_location[0] + ref_image_distance_from_rig
        ref_side.location.y = metarig_location[1]
        ref_side.location.z = metarig_location[2] + (ref_side.dimensions.z / 2) # Lift to align bottom with ground

        ref_images_created.append(ref_side)
    elif ref_image_side_path:
        print(f"Warning: Side reference image not found at '{ref_image_side_path}'. Skipping.")
        
    # --- 5. Finalize ---
    # Deselect all and then select the metarig (if created) to match the video's end state
    bpy.ops.object.select_all(action='DESELECT')
    if metarig_obj:
        metarig_obj.select_set(True)
        bpy.context.view_layer.objects.active = metarig_obj

    return f"Set up character modeling scene for '{object_prefix}' with {len(ref_images_created)} references and {'a Human Metarig' if metarig_obj else 'no Metarig'}."

