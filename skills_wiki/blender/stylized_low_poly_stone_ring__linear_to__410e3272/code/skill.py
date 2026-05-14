def create_low_poly_well_base(
    scene_name: str = "Scene",
    object_name: str = "LowPolyWellBase",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.55, 0.53, 0.58),
    **kwargs,
) -> str:
    """
    Create a stylized low-poly well base by bending a row of randomized stones into a ring.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created parent empty.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color of the stones.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector

    # Ensure we are in object mode
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    # Generation Parameters
    num_stones = 14
    base_radius = 1.2
    circumference = 2 * math.pi * base_radius
    avg_length = circumference / num_stones
    base_height = 0.25
    
    bricks = []
    current_x = 0.0
    
    # === Step 1: Generate a straight line of randomized stones ===
    for i in range(num_stones):
        length = avg_length * random.uniform(0.85, 1.15)
        depth = 0.35 * random.uniform(0.8, 1.2)
        height = base_height * random.uniform(0.8, 1.2)
        
        bpy.ops.mesh.primitive_cube_add(size=1, location=(current_x + length/2, 0, 0))
        brick = bpy.context.active_object
        brick.scale = (length, depth, height)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Detail generation via BMesh
        bm = bmesh.new()
        bm.from_mesh(brick.data)
        
        # Chiseled bevel
        bmesh.ops.bevel(bm, geom=bm.edges, offset=0.03, segments=1, profile=0.5)
        
        # Subdivide for wobble and decimation topology
        bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=2, use_grid_fill=True)
        
        # Distort/Randomize vertices (Wobble)
        for v in bm.verts:
            v.co.x += random.uniform(-0.015, 0.015)
            v.co.y += random.uniform(-0.015, 0.015)
            v.co.z += random.uniform(-0.015, 0.015)
            
        bm.to_mesh(brick.data)
        bm.free()
            
        bricks.append(brick)
        current_x += length + 0.02 # Small mortar gap
        
    # === Step 2: Join into a single linear object ===
    bpy.ops.object.select_all(action='DESELECT')
    for b in bricks:
        b.select_set(True)
    bpy.context.view_layer.objects.active = bricks[0]
    bpy.ops.object.join()
    
    ring = bpy.context.active_object
    ring.name = f"{object_name}_Ring_Bottom"
    
    # Center object along X axis so the Bend modifier closes perfectly
    bm = bmesh.new()
    bm.from_mesh(ring.data)
    for v in bm.verts:
        v.co.x -= current_x / 2
    bm.to_mesh(ring.data)
    bm.free()
    
    # === Step 3: Apply Modifiers (Bend & Decimate) ===
    bend_mod = ring.modifiers.new(name="BendRing", type='SIMPLE_DEFORM')
    bend_mod.deform_method = 'BEND'
    bend_mod.angle = 2 * math.pi # 360 degrees
    bend_mod.deform_axis = 'Z'
    
    dec_mod = ring.modifiers.new(name="ChunkyDecimate", type='DECIMATE')
    dec_mod.ratio = 0.4
    
    bpy.ops.object.modifier_apply(modifier=bend_mod.name)
    bpy.ops.object.modifier_apply(modifier=dec_mod.name)
    
    # Ensure flat shading for the low-poly look
    for poly in ring.data.polygons:
        poly.use_smooth = False
    
    # === Step 4: Material with 'Random Per Island' Variation ===
    mat = bpy.data.materials.new(name=f"{object_name}_StoneMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    
    if bsdf:
        geom_node = nodes.new('ShaderNodeNewGeometry')
        color_ramp = nodes.new('ShaderNodeValToRGB')
        
        # Create subtle variance between dark and light tones of the base color
        color_ramp.color_ramp.elements[0].position = 0.0
        color_ramp.color_ramp.elements[0].color = (material_color[0]*0.7, material_color[1]*0.7, material_color[2]*0.7, 1)
        color_ramp.color_ramp.elements[1].position = 1.0
        color_ramp.color_ramp.elements[1].color = (material_color[0]*1.1, material_color[1]*1.1, material_color[2]*1.1, 1)
        
        links.new(geom_node.outputs['Random Per Island'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
        bsdf.inputs['Roughness'].default_value = 0.9
        
    ring.data.materials.append(mat)
    
    # === Step 5: Stack Rings to Form Base ===
    ring.location.z = base_height / 2
    
    # Middle Ring (Slightly smaller, offset rotation)
    bpy.ops.object.duplicate(linked=False)
    mid_ring = bpy.context.active_object
    mid_ring.name = f"{object_name}_Ring_Middle"
    mid_ring.location.z = ring.location.z + base_height * 0.95
    mid_ring.rotation_euler.z = math.radians(25)
    mid_ring.scale = (0.85, 0.85, 1.0)
    
    # Top Ring (Slightly larger, offset rotation)
    bpy.ops.object.duplicate(linked=False)
    top_ring = bpy.context.active_object
    top_ring.name = f"{object_name}_Ring_Top"
    top_ring.location.z = mid_ring.location.z + base_height * 0.95
    top_ring.rotation_euler.z = math.radians(-15)
    top_ring.scale = (1.0, 1.0, 1.0)
    
    # === Step 6: Parent and Final Placement ===
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    parent = bpy.context.active_object
    parent.name = object_name
    parent.scale = (scale, scale, scale)
    
    for r in [ring, mid_ring, top_ring]:
        r.parent = parent
        
    return f"Created '{object_name}' (3 rings, {num_stones} stones each) at {location}"
