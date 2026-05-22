def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedCookieScene",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.45, 0.2),  # Cookie dough color
    **kwargs,
) -> str:
    """
    Create a stylized Chocolate Chip Cookie sitting on a square tray in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the hierarchy.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the entire assembly.
        material_color: (R, G, B) base color of the cookie dough.
        **kwargs: 
            num_chips (int): Amount of chocolate chips to scatter (default: 15)
            tray_color (tuple): (R, G, B) color for the tray (default: blue)
            chip_color (tuple): (R, G, B) color for the chocolate chips
            add_light (bool): Whether to spawn a warm area light pointing at the cookie

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector

    # Fetch or set target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Parent Hierarchy ===
    parent_empty = bpy.data.objects.new(object_name, None)
    scene.collection.objects.link(parent_empty)
    parent_empty.location = Vector(location)
    parent_empty.scale = (scale, scale, scale)

    # === Step 2: Build Materials ===
    def create_material(name, color, roughness):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*color, 1.0)
            bsdf.inputs["Roughness"].default_value = roughness
        return mat

    mat_cookie = create_material(f"{object_name}_CookieMat", material_color, 0.8)
    
    tray_color = kwargs.get("tray_color", (0.1, 0.3, 0.8))
    mat_tray = create_material(f"{object_name}_TrayMat", tray_color, 0.4)
    
    chip_color = kwargs.get("chip_color", (0.1, 0.05, 0.02))
    mat_chip = create_material(f"{object_name}_ChipMat", chip_color, 0.6)

    # === Step 3: Create the Tray ===
    mesh_tray = bpy.data.meshes.new(f"{object_name}_Tray")
    obj_tray = bpy.data.objects.new(f"{object_name}_Tray", mesh_tray)
    scene.collection.objects.link(obj_tray)
    obj_tray.parent = parent_empty
    obj_tray.data.materials.append(mat_tray)

    bm_tray = bmesh.new()
    bmesh.ops.create_cube(bm_tray, size=1.0)
    
    # Scale wide and flat, shift origin to bottom
    bmesh.ops.scale(bm_tray, vec=Vector((3.0, 3.0, 0.1)), verts=bm_tray.verts)
    bmesh.ops.translate(bm_tray, vec=Vector((0, 0, 0.05)), verts=bm_tray.verts)
    
    bm_tray.faces.ensure_lookup_table()
    top_face = max(bm_tray.faces, key=lambda f: f.calc_center_median().z)
    
    # Inset face to create the rim
    bmesh.ops.inset_region(bm_tray, faces=[top_face], thickness=0.1)
    
    # Extrude inset face down to create the tray bed
    extrude_res = bmesh.ops.extrude_face_region(bm_tray, geom=[top_face])
    extruded_verts = [elem for elem in extrude_res['geom'] if isinstance(elem, bmesh.types.BMVert)]
    bmesh.ops.translate(bm_tray, vec=Vector((0, 0, -0.04)), verts=extruded_verts)

    bm_tray.to_mesh(mesh_tray)
    bm_tray.free()

    # === Step 4: Create the Cookie Base ===
    mesh_cookie = bpy.data.meshes.new(f"{object_name}_Cookie")
    obj_cookie = bpy.data.objects.new(f"{object_name}_Cookie", mesh_cookie)
    scene.collection.objects.link(obj_cookie)
    obj_cookie.parent = parent_empty
    obj_cookie.location = Vector((0, 0, 0.06))  # Sit exactly on the inside floor of the tray
    obj_cookie.data.materials.append(mat_cookie)

    bm_cookie = bmesh.new()
    bmesh.ops.create_cone(bm_cookie, cap_ends=True, cap_tris=False, segments=32, radius1=1.0, radius2=1.0, depth=0.2)
    bmesh.ops.translate(bm_cookie, vec=Vector((0, 0, 0.1)), verts=bm_cookie.verts)
    
    for f in bm_cookie.faces:
        f.smooth = True
        
    bm_cookie.to_mesh(mesh_cookie)
    bm_cookie.free()

    # === Step 5: Scatter Chocolate Chips ===
    num_chips = kwargs.get("num_chips", 15)
    
    # Prepare base chip mesh in bmesh
    mesh_chip = bpy.data.meshes.new(f"{object_name}_Chip_Data")
    bm_chip = bmesh.new()
    bmesh.ops.create_icosphere(bm_chip, subdivisions=2, radius=0.08)
    bmesh.ops.scale(bm_chip, vec=Vector((1.0, 1.0, 0.6)), verts=bm_chip.verts) # Squash it
    for f in bm_chip.faces:
        f.smooth = True
    bm_chip.to_mesh(mesh_chip)
    bm_chip.free()

    chip_objects_created = 0
    for i in range(num_chips):
        obj_chip = bpy.data.objects.new(f"{object_name}_Chip_{i}", mesh_chip)
        scene.collection.objects.link(obj_chip)
        obj_chip.parent = obj_cookie
        obj_chip.data.materials.append(mat_chip)
        
        # Uniform circular distribution using square root curve
        r = 0.85 * math.sqrt(random.random())
        theta = random.uniform(0.0, 2.0 * math.pi)
        
        # Coordinates local to cookie
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        z = 0.2  # Placed directly intersecting the top face of the cookie base
        
        obj_chip.location = Vector((x, y, z))
        
        # Add random orientation and slight size variations
        obj_chip.rotation_euler = (
            random.uniform(-0.5, 0.5),
            random.uniform(-0.5, 0.5),
            random.uniform(0.0, 2.0 * math.pi)
        )
        s = random.uniform(0.7, 1.3)
        obj_chip.scale = (s, s, s)
        chip_objects_created += 1

    # === Step 6: Add Lighting ===
    if kwargs.get("add_light", True):
        light_data = bpy.data.lights.new(name=f"{object_name}_WarmLight", type='AREA')
        light_data.energy = 850.0
        light_data.color = (1.0, 0.85, 0.7) # Warm 4000K approx
        light_data.size = 2.0
        
        light_obj = bpy.data.objects.new(name=f"{object_name}_WarmLight", object_data=light_data)
        scene.collection.objects.link(light_obj)
        light_obj.parent = parent_empty
        light_obj.location = Vector((2.0, -2.0, 3.0))
        
        # Track light to the center of the scene/tray
        direction = -light_obj.location
        rot_quat = direction.to_track_quat('-Z', 'Y')
        light_obj.rotation_euler = rot_quat.to_euler()

    return f"Created '{object_name}' at {location} with 1 Tray, 1 Cookie, and {chip_objects_created} Chips."
