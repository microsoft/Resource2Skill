def create_object(
    scene_name: str = "Scene",
    object_name: str = "CookieAsset",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    cookie_color: tuple = (0.6, 0.35, 0.1),
    chip_color: tuple = (0.05, 0.02, 0.01),
    tray_color: tuple = (0.05, 0.2, 0.6),
    **kwargs,
) -> str:
    """
    Create a composite prop of a Chocolate Chip Cookie sitting on a tray.

    Args:
        scene_name: Name of the target scene.
        object_name: Root name for the created objects.
        location: (x, y, z) world-space position of the tray.
        scale: Uniform scale factor for the entire asset.
        cookie_color: (R, G, B) base color for the cookie dough.
        chip_color: (R, G, B) base color for the chocolate chips.
        tray_color: (R, G, B) base color for the serving tray.
        **kwargs: Can include 'num_chips' (int) to define chocolate chip density.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    num_chips = kwargs.get("num_chips", 15)

    # === Helper: Material Setup ===
    def make_material(name, color, roughness):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Handle Blender 4.0+ Base Color input changes gracefully
            color_input = bsdf.inputs.get('Base Color') or bsdf.inputs.get('Base Color')
            if color_input:
                color_input.default_value = (*color, 1.0)
            roughness_input = bsdf.inputs.get('Roughness')
            if roughness_input:
                roughness_input.default_value = roughness
        return mat

    tray_mat = make_material(f"{object_name}_TrayMat", tray_color, 0.5)
    cookie_mat = make_material(f"{object_name}_CookieMat", cookie_color, 0.85)
    chip_mat = make_material(f"{object_name}_ChipMat", chip_color, 0.2)

    # === Step 1: Create the Tray ===
    bm_tray = bmesh.new()
    bmesh.ops.create_cube(bm_tray, size=1.0)
    # Scale cube into a flat 4x4 board (Z range becomes -0.1 to 0.1)
    bmesh.ops.scale(bm_tray, vec=(4.0, 4.0, 0.2), verts=bm_tray.verts)
    
    # Identify the top-facing polygon to inset
    top_face = None
    max_z = -1000
    for f in bm_tray.faces:
        if f.normal.z > 0.9:
            cz = f.calc_center_median().z
            if cz > max_z:
                max_z = cz
                top_face = f
                
    if top_face:
        # Inset the top face to create a rim, then translate the inner face down to form the tray floor
        bmesh.ops.inset_region(bm_tray, faces=[top_face], thickness=0.2)
        bmesh.ops.translate(bm_tray, verts=top_face.verts, vec=(0, 0, -0.1))
        
    tray_mesh = bpy.data.meshes.new(f"{object_name}_TrayMesh")
    bm_tray.to_mesh(tray_mesh)
    bm_tray.free()
    tray_mesh.materials.append(tray_mat)
    
    tray_obj = bpy.data.objects.new(object_name, tray_mesh)
    scene.collection.objects.link(tray_obj)

    # === Step 2: Create the Cookie Base ===
    bm_cookie = bmesh.new()
    # Create a cylinder (cone with equal radii) with radius 1.2 and depth 0.2 (Z range -0.1 to 0.1)
    bmesh.ops.create_cone(bm_cookie, cap_ends=True, cap_tris=False, segments=32, radius1=1.2, radius2=1.2, depth=0.2)
    for f in bm_cookie.faces:
        f.smooth = True  # Shade smooth
        
    cookie_mesh = bpy.data.meshes.new(f"{object_name}_CookieMesh")
    bm_cookie.to_mesh(cookie_mesh)
    bm_cookie.free()
    cookie_mesh.materials.append(cookie_mat)
    
    cookie_obj = bpy.data.objects.new(f"{object_name}_Cookie", cookie_mesh)
    scene.collection.objects.link(cookie_obj)
    cookie_obj.parent = tray_obj
    
    # Place cookie on the tray floor (Tray floor is at local Z=0.0. Cookie bottom is at local Z=-0.1. Shift up by 0.1)
    cookie_obj.location = (0, 0, 0.1)

    # === Step 3: Create & Distribute Chocolate Chips ===
    bm_chip = bmesh.new()
    bmesh.ops.create_uvsphere(bm_chip, u_segments=16, v_segments=8, radius=0.08)
    # Flatten the spheres on the Z-axis to look like melted chips
    bmesh.ops.scale(bm_chip, vec=(1.0, 1.0, 0.6), verts=bm_chip.verts)
    for f in bm_chip.faces:
        f.smooth = True
        
    chip_mesh = bpy.data.meshes.new(f"{object_name}_ChipMesh")
    bm_chip.to_mesh(chip_mesh)
    bm_chip.free()
    chip_mesh.materials.append(chip_mat)
    
    for i in range(num_chips):
        chip_obj = bpy.data.objects.new(f"{object_name}_Chip_{i}", chip_mesh)
        scene.collection.objects.link(chip_obj)
        chip_obj.parent = cookie_obj
        
        # Calculate random polar coordinates within the cookie's radius
        r = random.uniform(0.0, 1.0) 
        theta = random.uniform(0, 2 * math.pi)
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        
        # Cookie top is at local Z=0.1. Sink chip slightly (Z=0.08) so it intersects the dough
        chip_obj.location = (x, y, 0.08)
        # Random slight tilt to make placement look organic
        chip_obj.rotation_euler = (
            random.uniform(-0.3, 0.3),
            random.uniform(-0.3, 0.3),
            random.uniform(0, 2 * math.pi)
        )

    # === Step 4: Finalize Global Transforms ===
    # The tray acts as the master parent controller for the prop
    tray_obj.location = Vector(location)
    tray_obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' (1 Tray, 1 Cookie Base, {num_chips} Chips) at {location}"
