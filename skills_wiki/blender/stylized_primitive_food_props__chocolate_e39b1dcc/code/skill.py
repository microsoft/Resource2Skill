def create_stylized_cookie_prop(
    scene_name: str = "Scene",
    object_name: str = "CookieProp",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.76, 0.60, 0.40),
    **kwargs,
) -> str:
    """
    Create a Stylized Chocolate Chip Cookie and Tray in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the parent empty object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color of the cookie dough.
        **kwargs: num_chips (int) to define how many chocolate chips to scatter.

    Returns:
        Status string describing the created asset.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    num_chips = kwargs.get("num_chips", 14)

    # === Step 1: Create Materials ===
    cookie_mat = bpy.data.materials.new(name=f"{object_name}_CookieMat")
    cookie_mat.use_nodes = True
    bsdf = cookie_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.8

    chip_mat = bpy.data.materials.new(name=f"{object_name}_ChipMat")
    chip_mat.use_nodes = True
    chip_bsdf = chip_mat.node_tree.nodes.get("Principled BSDF")
    if chip_bsdf:
        chip_bsdf.inputs['Base Color'].default_value = (0.05, 0.02, 0.01, 1.0)
        chip_bsdf.inputs['Roughness'].default_value = 0.4
        
    tray_mat = bpy.data.materials.new(name=f"{object_name}_TrayMat")
    tray_mat.use_nodes = True
    tray_bsdf = tray_mat.node_tree.nodes.get("Principled BSDF")
    if tray_bsdf:
        tray_bsdf.inputs['Base Color'].default_value = (0.02, 0.15, 0.50, 1.0)
        tray_bsdf.inputs['Roughness'].default_value = 0.3

    # === Step 2: Create Parent Controller ===
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    parent_obj = bpy.context.active_object
    parent_obj.name = object_name
    parent_obj.scale = (scale, scale, scale)

    # === Step 3: Create the Tray ===
    tray_mesh = bpy.data.meshes.new(f"{object_name}_TrayMesh")
    tray_obj = bpy.data.objects.new(f"{object_name}_Tray", tray_mesh)
    scene.collection.objects.link(tray_obj)
    tray_obj.parent = parent_obj
    tray_obj.data.materials.append(tray_mat)
    
    bm_tray = bmesh.new()
    bmesh.ops.create_cube(bm_tray, size=1.0)
    
    # Scale cube to be wide and flat, then drop it so top is at z=0
    bmesh.ops.scale(bm_tray, vec=(4.0, 4.0, 0.2), verts=bm_tray.verts)
    bmesh.ops.translate(bm_tray, vec=(0, 0, -0.1), verts=bm_tray.verts)
    
    # Identify the top face and inset it to create a lip
    bm_tray.faces.ensure_lookup_table()
    top_face = max(bm_tray.faces, key=lambda f: f.calc_center_median().z)
    bmesh.ops.inset_region(bm_tray, faces=[top_face], thickness=0.1)
    
    # Push the newly inset top face down to create the tray cavity (floor at z = -0.1)
    bmesh.ops.translate(bm_tray, vec=(0, 0, -0.1), verts=top_face.verts)
    
    bm_tray.to_mesh(tray_mesh)
    bm_tray.free()

    # === Step 4: Create the Cookie Base ===
    cookie_mesh = bpy.data.meshes.new(f"{object_name}_BaseMesh")
    cookie_obj = bpy.data.objects.new(f"{object_name}_Base", cookie_mesh)
    scene.collection.objects.link(cookie_obj)
    cookie_obj.parent = parent_obj
    cookie_obj.data.materials.append(cookie_mat)

    bm_cookie = bmesh.new()
    # A cone with identical radii is a cylinder. Depth 0.2 centers it at 0.
    bmesh.ops.create_cone(bm_cookie, cap_ends=True, segments=32, radius1=1.2, radius2=1.2, depth=0.2)
    # The tray floor is at z = -0.1, so keeping the cookie centered at z=0 
    # perfectly rests its bottom (-0.1) on the tray floor.
    
    for f in bm_cookie.faces:
        f.smooth = True
        
    bm_cookie.to_mesh(cookie_mesh)
    bm_cookie.free()

    # === Step 5: Create the Chocolate Chips ===
    # Pre-generate a single chip mesh to share across instances
    chip_mesh = bpy.data.meshes.new(f"{object_name}_ChipMesh")
    bm_chip = bmesh.new()
    bmesh.ops.create_uvsphere(bm_chip, u_segments=16, v_segments=8, radius=0.1)
    bmesh.ops.scale(bm_chip, vec=(1.0, 1.0, 0.5), verts=bm_chip.verts) # Squash it
    for f in bm_chip.faces:
        f.smooth = True
    bm_chip.to_mesh(chip_mesh)
    bm_chip.free()

    random.seed(hash(object_name)) # Deterministic scatter based on object name
    
    for i in range(num_chips):
        chip_obj = bpy.data.objects.new(f"{object_name}_Chip_{i}", chip_mesh)
        scene.collection.objects.link(chip_obj)
        chip_obj.parent = parent_obj
        chip_obj.data.materials.append(chip_mat)
        
        # Distribute randomly within the cookie's radius
        angle = random.uniform(0, math.pi * 2)
        radius = math.sqrt(random.uniform(0, 1)) * 1.05 # Slightly smaller than cookie radius 1.2
        
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        z = 0.1 # Top surface of the cookie
        
        chip_obj.location = (x, y, z)
        
        # Add random rotation and subtle scaling variance
        chip_obj.rotation_euler = (
            random.uniform(-0.3, 0.3),
            random.uniform(-0.3, 0.3),
            random.uniform(0, math.pi * 2)
        )
        s = random.uniform(0.7, 1.3)
        chip_obj.scale = (s, s, s)

    return f"Created '{object_name}' (Stylized Cookie on Tray with {num_chips} chips) at {location}"
