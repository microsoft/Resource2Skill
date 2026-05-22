def create_object(
    scene_name: str = "Scene",
    object_name: str = "Stylized_Project_Setup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.5), # Color for the placeholder reference planes
    **kwargs,
) -> str:
    """
    Configures the Blender scene for stylized character modeling and sets up a scale reference environment.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the setup objects.
        location: (x, y, z) world-space position for the setup origin.
        scale: Overall scale factor for the reference setup.
        material_color: (R, G, B) tint for the reference planes.
        **kwargs: Additional overrides.
        
    Returns:
        Status string describing the setup.
    """
    import bpy
    import bmesh
    from mathutils import Vector, Euler
    import math
    import addon_utils

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Configure Render Engine and Color Management ===
    # Crucial for stylized/anime characters: use Eevee and Standard color transform
    scene.render.engine = 'BLENDER_EEVEE'
    scene.eevee.use_gtao = False
    scene.eevee.use_bloom = False
    scene.eevee.use_ssr = False
    scene.eevee.use_motion_blur = False
    
    # Prevents "washed out" colors, mapping hex codes 1:1 to the screen
    scene.view_settings.view_transform = 'Standard'

    # Create a root empty to keep the outliner organized
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    setup_root = bpy.context.active_object
    setup_root.name = object_name
    setup_root.scale = (scale, scale, scale)

    # === Step 2: Add Scale Reference (Human Meta-Rig) ===
    rig_added = False
    try:
        # Attempt to enable Rigify and spawn the human meta-rig
        addon_utils.enable("rigify")
        bpy.ops.object.armature_human_metarig_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_ScaleRef_Rig"
        rig.parent = setup_root
        
        # The Rigify meta-rig is generated with its origin slightly off the floor
        rig.location.z += 0.95 
        rig_added = True
    except Exception as e:
        print(f"Could not add Rigify rig (context issue): {e}. Using fallback.")
        # Fallback to a basic bounding box representing a 1.8m tall human
        bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=1.8, location=(location[0], location[1], location[2] + 0.9))
        rig = bpy.context.active_object
        rig.name = f"{object_name}_ScaleRef_Fallback"
        rig.parent = setup_root

    # Lock the scale reference so it isn't accidentally edited
    rig.hide_select = True

    # === Step 3: Add Reference Planes ===
    # We construct semi-transparent planes to mimic the behavior of Reference Image Empties
    
    mat_ref = bpy.data.materials.new(name=f"{object_name}_RefPlane_Mat")
    mat_ref.use_nodes = True
    mat_ref.blend_method = 'BLEND' # Enable Eevee transparency
    mat_ref.shadow_method = 'NONE' # References shouldn't cast shadows
    
    bsdf = mat_ref.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        # Set to 50% opacity as instructed in the tutorial
        bsdf.inputs["Alpha"].default_value = 0.5 
        bsdf.inputs["Roughness"].default_value = 1.0

    plane_size = 2.2 # Covers a standard human height

    # Front Reference Plane
    # Moved backwards along Y, rotated to face Front orthographic (Numpad 1)
    bpy.ops.mesh.primitive_plane_add(size=plane_size)
    front_ref = bpy.context.active_object
    front_ref.name = f"{object_name}_Ref_Front"
    front_ref.location = Vector((location[0], location[1] + 1.2, location[2] + plane_size/2))
    front_ref.rotation_euler = Euler((math.radians(90), 0, 0), 'XYZ')
    front_ref.data.materials.append(mat_ref)
    front_ref.parent = setup_root
    front_ref.hide_select = True # Prevent accidental selection during modeling

    # Side Reference Plane
    # Moved left along X, rotated to face Right orthographic (Numpad 3)
    bpy.ops.mesh.primitive_plane_add(size=plane_size)
    side_ref = bpy.context.active_object
    side_ref.name = f"{object_name}_Ref_Side"
    side_ref.location = Vector((location[0] - 1.2, location[1], location[2] + plane_size/2))
    side_ref.rotation_euler = Euler((math.radians(90), 0, math.radians(-90)), 'XYZ')
    side_ref.data.materials.append(mat_ref)
    side_ref.parent = setup_root
    side_ref.hide_select = True # Prevent accidental selection during modeling

    return f"Created Stylized Project Setup '{object_name}' (Standard View Transform set, Rigify reference: {rig_added})"
