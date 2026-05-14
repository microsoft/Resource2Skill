def create_stylized_stone_ring(
    scene_name: str = "Scene",
    object_name: str = "StylizedWellBase",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.55, 0.55, 0.60),
    radius: float = 1.5,
    stone_count: int = 12,
    layers: int = 3,
    **kwargs
) -> str:
    """
    Creates a stylized, low-poly chiseled stone ring using a procedural modifier stack.
    
    Args:
        scene_name: Name of the scene to add the object to.
        object_name: Base name for the generated objects.
        location: (x, y, z) coordinates for the center base of the ring.
        scale: Uniform scaling factor for the stones.
        material_color: (R, G, B) color of the stones.
        radius: Inner radius of the stone ring.
        stone_count: Number of stones per layer.
        layers: Number of stacked stone layers.
        
    Returns:
        A status string describing the outcome.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 1. Material Setup ---
    mat_name = f"{object_name}_Mat"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.85
            # Handle Blender 4.0+ vs older versions for Specular
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.2
            elif 'Specular' in bsdf.inputs:
                bsdf.inputs['Specular'].default_value = 0.2

    # --- 2. Procedural Noise Texture ---
    tex_name = f"{object_name}_Noise"
    tex = bpy.data.textures.get(tex_name)
    if not tex:
        tex = bpy.data.textures.new(name=tex_name, type='CLOUDS')
        tex.noise_scale = 0.7 * scale

    # --- 3. Center Origin Empty (Crucial for perfect circular deformation) ---
    empty = bpy.data.objects.new(f"{object_name}_Center", None)
    empty.empty_display_type = 'PLAIN_AXES'
    empty.empty_display_size = 0.5 * scale
    empty.location = location
    scene.collection.objects.link(empty)

    # --- 4. Mathematical Dimensional Setup ---
    circumference = 2 * math.pi * (radius * scale)
    brick_length = circumference / stone_count
    
    gap_ratio = 0.05
    actual_brick_len = brick_length * (1.0 - gap_ratio)
    brick_depth = 0.45 * scale
    brick_height = 0.35 * scale

    # To cleanly bend 360 degrees, the X-span of the array must perfectly match the arc length.
    array_length = (stone_count - 1) * brick_length + actual_brick_len
    effective_radius = array_length / (2 * math.pi)

    created_layers = []

    # --- 5. Generate Layers ---
    for layer in range(layers):
        # Create Mesh and Object
        mesh = bpy.data.meshes.new(f"{object_name}_Mesh_{layer}")
        brick_obj = bpy.data.objects.new(f"{object_name}_Layer_{layer}", mesh)
        scene.collection.objects.link(brick_obj)
        
        brick_obj.location = location
        brick_obj.data.materials.append(mat)

        # Build local geometry
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        
        # Scale to brick proportions
        bmesh.ops.scale(bm, vec=(actual_brick_len, brick_depth, brick_height), verts=bm.verts)

        # Offset geometry: Center the line on X, offset on Y by the required bend radius
        start_x = -(array_length / 2.0) + (actual_brick_len / 2.0)
        layer_z = layer * brick_height * 1.05  # 5% vertical gap between layers
        
        bmesh.ops.translate(bm, vec=(start_x, effective_radius, layer_z), verts=bm.verts)
        
        bm.to_mesh(mesh)
        bm.free()

        # Stagger every other layer by rotating the object itself
        # This keeps the deform math clean while creating visual interlocking
        if layer % 2 == 1:
            stagger_angle = (2 * math.pi / stone_count) / 2.0
            brick_obj.rotation_euler[2] = stagger_angle

        # --- 6. Build the Procedural Modifier Stack ---
        
        # A) Bevel: Soften base cube
        mod_bevel = brick_obj.modifiers.new(name="Bevel", type='BEVEL')
        mod_bevel.width = 0.06 * scale
        mod_bevel.segments = 2

        # B) Subdiv: Add geometry for deformation
        mod_subdiv = brick_obj.modifiers.new(name="Subdiv", type='SUBSURF')
        mod_subdiv.levels = 2
        mod_subdiv.render_levels = 2

        # C) Array: Create the line of stones
        mod_array = brick_obj.modifiers.new(name="Array", type='ARRAY')
        mod_array.count = stone_count
        mod_array.use_relative_offset = False
        mod_array.use_constant_offset = True
        mod_array.constant_offset_displace = (brick_length, 0, 0)

        # D) Displace: Add global noise. Each stone hits different noise coordinates!
        mod_displace = brick_obj.modifiers.new(name="Displace", type='DISPLACE')
        mod_displace.texture = tex
        mod_displace.texture_coords = 'GLOBAL'
        mod_displace.strength = 0.12 * scale

        # E) Simple Deform: Wrap the array 360 degrees around the Empty
        mod_bend = brick_obj.modifiers.new(name="Bend", type='SIMPLE_DEFORM')
        mod_bend.deform_method = 'BEND'
        mod_bend.angle = 2 * math.pi
        mod_bend.origin = empty

        # F) Decimate: Destroy the smooth noise to create crisp, low-poly planar facets
        mod_decimate = brick_obj.modifiers.new(name="Decimate", type='DECIMATE')
        mod_decimate.decimate_type = 'COLLAPSE'
        mod_decimate.ratio = 0.35

        # Parent layer to empty for easy scene organization
        brick_obj.parent = empty
        created_layers.append(brick_obj.name)

    return f"Created procedural well base '{object_name}' with {layers} layers and {stone_count * layers} total stones at {location}."
