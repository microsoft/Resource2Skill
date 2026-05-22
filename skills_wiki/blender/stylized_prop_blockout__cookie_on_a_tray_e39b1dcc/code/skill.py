def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedCookieTray",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.3, 0.1),
    **kwargs,
) -> str:
    """
    Create a Stylized Cookie on a Tray in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the master parent object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the cookie dough.
        **kwargs: 
            tray_color (tuple): (R, G, B) color for the tray.
            num_chips (int): Number of chocolate chips to scatter.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Parse kwargs
    tray_color = kwargs.get("tray_color", (0.1, 0.2, 0.6))
    num_chips = kwargs.get("num_chips", 12)

    # === Master Controller ===
    master = bpy.data.objects.new(object_name, None)
    master.empty_display_size = 2.0
    master.empty_display_type = 'ARROWS'
    master.location = location
    master.scale = (scale, scale, scale)
    scene.collection.objects.link(master)

    # === Materials ===
    # 1. Cookie Dough
    cookie_mat = bpy.data.materials.new(f"{object_name}_CookieMat")
    cookie_mat.use_nodes = True
    c_bsdf = cookie_mat.node_tree.nodes.get("Principled BSDF")
    c_bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
    c_bsdf.inputs["Roughness"].default_value = 0.8

    # 2. Chocolate Chips
    chip_mat = bpy.data.materials.new(f"{object_name}_ChipMat")
    chip_mat.use_nodes = True
    ch_bsdf = chip_mat.node_tree.nodes.get("Principled BSDF")
    ch_bsdf.inputs["Base Color"].default_value = (0.05, 0.02, 0.01, 1.0)
    ch_bsdf.inputs["Roughness"].default_value = 0.5

    # 3. Tray
    tray_mat = bpy.data.materials.new(f"{object_name}_TrayMat")
    tray_mat.use_nodes = True
    t_bsdf = tray_mat.node_tree.nodes.get("Principled BSDF")
    t_bsdf.inputs["Base Color"].default_value = (*tray_color, 1.0)
    t_bsdf.inputs["Roughness"].default_value = 0.4

    # === 1. Create Tray (Using BMesh for Inset/Extrude) ===
    tray_mesh = bpy.data.meshes.new(f"{object_name}_TrayMesh")
    tray_mesh.materials.append(tray_mat)
    tray_obj = bpy.data.objects.new(f"{object_name}_Tray", tray_mesh)
    scene.collection.objects.link(tray_obj)
    tray_obj.parent = master

    bm_tray = bmesh.new()
    bmesh.ops.create_cube(bm_tray, size=2.0)
    # Scale cube down on Z to make it a flat tray board
    bmesh.ops.scale(bm_tray, vec=(1.0, 1.0, 0.1), verts=bm_tray.verts)
    bm_tray.faces.ensure_lookup_table()
    
    # Find the top face (Z normal pointing up)
    top_face = next((f for f in bm_tray.faces if f.normal.z > 0.9), None)
    if top_face:
        # Inset the top face to create a rim
        bmesh.ops.inset_region(bm_tray, faces=[top_face], thickness=0.1)
        # Extrude downwards by translating the inset face down
        bmesh.ops.translate(bm_tray, vec=(0, 0, -0.1), verts=top_face.verts)
        
    bm_tray.to_mesh(tray_mesh)
    bm_tray.free()

    # === 2. Create Cookie ===
    cookie_mesh = bpy.data.meshes.new(f"{object_name}_CookieMesh")
    cookie_mesh.materials.append(cookie_mat)
    cookie_obj = bpy.data.objects.new(f"{object_name}_Cookie", cookie_mesh)
    scene.collection.objects.link(cookie_obj)
    cookie_obj.parent = master
    # The tray cavity floor is at Z = 0.0 in local space
    cookie_obj.location = (0, 0, 0.0) 

    bm_cookie = bmesh.new()
    # create_cone with equal radii acts as a cylinder
    bmesh.ops.create_cone(
        bm_cookie, cap_ends=True, cap_tris=False, segments=32, 
        radius1=0.7, radius2=0.7, depth=0.2
    )
    # Shift vertices so the cylinder base rests exactly at Z=0
    bmesh.ops.translate(bm_cookie, vec=(0, 0, 0.1), verts=bm_cookie.verts)
    bm_cookie.to_mesh(cookie_mesh)
    bm_cookie.free()

    # Apply smooth shading to cookie
    for poly in cookie_mesh.polygons:
        poly.use_smooth = True

    # === 3. Create & Scatter Chocolate Chips ===
    chip_mesh = bpy.data.meshes.new(f"{object_name}_ChipMesh")
    chip_mesh.materials.append(chip_mat)
    
    bm_chip = bmesh.new()
    bmesh.ops.create_uvsphere(bm_chip, u_segments=16, v_segments=8, radius=0.06)
    bm_chip.to_mesh(chip_mesh)
    bm_chip.free()
    
    for poly in chip_mesh.polygons:
        poly.use_smooth = True

    for i in range(num_chips):
        chip_obj = bpy.data.objects.new(f"{object_name}_Chip_{i}", chip_mesh)
        scene.collection.objects.link(chip_obj)
        chip_obj.parent = master
        
        # Calculate random polar coordinates on the cookie surface
        r_dist = random.uniform(0.0, 0.55) # Stay within cookie radius
        theta = random.uniform(0.0, 2.0 * math.pi)
        
        cx = r_dist * math.cos(theta)
        cy = r_dist * math.sin(theta)
        # Place slightly embedded into the top of the cookie (Cookie top is Z=0.2)
        cz = 0.2 + random.uniform(-0.02, 0.01) 
        
        chip_obj.location = (cx, cy, cz)
        
        # Randomize rotation and slight scale variation
        chip_obj.rotation_euler = (
            random.uniform(0, 3.14), 
            random.uniform(0, 3.14), 
            random.uniform(0, 3.14)
        )
        chip_obj.scale = (
            random.uniform(0.8, 1.2), 
            random.uniform(0.8, 1.2), 
            random.uniform(0.5, 0.9)
        )

    # === 4. Lighting ===
    light_data = bpy.data.lights.new(name=f"{object_name}_AreaLight", type='AREA')
    light_data.energy = 800.0
    light_data.color = (1.0, 0.95, 0.85) # Slightly warm light
    light_data.size = 2.0
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_Light", object_data=light_data)
    scene.collection.objects.link(light_obj)
    light_obj.parent = master
    
    # Position diagonally above and track to the cookie center
    light_obj.location = (1.5, -1.5, 2.0)
    direction = Vector((0, 0, 0)) - light_obj.location
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    return f"Created '{object_name}' (Cookie on Tray with {num_chips} chips) at {location} scaled by {scale}."
