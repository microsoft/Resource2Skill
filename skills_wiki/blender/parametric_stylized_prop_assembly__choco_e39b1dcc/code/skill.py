def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedCookieProp",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.76, 0.52, 0.25),  # Cookie dough color
    **kwargs,
) -> str:
    """
    Create a Parametric Stylized Chocolate Chip Cookie on a Tray.

    Args:
        scene_name: Name of the target scene.
        object_name: Root name for the created objects.
        location: (x, y, z) world-space base position of the tray.
        scale: Uniform scale factor for the entire prop assembly.
        material_color: (R, G, B) base color for the cookie dough.
        **kwargs: 
            - chip_count (int): Number of chocolate chips to generate (default: 12)
            - chip_color (tuple): RGB color for the chocolate chips
            - tray_color (tuple): RGB color for the tray

    Returns:
        Status string detailing the generated object hierarchy.
    """
    import bpy
    import random
    import math
    from mathutils import Vector

    # --- Parameters ---
    chip_count = kwargs.get("chip_count", 12)
    chip_color = kwargs.get("chip_color", (0.15, 0.07, 0.02))
    tray_color = kwargs.get("tray_color", (0.1, 0.3, 0.8))
    
    # Ensure colors have an alpha channel for Principled BSDF
    if len(material_color) == 3: material_color = (*material_color, 1.0)
    if len(chip_color) == 3: chip_color = (*chip_color, 1.0)
    if len(tray_color) == 3: tray_color = (*tray_color, 1.0)

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    base_loc = Vector(location)

    # --- Material Generator Helper ---
    def create_simple_material(mat_name, color, roughness=0.85):
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = color
            bsdf.inputs["Roughness"].default_value = roughness
        return mat

    mat_cookie = create_simple_material(f"{object_name}_Mat_Dough", material_color)
    mat_chip = create_simple_material(f"{object_name}_Mat_Chip", chip_color, roughness=0.4)
    mat_tray = create_simple_material(f"{object_name}_Mat_Tray", tray_color, roughness=0.6)

    # --- 1. Create the Tray (Cube) ---
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    tray = bpy.context.active_object
    tray.name = f"{object_name}_Tray"
    
    # Scale: wider X/Y, very thin Z
    tray.scale = (3.0 * scale, 3.0 * scale, 0.1 * scale)
    # Move so the bottom of the tray sits exactly at the provided location Z
    tray.location = base_loc + Vector((0, 0, 0.05 * scale))
    
    if len(tray.data.materials) == 0:
        tray.data.materials.append(mat_tray)

    # --- 2. Create the Cookie Base (Cylinder) ---
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1.0, depth=1.0)
    cookie = bpy.context.active_object
    cookie.name = f"{object_name}_Dough"
    
    # Scale: standard radius, squashed Z
    cookie.scale = (1.0 * scale, 1.0 * scale, 0.25 * scale)
    # Position cookie on top of the tray
    cookie_z_offset = (0.1 * scale) + (0.125 * scale) # Tray thickness + Half cookie thickness
    cookie.location = base_loc + Vector((0, 0, cookie_z_offset))
    cookie.parent = tray
    
    # Apply smooth shading to cookie
    for poly in cookie.data.polygons:
        poly.use_smooth = True
        
    if len(cookie.data.materials) == 0:
        cookie.data.materials.append(mat_cookie)

    # --- 3. Generate Chocolate Chips (Scattered UV Spheres) ---
    # The top surface of the cookie is at cookie.location.z + (0.125 * scale)
    cookie_top_z = cookie.location.z + (0.125 * scale)
    scatter_radius = 0.8 * scale # Keep slightly away from the absolute edge
    
    chips_created = 0
    for i in range(chip_count):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=1.0)
        chip = bpy.context.active_object
        chip.name = f"{object_name}_Chip_{i:02d}"
        
        # Base scale for chip with slight randomization
        c_scale = scale * random.uniform(0.12, 0.18)
        # Squash slightly on Z
        chip.scale = (c_scale, c_scale, c_scale * 0.7)
        
        # Smooth shading
        for poly in chip.data.polygons:
            poly.use_smooth = True
            
        if len(chip.data.materials) == 0:
            chip.data.materials.append(mat_chip)
            
        # Random radial positioning
        r = scatter_radius * math.sqrt(random.random()) # sqrt ensures even distribution
        theta = random.uniform(0, 2 * math.pi)
        
        # Position chip, embedding it slightly into the cookie
        chip_z_embed = c_scale * 0.4
        chip.location = (
            cookie.location.x + r * math.cos(theta),
            cookie.location.y + r * math.sin(theta),
            cookie_top_z - chip_z_embed
        )
        
        # Randomize rotation
        chip.rotation_euler = (
            random.uniform(0, math.pi),
            random.uniform(0, math.pi),
            random.uniform(0, math.pi)
        )
        
        chip.parent = cookie
        chips_created += 1

    # Deselect all, then select the root tray object
    bpy.ops.object.select_all(action='DESELECT')
    tray.select_set(True)
    bpy.context.view_layer.objects.active = tray

    return f"Created '{object_name}' (1 Tray, 1 Cookie Base, {chips_created} Chips) at {location} with scale {scale}."
