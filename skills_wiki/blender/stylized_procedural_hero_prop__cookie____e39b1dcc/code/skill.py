def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedCookieProp",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.54, 0.34, 0.16),  # Cookie dough color
    **kwargs,
) -> str:
    """
    Create a Stylized Cookie and Tray mini-diorama in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects and parent.
        location: (x, y, z) world-space position for the diorama.
        scale: Uniform scale factor for the entire group.
        material_color: (R, G, B) base color for the cookie dough.
        **kwargs: 
            tray_color (tuple): (R, G, B) for the plastic tray.
            chip_color (tuple): (R, G, B) for the chocolate chips.
            num_chips (int): Number of chips to scatter.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector, Euler

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # Configurable parameters
    tray_color = kwargs.get("tray_color", (0.05, 0.15, 0.6))
    chip_color = kwargs.get("chip_color", (0.04, 0.02, 0.01))
    num_chips = kwargs.get("num_chips", 15)

    # === Step 1: Material Setup ===
    def create_material(name, color, roughness):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*color, 1.0)
            bsdf.inputs["Roughness"].default_value = roughness
        return mat

    mat_cookie = create_material(f"{object_name}_CookieMat", material_color, 0.8)
    mat_chip = create_material(f"{object_name}_ChipMat", chip_color, 0.4)
    mat_tray = create_material(f"{object_name}_TrayMat", tray_color, 0.3)

    # === Step 2: Master Parent Setup ===
    master = bpy.data.objects.new(object_name, None)
    master.empty_display_size = 2.0
    master.empty_display_type = 'PLAIN_AXES'
    scene.collection.objects.link(master)
    master.location = Vector(location)
    master.scale = (scale, scale, scale)

    # === Step 3: Tray Generation (BMesh) ===
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    tray = bpy.context.active_object
    tray.name = f"{object_name}_Tray"
    
    # Scale tray
    tray.scale = (2.5, 2.5, 0.15)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    tray.data.materials.append(mat_tray)
    
    # BMesh operations for inset and extrusion
    bm = bmesh.new()
    bm.from_mesh(tray.data)
    
    # Identify the top face based on the median Z axis
    top_face = max(bm.faces, key=lambda f: f.calc_center_median().z)
    
    # Inset face to create the rim boundary
    ret = bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.15, depth=0.0)
    inset_faces = ret['faces']
    
    # Extrude inner area downwards to create the bowl/tray depth
    ret = bmesh.ops.extrude_face_region(bm, geom=inset_faces)
    extruded_faces = [elem for elem in ret['geom'] if isinstance(elem, bmesh.types.BMFace)]
    bmesh.ops.translate(bm, vec=Vector((0, 0, -0.05)), verts=list(set(v for f in extruded_faces for v in f.verts)))
    
    bm.to_mesh(tray.data)
    bm.free()
    
    # Parent tray to master (maintains local zero offset)
    tray.parent = master

    # === Step 4: Cookie Base Generation ===
    cookie_z_offset = 0.175  # Tray is 0.15 thick (+0.075 to top), cookie is 0.2 thick (+0.1 to center)
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.8, depth=0.2, location=(0, 0, cookie_z_offset))
    cookie = bpy.context.active_object
    cookie.name = f"{object_name}_Base"
    cookie.data.materials.append(mat_cookie)
    
    for poly in cookie.data.polygons:
        poly.use_smooth = True
        
    cookie.parent = master

    # === Step 5: Chocolate Chip Scattering ===
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=16, radius=0.06, location=(0, 0, 0))
    chip_master = bpy.context.active_object
    chip_master.data.materials.append(mat_chip)
    for poly in chip_master.data.polygons:
        poly.use_smooth = True

    for i in range(num_chips):
        chip = chip_master.copy()
        chip.data = chip_master.data.copy() # Independent mesh copy
        scene.collection.objects.link(chip)
        chip.name = f"{object_name}_Chip_{i:02d}"
        chip.parent = cookie
        
        # Calculate random polar coordinates within cookie bounds (radius = 0.8)
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(0.0, 0.65) # Kept slightly inward from the edge
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        z = 0.1  # Local Z relative to cookie center (surface level)
        
        chip.location = Vector((x, y, z))
        chip.rotation_euler = Euler((random.uniform(0, 3.14), random.uniform(0, 3.14), random.uniform(0, 3.14)))
        
        # Slight randomized scaling and flattening
        sf = random.uniform(0.7, 1.3)
        chip.scale = (sf, sf, sf * random.uniform(0.4, 0.8))

    # Clean up the hidden master chip instance
    bpy.data.objects.remove(chip_master, do_unlink=True)

    # === Step 6: Contextual Lighting ===
    light_data = bpy.data.lights.new(name=f"{object_name}_LightData", type='AREA')
    light_data.energy = 800.0
    light_data.color = (1.0, 0.9, 0.7)  # Warm 4000K bake lighting
    light_data.size = 2.0
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_AreaLight", object_data=light_data)
    scene.collection.objects.link(light_obj)
    light_obj.parent = master
    light_obj.location = Vector((1.5, -1.5, 2.0))
    
    # Aim light straight at the cookie
    direction = -light_obj.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    light_obj.rotation_euler = rot_quat.to_euler()

    return f"Created '{object_name}' (Tray, Cookie, and {num_chips} scattered chips) at {location}."
