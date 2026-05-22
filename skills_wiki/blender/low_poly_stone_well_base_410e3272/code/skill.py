def create_low_poly_well_base(
    scene_name: str = "Scene",
    object_name_prefix: str = "WellStone",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    base_color_rgb: tuple = (0.5, 0.5, 0.5), 
    decimate_ratio: float = 0.375,
    num_layers: int = 4, 
    layer_taper_scale: float = 0.92, 
    layer_stack_overlap_factor: float = 0.8, 
    layer_z_rotation_degrees: float = 22.5, 
    stones_per_ring: int = 12, 
    **kwargs,
) -> str:
    """
    Create a low-poly well base with modular stones in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name_prefix: Prefix for the created stone objects.
        location: (x, y, z) world-space position for the overall well.
        scale: Uniform scale factor for the entire well.
        base_color_rgb: (R, G, B) base color in 0-1 range for the stones.
        decimate_ratio: Ratio for the decimate modifier (0 to 1). Lower = more jagged.
        num_layers: Number of stacked circular layers for the well.
        layer_taper_scale: Scale factor for successive layers (e.g., 0.9 for tapering).
        layer_stack_overlap_factor: Z-axis stacking factor (1.0 for no overlap, <1.0 for overlap).
        layer_z_rotation_degrees: Rotation around Z for each stacked layer.
        stones_per_ring: Number of individual stone objects to form one circular layer.
        **kwargs: Additional overrides (e.g., stone_bevel_offset, stone_randomize_amount).

    Returns:
        Status string, e.g., "Created 'WellStone_Base_Parent' at (0, 0, 0) with multiple objects"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math
    import random 

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Create Material ---
    material = bpy.data.materials.new(name=f"{object_name_prefix}_Material")
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (base_color_rgb[0], base_color_rgb[1], base_color_rgb[2], 1.0)
    bsdf.inputs["Roughness"].default_value = kwargs.get('material_roughness', 0.7)
    bsdf.inputs["Specular"].default_value = kwargs.get('material_specular', 0.2)

    # --- Helper function to create a single stone template ---
    def create_single_stone_template(stone_name, initial_dims, bevel_offset, randomize_amount):
        bpy.ops.mesh.primitive_cube_add(
            size=2, # Default cube size is 2m, scaled relative to this
            enter_editmode=False, 
            align='WORLD', 
            location=(0,0,0)
        )
        obj = bpy.context.object
        obj.name = stone_name

        # Scale to target dimensions, then apply
        obj.scale.x = initial_dims[0] / 2
        obj.scale.y = initial_dims[1] / 2
        obj.scale.z = initial_dims[2] / 2
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Set origin to bottom center for easier stacking
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY_WITH_PROJECTION') # Origin at bottom center
        obj.location.z = 0 # Ensure base is on Z=0

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Bevel all edges
        bpy.ops.mesh.bevel(offset=bevel_offset, segments=1, profile=0.5, affect='EDGES', clamp_overlap=True)

        # Add loop cuts for randomization (using default behavior for variety as in video)
        # The specific 'object_index' for loopcut_slide determines which edge to make the cut on.
        # For general randomization, simply adding cuts on various axes is typical.
        bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut_slide={"number_cuts":2}) # 2 cuts on one axis
        bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut_slide={"number_cuts":1}) # 1 cut on another axis
        bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut_slide={"number_cuts":1}) # 1 cut on the third axis

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.randomize(factor=randomize_amount, normal=0)

        bmesh.update_edit_mesh(obj.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        obj.data.materials.append(material)
        return obj

    # --- Create initial stone templates based on video ---
    stone_bevel_offset = kwargs.get('stone_bevel_offset', 0.04)
    stone_randomize_amount = kwargs.get('stone_randomize_amount', 0.005) 

    # Template 1 (long, basic, matches video's first stone)
    template1_dims = (0.76, 0.381, 0.381) 
    template_stone1 = create_single_stone_template(f"{object_name_prefix}_Template_01", template1_dims, 
                                                 bevel_offset=stone_bevel_offset, 
                                                 randomize_amount=stone_randomize_amount)
    
    # Template 2 (shorter, slightly rotated in X, visual match for video's second stone)
    bpy.context.view_layer.objects.active = template_stone1 
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={'linked':False, 'mode':'DUMMY'}, TRANSFORM_OT_translate={'value':(template1_dims[0] + 0.1, 0, 0)})
    template_stone2 = bpy.context.object
    template_stone2.name = f"{object_name_prefix}_Template_02"
    template_stone2.scale.x *= 0.6 # Make it shorter
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    template_stone2.rotation_euler.x = math.radians(kwargs.get('template2_rot_x', 90)) # Rotate around X
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY_WITH_PROJECTION') # Recenter origin
    template_stone2.location.z = 0 # Ensure base is on Z=0

    # Template 3 (small, squarish, slightly rotated in Y, visual match for video's third stone)
    bpy.context.view_layer.objects.active = template_stone1 
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={'linked':False, 'mode':'DUMMY'}, TRANSFORM_OT_translate={'value':(template1_dims[0] + 0.1 + template_stone2.dimensions.x + 0.1, 0, 0)})
    template_stone3 = bpy.context.object
    template_stone3.name = f"{object_name_prefix}_Template_03"
    template_stone3.scale.x *= kwargs.get('template3_scale_x', 0.4) 
    template_stone3.scale.y *= kwargs.get('template3_scale_y', 0.8) 
    template_stone3.scale.z *= kwargs.get('template3_scale_z', 0.5) 
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    template_stone3.rotation_euler.y = math.radians(kwargs.get('template3_rot_y', 90)) # Rotate around Y
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY_WITH_PROJECTION') 
    template_stone3.location.z = 0 

    templates = [template_stone1, template_stone2, template_stone3]

    # --- Assemble a long line of stones ---
    all_line_stones = []
    x_current_pos = 0

    for i in range(stones_per_ring): 
        template_idx = i % len(templates) 
        stone_template = templates[template_idx]
        
        bpy.context.view_layer.objects.active = stone_template
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={'linked':False, 'mode':'DUMMY'}, TRANSFORM_OT_translate={'value':(x_current_pos, 0, 0)})
        duplicated_stone = bpy.context.object
        duplicated_stone.name = f"{object_name_prefix}_LineStone_{i}"
        
        # Randomize rotation and slight position for more variety on duplicated instances
        duplicated_stone.rotation_euler.z = math.radians(random.uniform(-5, 5))
        duplicated_stone.location.y += random.uniform(-0.01, 0.01)
        duplicated_stone.location.z += random.uniform(-0.01, 0.01)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False) 

        all_line_stones.append(duplicated_stone)
        x_current_pos += duplicated_stone.dimensions.x * kwargs.get('stone_overlap_factor', 0.9) 

    # --- Move original templates to a hidden collection ---
    original_collection_name = f"{object_name_prefix}_Templates"
    if original_collection_name not in bpy.data.collections:
        original_collection = bpy.data.collections.new(original_collection_name)
        scene.collection.children.link(original_collection)
    else:
        original_collection = bpy.data.collections[original_collection_name]

    for stone_obj in templates:
        # Unlink from current collection (usually "Collection")
        if bpy.data.collections.get('Collection') and stone_obj in bpy.data.collections['Collection'].objects:
             bpy.data.collections['Collection'].objects.unlink(stone_obj)
        if stone_obj not in original_collection.objects: 
            original_collection.objects.link(stone_obj)
        stone_obj.hide_set(True) 
        stone_obj.hide_render = True 

    # --- Join all line stones ---
    if not all_line_stones:
        return "No stones created to form well base."
        
    bpy.context.view_layer.objects.active = all_line_stones[0]
    bpy.ops.object.select_all(action='DESELECT') 
    for obj in all_line_stones:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = all_line_stones[0] 
    bpy.ops.object.join()
    joined_line_obj = bpy.context.object
    joined_line_obj.name = f"{object_name_prefix}_JoinedLine"
    
    # --- Add Simple Deform (Bend) modifier ---
    bend_mod = joined_line_obj.modifiers.new(name="SimpleDeform_Bend", type='SIMPLE_DEFORM')
    bend_mod.deform_method = 'BEND'
    bend_mod.deform_axis = 'Z' 
    bend_mod.angle = math.radians(360) 
    
    bpy.context.view_layer.objects.active = joined_line_obj
    bpy.ops.object.modifier_apply(modifier=bend_mod.name) 

    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY_WITH_PROJECTION') 
    joined_line_obj.location.z = 0 # Ensure base is on Z=0

    # --- Stack and modify layers ---
    well_layers = []
    
    first_layer_obj = joined_line_obj
    # Apply initial overall scale to the first layer's dimensions
    first_layer_obj.scale = (scale, scale, scale) 
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True) 
    well_layers.append(first_layer_obj) 

    # current_stack_z tracks the Z position of the base of the current stack
    current_stack_z = 0.0 
    
    # Set 3D cursor to global origin (0,0,0) for consistent rotation pivot
    scene.cursor.location = Vector((0,0,0))
    bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
    
    for i in range(1, num_layers):
        bpy.context.view_layer.objects.active = well_layers[-1] 
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={'linked':False, 'mode':'DUMMY'}, TRANSFORM_OT_translate={'value':(0, 0, 0)})
        new_layer = bpy.context.object
        new_layer.name = f"{object_name_prefix}_Layer_{i+1}"
        
        # Calculate new Z position based on previous layer's top and overlap factor
        current_stack_z = well_layers[-1].location.z + (well_layers[-1].dimensions.z * layer_stack_overlap_factor)
        new_layer.location.z = current_stack_z
        
        # Scale down slightly for tapering
        current_layer_scale_factor = scale * (layer_taper_scale ** i)
        new_layer.scale = (current_layer_scale_factor, current_layer_scale_factor, current_layer_scale_factor)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True) 
        
        # Rotate around Z-axis at 3D cursor
        new_layer.rotation_euler.z = math.radians(i * layer_z_rotation_degrees)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False) 
        
        well_layers.append(new_layer)
        
    # --- Add Decimate modifier to all layers ---
    for layer_obj in well_layers:
        decimate_mod = layer_obj.modifiers.new(name=f"Decimate_{layer_obj.name}", type='DECIMATE')
        decimate_mod.decimate_type = 'COLLAPSE'
        decimate_mod.ratio = decimate_ratio

    # --- Restore pivot point ---
    bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'

    # --- Parent all layers to an empty for overall control ---
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0)) # Create empty at origin
    parent_empty = bpy.context.object
    parent_empty.name = f"{object_name_prefix}_Base_Parent"
    
    bpy.context.view_layer.objects.active = parent_empty
    bpy.ops.object.select_all(action='DESELECT')
    for layer_obj in well_layers:
        layer_obj.select_set(True)
    parent_empty.select_set(True)
    bpy.context.view_layer.objects.active = parent_empty 
    bpy.ops.object.parent_set(type='OBJECT')

    # Apply the overall `location` to the parent empty
    parent_empty.location = Vector(location)

    return f"Created '{parent_empty.name}' at {location} with {len(well_layers)} stone layers."
