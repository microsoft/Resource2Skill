def create_cookie_scene(
    scene_name: str = "Scene",
    object_name: str = "StylizedCookieSet",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    tray_color: tuple = (0.1, 0.3, 0.8),
    cookie_color: tuple = (0.4, 0.15, 0.05),
    chip_color: tuple = (0.02, 0.01, 0.0),
    **kwargs,
) -> str:
    """
    Create a Stylized Chocolate Chip Cookie sitting on a tray, lit by a warm Area light.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created object hierarchy.
        location: (x, y, z) world-space position for the entire set.
        scale: Uniform scale factor for the set.
        tray_color: (R, G, B) color of the tray.
        cookie_color: (R, G, B) color of the cookie dough.
        chip_color: (R, G, B) color of the chocolate chips.

    Returns:
        Status string indicating success.
    """
    import bpy
    import math
    import random
    from mathutils import Vector, Euler

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Helper function to create simple colored materials
    def create_simple_material(name, color):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Ensure color is RGBA
            rgba = (color[0], color[1], color[2], 1.0)
            bsdf.inputs['Base Color'].default_value = rgba
            # Give it a slightly matte look
            bsdf.inputs['Roughness'].default_value = 0.6 
        return mat

    # Create materials
    mat_tray = create_simple_material(f"{object_name}_TrayMat", tray_color)
    mat_cookie = create_simple_material(f"{object_name}_CookieMat", cookie_color)
    mat_chip = create_simple_material(f"{object_name}_ChipMat", chip_color)

    # === Step 1: Create Parent Empty ===
    # Keeps the hierarchy clean and allows easy movement/scaling of the whole group
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    master_empty = bpy.context.active_object
    master_empty.name = object_name

    # === Step 2: Create Tray ===
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.025))
    tray = bpy.context.active_object
    tray.name = f"{object_name}_Tray"
    tray.scale = (3.0, 3.0, 0.05) # Scaled non-uniformly to form a platter
    tray.data.materials.append(mat_tray)
    tray.parent = master_empty

    # === Step 3: Create Cookie Base ===
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1, depth=1, location=(0, 0, 0.1))
    cookie = bpy.context.active_object
    cookie.name = f"{object_name}_Base"
    cookie.scale = (0.8, 0.8, 0.1) # Scaled flat
    bpy.ops.object.shade_smooth()
    cookie.data.materials.append(mat_cookie)
    cookie.parent = master_empty

    # === Step 4: Scatter Chocolate Chips ===
    chip_count = 14
    for i in range(chip_count):
        # Create base sphere
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=1, location=(0,0,0))
        chip = bpy.context.active_object
        chip.name = f"{object_name}_Chip_{i:02d}"
        bpy.ops.object.shade_smooth()
        chip.data.materials.append(mat_chip)
        
        # Calculate random placement within a radius
        # Radius goes up to 0.65 (cookie edge is ~0.8)
        r = random.uniform(0.0, 0.65)
        # Sqrt ensures uniform distribution in a circle instead of clustering at center
        r = math.sqrt(random.uniform(0.0, 1.0)) * 0.65
        theta = random.uniform(0, 2 * math.pi)
        
        cx = r * math.cos(theta)
        cy = r * math.sin(theta)
        cz = 0.15 + random.uniform(-0.01, 0.01) # Sits just atop the cookie

        chip.location = (cx, cy, cz)
        chip.scale = (0.08, 0.08, 0.05) # Squashed slightly
        
        # Add random rotation for variety
        chip.rotation_euler = Euler((random.uniform(0, 0.5), random.uniform(0, 0.5), random.uniform(0, 2*math.pi)), 'XYZ')
        chip.parent = master_empty

    # === Step 5: Add Warm Area Light ===
    bpy.ops.object.light_add(type='AREA', radius=2.0, location=(2.5, -2.5, 3.0))
    light = bpy.context.active_object
    light.name = f"{object_name}_WarmLight"
    light.data.energy = 850.0  # 850 Watts
    light.data.color = (1.0, 0.8, 0.6) # Approx 4000K warm tone
    
    # Point light precisely at the center of the cookie (0,0,0)
    direction = Vector((0, 0, 0)) - light.location
    light.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    light.parent = master_empty

    # === Step 6: Final Transformations ===
    master_empty.location = Vector(location)
    master_empty.scale = (scale, scale, scale)

    # Deselect all when done
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created '{object_name}' (Tray, Cookie, {chip_count} Chips, and Lighting) at {location} with scale {scale}."
