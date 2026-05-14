def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedHead",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.4, 0.3),
    **kwargs,
) -> str:
    """
    Create a procedural stylized head base in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base skin color in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    # Target scene and collection
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    target_collection = scene.collection
    
    # === Step 1: Create Base Head Mesh ===
    mesh = bpy.data.meshes.new(object_name)
    obj = bpy.data.objects.new(object_name, mesh)
    target_collection.objects.link(obj)
    
    bm = bmesh.new()
    # High-density base to mimic the sculpting remesh workflow
    bmesh.ops.create_icosphere(bm, subdivisions=4, radius=1.0)
    
    # Procedural "Grab Brush" application via spatial falloffs
    for v in bm.verts:
        x, y, z = v.co.x, v.co.y, v.co.z
        
        # 1. Jaw and Chin (Pull down and forward)
        if z < -0.1:
            inf = min(1.0, (-z - 0.1) / 0.9)
            z -= inf * 0.7 
            y -= inf * 0.25 
            x *= (1.0 - inf * 0.35) # Narrow the jaw
            
        # 2. Cranium (Bulbous expansion at top)
        if z > 0.1:
            inf = min(1.0, (z - 0.1) / 0.9)
            x *= (1.0 + inf * 0.15)
            y *= (1.0 + inf * 0.2)
            z += inf * 0.2
            
        # 3. Nose (Pull outwards at front middle)
        dist_nose = Vector((x, y + 0.8, z + 0.1)).length
        if dist_nose < 0.6:
            inf = (1.0 - (dist_nose / 0.6)) ** 2
            y -= inf * 0.6
            z -= inf * 0.15
                
        # 4. Eye Sockets (Push geometry inwards to make room for eyeballs)
        dist_l = Vector((x - 0.35, y + 0.7, z - 0.2)).length
        dist_r = Vector((x + 0.35, y + 0.7, z - 0.2)).length
        if dist_l < 0.35:
            inf = (1.0 - (dist_l / 0.35)) ** 2
            y += inf * 0.3
        if dist_r < 0.35:
            inf = (1.0 - (dist_r / 0.35)) ** 2
            y += inf * 0.3
            
        # 5. Ears (Pull outwards at sides)
        dist_ear_l = Vector((x - 0.8, y - 0.1, z)).length
        dist_ear_r = Vector((x + 0.8, y - 0.1, z)).length
        if dist_ear_l < 0.4:
            inf = (1.0 - (dist_ear_l / 0.4)) ** 2
            x += inf * 0.45
            y -= inf * 0.15
            z += inf * 0.15
        if dist_ear_r < 0.4:
            inf = (1.0 - (dist_ear_r / 0.4)) ** 2
            x -= inf * 0.45
            y -= inf * 0.15
            z += inf * 0.15
            
        # 6. Neck (Pull down bottom back/center)
        if z < -0.6 and abs(x) < 0.4 and y > -0.3:
            inf = min(1.0, (-z - 0.6) / 0.6)
            z -= inf * 0.6
            y += inf * 0.2

        v.co = Vector((x, y, z))

    bm.to_mesh(mesh)
    bm.free()
    
    # Set smooth shading
    for poly in mesh.polygons:
        poly.use_smooth = True
        
    # Add subdivision to mimic the smooth "Remesh" look
    subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.levels = 1
    subdiv.render_levels = 2
    
    # === Step 2: Build Materials ===
    # Skin Material
    skin_mat = bpy.data.materials.new(name=f"{object_name}_Skin")
    skin_mat.use_nodes = True
    bsdf = skin_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.45
        # Attempt to add Subsurface Scattering safely across Blender versions
        if 'Subsurface Weight' in bsdf.inputs:
            bsdf.inputs['Subsurface Weight'].default_value = 0.15
        elif 'Subsurface' in bsdf.inputs:
            bsdf.inputs['Subsurface'].default_value = 0.15
    obj.data.materials.append(skin_mat)
    
    # Eye Material
    eye_mat = bpy.data.materials.new(name=f"{object_name}_Eye")
    eye_mat.use_nodes = True
    eye_bsdf = eye_mat.node_tree.nodes.get("Principled BSDF")
    if eye_bsdf:
        eye_bsdf.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1.0)
        eye_bsdf.inputs['Roughness'].default_value = 0.1
        
    # === Step 3: Create & Parent Eyes ===
    eye_locs = [(0.35, -0.62, 0.2), (-0.35, -0.62, 0.2)]
    created_objects = [obj]
    
    for i, eloc in enumerate(eye_locs):
        eye_name = f"{object_name}_Eye_{'L' if i==0 else 'R'}"
        emesh = bpy.data.meshes.new(eye_name)
        eye_obj = bpy.data.objects.new(eye_name, emesh)
        target_collection.objects.link(eye_obj)
        
        ebm = bmesh.new()
        bmesh.ops.create_uvsphere(ebm, u_segments=32, v_segments=16, radius=0.12)
        ebm.to_mesh(emesh)
        ebm.free()
        
        for poly in emesh.polygons:
            poly.use_smooth = True
            
        eye_obj.data.materials.append(eye_mat)
        eye_obj.parent = obj
        eye_obj.location = eloc
        created_objects.append(eye_obj)
        
    # === Step 4: Finalize Transform ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    return f"Created '{object_name}' at {location} with {len(created_objects)} linked objects (Head + Eyes)."
