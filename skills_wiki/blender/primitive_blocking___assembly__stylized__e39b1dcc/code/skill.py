def create_object(
    scene_name: str = "Scene",
    object_name: str = "CookiePlatter",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.75, 0.55, 0.35),  # Default cookie tan
    **kwargs,
) -> str:
    """
    Create a Stylized Cookie Platter (Tray, Cookie, Chocolate Chips, and Light) in the active scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created assembly.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the cookie dough in 0-1 range.
        **kwargs: Additional overrides (e.g., num_chips).

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector

    # Configuration
    num_chips = kwargs.get("num_chips", 15)
    tray_color = (0.1, 0.25, 0.8, 1.0)
    chip_color = (0.12, 0.05, 0.02, 1.0)
    cookie_color = (*material_color, 1.0)

    # Make sure we are in object mode
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    collection = bpy.context.scene.collection

    # === Helper Function: Create Material ===
    def make_material(name, color):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = color
            # Increase roughness slightly for baked goods / clay look
            bsdf.inputs['Roughness'].default_value = 0.6
        return mat

    mat_cookie = make_material(f"{object_name}_Cookie_Mat", cookie_color)
    mat_chip = make_material(f"{object_name}_Chip_Mat", chip_color)
    mat_tray = make_material(f"{object_name}_Tray_Mat", tray_color)

    # === Helper Function: Smooth Shading ===
    def apply_smooth_shading(obj):
        for poly in obj.data.polygons:
            poly.use_smooth = True

    # === Step 1: Create Root Parent Empty ===
    parent_empty = bpy.data.objects.new(f"{object_name}_Root", None)
    parent_empty.empty_display_size = 2.0
    parent_empty.empty_display_type = 'ARROWS'
    collection.objects.link(parent_empty)

    # === Step 2: Create Tray (Base Cube, scaled) ===
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.15))
    tray_obj = bpy.context.active_object
    tray_obj.name = f"{object_name}_Tray"
    tray_obj.scale = (3.5, 3.5, 0.1)
    tray_obj.data.materials.append(mat_tray)
    tray_obj.parent = parent_empty

    # === Step 3: Create Cookie Base (Cylinder, squashed) ===
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1.2, depth=0.2, location=(0, 0, 0))
    cookie_obj = bpy.context.active_object
    cookie_obj.name = f"{object_name}_Dough"
    apply_smooth_shading(cookie_obj)
    cookie_obj.data.materials.append(mat_cookie)
    cookie_obj.parent = parent_empty

    # === Step 4: Scatter Chocolate Chips (Spheres) ===
    # Distribute chips randomly within the radius of the cookie
    chip_radius = 0.08
    scatter_radius = 1.0  # Slightly less than cookie radius to avoid floating off edge
    
    for i in range(num_chips):
        # Random position in a circle
        angle = random.uniform(0, 2 * math.pi)
        r = math.sqrt(random.uniform(0, 1)) * scatter_radius
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        
        # Add sphere
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=16, ring_count=8, 
            radius=chip_radius, 
            location=(x, y, 0.08)  # Sit slightly embedded into the top of the cookie
        )
        chip_obj = bpy.context.active_object
        chip_obj.name = f"{object_name}_Chip_{i:03d}"
        chip_obj.scale.z = 0.7  # Squash chip slightly
        
        # Random slight rotation for variety
        chip_obj.rotation_euler = (
            random.uniform(-0.2, 0.2), 
            random.uniform(-0.2, 0.2), 
            random.uniform(0, 2 * math.pi)
        )
        
        apply_smooth_shading(chip_obj)
        chip_obj.data.materials.append(mat_chip)
        chip_obj.parent = parent_empty

    # === Step 5: Add Lighting Context ===
    light_data = bpy.data.lights.new(name=f"{object_name}_WarmLight", type='AREA')
    light_data.energy = 850.0  # High wattage
    light_data.color = (1.0, 0.85, 0.7)  # Warm ~4000K look
    light_data.shape = 'SQUARE'
    light_data.size = 2.0
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_WarmLight_Obj", object_data=light_data)
    collection.objects.link(light_obj)
    light_obj.parent = parent_empty
    # Position above and slightly offset, angled down
    light_obj.location = (-1.5, -1.5, 3.0)
    light_obj.rotation_euler = (math.radians(45), 0, math.radians(-45))

    # === Step 6: Position & Scale the Entire Assembly ===
    parent_empty.location = Vector(location)
    parent_empty.scale = (scale, scale, scale)

    return f"Created '{object_name}' platter at {location} with 1 cookie, 1 tray, {num_chips} chips, and 1 warm area light."
