def create_cookie_scene(
    scene_name: str = "Scene",
    object_name: str = "CookieProp",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    cookie_color: tuple = (0.53, 0.25, 0.1, 1.0),
    chip_color: tuple = (0.02, 0.01, 0.0, 1.0),
    tray_color: tuple = (0.02, 0.08, 0.35, 1.0),
    num_chips: int = 12,
    **kwargs,
) -> str:
    """
    Create a primitive-based Chocolate Chip Cookie scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position for the center of the tray.
        scale: Uniform scale factor for the entire scene.
        cookie_color: (R, G, B, A) base color for the cookie.
        chip_color: (R, G, B, A) base color for the chocolate chips.
        tray_color: (R, G, B, A) base color for the tray.
        num_chips: Number of chocolate chips to randomly distribute.

    Returns:
        Status string.
    """
    import bpy
    import random
    import math
    from mathutils import Vector, Euler

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Helper function to create solid color materials
    def create_simple_material(name, color):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = color
            bsdf.inputs["Roughness"].default_value = 0.65
        return mat

    mat_cookie = create_simple_material(f"{object_name}_CookieMat", cookie_color)
    mat_chip = create_simple_material(f"{object_name}_ChipMat", chip_color)
    mat_tray = create_simple_material(f"{object_name}_TrayMat", tray_color)

    # 1. Create a root empty to keep the hierarchy organized
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    root_empty = bpy.context.active_object
    root_empty.name = object_name
    root_empty.scale = (scale, scale, scale)

    # 2. Create the Tray (Flattened Cube)
    bpy.ops.mesh.primitive_cube_add(size=2.0)
    tray = bpy.context.active_object
    tray.name = f"{object_name}_Tray"
    tray.scale = (2.0, 2.0, 0.1)
    tray.location = Vector((0, 0, -0.1))
    tray.parent = root_empty
    tray.data.materials.append(mat_tray)

    # 3. Create the Cookie Base (Flattened Cylinder)
    bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=2.0, vertices=32)
    cookie = bpy.context.active_object
    cookie.name = f"{object_name}_Base"
    cookie.scale = (1.3, 1.3, 0.15)
    cookie.location = Vector((0, 0, 0.15))
    bpy.ops.object.shade_smooth()
    cookie.parent = root_empty
    cookie.data.materials.append(mat_cookie)

    # 4. Create and Distribute Chocolate Chips (Scaled UV Spheres)
    for i in range(num_chips):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=16, ring_count=8)
        chip = bpy.context.active_object
        chip.name = f"{object_name}_Chip_{i}"
        
        # Randomize size
        chip_scale = random.uniform(0.12, 0.18)
        chip.scale = (chip_scale, chip_scale, chip_scale * 0.7) # Flatten slightly
        
        # Distribute within the radius of the cookie using polar coordinates
        angle = random.uniform(0, math.pi * 2)
        radius_offset = random.uniform(0, 1.1) 
        
        x = math.cos(angle) * radius_offset
        y = math.sin(angle) * radius_offset
        z = 0.28 # Embed slightly into the top of the cookie surface
        
        chip.location = Vector((x, y, z))
        
        # Add random rotation so they don't look perfectly uniform
        chip.rotation_euler = Euler((
            random.uniform(-0.5, 0.5), 
            random.uniform(-0.5, 0.5), 
            random.uniform(0, math.pi * 2)
        ))
        
        bpy.ops.object.shade_smooth()
        chip.parent = root_empty
        chip.data.materials.append(mat_chip)

    # 5. Setup Lighting (Warm Area Light)
    bpy.ops.object.light_add(type='AREA')
    light = bpy.context.active_object
    light.name = f"{object_name}_AreaLight"
    light.location = Vector((-2.5, -2.5, 3.5))
    
    # Track light to the center of the cookie
    direction = Vector((0,0,0)) - light.location
    light.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    
    # Configure light properties
    light.data.energy = 800.0
    light.data.size = 2.0
    light.data.color = (1.0, 0.85, 0.7) # Warm yellowish light to simulate 4000K
    light.parent = root_empty

    # Cleanup selection
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created scene '{object_name}' (Tray, Cookie Base, {num_chips} Chips, Area Light) under Empty at {location}"
