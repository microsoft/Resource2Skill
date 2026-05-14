def create_stylized_well_base(
    scene_name: str = "Scene",
    object_name: str = "LowPolyWellBase",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.45, 0.40, 0.50),
    radius: float = 1.5,
    layers: int = 4,
    stones_per_layer: int = 12,
    **kwargs
) -> str:
    """
    Create a procedural, stylized low-poly stone ring (e.g., for a well base).

    Args:
        scene_name: Name of the active scene.
        object_name: Base name for the generated objects.
        location: (x, y, z) world-space origin of the well base.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the stones.
        radius: Inner radius of the well.
        layers: Number of stacked stone rings.
        stones_per_layer: Number of individual stone blocks per ring.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Parent Hierarchy ===
    parent_obj = bpy.data.objects.new(object_name, None)
    parent_obj.location = location
    parent_obj.scale = (scale, scale, scale)
    bpy.context.collection.objects.link(parent_obj)

    # === Step 2: Generate Material Palette ===
    # Create slightly varying colors to simulate natural stone distribution
    mats = []
    for i in range(4):
        mat = bpy.data.materials.new(name=f"{object_name}_Mat_{i}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Shift the base color slightly for variation
            c = (
                max(0.0, min(1.0, material_color[0] + random.uniform(-0.04, 0.04))),
                max(0.0, min(1.0, material_color[1] + random.uniform(-0.04, 0.04))),
                max(0.0, min(1.0, material_color[2] + random.uniform(-0.06, 0.06))),
                1.0
            )
            bsdf.inputs['Base Color'].default_value = c
            bsdf.inputs['Roughness'].default_value = 0.95
        mats.append(mat)

    stone_height = 0.35
    stone_depth = 0.5

    # === Step 3: Procedural Layer Construction ===
    for layer in range(layers):
        mesh = bpy.data.meshes.new(f"{object_name}_Layer_{layer}")
        obj = bpy.data.objects.new(f"{object_name}_Layer_{layer}", mesh)
        obj.parent = parent_obj
        bpy.context.collection.objects.link(obj)

        for m in mats:
            obj.data.materials.append(m)

        # Stagger the masonry (rotate alternate layers by half a stone)
        if layer % 2 == 1:
            obj.rotation_euler[2] = (2 * math.pi / stones_per_layer) * 0.5

        bm = bmesh.new()
        
        # Add slight organic variation to the radius per layer
        layer_radius = radius * random.uniform(0.97, 1.03)
        if layer == layers - 1:
            layer_radius *= 0.93  # Top layer tapers inward slightly

        circumference = 2 * math.pi * layer_radius
        current_x = -circumference / 2.0

        # Build a flat line of stones
        for i in range(stones_per_layer):
            stone_len = circumference / stones_per_layer
            
            # Individual stone dimensions (incorporating gaps via scaling)
            sl = stone_len * random.uniform(0.85, 0.95)
            sh = stone_height * random.uniform(0.85, 1.15)
            sd = stone_depth * random.uniform(0.85, 1.15)

            start_faces = len(bm.faces)
            ret = bmesh.ops.create_cube(bm, size=1.0)
            verts = ret['verts']
            
            bmesh.ops.scale(bm, vec=(sl, sd, sh), verts=verts)
            # Center the cube vertically based on the layer index
            bmesh.ops.translate(bm, vec=(current_x + stone_len / 2.0, 0, layer * stone_height), verts=verts)

            # Assign a random material from our palette
            bm.faces.ensure_lookup_table()
            mat_idx = random.randint(0, len(mats) - 1)
            for f_idx in range(start_faces, len(bm.faces)):
                bm.faces[f_idx].material_index = mat_idx

            current_x += stone_len

        # Introduce dense geometry for organic distortion
        bmesh.ops.subdivide_edges(bm, edges=list(bm.edges), cuts=2, use_grid_fill=True)

        # Apply vertex "wobble" (replicates manual randomization)
        for v in bm.verts:
            v.co.x += random.uniform(-0.04, 0.04)
            v.co.y += random.uniform(-0.04, 0.04)
            v.co.z += random.uniform(-0.04, 0.04)

        # Radially map the X-coordinates to wrap seamlessly into a circle
        for v in bm.verts:
            factor = v.co.x / circumference
            angle = factor * 2 * math.pi
            r = layer_radius + v.co.y
            
            new_x = r * math.cos(angle)
            new_y = r * math.sin(angle)
            
            v.co.x = new_x
            v.co.y = new_y
            # v.co.z remains unchanged to maintain height

        bm.to_mesh(mesh)
        bm.free()

        # === Step 4: The Low-Poly Chisel Effect ===
        # The decimate modifier aggressively collapses the smooth/wobbly geometry into stark facets
        decimate = obj.modifiers.new(name="Decimate", type='DECIMATE')
        decimate.ratio = 0.35  # Lower ratio = more chunky/stylized

    return f"Created '{object_name}' at {location} with {layers} rings and {layers * stones_per_layer} stones."
