def create_stylized_character_setup(
    scene_name: str = "Scene",
    object_name: str = "CharacterSetup",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.5),
    **kwargs,
) -> str:
    """
    Create a stylized character modeling workspace including color management fixes,
    a scale-reference Meta-Rig, and orthogonal reference boards.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created setup objects.
        location: (x, y, z) world-space base position.
        scale: Uniform scale factor for the rig and boards.
        material_color: (R, G, B) color for the placeholder reference grid.

    Returns:
        Status string.
    """
    import bpy
    import addon_utils
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    base_loc = Vector(location)

    # === Step 1: Stylized Rendering & Color Management Setup ===
    # Force View Transform to Standard to prevent AgX/Filmic from desaturating stylized colors
    scene.view_settings.view_transform = 'Standard'
    
    # Set to EEVEE and disable realistic post-processing overlays
    scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(scene, "eevee_next") else 'BLENDER_EEVEE'
    
    # Safely disable legacy EEVEE settings (Graceful fallback for Blender 4.2+)
    if hasattr(scene, "eevee"):
        if hasattr(scene.eevee, "use_gtao"): scene.eevee.use_gtao = False
        if hasattr(scene.eevee, "use_bloom"): scene.eevee.use_bloom = False
        if hasattr(scene.eevee, "use_ssr"): scene.eevee.use_ssr = False
        if hasattr(scene.eevee, "use_motion_blur"): scene.eevee.use_motion_blur = False

    created_objects = []

    # === Step 2: Enable Rigify & Add Scale Reference Meta-Rig ===
    addon_utils.enable("rigify", default_set=True)
    
    try:
        bpy.ops.object.select_all(action='DESELECT')
        # Add Human Meta-Rig as a proportion/scale blueprint
        bpy.ops.object.armature_human_metarig_add(location=base_loc)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_Scale_MetaRig"
        rig.scale = (scale, scale, scale)
        created_objects.append(rig.name)
    except Exception as e:
        print(f"Rigify rig creation failed (add-on may be missing): {e}")

    # === Step 3: Create Semi-Transparent Placeholder Reference Boards ===
    # Setup transparency material
    mat_ref = bpy.data.materials.new(name=f"{object_name}_Reference_Grid")
    mat_ref.use_nodes = True
    mat_ref.blend_method = 'BLEND' # Essential for EEVEE transparency
    
    nodes = mat_ref.node_tree.nodes
    links = mat_ref.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    
    if bsdf:
        bsdf.inputs["Alpha"].default_value = 0.4
        bsdf.inputs["Roughness"].default_value = 1.0
        
        # Add a procedural checker grid to act as a measurement reference
        checker = nodes.new(type="ShaderNodeTexChecker")
        checker.inputs["Color1"].default_value = (*material_color, 1.0) 
        checker.inputs["Color2"].default_value = (0.05, 0.05, 0.05, 1.0)
        checker.inputs["Scale"].default_value = 8.0
        links.new(checker.outputs["Color"], bsdf.inputs["Base Color"])

    # Build Front View Reference Board
    front_loc = base_loc + Vector((0.0, 1.5 * scale, 1.0 * scale))
    bpy.ops.mesh.primitive_plane_add(
        size=2.0 * scale, 
        location=front_loc, 
        rotation=(math.radians(90), 0, 0)
    )
    front_ref = bpy.context.active_object
    front_ref.name = f"{object_name}_RefBoard_Front"
    front_ref.scale = (1.0, 2.0, 1.0) # Scale to human proportion aspect ratio
    front_ref.data.materials.append(mat_ref)
    created_objects.append(front_ref.name)

    # Build Side View Reference Board
    side_loc = base_loc + Vector((1.5 * scale, 0.0, 1.0 * scale))
    bpy.ops.mesh.primitive_plane_add(
        size=2.0 * scale, 
        location=side_loc, 
        rotation=(math.radians(90), 0, math.radians(90))
    )
    side_ref = bpy.context.active_object
    side_ref.name = f"{object_name}_RefBoard_Side"
    side_ref.scale = (1.0, 2.0, 1.0)
    side_ref.data.materials.append(mat_ref)
    created_objects.append(side_ref.name)

    # Disable selection on reference boards so they don't interfere with modeling
    front_ref.hide_select = True
    side_ref.hide_select = True

    return f"Created Setup '{object_name}' (Color space set to Standard). Spawned: {', '.join(created_objects)}"
