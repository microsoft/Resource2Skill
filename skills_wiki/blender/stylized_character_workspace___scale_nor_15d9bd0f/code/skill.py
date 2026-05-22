def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedWorkspace",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a Stylized Character Workspace in the active Blender scene.
    Adjusts Color Management to 'Standard', adds a human scale reference rig, 
    and aligns transparent Image Empties for front and side orthographic modeling.

    Args:
        scene_name: Name of the target scene.
        object_name: Prefix name for the created setup objects.
        location: (x, y, z) world-space position for the setup origin.
        scale: Uniform scale factor.
        material_color: Unused in this specific setup, kept for API consistency.

    Returns:
        Status string.
    """
    import bpy
    import addon_utils
    from math import radians

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Stylized Color Management & Render Settings ===
    # Set to Standard to prevent Filmic/AgX from washing out flat stylized colors
    scene.view_settings.view_transform = 'Standard'
    
    # Try to set engine to EEVEE for real-time stylized rendering
    try:
        scene.render.engine = 'BLENDER_EEVEE_NEXT' # Blender 4.2+
    except TypeError:
        scene.render.engine = 'BLENDER_EEVEE' # Older versions

    # === Step 2: Add Scale Reference Anchor ===
    scale_ref_obj = None
    original_active = bpy.context.view_layer.objects.active
    
    try:
        # Enable Rigify and add the meta-rig
        addon_utils.enable("rigify")
        bpy.ops.object.armature_human_metarig_add(location=location)
        scale_ref_obj = bpy.context.active_object
        scale_ref_obj.name = object_name + "_ScaleRig"
        scale_ref_obj.scale = (scale, scale, scale)
        bpy.context.view_layer.objects.active = original_active
    except Exception as e:
        # Fallback if Rigify fails due to context issues: Create a 1.8m bounding box
        mesh = bpy.data.meshes.new(object_name + "_ProxyMesh")
        scale_ref_obj = bpy.data.objects.new(object_name + "_ScaleProxy", mesh)
        scene.collection.objects.link(scale_ref_obj)
        
        import bmesh
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bm.to_mesh(mesh)
        bm.free()
        
        # Scale to standard human height (1.8m)
        scale_ref_obj.scale = (0.5 * scale, 0.5 * scale, 1.8 * scale)
        scale_ref_obj.location = (location[0], location[1], location[2] + (0.9 * scale))
        scale_ref_obj.display_type = 'WIRE'

    # === Step 3: Create Transparent Orthographic Reference Empties ===
    # Front View Empty (Facing -Y)
    front_ref = bpy.data.objects.new(object_name + "_FrontRef", None)
    front_ref.empty_display_type = 'IMAGE'
    front_ref.empty_display_size = 2.0 * scale
    # Push back on Y axis so it doesn't clip through the model
    front_ref.location = (location[0], location[1] + (1.5 * scale), location[2] + (1.0 * scale))
    front_ref.rotation_euler = (radians(90), 0, 0)
    front_ref.color = (1.0, 1.0, 1.0, 0.5)  # 50% Transparency
    
    # Side View Empty (Facing +X)
    side_ref = bpy.data.objects.new(object_name + "_SideRef", None)
    side_ref.empty_display_type = 'IMAGE'
    side_ref.empty_display_size = 2.0 * scale
    # Push left on X axis
    side_ref.location = (location[0] - (1.5 * scale), location[1], location[2] + (1.0 * scale))
    side_ref.rotation_euler = (radians(90), 0, radians(-90))
    side_ref.color = (1.0, 1.0, 1.0, 0.5) # 50% Transparency

    # === Step 4: Organize into a Collection ===
    setup_coll = bpy.data.collections.new(object_name + "_SetupGroup")
    scene.collection.children.link(setup_coll)
    
    for obj in [front_ref, side_ref]:
        setup_coll.objects.link(obj)
        
    if scale_ref_obj and scale_ref_obj.name in scene.collection.objects:
        scene.collection.objects.unlink(scale_ref_obj)
        setup_coll.objects.link(scale_ref_obj)

    return f"Created '{object_name}' scene setup. Note: Scene View Transform changed to 'Standard' for accurate stylized colors."
