def create_object(
    scene_name: str = "Scene",
    object_name: str = "CharBlueprint",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 1.0),
    **kwargs,
) -> str:
    """
    Create Character Modeling Blueprint Setup in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created reference objects.
        location: (x, y, z) world-space position for the setup.
        scale: Uniform scale factor (1.0 = standard 2-meter human).
        material_color: (R, G, B) tint for the reference blueprint planes.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import addon_utils
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Render & Color Management Settings ===
    # Set to EEVEE (Handle both 4.2+ EEVEE_NEXT and older EEVEE)
    if 'BLENDER_EEVEE_NEXT' in [e.idname for e in bpy.types.RenderEngine.__subclasses__()]:
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
    else:
        scene.render.engine = 'BLENDER_EEVEE'
        
    # Standard view transform is critical for stylized/low-poly color accuracy
    scene.view_settings.view_transform = 'Standard'

    # Disable interfering post-processing effects (if using pre-4.2 Eevee settings structure)
    try:
        scene.eevee.use_gtao = False
        scene.eevee.use_bloom = False
        scene.eevee.use_ssr = False
        scene.eevee.use_motion_blur = False
    except AttributeError:
        pass # Handle graceful fallback for Blender 4.2+ changed attributes

    # === Step 2: Enable Rigify and Add Meta-Rig ===
    if not addon_utils.check("rigify")[1]:
        addon_utils.enable("rigify")

    # Add Human Meta-rig
    bpy.ops.object.armature_human_metarig_add(location=location)
    rig = bpy.context.active_object
    rig.name = f"{object_name}_MetaRig"
    rig.scale = (scale, scale, scale)
    # Move rig's origin exactly to the floor line if it isn't already
    rig.location.z += (rig.dimensions.z / 2) * scale if rig.location.z < 0 else 0

    # === Step 3: Create Semi-Transparent Blueprint Material ===
    mat_name = f"{object_name}_BlueprintMat"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    mat.blend_method = 'BLEND'  # Enable Alpha Blending for Eevee
    mat.shadow_method = 'NONE'  # References shouldn't cast shadows

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Alpha"].default_value = 0.35  # Semi-transparent like the video
        bsdf.inputs["Roughness"].default_value = 1.0
        # If emission is needed to make it act unlit:
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (*material_color, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 0.5

    # === Step 4: Create Reference Planes ===
    # Front View Plane (Behind the character on the Y axis)
    front_offset = Vector((0, 1.5 * scale, 1.0 * scale))
    bpy.ops.mesh.primitive_plane_add(size=2.2, location=Vector(location) + front_offset)
    front_plane = bpy.context.active_object
    front_plane.name = f"{object_name}_FrontRef"
    front_plane.rotation_euler = (math.radians(90), 0, 0)
    front_plane.scale = (scale, scale, scale)
    if len(front_plane.data.materials) == 0:
        front_plane.data.materials.append(mat)
    
    # Side View Plane (To the side of the character on the X axis)
    side_offset = Vector((1.5 * scale, 0, 1.0 * scale))
    bpy.ops.mesh.primitive_plane_add(size=2.2, location=Vector(location) + side_offset)
    side_plane = bpy.context.active_object
    side_plane.name = f"{object_name}_SideRef"
    side_plane.rotation_euler = (math.radians(90), 0, math.radians(90))
    side_plane.scale = (scale, scale, scale)
    if len(side_plane.data.materials) == 0:
        side_plane.data.materials.append(mat)

    # Disable selection for reference planes so they don't get in the way of modeling
    front_plane.hide_select = True
    side_plane.hide_select = True

    return f"Created Character Reference Setup '{object_name}' with Meta-Rig and Orthogonal Planes at {location}"
