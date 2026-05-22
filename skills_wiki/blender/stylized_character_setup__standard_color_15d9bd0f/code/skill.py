def create_object(
    scene_name: str = "Scene",
    object_name: str = "Stylized_Setup_Group",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (1.0, 1.0, 1.0),
    **kwargs,
) -> str:
    """
    Sets up a scene for Stylized/Low-Poly modeling as demonstrated in the tutorial,
    including Color Management tweaks, EEVEE optimization, and Reference Image planes.

    Args:
        scene_name: Name of the target scene.
        object_name: Prefix for the generated reference objects.
        location: Base location for the scale reference.
        scale: Multiplier for the default human height (1.7m base).
        material_color: Unused directly in setup, kept for signature consistency.
        
    Returns:
        Status string detailing the setup execution.
    """
    import bpy
    import math
    import addon_utils
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Stylized Render Settings ===
    # Force EEVEE for real-time stylized preview
    if scene.render.engine != 'BLENDER_EEVEE':
        scene.render.engine = 'BLENDER_EEVEE'
    
    # Disable photorealistic effects that interfere with stylized/flat shading
    if hasattr(scene, "eevee"):
        scene.eevee.use_gtao = False
        scene.eevee.use_bloom = False
        scene.eevee.use_ssr = False
        scene.eevee.use_motion_blur = False

    # CRITICAL: Set View Transform to Standard to preserve true hex colors
    scene.view_settings.view_transform = 'Standard'

    # === Step 2: Generate Placeholder Reference Images ===
    # Since we cannot download the zip file in a sandboxed script, we generate a placeholder
    img_name = f"{object_name}_Ref_Image"
    img = bpy.data.images.get(img_name)
    if not img:
        img = bpy.data.images.new(img_name, width=1024, height=1024)
        img.generated_type = 'COLOR_GRID'
    
    ref_height = 1.7 * scale

    # === Step 3: Front Reference ===
    bpy.ops.object.empty_add(type='IMAGE', location=(location[0], location[1], location[2] + (ref_height/2)))
    front_ref = bpy.context.active_object
    front_ref.name = f"{object_name}_Front_Ref"
    front_ref.data = img
    front_ref.empty_display_size = ref_height
    front_ref.rotation_euler = (math.radians(90), 0, 0)
    
    # Set transparency
    front_ref.use_empty_image_alpha = True
    front_ref.color[3] = 0.5  # 50% opacity

    # === Step 4: Side Reference ===
    # Offset backward on Y so it doesn't intersect with the front view modeling
    bpy.ops.object.empty_add(type='IMAGE', location=(location[0], location[1] - (ref_height/2), location[2] + (ref_height/2)))
    side_ref = bpy.context.active_object
    side_ref.name = f"{object_name}_Side_Ref"
    side_ref.data = img
    side_ref.empty_display_size = ref_height
    side_ref.rotation_euler = (math.radians(90), 0, math.radians(90))
    
    # Set transparency
    side_ref.use_empty_image_alpha = True
    side_ref.color[3] = 0.5

    # === Step 5: Scale Reference ===
    # Attempt to use Rigify as shown in video; use wireframe cylinder as robust fallback
    scale_ref_created = False
    
    # Check if rigify can be enabled
    try:
        addon_utils.enable("rigging_rigify")
        bpy.ops.object.armature_human_metarig_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_Scale_MetaRig"
        rig.scale = (scale, scale, scale)
        scale_ref_created = True
    except Exception:
        pass
        
    if not scale_ref_created:
        # Fallback to a simple 1.7m primitive to represent human scale
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.25 * scale, 
            depth=ref_height, 
            location=(location[0], location[1], location[2] + (ref_height/2))
        )
        rig = bpy.context.active_object
        rig.name = f"{object_name}_Scale_Dummy"
        rig.display_type = 'WIRE'  # Set to wireframe so it doesn't block modeling

    # Optional: Group them in a collection for neatness
    setup_collection_name = f"{object_name}_Collection"
    setup_col = bpy.data.collections.get(setup_collection_name)
    if not setup_col:
        setup_col = bpy.data.collections.new(setup_collection_name)
        scene.collection.children.link(setup_col)
    
    # Move created objects to the new collection
    for obj in [front_ref, side_ref, rig]:
        for col in obj.users_collection:
            col.objects.unlink(obj)
        setup_col.objects.link(obj)

    return f"Prepared Stylized Scene: View Transform set to 'Standard'. Created {object_name}_Front_Ref, Side_Ref, and Scale Reference at {location}."
