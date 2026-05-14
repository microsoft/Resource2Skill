def create_object(
    scene_name: str = "Scene",
    object_name: str = "Stylized_Ref_Setup",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.5, 0.8), # Blueprint tint color
    **kwargs,
) -> str:
    """
    Create a calibrated environment and reference blueprint setup for Stylized Character Modeling.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the root tracking empty.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the entire reference group.
        material_color: (R, G, B) tint for the reference planes.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    import addon_utils
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Calibrate Scene for Stylized Modeling ===
    scene.render.engine = 'BLENDER_EEVEE'
    
    # Force Standard View Transform for 1:1 hex color matching
    try:
        scene.view_settings.view_transform = 'Standard'
    except Exception:
        pass

    # Disable PBR post-processing for a clean orthographic view
    if hasattr(scene, 'eevee'):
        for attr in ['use_gtao', 'use_bloom', 'use_ssr', 'use_motion_blur']:
            if hasattr(scene.eevee, attr):
                setattr(scene.eevee, attr, False)

    # === Step 2: Create Root Controller ===
    bpy.ops.object.empty_add(type='ARROWS', align='WORLD', location=location)
    root = bpy.context.active_object
    root.name = object_name
    root.scale = (scale, scale, scale)

    # === Step 3: Create Blueprint Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Blueprint_Mat")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'
    mat.shadow_method = 'NONE'
    
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        # Base color + Transparency
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        if 'Alpha' in bsdf.inputs:
            bsdf.inputs['Alpha'].default_value = 0.25
        
        # Slight emission to keep references visible without lights
        if 'Emission Color' in bsdf.inputs:  # Blender 4.0+
            bsdf.inputs['Emission Color'].default_value = (*material_color, 1.0)
            bsdf.inputs['Emission Strength'].default_value = 0.5
        elif 'Emission' in bsdf.inputs:      # Pre-4.0
            bsdf.inputs['Emission'].default_value = (*material_color, 1.0)

    # === Step 4: Create Reference Planes ===
    # Front Reference
    bpy.ops.mesh.primitive_plane_add(size=2.0)
    front_ref = bpy.context.active_object
    front_ref.name = f"{object_name}_Front_Ref"
    front_ref.data.materials.append(mat)
    front_ref.parent = root
    # Stand up on X axis, offset behind the center
    front_ref.rotation_euler = (math.radians(90), 0, 0)
    front_ref.location = Vector((0.0, 2.0, 2.0))
    front_ref.scale = Vector((2.0, 2.0, 2.0))

    # Side Reference
    bpy.ops.mesh.primitive_plane_add(size=2.0)
    side_ref = bpy.context.active_object
    side_ref.name = f"{object_name}_Side_Ref"
    side_ref.data.materials.append(mat)
    side_ref.parent = root
    # Stand up and rotate to face side, offset to the right
    side_ref.rotation_euler = (math.radians(90), 0, math.radians(90))
    side_ref.location = Vector((2.0, 0.0, 2.0))
    side_ref.scale = Vector((2.0, 2.0, 2.0))

    # === Step 5: Add Scale Reference Rig ===
    addon_utils.enable("rigify")
    rig_added = False
    try:
        # Add the human metarig shown in the video
        bpy.ops.object.armature_human_metarig_add(location=(0,0,0))
        rig = bpy.context.active_object
        rig.name = f"{object_name}_Scale_Guide"
        rig.parent = root
        rig.location = Vector((0.0, 0.0, 0.0))
        # Ensure bone wireframes show through geometry
        rig.show_in_front = True 
        rig_added = True
    except Exception as e:
        print(f"Rigify metarig generation skipped/failed: {e}")

    # Fallback to basic armature if Rigify isn't functioning in headless mode
    if not rig_added:
        bpy.ops.object.armature_add(location=(0,0,0))
        rig = bpy.context.active_object
        rig.name = f"{object_name}_Scale_Guide"
        rig.parent = root
        rig.location = Vector((0.0, 0.0, 0.0))
        rig.show_in_front = True

    return f"Created '{object_name}' (Reference planes + Scale Rig) at {location} with standard view transform applied."
