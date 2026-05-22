def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedCharacterSetup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 0.8), # Blueprint placeholder tint
    **kwargs,
) -> str:
    """
    Create a Stylized Character Modeling Setup in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the root container object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the rig and references.
        material_color: (R, G, B) tint for the placeholder reference planes.

    Returns:
        Status string describing the created setup.
    """
    import bpy
    import math
    import addon_utils
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Stylized Render & Color Management Setup ===
    # For stylized/anime models, 'Standard' view transform is absolutely required 
    # to prevent colors from washing out (unlike AgX/Filmic which are for photorealism).
    scene.render.engine = 'BLENDER_EEVEE'
    scene.display_settings.display_device = 'sRGB'
    scene.view_settings.view_transform = 'Standard'

    # Ensure we are in object mode before adding items
    if bpy.context.active_object and bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # === Step 2: Create Root Container ===
    root = bpy.data.objects.new(object_name, None)
    scene.collection.objects.link(root)
    root.location = Vector(location)
    root.scale = (scale, scale, scale)

    # === Step 3: Add Scale Reference Rig (Rigify) ===
    rig_added = False
    try:
        # Safely enable rigify addon if not already enabled
        if not addon_utils.check("rigify")[0]:
            addon_utils.enable("rigify", default_set=True)
            
        bpy.ops.object.armature_human_metarig_add(location=(0, 0, 0))
        rig = bpy.context.active_object
        rig_added = True
    except Exception:
        # Fallback if rigify fails/is missing
        bpy.ops.object.armature_add(location=(0, 0, 0))
        rig = bpy.context.active_object

    rig.name = f"{object_name}_ScaleRefRig"
    rig.display_type = 'WIRE'
    rig.show_in_front = True
    
    # Parent rig to root
    rig.parent = root
    rig.location = (0, 0, 0) # Zero out location relative to parent

    # === Step 4: Create Transparent Reference Planes ===
    # Material for blueprint references
    mat = bpy.data.materials.new(name=f"{object_name}_Ref_Mat")
    mat.use_nodes = True
    mat.blend_method = 'BLEND' # Enable transparency in EEVEE
    mat.shadow_method = 'NONE'
    
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Alpha'].default_value = 0.4 # Semi-transparent
        bsdf.inputs['Roughness'].default_value = 1.0 # Matte
        
        # Safely handle Specular inputs across different Blender versions (pre-4.0 and 4.0+)
        if 'Specular' in bsdf.inputs:
            bsdf.inputs['Specular'].default_value = 0.0
        elif 'Specular IOR Level' in bsdf.inputs:
            bsdf.inputs['Specular IOR Level'].default_value = 0.0

    # Add Front Reference Plane
    bpy.ops.mesh.primitive_plane_add(size=2)
    front_ref = bpy.context.active_object
    front_ref.name = f"{object_name}_Blueprint_Front"
    front_ref.rotation_euler = (math.radians(90), 0, 0)
    # Move back on Y so it doesn't block front modeling, scale to roughly human rig height
    front_ref.location = (0, 1.5, 1.0) 
    front_ref.scale = (1.5, 1.2, 1.5) 
    front_ref.data.materials.append(mat)
    front_ref.parent = root

    # Add Side Reference Plane
    bpy.ops.mesh.primitive_plane_add(size=2)
    side_ref = bpy.context.active_object
    side_ref.name = f"{object_name}_Blueprint_Side"
    side_ref.rotation_euler = (math.radians(90), 0, math.radians(90))
    # Move left on X so it doesn't block side modeling
    side_ref.location = (-1.5, 0, 1.0) 
    side_ref.scale = (1.5, 1.2, 1.5)
    side_ref.data.materials.append(mat)
    side_ref.parent = root

    # Clean up selection state
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created '{object_name}' setup at {location}. View Transform explicitly set to 'Standard'. Human Meta-Rig included: {rig_added}"
