def create_object(
    scene_name: str = "Scene",
    object_name: str = "CookieDiorama",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.75, 0.50, 0.25),  # Cookie Base Color
    **kwargs,
) -> str:
    """
    Create a Stylized Chocolate Chip Cookie on a tray with custom lighting.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated collection/objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the cookie.
        **kwargs: 
            - chip_color: (R, G, B) color for the chocolate chips
            - tray_color: (R, G, B) color for the tray
            - num_chips: integer, number of chips to scatter
            - add_lighting: boolean, whether to add the tutorial's area light

    Returns:
        Status string describing the creation.
    """
    import bpy
    import math
    import random
    from mathutils import Vector

    # Extract kwargs
    chip_color = kwargs.get("chip_color", (0.05, 0.02, 0.01))
    tray_color = kwargs.get("tray_color", (0.05, 0.20, 0.60))
    num_chips = kwargs.get("num_chips", 12)
    add_lighting = kwargs.get("add_lighting", True)

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    base_loc = Vector(location)

    # Helper: Create unlinked material
    def create_material(mat_name, color, roughness=0.8):
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Blender 4.0+ uses "Base Color", older versions use same. Ensure alpha is 1.0.
            bsdf.inputs["Base Color"].default_value = (*color, 1.0)
            bsdf.inputs["Roughness"].default_value = roughness
        return mat

    # Create Materials
    mat_cookie = create_material(f"{object_name}_Mat_Cookie", material_color, 0.85)
    mat_chip = create_material(f"{object_name}_Mat_Chip", chip_color, 0.4) # Slightly shinier chips
    mat_tray = create_material(f"{object_name}_Mat_Tray", tray_color, 0.6)

    # Create a new collection to keep the additive scene organized
    collection = bpy.data.collections.new(f"{object_name}_Collection")
    scene.collection.children.link(collection)

    # Helper: Ensure object is linked only to our specific collection
    def link_to_collection(obj):
        for coll in obj.users_collection:
            coll.objects.unlink(obj)
        collection.objects.link(obj)

    # --- 1. Build the Tray ---
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=base_loc)
    tray = bpy.context.active_object
    tray.name = f"{object_name}_Tray"
    # Scale tray: Wide X/Y, thin Z
    tray.scale = (2.5 * scale, 2.5 * scale, 0.1 * scale)
    tray.data.materials.append(mat_tray)
    link_to_collection(tray)

    # --- 2. Build the Cookie Base ---
    # Position slightly above the tray
    cookie_z = base_loc.z + (0.05 * scale) + (0.15 * scale)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32, 
        radius=1.0, 
        depth=1.0, 
        location=(base_loc.x, base_loc.y, cookie_z)
    )
    cookie = bpy.context.active_object
    cookie.name = f"{object_name}_Base"
    # Scale cookie: smaller than tray, squashed Z
    cookie_radius = 1.0 * scale
    cookie.scale = (cookie_radius, cookie_radius, 0.3 * scale)
    bpy.ops.object.shade_smooth()
    cookie.data.materials.append(mat_cookie)
    cookie.parent = tray
    link_to_collection(cookie)

    # --- 3. Build the Chocolate Chips ---
    # Top surface Z height of the cookie
    chip_base_z = cookie_z + (0.15 * scale) 
    
    for i in range(num_chips):
        # Random distribution within a circle (slightly inset from edge)
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, cookie_radius * 0.8)
        
        c_x = base_loc.x + (radius * math.cos(angle))
        c_y = base_loc.y + (radius * math.sin(angle))
        # Bury chips slightly into the cookie, add slight random height variation
        c_z = chip_base_z - random.uniform(0.01 * scale, 0.05 * scale)
        
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=32, 
            ring_count=16, 
            radius=0.1 * scale, 
            location=(c_x, c_y, c_z)
        )
        chip = bpy.context.active_object
        chip.name = f"{object_name}_Chip_{i+1:02d}"
        
        # Add slight random non-uniform scale to chips so they aren't perfect spheres
        s_x = random.uniform(0.8, 1.2)
        s_y = random.uniform(0.8, 1.2)
        s_z = random.uniform(0.6, 0.9) # Flattened on top
        chip.scale = (s_x, s_y, s_z)
        
        # Random Z rotation for variation
        chip.rotation_euler[2] = random.uniform(0, 2 * math.pi)
        
        bpy.ops.object.shade_smooth()
        chip.data.materials.append(mat_chip)
        chip.parent = cookie
        link_to_collection(chip)

    # --- 4. Add Tutorial Lighting ---
    if add_lighting:
        # Create Area Light
        light_data = bpy.data.lights.new(name=f"{object_name}_AreaLight", type='AREA')
        light_data.energy = 850.0  # 850W from tutorial
        light_data.color = (1.0, 0.85, 0.7)  # Warm light approx 4000K
        light_data.shape = 'SQUARE'
        light_data.size = 2.0 * scale
        
        light_obj = bpy.data.objects.new(name=f"{object_name}_AreaLight", object_data=light_data)
        collection.objects.link(light_obj)
        
        # Position offset from base, looking down at the cookie
        light_obj.location = base_loc + Vector((-1.5 * scale, -1.5 * scale, 3.0 * scale))
        
        # Point the light at the center of the cookie using a Tracking constraint
        track_mod = light_obj.constraints.new(type='TRACK_TO')
        track_mod.target = cookie
        track_mod.track_axis = 'TRACK_NEGATIVE_Z'
        track_mod.up_axis = 'UP_Y'
        light_obj.parent = tray

    # Deselect all to finish cleanly
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created '{object_name}' (Tray, Cookie, {num_chips} Chips) at {location} in collection '{collection.name}'"
