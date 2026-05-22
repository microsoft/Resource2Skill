def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyWellBase",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.5, 0.48, 0.52),
    **kwargs,
) -> str:
    """
    Creates a stylized, low-poly chiseled stone ring structure (e.g., a well base).
    
    Args:
        scene_name: Target scene.
        object_name: Name of the generated well base object.
        location: (X, Y, Z) world coordinates.
        scale: Uniform scale.
        material_color: Base (R, G, B) color for the stone.
        **kwargs: 
            rings (int): Number of vertically stacked rings (default: 3).
            base_radius (float): Radius of the bottom ring (default: 1.0).
            
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector, Matrix

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    rings_count = kwargs.get('rings', 3)
    base_radius = kwargs.get('base_radius', 1.0)
    stone_height = 0.22
    stone_depth = 0.22
    randomness = 0.015

    # === Step 1: Create Procedural Shader Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Roughness'].default_value = 0.85
        bsdf.inputs['Specular IOR Level'].default_value = 0.2
        
        # Add random color variation per stone island
        geom_node = nodes.new(type="ShaderNodeNewGeometry")
        ramp_node = nodes.new(type="ShaderNodeValToRGB")
        
        # Darker and lighter variants of the base color
        c1 = (material_color[0]*0.75, material_color[1]*0.75, material_color[2]*0.75, 1.0)
        c2 = (min(1.0, material_color[0]*1.25), min(1.0, material_color[1]*1.25), min(1.0, material_color[2]*1.25), 1.0)
        
        ramp_node.color_ramp.elements[0].color = c1
        ramp_node.color_ramp.elements[1].color = c2
        
        links.new(geom_node.outputs['Random Per Island'], ramp_node.inputs['Fac'])
        links.new(ramp_node.outputs['Color'], bsdf.inputs['Base Color'])

    # Helper function to generate a single ring
    def create_stone_ring(radius, decimate_ratio):
        circumference = 2 * math.pi * radius
        bm = bmesh.new()
        current_x = 0.0
        
        while current_x < circumference:
            # Vary individual stone lengths
            length = 0.4 * random.uniform(0.7, 1.3)
            # Close the gap nicely at the end of the ring
            if current_x + length > circumference - 0.2:
                length = circumference - current_x
                
            actual_length = max(0.05, length - 0.02) # Ensure visual gap between stones
            cx = current_x + length / 2.0
            
            # Create primitive and scale to proportions
            ret = bmesh.ops.create_cube(bm, size=1.0)
            verts = ret['verts']
            edges = ret['edges']
            
            # Apply rectangular dimensions (Y becomes height when bent into XZ plane later)
            for v in verts:
                v.co.x = (v.co.x * actual_length) + cx
                v.co.y = v.co.y * stone_height
                v.co.z = v.co.z * stone_depth
                
            # Bevel edges for a rounder base before distortion
            cube_edges = [e for e in edges]
            try:
                bmesh.ops.bevel(bm, geom=cube_edges, offset=0.03, segments=2, profile=0.5, affect_edges=True)
            except Exception:
                pass
                
            current_x += length

        # Subdivide for adequate distortion topology
        bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=1, use_grid_fill=True)
        
        # Center bounds around origin and add wobbly distortion
        shift_x = circumference / 2.0
        for v in bm.verts:
            v.co.x -= shift_x
            v.co.x += random.uniform(-randomness, randomness)
            v.co.y += random.uniform(-randomness, randomness)
            v.co.z += random.uniform(-randomness, randomness)

        mesh = bpy.data.meshes.new("RingTemp")
        bm.to_mesh(mesh)
        bm.free()
        
        ring_obj = bpy.data.objects.new("RingTemp", mesh)
        scene.collection.objects.link(ring_obj)
        
        # 1. Bend linearly arranged stones into a circle
        mod_bend = ring_obj.modifiers.new("Bend", 'SIMPLE_DEFORM')
        mod_bend.deform_method = 'BEND'
        mod_bend.deform_axis = 'X'
        mod_bend.angle = 2 * math.pi
        
        # 2. Add jagged, low-poly chiseled aesthetic
        mod_decimate = ring_obj.modifiers.new("Decimate", 'DECIMATE')
        mod_decimate.ratio = decimate_ratio
        
        return ring_obj

    ring_objects = []
    
    # === Step 2: Generate all stacked rings ===
    for i in range(rings_count):
        # Taper the well slightly by reducing radius as we go up
        current_radius = base_radius - (i * 0.05)
        ring_obj = create_stone_ring(radius=current_radius, decimate_ratio=random.uniform(0.35, 0.45))
        ring_obj.data.materials.append(mat)
        
        # Enforce flat shading for stylized look
        for poly in ring_obj.data.polygons:
            poly.use_smooth = False
            
        ring_objects.append(ring_obj)

    # Make sure we evaluate object operations in OBJECT mode
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # === Step 3: Apply Modifiers Safely and Position Properly ===
    # We apply modifiers via the Dependency Graph to avoid context override bugs
    depsgraph = bpy.context.evaluated_depsgraph_get()
    
    for i, ring in enumerate(ring_objects):
        # 1. Evaluate mesh with modifiers applied
        object_eval = ring.evaluated_get(depsgraph)
        new_mesh = bpy.data.meshes.new_from_object(object_eval)
        
        # 2. Clear procedural stack and apply raw mesh
        ring.modifiers.clear()
        old_mesh = ring.data
        ring.data = new_mesh
        bpy.data.meshes.remove(old_mesh)
        
        # 3. Mathematically recenter to local origin and orient to lay flat
        local_verts = [v.co for v in ring.data.vertices]
        if local_verts:
            median = sum(local_verts, Vector()) / len(local_verts)
            # Rotate 90 degrees around X to lie down in XY plane
            rot_mat = Matrix.Rotation(math.pi / 2.0, 4, 'X')
            
            for v in ring.data.vertices:
                v.co = rot_mat @ (v.co - median)
                
        # 4. Position in vertical stack and stagger rotation
        ring.location = (location[0], location[1], location[2] + (i * stone_height * 0.95))
        ring.rotation_euler.z = random.uniform(0, 2 * math.pi)

    # === Step 4: Join into a single Hero Object ===
    bpy.ops.object.select_all(action='DESELECT')
    for ring in ring_objects:
        ring.select_set(True)
        
    bpy.context.view_layer.objects.active = ring_objects[0]
    bpy.ops.object.join()
    
    final_obj = bpy.context.active_object
    final_obj.name = object_name
    final_obj.scale = (scale, scale, scale)
    
    return f"Created '{object_name}' (Stylized Stone Well Base) at {location} with {rings_count} rings"
