def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedCharacter_Studio",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.5, 0.8),
    **kwargs,
) -> str:
    """
    Create a Stylized Character Modeling Studio setup including NPR color config,
    a Rigify Meta-Rig scale reference, and aligned semi-transparent reference planes.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated setup objects.
        location: (x, y, z) world-space position for the setup center.
        scale: Uniform scale factor for the rig and planes.
        material_color: (R, G, B) tint for the semi-transparent reference proxy planes.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    import addon_utils
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: NPR Engine and Color Management Configuration ===
    scene.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderEngine.bl_rna_get_subclass_py('RenderEngine').__subclasses__()] else 'BLENDER_EEVEE'
    
    # Crucial for Stylized/Anime colors: Change from AgX/Filmic to Standard
    scene.view_settings.view_transform = 'Standard'
    
    # Attempt to disable photorealistic Eevee post-processing (API varies slightly by version)
    try:
        scene.eevee.use_gtao = False
        scene.eevee.use_bloom = False
        scene.eevee.use_ssr = False
    except AttributeError:
        pass # Silently pass if using a newer/older EEVEE API version

    # === Step 2: Spawn Scale Reference (Rigify Human Meta-Rig) ===
    # Attempt to enable Rigify and add the rig
    rig = None
    try:
        addon_utils.enable("rigify", default_set=True)
        # Create a temporary override to safely use bpy.ops
        with bpy.context.temp_override(scene=scene):
            bpy.ops.object.armature_human_metarig_add(location=location)
            rig = bpy.context.active_object
            rig.name = f"{object_name}_ScaleRig"
            rig.scale = (scale, scale, scale)
    except Exception as e:
        print(f"Rigify setup failed, creating generic bounding box: {e}")
        # Fallback if Rigify is missing or fails
        bpy.ops.mesh.primitive_cube_add(size=2, location=(location[0], location[1], location[2] + 1))
        rig = bpy.context.active_object
        rig.name = f"{object_name}_ScaleFallback"
        rig.scale = (scale * 0.5, scale * 0.5, scale * 1.0) # Approx human proportion
        rig.display_type = 'WIRE'

    # === Step 3: Create Semi-Transparent Reference Material ===
    mat_name = f"{object_name}_RefProxyMat"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        mat.blend_method = 'BLEND'  # Enable Alpha Blending in EEVEE
        mat.shadow_method = 'NONE'  # Prevents planes from casting shadows
        
        nodes = mat.node_tree.nodes
        nodes.clear()
        links = mat.node_tree.links
        
        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (400, 0)
        
        emission = nodes.new(type='ShaderNodeEmission')
        emission.inputs['Color'].default_value = (*material_color, 1.0)
        emission.location = (0, 100)
        
        transparent = nodes.new(type='ShaderNodeBsdfTransparent')
        transparent.location = (0, -100)
        
        mix = nodes.new(type='ShaderNodeMixShader')
        mix.inputs['Fac'].default_value = 0.5 # 50% opacity
        mix.location = (200, 0)
        
        links.new(emission.outputs[0], mix.inputs[2])
        links.new(transparent.outputs[0], mix.inputs[1])
        links.new(mix.outputs[0], output.inputs[0])

    # === Step 4: Spawn and Align Reference Planes ===
    plane_size = 2.5 * scale
    
    # Front Plane (Placed slightly behind the center on Y axis)
    front_loc = (location[0], location[1] + (1.0 * scale), location[2] + (1.0 * scale))
    bpy.ops.mesh.primitive_plane_add(size=plane_size, location=front_loc)
    front_plane = bpy.context.active_object
    front_plane.name = f"{object_name}_RefPlane_Front"
    front_plane.rotation_euler = (math.radians(90), 0, 0)
    front_plane.data.materials.append(mat)
    
    # Side Plane (Placed slightly behind the center on X axis)
    side_loc = (location[0] - (1.0 * scale), location[1], location[2] + (1.0 * scale))
    bpy.ops.mesh.primitive_plane_add(size=plane_size, location=side_loc)
    side_plane = bpy.context.active_object
    side_plane.name = f"{object_name}_RefPlane_Side"
    side_plane.rotation_euler = (math.radians(90), 0, math.radians(90))
    side_plane.data.materials.append(mat)

    # Optional: Make planes unselectable so they don't interfere with modeling
    front_plane.hide_select = True
    side_plane.hide_select = True

    return f"Created Studio Setup '{object_name}' with NPR config, Scale Rig, and Reference Planes at {location}"
