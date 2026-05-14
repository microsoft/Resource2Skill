def setup_character_modeling_scene(
    scene_name: str = "Scene",
    reference_image_front_path: str = "",  # Absolute path required (e.g., "C:/Users/User/Documents/Love_Chan_Frontview.png")
    reference_image_side_path: str = "",   # Absolute path required (e.g., "C:/Users/User/Documents/Love_Chan_Sideview.png")
    character_height_m: float = 2.0,       # Desired approximate height of the character in meters
    reference_opacity: float = 0.5,
    reference_image_front_y_offset: float = -2.0, # Y-axis offset for the front reference image relative to metarig
    reference_image_side_x_offset: float = 2.0,   # X-axis offset for the side reference image relative to metarig
    **kwargs,
) -> str:
    """
    Sets up a Blender scene for stylized character modeling.
    Configures render settings, adds reference images, and a Rigify Human Metarig
    for scale and proportion guidance.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        reference_image_front_path: Absolute file path to the front reference image (PNG/JPG).
                                    Provide an empty string to skip adding this reference.
        reference_image_side_path: Absolute file path to the side reference image (PNG/JPG).
                                   Provide an empty string to skip adding this reference.
        character_height_m: Desired approximate height of the character in meters for metarig scaling.
        reference_opacity: Opacity for the reference image planes (0.0 to 1.0).
        reference_image_front_y_offset: Y-axis offset for the front reference image relative to metarig's origin.
        reference_image_side_x_offset: X-axis offset for the side reference image relative to metarig's origin.
        **kwargs: Additional overrides (not used in this version).

    Returns:
        Status string, e.g., "Set up character modeling scene with references and metarig. Character height: 2.0m."
    """
    import bpy
    from mathutils import Vector
    import math
    import os

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 1. Scene Configuration ---
    # Set Render Engine to EEVEE
    scene.render.engine = 'BLENDER_EEVEE'

    # Disable features for stylized look (as per tutorial)
    scene.eevee.use_bloom = False
    scene.eevee.use_ssao = False
    scene.eevee.use_ssr = False
    scene.render.use_motion_blur = False

    # Set Color Management View Transform to Standard
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None' # Ensure no look is applied (e.g., Medium Contrast)

    # --- 2. Enable Rigify Add-on ---
    # Ensure Rigify is enabled (it's a default add-on)
    if 'rigify' not in bpy.context.preferences.addons:
        bpy.ops.preferences.addon_enable(module='rigify')

    front_ref_obj = None
    side_ref_obj = None
    metarig_obj = None
    all_created_objects = []

    # --- 3. Add Reference Images ---
    bpy.ops.object.select_all(action='DESELECT')
    if reference_image_front_path and os.path.exists(reference_image_front_path):
        bpy.ops.image.reference_add(filepath=reference_image_front_path)
        front_ref_obj = bpy.context.view_layer.objects.active
        front_ref_obj.name = "CharacterFrontRef"
        front_ref_obj.data.display_settings.opacity = reference_opacity
        front_ref_obj.empty_display_type = 'IMAGE'
        all_created_objects.append(front_ref_obj)
        print(f"Added front reference image: {front_ref_obj.name}")
    else:
        print(f"Warning: Front reference image not found or path empty: {reference_image_front_path}. Skipping.")

    bpy.ops.object.select_all(action='DESELECT')
    if reference_image_side_path and os.path.exists(reference_image_side_path):
        bpy.ops.image.reference_add(filepath=reference_image_side_path)
        side_ref_obj = bpy.context.view_layer.objects.active
        side_ref_obj.name = "CharacterSideRef"
        side_ref_obj.data.display_settings.opacity = reference_opacity
        side_ref_obj.empty_display_type = 'IMAGE'
        all_created_objects.append(side_ref_obj)
        print(f"Added side reference image: {side_ref_obj.name}")
    else:
        print(f"Warning: Side reference image not found or path empty: {reference_image_side_path}. Skipping.")

    # --- 4. Add Rigify Human Metarig ---
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.armature_add(type='HUMAN')
    metarig_obj = bpy.context.view_layer.objects.active
    metarig_obj.name = "CharacterMetarig"
    all_created_objects.append(metarig_obj)
    print(f"Added metarig: {metarig_obj.name}")

    if not all_created_objects:
        return "Error: No reference images or metarig could be added. Please check file paths."

    # --- 5. Initial Alignment of all components ---
    # Select all created objects to apply common transformations
    bpy.ops.object.select_all(action='DESELECT')
    for obj in all_created_objects:
        obj.select_set(True)
    
    if metarig_obj:
        bpy.context.view_layer.objects.active = metarig_obj # Set metarig as active for transformations

    # Clear transformations (Alt+G, Alt+R, Alt+S equivalent)
    bpy.ops.object.location_clear()
    bpy.ops.object.rotation_clear()
    bpy.ops.object.scale_clear()

    # --- 6. Detailed Positioning and Rotation ---
    # Rigify metarig is typically 2 units tall by default.
    # Scale metarig to desired character height and align feet to Z=0 (ground plane)
    if metarig_obj:
        metarig_scale_factor = character_height_m / 2.0 # Default metarig height is 2 units
        metarig_obj.scale = (metarig_scale_factor, metarig_scale_factor, metarig_scale_factor)
        metarig_obj.location.z = character_height_m / 2.0 # Move up half its height to put feet at Z=0

    # Position Front Reference (assumes character faces +Y axis)
    if front_ref_obj:
        front_ref_obj.rotation_euler.x = math.radians(90) # Rotate to stand upright
        front_ref_obj.location.y = metarig_obj.location.y + reference_image_front_y_offset
        front_ref_obj.location.z = metarig_obj.location.z

    # Position Side Reference (assumes character faces +X axis from side view)
    if side_ref_obj:
        side_ref_obj.rotation_euler.x = math.radians(90) # Rotate to stand upright
        side_ref_obj.rotation_euler.z = math.radians(90) # Rotate around Z to face sideways (+X)
        side_ref_obj.location.x = metarig_obj.location.x + reference_image_side_x_offset
        side_ref_obj.location.z = metarig_obj.location.z

    # Select only the metarig as the final active object for convenience
    bpy.ops.object.select_all(action='DESELECT')
    if metarig_obj:
        metarig_obj.select_set(True)
        bpy.context.view_layer.objects.active = metarig_obj

    return f"Set up character modeling scene with references and metarig. Character height: {character_height_m}m."

