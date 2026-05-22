def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyPine",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.4, 0.1),
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Pine Tree in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the foliage in 0-1 range.
        **kwargs: 
            layers (int): Number of foliage tiers (default: 3).

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    
    # === Step 1: Initialize Mesh and Object ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    bm = bmesh.new()
    
    trunk_mat_idx = 0
    foliage_mat_idx = 1
    
    # === Step 2: Create the Trunk ===
    trunk_radius = 0.4 * scale
    trunk_height = 2.5 * scale
    segments = 12
    
    ret = bmesh.ops.create_cone(
        bm, 
        cap_ends=True, 
        cap_tris=False, 
        segments=segments, 
        radius1=trunk_radius, 
        radius2=trunk_radius * 0.4, # Taper top
        depth=trunk_height
    )
    trunk_verts = ret['verts']
    
    # Translate so the base of the trunk sits flat on Z=0
    bmesh.ops.translate(bm, verts=trunk_verts, vec=(0, 0, trunk_height / 2.0))
    
    for v in trunk_verts:
        for f in v.link_faces:
            f.material_index = trunk_mat_idx

    # === Step 3: Create the Foliage Layers ===
    layers = kwargs.get('layers', 3)
    base_foliage_radius = 1.8 * scale
    foliage_height = 2.0 * scale
    
    # Start foliage partway up the trunk
    current_z = trunk_height * 0.4 
    
    for i in range(layers):
        # Scale each tier down as we go up
        layer_scale = 1.0 - (i * (1.0 / (layers + 1.5))) 
        radius = base_foliage_radius * layer_scale
        height = foliage_height * layer_scale
        
        # 3a. Create base cone for this tier
        ret = bmesh.ops.create_cone(
            bm, 
            cap_ends=True, 
            cap_tris=False, 
            segments=segments, 
            radius1=radius, 
            radius2=radius * 0.1, # Pointy but flat top
            depth=height
        )
        layer_verts = ret['verts']
        
        # Translate to correct Z height (offset by half height since origin is center)
        bmesh.ops.translate(bm, verts=layer_verts, vec=(0, 0, current_z + height / 2.0))
        
        for v in layer_verts:
            for f in v.link_faces:
                f.material_index = foliage_mat_idx
                
        # 3b. Add Rim Detail (Mimicking Extrude & Scale inward/outward)
        bottom_face = None
        for v in layer_verts:
            for f in v.link_faces:
                # Identify the large bottom-facing polygon
                if len(f.verts) >= segments and f.normal.z < -0.9:
                    if abs(f.calc_center_bounds().z - current_z) < 0.1 * scale:
                        bottom_face = f
                        break
            if bottom_face:
                break
        
        if bottom_face:
            # First Extrude: Inset inwards to create thickness
            res = bmesh.ops.extrude_discrete_faces(bm, faces=[bottom_face])
            new_bottom = res['faces'][0]
            center = new_bottom.calc_center_bounds()
            
            for v in new_bottom.verts:
                v.co.x = center.x + (v.co.x - center.x) * 0.5
                v.co.y = center.y + (v.co.y - center.y) * 0.5
                
            # Second Extrude: Pull down and flare outwards for the overhanging leaf rim
            res2 = bmesh.ops.extrude_discrete_faces(bm, faces=[new_bottom])
            final_bottom = res2['faces'][0]
            center2 = final_bottom.calc_center_bounds()
            down_dist = height * 0.15
            
            for v in final_bottom.verts:
                v.co.z -= down_dist
                v.co.x = center2.x + (v.co.x - center2.x) * 1.3
                v.co.y = center2.y + (v.co.y - center2.y) * 1.3
                
        # Advance Z for the next overlapping layer
        current_z += height * 0.55
        
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    
    # Ensure flat shading for the faceted low-poly look
    for f in mesh.polygons:
        f.use_smooth = False
    mesh.update()
    
    # === Step 4: Materials Setup ===
    # Trunk Material
    mat_trunk = bpy.data.materials.new(name=f"{object_name}_Trunk")
    mat_trunk.use_nodes = True
    bsdf_trunk = mat_trunk.node_tree.nodes.get("Principled BSDF")
    if bsdf_trunk:
        bsdf_trunk.inputs['Base Color'].default_value = (0.15, 0.07, 0.03, 1.0)
        bsdf_trunk.inputs['Roughness'].default_value = 0.9

    # Foliage Material
    mat_foliage = bpy.data.materials.new(name=f"{object_name}_Foliage")
    mat_foliage.use_nodes = True
    bsdf_foliage = mat_foliage.node_tree.nodes.get("Principled BSDF")
    if bsdf_foliage:
        bsdf_foliage.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf_foliage.inputs['Roughness'].default_value = 0.85
        
    obj.data.materials.append(mat_trunk)
    obj.data.materials.append(mat_foliage)
    
    # === Step 5: Final Positioning ===
    obj.location = Vector(location)
    obj.name = object_name
    
    return f"Created '{object_name}' (Stylized Low-Poly Tree) at {location} with {layers} foliage tiers."
