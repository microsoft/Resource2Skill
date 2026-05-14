def create_object(
    scene_name: str = "Scene",
    object_name: str = "Stylized_Setup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (1.0, 1.0, 1.0),
    **kwargs,
) -> str:
    """
    Create Stylized Character Modeling Scene Prep in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created reference objects.
        location: (x, y, z) world-space position for the rig.
        scale: Uniform scale factor (1.0 = standard human height).
        material_color: Ignored here (uses a generated grid texture).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector
    import addon_utils

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Stylized Render Engine Configuration ===
    # For stylized low-poly, we want raw colors without photorealistic tonemapping
    scene.view_settings.view_transform = 'Standard'
    
    # Try to set EEVEE as it is preferred for stylized rendering
    if 'BLENDER_EEVEE_NEXT' in [e.idname for e in bpy.types.RenderEngine.__subclasses__()]:
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
    else:
        try:
            scene.render.engine = 'BLENDER_EEVEE'
        except Exception:
            pass

    # Disable effects that ruin flat stylized looks (handle attribute differences safely)
    for attr in ['use_gtao', 'use_bloom', 'use_ssr', 'use_motion_blur']:
        if hasattr(scene.eevee, attr):
            setattr(scene.eevee, attr, False)

    # === Step 2: Scale Reference Rig (Rigify) ===
    # Enable the built-in Rigify addon
    addon_utils.enable("rigging_rigify")
    
    rig_obj = None
    try:
        # Spawn the Human Meta-Rig as a human-scale reference
        bpy.ops.object.armature_human_metarig_add(location=location)
        rig_obj = bpy.context.active_object
        rig_obj.name = f"{object_name}_ScaleRig"
        rig_obj.scale = (scale, scale, scale)
    except Exception as e:
        # Fallback to a basic primitive if the addon fails to load
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.3*scale, 
            depth=1.8*scale, 
            location=(location[0], location[1], location[2]+0.9*scale)
        )
        rig_obj = bpy.context.active_object
        rig_obj.name = f"{object_name}_ScaleFallback"

    # === Step 3: Transparent Reference Planes Setup ===
    # Generate a placeholder grid image to represent character concept art
    img_width, img_height = 1024, 1024
    placeholder_img = bpy.data.images.new(name=f"{object_name}_RefImg", width=img_width, height=img_height)
    placeholder_img.generated_type = 'COLOR_GRID'
    
    # Material for References with 50% opacity
    mat = bpy.data.materials.new(name=f"{object_name}_RefMat")
    mat.use_nodes = True
    
    # Handle blend modes for older EEVEE versions (safely ignored in 4.2+)
    try:
        mat.blend_method = 'BLEND' 
        mat.shadow_method = 'NONE' 
    except AttributeError:
        pass
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Setup unlit emission shader for the reference image
    emit = nodes.new(type='ShaderNodeEmission')
    tex = nodes.new(type='ShaderNodeTexImage')
    tex.image = placeholder_img
    
    transparent = nodes.new(type='ShaderNodeBsdfTransparent')
    mix = nodes.new(type='ShaderNodeMixShader')
    mix.inputs['Fac'].default_value = 0.5 # 50% opacity as requested in tutorial
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    
    links.new(tex.outputs['Color'], emit.inputs['Color'])
    links.new(transparent.outputs['BSDF'], mix.inputs[1])
    links.new(emit.outputs['Emission'], mix.inputs[2])
    links.new(mix.outputs['Shader'], output.inputs['Surface'])

    # Spawn Front Reference Plane (pushed back on Y)
    bpy.ops.mesh.primitive_plane_add(
        size=3*scale, 
        location=(location[0], location[1]+1.5*scale, location[2]+1.5*scale), 
        rotation=(math.radians(90), 0, 0)
    )
    front_plane = bpy.context.active_object
    front_plane.name = f"{object_name}_FrontRef"
    front_plane.data.materials.append(mat)
    
    # Spawn Side Reference Plane (pushed back on X)
    bpy.ops.mesh.primitive_plane_add(
        size=3*scale, 
        location=(location[0]-1.5*scale, location[1], location[2]+1.5*scale), 
        rotation=(math.radians(90), 0, math.radians(-90))
    )
    side_plane = bpy.context.active_object
    side_plane.name = f"{object_name}_SideRef"
    side_plane.data.materials.append(mat)

    return f"Created '{object_name}' scene configuration: Standard View Transform, scale rig, and 2 transparent reference planes at {location}."
