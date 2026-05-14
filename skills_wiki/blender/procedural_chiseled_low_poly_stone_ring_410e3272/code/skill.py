def create_stylized_stone_ring(
    scene_name: str = "Scene",
    object_name: str = "WellBase",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.45, 0.40, 0.48),
    layers: int = 3,
    radius: float = 1.2,
    **kwargs,
) -> str:
    """
    Creates a stylized, chiseled low-poly stone ring (e.g., for a well base) using procedural displacement and decimation.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created ring object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: Base color of the stylized stone.
        layers: Number of stacked stone rows.
        radius: The inner radius of the stone ring.

    Returns:
        Status string.
    """
    import bpy
    import math
    import random
    import mathutils

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 1. Create Stylized Material ---
    mat = bpy.data.materials.new(name=f"{object_name}_StoneMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.9
        bsdf.inputs['Specular IOR Level'].default_value = 0.2

    # --- 2. Setup Procedural Noise Texture ---
    tex_name = f"{object_name}_Noise"
    tex = bpy.data.textures.get(tex_name)
    if not tex:
        tex = bpy.data.textures.new(tex_name, 'CLOUDS')
        tex.noise_scale = 0.6

    stones = []
    num_stones_per_layer = 12
    stone_gap = 0.04
    perimeter = 2 * math.pi * radius
    base_len = (perimeter / num_stones_per_layer) - stone_gap
    base_height = 0.3

    # Ensure we don't accidentally join pre-existing selected objects
    bpy.ops.object.select_all(action='DESELECT')

    # --- 3. Generate Stones ---
    for layer in range(layers):
        # Stagger every other layer to create an interlocking brick pattern
        layer_offset_angle = (math.pi / num_stones_per_layer) if layer % 2 != 0 else 0
        z_pos = layer * base_height

        for i in range(num_stones_per_layer):
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
            stone = bpy.context.active_object
            
            # Randomize dimensions slightly for organic variation
            slen = base_len + random.uniform(-0.02, 0.05)
            swidth = 0.35 + random.uniform(-0.04, 0.06)
            sheight = base_height + random.uniform(-0.02, 0.02)
            
            stone.scale = (slen, swidth, sheight)
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            # A. Bevel to soften perfect cube edges
            bev = stone.modifiers.new("Bevel", 'BEVEL')
            bev.width = 0.05
            bev.segments = 2

            # B. Subdivide to give geometry for displacement
            subd = stone.modifiers.new("Subd", 'SUBSURF')
            subd.levels = 2

            # C. Displace with noise to create organic wobbliness
            disp = stone.modifiers.new("Disp", 'DISPLACE')
            disp.texture = tex
            disp.strength = 0.05
            disp.texture_coords = 'GLOBAL' # Global ensures each stone gets a unique noise slice

            # Apply modifiers immediately to bake the high-poly organic shape
            bpy.context.view_layer.objects.active = stone
            bpy.ops.object.modifier_apply(modifier="Bevel")
            bpy.ops.object.modifier_apply(modifier="Subd")
            bpy.ops.object.modifier_apply(modifier="Disp")

            # Calculate circular masonry placement
            angle = i * (2 * math.pi / num_stones_per_layer) + layer_offset_angle
            stone.location = (
                math.sin(angle) * radius,
                math.cos(angle) * radius,
                z_pos + (sheight / 2)
            )
            # Rotate so the length follows the tangent of the circle
            stone.rotation_euler = (0, 0, -angle)

            stone.data.materials.append(mat)
            bpy.ops.object.shade_flat() # Crucial for the low-poly faceted look
            stones.append(stone)

    # --- 4. Assemble and Apply the Secret Sauce (Decimate) ---
    # Select all generated stones and join them
    for s in stones:
        s.select_set(True)
    bpy.context.view_layer.objects.active = stones[0]
    bpy.ops.object.join()

    ring = bpy.context.active_object
    ring.name = object_name

    # The joined object's origin is at the location of stones[0].
    # We mathematically shift the origin to (0,0,0) at the base of the well.
    saved_loc = ring.location.copy()
    ring.location = (0, 0, 0)
    ring.data.transform(mathutils.Matrix.Translation(saved_loc))

    # Apply the Decimate modifier. 
    # This collapses the smooth, wobbly displaced geometry into sharp, irregular planar facets.
    dec = ring.modifiers.new("Decimate", 'DECIMATE')
    dec.ratio = 0.35 # Keep 35% of faces - adjust this for more/less aggressive low-poly styling
    
    # --- 5. Final Placement & Scaling ---
    ring.scale = (scale, scale, scale)
    ring.location = location
    
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created stylized low-poly '{object_name}' with {layers} layers at {location}."
