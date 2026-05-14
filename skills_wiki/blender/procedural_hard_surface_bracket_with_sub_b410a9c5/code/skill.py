def create_object(
    scene_name: str = "Scene",
    object_name: str = "SubD_Bracket",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.7, 0.7),
    **kwargs,
) -> str:
    """
    Create a highly clean, subdivision-ready curved mechanical bracket.
    
    Args:
        scene_name: Name of the active scene.
        object_name: Name of the generated object.
        location: (x, y, z) placement in the world.
        scale: Uniform scale factor.
        material_color: (R, G, B) color of the machined metal.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    # --- 1. Base Parameters ---
    D = 2.5            # Distance of circular ends from center
    R_out = 1.0        # Outer radius
    R_in = 0.45        # Inner hole radius
    cuts = 5           # Horizontal edge loops along the straight segment
    segments = 32      # Resolution of full circle
    
    # --- 2. Build Right Half in BMesh ---
    bm = bmesh.new()
    
    v_in = []
    v_out = []
    for i in range(segments):
        angle = i * 2 * math.pi / segments
        v_in.append(bm.verts.new((D + R_in * math.cos(angle), R_in * math.sin(angle), 0)))
        v_out.append(bm.verts.new((D + R_out * math.cos(angle), R_out * math.sin(angle), 0)))
        
    for i in range(segments):
        next_i = (i + 1) % segments
        bm.faces.new((v_in[i], v_out[i], v_out[next_i], v_in[next_i]))
        
    grid_verts = [] 
    for i_rel in range(17):
        i = (8 + i_rel) % segments
        row = [v_out[i]]
        v_center = Vector((0, v_out[i].co.y, 0))
        for j in range(1, cuts + 1):
            t = j / (cuts + 1)
            pos = v_out[i].co * (1 - t) + v_center * t
            row.append(bm.verts.new(pos))
        row.append(bm.verts.new(v_center))
        grid_verts.append(row)
        
    for i_rel in range(16):
        for j in range(cuts + 1):
            v1 = grid_verts[i_rel][j]
            v2 = grid_verts[i_rel+1][j]
            v3 = grid_verts[i_rel+1][j+1]
            v4 = grid_verts[i_rel][j+1]
            if len({v1, v2, v3, v4}) == 4:
                try:
                    bm.faces.new((v1, v4, v3, v2))
                except ValueError:
                    pass
                    
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    
    mesh = bpy.data.meshes.new(name=f"{object_name}_base")
    bm.to_mesh(mesh)
    bm.free()
    
    obj = bpy.data.objects.new(object_name, mesh)
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    scene.collection.objects.link(obj)
    
    # --- 3. Mirror & Bend Modifiers ---
    mod_mirror = obj.modifiers.new("Mirror", 'MIRROR')
    mod_mirror.use_axis[0] = True
    mod_mirror.use_clip = True
    
    mod_bend = obj.modifiers.new("Bend", 'SIMPLE_DEFORM')
    mod_bend.deform_method = 'BEND'
    mod_bend.deform_axis = 'Y'
    mod_bend.angle = math.radians(60)
    
    # Apply Deformation Modifiers cleanly via Depsgraph
    dg = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(dg)
    applied_mesh = bpy.data.meshes.new_from_object(eval_obj)
    obj.modifiers.clear()
    obj.data = applied_mesh
    
    # --- 4. Extrude Skirt & Create Quad-Hole ---
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    
    # Trace outer boundary loop robustly
    boundary_edges = set(e for e in bm.edges if len(e.link_faces) == 1)
    loops = []
    while boundary_edges:
        e = boundary_edges.pop()
        current_loop = [e]
        queue = [e]
        while queue:
            curr_e = queue.pop(0)
            for v in curr_e.verts:
                for linked_e in v.link_edges:
                    if linked_e in boundary_edges:
                        boundary_edges.remove(linked_e)
                        current_loop.append(linked_e)
                        queue.append(linked_e)
        loops.append(current_loop)
        
    outer_loop = max(loops, key=len)
    
    # Extrude skirt downward in increments to create holding loops
    skirt_cuts = 4
    flat_z = -1.2
    curr_edges = outer_loop
    v_to_orig_z = {v: v.co.z for e in outer_loop for v in e.verts}
    
    for step in range(1, skirt_cuts + 1):
        t = step / skirt_cuts
        ret = bmesh.ops.extrude_edge_only(bm, edges=curr_edges)
        geom = ret['geom']
        new_verts = [e for e in geom if isinstance(e, bmesh.types.BMVert)]
        new_edges = [e for e in geom if isinstance(e, bmesh.types.BMEdge)]
        curr_edges = [e for e in new_edges if e.verts[0] in new_verts and e.verts[1] in new_verts]
        
        next_v_to_orig_z = {}
        for v in new_verts:
            vertical_edge = [e for e in v.link_edges if e not in curr_edges][0]
            old_v = vertical_edge.other_vert(v)
            z0 = v_to_orig_z[old_v]
            v.co.z = z0 * (1 - t) + flat_z * t  # Interpolate down to flat_z
            next_v_to_orig_z[v] = z0
        v_to_orig_z = next_v_to_orig_z
        
    # Isolate specific faces on the front and back skirts to punch holes
    def select_skirt_faces(is_front):
        target = []
        for f in bm.faces:
            c = f.calc_center_median()
            side_ok = c.y > 0.5 if is_front else c.y < -0.5
            if side_ok and abs(c.x) < 0.55 and -0.95 < c.z < -0.3 and abs(f.normal.z) < 0.5:
                target.append(f)
        return target
        
    front_faces = select_skirt_faces(True)
    back_faces = select_skirt_faces(False)
    
    # Inset, project to perfect circle, and bridge loops
    if front_faces and back_faces:
        def process_hole(faces):
            ret = bmesh.ops.inset_region(bm, faces=faces, thickness=0.08)
            inner_faces = ret['faces']
            # Find the perimeter edge loop of the inset
            bound_edges = [e for e in bm.edges if sum(1 for f in e.link_faces if f in inner_faces) == 1 and sum(1 for f in e.link_faces if f not in inner_faces) > 0]
            bound_verts = list(set(v for e in bound_edges for v in e.verts))
            
            # Project vertices to a mathematical circle
            center = sum((v.co for v in bound_verts), Vector()) / len(bound_verts)
            radius = 0.25
            for v in bound_verts:
                vec = Vector((v.co.x - center.x, 0, v.co.z - center.z))
                if vec.length > 0:
                    vec.normalize()
                    v.co.x = center.x + vec.x * radius
                    v.co.z = center.z + vec.z * radius
            return inner_faces, bound_edges
            
        inner_front, bound_front = process_hole(front_faces)
        inner_back, bound_back = process_hole(back_faces)
        
        bmesh.ops.delete(bm, geom=inner_front + inner_back, context='FACES')
        try:
            bmesh.ops.bridge_loops(bm, edges=bound_front + bound_back)
        except Exception:
            pass
            
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    
    # --- 5. Final Modifiers & Polish ---
    for poly in obj.data.polygons:
        poly.use_smooth = True
        
    # Add thickness to the bridged sheet
    mod_solid = obj.modifiers.new("Solidify", 'SOLIDIFY')
    mod_solid.thickness = 0.15
    
    # Automatically catch 90 degree bends to hold edges
    mod_bevel = obj.modifiers.new("Bevel", 'BEVEL')
    mod_bevel.limit_method = 'ANGLE'
    mod_bevel.angle_limit = math.radians(35)
    mod_bevel.segments = 2
    mod_bevel.width = 0.02
    
    # Smooth final result
    mod_subd = obj.modifiers.new("Subdivision", 'SUBSURF')
    mod_subd.levels = 2
    mod_subd.render_levels = 2
    
    # Apply Transform
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    # Add Metal Material
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.8
        bsdf.inputs['Roughness'].default_value = 0.25
    obj.data.materials.append(mat)
    
    return f"Created procedural bracket '{object_name}' perfectly prepped for SubD shading at {location}."
