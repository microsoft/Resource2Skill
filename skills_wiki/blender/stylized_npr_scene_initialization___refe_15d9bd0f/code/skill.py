def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedSetup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 1.0), # Color for the reference planes
    **kwargs,
) -> str:
    """
    Initialize a stylized/NPR modeling workspace in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created reference setup.
        location: (x, y, z) world-space origin for the setup.
        scale: Uniform scale factor (1.0 represents standard human height ~1.8m).
        material_color: (R, G, B) base color for the reference planes.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the setup.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Render Engine & Scene Settings ===
    scene.render.engine = 'BLENDER_EEVEE'
    
    # Disable PBR screen-space effects for a pure stylized/flat look
    if hasattr(scene, "eevee"):
        scene.eevee.use_gtao = False
        scene.eevee.use_bloom = False
        scene.eevee.use_ssr = False
        if hasattr(scene.eevee, "use_motion_blur"):
            scene.eevee.use_motion_blur = False

    # CRITICAL: Set View Transform to 'Standard' to prevent color shifting/desaturation
    scene.view_settings.view_transform = 'Standard'

    # === Step 2: Reference Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_RefMat")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'
    mat.shadow_method = 'NONE'
    
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        
        # Handle alpha for transparency
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = 0.25
            
        # Make it unlit/emission-like so it's always visible for tracing
        if "Emission Color" in bsdf.inputs: # Blender 4.0+
            bsdf.inputs["Emission Color"].default_value = (*material_color, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 0.5
        elif "Emission" in bsdf.inputs: # Blender 3.x
            bsdf.inputs["Emission"].default_value = (*material_color, 1.0)
            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = 0.5

    # === Step 3: Reference Planes ===
    base_loc = Vector(location)
    
    # Front Reference Plane (moved back on Y axis)
    bpy.ops.mesh.primitive_plane_add(
        size=2.5 * scale, 
        location=base_loc + Vector((0, 1.5 * scale, 1.25 * scale))
    )
    front_ref = bpy.context.active_object
    front_ref.name = f"{object_name}_Front"
    front_ref.rotation_euler = (math.radians(90), 0, 0)
    front_ref.data.materials.append(mat)
    
    # Side Reference Plane (moved left on X axis)
    bpy.ops.mesh.primitive_plane_add(
        size=2.5 * scale, 
        location=base_loc + Vector((-1.5 * scale, 0, 1.25 * scale))
    )
    side_ref = bpy.context.active_object
    side_ref.name = f"{object_name}_Side"
    side_ref.rotation_euler = (math.radians(90), 0, math.radians(90))
    side_ref.data.materials.append(mat)

    # === Step 4: Scale Dummy (Replacing Rigify Metarig) ===
    # Adds a lightweight wireframe cylinder representing a ~1.8m tall human bounding box
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8, 
        radius=0.35 * scale, 
        depth=1.8 * scale, 
        location=base_loc + Vector((0, 0, 0.9 * scale))
    )
    scale_dummy = bpy.context.active_object
    scale_dummy.name = f"{object_name}_Scale_Dummy"
    scale_dummy.display_type = 'WIRE'
    scale_dummy.hide_render = True # Do not show in final renders

    # === Step 5: Organization ===
    # Group everything under a master Empty
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    parent_empty = bpy.context.active_object
    parent_empty.name = object_name
    
    front_ref.parent = parent_empty
    side_ref.parent = parent_empty
    scale_dummy.parent = parent_empty

    return f"Created Stylized Scene Setup '{object_name}' at {location}. View Transform is now 'Standard'."
