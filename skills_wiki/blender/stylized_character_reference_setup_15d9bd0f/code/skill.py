def setup_character_references(
    scene_name: str = "Scene",
    metarig_name: str = "CharacterMetarig",
    front_image_path: str = "lovechan_frontview.png",
    side_image_path: str = "lovechan_sideview.png",
    resources_dir: str = "",  # Directory containing reference images
    character_height: float = 1.75,  # Target height for the Metarig in Blender units
    front_img_y_offset: float = -1.0,  # Y-offset for the front reference image
    side_img_x_offset: float = 1.0,  # X-offset for the side reference image
    **kwargs,
) -> str:
    """
    Sets up Blender scene with specified rendering settings, a Rigify Human Meta-Rig,
    and aligned 2D reference images for character modeling.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        metarig_name: Name for the created Human Meta-Rig object.
        front_image_path: Filename of the front view reference image.
        side_image_path: Filename of the side view reference image.
        resources_dir: Absolute path to the directory containing the reference images.
                       e.g., "C:/Users/User/Documents/BlenderProjects/LowPolyCharacter/resources"
        character_height: Target height for the Metarig (and thus the character) in Blender units.
        front_img_y_offset: Y-axis offset for the front reference image relative to origin.
        side_img_x_offset: X-axis offset for the side reference image relative to origin.
        **kwargs: Additional overrides (e.g., opacity, other render settings).

    Returns:
        Status string, e.g., "Created 'CharacterMetarig' and 2 reference images."
    """
    import bpy
    import os
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # --- 1. Scene Configuration ---
    # Set render engine to EEVEE
    scene.render.engine = 'BLENDER_EEVEE'
    
    # Disable EEVEE post-processing effects
    scene.eevee.use_bloom = kwargs.get('use_bloom', False)
    scene.eevee.use_ssr = kwargs.get('use_ssr', False) # Screen Space Reflections
    scene.eevee.use_ao = kwargs.get('use_ao', False)   # Ambient Occlusion
    scene.render.use_motion_blur = kwargs.get('use_motion_blur', False)

    # Set View Transform to 'Standard' for consistent color appearance
    scene.view_settings.view_transform = 'Standard'

    # --- 2. Add Human Meta-Rig (Scale Reference) ---
    # Enable Rigify Add-on if not already enabled
    try:
        bpy.ops.preferences.addon_enable(module='rigify')
    except Exception as e:
        print(f"Could not enable Rigify: {e}. It might already be enabled or missing.")

    # Deselect all objects first
    bpy.ops.object.select_all(action='DESELECT')
    
    # Add Human Meta-Rig
    # Note: 'object.armature_add' requires Rigify to be enabled.
    bpy.ops.object.armature_add(type='HUMAN', enter_editmode=False, align='WORLD')
    metarig_obj = bpy.context.active_object
    metarig_obj.name = metarig_name
    
    # Reset Metarig transforms (it spawns in T-pose at origin by default)
    # Scaling can sometimes be applied without needing to reset, but good practice.
    bpy.ops.object.visual_transform_apply() # Apply visual scale/rot/loc to actual values

    # Scale Metarig to desired character height (default Metarig height is approx 2.0 units)
    default_metarig_height = 2.0 # Standard Metarig is approx 2 units tall
    scale_factor = character_height / default_metarig_height
    metarig_obj.scale = (scale_factor, scale_factor, scale_factor)
    
    # Apply scale to prevent issues later (e.g., with parenting or modifiers)
    bpy.ops.object.select_all(action='DESELECT')
    metarig_obj.select_set(True)
    bpy.context.view_layer.objects.active = metarig_obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # --- 3. Add Reference Images ---
    opacity = kwargs.get('opacity', 0.5)

    # Resolve full paths for images
    full_front_image_path = os.path.join(resources_dir, front_image_path)
    full_side_image_path = os.path.join(resources_dir, side_image_path)

    # Front Reference Image
    bpy.ops.object.empty_image_add(
        name=f"{object_name}_FrontRef",
        filepath=full_front_image_path,
        align_axis_x=True, # Align X to world X (for upright image)
        align_axis_y=False, 
        align_axis_z=True, # This makes the image stand upright, along Z axis
        location=(0, front_img_y_offset * scale_factor, 0), # Place behind Metarig on Y
        rotation=(math.radians(90), 0, 0) # Rotate to stand upright if not already. Ensure to align correctly.
    )
    front_ref_obj = bpy.context.active_object
    front_ref_obj.name = f"{object_name}_FrontRef"
    front_ref_obj.empty_display_type = 'IMAGE'
    front_ref_obj.image_user.opacity = opacity
    
    # Set image scale based on character height, assuming 1:1 image aspect ratio
    # If image aspect ratio is not 1:1, adjust width/height properties accordingly.
    if front_ref_obj.data and front_ref_obj.data.images:
        image = front_ref_obj.data.images[0]
        aspect_ratio = image.size[0] / image.size[1]
        front_ref_obj.scale = (character_height * aspect_ratio, character_height, character_height) # Scale X by aspect ratio
        front_ref_obj.scale = (front_ref_obj.scale[0] * scale_factor, front_ref_obj.scale[1] * scale_factor, front_ref_obj.scale[2] * scale_factor) # Apply general scale factor


    # Side Reference Image
    bpy.ops.object.empty_image_add(
        name=f"{object_name}_SideRef",
        filepath=full_side_image_path,
        align_axis_x=False,
        align_axis_y=True, # Align Y to world Y (for upright image)
        align_axis_z=True, # This makes the image stand upright, along Z axis
        location=(side_img_x_offset * scale_factor, 0, 0), # Place to the side of Metarig on X
        rotation=(math.radians(90), 0, math.radians(90)) # Rotate to stand upright and face -X
    )
    side_ref_obj = bpy.context.active_object
    side_ref_obj.name = f"{object_name}_SideRef"
    side_ref_obj.empty_display_type = 'IMAGE'
    side_ref_obj.image_user.opacity = opacity

    # Set image scale based on character height
    if side_ref_obj.data and side_ref_obj.data.images:
        image = side_ref_obj.data.images[0]
        aspect_ratio = image.size[0] / image.size[1]
        side_ref_obj.scale = (character_height * aspect_ratio, character_height, character_height) # Scale X by aspect ratio
        side_ref_obj.scale = (side_ref_obj.scale[0] * scale_factor, side_ref_obj.scale[1] * scale_factor, side_ref_obj.scale[2] * scale_factor) # Apply general scale factor


    # Align Metarig to the bottom of the character's feet (assuming image feet are at Z=0)
    # The Metarig's root bone is usually at its feet, so this might not be needed if character_height is correctly set
    # and the images are centered around Z=0.
    
    # --- 4. Finalize ---
    # Group reference objects into a collection for easy management
    ref_collection_name = f"{object_name}_References"
    if ref_collection_name not in bpy.data.collections:
        ref_collection = bpy.data.collections.new(name=ref_collection_name)
        scene.collection.children.link(ref_collection)
    else:
        ref_collection = bpy.data.collections[ref_collection_name]

    # Link objects to the new collection and unlink from scene collection
    for obj in [metarig_obj, front_ref_obj, side_ref_obj]:
        if obj and obj.name not in ref_collection.objects:
            ref_collection.objects.link(obj)
            # Unlink from scene collection, only if it's not the primary collection
            if obj.name in scene.collection.objects:
                 scene.collection.objects.unlink(obj)

    return f"Created '{metarig_name}' and 2 reference images in '{ref_collection_name}'."

