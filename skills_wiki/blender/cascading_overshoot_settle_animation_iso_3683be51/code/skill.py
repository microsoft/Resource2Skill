def create_object(
    scene_name: str = "Scene",
    object_name: str = "AnimatedPopGrid",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.9, 0.85, 0.75), # Warm wood/tile color
    **kwargs,
) -> str:
    """
    Creates a grid of tiles that animate in using a cascading 'Overshoot & Settle' scale effect.
    Replicates the 'Isometric Room Build' animation pattern.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the collection and objects.
        location: Center of the animated grid.
        scale: Overall scale multiplier for the tiles and spacing.
        material_color: RGB base color for the tiles.
        **kwargs: 
            grid_size (int): N x N dimension of the grid (default: 7)
            anim_start (int): Frame the animation begins (default: 10)
            overshoot_factor (float): How far past 1.0 it scales before settling (default: 1.15)
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    # Configuration parameters
    grid_size = kwargs.get("grid_size", 7) 
    tile_spacing = kwargs.get("tile_spacing", 1.05)
    anim_start = kwargs.get("anim_start", 10)
    anim_delay_factor = kwargs.get("anim_delay_factor", 3.0) # Frames delay per distance unit
    overshoot_factor = kwargs.get("overshoot_factor", 1.15)
    dur_overshoot = kwargs.get("dur_overshoot", 10)
    dur_settle = kwargs.get("dur_settle", 5)

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.3
        bsdf.inputs['Specular IOR Level'].default_value = 0.5

    # === Step 2: Prepare the Additive Collection ===
    collection = bpy.data.collections.new(object_name)
    scene.collection.children.link(collection)

    # === Step 3: Create Optimized Base Mesh ===
    # We use bmesh to create a 1x1x1 cube and shift its vertices so the origin is at the BOTTOM.
    # This ensures that when scaled, the tiles grow upwards out of the floor instead of clipping through it.
    base_mesh = bpy.data.meshes.new(f"{object_name}_BaseMesh")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.z += 0.5 # Shift up by half size
    bm.to_mesh(base_mesh)
    bm.free()
    
    # Assign material to the base mesh so all instances inherit it automatically
    base_mesh.materials.append(mat)

    # === Step 4: Distribute and Animate ===
    created_count = 0
    center = Vector(location)
    half_grid = (grid_size - 1) / 2.0
    max_frame = anim_start
    
    # Final resting scale for each individual tile (flattened Z)
    base_scale_vec = Vector((scale * 0.95, scale * 0.95, scale * 0.15))

    for x in range(grid_size):
        for y in range(grid_size):
            # Calculate physical grid position
            pos_x = center.x + (x - half_grid) * tile_spacing * scale
            pos_y = center.y + (y - half_grid) * tile_spacing * scale
            pos_z = center.z

            # Create object instance linking to the shared mesh
            tile = bpy.data.objects.new(f"{object_name}_Tile_{x}_{y}", base_mesh)
            tile.location = (pos_x, pos_y, pos_z)
            collection.objects.link(tile)

            # Add Bevel modifier for stylized edges (catches light)
            bevel = tile.modifiers.new(name="Bevel", type='BEVEL')
            bevel.width = 0.02 * scale
            bevel.segments = 3

            # --- Animation Logic (Commotion + Overshoot) ---
            # 1. Calculate distance from center to determine the "wave" delay
            dist_to_center = math.sqrt((x - half_grid)**2 + (y - half_grid)**2)
            start_f = anim_start + int(dist_to_center * anim_delay_factor)

            # 2. Keyframe 1: Hidden state
            tile.scale = (0, 0, 0)
            tile.keyframe_insert(data_path="scale", frame=start_f)

            # 3. Keyframe 2: The Overshoot (Scale goes past target)
            tile.scale = base_scale_vec * overshoot_factor
            tile.keyframe_insert(data_path="scale", frame=start_f + dur_overshoot)

            # 4. Keyframe 3: The Settle (Scale returns to resting state)
            tile.scale = base_scale_vec
            tile.keyframe_insert(data_path="scale", frame=start_f + dur_overshoot + dur_settle)

            # 5. Smooth Interpolation
            if tile.animation_data and tile.animation_data.action:
                for fcurve in tile.animation_data.action.fcurves:
                    for kf in fcurve.keyframe_points:
                        kf.interpolation = 'BEZIER'

            created_count += 1
            max_frame = max(max_frame, start_f + dur_overshoot + dur_settle)

    # Ensure the scene timeline is long enough to show the full cascading animation
    if scene.frame_end < max_frame + 20:
        scene.frame_end = int(max_frame + 20)

    return f"Created '{object_name}' with {created_count} cascading animated tiles. Play the timeline to see the Overshoot & Settle wave effect."
