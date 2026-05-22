def create_object(
    scene_name: str = "Scene",
    object_name: str = "ScaleReferenceRig",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.94, 0.40, 0.55), # Stylized pink
    **kwargs,
) -> str:
    """
    Configures the scene for stylized flat-shading and creates a scale reference rig.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created armature rig.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the rig.
        material_color: (R, G, B) flat color applied to the display pedestal.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import addon_utils
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Render & Color Management Setup ===
    # Switch to EEVEE for stylized rendering
    scene.render.engine = 'BLENDER_EEVEE'

    # Set View Transform to Standard. This is critical for stylized rendering
    # as it prevents AgX/Filmic from desaturating pure color values.
    scene.view_settings.view_transform = 'Standard'

    # Disable photorealistic effects (using getattr/setattr to safely handle different Blender versions)
    if hasattr(scene, 'eevee'):
        for attr in ['use_gtao', 'use_bloom', 'use_ssr', 'use_motion_blur']:
            if hasattr(scene.eevee, attr):
                setattr(scene.eevee, attr, False)

    # === Step 2: Enable Rigify Addon ===
    addon_name = "rigging_rigify"
    is_loaded, is_enabled = addon_utils.check(addon_name)
    if not is_enabled:
        addon_utils.enable(addon_name, default_set=True)

    # === Step 3: Spawn Scale Reference (Human Meta-Rig) ===
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.armature_human_metarig_add(location=location)
    rig = bpy.context.active_object
    rig.name = object_name
    rig.scale = (scale, scale, scale)

    # Apply scale so modeling on top of it has 1.0 scale dimensions
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Make the rig display in front of geometry
    rig.show_in_front = True

    # === Step 4: Create a stylized base pedestal to demonstrate flat color ===
    pedestal_loc = (location[0], location[1], location[2] - (0.05 * scale))
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=1.5 * scale,
        depth=0.1 * scale,
        location=pedestal_loc
    )
    pedestal = bpy.context.active_object
    pedestal.name = f"{object_name}_Pedestal"

    # Create flat/unlit material
    mat = bpy.data.materials.new(name=f"{object_name}_UnlitMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    emission_node = nodes.new(type='ShaderNodeEmission')
    emission_node.inputs['Color'].default_value = (*material_color, 1.0)
    links.new(emission_node.outputs['Emission'], out_node.inputs['Surface'])

    pedestal.data.materials.append(mat)

    # Parent pedestal to rig for scene organization
    pedestal.parent = rig

    return f"Configured scene to Standard color space and spawned '{object_name}' with pedestal at {location}"
