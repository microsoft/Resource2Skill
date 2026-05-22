def create_stylized_stone_ring(
    scene_name: str = "Scene",
    object_name: str = "WellBase",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.45, 0.40, 0.43),
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Stone Ring (Well Base) in the active Blender scene.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the entire ring (1.0 = ~3m diameter).
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Extensible parameters.
        
    Returns:
        Status string describing the created object.
    """
    import bpy
    import math
    import random
    from mathutils import Vector

    # Ensure scene exists and is active
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    bpy.context.window.scene = scene

    # Parameters for the layers (radius, height_offset, num_stones, thickness)
    ring_configs = [
        (1.5 * scale, 0.0 * scale, 12, 0.4 * scale),  # Bottom row
        (1.4 * scale, 0.4 * scale, 10, 0.3 * scale),  # Middle row (slightly smaller radius/height)
        (1.5 * scale, 0.7 * scale, 12, 0.4 * scale),  # Top row
    ]

    # Create procedural noise texture for vertex randomization
    noise_tex = bpy.data.textures.get("StoneNoise")
    if not noise_tex:
        noise_tex = bpy.data.textures.new("StoneNoise", type='CLOUDS')
        noise_tex.noise_scale = 0.3

    layer_objects = []

    # Save original cursor location to restore later
    saved_cursor_loc = scene.cursor.location.copy()

    for layer_idx, (radius, z_offset, num_stones, height) in enumerate(ring_configs):
        circumference = 2 * math.pi * radius
        # Leave a tiny gap between stones to emphasize they are individual blocks
        stone_length = (circumference / num_stones) * 0.95 
        stone_depth = 0.4 * scale

        start_x = -circumference / 2.0 + (stone_length / 2.0)
        
        stones_in_layer = []

        # Generate individual stones for this layer
        for i in range(num_stones):
            pos_x = start_x + i * (circumference / num_stones)
            bpy.ops.mesh.primitive_cube_add(size=1, location=(pos_x, 0, z_offset))
            stone = bpy.context.active_object
            
            # Apply initial varied scale to make stones non-uniform
            stone.scale = (
                stone_length * random.uniform(0.9, 1.1),
                stone_depth * random.uniform(0.85, 1.15),
                height * random.uniform(0.9, 1.1)
            )
            
            # 1. Bevel modifier
            bev = stone.modifiers.new("Bevel", 'BEVEL')
            bev.width = 0.05 * scale
            bev.segments = 2
            
            # 2. Subdivision (to provide vertices for distortion)
            sub = stone.modifiers.new("Subdiv", 'SUBSURF')
            sub.levels = 1
            
            # 3. Displace (to simulate vertex randomization)
            disp = stone.modifiers.new("Displace", 'DISPLACE')
            disp.texture = noise_tex
            disp.strength = 0.06 * scale
            disp.texture_coords = 'GLOBAL'  # Ensures each stone gets a unique noise crop
            
            # Evaluate and bake modifiers to mesh (Procedural -> Destructive per stone)
            dg = bpy.context.evaluated_depsgraph_get()
            eval_stone = stone.evaluated_get(dg)
            mesh = bpy.data.meshes.new_from_object(eval_stone)
            stone.modifiers.clear()
            stone.data = mesh
            
            stones_in_layer.append(stone)
            
        # Join all stones in this layer
        bpy.ops.object.select_all(action='DESELECT')
        for s in stones_in_layer:
            s.select_set(True)
        bpy.context.view_layer.objects.active = stones_in_layer[0]
        bpy.ops.object.join()
        
        layer_obj = bpy.context.active_object
        
        # Center origin exactly at (0, 0, z_offset) so the Bend modifier wraps perfectly
        scene.cursor.location = (0.0, 0.0, z_offset)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        
        # 4. Simple Deform (Bend into a circle)
        bend = layer_obj.modifiers.new("Bend", 'SIMPLE_DEFORM')
        bend.deform_method = 'BEND'
        bend.angle = 2 * math.pi  # 360 degrees
        bend.deform_axis = 'Z'
        
        # 5. Decimate (For stylized low-poly variation)
        # Apply more decimation to middle rows to break symmetry
        dec = layer_obj.modifiers.new("Decimate", 'DECIMATE')
        dec.ratio = random.uniform(0.3, 0.6)
        
        layer_objects.append(layer_obj)

    # Join all layers into the final object
    bpy.ops.object.select_all(action='DESELECT')
    for obj in layer_objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = layer_objects[0]
    bpy.ops.object.join()
    
    final_ring = bpy.context.active_object
    final_ring.name = object_name
    
    # Restore cursor
    scene.cursor.location = saved_cursor_loc
    
    # Position and scale the final grouped asset
    final_ring.location = Vector(location)
    
    # === Material Setup ===
    mat_name = f"Mat_StylizedStone_{object_name}"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Base color
            bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
            # High roughness for matte stone
            if "Roughness" in bsdf.inputs:
                bsdf.inputs["Roughness"].default_value = 0.85
            # Zero metallic
            if "Metallic" in bsdf.inputs:
                bsdf.inputs["Metallic"].default_value = 0.0
            # Slight color variation trick:
            # (Optional enhancement to node tree could go here)
            
    if len(final_ring.data.materials) == 0:
        final_ring.data.materials.append(mat)
    else:
        final_ring.data.materials[0] = mat

    # Apply all final modifiers (Bend & Decimate) to bake the object
    dg = bpy.context.evaluated_depsgraph_get()
    eval_final = final_ring.evaluated_get(dg)
    final_mesh = bpy.data.meshes.new_from_object(eval_final)
    final_ring.modifiers.clear()
    final_ring.data = final_mesh

    return f"Created '{object_name}' (Stylized Stone Base) at {location} with {len(ring_configs)} layers."
