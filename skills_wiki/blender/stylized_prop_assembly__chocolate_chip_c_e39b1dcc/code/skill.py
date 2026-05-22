def create_cookie_scene(
    scene_name: str = "Scene",
    object_name: str = "ChocolateChipCookie",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    cookie_color: tuple = (0.7, 0.5, 0.25),
    chip_color: tuple = (0.08, 0.04, 0.01),
    tray_color: tuple = (0.1, 0.3, 0.8),
    **kwargs
) -> str:
    """
    Create a Stylized Chocolate Chip Cookie sitting on a tray in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created object hierarchy.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        cookie_color: (R, G, B) base color for the dough.
        chip_color: (R, G, B) base color for the chocolate chips.
        tray_color: (R, G, B) base color for the tray.

    Returns:
        Status string confirming successful creation.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector, Euler

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Helper function for materials
    def create_material(name, color, roughness=0.5):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*color, 1.0)
            bsdf.inputs["Roughness"].default_value = roughness
        return mat

    # Generate Materials
    tray_mat = create_material(f"{object_name}_TrayMat", tray_color, 0.3)
    cookie_mat = create_material(f"{object_name}_CookieMat", cookie_color, 0.8)
    chip_mat = create_material(f"{object_name}_ChipMat", chip_color, 0.2)

    # 1. Build the Tray
    bm_tray = bmesh.new()
    bmesh.ops.create_cube(bm_tray, size=2.0)
    # Scale to flat tray bounds
    bmesh.ops.scale(bm_tray, vec=(1.2, 1.2, 0.1), verts=bm_tray.verts)
    bmesh.ops.translate(bm_tray, vec=(0, 0, 0.1), verts=bm_tray.verts)

    # Inset top face and push down to create the tray rim
    top_faces = [f for f in bm_tray.faces if f.normal.z > 0.5]
    if top_faces:
        top_face = top_faces[0]
        bmesh.ops.inset_region(bm_tray, faces=[top_face], thickness=0.1)
        bmesh.ops.translate(bm_tray, vec=(0, 0, -0.1), verts=top_face.verts)

    mesh_tray = bpy.data.meshes.new(f"{object_name}_Tray")
    bm_tray.to_mesh(mesh_tray)
    bm_tray.free()
    tray_obj = bpy.data.objects.new(f"{object_name}_Tray", mesh_tray)
    tray_obj.data.materials.append(tray_mat)

    # 2. Build the Cookie Base (cylinder)
    bm_cookie = bmesh.new()
    bmesh.ops.create_cone(bm_cookie, cap_ends=True, cap_tris=False, segments=32, radius1=0.8, radius2=0.8, depth=0.2)
    # Move it so it rests perfectly inside the tray's inner surface
    bmesh.ops.translate(bm_cookie, vec=(0, 0, 0.2), verts=bm_cookie.verts)
    for f in bm_cookie.faces:
        f.smooth = True

    mesh_cookie = bpy.data.meshes.new(f"{object_name}_Cookie")
    bm_cookie.to_mesh(mesh_cookie)
    bm_cookie.free()
    cookie_obj = bpy.data.objects.new(f"{object_name}_Cookie", mesh_cookie)
    cookie_obj.data.materials.append(cookie_mat)

    # 3. Build and Scatter the Chocolate Chips
    bm_chips = bmesh.new()
    for _ in range(20):
        # Polar coordinate random scatter
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, 0.7)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = 0.3  # Set to the top surface height of the cookie base

        chip_radius = random.uniform(0.04, 0.08)
        ret = bmesh.ops.create_uvsphere(bm_chips, u_segments=12, v_segments=8, radius=chip_radius)
        verts = ret['verts']

        # Flatten it slightly and apply random rotation
        bmesh.ops.scale(bm_chips, vec=(1.0, 1.0, 0.6), verts=verts)
        rot = Euler((random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3), random.uniform(0, 6.28)), 'XYZ').to_matrix()
        bmesh.ops.rotate(bm_chips, cent=(0,0,0), matrix=rot, verts=verts)
        bmesh.ops.translate(bm_chips, vec=(x, y, z), verts=verts)

    for f in bm_chips.faces:
        f.smooth = True

    mesh_chips = bpy.data.meshes.new(f"{object_name}_Chips")
    bm_chips.to_mesh(mesh_chips)
    bm_chips.free()
    chips_obj = bpy.data.objects.new(f"{object_name}_Chips", mesh_chips)
    chips_obj.data.materials.append(chip_mat)

    # 4. Create Area Light for localized baking aesthetics
    light_data = bpy.data.lights.new(name=f"{object_name}_LightData", type='AREA')
    light_data.energy = 800 * (scale ** 2)
    light_data.color = (1.0, 0.9, 0.8) # Warm 4000K look
    light_data.size = 2.0 * scale
    light_obj = bpy.data.objects.new(name=f"{object_name}_Light", object_data=light_data)
    light_obj.location = (0, 0, 3)

    # 5. Connect Hierarchy and Apply Global Transforms
    root = bpy.data.objects.new(object_name, None)
    scene.collection.objects.link(root)
    scene.collection.objects.link(tray_obj)
    scene.collection.objects.link(cookie_obj)
    scene.collection.objects.link(chips_obj)
    scene.collection.objects.link(light_obj)

    tray_obj.parent = root
    cookie_obj.parent = root
    chips_obj.parent = root
    light_obj.parent = root

    root.location = Vector(location)
    root.scale = (scale, scale, scale)

    return f"Created '{object_name}' (Cookie, Tray, scattered Chips, and Light) at {location}"
