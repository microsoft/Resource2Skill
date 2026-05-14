def create_cookie_on_tray(
    scene_name: str = "Scene",
    object_name: str = "CookieProp",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    cookie_color: tuple = (0.60, 0.35, 0.15, 1.0),
    chip_color: tuple = (0.08, 0.04, 0.01, 1.0),
    tray_color: tuple = (0.15, 0.30, 0.60, 1.0),
    **kwargs,
) -> str:
    """
    Create a composite Chocolate Chip Cookie on a Tray in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created hierarchy of objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        cookie_color: (R, G, B, A) base color for the cookie.
        chip_color: (R, G, B, A) base color for the chocolate chips.
        tray_color: (R, G, B, A) base color for the tray.

    Returns:
        Status string confirming the objects and lights created.
    """
    import bpy
    import random
    import math
    from mathutils import Vector, Euler

    # Ensure the target scene exists
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Helper to generate a flat color material
    def create_simple_material(mat_name, color):
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = color
            bsdf.inputs["Roughness"].default_value = 0.6
        return mat

    # === Step 1: Initialize Materials ===
    tray_mat = create_simple_material(f"{object_name}_TrayMat", tray_color)
    cookie_mat = create_simple_material(f"{object_name}_CookieMat", cookie_color)
    chip_mat = create_simple_material(f"{object_name}_ChipMat", chip_color)
    
    base_loc = Vector(location)
    
    # === Step 2: Create Tray Geometry ===
    bpy.ops.mesh.primitive_cube_add(
        size=2.0, 
        location=base_loc + Vector((0, 0, 0.1)) * scale
    )
    tray = bpy.context.active_object
    tray.name = f"{object_name}_Tray"
    tray.scale = (1.5 * scale, 1.5 * scale, 0.1 * scale)
    tray.data.materials.append(tray_mat)
    
    # === Step 3: Create Cookie Geometry ===
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=64, 
        radius=1.0, 
        depth=2.0, 
        location=base_loc + Vector((0, 0, 0.3)) * scale
    )
    cookie = bpy.context.active_object
    cookie.name = f"{object_name}_Cookie"
    cookie.scale = (0.8 * scale, 0.8 * scale, 0.1 * scale)
    bpy.ops.object.shade_smooth()
    cookie.data.materials.append(cookie_mat)
    cookie.parent = tray
    
    # === Step 4: Scatter Chocolate Chips ===
    num_chips = 12
    random.seed(42) # Seed for predictable randomness
    
    for i in range(num_chips):
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=16, 
            ring_count=8, 
            radius=1.0
        )
        chip = bpy.context.active_object
        chip.name = f"{object_name}_Chip_{i+1}"
        chip.scale = (0.08 * scale, 0.08 * scale, 0.06 * scale)
        bpy.ops.object.shade_smooth()
        chip.data.materials.append(chip_mat)
        
        # Calculate random polar coordinates within the cookie's radius
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(0.0, 0.65) * scale 
        
        cx = base_loc.x + r * math.cos(angle)
        cy = base_loc.y + r * math.sin(angle)
        cz = base_loc.z + 0.38 * scale # Sink slightly into the top face of the cookie
        
        chip.location = (cx, cy, cz)
        
        # Add random subtle rotation to make them look organic
        chip.rotation_euler = Euler((
            random.uniform(-0.5, 0.5), 
            random.uniform(-0.5, 0.5), 
            random.uniform(0, math.pi * 2)
        ), 'XYZ')
        
        chip.parent = cookie

    # === Step 5: Add Scene Lighting ===
    light_data = bpy.data.lights.new(name=f"{object_name}_LightData", type='AREA')
    light_data.energy = 850.0 * (scale ** 2) # Scale energy based on object scale
    light_data.color = (1.0, 0.85, 0.70) # Warm 4000K approximation
    light_data.shape = 'SQUARE'
    light_data.size = 2.0 * scale
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_AreaLight", object_data=light_data)
    scene.collection.objects.link(light_obj)
    
    # Position diagonally above and track to cookie
    light_obj.location = base_loc + Vector((1.5, -1.5, 2.0)) * scale
    direction = cookie.location - light_obj.location
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    light_obj.parent = tray

    return f"Created '{object_name}' hierarchy (Tray, Cookie, {num_chips} Chips, and Area Light) at {location}"
