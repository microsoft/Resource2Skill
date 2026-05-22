def create_object(
    scene_name: str = "Scene",
    object_name: str = "CharacterSetup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.8),
    **kwargs,
) -> str:
    """
    Create a Stylized Character Environment & Scale Setup in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created reference setup.
        location: (x, y, z) world-space position for the center of the setup.
        scale: Uniform scale factor (1.0 = ~2 meter tall character reference).
        material_color: (R, G, B) tint color for the generated placeholder reference images.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created setup.
    """
    import bpy
    import addon_utils
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Configure Environment for Stylized Rendering ===
    scene.render.engine = 'BLENDER_EEVEE'
    scene.view_settings.view_transform = 'Standard'

    # Disable realistic post-processing in EEVEE (checks attributes for cross-version compatibility)
    if hasattr(scene, "eevee"):
        if hasattr(scene.eevee, "use_gtao"):
            scene.eevee.use_gtao = False
        if hasattr(scene.eevee, "use_bloom"):
            scene.eevee.use_bloom = False
        if hasattr(scene.eevee, "use_ssr"):
            scene.eevee.use_ssr = False
        if hasattr(scene.eevee, "use_motion_blur"):
            scene.eevee.use_motion_blur = False

    created_items = []

    # === Step 2: Enable Rigify & Add Human Meta-Rig ===
    try:
        addon_utils.enable("rigging_rigify", default_set=True)
        
        # Add the meta-rig using the operator
        bpy.ops.object.armature_human_metarig_add(location=location)
        metarig = bpy.context.active_object
        metarig.name = f"{object_name}_Scale_Metarig"
        metarig.scale = (scale, scale, scale)
        metarig.display_type = 'WIRE'
        
        created_items.append(metarig.name)
    except Exception as e:
        print(f"Note: Could not add Rigify metarig. Error: {e}")

    # === Step 3: Create Synthetic Reference Images ===
    # We generate semi-transparent blank images as placeholders.
    # Users can later replace the file paths of these images with real character art.
    img_width, img_height = 512, 1024
    front_img = bpy.data.images.new(name=f"{object_name}_Front_Art", width=img_width, height=img_height, alpha=True)
    side_img = bpy.data.images.new(name=f"{object_name}_Side_Art", width=img_width, height=img_height, alpha=True)
    
    # Fill image pixels with a flat color
    rgba = list(material_color) + [0.3] # Base color + low alpha
    pixels = rgba * (img_width * img_height)
    front_img.pixels = pixels
    side_img.pixels = pixels

    # === Step 4: Setup Front Reference Empty ===
    front_empty = bpy.data.objects.new(f"{object_name}_Ref_Front", None)
    front_empty.empty_display_type = 'IMAGE'
    front_empty.data = front_img
    # Push back on Y axis, lift on Z axis
    front_empty.location = Vector(location) + Vector((0, 1.5 * scale, 1.0 * scale))
    front_empty.rotation_euler = (math.radians(90), 0, 0)
    front_empty.empty_display_size = 2.0 * scale
    front_empty.use_empty_image_alpha = True
    front_empty.empty_image_alpha = 0.5
    
    scene.collection.objects.link(front_empty)
    created_items.append(front_empty.name)

    # === Step 5: Setup Side Reference Empty ===
    side_empty = bpy.data.objects.new(f"{object_name}_Ref_Side", None)
    side_empty.empty_display_type = 'IMAGE'
    side_empty.data = side_img
    # Push back on X axis, lift on Z axis, rotate to face X
    side_empty.location = Vector(location) + Vector((-1.5 * scale, 0, 1.0 * scale))
    side_empty.rotation_euler = (math.radians(90), 0, math.radians(-90))
    side_empty.empty_display_size = 2.0 * scale
    side_empty.use_empty_image_alpha = True
    side_empty.empty_image_alpha = 0.5
    
    scene.collection.objects.link(side_empty)
    created_items.append(side_empty.name)

    return f"Created Stylized Scene Environment '{object_name}' with elements: {', '.join(created_items)}"
