def create_object(
    scene_name: str = "Scene",
    object_name: str = "CharacterSetup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.8, 0.8),
    **kwargs,
) -> str:
    """
    Create Stylized Workspace & Orthographic Reference Setup in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the setup collection.
        location: (x, y, z) world-space position for the setup origin.
        scale: Uniform scale factor for the human rig and reference planes.
        material_color: Base color for the transparent reference boards.
        **kwargs: Additional overrides (e.g., character_height).

    Returns:
        Status string.
    """
    import bpy
    import addon_utils
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    character_height = kwargs.get("character_height", 1.8) # Average human height

    # === Step 1: Stylized Scene Settings ===
    # Set Render Engine to EEVEE
    scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types.Scene, 'eevee') else 'BLENDER_EEVEE'
    
    # CRITICAL: Set Color Management to Standard for accurate 1:1 color picking
    scene.display_settings.display_device = 'sRGB'
    scene.view_settings.view_transform = 'Standard'
    
    # Disable photorealistic post-processing for a clean viewport
    if hasattr(scene, 'eevee'):
        try: scene.eevee.use_bloom = False
        except AttributeError: pass # Varies by Blender version
        try: scene.eevee.use_ssr = False
        except AttributeError: pass
        try: scene.eevee.use_gtao = False
        except AttributeError: pass
        try: scene.eevee.use_motion_blur = False
        except AttributeError: pass

    # === Step 2: Ensure Rigify is Enabled ===
    # Ships with Blender by default, just needs to be turned on
    if "rigify" not in [mod.__name__ for mod in addon_utils.modules() if addon_utils.check(mod.__name__)[0]]:
        addon_utils.enable("rigify")

    # === Step 3: Create Setup Collection ===
    setup_col = bpy.data.collections.new(object_name)
    scene.collection.children.link(setup_col)

    # === Step 4: Spawn Meta-Rig Anchor ===
    # Using ops here because rig generation is heavily tied to internal C-ops
    bpy.ops.object.armature_human_metarig_add(location=location)
    metarig = bpy.context.active_object
    metarig.name = f"{object_name}_ScaleAnchor"
    
    # Scale rig to match specified character height (Default rig is ~2m tall)
    rig_scale = (character_height / 2.0) * scale
    metarig.scale = (rig_scale, rig_scale, rig_scale)
    
    # Link to our collection, remove from default
    for col in metarig.users_collection:
        col.objects.unlink(metarig)
    setup_col.objects.link(metarig)

    # === Step 5: Build Transparent Reference Material ===
    ref_mat = bpy.data.materials.new(name=f"{object_name}_RefMaterial")
    ref_mat.use_nodes = True
    ref_mat.blend_method = 'BLEND' # Enable transparency in EEVEE
    bsdf = ref_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Alpha'].default_value = 0.3 # Make see-through
        bsdf.inputs['Roughness'].default_value = 1.0

    # === Step 6: Spawn Reference Boards ===
    base_loc = Vector(location)
    plane_size = character_height * scale

    # Front View Reference (Placed behind the model on the Y axis)
    bpy.ops.mesh.primitive_plane_add(size=plane_size)
    front_ref = bpy.context.active_object
    front_ref.name = f"{object_name}_FrontView"
    front_ref.rotation_euler = (math.radians(90), 0, 0)
    front_ref.location = base_loc + Vector((0, 1.5 * scale, plane_size / 2.0))
    front_ref.data.materials.append(ref_mat)
    
    for col in front_ref.users_collection:
        col.objects.unlink(front_ref)
    setup_col.objects.link(front_ref)

    # Side View Reference (Placed to the left of the model on the X axis)
    bpy.ops.mesh.primitive_plane_add(size=plane_size)
    side_ref = bpy.context.active_object
    side_ref.name = f"{object_name}_SideView"
    side_ref.rotation_euler = (math.radians(90), 0, math.radians(90))
    side_ref.location = base_loc + Vector((-1.5 * scale, 0, plane_size / 2.0))
    side_ref.data.materials.append(ref_mat)
    
    for col in side_ref.users_collection:
        col.objects.unlink(side_ref)
    setup_col.objects.link(side_ref)

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created Stylized Reference Setup '{object_name}' with 3 objects (Rig, Front Ref, Side Ref) at {location}"
