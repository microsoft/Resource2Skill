def create_low_poly_well_base(
    scene_name: str = "Scene",
    object_name: str = "LowPolyWellBase",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    stone_material_color: tuple = (0.6, 0.6, 0.6), # Grey default
    num_stones_per_layer: int = 12,
    num_layers: int = 4,
    layer_height_factor: float = 1.0, # Multiplier for average stone height
    base_layer_scale_factor: float = 1.0, # Scale of the outermost (bottom) layer
    top_layer_scale_factor: float = 0.8, # Relative scale factor for the innermost (top) layer
    decimate_ratio: float = 0.37,
    bevel_amount: float = 0.05,
    bevel_segments: int = 1,
    randomize_amount: float = 0.001,
    **kwargs,
) -> str:
    """
    Create a stylized low-poly well base with stacked circular stone layers.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created well base object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the entire well base.
        stone_material_color: (R, G, B) base color in 0-1 range for stones.
        num_stones_per_layer: Number of individual stone segments in each circular layer.
        num_layers: Number of stacked circular layers.
        layer_height_factor: Multiplier for average stone height to determine vertical spacing.
        base_layer_scale_factor: Scale factor for the innermost (bottom) layer.
        top_layer_scale_factor: Relative scale factor for the outermost (top) layer.
        decimate_ratio: Ratio for the decimate modifier (0.0 to 1.0).
        bevel_amount: Bevel amount for individual stone edges.
        bevel_segments: Number of segments for the bevel.
        randomize_amount: Amount for vertex randomization in individual stones.
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'LowPolyWellBase' at (0, 0, 0) with 4 layers"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import random
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Ensure 3D cursor is at world origin for consistent pivot operations
    scene.cursor.location = (0.0, 0.0, 0.0)

    # --- 1. Create multiple reference stone variants ---
    stone_initial_scale = kwargs.get('initial_stone_scale', 0.181)
    stone_x_stretch = kwargs.get('stone_x_stretch', 2.190)

    # Reference stone 1: Long, default-like
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0,0,0))
    ref_stone_1 = bpy.context.active_object
    ref_stone_1.name = "Ref_Stone_01"
    ref_stone_1.scale = (stone_initial_scale * stone_x_stretch, stone_initial_scale, stone_initial_scale)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    bpy.ops.object.mode_set(mode='EDIT')
    bm_1 = bmesh.from_edit_mesh(ref_stone_1.data)
    for edge in bm_1.edges: edge.select = True
    bmesh.ops.bevel(bm_1, geom=bm_1.edges, offset=bevel_amount, segments=bevel_segments)
    
    # Add loop cuts for more detail to randomize
    bmesh.ops.subdivide_edges(bm_1, edges=[e for e in bm_1.edges if e.normal.x == 0 and e.normal.y == 0], cuts=1) # Z-axis (horizontal)
    bmesh.ops.subdivide_edges(bm_1, edges=[e for e in bm_1.edges if e.normal.y == 0 and e.normal.z == 0], cuts=2) # X-axis (vertical along length)
    bmesh.ops.subdivide_edges(bm_1, edges=[e for e in bm_1.edges if e.normal.x == 0 and e.normal.z == 0], cuts=2) # Y-axis (vertical across width)
    
    for vert in bm_1.verts: vert.select = True
    bpy.ops.mesh.vertices_randomize(amount=randomize_amount)
    bmesh.update_edit_mesh(ref_stone_1.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Reference stone 2: Shorter, rotated
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'})
    ref_stone_2 = bpy.context.active_object
    ref_stone_2.name = "Ref_Stone_02"
    bpy.ops.object.mode_set(mode='EDIT')
    bm_2 = bmesh.from_edit_mesh(ref_stone_2.data)
    for vert in bm_2.verts: vert.select = True
    bpy.ops.transform.resize(value=(0.7, 1, 1), orient_type='GLOBAL')
    bpy.ops.mesh.vertices_randomize(amount=randomize_amount)
    bmesh.update_edit_mesh(ref_stone_2.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    ref_stone_2.rotation_euler.x = math.radians(random.uniform(80, 100)) # Randomize rotation slightly around 90
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

    # Reference stone 3: Squarer, rotated
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'})
    ref_stone_3 = bpy.context.active_object
    ref_stone_3.name = "Ref_Stone_03"
    bpy.ops.object.mode_set(mode='EDIT')
    bm_3 = bmesh.from_edit_mesh(ref_stone_3.data)
    for vert in bm_3.verts: vert.select = True
    bpy.ops.transform.resize(value=(0.5, 1, 0.8), orient_type='GLOBAL')
    bpy.ops.mesh.vertices_randomize(amount=randomize_amount)
    bmesh.update_edit_mesh(bm_3) # Corrected to update bm_3
    bpy.ops.object.mode_set(mode='OBJECT')
    ref_stone_3.rotation_euler.y = math.radians(random.uniform(80, 100))
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

    stone_variants = [ref_stone_1, ref_stone_2, ref_stone_3]

    # Hide reference stones in a collection
    ref_stones_collection = bpy.data.collections.new(f"{object_name}_Stone_Refs")
    scene.collection.children.link(ref_stones_collection)
    for stone_obj in stone_variants:
        scene.collection.objects.unlink(stone_obj)
        ref_stones_collection.objects.link(stone_obj)
    ref_stones_collection.hide_viewport = True
    ref_stones_collection.hide_render = True

    # --- 2. Create the linear arrangement of stones ---
    active_objects_for_join = []
    current_x_offset = 0
    
    bpy.ops.object.select_all(action='DESELECT')

    for i in range(num_stones_per_layer):
        chosen_variant = random.choice(stone_variants)
        bpy.context.view_layer.objects.active = chosen_variant
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'})
        new_stone = bpy.context.active_object
        new_stone.name = f"{object_name}_Segment_{i:02d}"
        
        new_stone.location.x = current_x_offset 
        current_x_offset += new_stone.dimensions.x * 0.95 # Slight overlap

        # Apply local rotations for variety
        new_stone.rotation_euler.z = math.radians(random.uniform(-5, 5))
        new_stone.rotation_euler.y = math.radians(random.uniform(-5, 5))
        new_stone.rotation_euler.x = math.radians(random.uniform(-5, 5))
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        active_objects_for_join.append(new_stone)
        new_stone.select_set(True)

    if not active_objects_for_join:
        return "Failed to create any stone segments for the well base."

    # Set the first object in the line as active for joining (so its origin is used)
    bpy.context.view_layer.objects.active = active_objects_for_join[0]
    bpy.ops.object.join()
    joined_line_obj = bpy.context.active_object
    joined_line_obj.name = f"{object_name}_Linear_Joined"

    # --- 3. Apply Simple Deform modifier to bend into a circle ---
    simple_deform_mod = joined_line_obj.modifiers.new(name="SimpleDeform", type='SIMPLE_DEFORM')
    simple_deform_mod.deform_method = 'BEND'
    simple_deform_mod.deform_axis = 'Z'
    simple_deform_mod.angle = math.radians(360)
    
    # --- 4. Stack and vary circular layers ---
    well_layers = []
    
    # Get the average Z dimension of the original reference stones for consistent stacking height
    avg_stone_thickness_z = ref_stone_1.dimensions.z 
    
    # Create the parent empty first
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=location)
    parent_empty = bpy.context.active_object
    parent_empty.name = object_name
    parent_empty.scale = (scale, scale, scale) # Apply overall scale to parent

    for i in range(num_layers):
        # Duplicate the base bent line (which has SimpleDeform modifier)
        bpy.ops.object.select_all(action='DESELECT')
        joined_line_obj.select_set(True)
        bpy.context.view_layer.objects.active = joined_line_obj
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'})
        new_layer = bpy.context.active_object
        new_layer.name = f"{object_name}_Layer_{i:02d}"
        
        # Calculate individual layer scale for tapering
        taper_interpolation = i / (num_layers - 1) if num_layers > 1 else 0
        layer_current_scale = base_layer_scale_factor - taper_interpolation * (base_layer_scale_factor - top_layer_scale_factor)
        
        new_layer.scale = (layer_current_scale, layer_current_scale, 1) # Apply local scale for tapering

        # Position new layer vertically (relative to parent)
        new_layer.location.z = i * avg_stone_thickness_z * layer_height_factor
        
        # Randomize rotation around Z for varied brick placement
        new_layer.rotation_euler.z = math.radians(random.uniform(i * 15, i * 45)) 
        
        # Optionally add Decimate modifier for more jaggedness
        if i == 0 or i == num_layers -1 or (num_layers > 2 and i == 2): # Example: apply to bottom, top, and third layer
             decimate_mod = new_layer.modifiers.new(name=f"Decimate_Layer_{i:02d}", type='DECIMATE')
             decimate_mod.decimate_type = 'COLLAPSE'
             decimate_mod.ratio = decimate_ratio

        well_layers.append(new_layer)
        new_layer.select_set(True)
        new_layer.parent = parent_empty # Parent to the main empty

    # Delete the original joined_line (not needed after duplicating)
    bpy.data.objects.remove(joined_line_obj, do_unlink=True)
    
    # --- 5. Apply Material ---
    stone_mat = bpy.data.materials.new(name=f"{object_name}_Material")
    stone_mat.use_nodes = True
    bsdf = stone_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*stone_material_color, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.7 
    
    for layer in well_layers:
        if layer.data.materials:
            layer.data.materials[0] = stone_mat
        else:
            layer.data.materials.append(stone_mat)

    return f"Created '{object_name}' at {location} with {num_layers} layers."
