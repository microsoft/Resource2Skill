def create_character_modeling_setup(
    scene_name: str = "Scene",
    object_prefix: str = "LoveChan",
    scale: float = 1.0,
    front_image_path: str = "//resources/lovechan_frontview.png",
    side_image_path: str = "//resources/lovechan_sideview.png",
    image_offset_from_rig: float = 0.5, # Distance references are moved along Y/X-axis from rig
    image_opacity: float = 0.5,
    meta_rig_location: tuple = (0, 0, 0),
    meta_rig_height_units: float = 2.0, # Default height of Rigify Human (Meta-Rig in Blender units)
    **kwargs,
) -> str:
    """
    Sets up a Blender scene for character modeling with 2D image references and a Human (Meta-Rig).

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_prefix: Prefix for the created objects (e.g., LoveChan_FrontRef, LoveChan_MetaRig).
        scale: Uniform scale factor for the entire setup.
        front_image_path: Relative or absolute path to the front reference image.
        side_image_path: Relative or absolute path to the side reference image.
        image_offset_from_rig: Distance to move image planes from the meta-rig along Y/X axis.
        image_opacity: Opacity level for the reference images (0.0 to 1.0).
        meta_rig_location: (x, y, z) world-space position for the meta-rig.
        meta_rig_height_units: Nominal height of the Rigify Human (Meta-Rig) in Blender units (default is ~2 units).
        **kwargs: Additional overrides for specific settings (not used in this version but for future expansion).

    Returns:
        Status string, e.g., "Created 'LoveChan' modeling setup in Scene."
    """
    import bpy
    from mathutils import Vector
    import os
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # --- 1. Enable Rigify Add-on (if not already enabled) ---
    try:
        if "rigify" not in bpy.context.preferences.addons:
             bpy.ops.preferences.addon_enable(module="rigify")
        else:
             print("Rigify add-on is already enabled.")
    except Exception as e:
        print(f"Failed to enable Rigify add-on: {e}")

    # --- 2. Configure Render Settings for Stylized Modeling ---
    render = scene.render
    render.engine = 'BLENDER_EEVEE'
    
    scene.eevee.use_gtao = False 
    scene.eevee.use_bloom = False
    scene.eevee.use_ssr = False
    render.use_motion_blur = False

    # --- 3. Set Color Management View Transform to Standard ---
    scene.view_settings.view_transform = 'Standard'

    # --- 4. Get absolute paths for images ---
    blend_dir = os.path.dirname(bpy.data.filepath)
    if not blend_dir:
        print("Warning: Blender file not saved. Cannot resolve relative image paths reliably.")
        # Attempt to use absolute paths directly if blend file not saved
        front_img_abs_path = front_image_path
        side_img_abs_path = side_image_path
    else:
        front_img_abs_path = bpy.path.abspath(front_image_path)
        side_img_abs_path = bpy.path.abspath(side_image_path)
    
    if not os.path.exists(front_img_abs_path):
        return f"Error: Front image not found at '{front_img_abs_path}'"
    if not os.path.exists(side_img_abs_path):
        return f"Error: Side image not found at '{side_img_abs_path}'"

    # Store created objects
    created_objects = []

    # --- 5. Add Human Meta-Rig ---
    # Deselect all before adding to ensure context is clear
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None

    bpy.ops.object.armature_add(type='HUMAN')
    meta_rig_obj = bpy.context.object
    meta_rig_obj.name = f"{object_prefix}_MetaRig"
    meta_rig_obj.location = Vector(meta_rig_location)
    meta_rig_obj.scale = (scale, scale, scale)
    created_objects.append(meta_rig_obj)

    # --- 6. Add Reference Images ---
    # Set 3D cursor to origin for consistent placement before adding images
    scene.cursor.location = (0, 0, 0)

    # Use a temporary area context for view operations to ensure consistency
    view_3d_area = None
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            view_3d_area = area
            break

    if not view_3d_area:
        return "Error: No 3D Viewport found to add references. Please ensure a 3D Viewport is open."
    
    with bpy.context.temp_override(area=view_3d_area):
        # --- Front Reference ---
        # Go to Front Orthographic view
        bpy.ops.view3d.view_axis(type='FRONT', align_active=True, orthographic=True)
        bpy.ops.image.reference_add(filepath=front_img_abs_path, view_align=True)
        front_ref_obj = bpy.context.object
        front_ref_obj.name = f"{object_prefix}_FrontRef"
        created_objects.append(front_ref_obj)

        # Scale and position front reference
        # `bpy.ops.image.reference_add` adds empty at cursor, scaled to fit 1 unit height by default for images,
        # but its dimensions can vary depending on image aspect ratio and default scaling.
        image_data = front_ref_obj.data
        if image_data:
            # Assuming image empty origin is at its center after creation (default for Image Empty)
            # Its Z-dimension is the height of the image plane
            current_empty_height = front_ref_obj.dimensions.z # Height of the image plane in current scale
            
            if current_empty_height > 0:
                target_height = meta_rig_height_units * scale
                scale_factor = target_height / current_empty_height
                front_ref_obj.scale *= scale_factor
                
                # Move up so bottom of image is at Z=0. Origin is at center of plane.
                front_ref_obj.location.z = (front_ref_obj.dimensions.z / 2) 
                front_ref_obj.location.y = -image_offset_from_rig * scale # Move slightly in front

        # --- Side Reference ---
        # Go to Right Orthographic view
        bpy.ops.view3d.view_axis(type='RIGHT', align_active=True, orthographic=True)
        bpy.ops.image.reference_add(filepath=side_img_abs_path, view_align=True)
        side_ref_obj = bpy.context.object
        side_ref_obj.name = f"{object_prefix}_SideRef"
        created_objects.append(side_ref_obj)

        # Scale and position side reference
        image_data = side_ref_obj.data
        if image_data:
            current_empty_height = side_ref_obj.dimensions.z
            
            if current_empty_height > 0:
                target_height = meta_rig_height_units * scale
                scale_factor = target_height / current_empty_height
                side_ref_obj.scale *= scale_factor
                
                # Move up so bottom of image is at Z=0
                side_ref_obj.location.z = (side_ref_obj.dimensions.z / 2)
                side_ref_obj.location.x = image_offset_from_rig * scale # Move slightly to the right

        # --- Revert view to user perspective ---
        bpy.ops.view3d.view_persp_toggle() # Toggle back if in ortho

    # --- 7. Set Image Opacity ---
    def set_image_opacity(obj, opacity):
        if obj and obj.type == 'EMPTY' and obj.empty_display_type == 'IMAGE':
            if obj.data.materials:
                mat = obj.data.materials[0]
                if mat and mat.use_nodes:
                    principled_node = None
                    for node in mat.node_tree.nodes:
                        if node.type == 'BSDF_PRINCIPLED':
                            principled_node = node
                            break
                    if principled_node and principled_node.inputs.get("Alpha"):
                        principled_node.inputs["Alpha"].default_value = opacity
                    
                    mat.blend_method = 'BLEND'
                    mat.shadow_method = 'HASHED' 
            
            # X-Ray makes the object visible through other geometry, useful for references
            obj.show_in_front = True # Always show in front of other objects
            obj.show_xray = True # Enable X-ray for empty (this is for viewport display)

    set_image_opacity(front_ref_obj, image_opacity)
    set_image_opacity(side_ref_obj, image_opacity)
    
    # --- Final Cleanup / Selection ---
    bpy.ops.object.select_all(action='DESELECT')
    if meta_rig_obj: # Select the rig as the main working object
        meta_rig_obj.select_set(True)
        bpy.context.view_layer.objects.active = meta_rig_obj
    
    return f"Created '{object_prefix}' modeling setup with {len(created_objects)} objects in scene '{scene.name}'."

