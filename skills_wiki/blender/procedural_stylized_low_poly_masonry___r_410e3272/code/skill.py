def create_stylized_stone_well_base(
    scene_name: str = "Scene",
    object_name: str = "StylizedWellBase",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.55, 0.50, 0.55),
    radius: float = 1.5,
    tiers: int = 3,
    **kwargs
) -> str:
    """
    Create a stylized, low-poly stone well base in the active Blender scene.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created joined object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the stones.
        radius: Inner radius of the base ring.
        tiers: Number of vertical stone layers.
        
    Returns:
        Status string confirming creation.
    """
    import bpy
    import random
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Stone Material ===
    mat_name = f"{object_name}_StoneMat"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.9

    # === Step 2: Procedural Noise Texture for Displacement ===
    tex_name = f"{object_name}_Noise"
    tex = bpy.data.textures.get(tex_name)
    if not tex:
        tex = bpy.data.textures.new(tex_name, type='CLOUDS')
        tex.noise_scale = 0.4

    stones = []
    
    # Base stone dimensions
    stone_length = 0.8
    stone_depth = 0.4
    stone_height = 0.35

    # === Step 3: Generate Tiered Rings ===
    for tier in range(tiers):
        # Slightly taper the rings inwards as they go up
        current_radius = radius - (tier * 0.05) 
        circumference = 2 * math.pi * current_radius
        
        # Calculate how many stones fit in this tier
        num_stones = max(4, int(circumference / stone_length))
        angle_step = (2 * math.pi) / num_stones
        
        # Z-position for the tier (with slight vertical overlap)
        tier_z = tier * stone_height * 0.9 
        
        for i in range(num_stones):
            # Calculate polar coordinates with jitter for organic placement
            angle_jitter = random.uniform(-0.05, 0.05)
            rad_jitter = random.uniform(-0.05, 0.05)
            final_angle = (i * angle_step) + angle_jitter
            final_rad = current_radius + rad_jitter
            
            x = final_rad * math.cos(final_angle)
            y = final_rad * math.sin(final_angle)
            
            # Create base primitive
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, tier_z))
            stone = bpy.context.active_object
            stone.name = f"{object_name}_Stone_T{tier}_{i}"
            
            # Apply individual random scaling
            sl = stone_length * random.uniform(0.85, 1.15)
            sd = stone_depth * random.uniform(0.85, 1.15)
            sh = stone_height * random.uniform(0.85, 1.15)
            stone.scale = (sl, sd, sh)
            
            # Rotate to face outward, with slight tumbling
            stone.rotation_euler[2] = final_angle + (math.pi / 2)
            stone.rotation_euler[0] = random.uniform(-0.08, 0.08)
            stone.rotation_euler[1] = random.uniform(-0.08, 0.08)
            
            # Isolate selection to apply scale safely
            bpy.ops.object.select_all(action='DESELECT')
            stone.select_set(True)
            bpy.context.view_layer.objects.active = stone
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # === Step 4: Stylization Modifier Stack ===
            # A. Round sharp edges
            mod_bevel = stone.modifiers.new(name="Bevel", type='BEVEL')
            mod_bevel.width = 0.04
            mod_bevel.segments = 2
            
            # B. Add vertex density for displacement
            mod_subd = stone.modifiers.new(name="Subsurf", type='SUBSURF')
            mod_subd.subdivision_type = 'SIMPLE'
            mod_subd.levels = 3
            
            # C. Warp the shape organically
            mod_disp = stone.modifiers.new(name="Displace", type='DISPLACE')
            mod_disp.texture = tex
            mod_disp.strength = random.uniform(0.04, 0.08)
            mod_disp.texture_coords = 'GLOBAL' # Ensures unique noise per stone location
            
            # D. Collapse into faceted low-poly style
            mod_dec = stone.modifiers.new(name="Decimate", type='DECIMATE')
            mod_dec.decimate_type = 'COLLAPSE'
            mod_dec.ratio = random.uniform(0.2, 0.4)
            
            # Apply modifiers to bake the geometry
            for mod in stone.modifiers:
                bpy.ops.object.modifier_apply(modifier=mod.name)
            
            # Assign material
            stone.data.materials.append(mat)
            
            # Ensure flat shading is active
            for poly in stone.data.polygons:
                poly.use_smooth = False
                
            stones.append(stone)

    # === Step 5: Final Assembly ===
    # Join all generated stones into a single mesh
    bpy.ops.object.select_all(action='DESELECT')
    for stone in stones:
        stone.select_set(True)
    
    bpy.context.view_layer.objects.active = stones[0]
    bpy.ops.object.join()
    
    final_obj = bpy.context.active_object
    final_obj.name = object_name
    
    # Set final transforms
    final_obj.location = Vector(location)
    final_obj.scale = (scale, scale, scale)
    
    # Clear selection
    bpy.ops.object.select_all(action='DESELECT')
    
    return f"Created '{object_name}' with {tiers} tiers and {len(stones)} stylized stones at {location}."
