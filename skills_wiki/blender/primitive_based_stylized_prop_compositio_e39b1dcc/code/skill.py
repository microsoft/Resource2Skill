def create_cookie_tray(
    scene_name: str = "Scene",
    object_name: str = "StylizedCookieProp",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    cookie_color: tuple = (0.70, 0.45, 0.20),
    chip_color: tuple = (0.05, 0.02, 0.01),
    tray_color: tuple = (0.05, 0.15, 0.60),
    num_chips: int = 12,
    **kwargs
) -> str:
    """
    Create a Stylized Chocolate Chip Cookie on a Baking Tray.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position for the tray.
        scale: Uniform scale factor for the entire composition.
        cookie_color: (R, G, B) base color for the cookie dough.
        chip_color: (R, G, B) base color for the chocolate chips.
        tray_color: (R, G, B) base color for the tray.
        num_chips: Number of chocolate chips to scatter.
        **kwargs: Additional optional overrides.

    Returns:
        Status string.
    """
    import bpy
    import random
    import math
    from mathutils import Vector, Euler

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Helper function to create simple colored materials
    def create_solid_material(mat_name, rgb_color, roughness=0.7):
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Ensure alpha is 1.0
            bsdf.inputs['Base Color'].default_value = (*rgb_color, 1.0)
            bsdf.inputs['Roughness'].default_value = roughness
        return mat

    # --- Step 1: Create Materials ---
    tray_mat = create_solid_material(f"{object_name}_TrayMat", tray_color, roughness=0.6)
    cookie_mat = create_solid_material(f"{object_name}_CookieMat", cookie_color, roughness=0.8)
    chip_mat = create_solid_material(f"{object_name}_ChipMat", chip_color, roughness=0.3)

    base_loc = Vector(location)

    # --- Step 2: Create the Tray ---
    bpy.ops.mesh.primitive_cube_add(size=2.0)
    tray_obj = bpy.context.active_object
    tray_obj.name = f"{object_name}_Tray"
    # Scale: wide and flat
    tray_obj.scale = (1.5 * scale, 1.5 * scale, 0.05 * scale)
    tray_obj.location = base_loc
    tray_obj.data.materials.append(tray_mat)

    # --- Step 3: Create the Cookie Base ---
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1.0, depth=2.0)
    cookie_obj = bpy.context.active_object
    cookie_obj.name = f"{object_name}_Cookie"
    cookie_radius = 0.8 * scale
    cookie_height = 0.1 * scale
    cookie_obj.scale = (cookie_radius, cookie_radius, cookie_height)
    
    # Rest on top of the tray
    tray_top_z = base_loc.z + (0.05 * scale)
    cookie_obj.location = base_loc + Vector((0, 0, tray_top_z + cookie_height))
    
    # Shade Smooth for the cookie
    for poly in cookie_obj.data.polygons:
        poly.use_smooth = True
        
    cookie_obj.data.materials.append(cookie_mat)
    cookie_obj.parent = tray_obj

    # --- Step 4: Scatter Chocolate Chips ---
    chip_radius = 0.08 * scale
    for i in range(num_chips):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=chip_radius)
        chip_obj = bpy.context.active_object
        chip_obj.name = f"{object_name}_Chip_{i+1:02d}"
        
        # Shade Smooth for the chips
        for poly in chip_obj.data.polygons:
            poly.use_smooth = True
            
        chip_obj.data.materials.append(chip_mat)
        
        # Procedurally place chips in a circular radius on the cookie
        # Keep them slightly away from the absolute edge
        scatter_radius = random.uniform(0, cookie_radius * 0.75)
        theta = random.uniform(0, 2 * math.pi)
        
        x_offset = scatter_radius * math.cos(theta)
        y_offset = scatter_radius * math.sin(theta)
        
        # Position chips so they sit embedded in the top of the cookie surface
        chip_z = cookie_obj.location.z + cookie_height - (chip_radius * 0.4)
        
        chip_obj.location = cookie_obj.location.copy()
        chip_obj.location.x += x_offset
        chip_obj.location.y += y_offset
        chip_obj.location.z = chip_z
        
        # Add slight random rotation for organic feel
        chip_obj.rotation_euler = Euler((random.uniform(0, 3.14), random.uniform(0, 3.14), random.uniform(0, 3.14)))
        
        # Parent to cookie
        chip_obj.parent = cookie_obj

    # --- Step 5: Add Area Light (Optional/Bonus based on Tutorial) ---
    bpy.ops.object.light_add(type='AREA')
    light_obj = bpy.context.active_object
    light_obj.name = f"{object_name}_AreaLight"
    light_obj.location = base_loc + Vector((1.5 * scale, -1.5 * scale, 2.5 * scale))
    
    # Point light roughly at the center of the cookie
    direction = cookie_obj.location - light_obj.location
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    
    light_obj.data.energy = 800.0 * (scale ** 2)
    light_obj.data.shape = 'SQUARE'
    light_obj.data.size = 1.5 * scale
    light_obj.data.color = (1.0, 0.95, 0.85) # Warm lighting
    light_obj.parent = tray_obj

    # Deselect all when done
    bpy.ops.object.select_all(action='DESELECT')
    tray_obj.select_set(True)
    bpy.context.view_layer.objects.active = tray_obj

    return f"Created stylized prop '{object_name}' (Tray, Cookie, and {num_chips} Chips) at {location}."
