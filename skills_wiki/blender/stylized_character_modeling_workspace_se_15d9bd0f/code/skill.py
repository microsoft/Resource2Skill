def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedWorkspace",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 0.8),
    **kwargs,
) -> str:
    """
    Create a Stylized Character Modeling Workspace.
    Configures EEVEE, sets 'Standard' color transform, spawns a scale reference rig,
    and sets up semi-transparent orthographic reference planes.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Prefix name for the created objects.
        location: (x, y, z) world-space position offset for the workspace.
        scale: Uniform scale factor (1.0 = standard human height ~1.8m).
        material_color: (R, G, B) base color for the placeholder reference planes.

    Returns:
        Status string.
    """
    import bpy
    import addon_utils
    from mathutils import Vector, Euler
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Render Engine & Color Management Configuration ===
    scene.render.engine = 'BLENDER_EEVEE'
    
    # Disable interfering post-processing for flat stylized look
    scene.eevee.use_gtao = False
    scene.eevee.use_bloom = False
    scene.eevee.use_ssr = False
    scene.eevee.use_motion_blur = False
    
    # CRITICAL: Set View Transform to Standard (prevents desaturation of stylized colors)
    scene.view_settings.view_transform = 'Standard'

    objects_created = []

    # === Step 2: Spawn Scale Reference (Rigify Human Meta-Rig) ===
    # Attempt to enable rigify, fallback to standard armature if it fails
    rig_spawned = False
    try:
        addon_utils.enable("rigify", default_set=True)
        bpy.ops.object.armature_human_metarig_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_MetaRig_ScaleRef"
        rig_spawned = True
    except Exception:
        pass

    if not rig_spawned:
        bpy.ops.object.armature_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_BasicRig_ScaleRef"
        # Scale a single bone to roughly 1.8 meters
        rig.scale = (1.8 * scale, 1.8 * scale, 1.8 * scale)
    
    # Push rig back slightly so it doesn't clip with the origin where we model
    rig.location.y += 0.5
    objects_created.append(rig.name)

    # === Step 3: Create Transparent Blueprint Reference Material ===
    mat_name = f"{object_name}_Reference_Mat"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    mat.blend_method = 'BLEND' # Enable transparency in Eevee
    mat.shadow_method = 'NONE' # References shouldn't cast shadows
    
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        # Set alpha to 0.5 for semi-transparency
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = 0.5
        bsdf.inputs["Roughness"].default_value = 1.0
        bsdf.inputs["Specular IOR Level"].default_value = 0.0

    # === Step 4: Create Orthographic Reference Planes ===
    
    # Front Reference Plane (Pushed back on Y)
    bpy.ops.mesh.primitive_plane_add(size=2.0 * scale, location=(location[0], location[1] + 1.5 * scale, location[2] + 1.0 * scale))
    front_plane = bpy.context.active_object
    front_plane.name = f"{object_name}_Ref_Front"
    front_plane.rotation_euler = Euler((math.radians(90), 0, 0), 'XYZ')
    
    # Scale up vertically to mimic a character drawing (1:2 ratio)
    front_plane.scale.y = 2.0
    
    if len(front_plane.data.materials) == 0:
        front_plane.data.materials.append(mat)
    objects_created.append(front_plane.name)

    # Side Reference Plane (Pushed back on X)
    bpy.ops.mesh.primitive_plane_add(size=2.0 * scale, location=(location[0] - 1.5 * scale, location[1], location[2] + 1.0 * scale))
    side_plane = bpy.context.active_object
    side_plane.name = f"{object_name}_Ref_Side"
    side_plane.rotation_euler = Euler((math.radians(90), 0, math.radians(90)), 'XYZ')
    
    side_plane.scale.y = 2.0
    
    if len(side_plane.data.materials) == 0:
        side_plane.data.materials.append(mat)
    objects_created.append(side_plane.name)

    # Prevent references from being accidentally selected during modeling
    front_plane.hide_select = True
    side_plane.hide_select = True

    return f"Created Stylized Workspace '{object_name}' (Configured 'Standard' view transform, added scale rig and 2 reference planes)."
