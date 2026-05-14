def create_stylized_stone_well(
    scene_name: str = "Scene",
    object_name: str = "StylizedWellBase",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.45, 0.42, 0.48),
    **kwargs
) -> str:
    """
    Create a procedural, stylized low-poly stone ring (like a well base).
    Uses a modifier stack to simulate hand-sculpted, faceted stonework.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the stone.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Matrix

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # 1. Create Parent Empty
    parent_obj = bpy.data.objects.new(object_name, None)
    scene.collection.objects.link(parent_obj)
    parent_obj.location = location
    parent_obj.scale = (scale, scale, scale)
    
    # 2. Setup Material
    mat_name = f"{object_name}_StoneMat"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.85
            bsdf.inputs['Specular IOR Level'].default_value = 0.2
            
    # 3. Setup Noise Texture for Displacement
    tex_name = f"{object_name}_WobbleNoise"
    tex = bpy.data.textures.get(tex_name)
    if not tex:
        tex = bpy.data.textures.new(tex_name, 'CLOUDS')
        tex.noise_scale = 0.5
        
    # --- Generation Parameters ---
    radius = kwargs.get('radius', 1.2)
    layers = kwargs.get('layers', 3)
    stones_per_layer = kwargs.get('stones_per_layer', 12)
    stone_h = 0.35
    stone_d = 0.4
    # Calculate length to fit circumference with a small gap
    stone_l = (2 * math.pi * radius) / stones_per_layer * 0.9 
    
    created_objects = 0
    
    # 4. Generate Layers
    for layer_idx in range(layers):
        mesh = bpy.data.meshes.new(f"{object_name}_Layer_{layer_idx}")
        layer_obj = bpy.data.objects.new(f"{object_name}_Layer_{layer_idx}", mesh)
        scene.collection.objects.link(layer_obj)
        layer_obj.parent = parent_obj
        layer_obj.data.materials.append(mat)
        created_objects += 1
        
        bm = bmesh.new()
        
        # Layer shape logic (middle layer slightly smaller, top layer larger)
        if layer_idx == 0:
            layer_radius = radius
            decimate_ratio = 0.3
        elif layer_idx == 1:
            layer_radius = radius * 0.95
            decimate_ratio = 0.35 # Slightly more fragmented
        else:
            layer_radius = radius * 1.05
            decimate_ratio = 0.25 # Chunkier
            
        layer_z = layer_idx * stone_h
        angle_step = 2 * math.pi / stones_per_layer
        offset = (angle_step / 2.0) if layer_idx % 2 == 1 else 0.0
        
        for i in range(stones_per_layer):
            # Random chances for ruined/irregular look
            if random.random() < 0.05: # 5% chance to skip a stone completely
                continue
                
            angle = i * angle_step + offset
            
            # Base dimensions
            l = stone_l * random.uniform(0.85, 1.15)
            d = stone_d * random.uniform(0.8, 1.2)
            h = stone_h * random.uniform(0.85, 1.1)
            
            # 15% chance for a uniquely small block
            if random.random() < 0.15:
                l *= random.uniform(0.4, 0.6)
                h *= random.uniform(0.7, 0.9)
                angle += random.uniform(-0.1, 0.1)
            
            # Create cube in BMesh
            ret = bmesh.ops.create_cube(bm, size=1.0)
            verts = ret['verts']
            
            # Scale locally
            for v in verts:
                v.co.x *= l
                v.co.y *= d
                v.co.z *= h
                
            # Move to circle perimeter
            rot_mat = Matrix.Rotation(angle, 4, 'Z')
            # Add slight tilt randomization
            tilt_mat = Matrix.Rotation(random.uniform(-0.05, 0.05), 4, 'X') @ Matrix.Rotation(random.uniform(-0.05, 0.05), 4, 'Y')
            trans_mat = Matrix.Translation((layer_radius * math.cos(angle), layer_radius * math.sin(angle), layer_z))
            
            transform_mat = trans_mat @ rot_mat @ tilt_mat
            
            for v in verts:
                v.co = transform_mat @ v.co
                
        # Ensure flat shading for the low-poly look
        for f in bm.faces:
            f.smooth = False
            
        bm.to_mesh(mesh)
        bm.free()
        
        # --- The Stylized Stone Modifier Stack ---
        
        # 1. Bevel: Softens the harsh cube edges
        mod_bevel = layer_obj.modifiers.new("Bevel", 'BEVEL')
        mod_bevel.width = 0.06
        mod_bevel.segments = 2
        mod_bevel.profile = 0.5
        
        # 2. Subdiv: Adds internal topology required for displacement
        mod_subdiv = layer_obj.modifiers.new("Subdiv", 'SUBSURF')
        mod_subdiv.subdivision_type = 'SIMPLE'
        mod_subdiv.levels = 3
        mod_subdiv.render_levels = 3
        
        # 3. Displace: Randomizes vertices for organic, wobbly unevenness
        mod_displace = layer_obj.modifiers.new("Displace", 'DISPLACE')
        mod_displace.texture = tex
        mod_displace.strength = random.uniform(0.06, 0.1)
        mod_displace.mid_level = 0.5
        
        # 4. Decimate: Collapses the wobbly mesh into sharp, triangulated facets
        mod_decimate = layer_obj.modifiers.new("Decimate", 'DECIMATE')
        mod_decimate.ratio = decimate_ratio
        mod_decimate.use_collapse_triangulate = True

    return f"Created '{object_name}' (Stylized Stone Well) at {location} with {created_objects} layer objects."
