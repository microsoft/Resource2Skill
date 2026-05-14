def create_stylized_cookie_scene(
    scene_name: str = "Scene",
    object_name: str = "StylizedCookie",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    cookie_color: tuple = (0.65, 0.45, 0.25),
    chip_color: tuple = (0.08, 0.04, 0.01),
    tray_color: tuple = (0.1, 0.25, 0.75),
    num_chips: int = 15,
    **kwargs,
) -> str:
    """
    Create a stylized chocolate chip cookie on a tray with warm area lighting.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position for the master parent.
        scale: Uniform scale factor for the entire scene.
        cookie_color: RGB tuple for the cookie base.
        chip_color: RGB tuple for the chocolate chips.
        tray_color: RGB tuple for the tray.
        num_chips: Amount of chocolate chips to scatter.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math
    import random

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection

    # === Step 1: Create Materials ===
    def make_mat(name, color):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*color, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.6
        return mat

    cookie_mat = make_mat(f"{object_name}_Mat_Cookie", cookie_color)
    chip_mat = make_mat(f"{object_name}_Mat_Chip", chip_color)
    tray_mat = make_mat(f"{object_name}_Mat_Tray", tray_color)

    # === Step 2: Create Master Parent ===
    master_empty = bpy.data.objects.new(object_name, None)
    master_empty.empty_display_type = 'ARROWS'
    master_empty.location = Vector(location)
    master_empty.scale = (scale, scale, scale)
    collection.objects.link(master_empty)

    # === Step 3: Create Tray (Base sits at Z=0) ===
    tray_mesh = bpy.data.meshes.new(f"{object_name}_TrayMesh")
    tray_obj = bpy.data.objects.new(f"{object_name}_Tray", tray_mesh)
    collection.objects.link(tray_obj)
    tray_obj.parent = master_empty
    tray_obj.data.materials.append(tray_mat)

    bm_tray = bmesh.new()
    bmesh.ops.create_cube(bm_tray, size=1.0)
    # Scale to be a wide thin plate (X:3, Y:3, Z:0.2)
    bmesh.ops.scale(bm_tray, vec=(3.0, 3.0, 0.2), verts=bm_tray.verts)
    # Translate so top is exactly at Z=0
    bmesh.ops.translate(bm_tray, vec=(0, 0, -0.1), verts=bm_tray.verts)
    
    top_face_tray = next((f for f in bm_tray.faces if f.normal.z > 0.9), None)
    if top_face_tray:
        ret = bmesh.ops.inset_region(bm_tray, faces=[top_face_tray], thickness=0.1)
        bmesh.ops.translate(bm_tray, vec=(0, 0, -0.1), verts=list(set(v for f in ret['faces'] for v in f.verts)))
    bm_tray.to_mesh(tray_mesh)
    bm_tray.free()

    # === Step 4: Create Cookie Base ===
    cookie_mesh = bpy.data.meshes.new(f"{object_name}_BaseMesh")
    cookie_obj = bpy.data.objects.new(f"{object_name}_Base", cookie_mesh)
    collection.objects.link(cookie_obj)
    cookie_obj.parent = master_empty
    cookie_obj.data.materials.append(cookie_mat)

    bm_cookie = bmesh.new()
    # Create cylinder/cone. depth 0.3 means it goes from Z=-0.15 to Z=0.15
    bmesh.ops.create_cone(bm_cookie, cap_ends=True, cap_tris=False, segments=32, radius1=1.0, radius2=1.0, depth=0.3)
    # Translate so bottom sits on the tray (Z=0), top is at Z=0.3
    bmesh.ops.translate(bm_cookie, vec=(0, 0, 0.15), verts=bm_cookie.verts)

    top_face_cookie = next((f for f in bm_cookie.faces if f.normal.z > 0.9), None)
    if top_face_cookie:
        ret = bmesh.ops.inset_region(bm_cookie, faces=[top_face_cookie], thickness=0.1)
        bmesh.ops.translate(bm_cookie, vec=(0, 0, -0.05), verts=list(set(v for f in ret['faces'] for v in f.verts)))

    for f in bm_cookie.faces:
        f.smooth = True
    bm_cookie.to_mesh(cookie_mesh)
    bm_cookie.free()

    # === Step 5: Scatter Chocolate Chips ===
    for i in range(num_chips):
        r = random.uniform(0.0, 0.8)
        theta = random.uniform(0.0, 2.0 * math.pi)
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        z = 0.28  # Slightly embedded in the interior cookie floor (which is at 0.25)

        chip_mesh = bpy.data.meshes.new(f"{object_name}_ChipMesh_{i}")
        chip_obj = bpy.data.objects.new(f"{object_name}_Chip_{i}", chip_mesh)
        collection.objects.link(chip_obj)
        chip_obj.parent = master_empty
        chip_obj.data.materials.append(chip_mat)

        bm_chip = bmesh.new()
        bmesh.ops.create_uvsphere(bm_chip, u_segments=16, v_segments=8, radius=0.08)
        bmesh.ops.translate(bm_chip, vec=(x, y, z), verts=bm_chip.verts)
        for f in bm_chip.faces:
            f.smooth = True
        bm_chip.to_mesh(chip_mesh)
        bm_chip.free()

    # === Step 6: Add Warm Area Lighting ===
    light_data = bpy.data.lights.new(name=f"{object_name}_LightData", type='AREA')
    light_data.energy = 800.0
    light_data.size = 2.0
    light_data.color = (1.0, 0.85, 0.65) # Warm baked feel

    light_obj = bpy.data.objects.new(name=f"{object_name}_Light", object_data=light_data)
    collection.objects.link(light_obj)
    light_obj.parent = master_empty
    
    # Position light and point it at the cookie
    light_pos = Vector((2.0, -2.0, 3.0))
    light_obj.location = light_pos
    direction = Vector((0, 0, 0)) - light_pos
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    return f"Created '{object_name}' (Cookie, Tray, {num_chips} Chips, Light) at {location} scaled by {scale}x."
