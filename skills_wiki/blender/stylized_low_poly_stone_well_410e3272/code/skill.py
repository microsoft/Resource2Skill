def create_low_poly_well(
    scene_name: str = "Scene",
    object_name: str = "LowPolyWell",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_colors: list = [(0.5, 0.5, 0.5, 1.0), (0.6, 0.6, 0.6, 1.0), (0.4, 0.4, 0.4, 1.0)],
    num_rows: int = 4,
    blocks_per_row: int = 12,
    block_dimensions: tuple = (0.7, 0.3, 0.2), # (length, width, height) in meters
    bevel_offset_factor: float = 0.03, # Factor for bevel offset
    randomize_block_amount: float = 0.005, # Max displacement in meters
    decimate_ratio: float = 0.4, # Ratio of faces to keep (0-1)
    row_scale_factor: float = 0.9, # Scale of subsequent rows relative to previous (inner diameter)
    row_offset_angle: float = 15.0 # Degrees to rotate each subsequent row for brick offset
) -> str:
    """
    Creates a low-poly stone well base with customizable rows and block styles.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created well object.
        location: (x, y, z) world-space position for the entire well.
        scale: Uniform scale factor for the entire well.
        material_colors: List of (R, G, B, A) tuples for materials, cycled per row.
        num_rows: Number of stacked rings forming the well.
        blocks_per_row: Number of individual blocks in each ring.
        block_dimensions: (length, width, height) of a single block.
        bevel_offset_factor: Controls how much the edges are beveled (relative to block size).
        randomize_block_amount: Maximum displacement for vertex randomization.
        decimate_ratio: Ratio of faces to keep after decimation (0.0 to 1.0).
        row_scale_factor: Factor by which each subsequent row is scaled down (0.0 to 1.0).
        row_offset_angle: Angle in degrees to rotate each subsequent row for brick staggering.

    Returns:
        Status string, e.g., "Created 'LowPolyWell' at (0, 0, 0) with 4 stone layers."
    """
    import bpy
    import bmesh
    from mathutils import Vector, Euler, Matrix
    import math
    import random # For random seed generation

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Create new collections for organization
    well_collection_name = f"{object_name}_Collection"
    well_collection = bpy.data.collections.get(well_collection_name)
    if not well_collection:
        well_collection = bpy.data.collections.new(name=well_collection_name)
        scene.collection.children.link(well_collection)

    originals_collection_name = f"{object_name}_Original_Blocks"
    originals_collection = bpy.data.collections.get(originals_collection_name)
    if not originals_collection:
        originals_collection = bpy.data.collections.new(name=originals_collection_name)
        scene.collection.children.link(originals_collection)
    originals_collection.hide_viewport = True
    originals_collection.hide_render = True

    all_ring_objects = []
    current_z_offset = 0.0 # Tracks the base Z position for each new layer

    # Store current pivot point and 3D cursor location to restore later
    original_pivot_point = bpy.context.scene.tool_settings.transform_pivot_point
    original_cursor_location = scene.cursor.location.copy()
    original_cursor_rotation = scene.cursor.rotation_euler.copy()

    # Set 3D cursor to world origin for consistent pivot points when bending/rotating rings
    scene.cursor.location = (0, 0, 0)
    scene.cursor.rotation_euler = (0, 0, 0)
    bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'

    for i in range(num_rows):
        row_blocks_list = []
        
        # Create unique material for each row layer
        mat_name = f"{object_name}_Mat_Layer_{i}"
        mat = bpy.data.materials.get(mat_name)
        if not mat:
            mat = bpy.data.materials.new(name=mat_name)
            mat.use_nodes = True
            principled_bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if principled_bsdf:
                principled_bsdf.inputs['Base Color'].default_value = material_colors[i % len(material_colors)]
                principled_bsdf.inputs['Roughness'].default_value = 0.7

        # --- 1. Create a row of individual blocks ---
        for j in range(blocks_per_row):
            # Create cube mesh data
            block_mesh_data = bpy.data.meshes.new(f"{object_name}_BlockData_{i}_{j}")
            bm = bmesh.new()
            bmesh.ops.create(bm, geom=bmesh.ops.create_cube(bm, size=2.0)['verts']) # Default 2m cube
            
            # Convert dimensions to scale factors for 2m cube
            scale_x = block_dimensions[0] / 2.0
            scale_y = block_dimensions[1] / 2.0
            scale_z = block_dimensions[2] / 2.0
            
            # Apply initial object scale (will be baked into mesh)
            # This simulates the video's S, SX, Ctrl+A Scale
            bmesh.ops.transform(bm, verts=bm.verts, matrix=Matrix.Scale(scale_x, 4, (1,0,0)))
            bmesh.ops.transform(bm, verts=bm.verts, matrix=Matrix.Scale(scale_y, 4, (0,1,0)))
            bmesh.ops.transform(bm, verts=bm.verts, matrix=Matrix.Scale(scale_z, 4, (0,0,1)))

            # Bevel all edges
            bmesh.ops.select_all(bm, geom=bm.edges)
            bmesh.ops.bevel(
                bm,
                geom=bm.edges,
                segments=2, # As shown in video
                offset=bevel_offset_factor * max(block_dimensions),
                profile=0.5
            )

            # Add loop cuts for randomization points
            bmesh.ops.subdivide_edges(bm, edges=[e for e in bm.edges if abs(e.normal.x) > 0.9], cuts=2) # Along length (X)
            bmesh.ops.subdivide_edges(bm, edges=[e for e in bm.edges if abs(e.normal.y) > 0.9], cuts=1) # Along width (Y)
            bmesh.ops.subdivide_edges(bm, edges=[e for e in bm.edges if abs(e.normal.z) > 0.9], cuts=1) # Along height (Z)

            # Randomize vertices
            bmesh.ops.transform.vert_random(
                bm,
                verts=bm.verts,
                factor=randomize_block_amount,
                seed=random.randint(0, 10000) # Unique random seed for each block
            )
            
            bm.to_mesh(block_mesh_data)
            bm.free()
            
            block_obj = bpy.data.objects.new(f"{object_name}_Block_{i}_{j}", block_mesh_data)
            originals_collection.objects.link(block_obj) # Temporarily link to originals for tracking
            
            # Position blocks in a line (slightly overlapping)
            block_obj.location.x = j * block_dimensions[0] * 0.95 # Adjust for overlap
            block_obj.location.z = block_dimensions[2] / 2 # Lift block off ground
            
            if block_obj.data.materials:
                block_obj.data.materials[0] = mat
            else:
                block_obj.data.materials.append(mat)
            
            row_blocks_list.append(block_obj)
        
        # --- 2. Join blocks into a single linear object ---
        bpy.ops.object.select_all(action='DESELECT')
        for block_obj in row_blocks_list:
            block_obj.select_set(True)
        bpy.context.view_layer.objects.active = row_blocks_list[0] # Active object for joining
        bpy.ops.object.join()
        
        linear_obj = bpy.context.active_object
        linear_obj.name = f"{object_name}_Linear_{i}"
        
        # Unlink from originals collection after joining
        for block_obj_orig in row_blocks_list:
            if block_obj_orig.name != linear_obj.name and block_obj_orig.users_collection:
                for coll in block_obj_orig.users_collection:
                    if coll == originals_collection:
                        coll.objects.unlink(block_obj_orig)
        
        # --- 3. Apply Simple Deform (Bend) to create a ring ---
        deform_mod = linear_obj.modifiers.new(name="BendDeform", type='SIMPLE_DEFORM')
        deform_mod.deform_method = 'BEND'
        deform_mod.angle = math.radians(360)
        deform_mod.deform_axis = 'Z' # Bend around Z-axis
        deform_mod.origin = 'X' # The original length of the line of blocks is along X
        
        # Apply the modifier to make it a permanent ring
        bpy.ops.object.modifier_apply(modifier=deform_mod.name)
        
        # --- 4. Position and scale the ring layer ---
        # Set origin to geometry center for consistent scaling/rotation
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        linear_obj.location = (0, 0, 0) # Center the ring at world origin temporarily

        current_ring_scale_factor = scale * (row_scale_factor ** i)
        linear_obj.scale = (current_ring_scale_factor, current_ring_scale_factor, current_ring_scale_factor)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True) # Apply scale after positioning

        # Position the ring vertically
        linear_obj.location.z = current_z_offset + (linear_obj.dimensions.z / 2)
        current_z_offset += linear_obj.dimensions.z # Accumulate height for next layer
        
        # Rotate current layer for offset bricks
        linear_obj.rotation_euler.z = math.radians(i * row_offset_angle)
        
        # --- 5. Add Decimate modifier (Collapse type for jaggedness) ---
        decimate_mod = linear_obj.modifiers.new(name="Decimate", type='DECIMATE')
        decimate_mod.decimate_type = 'COLLAPSE'
        decimate_mod.ratio = decimate_ratio # Controls percentage of faces to keep (0.0 - 1.0)
        
        all_ring_objects.append(linear_obj)

    # --- 6. Final Join of all rings and Positioning of the Well ---
    if all_ring_objects:
        bpy.ops.object.select_all(action='DESELECT')
        for ring_obj in all_ring_objects:
            ring_obj.select_set(True)
        bpy.context.view_layer.objects.active = all_ring_objects[0]
        bpy.ops.object.join()
        
        final_well_obj = bpy.context.active_object
        final_well_obj.name = object_name
        
        # Set origin of the final well to its base center
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        final_well_obj.location = Vector(location) # Apply desired world location for the entire well
        final_well_obj.scale = (scale, scale, scale) # Apply overall scale last
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        # Move intermediate block data and meshes to the originals collection
        for obj in bpy.data.objects:
            if obj.name.startswith(f"{object_name}_BlockData_") or obj.name.startswith(f"{object_name}_Linear_"):
                 # Check if it's not the final joined object
                if obj.name != final_well_obj.name:
                    if obj.users_collection:
                        for coll in obj.users_collection:
                            coll.objects.unlink(obj)
                    originals_collection.objects.link(obj)

        # Ensure final object is in the main well_collection
        if final_well_obj.users_collection:
            for coll in final_well_obj.users_collection:
                if coll != well_collection:
                    coll.objects.unlink(final_well_obj)
            if well_collection not in final_well_obj.users_collection:
                well_collection.objects.link(final_well_obj)
        else:
            well_collection.objects.link(final_well_obj)

        # Clear selected objects
        bpy.ops.object.select_all(action='DESELECT')
        
        # Restore original pivot point and cursor location
        bpy.context.scene.tool_settings.transform_pivot_point = original_pivot_point
        scene.cursor.location = original_cursor_location
        scene.cursor.rotation_euler = original_cursor_rotation

        return f"Created '{object_name}' at {location} with {num_rows} stone layers."
    else:
        # Restore original pivot point and cursor location
        bpy.context.scene.tool_settings.transform_pivot_point = original_pivot_point
        scene.cursor.location = original_cursor_location
        scene.cursor.rotation_euler = original_cursor_rotation
        return "No well created."

