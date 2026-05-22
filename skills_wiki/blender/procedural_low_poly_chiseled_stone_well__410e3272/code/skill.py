def create_low_poly_well(
    scene_name: str = "Scene",
    object_name: str = "LowPolyWell",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.8, 0.8),
    num_layers: int = 3,
    num_stones_per_layer: int = 12,
    stone_template_scale: tuple = (0.38, 0.18, 0.18),  # Roughly 76cm x 36cm x 36cm in dimensions
    randomize_amount: float = 0.001,
    bevel_amount: float = 0.02,
    decimate_ratio: float = 0.37,
    layer_vertical_offset: float = 0.37, # Based on stone_template_scale[1]*2 approximately
    layer_rotation_variance: float = 20.0, # degrees
    layer_scale_variance: float = 0.05,
    **kwargs,
) -> str:
    """
    Create a low-poly chiseled stone well base in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created well base object.
        location: (x, y, z) world-space position for the final well base.
        scale: Uniform scale factor for the final well base (1.0 = default size).
        material_color: (R, G, B) base color for the stones in 0-1 range.
        num_layers: Number of stacked stone rings for the well base.
        num_stones_per_layer: Number of individual stones in each ring.
        stone_template_scale: (sx, sy, sz) scale for the initial rectangular stone.
        randomize_amount: Amount of randomization for stone vertices.
        bevel_amount: Amount for bevelling stone edges.
        decimate_ratio: Ratio for the Decimate modifier to reduce faces.
        layer_vertical_offset: Vertical distance between stacked layers.
        layer_rotation_variance: Max random Z rotation for each layer (degrees).
        layer_scale_variance: Max random uniform scale variance for each layer.
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'LowPolyWell' at (0, 0, 0) with 1 object"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math
    import random

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # Store original selection and mode
    original_selection = bpy.context.selected_objects[:]
    original_active_object = bpy.context.view_layer.objects.active
    original_mode = bpy.context.object.mode if bpy.context.object else None

    # Helper function to create a single chiseled stone
    def create_single_chiseled_stone(name, loc, sc, rot_eulers, loop_cuts, randomize_amt, bevel_amt):
        bpy.ops.mesh.primitive_cube_add(
            size=2,
            enter_editmode=False,
            align='WORLD',
            location=(0, 0, 0) # Create at origin, then move
        )
        obj = bpy.context.active_object
        obj.name = name

        # Scale to rectangular block
        obj.scale = (sc[0] / 2, sc[1] / 2, sc[2] / 2) # Cube is size=2, so divide scale by 2

        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        # Enter Edit Mode for bevelling, loop cuts, and randomization
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')

        # Bevel edges
        bpy.ops.mesh.bevel(offset=bevel_amt, segments=2, profile=0.5)

        # Add loop cuts
        bpy.ops.mesh.loopcut_slide(
            MESH_OT_loopcut_slide={"offset": 0, "edge_index": -1, "override_point": None, "normal_flip": False},
            NUMBER_OF_CUTS=loop_cuts
        )
        bpy.ops.mesh.loopcut_slide(
            MESH_OT_loopcut_slide={"offset": 0, "edge_index": -1, "override_point": None, "normal_flip": False},
            NUMBER_OF_CUTS=loop_cuts,
            AXIS_ROLL=math.radians(90) # Rotate loop cut axis
        )
        bpy.ops.mesh.loopcut_slide(
            MESH_OT_loopcut_slide={"offset": 0, "edge_index": -1, "override_point": None, "normal_flip": False},
            NUMBER_OF_CUTS=loop_cuts,
            AXIS_ROLL=math.radians(180) # Rotate loop cut axis again
        )

        # Randomize vertices
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.transform_randomize(
            offset=randomize_amt,
            normal=0,
            uniform=0,
            seed=random.randint(0, 1000)
        )
        bpy.ops.object.mode_set(mode='OBJECT')

        # Set final location and rotation for the individual stone instance
        obj.location = Vector(loc)
        obj.rotation_euler = (math.radians(rot_eulers[0]), math.radians(rot_eulers[1]), math.radians(rot_eulers[2]))

        return obj

    # Ensure 3D cursor is at world origin and set pivot point to 3D Cursor for later operations
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'

    all_layers = []

    # Calculate radius for the ring (sum of stone widths divided by 2pi)
    # The X dimension of a single stone is `stone_template_scale[0]`
    stone_length = stone_template_scale[0]
    ring_circumference = num_stones_per_layer * stone_length * 0.9 # Small overlap
    ring_radius = ring_circumference / (2 * math.pi)

    # Create individual layers
    for layer_idx in range(num_layers):
        stones_in_layer = []
        
        # Position stones for this layer along the X-axis
        for i in range(num_stones_per_layer):
            stone_name = f"TempStone_{layer_idx}_{i}"
            
            # Place stones along the X-axis such that the center of the total row is at (0,0,0)
            # This requires the first stone to be at -ring_radius, and then place subsequent stones
            # so the midpoint of the entire row is at 0.
            # The SimpleDeform modifier (Bend, Axis Z) needs the object's origin to be at the bend center.
            # If the object is aligned along X, its origin at (0,0,0) means it will bend around Z,
            # with the 'start' of the bend at -X and 'end' at +X forming a circle around the origin.
            
            # The original video's way: stones are laid out starting from origin.
            # Then SimpleDeform (Bend, Axis Z) curls it around.
            # Then the *whole ring* is rotated R X 90 to stand up.
            
            # Let's adjust positioning for the row to be centered on (0,0,0) for the bend.
            # Total length of the row without overlap is num_stones_per_layer * stone_length
            # To center it, start from -(total_length / 2)
            
            # However, the video's method uses the *object origin* as the bend point.
            # So if the combined object has its origin at the left end, it will bend from there.
            # The video starts with Cube at (0,0,0) and extends it along +X.
            # So the object origin *remains* at the start of the chain.
            # When bent around Z, the origin becomes the center of the circle on the XY plane.
            # Then rotating RX90 brings it upright. This actually works better.
            
            # So, position stones along X starting from 0, offset by its length/2 so its pivot point is at 0,0,0
            # then position it at the radius for the deformer to work
            
            # Simplified approach matching video: create stones starting from X=0 and extending in +X
            # Let's assume the well's circumference is formed by the total length of the stones.
            # To make the bend modifier work, the object's origin should be at the center of the ring.
            # If the total length of the linear stone arrangement is L, the radius of the resulting ring R = L / (2 * pi).
            # The object's origin needs to be placed at (-R, 0, 0) if the stones are created from 0 along +X and you want the ring centered at (0,0,0)
            
            # For this exercise, let's keep the object origin at (0,0,0) for the initial segment, and let SimpleDeform handle it.
            # The original video's stone arrangement is not centered before bend.
            # So, create stones starting from x=0 and extending along +x.
            # The initial location should be (stone_length / 2 + i * stone_length, 0, 0)
            # This makes the origin of the first stone at (0,0,0) if not explicitly centered.

            x_pos = (i * stone_length) + (stone_length / 2) # Center of each stone
            loc_stone = (x_pos, 0, 0)

            # Randomize individual stone rotation for more organic look
            rand_rot_z = random.uniform(-5, 5) # degrees
            rand_rot_y = random.uniform(-5, 5) # degrees

            stone_obj = create_single_chiseled_stone(
                stone_name,
                loc=loc_stone,
                sc=stone_template_scale,
                rot_eulers=(0, rand_rot_y, rand_rot_z), # Individual stone rotation
                loop_cuts=2,
                randomize_amt=randomize_amount,
                bevel_amt=bevel_amount
            )
            stones_in_layer.append(stone_obj)

        # Join stones into a single object for the layer
        if stones_in_layer:
            bpy.context.view_layer.objects.active = stones_in_layer[0]
            bpy.ops.object.select_all(action='DESELECT')
            for obj in stones_in_layer:
                obj.select_set(True)
            bpy.context.view_layer.objects.active = stones_in_layer[0] # Make sure one is active
            
            bpy.ops.object.join()
            layer_obj = bpy.context.active_object
            layer_obj.name = f"{object_name}_Layer_{layer_idx}_Segment"

            # Apply SimpleDeform modifier (Bend)
            simple_deform_mod = layer_obj.modifiers.new(name="SimpleDeform_Bend", type='SIMPLE_DEFORM')
            simple_deform_mod.deform_method = 'BEND'
            simple_deform_mod.axis = 'Z' # Bend around Z-axis (local)
            simple_deform_mod.angle = math.radians(360) # Full circle

            # Apply Decimate modifier (Planar)
            decimate_mod = layer_obj.modifiers.new(name="Decimate_Planar", type='DECIMATE')
            decimate_mod.decimate_type = 'COLLAPSE' # Or 'PLANAR' for more flat faces
            decimate_mod.ratio = decimate_ratio # Adjust this value for desired low-poly effect

            # Rotate the bent ring to stand upright (as in video)
            layer_obj.rotation_euler = (math.radians(90), 0, 0)
            
            # Apply modifiers for consistent geometry when stacking
            bpy.context.view_layer.objects.active = layer_obj
            bpy.ops.object.select_all(action='DESELECT')
            layer_obj.select_set(True)
            bpy.ops.object.modifier_apply(modifier=simple_deform_mod.name)
            bpy.ops.object.modifier_apply(modifier=decimate_mod.name)


            all_layers.append(layer_obj)
            
    # Stack and vary layers
    if all_layers:
        base_layer = all_layers[0]
        base_layer.location = (0, 0, 0) # Base layer is at world origin
        
        for i in range(1, num_layers):
            current_layer = all_layers[i]
            
            # Position layer vertically
            current_layer.location = (0, 0, layer_vertical_offset * i)
            
            # Add random rotation around Z and scale using 3D cursor as pivot
            rand_z_rot = random.uniform(-layer_rotation_variance, layer_rotation_variance)
            rand_scale = random.uniform(1 - layer_scale_variance, 1 + layer_scale_variance)
            
            current_layer.rotation_euler = (math.radians(90), 0, math.radians(rand_z_rot))
            current_layer.scale = (rand_scale, rand_scale, rand_scale)
            
            # Apply location, rotation, scale to make them concrete objects
            bpy.context.view_layer.objects.active = current_layer
            bpy.ops.object.select_all(action='DESELECT')
            current_layer.select_set(True)
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        # Join all layers into a single final well base object
        bpy.ops.object.select_all(action='DESELECT')
        for layer_obj in all_layers:
            layer_obj.select_set(True)
        bpy.context.view_layer.objects.active = all_layers[0] # Active object for join

        bpy.ops.object.join()
        final_well_base = bpy.context.active_object
        final_well_base.name = object_name
        
        # Apply final location and scale
        final_well_base.location = Vector(location)
        final_well_base.scale = (scale, scale, scale)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        # Add material
        mat = bpy.data.materials.new(name=f"{object_name}_Material")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (material_color[0], material_color[1], material_color[2], 1)
        bsdf.inputs["Roughness"].default_value = 0.8
        final_well_base.data.materials.append(mat)
        
    else:
        return "Failed to create any layers."

    # Restore original selection and mode
    bpy.ops.object.select_all(action='DESELECT')
    for obj in original_selection:
        obj.select_set(True)
    if original_active_object:
        bpy.context.view_layer.objects.active = original_active_object
    if original_mode:
        bpy.ops.object.mode_set(mode=original_mode)
        
    # Reset pivot point to MEDIAN_POINT (default)
    bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'

    return f"Created '{object_name}' at {location} with 1 object"


# Example of how to call the function:
# create_low_poly_well(
#     object_name="MyStoneWell",
#     location=(0, 0, 0),
#     scale=1.0,
#     material_color=(0.5, 0.4, 0.35),
#     num_layers=4,
#     num_stones_per_layer=15,
#     stone_template_scale=(0.3, 0.15, 0.15),
#     randomize_amount=0.002,
#     bevel_amount=0.015,
#     decimate_ratio=0.4,
#     layer_vertical_offset=0.15
# )
