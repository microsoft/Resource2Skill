def create_lowpoly_stone_well_base(
    scene_name: str = "Scene",
    object_name: str = "WellBase",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.55, 0.50, 0.58),
    radius: float = 1.2,
    ring_count: int = 3,
    brick_height: float = 0.25,
    brick_depth: float = 0.35,
    decimate_ratio: float = 0.4,
    **kwargs
) -> str:
    """
    Create a procedural low-poly stone well base.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the stone.
        radius: Inner radius of the well.
        ring_count: Number of vertical stone layers.
        brick_height: Vertical height of a single brick.
        brick_depth: Thickness of the wall.
        decimate_ratio: Ratio for the decimate modifier (lower = more faceted).

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import random
    import mathutils
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    circumference = 2 * math.pi * radius
    avg_brick_length = 0.4
    
    # We build the entire structure inside a single bmesh for performance and cleanliness
    bm_master = bmesh.new()
    
    for row in range(ring_count):
        current_x = 0.0
        # Interlocking masonry offset (stretcher bond)
        row_offset_x = (avg_brick_length / 2.0) if row % 2 == 1 else 0.0
        
        while current_x < circumference:
            # Vary brick length slightly for organic feel
            b_len = avg_brick_length * random.uniform(0.7, 1.3)
            
            # Clamp the last brick so it fits exactly into the circumference
            if current_x + b_len > circumference:
                b_len = circumference - current_x
                if b_len < 0.1: # Skip tiny sliver bricks
                    break
                    
            existing_verts = set(bm_master.verts)
            existing_edges = set(bm_master.edges)
            
            # Create base cube for the brick
            bmesh.ops.create_cube(bm_master, size=1.0)
            
            # Isolate the newly created geometry
            new_verts = [v for v in bm_master.verts if v not in existing_verts]
            new_edges = [e for e in bm_master.edges if e not in existing_edges]
            
            # Scale cube to brick dimensions (subtracting a small gap from length)
            bmesh.ops.scale(bm_master, vec=(b_len - 0.02, brick_depth, brick_height), verts=new_verts)
            
            # Bevel the edges for a chiseled look
            try:
                bmesh.ops.bevel(bm_master, geom=new_edges, offset=0.04, segments=2, profile=0.5)
            except Exception:
                pass # Safe fallback
                
            new_verts = [v for v in bm_master.verts if v not in existing_verts]
            new_edges = [e for e in bm_master.edges if e not in existing_edges]
            
            # Subdivide for extra internal geometry to deform
            bmesh.ops.subdivide_edges(bm_master, edges=new_edges, cuts=1, use_grid_fill=True)
            
            new_verts = [v for v in bm_master.verts if v not in existing_verts]
            
            # Randomize vertices (organic wobble)
            for v in new_verts:
                offset = Vector((
                    random.uniform(-0.015, 0.015),
                    random.uniform(-0.015, 0.015),
                    random.uniform(-0.015, 0.015)
                ))
                v.co += offset
                
            # Compute position along the arc
            x_pos_arc = current_x + b_len/2.0 + row_offset_x
            theta = (x_pos_arc / circumference) * 2 * math.pi
            
            # Align the brick's length to the circle's tangent
            rot_matrix = mathutils.Euler((0, 0, theta + math.pi/2), 'XYZ').to_matrix()
            
            # Add slight radial depth variation so some stones stick out
            current_r = radius + random.uniform(-0.02, 0.02)
            
            # Calculate final world position for this brick
            loc_vec = Vector((
                current_r * math.cos(theta),
                current_r * math.sin(theta),
                (row * brick_height) + (brick_height / 2.0) # Rest flush on Z=0
            ))
            
            # Apply rotation and translation to the new vertices
            for v in new_verts:
                v.co = rot_matrix @ v.co
                v.co += loc_vec
                
            current_x += b_len

    # Finalize mesh
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    bm_master.to_mesh(mesh)
    bm_master.free()
    
    # Enforce flat shading for low-poly look
    mesh.polygons.foreach_set('use_smooth', [False] * len(mesh.polygons))
    mesh.update()
    
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    # Add Decimate modifier to crunch geometry into planar low-poly facets
    mod_decimate = obj.modifiers.new(name="Decimate", type='DECIMATE')
    mod_decimate.ratio = decimate_ratio
    
    # Create and assign material
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.95
        if 'Specular IOR Level' in bsdf.inputs:
            bsdf.inputs['Specular IOR Level'].default_value = 0.2
        elif 'Specular' in bsdf.inputs: # For older Blender versions
            bsdf.inputs['Specular'].default_value = 0.2
    obj.data.materials.append(mat)
    
    # Apply spatial transformations
    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))
    
    return f"Created '{object_name}' with {ring_count} stone rings (radius {radius}) at {location}."
