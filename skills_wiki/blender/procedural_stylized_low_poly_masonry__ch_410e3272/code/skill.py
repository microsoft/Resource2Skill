def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedWellBase",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.55, 0.52, 0.58),
    **kwargs
) -> str:
    """
    Create a procedural, stylized low-poly stone ring (e.g., for a well base).

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created parent object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the stones.
        **kwargs: Overrides for 'layers', 'radius', 'stone_thickness', etc.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Matrix, Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Configure parameters
    layers = kwargs.get('layers', 3)
    radius = kwargs.get('radius', 1.5)
    layer_height = kwargs.get('layer_height', 0.4)
    stone_thickness = kwargs.get('stone_thickness', 0.5)
    wobble_strength = kwargs.get('wobble_strength', 0.1)
    chisel_ratio = kwargs.get('chisel_ratio', 0.15)
    gap_factor = kwargs.get('gap_factor', 0.1)
    
    # === Step 1: Initialize Parent & Shared Resources ===
    parent_obj = bpy.data.objects.new(object_name, None)
    parent_obj.location = Vector(location)
    parent_obj.scale = (scale, scale, scale)
    scene.collection.objects.link(parent_obj)
    
    # Shared noise texture for displacement
    tex_name = "StylizedStoneNoise"
    tex = bpy.data.textures.get(tex_name)
    if not tex:
        tex = bpy.data.textures.new(name=tex_name, type='CLOUDS')
        tex.noise_scale = 0.6
        
    # Shared material
    mat_name = object_name + "_StoneMat"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.9
            # Handle API variations between Blender 3.x and 4.x
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.1
            elif 'Specular' in bsdf.inputs:
                bsdf.inputs['Specular'].default_value = 0.1
    
    stones_created = 0
    
    # === Step 2: Procedural Ring Generation ===
    for layer in range(layers):
        # Slightly vary the radius per layer for an organic stacked look
        current_rad = radius + random.uniform(-0.05, 0.05)
        num_stones = random.randint(12, 15)
        stones_created += num_stones
        
        mesh_name = f"{object_name}_Ring_{layer}"
        mesh = bpy.data.meshes.new(mesh_name)
        obj = bpy.data.objects.new(mesh_name, mesh)
        scene.collection.objects.link(obj)
        
        bm = bmesh.new()
        
        # Calculate random proportions ensuring they sum to exactly a full circle
        stone_weights = [random.uniform(0.8, 1.2) for _ in range(num_stones)]
        total_weight = sum(stone_weights)
        angles = [(w / total_weight) * 2 * math.pi for w in stone_weights]
        
        current_angle = 0.0
        for i in range(num_stones):
            arc_angle = angles[i]
            arc_length = arc_angle * current_rad
            
            # Dimensions
            sl = arc_length * (1.0 - gap_factor) # Leave space between stones
            sw = stone_thickness * random.uniform(0.85, 1.15)
            sh = layer_height * random.uniform(0.85, 1.15)
            
            start_v = len(bm.verts)
            bmesh.ops.create_cube(bm, size=1.0)
            cube_verts = bm.verts[start_v:]
            
            # Scale primitive to brick shape
            bmesh.ops.scale(bm, vec=(sl, sw, sh), verts=cube_verts)
            
            # Orient and Position:
            # Move out along Y by radius, then rotate around Z
            # This perfectly aligns the cube's length (X) tangent to the circle
            angle_offset = current_angle + (arc_angle / 2)
            trans_mat = Matrix.Translation((0, current_rad, 0))
            rot_mat = Matrix.Rotation(angle_offset, 4, 'Z')
            
            bmesh.ops.transform(bm, matrix=rot_mat @ trans_mat, verts=cube_verts)
            current_angle += arc_angle
            
        bm.to_mesh(mesh)
        bm.free()
        
        # === Step 3: Stylized Chiseled Modifier Stack ===
        
        # A. Add internal geometry without smoothing
        subsurf = obj.modifiers.new(name="Subdivide", type='SUBSURF')
        subsurf.subdivision_type = 'SIMPLE'
        subsurf.levels = 3
        
        # B. Round off sharp 90-degree outer corners
        bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
        bevel.segments = 2
        bevel.width = 0.08
        bevel.limit_method = 'ANGLE'
        bevel.angle_limit = math.radians(60)
        
        # C. Add organic wobble (Global coords so stacked layers look different)
        displace = obj.modifiers.new(name="Displace", type='DISPLACE')
        displace.texture = tex
        displace.strength = wobble_strength
        displace.texture_coords = 'GLOBAL'  
        
        # D. Collapse into stark, low-poly planar facets
        decimate = obj.modifiers.new(name="Decimate", type='DECIMATE')
        decimate.ratio = chisel_ratio
        
        # === Step 4: Finalization ===
        for poly in mesh.polygons:
            poly.use_smooth = False
            
        obj.data.materials.append(mat)
        
        # Parent and stack layers
        obj.parent = parent_obj
        obj.location = (0, 0, layer * layer_height)
        
        # Rotate each layer so the vertical gaps stagger like real brickwork
        obj.rotation_euler[2] = (layer * (2 * math.pi / 2.5)) + random.uniform(-0.15, 0.15)
        
    return f"Created '{object_name}' at {location}: {layers} layers containing {stones_created} stylized chiseled stones."
