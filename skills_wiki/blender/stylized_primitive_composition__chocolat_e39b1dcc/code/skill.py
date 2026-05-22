def create_stylized_cookie_scene(
    scene_name: str = "Scene",
    object_name: str = "StylizedCookieScene",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    cookie_color: tuple = (0.60, 0.35, 0.10),
    chip_color: tuple = (0.05, 0.02, 0.01),
    tray_color: tuple = (0.05, 0.15, 0.60),
    **kwargs,
) -> str:
    """
    Create a stylized chocolate chip cookie resting on a tray in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created objects and parent empty.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        cookie_color: (R, G, B) base color for the cookie dough.
        chip_color: (R, G, B) base color for the chocolate chips.
        tray_color: (R, G, B) base color for the resting tray.
        **kwargs: Additional overrides (e.g., num_chips).

    Returns:
        Status string describing the created compound object.
    """
    import bpy
    import random
    import math
    from mathutils import Vector

    # Ensure context is clean and in object mode
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    collection = bpy.context.collection

    # === Step 1: Create Parent Empty ===
    parent_empty = bpy.data.objects.new(object_name, None)
    parent_empty.empty_display_type = 'ARROWS'
    collection.objects.link(parent_empty)
    parent_empty.location = Vector(location)
    parent_empty.scale = (scale, scale, scale)

    # Helper function to generate and assign simple colored materials
    def create_solid_material(mat_name, rgb_color):
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Set Base Color (RGBA)
            bsdf.inputs['Base Color'].default_value = (*rgb_color, 1.0)
            # Give it a matte baked look
            bsdf.inputs['Roughness'].default_value = 0.6
        return mat

    mat_cookie = create_solid_material(f"{object_name}_CookieMat", cookie_color)
    mat_chip = create_solid_material(f"{object_name}_ChipMat", chip_color)
    mat_tray = create_solid_material(f"{object_name}_TrayMat", tray_color)

    # === Step 2: Build the Tray ===
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    tray = bpy.context.active_object
    tray.name = f"{object_name}_Tray"
    tray.scale = (3.0, 3.0, 0.1)
    # Move so the top face of the tray rests exactly at Z = 0
    tray.location = (0, 0, -0.05)
    tray.data.materials.append(mat_tray)
    tray.parent = parent_empty

    # === Step 3: Build the Base Cookie ===
    bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=0.2, vertices=32)
    cookie = bpy.context.active_object
    cookie.name = f"{object_name}_CookieBase"
    # Move so the bottom face rests on the tray (Z=0), putting the top face at Z=0.2
    cookie.location = (0, 0, 0.1)
    bpy.ops.object.shade_smooth()
    cookie.data.materials.append(mat_cookie)
    cookie.parent = parent_empty

    # === Step 4: Scatter Chocolate Chips ===
    num_chips = kwargs.get("num_chips", 15)
    
    for i in range(num_chips):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=16, ring_count=8)
        chip = bpy.context.active_object
        chip.name = f"{object_name}_Chip_{i:03d}"
        
        # Randomly scale the chip and slightly flatten it
        s = random.uniform(0.08, 0.15)
        chip.scale = (s, s, s * 0.8)
        
        # Uniform circular distribution logic
        angle = random.uniform(0, 2 * math.pi)
        # sqrt() ensures uniform area distribution so they don't bunch in the center
        # Multiply by 0.85 to keep chips comfortably inside the cookie's outer radius (1.0)
        dist = math.sqrt(random.uniform(0, 1)) * 0.85 
        
        x = math.cos(angle) * dist
        y = math.sin(angle) * dist
        # Place directly on top of the cookie surface (Z=0.2) + offset for chip scale
        z = 0.2 + (s * 0.4) 
        
        chip.location = (x, y, z)
        
        # Add random rotation so they look organic
        chip.rotation_euler = (
            random.uniform(-0.5, 0.5), 
            random.uniform(-0.5, 0.5), 
            random.uniform(0, 2 * math.pi)
        )
        
        bpy.ops.object.shade_smooth()
        chip.data.materials.append(mat_chip)
        chip.parent = parent_empty

    # Deselect all when finished
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created '{object_name}' (stylized cookie tray with {num_chips} chips) successfully at {location}."
