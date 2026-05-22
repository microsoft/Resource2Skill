def create_object(
    scene_name: str = "Scene",
    object_name: str = "Mechanical_Notch_Block",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.25, 0.25, 0.25),
    **kwargs,
) -> str:
    """
    Create a Hard-Surface Mechanical Notch Block in the active Blender scene.
    Replicates add-on detailing workflows using vanilla BMesh operations.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Create Base Geometry ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    
    # === Step 2: BMesh Procedural Detailing ===
    # 2a. Find Target Edge (Top-Front edge: +Y, +Z)
    target_edges = []
    for e in bm.edges:
        # Identify the edge residing perfectly at +Y and +Z bounding box limits
        if all((v.co.y > 0.9 and v.co.z > 0.9) for v in e.verts):
            target_edges.append(e)
            
    if target_edges:
        e = target_edges[0]
        
        # 2b. Chamfer the edge
        bmesh.ops.bevel(bm, geom=[e], offset=0.4, segments=1, vertex_only=False)
        
        # Recalculate normals to find the newly created sloped face
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        target_face = None
        for f in bm.faces:
            # The chamfered face will point diagonally up and forward (+Y, +Z)
            if f.normal.y > 0.1 and f.normal.z > 0.1 and abs(f.normal.x) < 0.1:
                target_face = f
                break
                
        if target_face:
            # 2c. Inset (Extrude + Scale to center)
            ext1 = bmesh.ops.extrude_face_region(bm, geom=[target_face])
            ext1_faces = [geom for geom in ext1['geom'] if isinstance(geom, bmesh.types.BMFace)]
            if ext1_faces:
                new_face = ext1_faces[0]
                center = new_face.calc_center_median()
                
                # Scale vertices towards the median center to act as an inset
                for v in new_face.verts:
                    v.co = center + (v.co - center) * 0.75
                
                # 2d. Extrude Inward (Create the notch depth)
                bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
                ext2 = bmesh.ops.extrude_face_region(bm, geom=[new_face])
                ext2_faces = [geom for geom in ext2['geom'] if isinstance(geom, bmesh.types.BMFace)]
                if ext2_faces:
                    inner_face = ext2_faces[0]
                    inward_vec = -inner_face.normal * 0.15  # Push inwards
                    bmesh.ops.translate(bm, verts=inner_face.verts, vec=inward_vec)
                    
    # Finalize BMesh
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    
    # Enable smooth shading on all polygons
    for f in mesh.polygons:
        f.use_smooth = True
        
    # Support for legacy Auto Smooth (Blender 4.0 and below)
    try:
        mesh.use_auto_smooth = True
        mesh.auto_smooth_angle = 0.523599 # 30 degrees
    except AttributeError:
        pass # Blender 4.1+ uses modifiers for this
    
    # === Step 3: Global Hard-Surface Modifiers ===
    bevel_mod = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel_mod.limit_method = 'ANGLE'
    bevel_mod.angle_limit = 0.523599 # 30 degrees
    bevel_mod.width = 0.02
    bevel_mod.segments = 3
    # Optional: Harden normals requires Auto Smooth or equivalent data setup to look correct
    bevel_mod.harden_normals = False 
    
    # === Step 4: Build Material ===
    mat = bpy.data.materials.new(name=object_name + "_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Metallic"].default_value = 0.8
        bsdf.inputs["Roughness"].default_value = 0.3
    
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
        
    # === Step 5: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    return f"Created '{object_name}' at {location} with mechanical notch detailing."
