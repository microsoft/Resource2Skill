def create_object(
    scene_name: str = "Scene",
    object_name: str = "CookieDiorama",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.4, 0.15),  # Cookie base color
    **kwargs,
) -> str:
    """
    Create a Stylized Chocolate Chip Cookie on a Tray in the active scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position of the diorama.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the cookie dough.
        **kwargs: Optional color overrides (tray_color, chip_color, chip_count).

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector

    # Fetch target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Helper: BMesh to Object ===
    def create_mesh_obj(name, bm):
        mesh = bpy.data.meshes.new(name)
        bm.to_mesh(mesh)
        bm.free()
        obj = bpy.data.objects.new(name, mesh)
        scene.collection.objects.link(obj)
        return obj

    # === Helper: Simple Color Material ===
    def create_color_mat(name, color):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (*color, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.6  # Matte, food-like
        return mat

    # Extract optional kwargs
    tray_color = kwargs.get("tray_color", (0.1, 0.2, 0.8))
    chip_color = kwargs.get("chip_color", (0.05, 0.02, 0.01))
    chip_count = kwargs.get("chip_count", 15)

    # Setup parent empty for composability
    parent_empty = bpy.data.objects.new(object_name, None)
    scene.collection.objects.link(parent_empty)
    parent_empty.location = Vector(location)
    parent_empty.scale = (scale, scale, scale)

    # === Step 1: Create Tray (Inset & Extrude) ===
    bm_tray = bmesh.new()
    bmesh.ops.create_cube(bm_tray, size=1.0)
    # Flatten and widen the cube (height = 0.2, top surface at Z=0.1)
    bmesh.ops.scale(bm_tray, vec=(3.0, 3.0, 0.2), verts=bm_tray.verts)
    
    # Isolate top face
    top_face = next((f for f in bm_tray.faces if f.normal.z > 0.9), None)
    if top_face:
        # Inset to create a lip
        bmesh.ops.inset_region(bm_tray, faces=[top_face], thickness=0.2)
        # Extrude internal region down
        bmesh.ops.extrude_face_region(bm_tray, geom=[top_face])
        bmesh.ops.translate(bm_tray, vec=(0, 0, -0.15), verts=top_face.verts)
        
    tray_obj = create_mesh_obj(f"{object_name}_Tray", bm_tray)
    tray_obj.parent = parent_empty
    tray_obj.data.materials.append(create_color_mat(f"{object_name}_TrayMat", tray_color))

    # === Step 2: Create Cookie Base (Smooth Cylinder) ===
    bm_cookie = bmesh.new()
    # Using cone with equal radii to create a cylinder
    bmesh.ops.create_cone(
        bm_cookie, cap_ends=True, cap_tris=False, segments=32, 
        radius1=1.2, radius2=1.2, depth=0.3
    )
    # Move up so bottom rests on the tray interior (Z=0.1)
    bmesh.ops.translate(bm_cookie, vec=(0, 0, 0.25), verts=bm_cookie.verts)
    
    for f in bm_cookie.faces:
        f.smooth = True
        
    cookie_obj = create_mesh_obj(f"{object_name}_Cookie", bm_cookie)
    cookie_obj.parent = parent_empty
    cookie_obj.data.materials.append(create_color_mat(f"{object_name}_CookieMat", material_color))

    # === Step 3: Create Scattered Chocolate Chips ===
    chip_mat = create_color_mat(f"{object_name}_ChipMat", chip_color)
    for i in range(chip_count):
        bm_chip = bmesh.new()
        bmesh.ops.create_uvsphere(bm_chip, u_segments=16, v_segments=8, radius=0.1)
        for f in bm_chip.faces:
            f.smooth = True
            
        # Random placement across the top of the cookie disc
        r = random.uniform(0.0, 0.95)
        theta = random.uniform(0.0, 2 * math.pi)
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        z = 0.4 + random.uniform(-0.02, 0.05)  # Slightly embedded in cookie top (Z=0.4)
        
        # Randomize shape/scale
        s = random.uniform(0.7, 1.3)
        bmesh.ops.scale(bm_chip, vec=(s, s, s), verts=bm_chip.verts)
        bmesh.ops.translate(bm_chip, vec=(x, y, z), verts=bm_chip.verts)
        
        chip_obj = create_mesh_obj(f"{object_name}_Chip_{i}", bm_chip)
        chip_obj.parent = parent_empty
        chip_obj.data.materials.append(chip_mat)

    # === Step 4: Add Presentation Lighting ===
    light_data = bpy.data.lights.new(name=f"{object_name}_LightData", type='AREA')
    light_data.energy = 800.0
    light_data.color = (1.0, 0.85, 0.7)  # Warm, baked-goods color temperature
    light_data.size = 2.0

    light_obj = bpy.data.objects.new(name=f"{object_name}_AreaLight", object_data=light_data)
    scene.collection.objects.link(light_obj)
    light_obj.parent = parent_empty
    light_obj.location = (2.5, -2.5, 3.5)
    
    # Point light mathematically towards the center of the diorama
    direction = Vector((0.0, 0.0, 0.0)) - light_obj.location
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    return f"Created '{object_name}' (Cookie Diorama) at {location} with {chip_count} chocolate chips and presentation lighting."
