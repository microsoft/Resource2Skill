def create_stylized_pine_tree(
    scene_name: str = "Scene",
    object_name: str = "StylizedPineTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    trunk_color: tuple = (0.5, 0.3, 0.1, 1.0), # RGBA for trunk (e.g., brown)
    foliage_color: tuple = (0.2, 0.6, 0.3, 1.0), # RGBA for foliage (e.g., green)
    trunk_height: float = 2.0,
    trunk_radius_bottom: float = 0.2,
    trunk_radius_top: float = 0.05,
    foliage_layers: int = 5,
    foliage_base_radius: float = 0.8,
    foliage_top_radius_ratio: float = 0.1, # Ratio of foliage_base_radius for top layers
    foliage_layer_height: float = 0.6,
    foliage_segment_count: int = 12, # Number of vertices for circular base/trunk
    **kwargs,
) -> str:
    """
    Create a stylized low-poly pine tree with a trunk and layered foliage.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created tree objects.
        location: (x, y, z) world-space position for the tree's base.
        scale: Uniform scale factor for the entire tree.
        trunk_color: (R, G, B, A) base color for the trunk material.
        foliage_color: (R, G, B, A) base color for the foliage material.
        trunk_height: Height of the tree trunk.
        trunk_radius_bottom: Radius of the trunk at its base.
        trunk_radius_top: Radius of the trunk at its top.
        foliage_layers: Number of foliage layers.
        foliage_base_radius: Radius of the widest (bottom-most) foliage layer.
        foliage_top_radius_ratio: Ratio to apply to foliage_base_radius for the smallest (top-most) foliage layer.
        foliage_layer_height: Height of each individual foliage layer segment.
        foliage_segment_count: Number of vertices for the circular base of each foliage layer (e.g., 8 or 12).
        **kwargs: Additional overrides (e.g., auto_smooth_angle).

    Returns:
        Status string, e.g., "Created 'StylizedPineTree' at (0, 0, 0) with 6 objects"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math
    import random # For random rotation offset

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Materials ---
    trunk_mat = bpy.data.materials.new(name=f"{object_name}_TrunkMat")
    trunk_mat.use_nodes = True
    bsdf_trunk = trunk_mat.node_tree.nodes["Principled BSDF"]
    bsdf_trunk.inputs[0].default_value = trunk_color # Base Color
    bsdf_trunk.inputs[7].default_value = kwargs.get('roughness_trunk', 0.8) # Roughness

    foliage_mat = bpy.data.materials.new(name=f"{object_name}_FoliageMat")
    foliage_mat.use_nodes = True
    bsdf_foliage = foliage_mat.node_tree.nodes["Principled BSDF"]
    bsdf_foliage.inputs[0].default_value = foliage_color # Base Color
    bsdf_foliage.inputs[7].default_value = kwargs.get('roughness_foliage', 0.8) # Roughness

    auto_smooth_angle_rad = math.radians(kwargs.get('auto_smooth_angle', 60))

    # --- Trunk Creation ---
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=foliage_segment_count,
        radius=trunk_radius_bottom,
        depth=trunk_height,
        location=location,
        enter_editmode=False
    )
    trunk_obj = bpy.context.active_object
    trunk_obj.name = f"{object_name}_Trunk"
    
    # Apply material
    if trunk_obj.data.materials:
        trunk_obj.data.materials[0] = trunk_mat
    else:
        trunk_obj.data.materials.append(trunk_mat)

    # Taper the trunk using edit mode operations
    bpy.context.view_layer.objects.active = trunk_obj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(trunk_obj.data)

    # Select top face and scale
    top_faces = [f for f in bm.faces if f.normal.z > 0.9 and f.select == False] # Ensure not already selected
    if top_faces:
        for face in top_faces:
            face.select = True
        
        # Scale top face to match trunk_radius_top
        scale_factor = trunk_radius_top / trunk_radius_bottom
        bpy.ops.transform.resize(value=(scale_factor, scale_factor, 1), orient_type='LOCAL') 
        
        # Move top face to maintain desired trunk height if the scale affected its Z position
        # For a default cylinder, it scales around its origin (center), so Z movement isn't strictly needed for correct height
        # unless depth was scaled as well, which is not the case here.

    bmesh.update_edit_mesh(trunk_obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth() # Apply initial shade smooth

    # Apply Auto Smooth
    trunk_obj.data.use_auto_smooth = True
    trunk_obj.data.auto_smooth_angle = auto_smooth_angle_rad

    # --- Foliage Layers Creation ---
    foliage_objects = []
    # Start foliage from slightly above the trunk's top
    current_z_offset = trunk_height * 0.5 + foliage_layer_height * 0.25 

    for i in range(foliage_layers):
        # Interpolate radius for current layer
        # Linearly decrease radius from foliage_base_radius to foliage_base_radius * foliage_top_radius_ratio
        foliage_min_radius = foliage_base_radius * foliage_top_radius_ratio
        layer_radius = foliage_base_radius - (foliage_base_radius - foliage_min_radius) * (i / max(1, foliage_layers - 1))
        
        # Create a new cone for each layer
        bpy.ops.mesh.primitive_cone_add(
            vertices=foliage_segment_count,
            radius1=layer_radius,
            radius2=0.01, # Small top radius to make it pointy
            depth=foliage_layer_height,
            location=(location[0], location[1], location[2] + current_z_offset), # Position base of cone
            enter_editmode=False
        )
        foliage_obj = bpy.context.active_object
        foliage_obj.name = f"{object_name}_Foliage_{i:02d}"
        
        # Apply material
        if foliage_obj.data.materials:
            foliage_obj.data.materials[0] = foliage_mat
        else:
            foliage_obj.data.materials.append(foliage_mat)

        bpy.ops.object.shade_smooth() # Apply initial shade smooth

        # Apply Auto Smooth
        foliage_obj.data.use_auto_smooth = True
        foliage_obj.data.auto_smooth_angle = auto_smooth_angle_rad

        # Randomize Z rotation for variety
        foliage_obj.rotation_euler.z = math.radians(random.uniform(0, 360))

        foliage_objects.append(foliage_obj)

        # Move up for next layer, with a slight overlap (adjust 0.6 as needed)
        current_z_offset += foliage_layer_height * 0.65 

    # --- Parenting & Final Scaling ---
    # Select all foliage objects
    for obj in foliage_objects:
        obj.select_set(True)
    
    # Select the trunk as the active object (parent)
    trunk_obj.select_set(True)
    bpy.context.view_layer.objects.active = trunk_obj
    
    # Parent foliage to trunk
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

    # Clear location of children to keep relative offset (already done with keep_transform but often useful)
    # This might reset locations if not careful, better to skip for this setup where initial location is correct.
    # for obj in foliage_objects:
    #     obj.location = obj.matrix_local.translation # Retain local position relative to parent

    # Scale the entire tree (parented objects will scale along)
    # The parent's scale will propagate to children
    trunk_obj.scale = (scale, scale, scale)

    # Clear selection after operations
    bpy.ops.object.select_all(action='DESELECT')
    trunk_obj.select_set(True) # Re-select the main tree object (trunk)

    return f"Created '{object_name}' at {location} with {1 + len(foliage_objects)} objects (trunk + {len(foliage_objects)} foliage layers)."

