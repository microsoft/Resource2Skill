def create_object(
    scene_name: str = "Scene",
    object_name: str = "CharacterSetup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.6, 0.9),  # Cyan blueprint color
    **kwargs,
) -> str:
    """
    Create Character Modeling Environment & Reference Setup in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created reference objects.
        location: (x, y, z) world-space origin for the setup.
        scale: Uniform scale factor (1.0 = ~2 meter tall character).
        material_color: (R, G, B) color of the blueprint grid lines.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import addon_utils
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Configure Scene for Flat Reference Modeling ===
    scene.render.engine = 'BLENDER_EEVEE'
    scene.view_settings.view_transform = 'Standard'
    
    # Disable distracting EEVEE post-processing effects
    if hasattr(scene, 'eevee'):
        if hasattr(scene.eevee, 'use_gtao'): scene.eevee.use_gtao = False
        if hasattr(scene.eevee, 'use_bloom'): scene.eevee.use_bloom = False
        if hasattr(scene.eevee, 'use_ssr'): scene.eevee.use_ssr = False
        if hasattr(scene.eevee, 'use_motion_blur'): scene.eevee.use_motion_blur = False

    created_objects = []

    # === Step 2: Establish Scale Guide (Human Metarig) ===
    rig_created = False
    try:
        addon_utils.enable("rigify")
        # Attempt to spawn metarig (can fail depending on context execution environment)
        bpy.ops.object.armature_human_metarig_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_ScaleRig"
        rig.scale = (scale, scale, scale)
        created_objects.append(rig.name)
        rig_created = True
    except Exception:
        pass
        
    # Fallback to a programmatic scale dummy if Rigify context fails
    if not rig_created:
        mesh = bpy.data.meshes.new(f"{object_name}_ScaleMesh")
        rig = bpy.data.objects.new(f"{object_name}_ScaleDummy", mesh)
        scene.collection.objects.link(rig)
        
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=2.0 * scale)
        bm.to_mesh(mesh)
        bm.free()
        
        # Adjust to human bounding box (narrower on X/Y, standing on origin)
        for v in mesh.vertices:
            v.co.z += 1.0 * scale
            v.co.x *= 0.3
            v.co.y *= 0.2
            
        rig.location = location
        rig.display_type = 'WIRE'
        rig.color = (0.2, 0.8, 0.2, 1.0)
        created_objects.append(rig.name)

    # === Step 3: Build Procedural Blueprint Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_BlueprintMat")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    node_out = nodes.new('ShaderNodeOutputMaterial')
    node_out.location = (400, 0)
    
    node_transp = nodes.new('ShaderNodeBsdfTransparent')
    node_transp.location = (200, -100)
    
    node_emit = nodes.new('ShaderNodeEmission')
    node_emit.location = (200, 100)
    node_emit.inputs['Color'].default_value = (*material_color, 1.0)
    node_emit.inputs['Strength'].default_value = 1.5
    
    node_mix = nodes.new('ShaderNodeMixShader')
    node_mix.location = (300, 0)
    
    # Procedural Grid using Brick Texture
    node_grid = nodes.new('ShaderNodeTexBrick')
    node_grid.location = (0, 0)
    node_grid.inputs['Color1'].default_value = (0, 0, 0, 1) # Pure black (Transparent)
    node_grid.inputs['Color2'].default_value = (0, 0, 0, 1) # Pure black (Transparent)
    node_grid.inputs['Mortar'].default_value = (1, 1, 1, 1) # Pure white (Emission)
    node_grid.inputs['Scale'].default_value = 15.0
    node_grid.inputs['Mortar Size'].default_value = 0.015
    
    links.new(node_grid.outputs['Color'], node_mix.inputs['Fac'])
    links.new(node_transp.outputs[0], node_mix.inputs[1])
    links.new(node_emit.outputs[0], node_mix.inputs[2])
    links.new(node_mix.outputs[0], node_out.inputs['Surface'])

    # === Step 4: Construct Reference Planes ===
    def create_ref_plane(name_suffix, loc_offset, rot_euler):
        mesh_ref = bpy.data.meshes.new(f"{object_name}_{name_suffix}_Mesh")
        ref_obj = bpy.data.objects.new(f"{object_name}_{name_suffix}", mesh_ref)
        scene.collection.objects.link(ref_obj)
        
        bm_ref = bmesh.new()
        bmesh.ops.create_grid(bm_ref, x_segments=1, y_segments=1, size=scale * 1.5)
        # Stretch to portrait aspect ratio (taller along local Y before rotation)
        for v in bm_ref.verts:
            v.co.y *= 1.4
        bm_ref.to_mesh(mesh_ref)
        bm_ref.free()
        
        ref_obj.location = (
            location[0] + loc_offset[0], 
            location[1] + loc_offset[1], 
            location[2] + loc_offset[2]
        )
        ref_obj.rotation_euler = rot_euler
        ref_obj.data.materials.append(mat)
        
        # Make unselectable to prevent accidental clicks during modeling
        ref_obj.hide_select = True
        return ref_obj.name

    # Front Reference (Placed BEHIND the origin on the +Y axis)
    front_name = create_ref_plane(
        "FrontRef", 
        (0.0, scale * 1.5, scale * 1.05), 
        (math.radians(90), 0, 0)
    )
    created_objects.append(front_name)

    # Side Reference (Placed BEHIND the origin on the -X axis)
    side_name = create_ref_plane(
        "SideRef", 
        (-scale * 1.5, 0.0, scale * 1.05), 
        (math.radians(90), 0, math.radians(90))
    )
    created_objects.append(side_name)

    return f"Created Setup '{object_name}' with {len(created_objects)} objects: {', '.join(created_objects)}"
