def create_cookie_scene(
    scene_name: str = "Scene",
    object_name: str = "KevinCookie",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    cookie_color: tuple = (0.7, 0.4, 0.15),
    chip_color: tuple = (0.08, 0.03, 0.01),
    tray_color: tuple = (0.1, 0.3, 0.8),
    num_chips: int = 15,
    **kwargs,
) -> str:
    """
    Creates a stylized 3D chocolate chip cookie on a baking tray with warm area lighting.

    Args:
        scene_name: Name of the active scene.
        object_name: Base name for the generated objects.
        location: (x, y, z) placement of the entire assembly.
        scale: Master scale for the assembly.
        cookie_color: RGB tuple for the cookie dough.
        chip_color: RGB tuple for the chocolate chips.
        tray_color: RGB tuple for the tray.
        num_chips: Amount of chocolate chips to scatter.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Helper: Material Creation ---
    def create_material(name, color, roughness):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Handle Blender 4.0+ Principled BSDF changes if needed, but Base Color is standard
            bsdf.inputs["Base Color"].default_value = (*color, 1.0)
            bsdf.inputs["Roughness"].default_value = roughness
        return mat

    mat_cookie = create_material(f"{object_name}_Mat_Cookie", cookie_color, 0.8)
    mat_chip = create_material(f"{object_name}_Mat_Chip", chip_color, 0.3)
    mat_tray = create_material(f"{object_name}_Mat_Tray", tray_color, 0.5)

    # Master Parent Empty
    parent_empty = bpy.data.objects.new(object_name, None)
    parent_empty.location = location
    parent_empty.scale = (scale, scale, scale)
    scene.collection.objects.link(parent_empty)

    # --- Step 1: Baking Tray ---
    tray_mesh = bpy.data.meshes.new(f"{object_name}_Tray")
    tray_obj = bpy.data.objects.new(f"{object_name}_Tray", tray_mesh)
    tray_obj.parent = parent_empty
    scene.collection.objects.link(tray_obj)

    bm_tray = bmesh.new()
    bmesh.ops.create_cube(bm_tray, size=2.0)
    # Scale to make a flat plate
    bmesh.ops.scale(bm_tray, vec=(1.5, 1.5, 0.1), verts=bm_tray.verts)
    
    # Inset and sink top face to make a tray
    top_face = next((f for f in bm_tray.faces if f.normal.z > 0.9), None)
    if top_face:
        bmesh.ops.inset_region(bm_tray, faces=[top_face], thickness=0.1)
        bmesh.ops.translate(bm_tray, vec=(0, 0, -0.15), verts=top_face.verts)
    
    bm_tray.to_mesh(tray_mesh)
    bm_tray.free()
    tray_obj.data.materials.append(mat_tray)
    tray_obj.location = (0, 0, -0.1)

    # --- Step 2: Cookie Base ---
    cookie_mesh = bpy.data.meshes.new(f"{object_name}_Dough")
    cookie_obj = bpy.data.objects.new(f"{object_name}_Dough", cookie_mesh)
    cookie_obj.parent = parent_empty
    scene.collection.objects.link(cookie_obj)

    bm_cookie = bmesh.new()
    # A cone with equal radii acts as a cylinder
    bmesh.ops.create_cone(bm_cookie, cap_ends=True, cap_tris=False, segments=32, radius1=1.0, radius2=1.0, depth=0.2)
    bm_cookie.to_mesh(cookie_mesh)
    bm_cookie.free()
    
    for p in cookie_mesh.polygons:
        p.use_smooth = True
        
    cookie_obj.data.materials.append(mat_cookie)
    cookie_obj.location = (0, 0, 0.1)

    # --- Step 3: Chocolate Chips ---
    chip_mesh = bpy.data.meshes.new(f"{object_name}_Chip_Mesh")
    bm_chip = bmesh.new()
    bmesh.ops.create_uvsphere(bm_chip, u_segments=16, v_segments=8, radius=0.08)
    # Squash the sphere to look like a melted chip
    bmesh.ops.scale(bm_chip, vec=(1.0, 1.0, 0.6), verts=bm_chip.verts)
    bm_chip.to_mesh(chip_mesh)
    bm_chip.free()
    
    for p in chip_mesh.polygons:
        p.use_smooth = True
        
    chip_mesh.materials.append(mat_chip)

    # Scatter chips
    for i in range(num_chips):
        chip_obj = bpy.data.objects.new(f"{object_name}_Chip_{i}", chip_mesh)
        chip_obj.parent = cookie_obj
        scene.collection.objects.link(chip_obj)
        
        # Random polar coordinates for scatter within cookie radius (0.8 max to avoid edges)
        r = math.sqrt(random.uniform(0, 1)) * 0.85
        theta = random.uniform(0, 2 * math.pi)
        
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        z = 0.12 # Slightly embedded into the top of the cookie
        
        chip_obj.location = (x, y, z)
        # Add random yaw rotation and slight tilt for organic look
        chip_obj.rotation_euler = (
            random.uniform(-0.1, 0.1),
            random.uniform(-0.1, 0.1),
            random.uniform(0, 2 * math.pi)
        )

    # --- Step 4: Warm Scene Lighting ---
    light_data = bpy.data.lights.new(name=f"{object_name}_Light", type='AREA')
    light_data.energy = 850.0
    light_data.color = (1.0, 0.85, 0.7)  # Warm tungsten/baking temperature
    light_data.size = 2.0
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_Light", object_data=light_data)
    light_obj.parent = parent_empty
    scene.collection.objects.link(light_obj)
    
    # Position light and point it at the cookie
    light_pos = Vector((2.0, -2.0, 3.0))
    light_obj.location = light_pos
    direction = Vector((0, 0, 0)) - light_pos
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    return f"Created '{object_name}' (Cookie, Tray, {num_chips} Chips, Light) successfully at {location}."
