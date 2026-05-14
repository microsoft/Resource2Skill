def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedSetup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a Stylized Workspace Setup with correct color management and reference proxies.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated proxy and references.
        location: (x, y, z) base position for the rig.
        scale: Uniform scale factor for the rig and references.
        material_color: Unused directly in this setup, but accepted for signature compatibility.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Render Engine & Realistic FX Cleanup ===
    # Enforce Eevee for stylized workflows
    if scene.render.engine not in ['BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE']:
        try:
            scene.render.engine = 'BLENDER_EEVEE_NEXT' # Blender 4.2+
        except TypeError:
            scene.render.engine = 'BLENDER_EEVEE' # Older versions

    # Disable generic realistic FX to keep the viewport clean and fast
    if hasattr(scene, "eevee"):
        if hasattr(scene.eevee, "use_bloom"): scene.eevee.use_bloom = False
        if hasattr(scene.eevee, "use_ssr"): scene.eevee.use_ssr = False
        if hasattr(scene.eevee, "use_gtao"): scene.eevee.use_gtao = False

    # === Step 2: CRITICAL - Stylized Color Management ===
    # Set View Transform to Standard for accurate 1:1 stylized colors (removes cinematic desaturation)
    scene.view_settings.view_transform = 'Standard'

    # === Step 3: Scale Reference Proxy ===
    # Enable Rigify addon to access the meta-rig
    try:
        bpy.ops.preferences.addon_enable(module="rigify")
    except Exception:
        pass

    # Add Human Meta-Rig as a physical size reference
    try:
        bpy.ops.object.armature_human_metarig_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_Scale_Proxy"
        rig.scale = (scale, scale, scale)
    except Exception:
        # Fallback if rigify fails to load (creates a roughly human-sized bounding box)
        bpy.ops.mesh.primitive_cube_add(location=(location[0], location[1], location[2] + scale))
        rig = bpy.context.active_object
        rig.name = f"{object_name}_Scale_Proxy_Fallback"
        rig.scale = (scale * 0.5, scale * 0.5, scale) 

    # === Step 4: Reference Image Placeholders ===
    # Front Reference (Facing -Y axis)
    bpy.ops.object.empty_add(
        type='IMAGE', 
        align='WORLD', 
        location=(location[0], location[1] + (0.5 * scale), location[2] + (1 * scale)), 
        rotation=(math.radians(90), 0, 0)
    )
    front_ref = bpy.context.active_object
    front_ref.name = f"{object_name}_Ref_Front"
    front_ref.empty_display_size = 2.0 * scale

    # Side Reference (Facing +X axis)
    bpy.ops.object.empty_add(
        type='IMAGE', 
        align='WORLD', 
        location=(location[0] - (0.5 * scale), location[1], location[2] + (1 * scale)), 
        rotation=(math.radians(90), 0, math.radians(90))
    )
    side_ref = bpy.context.active_object
    side_ref.name = f"{object_name}_Ref_Side"
    side_ref.empty_display_size = 2.0 * scale

    # Group everything nicely (Optional but good practice)
    for obj in [rig, front_ref, side_ref]:
        if obj.parent is None:
            pass # In a full system, we might parent the empties to the rig

    return f"Created Stylized Workspace '{object_name}' with Standard Color Management and Reference Proxies at {location}"
