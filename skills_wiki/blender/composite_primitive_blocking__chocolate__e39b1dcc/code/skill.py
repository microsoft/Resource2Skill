def create_object(
    scene_name: str = "Scene",
    object_name: str = "ChocolateChipCookie",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.76, 0.45, 0.2),
    **kwargs
) -> str:
    """
    Create a composite primitive Chocolate Chip Cookie on a tray.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects and collection.
        location: (x, y, z) world-space position of the tray's bottom center.
        scale: Uniform scale factor for the entire composition.
        material_color: (R, G, B) base color for the cookie dough.
        **kwargs: Overrides for 'chip_color', 'tray_color', and 'num_chips'.

    Returns:
        Status string.
    """
    import bpy
    import random
    from mathutils import Vector, Euler
    import math

    # Get target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # Optional parameter overrides
    chip_color = kwargs.get('chip_color', (0.05, 0.02, 0.01))
    tray_color = kwargs.get('tray_color', (0.1, 0.2, 0.8))
    num_chips = kwargs.get('num_chips', 14)

    # Collection management to group the composition
    col_name = f"{object_name}_Collection"
    if col_name not in bpy.data.collections:
        new_col = bpy.data.collections.new(col_name)
        scene.collection.children.link(new_col)
    else:
        new_col = bpy.data.collections[col_name]

    def move_to_collection(obj):
        # Move object from default collection to our specific group
        for col in obj.users_collection:
            col.objects.unlink(obj)
        new_col.objects.link(obj)

    # Helper function for base color materials
    def create_material(name, color):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (*color, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.8
        return mat

    cookie_mat = create_material(f"{object_name}_CookieMat", material_color)
    chip_mat = create_material(f"{object_name}_ChipMat", chip_color)
    tray_mat = create_material(f"{object_name}_TrayMat", tray_color)

    base_loc = Vector(location)

    # === Step 1: Create Tray (Flattened Cube) ===
    bpy.ops.mesh.primitive_cube_add(size=2.0)
    tray = bpy.context.active_object
    tray.name = f"{object_name}_Tray"
    tray.scale = (2.0 * scale, 2.0 * scale, 0.1 * scale)
    tray.location = base_loc + Vector((0, 0, 0.1 * scale))
    if tray.data.materials:
        tray.data.materials[0] = tray_mat
    else:
        tray.data.materials.append(tray_mat)
    move_to_collection(tray)

    # === Step 2: Create Cookie Base (Flattened Cylinder) ===
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1.0, depth=2.0)
    cookie = bpy.context.active_object
    cookie.name = f"{object_name}_Base"
    cookie.scale = (1.2 * scale, 1.2 * scale, 0.15 * scale)
    cookie.location = base_loc + Vector((0, 0, 0.35 * scale))
    
    # Smooth the faceting of the cylinder
    bpy.ops.object.shade_smooth()
    
    if cookie.data.materials:
        cookie.data.materials[0] = cookie_mat
    else:
        cookie.data.materials.append(cookie_mat)
    move_to_collection(cookie)

    # === Step 3: Create Chocolate Chips (Scattered Spheres) ===
    chip_radius = 0.12 * scale
    for i in range(num_chips):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=chip_radius)
        chip = bpy.context.active_object
        chip.name = f"{object_name}_Chip_{i}"
        
        # Calculate random circular distribution on top of cookie
        r = random.uniform(0, 0.9 * scale)
        theta = random.uniform(0, 2 * math.pi)
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        
        # Slightly embed into the top of the cookie surface
        chip.location = base_loc + Vector((x, y, 0.5 * scale))
        
        # Slightly randomize scale and flatten the top
        s = random.uniform(0.8, 1.2)
        chip.scale = (s, s, s * 0.6)
        
        # Add random pitch and yaw rotation for organic variation
        chip.rotation_euler = Euler((random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3), random.uniform(0, 2*math.pi)))
        
        bpy.ops.object.shade_smooth()
        
        if chip.data.materials:
            chip.data.materials[0] = chip_mat
        else:
            chip.data.materials.append(chip_mat)
        move_to_collection(chip)

    # === Step 4: Lighting Context (Area Light) ===
    bpy.ops.object.light_add(type='AREA', radius=2.0 * scale)
    light = bpy.context.active_object
    light.name = f"{object_name}_Light"
    light.location = base_loc + Vector((1.5 * scale, -1.5 * scale, 3.0 * scale))
    
    # Orient light to point directly at the cookie base
    direction = cookie.location - light.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    light.rotation_euler = rot_quat.to_euler()
    
    # Configure energy (watts) and warm color temperature
    light.data.energy = 800.0 * (scale ** 2)
    light.data.color = (1.0, 0.9, 0.8)
    move_to_collection(light)
    
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')
    
    return f"Created '{object_name}' (Composite Primitive) containing tray, cookie, {num_chips} chips, and lighting at {location}."
