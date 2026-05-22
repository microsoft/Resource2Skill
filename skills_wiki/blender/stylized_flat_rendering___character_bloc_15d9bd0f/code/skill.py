def create_stylized_character_env(
    scene_name: str = "Scene",
    object_name: str = "StylizedBlockout",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.15, 0.2),  # Main Jacket Color
    **kwargs,
) -> str:
    """
    Creates a Color-Managed Stylized Workspace and a proportional 
    low-poly character blockout.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created proxy objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) color for the primary clothing.
        **kwargs: Additional overrides.
        
    Returns:
        Status string.
    """
    import bpy
    import addon_utils
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Stylized Render Settings ===
    # Set engine to EEVEE
    scene.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in dir(bpy.types.RenderSettings) else 'BLENDER_EEVEE'
    
    # CRITICAL: Bypass photorealistic tone mapping for exact 2D color matching
    scene.view_settings.view_transform = 'Standard'
    
    # Disable realism post-processing
    if hasattr(scene.eevee, 'use_ssr'): scene.eevee.use_ssr = False
    if hasattr(scene.eevee, 'use_gtao'): scene.eevee.use_gtao = False
    if hasattr(scene.eevee, 'use_bloom'): scene.eevee.use_bloom = False

    # === Step 2: Establish Scale Reference (Rigify Meta-Rig) ===
    addon_utils.enable("rigify", default_set=True)
    try:
        bpy.ops.object.armature_human_metarig_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_MetaRig_Ref"
        rig.scale = (scale, scale, scale)
        rig.display_type = 'WIRE'
        rig.show_in_front = True
    except Exception as e:
        print(f"Notice: Could not spawn Meta-Rig ({e}). Proceeding with blockout.")
        
    # === Step 3: Material Generation ===
    def create_flat_mat(name, color):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes.clear()
        
        out = nodes.new(type="ShaderNodeOutputMaterial")
        bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
        
        # Ensure flat shading profile
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = 1.0
        
        # Handle Blender 4.0+ vs older API for Specular
        if 'Specular IOR Level' in bsdf.inputs:
            bsdf.inputs['Specular IOR Level'].default_value = 0.0
        elif 'Specular' in bsdf.inputs:
            bsdf.inputs['Specular'].default_value = 0.0
            
        mat.node_tree.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
        return mat

    # Define the stylized palette from the reference
    mat_skin = create_flat_mat(f"{object_name}_Skin", (0.35, 0.75, 0.85, 1.0))
    mat_hair = create_flat_mat(f"{object_name}_Hair", (0.85, 0.35, 0.45, 1.0))
    mat_jacket = create_flat_mat(f"{object_name}_Jacket", (*material_color, 1.0))
    mat_shorts = create_flat_mat(f"{object_name}_Shorts", (0.2, 0.4, 0.7, 1.0))

    # === Step 4: Construct Proportional Blockout ===
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    parent_obj = bpy.context.active_object
    parent_obj.name = object_name
    parent_obj.scale = (scale, scale, scale)

    def add_proxy_block(name, dim, loc_offset, mat):
        bpy.ops.mesh.primitive_cube_add(size=1)
        obj = bpy.context.active_object
        obj.name = f"{object_name}_{name}"
        obj.scale = dim
        obj.location = Vector(location) + (Vector(loc_offset) * scale)
        obj.parent = parent_obj
        obj.data.materials.append(mat)
        return obj

    # Torso Hierarchy
    add_proxy_block("Torso", (0.35, 0.2, 0.4), (0, 0, 1.1), mat_jacket)
    add_proxy_block("Pelvis", (0.32, 0.18, 0.15), (0, 0, 0.8), mat_shorts)
    add_proxy_block("Head", (0.25, 0.25, 0.25), (0, 0, 1.5), mat_skin)
    add_proxy_block("Hair_Volume", (0.3, 0.3, 0.15), (0, -0.05, 1.6), mat_hair)
    
    # Limbs
    add_proxy_block("Leg_L", (0.12, 0.12, 0.4), (0.1, 0, 0.4), mat_skin)
    add_proxy_block("Leg_R", (0.12, 0.12, 0.4), (-0.1, 0, 0.4), mat_skin)
    add_proxy_block("Arm_L", (0.35, 0.1, 0.1), (0.4, 0, 1.2), mat_jacket)
    add_proxy_block("Arm_R", (0.35, 0.1, 0.1), (-0.4, 0, 1.2), mat_jacket)

    # Deselect all to finish cleanly
    bpy.ops.object.select_all(action='DESELECT')
    parent_obj.select_set(True)
    bpy.context.view_layer.objects.active = parent_obj

    return f"Created Stylized Environment & Blockout '{object_name}' at {location}. View Transform set to 'Standard'."
