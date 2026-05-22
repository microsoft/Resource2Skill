def create_object(
    scene_name: str = "Scene",
    object_name: str = "Stylized_Workspace",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.5),
    **kwargs,
) -> str:
    """
    Create a Stylized Character Workspace Setup in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created workspace rig.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = approx 2m character height).
        material_color: (R, G, B) placeholder color for reference planes.
        **kwargs: Additional overrides.

    Returns:
        Status string detailing the setup.
    """
    import bpy
    import math
    import addon_utils
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Configure Render & Color Management for Stylized Art ===
    scene.render.engine = 'BLENDER_EEVEE'
    
    # Force Standard view transform (crucial for flat/stylized color accuracy)
    if hasattr(scene, 'view_settings'):
        scene.view_settings.view_transform = 'Standard'
        
    # Disable post-processing for a clean viewport
    if hasattr(scene, 'eevee'):
        scene.eevee.use_gtao = False
        scene.eevee.use_bloom = False
        scene.eevee.use_ssr = False
        scene.eevee.use_motion_blur = False

    # Create root object to keep the outliner clean
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    setup_root = bpy.context.active_object
    setup_root.name = object_name
    setup_root.scale = (scale, scale, scale)

    # === Step 2: Add Scale Reference Rig ===
    addon_utils.enable("rigify")
    try:
        # Attempt to add Rigify Meta-rig
        bpy.ops.object.armature_human_metarig_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_ScaleReference"
    except Exception:
        # Fallback to basic armature if Rigify is unavailable
        bpy.ops.object.armature_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_ScaleReference"
        rig.scale = (1, 1, 1)
        
    rig.parent = setup_root

    # === Step 3: Create Semi-Transparent Reference Planes ===
    # Setup material to mimic image opacity behavior (50% transparent, slightly emissive)
    mat = bpy.data.materials.new(name=f"{object_name}_ReferenceMat")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'  # Enable transparency in Eevee
    
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Alpha'].default_value = 0.5  # 50% opacity
        
        # Connect emission for unlit visibility
        if 'Emission' in bsdf.inputs:
            # Handle Blender 4.0+ Principled BSDF
            if hasattr(bsdf.inputs['Emission'], "default_value") and type(bsdf.inputs['Emission'].default_value) == float:
                # Old API
                pass
            else:
                bsdf.inputs['Emission Color'].default_value = (*material_color, 1.0)
                if 'Emission Strength' in bsdf.inputs:
                    bsdf.inputs['Emission Strength'].default_value = 0.2
        elif 'Emission' in bsdf.inputs: # Older blender fallback
             bsdf.inputs['Emission'].default_value = (*material_color, 1.0)

    # Add Front Reference Plane (placed behind character on +Y)
    bpy.ops.mesh.primitive_plane_add(size=2, location=(location[0], location[1] + 1.5, location[2] + 1))
    front_ref = bpy.context.active_object
    front_ref.name = f"{object_name}_FrontView"
    front_ref.rotation_euler = (math.pi / 2, 0, 0)
    front_ref.data.materials.append(mat)
    front_ref.parent = setup_root
    
    # Add Side Reference Plane (placed to the left on -X)
    bpy.ops.mesh.primitive_plane_add(size=2, location=(location[0] - 1.5, location[1], location[2] + 1))
    side_ref = bpy.context.active_object
    side_ref.name = f"{object_name}_SideView"
    side_ref.rotation_euler = (math.pi / 2, 0, math.pi / 2)
    side_ref.data.materials.append(mat)
    side_ref.parent = setup_root

    # Deselect all to finish cleanly
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created Stylized Workspace '{object_name}' at {location} with scale rig, front/side reference boards, and 'Standard' color transform applied."
