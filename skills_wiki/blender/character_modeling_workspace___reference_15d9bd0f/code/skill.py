def create_object(
    scene_name: str = "Scene",
    object_name: str = "CharacterSetup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1), # Unused, kept for standard signature
    **kwargs,
) -> str:
    """
    Create a Character Modeling Workspace setup in the active Blender scene.
    Includes color management setup, a Rigify Meta-Rig for scale, 
    and positioned Image Empties for front and side references.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created setup objects.
        location: (x, y, z) world-space origin for the setup.
        scale: Uniform scale factor for the rig and empties.
        material_color: Unused in this specific tool.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created setup.
    """
    import bpy
    import math
    import addon_utils
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Scene & Render Settings ===
    # Set View Transform to Standard for accurate reference color picking
    scene.view_settings.view_transform = 'Standard'
    
    # Ensure EEVEE is the active engine for optimal modeling viewport
    if scene.render.engine != 'BLENDER_EEVEE_NEXT' and scene.render.engine != 'BLENDER_EEVEE':
        # Fallback to standard EEVEE depending on Blender version
        try:
            scene.render.engine = 'BLENDER_EEVEE_NEXT'
        except TypeError:
            scene.render.engine = 'BLENDER_EEVEE'

    # === Step 2: Spawn Scale Reference Rig ===
    # Enable Rigify add-on required for the human meta-rig
    addon_utils.enable("rigify")

    # Store current selection to restore later
    bpy.ops.object.select_all(action='DESELECT')

    loc_vec = Vector(location)

    try:
        # Spawn the Rigify Human Meta-Rig
        bpy.ops.object.armature_human_metarig_add(location=loc_vec)
        scale_rig = bpy.context.active_object
        scale_rig.name = f"{object_name}_Scale_Reference_Rig"
        scale_rig.scale = (scale, scale, scale)
        
        # Move rig to origin perfectly
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    except AttributeError:
        # Fallback if Rigify fails to load properly
        bpy.ops.object.armature_add(location=loc_vec)
        scale_rig = bpy.context.active_object
        scale_rig.name = f"{object_name}_Scale_Reference_Fallback"
        scale_rig.scale = (scale, scale, scale)

    # === Step 3: Spawn Reference Image Empties ===
    # Front Reference (Pushed back slightly on Y axis)
    front_loc = loc_vec + Vector((0, 1.5 * scale, 1.0 * scale))
    bpy.ops.object.empty_add(
        type='IMAGE', 
        location=front_loc, 
        rotation=(math.pi/2, 0, 0)
    )
    ref_front = bpy.context.active_object
    ref_front.name = f"{object_name}_Reference_Front"
    ref_front.empty_display_size = 2.0 * scale
    # Enable transparency for modeling visibility
    ref_front.use_empty_image_alpha = True
    ref_front.color[3] = 0.5  # 50% opacity
    ref_front.show_empty_image_only = True

    # Side Reference (Pushed left slightly on X axis)
    side_loc = loc_vec + Vector((-1.5 * scale, 0, 1.0 * scale))
    bpy.ops.object.empty_add(
        type='IMAGE', 
        location=side_loc, 
        rotation=(math.pi/2, 0, math.pi/2)
    )
    ref_side = bpy.context.active_object
    ref_side.name = f"{object_name}_Reference_Side"
    ref_side.empty_display_size = 2.0 * scale
    ref_side.use_empty_image_alpha = True
    ref_side.color[3] = 0.5
    ref_side.show_empty_image_only = True

    # Grouping (Optional, but clean)
    bpy.ops.object.select_all(action='DESELECT')
    ref_front.select_set(True)
    ref_side.select_set(True)
    scale_rig.select_set(True)
    bpy.context.view_layer.objects.active = scale_rig

    return f"Created character setup '{object_name}' at {location}. Note: Assign images manually to the created Empties."
