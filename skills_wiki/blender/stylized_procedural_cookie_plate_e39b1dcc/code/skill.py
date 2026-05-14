def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedCookie",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.5, 0.2), # Dough color
    **kwargs,
) -> str:
    """
    Create a Stylized Cookie on a Tray in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color of the cookie dough.
        **kwargs: Additional overrides (num_chips: int).

    Returns:
        Status string describing the generated objects.
    """
    import bpy
    import random
    import math
    from mathutils import Vector

    # --- Setup ---
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    num_chips = kwargs.get('num_chips', 14)
    
    # Helper function to create materials
    def create_material(name, color, roughness=0.5):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Support both older Blender (<4.0) and newer Blender (>=4.0) BSDF nodes
            color_input = bsdf.inputs.get('Base Color')
            if color_input:
                color_input.default_value = (*color, 1.0)
            roughness_input = bsdf.inputs.get('Roughness')
            if roughness_input:
                roughness_input.default_value = roughness
        return mat

    # Create Materials
    tray_mat = create_material(f"{object_name}_TrayMat", (0.05, 0.2, 0.6), roughness=0.5)
    cookie_mat = create_material(f"{object_name}_CookieMat", material_color, roughness=0.75)
    chip_mat = create_material(f"{object_name}_ChipMat", (0.04, 0.015, 0.005), roughness=0.35)

    # --- 1. Create the Tray (Cube) ---
    bpy.ops.mesh.primitive_cube_add(size=2.0)
    tray = bpy.context.active_object
    tray.name = f"{object_name}_Tray"
    
    # Scale wide and thin, position base at Z=0 relative to location
    tray.scale = (2.0 * scale, 2.0 * scale, 0.1 * scale)
    tray.location = Vector(location) + Vector((0, 0, 0.1 * scale))
    tray.data.materials.append(tray_mat)

    # --- 2. Create the Cookie (Cylinder) ---
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1.0, depth=2.0)
    cookie = bpy.context.active_object
    cookie.name = f"{object_name}_Dough"
    
    # Flatten on Z, rest on top of the tray
    cookie_radius = 1.3 * scale
    cookie_thickness = 0.15 * scale
    cookie.scale = (cookie_radius, cookie_radius, cookie_thickness)
    cookie.location = Vector(location) + Vector((0, 0, (0.2 + cookie_thickness) * scale))
    
    # Apply smooth shading
    cookie.data.polygons.foreach_set('use_smooth', [True] * len(cookie.data.polygons))
    cookie.data.materials.append(cookie_mat)
    cookie.parent = tray # Group hierarchy

    # --- 3. Create Chocolate Chips (Spheres) ---
    for i in range(num_chips):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.1)
        chip = bpy.context.active_object
        chip.name = f"{object_name}_Chip_{i:02d}"
        
        # Slightly flatten the chip so it looks melted
        chip.scale = (scale, scale, 0.7 * scale)
        
        # Procedurally scatter using polar coordinates (keep within cookie radius)
        angle = random.uniform(0, math.pi * 2)
        dist = random.uniform(0.1 * scale, cookie_radius * 0.85) # Avoid edges
        
        cx = cookie.location.x + math.cos(angle) * dist
        cy = cookie.location.y + math.sin(angle) * dist
        
        # Z-position: Embed slightly into the cookie dough
        # Cookie top is at location.z + thickness
        cz = cookie.location.z + (cookie_thickness * 0.8)
        
        chip.location = (cx, cy, cz)
        
        # Randomize rotation for variation
        chip.rotation_euler = (
            random.uniform(-0.4, 0.4),
            random.uniform(-0.4, 0.4),
            random.uniform(0, math.pi * 2)
        )
        
        # Apply smooth shading
        chip.data.polygons.foreach_set('use_smooth', [True] * len(chip.data.polygons))
        chip.data.materials.append(chip_mat)
        chip.parent = cookie

    # --- 4. Add Warm Area Lighting ---
    bpy.ops.object.light_add(type='AREA', radius=2.5 * scale)
    light = bpy.context.active_object
    light.name = f"{object_name}_WarmLight"
    
    # Position diagonally above the cookie
    light.location = tray.location + Vector((1.5 * scale, -1.5 * scale, 3.0 * scale))
    
    # Point light exactly at the cookie
    direction = cookie.location - light.location
    light.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    
    # Configure light energy and warm color
    light.data.energy = 850.0 * (scale ** 2)  # Scale energy correctly
    light.data.color = (1.0, 0.85, 0.7) # Warm ~4000K look
    light.parent = tray

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created '{object_name}' (Cookie with {num_chips} chips on Tray) at {location}."
