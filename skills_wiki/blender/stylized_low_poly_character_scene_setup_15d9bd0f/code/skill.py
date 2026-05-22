def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedCharacterSetup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Creates an optimized scene setup for stylized/low-poly character modeling,
    including color management fixes, scale reference, and orthographic image boards.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated setup collection.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the human rig and reference planes.
        material_color: Unused (Placeholder reference planes use a checkerboard).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import addon_utils
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Render Engine & Color Management Fixes ===
    # Stylized shading looks best in EEVEE
    if 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderEngine.__subclasses__()]:
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
    else:
        scene.render.engine = 'BLENDER_EEVEE'
        
    # Disable photorealistic features that interfere with flat colors
    try:
        scene.eevee.use_gtao = False
        scene.eevee.use_bloom = False
        scene.eevee.use_ssr = False
        scene.eevee.use_motion_blur = False
    except AttributeError:
        pass # Handle version differences gracefully
        
    # CRITICAL: Prevent Blender from washing out hand-painted colors
    scene.view_settings.view_transform = 'Standard'

    # === Step 2: Establish Human Scale ===
    addon_utils.enable("rigify")
    
    try:
        # Spawn Human Meta-rig
        bpy.ops.object.armature_human_metarig_add(location=location)
        rig = bpy.context.active_object
    except AttributeError:
        # Fallback if Rigify fails
        bpy.ops.object.armature_add(location=location)
        rig = bpy.context.active_object
        
    rig.name = f"{object_name}_Scale_Rig"
    rig.scale = (scale, scale, scale)
    rig.show_in_front = True # Always draw rig on top

    # === Step 3: Create Reference Image Boards ===
    # Front View Reference (Placed behind character on Y axis)
    bpy.ops.mesh.primitive_plane_add(
        size=2.5 * scale, 
        location=(location[0], location[1] + 1.0 * scale, location[2] + 1.25 * scale), 
        rotation=(math.radians(90), 0, 0)
    )
    front_ref = bpy.context.active_object
    front_ref.name = f"{object_name}_Ref_Front"
    
    # Side View Reference (Placed behind character on X axis for Right Ortho view)
    bpy.ops.mesh.primitive_plane_add(
        size=2.5 * scale, 
        location=(location[0] - 1.0 * scale, location[1], location[2] + 1.25 * scale), 
        rotation=(math.radians(90), 0, math.radians(-90))
    )
    side_ref = bpy.context.active_object
    side_ref.name = f"{object_name}_Ref_Side"

    # === Step 4: Transparent Material for References ===
    mat_name = f"{object_name}_Ref_Material"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        mat.blend_method = 'BLEND'  # Enable Alpha transparency in Viewport
        mat.shadow_method = 'NONE'  # Prevent shadow casting onto model
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            # Set transparency
            bsdf.inputs['Alpha'].default_value = 0.3
            bsdf.inputs['Roughness'].default_value = 1.0
            
            # Procedural grid to mimic drawing canvas
            checker = nodes.new('ShaderNodeTexChecker')
            checker.inputs['Scale'].default_value = 10.0
            checker.inputs['Color1'].default_value = (0.9, 0.9, 0.95, 1.0)
            checker.inputs['Color2'].default_value = (0.7, 0.7, 0.75, 1.0)
            links.new(checker.outputs['Color'], bsdf.inputs['Base Color'])

    front_ref.data.materials.append(mat)
    side_ref.data.materials.append(mat)

    # === Step 5: Organization ===
    col_name = f"{object_name}_Collection"
    col = bpy.data.collections.get(col_name)
    if not col:
        col = bpy.data.collections.new(col_name)
        scene.collection.children.link(col)
    
    # Move objects to dedicated collection
    for obj in [rig, front_ref, side_ref]:
        for old_col in obj.users_collection:
            old_col.objects.unlink(obj)
        col.objects.link(obj)

    return f"Created '{object_name}' (Standard Color Space + Scale Rig + Reference Boards) at {location}"
