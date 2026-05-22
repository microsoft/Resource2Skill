def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedSetup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (1.0, 1.0, 1.0),
    **kwargs,
) -> str:
    """
    Create a Stylized Character Scene Setup in the active Blender scene.
    Configures color management, Eevee settings, and spawns scale/reference objects.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created reference objects.
        location: (x, y, z) world-space position for the rig.
        scale: Uniform scale factor (1.0 = ~1.8 meters tall).
        material_color: Ignored (uses generated grid texture).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector
    import addon_utils

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Render & Color Management Setup ===
    # Ensure EEVEE is active
    if hasattr(bpy.types.Scene, 'eevee') and bpy.app.version >= (4, 2, 0):
        scene.render.engine = 'BLENDER_EEVEE_NEXT' 
    else:
        scene.render.engine = 'BLENDER_EEVEE'
    
    # Disable distracting post-processing for clean modeling silhouettes
    eevee = scene.eevee
    if hasattr(eevee, "use_ssr"): eevee.use_ssr = False
    if hasattr(eevee, "use_bloom"): eevee.use_bloom = False
    if hasattr(eevee, "use_motion_blur"): eevee.use_motion_blur = False
    if hasattr(eevee, "use_gtao"): eevee.use_gtao = False

    # CRITICAL: Use 'Standard' view transform for 1:1 color representation in stylized rendering
    scene.view_settings.view_transform = 'Standard'

    # === Step 2: Establish Scale with Meta-Rig ===
    # Enable Rigify temporarily to access the Human Meta-Rig
    is_rigify_enabled = addon_utils.check("rigify")[0]
    if not is_rigify_enabled:
        addon_utils.enable("rigify", default_set=True)
    
    scale_rig = None
    try:
        bpy.ops.object.armature_human_metarig_add(location=location)
        scale_rig = bpy.context.active_object
        scale_rig.name = f"{object_name}_ScaleRig"
        scale_rig.scale = (scale, scale, scale)
    except Exception:
        # Fallback if rigify fails to load
        bpy.ops.object.armature_add(location=location)
        scale_rig = bpy.context.active_object
        scale_rig.name = f"{object_name}_ScaleRig_Fallback"
        scale_rig.scale = (scale, scale, scale)

    # === Step 3: Reference Image Planes ===
    # Generate placeholder texture (since external downloads aren't available)
    img_name = f"{object_name}_Blueprint"
    img = bpy.data.images.get(img_name)
    if not img:
        img = bpy.data.images.new(img_name, width=1024, height=1024, alpha=True)
        img.generated_type = 'COLOR_GRID'
    
    # Setup Reference Material (Semi-transparent & Unlit)
    mat = bpy.data.materials.new(name=f"{object_name}_Ref_Mat")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'
    mat.shadow_method = 'NONE'
    
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        tex = mat.node_tree.nodes.new('ShaderNodeTexImage')
        tex.image = img
        mat.node_tree.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
        
        # Make transparent for modeling overlay
        if 'Alpha' in bsdf.inputs:
            bsdf.inputs['Alpha'].default_value = 0.5
        
        # Route to emission so blueprints are visible without scene lights
        emission_input = bsdf.inputs.get('Emission Color') or bsdf.inputs.get('Emission')
        if emission_input:
            mat.node_tree.links.new(tex.outputs['Color'], emission_input)
        if 'Emission Strength' in bsdf.inputs:
            bsdf.inputs['Emission Strength'].default_value = 1.0

    # Create Front Reference Plane
    bpy.ops.mesh.primitive_plane_add(size=2.5 * scale, location=(location[0], location[1] + 1.5 * scale, location[2] + 1.25 * scale))
    front_ref = bpy.context.active_object
    front_ref.name = f"{object_name}_Ref_Front"
    front_ref.rotation_euler = (math.radians(90), 0, 0)
    front_ref.data.materials.append(mat)
    front_ref.hide_select = True  # Prevent accidental selection while modeling
    if scale_rig:
        front_ref.parent = scale_rig

    # Create Side Reference Plane
    bpy.ops.mesh.primitive_plane_add(size=2.5 * scale, location=(location[0] - 1.5 * scale, location[1], location[2] + 1.25 * scale))
    side_ref = bpy.context.active_object
    side_ref.name = f"{object_name}_Ref_Side"
    side_ref.rotation_euler = (math.radians(90), 0, math.radians(90))
    side_ref.data.materials.append(mat)
    side_ref.hide_select = True
    if scale_rig:
        side_ref.parent = scale_rig

    return f"Created '{object_name}' scene setup: Standard View Transform, Meta-Rig, and Reference Planes at {location}"
