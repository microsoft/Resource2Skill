def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedSetup",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.8, 0.8),
    **kwargs,
) -> str:
    """
    Creates a stylized character modeling environment. Configures EEVEE for 1:1 color mapping,
    adds a Rigify Human Meta-Rig for proportions, and aligns semi-transparent reference placeholders.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated setup collection and objects.
        location: World-space position for the setup.
        scale: Overall scale factor.
        material_color: Placeholder color for the reference planes.

    Returns:
        Status string describing the setup.
    """
    import bpy
    import math
    import addon_utils
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Stylized Engine & Color Management Setup ===
    scene.render.engine = 'BLENDER_EEVEE'
    
    # Disable realism-focused post-processing (Handle API changes across Blender versions)
    if hasattr(scene, "eevee"):
        if hasattr(scene.eevee, "use_gtao"):
            scene.eevee.use_gtao = False
        if hasattr(scene.eevee, "use_bloom"):
            scene.eevee.use_bloom = False
        if hasattr(scene.eevee, "use_ssr"):
            scene.eevee.use_ssr = False
        if hasattr(scene.eevee, "use_motion_blur"):
            scene.eevee.use_motion_blur = False

    # CRITICAL: Force 1:1 Color Mapping (AgX -> Standard)
    scene.view_settings.view_transform = 'Standard'

    # === Step 2: Collection Management ===
    setup_col = bpy.data.collections.new(f"{object_name}_Collection")
    scene.collection.children.link(setup_col)

    # === Step 3: Anatomical Scaffold (Rigify Meta-Rig) ===
    addon_utils.enable("rigging_rigify", default_set=True)
    
    rig = None
    try:
        # Save current mode and ensure we are in Object mode to use the operator
        original_mode = bpy.context.mode
        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            
        bpy.ops.object.armature_human_metarig_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_MetaRig"
        rig.scale = (scale, scale, scale)
        
        # Move rig to our collection and remove from default scene collection
        setup_col.objects.link(rig)
        if rig.name in scene.collection.objects:
            scene.collection.objects.unlink(rig)
            
    except Exception as e:
        # Fallback if Rigify fails to load: create a basic simple armature
        arm_data = bpy.data.armatures.new(f"{object_name}_FallbackArmData")
        rig = bpy.data.objects.new(f"{object_name}_MetaRig", arm_data)
        setup_col.objects.link(rig)
        rig.location = location
        rig.scale = (scale, scale, scale)

    # === Step 4: Reference Image Placeholders ===
    # Create semi-transparent material
    ref_mat = bpy.data.materials.new(name=f"{object_name}_RefMaterial")
    ref_mat.use_nodes = True
    ref_mat.blend_method = 'BLEND' # Enable transparency in EEVEE
    ref_mat.shadow_method = 'NONE'
    
    bsdf = ref_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Alpha"].default_value = 0.5 # 50% Opacity as instructed in video
        bsdf.inputs["Roughness"].default_value = 1.0
        # For Blender 4.0+
        if "Specular IOR Level" in bsdf.inputs:
            bsdf.inputs["Specular IOR Level"].default_value = 0.0

    # The default Meta-Rig is ~2m tall. We create planes dimensioned 2x2.
    # Center is at Z=1 so the bottom edge rests exactly on Z=0 (the ground plane).
    
    # Front Reference Placeholder (Moved back on Y axis)
    bpy.ops.mesh.primitive_plane_add(size=2.0 * scale, location=(0, 0, 0))
    front_ref = bpy.context.active_object
    front_ref.name = f"{object_name}_Ref_Front"
    # Rotate to stand upright facing Front Orthographic (-Y)
    front_ref.rotation_euler = (math.radians(90), 0, 0)
    # Move up so feet touch ground, push back on Y so it doesn't intersect model
    front_ref.location = Vector(location) + Vector((0.0, 1.5 * scale, 1.0 * scale))
    front_ref.data.materials.append(ref_mat)
    
    setup_col.objects.link(front_ref)
    scene.collection.objects.unlink(front_ref)

    # Side Reference Placeholder (Moved back on X axis)
    bpy.ops.mesh.primitive_plane_add(size=2.0 * scale, location=(0, 0, 0))
    side_ref = bpy.context.active_object
    side_ref.name = f"{object_name}_Ref_Side"
    # Rotate to stand upright facing Right Orthographic (-X)
    side_ref.rotation_euler = (math.radians(90), 0, math.radians(90))
    # Move up so feet touch ground, push back on X so it doesn't intersect model
    side_ref.location = Vector(location) + Vector((-1.5 * scale, 0.0, 1.0 * scale))
    side_ref.data.materials.append(ref_mat)
    
    setup_col.objects.link(side_ref)
    scene.collection.objects.unlink(side_ref)
    
    # Lock the references so they aren't accidentally selected while modeling
    front_ref.hide_select = True
    side_ref.hide_select = True

    return f"Created Stylized Environment Setup '{object_name}' (View Transform: Standard). Generated Meta-Rig and 2 locked reference placeholders at {location}."
