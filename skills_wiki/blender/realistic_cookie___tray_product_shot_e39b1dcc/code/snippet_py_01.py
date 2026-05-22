def create_cookie_tray_product_shot(
    scene_name: str = "Scene",
    base_object_name: str = "Cookie",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    cookie_color_rgb: tuple = (0.46, 0.32, 0.18),  # RGB for cookie dough
    chip_color_rgb: tuple = (0.11, 0.06, 0.04),    # RGB for chocolate chips
    tray_color_rgb: tuple = (0.02, 0.18, 0.56),    # RGB for blue tray
    tray_inner_height: float = 0.02,
    num_chocolate_chips: int = 15,
    light_power: float = 850.0,
    light_temperature: float = 4000.0, # Kelvin
    camera_location: tuple = (7.2, -6.6, 6.0),
    camera_rotation_euler: tuple = (1.1, 0.0, 0.8), # Radians for pitch, yaw, roll
    **kwargs,
) -> str:
    """
    Create a 3D chocolate chip cookie on a tray with basic lighting in Blender.

    Args:
        scene_name: Name of the target scene.
        base_object_name: Base name for the created cookie object.
        location: (x, y, z) world-space position for the cookie and tray.
        scale: Uniform scale factor for the entire setup.
        cookie_color_rgb: (R, G, B) base color for the cookie dough (0-1 range).
        chip_color_rgb: (R, G, B) base color for the chocolate chips (0-1 range).
        tray_color_rgb: (R, G, B) base color for the tray (0-1 range).
        tray_inner_height: How much to extrude the inner part of the tray down.
        num_chocolate_chips: Number of chocolate chips to scatter on the cookie.
        light_power: Power of the area light (in Watts).
        light_temperature: Color temperature of the area light (in Kelvin).
        camera_location: (x, y, z) world-space position for the camera.
        camera_rotation_euler: (pitch, yaw, roll) rotation for the camera in radians.
        **kwargs: Additional overrides (e.g., cookie_segments, tray_size).

    Returns:
        Status string, e.g., "Created 'Cookie' setup at (0, 0, 0)"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import random
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 0. Setup: Ensure GPU compute for Cycles if available ---
    try:
        bpy.context.scene.render.engine = 'CYCLES'
        prefs = bpy.context.preferences
        cycles_prefs = prefs.addons['cycles'].preferences
        if 'CUDA' in cycles_prefs.get_devices():
            cycles_prefs.compute_device_type = 'CUDA'
            for device in cycles_prefs.devices:
                device.use = device.type == 'CUDA'
        elif 'OPTIX' in cycles_prefs.get_devices():
            cycles_prefs.compute_device_type = 'OPTIX'
            for device in cycles_prefs.devices:
                device.use = device.type == 'OPTIX'
        # Default to CPU if no GPU option is found or specific conditions aren't met
        else:
            cycles_prefs.compute_device_type = 'CPU'
            for device in cycles_prefs.devices:
                device.use = device.type == 'CPU'

        # Set default render samples for final render
        bpy.context.scene.cycles.samples = 128
        bpy.context.scene.cycles.max_bounces = 8
        bpy.context.scene.cycles.diffuse_bounces = 4
        bpy.context.scene.cycles.glossy_bounces = 4
        bpy.context.scene.cycles.transmission_bounces = 8

    except Exception as e:
        print(f"Failed to set Cycles GPU preferences: {e}. Falling back to CPU/default.")
        bpy.context.scene.render.engine = 'BLENDER_EEVEE' # EEVEE is faster for non-GPU cycles setup

    # --- 1. Materials ---
    # Cookie Dough Material
    cookie_mat = bpy.data.materials.new(name=f"{base_object_name}_DoughMat")
    cookie_mat.use_nodes = True
    bsdf_node = cookie_mat.node_tree.nodes["Principled BSDF"]
    bsdf_node.inputs["Base Color"].default_value = (*cookie_color_rgb, 1.0)
    bsdf_node.inputs["Metallic"].default_value = 0.0
    bsdf_node.inputs["Roughness"].default_value = 0.8

    # Chocolate Chip Material
    chip_mat = bpy.data.materials.new(name=f"{base_object_name}_ChipMat")
    chip_mat.use_nodes = True
    bsdf_node = chip_mat.node_tree.nodes["Principled BSDF"]
    bsdf_node.inputs["Base Color"].default_value = (*chip_color_rgb, 1.0)
    bsdf_node.inputs["Metallic"].default_value = 0.0
    bsdf_node.inputs["Roughness"].default_value = 0.3

    # Tray Material
    tray_mat = bpy.data.materials.new(name=f"{base_object_name}_TrayMat")
    tray_mat.use_nodes = True
    bsdf_node = tray_mat.node_tree.nodes["Principled BSDF"]
    bsdf_node.inputs["Base Color"].default_value = (*tray_color_rgb, 1.0)
    bsdf_node.inputs["Metallic"].default_value = 0.0
    bsdf_node.inputs["Roughness"].default_value = 0.4


    # --- 2. Cookie Object ---
    cookie_radius = 1.0 * scale
    cookie_depth = 0.15 * scale
    cookie_segments = kwargs.get('cookie_segments', 64)

    bpy.ops.mesh.primitive_cylinder_add(
        radius=cookie_radius,
        depth=cookie_depth,
        vertices=cookie_segments,
        location=location
    )
    cookie_obj = bpy.context.active_object
    cookie_obj.name = base_object_name
    bpy.ops.object.shade_smooth()
    cookie_obj.data.materials.append(cookie_mat)

    # --- 3. Chocolate Chips ---
    chips = []
    chip_scale_factor = 0.08 * scale
    for i in range(num_chocolate_chips):
        chip_x = random.uniform(-0.8 * cookie_radius, 0.8 * cookie_radius)
        chip_y = random.uniform(-0.8 * cookie_radius, 0.8 * cookie_radius)
        chip_z = cookie_obj.location.z + (cookie_depth / 2) + (chip_scale_factor / 2)
        
        # Ensure chips are mostly on the cookie surface but allow slight randomness
        # Avoid placing chips outside the cookie radius
        if (chip_x**2 + chip_y**2)**0.5 > (cookie_radius - chip_scale_factor/2):
            # Recalculate if outside main cookie area
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, cookie_radius - chip_scale_factor/2)
            chip_x = distance * math.cos(angle)
            chip_y = distance * math.sin(angle)

        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=chip_scale_factor,
            location=(location[0] + chip_x, location[1] + chip_y, location[2] + cookie_depth / 2 + chip_scale_factor / 4),
            segments=16,
            ring_count=8
        )
        chip_obj = bpy.context.active_object
        chip_obj.name = f"{base_object_name}_Chip_{i:03d}"
        bpy.ops.object.shade_smooth()
        chip_obj.data.materials.append(chip_mat)
        chips.append(chip_obj)

    # --- 4. Tray Object ---
    tray_size_x = 3.0 * scale
    tray_size_y = 3.0 * scale
    tray_depth = 0.1 * scale
    tray_inset_amount = 0.1 * scale

    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(location[0], location[1], location[2] - cookie_depth/2 - tray_depth/2)
    )
    tray_obj = bpy.context.active_object
    tray_obj.name = f"{base_object_name}_Tray"
    tray_obj.scale = (tray_size_x, tray_size_y, tray_depth) # Scale to desired dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True) # Apply scale for correct inset

    bpy.ops.object.shade_smooth()
    tray_obj.data.materials.append(tray_mat)

    # Go into edit mode to create the tray ridge
    bpy.context.view_layer.objects.active = tray_obj
    bpy.ops.object.mode_set(mode='EDIT')
    
    bm = bmesh.from_edit_mesh(tray_obj.data)
    # Select only the top face
    top_face = None
    for face in bm.faces:
        face.select = False
        if all(v.co.z > tray_obj.location.z + (tray_depth * scale / 2) - 0.001 for v in face.verts): # Check if face is top
            face.select = True
            top_face = face
            break
            
    if top_face:
        # Inset the top face
        bpy.ops.mesh.inset.faces(thickness=tray_inset_amount, depth=0)
        
        # Extrude the new inner face downwards
        # Select the newly created inner face (it's usually the second one after inset)
        # Re-evaluate top_face after inset as bmesh might reorder or add geometry
        bmesh.update_edit_mesh(tray_obj.data) # Update mesh to get new topology
        bm = bmesh.from_edit_mesh(tray_obj.data)
        
        inner_faces = [f for f in bm.faces if f.select]
        if len(inner_faces) == 1:
            inner_face = inner_faces[0]
            # Extrude the inner face downwards
            # Use bmesh.ops.extrude_face_region instead of bpy.ops for more control
            # and to keep bmesh data valid
            extrude_vector = Vector((0, 0, -tray_inner_height * scale))
            geom = bmesh.ops.extrude_face_region(bm, geom=[inner_face])
            bmesh.ops.translate(bm, verts=[v for v in geom["geom"] if isinstance(v, bmesh.types.BMVert)], vec=extrude_vector)

    bmesh.update_edit_mesh(tray_obj.data)
    bm.free()
    bpy.ops.object.mode_set(mode='OBJECT')

    # --- 5. Lighting ---
    bpy.ops.object.light_add(
        type='AREA',
        radius=1.0 * scale,
        location=(location[0] + 2.0 * scale, location[1] - 2.0 * scale, location[2] + 3.0 * scale)
    )
    area_light = bpy.context.active_object
    area_light.name = f"{base_object_name}_AreaLight"
    area_light.data.energy = light_power
    area_light.data.color = (1.0, 1.0, 1.0) # White light, temperature modifies perception
    
    # Set color temperature
    area_light.data.use_nodes = True
    nodes = area_light.data.node_tree.nodes
    temp_node = nodes.new(type='ShaderNodeBsdfHair') # Using Hair BSDF for a generic node for now
    
    # Actually, Blender's Area Light has a direct color temperature input under 'Light'
    # No need for separate node setup for temperature if using the direct input
    area_light.data.use_custom_distance = True # Ensure temperature is active
    area_light.data.temperature = light_temperature
    
    # Rotate light to point towards the cookie
    area_light.rotation_euler = (math.radians(50), math.radians(-30), math.radians(10))

    # --- 6. Camera Framing ---
    camera_obj = bpy.data.objects['Camera']
    camera_obj.location = Vector(camera_location)
    camera_obj.rotation_euler = (camera_rotation_euler[0], camera_rotation_euler[1], camera_rotation_euler[2])

    # To ensure the rendered view matches the viewport, set the camera to lock to view
    # (This is more for interactive use during scene setup than for the final render function itself)
    # The video shows locking it for framing, so it's good to demonstrate this.
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces.active
            if space.type == 'VIEW_3D':
                space.region_3d.lock_camera_to_view = True
                bpy.ops.view3d.view_camera() # Go to camera view

    # --- Finalize ---
    # Put all created objects into a new collection for organization
    new_collection = bpy.data.collections.new(f"{base_object_name}_Collection")
    scene.collection.children.link(new_collection)

    new_collection.objects.link(cookie_obj)
    for chip_obj in chips:
        new_collection.objects.link(chip_obj)
    new_collection.objects.link(tray_obj)
    new_collection.objects.link(area_light)
    new_collection.objects.link(camera_obj) # Link camera to the collection

    # Unlink from default scene collection if linked there automatically
    for obj in [cookie_obj, tray_obj, area_light, camera_obj] + chips:
        if obj.name in scene.collection.objects:
            scene.collection.objects.unlink(obj)

    return f"Created '{base_object_name}' setup at {location} with {1 + num_chocolate_chips + 1 + 1} objects" # Cookie, chips, tray, light, camera


