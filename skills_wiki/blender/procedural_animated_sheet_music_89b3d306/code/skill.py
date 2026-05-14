def create_object(
    scene_name: str = "Scene",
    object_name: str = "SheetMusic",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    line_color: tuple = (1.0, 0.769, 0.0), # Shiny gold
    note_color: tuple = (0.0, 0.0, 0.0), # Matte black
    **kwargs,
) -> str:
    """
    Create a procedural animated sheet music generator using Geometry Nodes.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created BezierCurve object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        line_color: (R, G, B) base color for the lines in 0-1 range.
        note_color: (R, G, B) base color for the notes in 0-1 range.
        **kwargs: Additional overrides for Geometry Node parameters.

    Returns:
        Status string, e.g., "Created 'SheetMusic' at (0, 0, 0) with 2 materials."
    """
    import bpy
    import bmesh
    from mathutils import Vector, Euler
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 1. Create Base Bezier Curve ---
    bpy.ops.curve.primitive_bezier_curve_add(
        enter_editmode=False, align='WORLD',
        location=location,
        rotation=(0, 0, 0),
        scale=(scale, scale, scale)
    )
    sheet_music_obj = bpy.context.active_object
    sheet_music_obj.name = object_name
    sheet_music_obj.data.name = f"{object_name}_Curve"

    # --- 2. Create Placeholder Note Models (as a collection) ---
    note_collection_name = f"{object_name}_Notes"
    note_collection = bpy.data.collections.get(note_collection_name)
    if not note_collection:
        note_collection = bpy.data.collections.new(note_collection_name)
        scene.collection.children.link(note_collection)
    
    # Simple cube as a note placeholder
    bpy.ops.mesh.primitive_cube_add(size=0.1, enter_editmode=False, location=(0,0,0))
    note1_obj = bpy.context.active_object
    note1_obj.name = f"{object_name}_Note1"
    bpy.ops.object.move_to_collection(collection_index=note_collection.index)
    
    # Simple sphere as another note placeholder
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.07, subdivisions=2, enter_editmode=False, location=(0,0,0))
    note2_obj = bpy.context.active_object
    note2_obj.name = f"{object_name}_Note2"
    bpy.ops.object.move_to_collection(collection_index=note_collection.index)

    # Hide note collection (only instances will be visible)
    note_collection.hide_viewport = True
    note_collection.hide_render = True

    # --- 3. Create Materials ---
    line_mat_name = f"{object_name}_LineMaterial"
    line_mat = bpy.data.materials.get(line_mat_name)
    if not line_mat:
        line_mat = bpy.data.materials.new(name=line_mat_name)
        line_mat.use_nodes = True
        bsdf = line_mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (line_color[0], line_color[1], line_color[2], 1.0)
        bsdf.inputs["Metallic"].default_value = 1.0
        bsdf.inputs["Roughness"].default_value = 0.222

    note_mat_name = f"{object_name}_NoteMaterial"
    note_mat = bpy.data.materials.get(note_mat_name)
    if not note_mat:
        note_mat = bpy.data.materials.new(name=note_mat_name)
        note_mat.use_nodes = True
        bsdf = note_mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (note_color[0], note_color[1], note_color[2], 1.0)
        bsdf.inputs["Metallic"].default_value = 0.0
        bsdf.inputs["Roughness"].default_value = 0.927
    
    # Ensure active object is selected
    bpy.context.view_layer.objects.active = sheet_music_obj
    sheet_music_obj.select_set(True)

    # --- 4. Add Geometry Nodes Modifier ---
    gn_modifier_name = f"{object_name}_GeoNodes"
    gn_modifier = sheet_music_obj.modifiers.new(name=gn_modifier_name, type='NODES')
    
    gn_tree_name = f"{object_name}_SheetMusicGN"
    gn_tree = bpy.data.node_groups.new(name=gn_tree_name, type='GeometryNodeTree')
    gn_modifier.node_group = gn_tree

    # --- 5. Build Geometry Node Tree ---
    nodes = gn_tree.nodes
    links = gn_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Input and Output nodes
    group_input = nodes.new(type='NodeGroupInput')
    group_input.location = (-1000, 0)
    group_output = nodes.new(type='NodeGroupOutput')
    group_output.location = (1000, 0)

    # Add custom inputs to Group Input
    gn_tree.inputs.new('NodeSocketFloat', 'Line Spacing').default_value = 0.072
    gn_tree.inputs.new('NodeSocketFloat', 'Curve Resolution').default_value = 0.18
    gn_tree.inputs.new('NodeSocketInt', 'Lines Resolution').default_value = 32
    gn_tree.inputs.new('NodeSocketFloat', 'Line Radius').default_value = 0.016
    gn_tree.inputs.new('NodeSocketFloat', 'Trim Start').default_value = 0.0
    gn_tree.inputs.new('NodeSocketFloat', 'Trim End').default_value = 1.0
    gn_tree.inputs.new('NodeSocketFloat', 'Note Spacing').default_value = 0.83
    gn_tree.inputs.new('NodeSocketFloat', 'Start Offset').default_value = 0.555
    gn_tree.inputs.new('NodeSocketFloat', 'End Offset').default_value = -1.323
    gn_tree.inputs.new('NodeSocketFloat', 'Expand Start').default_value = 1.157
    gn_tree.inputs.new('NodeSocketFloat', 'Expand End').default_value = 2.258
    gn_tree.inputs.new('NodeSocketFloat', 'Expand Both').default_value = 1.870
    gn_tree.inputs.new('NodeSocketFloat', 'Note Scale').default_value = 0.651
    gn_tree.inputs.new('NodeSocketFloat', 'Fly Offset').default_value = 0.175
    gn_tree.inputs.new('NodeSocketFloat', 'Fly Intensity').default_value = 0.940
    gn_tree.inputs.new('NodeSocketFloat', 'Note Height').default_value = 0.246
    gn_tree.inputs.new('NodeSocketInt', 'Note Seed').default_value = 0

    # --- LINES GENERATION ---
    # Node: Resample Curve (for uniform points)
    resample_curve_main = nodes.new(type='GeometryNodeResampleCurve')
    resample_curve_main.location = (-700, 200)
    resample_curve_main.inputs['Count'].default_value = 100 # Default, will be overridden
    resample_curve_main.mode = 'LENGTH'
    links.new(group_input.outputs['Geometry'], resample_curve_main.inputs['Curve'])
    links.new(group_input.outputs['Curve Resolution'], resample_curve_main.inputs['Length'])
    
    # Duplicate & Offset Lines
    join_geometry_lines = nodes.new(type='GeometryNodeJoinGeometry')
    join_geometry_lines.location = (-300, 200)
    links.new(resample_curve_main.outputs['Curve'], join_geometry_lines.inputs['Geometry']) # Original line

    # 4 more lines, 2 positive Z, 2 negative Z offsets
    offset_values = [-2, -1, 1, 2] # Multipliers for line spacing
    current_y = 0

    for i, multiplier in enumerate(offset_values):
        transform_line = nodes.new(type='GeometryNodeTransform')
        transform_line.location = (-500, 200 - i * 100)
        
        combine_xyz_line = nodes.new(type='ShaderNodeCombineXYZ')
        combine_xyz_line.location = (-600, 200 - i * 100)
        
        multiply_line_spacing = nodes.new(type='ShaderNodeMath')
        multiply_line_spacing.operation = 'MULTIPLY'
        multiply_line_spacing.location = (-700, 200 - i * 100)
        links.new(group_input.outputs['Line Spacing'], multiply_line_spacing.inputs[0])
        multiply_line_spacing.inputs[1].default_value = multiplier / 2 # Adjust multiplier for finer control
        
        links.new(multiply_line_spacing.outputs['Value'], combine_xyz_line.inputs['Z'])
        links.new(combine_xyz_line.outputs['Vector'], transform_line.inputs['Translation'])
        links.new(resample_curve_main.outputs['Curve'], transform_line.inputs['Geometry'])
        links.new(transform_line.outputs['Geometry'], join_geometry_lines.inputs['Geometry'])

    # Convert lines to mesh and back for thickness and trimming
    curve_to_mesh_lines = nodes.new(type='GeometryNodeCurveToMesh')
    curve_to_mesh_lines.location = (-100, 200)
    links.new(join_geometry_lines.outputs['Geometry'], curve_to_mesh_lines.inputs['Curve'])

    curve_circle_profile = nodes.new(type='GeometryNodeCurvePrimitiveCircle')
    curve_circle_profile.location = (-300, 0)
    curve_circle_profile.inputs['Resolution'].default_value = 3 # Low res for small profile
    links.new(group_input.outputs['Line Radius'], curve_circle_profile.inputs['Radius'])
    links.new(curve_circle_profile.outputs['Curve'], curve_to_mesh_lines.inputs['Profile Curve'])

    merge_by_distance_lines = nodes.new(type='GeometryNodeMergeByDistance')
    merge_by_distance_lines.location = (0, 200)
    merge_by_distance_lines.inputs['Distance'].default_value = 0.001 # Small distance to merge points
    links.new(curve_to_mesh_lines.outputs['Mesh'], merge_by_distance_lines.inputs['Geometry'])

    mesh_to_curve_lines = nodes.new(type='GeometryNodeMeshToCurve')
    mesh_to_curve_lines.location = (100, 200)
    links.new(merge_by_distance_lines.outputs['Geometry'], mesh_to_curve_lines.inputs['Mesh'])
    
    # Set material for lines
    set_material_lines = nodes.new(type='GeometryNodeSetMaterial')
    set_material_lines.location = (200, 200)
    set_material_lines.inputs['Material'].default_value = line_mat
    links.new(mesh_to_curve_lines.outputs['Curve'], set_material_lines.inputs['Geometry'])


    # --- CURVE TRIMMING & TAPERING ---
    # Resample Curve (for uniform factor)
    resample_curve_factor = nodes.new(type='GeometryNodeResampleCurve')
    resample_curve_factor.location = (-700, -200)
    resample_curve_factor.mode = 'LENGTH'
    resample_curve_factor.inputs['Length'].default_value = 0.1 # High resolution for smooth curves
    links.new(group_input.outputs['Geometry'], resample_curve_factor.inputs['Curve'])

    # Capture Factor attribute
    store_factor = nodes.new(type='GeometryNodeStoreNamedAttribute')
    store_factor.location = (-600, -200)
    store_factor.data_type = 'FLOAT'
    store_factor.domain = 'POINT'
    store_factor.inputs['Name'].default_value = "trim"
    spline_parameter_factor = nodes.new(type='GeometryNodeInputSplineParameter')
    spline_parameter_factor.location = (-750, -300)
    links.new(spline_parameter_factor.outputs['Factor'], store_factor.inputs['Value'])
    links.new(resample_curve_factor.outputs['Curve'], store_factor.inputs['Geometry'])
    
    # Trim Curve
    trim_curve = nodes.new(type='GeometryNodeTrimCurve')
    trim_curve.location = (-500, -200)
    trim_curve.mode = 'FACTOR'
    links.new(store_factor.outputs['Geometry'], trim_curve.inputs['Curve'])
    links.new(group_input.outputs['Trim Start'], trim_curve.inputs['Start'])
    links.new(group_input.outputs['Trim End'], trim_curve.inputs['End'])

    # Tapering Thickness (using captured factor)
    set_curve_radius = nodes.new(type='GeometryNodeSetCurveRadius')
    set_curve_radius.location = (-300, -200)
    links.new(trim_curve.outputs['Curve'], set_curve_radius.inputs['Curve'])

    get_factor = nodes.new(type='GeometryNodeInputNamedAttribute')
    get_factor.location = (-600, -400)
    get_factor.data_type = 'FLOAT'
    get_factor.inputs['Name'].default_value = "trim" # Use the stored factor
    
    rgb_curves_taper = nodes.new(type='ShaderNodeRGBCurves')
    rgb_curves_taper.location = (-400, -400)
    rgb_curves_taper.mapping.clip_min_x = 0.0
    rgb_curves_taper.mapping.clip_min_y = 0.0
    rgb_curves_taper.mapping.clip_max_x = 1.0
    rgb_curves_taper.mapping.clip_max_y = 1.0
    rgb_curves_taper.mapping.use_clip = True
    
    # Create the 0-1-0 curve shape for tapering
    point1 = rgb_curves_taper.mapping.curves[0].points[0] # (0,0)
    point2 = rgb_curves_taper.mapping.curves[0].points[1] # (1,1)
    
    rgb_curves_taper.mapping.curves[0].points.new(0.5, 1.0)
    
    links.new(get_factor.outputs['Attribute'], rgb_curves_taper.inputs['Color'])
    links.new(rgb_curves_taper.outputs['Color'], set_curve_radius.inputs['Radius'])

    # Convert back to mesh for final render
    curve_to_mesh_final = nodes.new(type='GeometryNodeCurveToMesh')
    curve_to_mesh_final.location = (-100, -200)
    links.new(set_curve_radius.outputs['Curve'], curve_to_mesh_final.inputs['Curve'])
    links.new(curve_circle_profile.outputs['Curve'], curve_to_mesh_final.inputs['Profile Curve']) # Reuse profile curve

    # --- NOTES DISTRIBUTION & ANIMATION ---
    # Capture Curve Tilt and Tangent
    capture_tilt_tangent = nodes.new(type='GeometryNodeCaptureAttribute')
    capture_tilt_tangent.location = (-800, -500)
    capture_tilt_tangent.data_type = 'FLOAT' # Tilt is float (angle)
    capture_tilt_tangent.domain = 'POINT'
    
    curve_tilt_node = nodes.new(type='GeometryNodeInputCurveTilt')
    curve_tilt_node.location = (-950, -500)
    links.new(curve_tilt_node.outputs['Tilt'], capture_tilt_tangent.inputs['Value'])
    links.new(resample_curve_factor.outputs['Curve'], capture_tilt_tangent.inputs['Geometry'])

    capture_tangent = nodes.new(type='GeometryNodeCaptureAttribute')
    capture_tangent.location = (-800, -600)
    capture_tangent.data_type = 'VECTOR' # Tangent is vector
    capture_tangent.domain = 'POINT'

    curve_tangent_node = nodes.new(type='GeometryNodeInputCurveTangent')
    curve_tangent_node.location = (-950, -600)
    links.new(curve_tangent_node.outputs['Tangent'], capture_tangent.inputs['Value'])
    links.new(resample_curve_factor.outputs['Curve'], capture_tangent.inputs['Geometry'])


    # Set Position for Note Height & Fly Animation
    set_position_notes = nodes.new(type='GeometryNodeSetPosition')
    set_position_notes.location = (-200, -500)
    links.new(resample_curve_factor.outputs['Curve'], set_position_notes.inputs['Geometry']) # Original resampled curve for notes

    # Random Note Height (local Z)
    random_height = nodes.new(type='GeometryNodeRandomValue')
    random_height.location = (-700, -800)
    random_height.data_type = 'VECTOR'
    links.new(group_input.outputs['Note Height'], random_height.inputs['Max'].inputs[2]) # Z-max
    links.new(random_height.outputs['Value'], set_position_notes.inputs['Offset']) # Offset Z-axis locally

    # Node Fly Offset & Intensity
    # Calculate factor for flying out (inverse of trim end)
    subtract_trim_end = nodes.new(type='ShaderNodeMath')
    subtract_trim_end.operation = 'SUBTRACT'
    subtract_trim_end.location = (-700, -900)
    subtract_trim_end.inputs[0].default_value = 1.0 # 1 - trim_end
    links.new(group_input.outputs['Trim End'], subtract_trim_end.inputs[1])

    add_fly_offset = nodes.new(type='ShaderNodeMath')
    add_fly_offset.operation = 'ADD'
    add_fly_offset.location = (-600, -900)
    links.new(subtract_trim_end.outputs['Value'], add_fly_offset.inputs[0])
    links.new(group_input.outputs['Fly Offset'], add_fly_offset.inputs[1])

    multiply_fly_intensity = nodes.new(type='ShaderNodeMath')
    multiply_fly_intensity.operation = 'MULTIPLY'
    multiply_fly_intensity.location = (-500, -900)
    links.new(add_fly_offset.outputs['Value'], multiply_fly_intensity.inputs[0])
    links.new(group_input.outputs['Fly Intensity'], multiply_fly_intensity.inputs[1])

    # Convert to Vector to control Y-axis only
    combine_xyz_fly = nodes.new(type='ShaderNodeCombineXYZ')
    combine_xyz_fly.location = (-400, -900)
    links.new(multiply_fly_intensity.outputs['Value'], combine_xyz_fly.inputs['Y'])

    # Rotate the fly offset vector to align with curve tangent and tilt
    vector_rotate_fly = nodes.new(type='GeometryNodeVectorRotate')
    vector_rotate_fly.location = (-300, -900)
    vector_rotate_fly.rotation_type = 'AXIS_ANGLE'
    links.new(combine_xyz_fly.outputs['Vector'], vector_rotate_fly.inputs['Vector'])
    links.new(capture_tangent.outputs['Value'], vector_rotate_fly.inputs['Axis'])
    links.new(capture_tilt_tangent.outputs['Value'], vector_rotate_fly.inputs['Angle'])
    
    # Add flying offset to notes' position offset
    add_offset = nodes.new(type='ShaderNodeVectorMath')
    add_offset.operation = 'ADD'
    add_offset.location = (-100, -900)
    links.new(random_height.outputs['Value'], add_offset.inputs[0]) # Existing random height offset
    links.new(vector_rotate_fly.outputs['Vector'], add_offset.inputs[1]) # Add flying offset
    links.new(add_offset.outputs['Vector'], set_position_notes.inputs['Offset'])


    # Instance Notes
    instance_notes = nodes.new(type='GeometryNodeInstanceOnPoints')
    instance_notes.location = (0, -500)
    links.new(set_position_notes.outputs['Geometry'], instance_notes.inputs['Points'])

    collection_info_notes = nodes.new(type='GeometryNodeCollectionInfo')
    collection_info_notes.location = (-300, -700)
    collection_info_notes.inputs['Collection'].default_value = note_collection
    collection_info_notes.inputs['Separate Children'].default_value = True
    collection_info_notes.inputs['Pick Instance'].default_value = True
    collection_info_notes.inputs['Reset Children'].default_value = True
    links.new(collection_info_notes.outputs['Instances'], instance_notes.inputs['Instances'])
    
    random_seed_node = nodes.new(type='GeometryNodeRandomValue')
    random_seed_node.location = (-500, -700)
    random_seed_node.data_type = 'INT'
    random_seed_node.inputs['Min'].default_value = -10000
    random_seed_node.inputs['Max'].default_value = 10000
    links.new(group_input.outputs['Note Seed'], random_seed_node.inputs['Seed'])
    links.new(random_seed_node.outputs['Value'], instance_notes.inputs['Instance Index'])

    # Align Note Rotation to Curve Tangent and Tilt
    align_rotation_tangent = nodes.new(type='GeometryNodeAlignRotationToVector')
    align_rotation_tangent.location = (100, -500)
    align_rotation_tangent.axis = 'Y' # Assuming notes are oriented along Y by default
    links.new(capture_tangent.outputs['Value'], align_rotation_tangent.inputs['Vector'])
    links.new(align_rotation_tangent.outputs['Rotation'], instance_notes.inputs['Rotation'])

    # Scale Notes based on Trimming
    # Retrieve stored 'trim' factor
    get_trim_factor = nodes.new(type='GeometryNodeInputNamedAttribute')
    get_trim_factor.location = (-800, -1000)
    get_trim_factor.data_type = 'FLOAT'
    get_trim_factor.inputs['Name'].default_value = "trim"

    # Offset Trim Start (for scale band width)
    subtract_start_offset = nodes.new(type='ShaderNodeMath')
    subtract_start_offset.operation = 'SUBTRACT'
    subtract_start_offset.location = (-700, -1000)
    links.new(get_trim_factor.outputs['Attribute'], subtract_start_offset.inputs[0])
    links.new(group_input.outputs['Start Offset'], subtract_start_offset.inputs[1])

    # Map Range for Start Scaling
    map_range_start_scale = nodes.new(type='ShaderNodeMapRange')
    map_range_start_scale.location = (-500, -1000)
    map_range_start_scale.inputs['To Min'].default_value = 0.0
    map_range_start_scale.inputs['To Max'].default_value = 2.0 # Max scale
    links.new(subtract_start_offset.outputs['Value'], map_range_start_scale.inputs['Value'])
    links.new(group_input.outputs['Expand Start'], map_range_start_scale.inputs['From Max'])
    
    # Offset Trim End (for scale band width)
    subtract_end_offset = nodes.new(type='ShaderNodeMath')
    subtract_end_offset.operation = 'SUBTRACT'
    subtract_end_offset.location = (-700, -1100)
    links.new(get_trim_factor.outputs['Attribute'], subtract_end_offset.inputs[0])
    links.new(group_input.outputs['End Offset'], subtract_end_offset.inputs[1])

    # Map Range for End Scaling (inverted)
    map_range_end_scale = nodes.new(type='ShaderNodeMapRange')
    map_range_end_scale.location = (-500, -1100)
    map_range_end_scale.inputs['From Min'].default_value = 0.0
    map_range_end_scale.inputs['From Max'].default_value = 1.0 # Default factor range
    map_range_end_scale.inputs['To Min'].default_value = 2.0 # Max scale
    map_range_end_scale.inputs['To Max'].default_value = 0.0 # Min scale
    links.new(subtract_end_offset.outputs['Value'], map_range_end_scale.inputs['Value'])
    links.new(group_input.outputs['Expand End'], map_range_end_scale.inputs['From Min']) # Link to expand end

    # Combine (Multiply) Start and End Scaling
    multiply_scale = nodes.new(type='ShaderNodeMath')
    multiply_scale.operation = 'MULTIPLY'
    multiply_scale.location = (-300, -1050)
    links.new(map_range_start_scale.outputs['Result'], multiply_scale.inputs[0])
    links.new(map_range_end_scale.outputs['Result'], multiply_scale.inputs[1])

    # Apply overall Note Scale
    multiply_overall_scale = nodes.new(type='ShaderNodeMath')
    multiply_overall_scale.operation = 'MULTIPLY'
    multiply_overall_scale.location = (-100, -1050)
    links.new(multiply_scale.outputs['Result'], multiply_overall_scale.inputs[0])
    links.new(group_input.outputs['Note Scale'], multiply_overall_scale.inputs[1])
    links.new(multiply_overall_scale.outputs['Result'], instance_notes.inputs['Scale'])

    # Set material for notes
    set_material_notes = nodes.new(type='GeometryNodeSetMaterial')
    set_material_notes.location = (200, -500)
    set_material_notes.inputs['Material'].default_value = note_mat
    links.new(instance_notes.outputs['Instances'], set_material_notes.inputs['Geometry'])
    
    # --- FINAL OUTPUT ---
    final_join_geometry = nodes.new(type='GeometryNodeJoinGeometry')
    final_join_geometry.location = (500, 0)
    links.new(set_material_lines.outputs['Geometry'], final_join_geometry.inputs['Geometry'])
    links.new(set_material_notes.outputs['Geometry'], final_join_geometry.inputs['Geometry'])
    links.new(final_join_geometry.outputs['Geometry'], group_output.inputs['Geometry'])


    # --- Organize Nodes (optional, for clarity) ---
    def create_frame(nodes_to_frame, label, color):
        frame = nodes.new(type='NodeFrame')
        frame.label = label
        frame.label_size = 20
        frame.color = color
        for node in nodes_to_frame:
            node.parent = frame
        return frame

    # Colors for frames
    purple = (0.5, 0.2, 0.8, 1.0)
    green = (0.2, 0.8, 0.3, 1.0)
    blue = (0.1, 0.3, 0.7, 1.0)

    create_frame([resample_curve_main, join_geometry_lines, transform_line, combine_xyz_line, multiply_line_spacing,
                  curve_to_mesh_lines, curve_circle_profile, merge_by_distance_lines, mesh_to_curve_lines,
                  set_material_lines], "Lines Generation & Thickness", green)
    create_frame([store_factor, spline_parameter_factor, trim_curve, set_curve_radius, get_factor,
                  rgb_curves_taper, curve_to_mesh_final], "Curve Trimming & Tapering", purple)
    create_frame([capture_tilt_tangent, curve_tilt_node, capture_tangent, curve_tangent_node, set_position_notes,
                  random_height, combine_xyz_fly, multiply_fly_intensity, add_fly_offset, vector_rotate_fly, add_offset,
                  instance_notes, collection_info_notes, random_seed_node, align_rotation_tangent,
                  get_trim_factor, subtract_start_offset, map_range_start_scale, subtract_end_offset,
                  map_range_end_scale, multiply_scale, multiply_overall_scale, set_material_notes], 
                 "Notes Distribution & Animation", blue)


    return f"Created '{object_name}' with Geometry Nodes."

