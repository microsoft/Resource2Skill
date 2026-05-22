def create_well_base_stones(
    scene_name: str = "Scene",
    object_name: str = "WellBase",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    stone_color: tuple = (0.6, 0.6, 0.6, 1.0), # Default light grey stone color, added alpha
    num_stones_per_layer: int = 12, # Number of stones to form a circle
    num_layers: int = 3,
    base_stone_dims: tuple = (0.76, 0.381, 0.381), # X, Y, Z dimensions
    bevel_amount: float = 0.04,
    randomize_amount: float = 0.001,
    decimate_ratio: float = 0.37,
    layer_taper_scale_factor: float = 0.9, # Scale factor for higher layers
    layer_offset_z_factor: float = 0.2, # Z offset for each layer relative to stone height
) -> str:
    """
    Create a low-poly well base made of stacked, slightly randomized stone rings.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created well base object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the entire well.
        stone_color: (R, G, B, A) base color in 0-1 range for the stones.
        num_stones_per_layer: How many stones make up one circular layer.
        num_layers: Number of stacked layers for the well base.
        base_stone_dims: (X, Y, Z) dimensions of a single stone before randomization.
        bevel_amount: Amount for the bevel modifier.
        randomize_amount: Amount for vertex randomization.
        decimate_ratio: Ratio for the decimate modifier (0 to 1).
        layer_taper_scale_factor: Scale higher layers by this factor (e.g., 0.9 for tapering).
        layer_offset_z_factor: Z offset between each layer, relative to base stone Z dimension.

    Returns:
        Status string, e.g., "Created 'WellBase' at (0, 0, 0) with 3 layers"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import random
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Create a new collection for the well base
    well_collection_name = object_name + "_Collection"
    well_collection = bpy.data.collections.get(well_collection_name)
    if not well_collection:
        well_collection = bpy.data.collections.new(well_collection_name)
        scene.collection.children.link(well_collection)

    # Create a "Spares" collection for intermediate objects
    spares_collection_name = "Spares_" + object_name
    spares_collection = bpy.data.collections.get(spares_collection_name)
    if not spares_collection:
        spares_collection = bpy.data.collections.new(spares_collection_name)
        scene.collection.children.link(spares_collection)
    spares_collection.hide_viewport = True
    spares_collection.hide_render = True

    # --- 1. Create a single base stone template ---
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    base_stone_obj = bpy.context.object
    base_stone_obj.name = "BaseStoneTemplate"
    
    # Scale to desired dimensions (cube is 2x2x2, so divide dims by 2 for scale)
    base_stone_obj.scale = (base_stone_dims[0] / 2, base_stone_dims[1] / 2, base_stone_dims[2] / 2)
    bpy.context.view_layer.objects.active = base_stone_obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Move it just above the floor (its origin is still at 0,0,0)
    base_stone_obj.location.z = base_stone_dims[2] / 2 

    # Switch to Edit Mode for bevel and randomize
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(base_stone_obj.data)
    bm.select_mode = {'VERT', 'EDGE', 'FACE'} # Ensure all modes are available

    # Bevel all edges
    bmesh.ops.bevel(bm, geom=bm.edges[:], segments=1, width=bevel_amount, profile=0.5)
    
    # Add loop cuts for randomization (adjusting cuts for different axes to match video more closely)
    # Along X-axis (long way)
    bmesh.ops.loopcut_slide(bm, edges=bm.edges, normal_factor=0, object_index=0, edge_index=0, cuts=2, smoothness=0, falloff='SMOOTH')
    # Along Y-axis (short way)
    bmesh.ops.loopcut_slide(bm, edges=bm.edges, normal_factor=0, object_index=0, edge_index=0, cuts=1, smoothness=0, falloff='SMOOTH')
    # Along Z-axis (height)
    bmesh.ops.loopcut_slide(bm, edges=bm.edges, normal_factor=0, object_index=0, edge_index=0, cuts=1, smoothness=0, falloff='SMOOTH')
    
    # Randomize vertices
    bmesh.ops.randomize(bm, verts=bm.verts[:], amount=randomize_amount)
    
    bmesh.update_edit_mesh(base_stone_obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Add material to the base stone template
    mat = bpy.data.materials.new(name="StoneMaterial")
    mat.diffuse_color = stone_color # RGBA tuple
    base_stone_obj.data.materials.append(mat)

    # Move template stone to spares collection
    bpy.context.collection.objects.unlink(base_stone_obj) # Unlink from original scene collection
    spares_collection.objects.link(base_stone_obj)

    # --- 2. Create a linear array of varied stones ---
    stone_array = []
    
    # The effective width of a single stone after scaling
    # We want the bend modifier to form a circle around 0,0,0
    # So stones need to be offset from 0,0,0 along X.
    # The length of the array will define the circumference if bent into a circle
    # Let's target the mid-point of the first stone at (bend_radius, 0, 0)
    # The bend radius will be length_of_array / (2 * pi) approximately.
    # To simplify, we will just place them sequentially and the modifier handles the bend.
    
    current_pos_x = 0
    # Average width of stone along X (for positioning)
    avg_stone_width_x = base_stone_dims[0] 

    for i in range(num_stones_per_layer):
        # Create a new stone by duplicating the template
        new_stone = base_stone_obj.copy()
        new_stone.data = base_stone_obj.data.copy() # Make data unique
        new_stone.name = f"IndividualStone_{i:02d}"
        well_collection.objects.link(new_stone)
        
        # Apply random scale and rotation for variation
        new_stone.scale = (
            random.uniform(0.9, 1.1), # Scale factor applied to already applied base_stone_dims
            random.uniform(0.9, 1.1),
            random.uniform(0.9, 1.1)
        )
        new_stone.rotation_euler.z = math.radians(random.uniform(-15, 15)) # Rotate around Z
        new_stone.rotation_euler.x = math.radians(random.uniform(-5, 5))   # Rotate around X
        new_stone.rotation_euler.y = math.radians(random.uniform(-5, 5))   # Rotate around Y

        # Position stones along X-axis, slightly overlapping
        new_stone.location.x = current_pos_x
        new_stone.location.y = random.uniform(-0.02, 0.02) # Small random Y offset
        new_stone.location.z = base_stone_dims[2] / 2 + random.uniform(-0.02, 0.02) # Random Z for slight wobble above ground
        
        # Apply transforms to make scale/rotation part of the mesh data
        bpy.context.view_layer.objects.active = new_stone
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        stone_array.append(new_stone)

        # Update position for next stone. Use current stone's actual X dimension.
        # Account for potential irregular scale in X
        current_stone_max_x = new_stone.dimensions.x / 2
        next_stone_min_x = base_stone_dims[0] / 2 * (1 - random.uniform(0.1, 0.2)) # Slight overlap
        
        current_pos_x += current_stone_max_x + next_stone_min_x - (random.uniform(0.01, 0.05) * avg_stone_width_x)
        
    # Select all created stones, making the first one active for correct origin after join
    bpy.ops.object.select_all(action='DESELECT')
    for stone in stone_array:
        stone.select_set(True)
    bpy.context.view_layer.objects.active = stone_array[0] # Make the first stone active for origin

    # Join stones into a single object
    bpy.ops.object.join()
    joined_stones_obj = bpy.context.object
    joined_stones_obj.name = f"{object_name}_Layer_0_Linear"

    # --- 3. Apply Simple Deform Modifier (Bend) to form a ring ---
    # The origin of `joined_stones_obj` is still at the original location of the first stone (around 0,0,0)
    # The stone array extends along the X-axis. Bending around Z will form a circle in XY plane.
    deform_mod = joined_stones_obj.modifiers.new(name="SimpleDeform_Bend", type='SIMPLE_DEFORM')
    deform_mod.deform_method = 'BEND'
    deform_mod.deform_axis = 'Z' # Bend around the Z-axis
    deform_mod.angle = math.radians(360.0)

    # Apply the modifier
    bpy.context.view_layer.objects.active = joined_stones_obj
    bpy.ops.object.modifier_apply(modifier=deform_mod.name)
    joined_stones_obj.name = f"{object_name}_Layer_0_Ring"

    # --- 4. Stack and modify layers ---
    well_base_layers = [joined_stones_obj]

    # Save current pivot point and set to 3D cursor
    original_pivot_point = bpy.context.scene.tool_settings.transform_pivot_point
    bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
    bpy.context.scene.cursor.location = (0,0,0) # Ensure 3D cursor is at world origin

    for i in range(1, num_layers):
        # Duplicate previous layer
        new_layer_obj = well_base_layers[-1].copy()
        new_layer_obj.data = well_base_layers[-1].data.copy()
        new_layer_obj.name = f"{object_name}_Layer_{i}_Ring"
        well_collection.objects.link(new_layer_obj)

        # Move up
        new_layer_obj.location.z = well_base_layers[-1].location.z + (base_stone_dims[2] * layer_offset_z_factor) * scale
        
        # Rotate around Z for offset stones
        new_layer_obj.rotation_euler.z += math.radians(random.uniform(15, 45)) # Cumulative random rotation
        
        # Scale for tapering effect (scale in XY, keep Z scale for height consistency relative to layer_offset_z)
        current_taper_scale = layer_taper_scale_factor**i
        new_layer_obj.scale = (current_taper_scale, current_taper_scale, 1.0)
        
        # Apply transforms
        bpy.context.view_layer.objects.active = new_layer_obj
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        # Add Decimate modifier for more jagged look
        decimate_mod = new_layer_obj.modifiers.new(name="Decimate", type='DECIMATE')
        decimate_mod.decimate_type = 'COLLAPSE'
        decimate_mod.ratio = decimate_ratio 
        
        well_base_layers.append(new_layer_obj)
    
    # Reset pivot point
    bpy.context.scene.tool_settings.transform_pivot_point = original_pivot_point
    
    # Select all layers and join them into a final single object
    bpy.ops.object.select_all(action='DESELECT')
    for layer_obj in well_base_layers:
        layer_obj.select_set(True)
    bpy.context.view_layer.objects.active = well_base_layers[0] # Make the first layer active again
    bpy.ops.object.join()
    final_well_obj = bpy.context.object
    final_well_obj.name = object_name
    
    # Apply final global location and scale
    final_well_obj.location = Vector(location)
    final_well_obj.scale = (scale, scale, scale)
    
    # Clean up: Ensure all original objects are moved to spares and new objects are in well_collection
    # The final_well_obj is already in well_collection
    for obj in bpy.data.objects:
        if obj.name.startswith("IndividualStone_") or obj.name == "BaseStoneTemplate":
            if obj.users_collection and obj.users_collection[0] != spares_collection:
                 # Unlink from any other collections (e.g. well_collection if not handled by join)
                for coll in obj.users_collection:
                    if coll != spares_collection:
                        coll.objects.unlink(obj)
                spares_collection.objects.link(obj)

    return f"Created '{object_name}' at {location} with {num_layers} layers."
