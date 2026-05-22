def create_object(
    scene_name: str = "Scene",
    object_name: str = "CookieAndTray",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.40, 0.20, 0.08),  # Cookie color
    **kwargs,
) -> str:
    """
    Create a Stylized Chocolate Chip Cookie on a blue tray with an Area Light.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the root empty and prefix for child objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the cookie dough.
        **kwargs: 
            tray_color: (R, G, B) color for the tray.
            chip_color: (R, G, B) color for the chocolate chips.

    Returns:
        Status string confirming creation.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector

    # Scene setup
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection

    # Extract Kwargs for additional colors
    tray_color = kwargs.get("tray_color", (0.05, 0.15, 0.60))
    chip_color = kwargs.get("chip_color", (0.03, 0.01, 0.005))

    # === Helper: Material Generator ===
    def make_material(name, color, roughness=0.6):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*color, 1.0)
            bsdf.inputs["Roughness"].default_value = roughness
        return mat

    mat_cookie = make_material(f"{object_name}_Mat_Cookie", material_color, 0.8)
    mat_chip = make_material(f"{object_name}_Mat_Chip", chip_color, 0.3)
    mat_tray = make_material(f"{object_name}_Mat_Tray", tray_color, 0.5)

    # === Step 1: Root Empty ===
    root = bpy.data.objects.new(object_name, None)
    root.empty_display_type = 'PLAIN_AXES'
    root.location = Vector(location)
    root.scale = (scale, scale, scale)
    collection.objects.link(root)

    # === Step 2: Create Tray ===
    mesh_tray = bpy.data.meshes.new(f"{object_name}_Tray")
    obj_tray = bpy.data.objects.new(mesh_tray.name, mesh_tray)
    obj_tray.parent = root
    obj_tray.data.materials.append(mat_tray)
    collection.objects.link(obj_tray)

    bm_tray = bmesh.new()
    # Create flat rectangular base
    bmesh.ops.create_cube(bm_tray, size=1.0)
    bmesh.ops.scale(bm_tray, vec=(3.0, 3.0, 0.2), verts=bm_tray.verts)
    
    # Extract top face (normal points up along Z)
    top_face = next(f for f in bm_tray.faces if f.normal.z > 0.9)
    
    # Inset face to create a rim, then translate inner face down to make a tray
    bmesh.ops.inset_region(bm_tray, faces=[top_face], thickness=0.15)
    bmesh.ops.translate(bm_tray, vec=(0, 0, -0.1), verts=top_face.verts)
    
    bm_tray.to_mesh(mesh_tray)
    bm_tray.free()

    # === Step 3: Create Cookie Base ===
    mesh_cookie = bpy.data.meshes.new(f"{object_name}_CookieBase")
    obj_cookie = bpy.data.objects.new(mesh_cookie.name, mesh_cookie)
    obj_cookie.parent = root
    obj_cookie.location = (0, 0, 0.1) # Sit inside tray
    obj_cookie.data.materials.append(mat_cookie)
    collection.objects.link(obj_cookie)

    bm_cookie = bmesh.new()
    # Use create_cone with equal radii to make a cylinder (bmesh standard approach)
    bmesh.ops.create_cone(
        bm_cookie, cap_ends=True, cap_tris=False, segments=32, 
        radius1=1.0, radius2=1.0, depth=0.2
    )
    bm_cookie.to_mesh(mesh_cookie)
    bm_cookie.free()
    
    # Shade Smooth
    for poly in mesh_cookie.polygons:
        poly.use_smooth = True

    # === Step 4: Scatter Chocolate Chips ===
    num_chips = 12
    cookie_radius = 0.85
    chip_radius = 0.08
    
    for i in range(num_chips):
        mesh_chip = bpy.data.meshes.new(f"{object_name}_Chip_{i}")
        obj_chip = bpy.data.objects.new(mesh_chip.name, mesh_chip)
        obj_chip.parent = obj_cookie
        obj_chip.data.materials.append(mat_chip)
        collection.objects.link(obj_chip)
        
        bm_chip = bmesh.new()
        bmesh.ops.create_uvsphere(bm_chip, u_segments=16, v_segments=8, radius=chip_radius)
        # Squash chips slightly to look melted
        bmesh.ops.scale(bm_chip, vec=(1.0, 1.0, 0.6), verts=bm_chip.verts)
        bm_chip.to_mesh(mesh_chip)
        bm_chip.free()
        
        for poly in mesh_chip.polygons:
            poly.use_smooth = True
            
        # Polar scattering logic
        r = random.uniform(0, cookie_radius)
        theta = random.uniform(0, 2 * math.pi)
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        
        # Place firmly on top of the cookie surface (Z offset based on depth)
        obj_chip.location = (x, y, 0.1)
        # Random rotation around Z
        obj_chip.rotation_euler = (0, 0, random.uniform(0, math.pi))

    # === Step 5: Add Area Light (Tutorial Environment) ===
    light_data = bpy.data.lights.new(name=f"{object_name}_Light", type='AREA')
    light_data.energy = 850.0
    light_data.color = (1.0, 0.85, 0.70) # Warm 4000K mapping
    light_data.shape = 'SQUARE'
    light_data.size = 2.0
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_AreaLight", object_data=light_data)
    light_obj.parent = root
    light_obj.location = (0.5, -0.5, 3.0)
    # Point light towards the cookie
    light_obj.rotation_euler = (0.1, -0.1, 0)
    collection.objects.link(light_obj)

    return f"Created '{object_name}' scene (Tray, Cookie, {num_chips} Chips, and Area Light) at {location} with scale {scale}."
