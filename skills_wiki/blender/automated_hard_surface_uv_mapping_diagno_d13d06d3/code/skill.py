def create_object(
    scene_name: str = "Scene",
    object_name: str = "UVMapped_Part",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.8, 0.8),
    **kwargs,
) -> str:
    """
    Create an Automated Hard-Surface UV Mapped Object.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: Fallback color (overridden by diagnostic texture).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (Mechanical Cylinder) ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    # Create base cylinder
    bmesh.ops.create_cylinder(
        bm, 
        cap_ends=True, 
        cap_tris=False, 
        segments=16, 
        radius=scale * 1.0, 
        depth=scale * 1.5
    )
    
    # Inset and extrude the top face to create a cavity
    top_faces = [f for f in bm.faces if f.normal.z > 0.9]
    if top_faces:
        res = bmesh.ops.inset_region(bm, faces=top_faces, thickness=scale * 0.2)
        inner_faces = [elem for elem in res['faces'] if isinstance(elem, bmesh.types.BMFace)]
        res_extrude = bmesh.ops.extrude_face_region(bm, geom=inner_faces)
        
        # Move the extruded faces down to create the hole
        extruded_verts = list(set(v for elem in res_extrude['geom'] if isinstance(elem, bmesh.types.BMFace) for v in elem.verts))
        bmesh.ops.translate(bm, vec=Vector((0, 0, -scale * 0.8)), verts=extruded_verts)

    # === Step 2: Automated Seam Marking (The Tutorial's Core Logic) ===
    bm.edges.ensure_lookup_table()
    for edge in bm.edges:
        if edge.is_manifold:
            # Calculate angle between adjacent faces
            angle = edge.calc_face_angle()
            # Mark seams on edges sharper than ~80 degrees (1.4 radians)
            if angle > 1.4:
                edge.seam = True
                
    # Add a vertical seam to allow the outer cylinder to unroll perfectly
    vertical_edges = [e for e in bm.edges if abs(e.verts[0].co.z - e.verts[1].co.z) > (scale * 0.5) and not e.seam]
    if vertical_edges:
        vertical_edges[0].seam = True

    bm.to_mesh(mesh)
    bm.free()

    # === Step 3: Unwrap & Pack ===
    # Set context for unwrapping
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    current_mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Unwrap using Angle Based method. Passing a margin automatically packs the islands.
    try:
        bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.025)
    except RuntimeError as e:
        print(f"UV Unwrap failed (this can happen in headless environments): {e}")
        
    bpy.ops.object.mode_set(mode=current_mode)

    # === Step 4: Diagnostic UV Material Setup ===
    mat_name = "UV_Diagnostic_Grid"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        # 4a. Create or retrieve the Generated Image
        img_name = "Diagnostic_Color_Grid"
        img = bpy.data.images.get(img_name)
        if not img:
            img = bpy.data.images.new(img_name, width=1024, height=1024)
            img.generated_type = 'COLOR_GRID' # Generates the testing grid shown in tutorial
        
        # 4b. Build Node Tree
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (300, 0)
        
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 0)
        bsdf.inputs['Roughness'].default_value = 0.5
        
        tex_img = nodes.new('ShaderNodeTexImage')
        tex_img.image = img
        tex_img.location = (-300, 0)
        
        # Replicate Node Wrangler mapping setup
        tex_coord = nodes.new('ShaderNodeTexCoord')
        tex_coord.location = (-500, 0)
        
        links.new(tex_coord.outputs['UV'], tex_img.inputs['Vector'])
        links.new(tex_img.outputs['Color'], bsdf.inputs['Base Color'])
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Apply material to object
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    # Position object
    obj.location = Vector(location)

    return f"Created UV mapped '{object_name}' at {location} with marked seams and packed islands."
