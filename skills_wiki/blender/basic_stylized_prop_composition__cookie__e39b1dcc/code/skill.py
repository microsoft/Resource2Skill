def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedCookieProp",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.45, 0.2, 1.0),  # Cookie color
    **kwargs,
) -> str:
    """
    Create a Stylized Cookie on a Tray with scattered chips and warm lighting.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position for the tray base.
        scale: Uniform scale factor.
        material_color: Base color of the cookie dough (RGBA).
        **kwargs: Can include 'tray_color', 'chip_color', 'num_chips'.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector, Euler

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    tray_color = kwargs.get('tray_color', (0.1, 0.25, 0.7, 1.0))
    chip_color = kwargs.get('chip_color', (0.1, 0.05, 0.02, 1.0))
    num_chips = kwargs.get('num_chips', 12)

    # Helper function for material creation
    def create_mat(name, color, roughness):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = color
            bsdf.inputs["Roughness"].default_value = roughness
        return mat

    tray_mat = create_mat(f"{object_name}_TrayMat", tray_color, 0.3)
    cookie_mat = create_mat(f"{object_name}_CookieMat", material_color, 0.8)
    chip_mat = create_mat(f"{object_name}_ChipMat", chip_color, 0.4)

    # === 1. Create Tray ===
    tray_mesh = bpy.data.meshes.new(f"{object_name}_Tray_Mesh")
    tray_obj = bpy.data.objects.new(f"{object_name}_Tray", tray_mesh)
    scene.collection.objects.link(tray_obj)

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    # Scale to tray proportions (2.5 x 2.5 x 0.2)
    bmesh.ops.scale(bm, vec=(2.5, 2.5, 0.2), verts=bm.verts)

    # Inset and sink the top face
    top_face = None
    for f in bm.faces:
        if f.calc_center_median().z > 0.05:  # Find the top face
            top_face = f
            break

    if top_face:
        bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.1)
        bmesh.ops.translate(bm, vec=(0, 0, -0.05), verts=top_face.verts)

    bm.to_mesh(tray_mesh)
    bm.free()
    tray_obj.data.materials.append(tray_mat)

    # === 2. Create Cookie ===
    cookie_mesh = bpy.data.meshes.new(f"{object_name}_Cookie_Mesh")
    cookie_obj = bpy.data.objects.new(f"{object_name}_Cookie", cookie_mesh)
    scene.collection.objects.link(cookie_obj)

    bm = bmesh.new()
    # A cone with identical radii acts as a cylinder, robust across API versions
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=32, radius1=0.8, radius2=0.8, depth=0.15)
    for f in bm.faces:
        f.smooth = True
    bm.to_mesh(cookie_mesh)
    bm.free()

    cookie_obj.location = (0, 0, 0.125)  # Rest inside the tray lip
    cookie_obj.parent = tray_obj
    cookie_obj.data.materials.append(cookie_mat)

    # === 3. Create Chocolate Chips ===
    chip_mesh = bpy.data.meshes.new(f"{object_name}_Chip_Mesh")
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=8, radius=0.08)
    for f in bm.faces:
        f.smooth = True
    bm.to_mesh(chip_mesh)
    bm.free()

    for i in range(num_chips):
        chip_obj = bpy.data.objects.new(f"{object_name}_Chip_{i}", chip_mesh)
        scene.collection.objects.link(chip_obj)
        chip_obj.parent = cookie_obj
        chip_obj.data.materials.append(chip_mat)
        
        # Distribute randomly across the top surface of the cookie
        angle = random.uniform(0, math.pi * 2)
        radius = random.uniform(0, 0.65)
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        z = 0.075  # Sitting slightly embedded in the top face
        
        chip_obj.location = (x, y, z)
        chip_obj.rotation_euler = Euler((random.uniform(0, 3.14), random.uniform(0, 3.14), random.uniform(0, 3.14)))

    # === 4. Create Warm Area Light ===
    light_data = bpy.data.lights.new(name=f"{object_name}_Light", type='AREA')
    light_data.energy = 800.0
    light_data.color = (1.0, 0.85, 0.7)  # Warm 4000K look
    light_data.size = 2.0

    light_obj = bpy.data.objects.new(name=f"{object_name}_LightObj", object_data=light_data)
    scene.collection.objects.link(light_obj)
    light_obj.parent = tray_obj
    light_obj.location = (1.5, -1.5, 2.0)
    # Point downwards and slightly inward at the cookie
    light_obj.rotation_euler = Euler((math.radians(45), 0, math.radians(45)))

    # === 5. Final Positioning & Scaling ===
    tray_obj.location = Vector(location)
    tray_obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' (Cookie on Tray) at {location} with {num_chips} chips and warm lighting."
