def create_object(
    scene_name: str = "Scene",
    object_name: str = "Stylized_Cookie_Prop",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.45, 0.2), # Cookie Dough Color
    **kwargs,
) -> str:
    """
    Create a Stylized Chocolate Chip Cookie on a tray with overhead area lighting.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the root controller object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the cookie dough in 0-1 range.
        **kwargs: 
            chip_color (tuple): (R, G, B) for the chocolate chips.
            tray_color (tuple): (R, G, B) for the tray.
            num_chips (int): Number of chocolate chips to scatter.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector, Euler

    # Safely get scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Extract optional kwargs
    chip_color = kwargs.get("chip_color", (0.12, 0.06, 0.03))
    tray_color = kwargs.get("tray_color", (0.1, 0.3, 0.8))
    num_chips = kwargs.get("num_chips", 12)

    # Helper function to create materials
    def create_simple_material(mat_name, color, roughness=0.5):
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Blender 4.0+ uses 'Base Color', earlier versions might differ slightly but this handles standard API
            if 'Base Color' in bsdf.inputs:
                bsdf.inputs['Base Color'].default_value = (*color, 1.0)
            if 'Roughness' in bsdf.inputs:
                bsdf.inputs['Roughness'].default_value = roughness
        return mat

    # Create Materials
    mat_cookie = create_simple_material(f"{object_name}_Mat_Dough", material_color, roughness=0.8)
    mat_chip = create_simple_material(f"{object_name}_Mat_Chip", chip_color, roughness=0.4)
    mat_tray = create_simple_material(f"{object_name}_Mat_Tray", tray_color, roughness=0.5)

    # === Create Root Controller ===
    root_obj = bpy.data.objects.new(object_name, None)
    root_obj.empty_display_size = 2.0
    root_obj.empty_display_type = 'ARROWS'
    scene.collection.objects.link(root_obj)

    # === Step 1: Create Tray ===
    mesh_tray = bpy.data.meshes.new(f"{object_name}_Tray_Mesh")
    obj_tray = bpy.data.objects.new(f"{object_name}_Tray", mesh_tray)
    scene.collection.objects.link(obj_tray)
    obj_tray.parent = root_obj
    obj_tray.data.materials.append(mat_tray)

    bm_tray = bmesh.new()
    bmesh.ops.create_cube(bm_tray, size=2.0)
    # Flatten into a plate
    bmesh.ops.scale(bm_tray, vec=(1.5, 1.5, 0.1), verts=bm_tray.verts)
    
    # Identify top face to inset and extrude
    top_faces = [f for f in bm_tray.faces if f.normal.z > 0.5]
    if top_faces:
        inset_result = bmesh.ops.inset_region(bm_tray, faces=top_faces, thickness=0.1)
        # Drop the newly inset inner faces down to create the tray lip
        inner_faces = [f for f in bm_tray.faces if f.normal.z > 0.5 and f.calc_area() < 4.0]
        if inner_faces:
            bmesh.ops.translate(bm_tray, vec=(0, 0, -0.05), verts=inner_faces[0].verts)

    bm_tray.to_mesh(mesh_tray)
    bm_tray.free()

    # === Step 2: Create Cookie Base ===
    mesh_cookie = bpy.data.meshes.new(f"{object_name}_Cookie_Mesh")
    obj_cookie = bpy.data.objects.new(f"{object_name}_Cookie", mesh_cookie)
    scene.collection.objects.link(obj_cookie)
    obj_cookie.parent = root_obj
    obj_cookie.data.materials.append(mat_cookie)

    bm_cookie = bmesh.new()
    # Cylinder radius=0.8, depth=0.15
    bmesh.ops.create_cone(bm_cookie, cap_ends=True, cap_tris=False, segments=32, radius1=0.8, radius2=0.8, depth=0.15)
    
    # Apply Shade Smooth
    for f in bm_cookie.faces:
        f.smooth = True
        
    # Translate up so it rests on the tray interior
    # Tray internal floor is roughly at Z=0.05. Cookie half-depth is 0.075. Center = 0.125
    bmesh.ops.translate(bm_cookie, vec=(0, 0, 0.125), verts=bm_cookie.verts)
    
    bm_cookie.to_mesh(mesh_cookie)
    bm_cookie.free()

    # === Step 3: Create & Scatter Chocolate Chips ===
    # Randomly scatter chips on top of the cookie
    for i in range(num_chips):
        mesh_chip = bpy.data.meshes.new(f"{object_name}_Chip_{i}_Mesh")
        obj_chip = bpy.data.objects.new(f"{object_name}_Chip_{i}", mesh_chip)
        scene.collection.objects.link(obj_chip)
        obj_chip.parent = obj_cookie
        obj_chip.data.materials.append(mat_chip)

        bm_chip = bmesh.new()
        bmesh.ops.create_uvsphere(bm_chip, u_segments=16, v_segments=8, radius=0.08)
        
        # Apply Shade Smooth
        for f in bm_chip.faces:
            f.smooth = True

        # Determine random polar placement on the cookie surface
        angle = random.uniform(0, 2 * math.pi)
        radius_offset = random.uniform(0.0, 0.65) # Stay within cookie bounds
        x = radius_offset * math.cos(angle)
        y = radius_offset * math.sin(angle)
        z = 0.125 + 0.075 # Z height sitting just embedded in the top surface

        # Apply transformations to individual chip mesh
        # Random Z-rotation and slight wobble
        rot = Euler((random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2), random.uniform(0, math.pi * 2)))
        bmesh.ops.rotate(bm_chip, matrix=rot.to_matrix(), verts=bm_chip.verts)
        
        # Flatten chip slightly to look more realistic
        bmesh.ops.scale(bm_chip, vec=(1.0, 1.0, 0.8), verts=bm_chip.verts)
        
        # Move into position
        bmesh.ops.translate(bm_chip, vec=(x, y, z), verts=bm_chip.verts)
        
        bm_chip.to_mesh(mesh_chip)
        bm_chip.free()

    # === Step 4: Add Area Light ===
    light_data = bpy.data.lights.new(name=f"{object_name}_AreaLight", type='AREA')
    light_data.energy = 800.0 # High power
    light_data.color = (1.0, 0.85, 0.7) # Warm 4000k light
    light_data.size = 2.0
    
    obj_light = bpy.data.objects.new(name=f"{object_name}_LightObj", object_data=light_data)
    scene.collection.objects.link(obj_light)
    obj_light.parent = root_obj
    
    # Position light overhead and to the side, pointing at the center
    obj_light.location = Vector((1.5, -1.5, 2.5))
    target_dir = Vector((0, 0, 0)) - obj_light.location
    obj_light.rotation_euler = target_dir.to_track_quat('-Z', 'Y').to_euler()

    # === Step 5: Final Transform Application ===
    root_obj.location = Vector(location)
    root_obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' (Cookie, {num_chips} Chips, Tray, and Light) at {location} scaled by {scale}."
