def create_stylized_pine_tree(
    scene_name: str = "Scene",
    object_name: str = "StylizedPineTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    trunk_color: tuple = (0.3, 0.15, 0.05, 1.0), # RGBA
    leaves_color: tuple = (0.1, 0.4, 0.1, 1.0), # RGBA
    num_leaf_layers: int = 5,
    layer_height_factor: float = 0.5, # Factor for the height of each leaf layer relative to overall scale
    layer_scale_reduction: float = 0.8, # Factor by which each subsequent leaf layer scales down
    trunk_subdivisions: int = 8,
    leaf_subdivisions: int = 8,
    randomize_leaf_rotation: bool = True,
    bevel_segments: int = 0, # Number of segments for optional bevel modifier (0 for none)
    bevel_amount: float = 0.05, # Amount for optional bevel modifier
    **kwargs,
) -> str:
    """
    Create a low-poly stylized pine tree in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        trunk_color: (R, G, B, A) base color for the trunk in 0-1 range.
        leaves_color: (R, G, B, A) base color for the leaves in 0-1 range.
        num_leaf_layers: Number of distinct leaf layers.
        layer_height_factor: Factor for the height of each leaf layer relative to overall scale.
        layer_scale_reduction: Factor by which each subsequent leaf layer scales down.
        trunk_subdivisions: Number of vertices for the trunk cylinder.
        leaf_subdivisions: Number of vertices for the leaf circles.
        randomize_leaf_rotation: If True, each leaf layer will have a slight random Z-axis rotation.
        bevel_segments: Number of segments for an optional bevel modifier (0 to disable).
        bevel_amount: Amount for optional bevel modifier.
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'StylizedPineTree' at (0, 0, 0) with 2 objects"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math
    import random

    # Ensure we are in object mode before starting operations
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # --- Materials ---
    # Create Trunk Material
    trunk_mat_name = f"{object_name}_Trunk_Material"
    trunk_mat = bpy.data.materials.get(trunk_mat_name)
    if not trunk_mat:
        trunk_mat = bpy.data.materials.new(name=trunk_mat_name)
        trunk_mat.use_nodes = True
        bsdf = trunk_mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = trunk_color
        bsdf.inputs["Roughness"].default_value = 0.8
    
    # Create Leaves Material
    leaves_mat_name = f"{object_name}_Leaves_Material"
    leaves_mat = bpy.data.materials.get(leaves_mat_name)
    if not leaves_mat:
        leaves_mat = bpy.data.materials.new(name=leaves_mat_name)
        leaves_mat.use_nodes = True
        bsdf = leaves_mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = leaves_color
        bsdf.inputs["Roughness"].default_value = 0.6

    # --- Create Trunk ---
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=trunk_subdivisions,
        radius=0.2 * scale,
        depth=1.5 * scale,
        location=(0, 0, (1.5 * scale) / 2) # Place bottom at 0 in local space
    )
    trunk_obj = bpy.context.active_object
    trunk_obj.name = f"{object_name}_Trunk"
    
    # Assign material
    if trunk_obj.data.materials:
        trunk_obj.data.materials[0] = trunk_mat
    else:
        trunk_obj.data.materials.append(trunk_mat)

    # Apply shading smooth
    bpy.ops.object.shade_smooth()
    trunk_obj.data.use_auto_smooth = True
    trunk_obj.data.auto_smooth_angle = math.radians(30)
    
    # --- Create Leaf Layers ---
    leaf_objs = []
    current_leaf_base_radius = 0.8 * scale
    current_z_pos = (1.5 * scale) # Starting Z above the trunk

    for i in range(num_leaf_layers):
        bpy.ops.mesh.primitive_circle_add(
            vertices=leaf_subdivisions,
            radius=current_leaf_base_radius,
            fill_type='NGON',
            location=(0, 0, current_z_pos)
        )
        leaf_obj = bpy.context.active_object
        leaf_obj.name = f"{object_name}_Leaf_Layer_{i + 1}"
        
        # Enter Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Extrude downwards to create cone shape
        # Select all vertices/face
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Extrude region along Z-axis
        bpy.ops.mesh.extrude_region_move(
            MESH_OT_extrude_region={"use_normals": False},
            TRANSFORM_OT_translate={"value": (0, 0, -layer_height_factor * scale), "orient_type":'NORMAL'}
        )
        
        # Scale down the new extruded bottom part
        bpy.ops.transform.resize(value=(layer_scale_reduction, layer_scale_reduction, 1), orient_type='LOCAL')
        
        # Exit Edit Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Assign material
        if leaf_obj.data.materials:
            leaf_obj.data.materials[0] = leaves_mat
        else:
            leaf_obj.data.materials.append(leaves_mat)
            
        # Apply shading smooth
        bpy.ops.object.shade_smooth()
        leaf_obj.data.use_auto_smooth = True
        leaf_obj.data.auto_smooth_angle = math.radians(30)

        # Rotate layer randomly around Z-axis (optional, for variation)
        if randomize_leaf_rotation:
            random_angle = math.radians(random.uniform(0, 360))
            leaf_obj.rotation_euler.z = random_angle

        leaf_objs.append(leaf_obj)
        current_leaf_base_radius *= layer_scale_reduction # Reduce radius for next layer
        current_z_pos += (layer_height_factor * scale) # Move up for next layer

    # --- Parenting and Final Transformations ---
    # Parent leaf layers to the trunk
    bpy.ops.object.select_all(action='DESELECT')
    for obj in leaf_objs:
        obj.select_set(True)
    trunk_obj.select_set(True)
    
    bpy.context.view_layer.objects.active = trunk_obj # Trunk is the active object for parenting
    bpy.ops.object.parent_set(type='OBJECT')

    # === Apply Bevel Modifier if requested (as shown in the general keys section of the video) ===
    if bevel_segments > 0:
        # Apply bevel to the trunk
        bevel_mod_trunk = trunk_obj.modifiers.new(name="Bevel", type='BEVEL')
        bevel_mod_trunk.width = bevel_amount * scale
        bevel_mod_trunk.segments = bevel_segments
        
        # Apply bevel to each leaf layer
        for leaf_obj in leaf_objs:
            bevel_mod_leaf = leaf_obj.modifiers.new(name="Bevel", type='BEVEL')
            bevel_mod_leaf.width = bevel_amount * scale
            bevel_mod_leaf.segments = bevel_segments

    # --- Position the entire tree ---
    # Set location of the main parent (trunk)
    trunk_obj.location = Vector(location)

    # Scale the trunk, which scales all children (already done at creation, but good to ensure)
    trunk_obj.scale = (scale, scale, scale) 

    total_objects_created = len(leaf_objs) + 1 # trunk + leaf layers

    return f"Created '{object_name}' at {location} with {total_objects_created} objects."

