def create_stylized_stone_well_base(
    scene_name: str = "Scene",
    object_name: str = "LowPolyWellBase",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.55, 0.6),
    radius: float = 1.2,
    layers: int = 3,
    **kwargs,
) -> str:
    """
    Create a Procedural Low-Poly Stone Well Base in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color of the stone.
        radius: Radius of the circular well base.
        layers: Number of stacked stone rings.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import random
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Create Stone Material ===
    mat_name = f"{object_name}_Mat"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.85
            bsdf.inputs['Specular IOR Level'].default_value = 0.2

    # Calculate circumference to determine block count and spacing
    circumference = 2 * math.pi * radius
    target_stone_length = 0.4
    num_stones = max(4, int(circumference / target_stone_length))
    actual_spacing = circumference / num_stones
    layer_height = 0.2
    
    layer_objects = []
    
    # === Step 2: Build Linear Stone Arrays per Layer ===
    for layer in range(layers):
        stones = []
        for i in range(num_stones):
            # Spawn base cube
            bpy.ops.mesh.primitive_cube_add(size=1)
            stone = bpy.context.active_object
            
            # Dimension logic (sx is length, sy is depth, sz is height)
            # We leave a 5% gap between stones to define individual blocks
            sx = actual_spacing * 0.95 
            sy = layer_height + random.uniform(-0.02, 0.02)
            sz = layer_height + random.uniform(-0.02, 0.02)
            stone.scale = (sx, sy, sz)
            
            # Position along X axis (centering the block within its allotted segment)
            stone.location = (i * actual_spacing + (actual_spacing / 2), 0, 0)
            
            # Apply scale for uniform modifier/bevel behavior
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Add topological detail & random denting
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.bevel(offset=0.03, offset_pct=0, segments=2)
            bpy.ops.mesh.subdivide(number_cuts=2)
            bpy.ops.transform.vertex_random(offset=0.015)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            stone.data.materials.append(mat)
            stones.append(stone)
            
        # Join the linear array of stones for this layer
        bpy.ops.object.select_all(action='DESELECT')
        for s in stones:
            s.select_set(True)
        bpy.context.view_layer.objects.active = stones[0]
        bpy.ops.object.join()
        layer_obj = bpy.context.active_object
        
        # === Step 3: Deform into a Perfect Circle ===
        mod_bend = layer_obj.modifiers.new(name="Bend", type='SIMPLE_DEFORM')
        mod_bend.deform_method = 'BEND'
        mod_bend.angle = 2 * math.pi # 360 degrees
        mod_bend.deform_axis = 'Z'
        bpy.ops.object.modifier_apply(modifier="Bend")
        
        # Recenters the object's origin to the exact middle of the new circle
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        
        # Orient and stack the layer
        layer_obj.location = (0, 0, layer * layer_height)
        layer_obj.rotation_euler = (0, 0, random.uniform(0, 2 * math.pi))
        
        # Slight tapering inwards as it gets higher
        layer_scale = 1.0 - (layer * 0.05)
        layer_obj.scale = (layer_scale, layer_scale, 1.0)
        
        # === Step 4: Add Jagged 'Low-Poly' Pass ===
        mod_dec = layer_obj.modifiers.new(name="Decimate", type='DECIMATE')
        mod_dec.ratio = 0.37
        bpy.ops.object.modifier_apply(modifier="Decimate")
        
        layer_objects.append(layer_obj)
        
    # === Step 5: Finalize Assembly ===
    bpy.ops.object.select_all(action='DESELECT')
    for lo in layer_objects:
        lo.select_set(True)
    bpy.context.view_layer.objects.active = layer_objects[0]
    bpy.ops.object.join()
    
    final_obj = bpy.context.active_object
    final_obj.name = object_name
    
    # Place at requested global position and scale
    final_obj.location = Vector(location)
    final_obj.scale = (scale, scale, scale)
    
    return f"Created '{object_name}' at {location} with {layers} layers and {num_stones} stones per layer."
