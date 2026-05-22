def create_stylized_character_prep(
    scene_name: str = "Scene",
    object_name: str = "CharacterPrep",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (1.0, 0.4, 0.7), 
    **kwargs,
) -> str:
    """
    Create a Stylized Character Modeling Prep Setup in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created rig and references.
        location: (x, y, z) world-space position for the setup.
        scale: Uniform scale factor for the rig and image references.
        material_color: (R, G, B) color used to tint the placeholder reference images.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import addon_utils
    from mathutils import Euler
    import math

    # Get target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Configure EEVEE for Stylized/Low-Poly Rendering ===
    scene.render.engine = 'BLENDER_EEVEE'
    scene.view_settings.view_transform = 'Standard' # Crucial for 1-to-1 flat colors
    
    # Disable photorealistic effects that ruin stylized colors
    if hasattr(scene, "eevee"):
        scene.eevee.use_gtao = False
        scene.eevee.use_bloom = False
        scene.eevee.use_ssr = False
        scene.eevee.use_motion_blur = False

    # === Step 2: Add Scale Reference Rig ===
    # Enable Rigify if not already enabled
    addon_utils.enable("rigify")
    
    # Store active collection
    collection = scene.collection
    
    # Spawning the human metarig
    bpy.ops.object.armature_human_metarig_add(location=location)
    rig = bpy.context.active_object
    rig.name = f"{object_name}_ScaleRig"
    rig.scale = (scale, scale, scale)
    rig.display_type = 'WIRE'
    rig.show_in_front = True # Ensures the rig is always visible

    # === Step 3: Create Placeholder Reference Images ===
    # Generate 64x64 solid color images in memory to act as reference placeholders
    img_size = 64
    front_img = bpy.data.images.new(f"{object_name}_Ref_Front", width=img_size, height=img_size)
    side_img = bpy.data.images.new(f"{object_name}_Ref_Side", width=img_size, height=img_size)
    
    # Fill Front image (Base color)
    front_pixels = [material_color[0], material_color[1], material_color[2], 1.0] * (img_size * img_size)
    front_img.pixels = front_pixels
    
    # Fill Side image (Inverted color for visual distinction)
    side_pixels = [material_color[2], material_color[0], material_color[1], 1.0] * (img_size * img_size)
    side_img.pixels = side_pixels

    # === Step 4: Add Reference Empties ===
    # Front Reference (placed behind the rig looking from Numpad 1)
    front_empty = bpy.data.objects.new(f"{object_name}_RefEmpty_Front", None)
    front_empty.empty_display_type = 'IMAGE'
    front_empty.data = front_img
    front_empty.color[3] = 0.5  # 50% opacity
    front_empty.use_empty_image_alpha = True
    front_empty.location = (location[0], location[1] + (2.0 * scale), location[2] + (1.0 * scale))
    front_empty.rotation_euler = Euler((math.radians(90), 0, 0))
    front_empty.empty_display_size = 2.2 * scale
    collection.objects.link(front_empty)

    # Side Reference (placed to the side looking from Numpad 3)
    side_empty = bpy.data.objects.new(f"{object_name}_RefEmpty_Side", None)
    side_empty.empty_display_type = 'IMAGE'
    side_empty.data = side_img
    side_empty.color[3] = 0.5   # 50% opacity
    side_empty.use_empty_image_alpha = True
    side_empty.location = (location[0] - (2.0 * scale), location[1], location[2] + (1.0 * scale))
    side_empty.rotation_euler = Euler((math.radians(90), 0, math.radians(90)))
    side_empty.empty_display_size = 2.2 * scale
    collection.objects.link(side_empty)

    # Clean up selection and make rig active
    bpy.ops.object.select_all(action='DESELECT')
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig

    return f"Created '{object_name}' modeling setup. View Transform set to 'Standard', spawned Scale Rig and 2 Orthographic Reference Empties at {location}."
