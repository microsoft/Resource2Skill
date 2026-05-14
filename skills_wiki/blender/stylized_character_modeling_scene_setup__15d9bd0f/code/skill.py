def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedSetup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a Stylized Character Modeling Scene Setup in the active Blender scene.
    Configures color management, lighting settings, and adds a scale-accurate 
    rig scaffolding with pre-configured reference image planes.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created setup objects.
        location: (x, y, z) world-space position for the setup.
        scale: Uniform scale factor (1.0 = standard human height ~1.7m).
        material_color: Unused in this specific setup script, kept for signature consistency.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created setup.
    """
    import bpy
    import math
    from mathutils import Vector
    import addon_utils

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Stylized Render & Color Management Setup ===
    scene.render.engine = 'BLENDER_EEVEE'
    
    # Disable photorealistic post-processing for clean stylized modeling
    if hasattr(scene.eevee, "use_bloom"): 
        scene.eevee.use_bloom = False
    if hasattr(scene.eevee, "use_ssr"): 
        scene.eevee.use_ssr = False
    if hasattr(scene.eevee, "use_gtao"): 
        scene.eevee.use_gtao = False
    if hasattr(scene.eevee, "use_motion_blur"): 
        scene.eevee.use_motion_blur = False
        
    # Crucial step for stylized textures: Prevent 'Filmic' color washing
    try:
        scene.view_settings.view_transform = 'Standard'
    except TypeError:
        pass # Failsafe

    created_objects = []

    # === Step 2: Add Human Meta-Rig for Exact Scaling ===
    rig_name = f"{object_name}_ScaleProxy_Rig"
    addon_utils.enable("rigify")
    
    try:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.armature_human_metarig_add(location=location)
        metarig = bpy.context.active_object
        metarig.name = rig_name
        metarig.scale = (scale, scale, scale)
        created_objects.append(metarig.name)
        anchor_obj = metarig
    except Exception as e:
        print(f"Rigify Meta-Rig failed: {e}. Generating fallback bounding box.")
        # Fallback if Rigify is missing/fails in the specific Blender environment
        bpy.ops.mesh.primitive_cube_add(location=(location[0], location[1], location[2] + 1.0 * scale))
        box = bpy.context.active_object
        box.name = rig_name
        box.scale = (scale * 0.3, scale * 0.3, scale * 1.0)
        box.display_type = 'WIRE'
        created_objects.append(box.name)
        anchor_obj = box

    # === Step 3: Add Pre-configured Reference Image Placeholders ===
    
    # Front Reference
    bpy.ops.object.empty_add(type='IMAGE', location=location)
    front_ref = bpy.context.active_object
    front_ref.name = f"{object_name}_Ref_Front"
    front_ref.scale = (scale * 2.0, scale * 2.0, scale * 2.0)
    # Set to 50% opacity
    front_ref.use_empty_image_alpha = True
    front_ref.color[3] = 0.5 
    # Push back on Y axis so it doesn't clip with the model being built
    front_ref.location.y += 1.5 * scale
    created_objects.append(front_ref.name)

    # Side Reference
    bpy.ops.object.empty_add(type='IMAGE', location=location)
    side_ref = bpy.context.active_object
    side_ref.name = f"{object_name}_Ref_Side"
    # Rotate 90 degrees for side view profile
    side_ref.rotation_euler = (0, 0, math.radians(90))
    side_ref.scale = (scale * 2.0, scale * 2.0, scale * 2.0)
    # Set to 50% opacity
    side_ref.use_empty_image_alpha = True
    side_ref.color[3] = 0.5
    # Push left on X axis so it doesn't clip with the model being built
    side_ref.location.x -= 1.5 * scale
    created_objects.append(side_ref.name)

    # Parent references to the scale proxy so they move as one unit
    front_ref.parent = anchor_obj
    side_ref.parent = anchor_obj

    return f"Created Setup '{object_name}' at {location}. Color space: 'Standard'. Objects: {', '.join(created_objects)}."
