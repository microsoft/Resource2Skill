def create_lowpoly_well_base(
    scene_name: str = "Scene",
    object_name: str = "WellBase",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.55, 0.5, 0.5),
    radius: float = 1.2,
    rings: int = 4,
    stones_per_ring: int = 14,
    **kwargs
) -> str:
    """
    Create a stylized low-poly stone ring structure using modifier baking.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the master object.
        location: (x, y, z) world-space position.
        scale: Uniform scale multiplier for the generated geometry.
        material_color: (R, G, B) base color of the stone.
        radius: Base radius of the bottom ring.
        rings: Number of stacked stone rings.
        stones_per_ring: Number of individual stone blocks per ring.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Material & Texture Setup ===
    mat_name = f"{object_name}_Mat"
    if mat_name not in bpy.data.materials:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.85
            # Handle API change for Blender 4.0+
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.2
            elif 'Specular' in bsdf.inputs:
                bsdf.inputs['Specular'].default_value = 0.2
    else:
        mat = bpy.data.materials[mat_name]

    tex_name = f"{object_name}_DispTex"
    if tex_name not in bpy.data.textures:
        tex = bpy.data.textures.new(tex_name, type='CLOUDS')
        tex.noise_scale = 0.5
    else:
        tex = bpy.data.textures[tex_name]

    # === Step 2: Create Master Parent ===
    master = bpy.data.objects.new(object_name, None)
    scene.collection.objects.link(master)
    master.location = location

    ring_objects = []

    # === Step 3: Generate Rings Procedurally ===
    for i in range(rings):
        # Calculate proportional dimensions
        ring_radius = (radius * scale) * (1.0 - i * 0.04) # Slight taper upwards
        circumference = 2 * math.pi * ring_radius
        stone_len = circumference / stones_per_ring
        stone_h = 0.3 * scale
        stone_w = 0.4 * scale

        # Create base brick
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        obj = bpy.context.active_object
        obj.name = f"{object_name}_Ring_{i}"
        
        # Apply base dimensions (1.05 length multiplier creates overlap)
        obj.scale = ((stone_len / 2) * 1.05, stone_w / 2, stone_h / 2)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        # 1. Array (Linear Wall)
        arr = obj.modifiers.new("Array", 'ARRAY')
        arr.count = stones_per_ring
        arr.use_relative_offset = False
        arr.use_constant_offset = True
        arr.constant_offset_displace = (stone_len, 0, 0)
        
        # Apply Array immediately to re-center the line's bounding box
        bpy.ops.object.modifier_apply(modifier="Array")
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        obj.location = (0, 0, 0)
        bpy.ops.object.transform_apply(location=True)

        # 2. Add Stylization Modifiers
        bev = obj.modifiers.new("Bevel", 'BEVEL')
        bev.width = 0.04 * scale
        bev.segments = 1

        sub = obj.modifiers.new("Subsurf", 'SUBSURF')
        sub.subdivision_type = 'SIMPLE'
        sub.levels = 2

        disp = obj.modifiers.new("Displace", 'DISPLACE')
        disp.texture = tex
        disp.strength = 0.05 * scale

        # 3. Bend into Circle
        bend = obj.modifiers.new("Bend", 'SIMPLE_DEFORM')
        bend.deform_method = 'BEND'
        bend.angle = 2 * math.pi
        bend.deform_axis = 'Z'

        weld = obj.modifiers.new("Weld", 'WELD')
        weld.merge_threshold = 0.05 * scale

        # 4. Decimate for low-poly chunkiness
        dec = obj.modifiers.new("Decimate", 'DECIMATE')
        dec.ratio = 0.28 

        # Apply all remaining modifiers to bake the geometry
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        for mod in list(obj.modifiers):
            bpy.ops.object.modifier_apply(modifier=mod.name)

        # Center the newly formed circular geometry to the object origin
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        bpy.ops.object.shade_flat()

        # Add material
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

        # Offset stacking and rotation (interlocking brick pattern)
        obj.parent = master
        obj.location = (0, 0, i * stone_h * 0.9)
        obj.rotation_euler[2] = (i * math.pi / stones_per_ring)
        
        ring_objects.append(obj)

    # Clean up selection
    bpy.ops.object.select_all(action='DESELECT')
    master.select_set(True)
    bpy.context.view_layer.objects.active = master

    return f"Created '{object_name}' at {location} with {rings} concentric low-poly stone rings."
