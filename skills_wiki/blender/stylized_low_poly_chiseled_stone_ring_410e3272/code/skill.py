def create_low_poly_well_base(
    scene_name: str = "Scene",
    object_name: str = "LowPolyWellBase",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.55, 0.52, 0.58),
    radius: float = 1.2,
    layers: int = 4,
    stones_per_layer: int = 12,
    layer_height: float = 0.25,
    stone_depth: float = 0.25,
    taper_amount: float = 0.05,
    **kwargs
) -> str:
    """
    Create a stylized, low-poly chiseled stone well base.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the stone.
        radius: Base radius of the well.
        layers: Number of vertical stone layers.
        stones_per_layer: Number of stones in each circular ring.
        layer_height: Vertical thickness of each stone layer.
        stone_depth: Radial depth/thickness of the stones.
        taper_amount: How much the radius decreases per layer (for a tapered well).

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector, Euler, Matrix

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Create Base Mesh and Object ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    bm = bmesh.new()
    
    # === Step 2: Procedural Stone Placement ===
    for layer in range(layers):
        z_offset = layer * layer_height
        
        # Stagger every other layer (Running Bond pattern)
        layer_rot_offset = (math.pi / stones_per_layer) if layer % 2 == 1 else 0
        current_radius = radius - (layer * taper_amount)
        
        for i in range(stones_per_layer):
            angle = (i / stones_per_layer) * 2 * math.pi + layer_rot_offset
            
            # Stone dimensions with slight variation
            circumference = 2 * math.pi * current_radius
            stone_width = (circumference / stones_per_layer) * random.uniform(0.85, 0.95)
            
            sx = stone_width
            sy = stone_depth * random.uniform(0.8, 1.2)
            sz = layer_height * random.uniform(0.85, 0.95)
            
            # Position with slight wobble to prevent perfect alignment
            loc_x = current_radius * math.cos(angle) + random.uniform(-0.02, 0.02)
            loc_y = current_radius * math.sin(angle) + random.uniform(-0.02, 0.02)
            loc_z = z_offset + random.uniform(-0.02, 0.02)
            
            # Rotations (facing outward tangentially, plus slight random tilt)
            rot_z = angle + math.pi / 2 + random.uniform(-0.05, 0.05)
            rot_y = random.uniform(-0.05, 0.05)
            rot_x = random.uniform(-0.05, 0.05)
            
            loc_vec = Vector((loc_x, loc_y, loc_z))
            rot_mat = Euler((rot_x, rot_y, rot_z), 'XYZ').to_matrix().to_4x4()
            scale_mat = Matrix.Diagonal((sx, sy, sz, 1.0))
            
            transform_mat = Matrix.Translation(loc_vec) @ rot_mat @ scale_mat
            
            # Create cube and transform it at the vertex level
            geom = bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.transform(bm, matrix=transform_mat, verts=geom['verts'])
            
    bm.to_mesh(mesh)
    bm.free()
    
    # Flat Shading (Crucial for Low Poly look)
    for poly in mesh.polygons:
        poly.use_smooth = False
    
    # === Step 3: Procedural Chiseling Modifier Stack ===
    
    # 1. Bevel: Rounds the perfect cube corners
    bevel = obj.modifiers.new(name="Bevel_Corners", type='BEVEL')
    bevel.width = 0.03
    bevel.segments = 1
    
    # 2. Simple Subdivision: Adds geometry to be displaced
    subd = obj.modifiers.new(name="Add_Topology", type='SUBSURF')
    subd.subdivision_type = 'SIMPLE'
    subd.levels = 2
    
    # 3. Displace: Adds the wobble/damage
    tex = bpy.data.textures.new(object_name + "_Noise", type='CLOUDS')
    tex.noise_scale = 0.15
    
    disp = obj.modifiers.new(name="Stone_Damage", type='DISPLACE')
    disp.texture = tex
    disp.strength = 0.07
    
    # 4. Decimate: Collapses dense wobbles into sharp low-poly facets
    dec = obj.modifiers.new(name="Low_Poly_Chisel", type='DECIMATE')
    dec.decimate_type = 'COLLAPSE'
    dec.ratio = 0.25 
    
    # === Step 4: Material Setup ===
    mat = bpy.data.materials.new(name=object_name + "_StoneMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.85
        # Ensure it looks matte and stony
        if 'Specular IOR Level' in bsdf.inputs: # Blender 4.0+
            bsdf.inputs['Specular IOR Level'].default_value = 0.1
        elif 'Specular' in bsdf.inputs: # Blender 3.x
            bsdf.inputs['Specular'].default_value = 0.1
            
    obj.data.materials.append(mat)
    
    # === Step 5: Final Placement ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    return f"Created '{object_name}' at {location} with {layers * stones_per_layer} chiseled low-poly stones."
