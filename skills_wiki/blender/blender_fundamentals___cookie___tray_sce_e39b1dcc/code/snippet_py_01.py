def create_blender_fundamentals_cookie_scene(
    scene_name: str = "Scene",
    cookie_name: str = "Cookie",
    tray_name: str = "Tray",
    light_name: str = "Area_Light",
    cookie_location: tuple = (0, 0, 0),
    cookie_scale: float = 0.5,
    cookie_color_rgb: tuple = (0.407, 0.231, 0.086),
    chip_color_rgb: tuple = (0.125, 0.047, 0.012),
    tray_color_rgb: tuple = (0.007, 0.007, 0.8),
    num_chocolate_chips: int = 15,
    light_location: tuple = (3.5, -3.5, 3.5),
    light_power: float = 850.0,
    light_temperature: float = 4000.0,
    camera_location: tuple = (7.29, -6.95, 4.97),
    camera_rotation_euler: tuple = (math.radians(55.59), math.radians(0), math.radians(46.52)),
    **kwargs,
) -> str:
    """
    Create a fundamental Blender scene with a cookie on a tray.

    Args:
        scene_name: Name of the target scene.
        cookie_name: Name for the main cookie object.
        tray_name: Name for the tray object.
        light_name: Name for the area light object.
        cookie_location: (x, y, z) world-space position for the cookie.
        cookie_scale: Uniform scale factor for the cookie and chips.
        cookie_color_rgb: (R, G, B) base color for the cookie in 0-1 range.
        chip_color_rgb: (R, G, B) base color for the chocolate chips in 0-1 range.
        tray_color_rgb: (R, G, B) base color for the tray in 0-1 range.
        num_chocolate_chips: Number of chocolate chips to scatter on the cookie.
        light_location: (x, y, z) world-space position for the area light.
        light_power: Power of the area light in Watts.
        light_temperature: Color temperature of the area light in Kelvin.
        camera_location: (x, y, z) world-space position for the camera.
        camera_rotation_euler: (roll, pitch, yaw) rotation for the camera in radians.
        **kwargs: Additional overrides for specific settings.

    Returns:
        Status string, e.g., "Created 'CookieScene' with 1 cookie, 15 chips, 1 tray, 1 light, 1 camera."
    """
    import bpy
    import bmesh
    from mathutils import Vector, Euler
    import math
    import random

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    bpy.context.view_layer.objects.active = None # Clear active selection to avoid unexpected bmesh behavior

    created_objects = []

    # --- 1. Create Cookie Base ---
    bpy.ops.mesh.primitive_cylinder_add(
        radius=cookie_scale * 1.0,
        depth=cookie_scale * 0.2, # Flattened
        location=cookie_location
    )
    cookie_obj = bpy.context.active_object
    cookie_obj.name = cookie_name
    bpy.ops.object.shade_smooth()
    created_objects.append(cookie_obj)

    # --- 2. Create Chocolate Chips ---
    chip_material = bpy.data.materials.new(name="ChocolateChipMaterial")
    chip_material.use_nodes = True
    bsdf_node_chip = chip_material.node_tree.nodes["Principled BSDF"]
    bsdf_node_chip.inputs["Base Color"].default_value = chip_color_rgb + (1.0,)
    bsdf_node_chip.inputs["Roughness"].default_value = kwargs.get("chip_roughness", 0.5)

    for i in range(num_chocolate_chips):
        random_x = random.uniform(-cookie_scale * 0.7, cookie_scale * 0.7)
        random_y = random.uniform(-cookie_scale * 0.7, cookie_scale * 0.7)
        random_z = cookie_location[2] + cookie_scale * 0.1 # Slightly above cookie surface

        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=cookie_scale * 0.1,
            location=(random_x, random_y, random_z)
        )
        chip_obj = bpy.context.active_object
        chip_obj.name = f"ChocolateChip_{i+1}"
        bpy.ops.object.shade_smooth()
        chip_obj.data.materials.append(chip_material)
        created_objects.append(chip_obj)

    # Apply cookie material
    cookie_material = bpy.data.materials.new(name="CookieDoughMaterial")
    cookie_material.use_nodes = True
    bsdf_node_cookie = cookie_material.node_tree.nodes["Principled BSDF"]
    bsdf_node_cookie.inputs["Base Color"].default_value = cookie_color_rgb + (1.0,)
    bsdf_node_cookie.inputs["Roughness"].default_value = kwargs.get("cookie_roughness", 0.8)
    cookie_obj.data.materials.append(cookie_material)


    # --- 3. Create Tray ---
    bpy.ops.mesh.primitive_cube_add(
        size=cookie_scale * 4.0,
        location=(cookie_location[0], cookie_location[1], cookie_location[2] - cookie_scale * 0.15)
    )
    tray_obj = bpy.context.active_object
    tray_obj.name = tray_name
    created_objects.append(tray_obj)

    # Switch to Edit Mode for detailed tray modeling
    bpy.context.view_layer.objects.active = tray_obj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(tray_obj.data)

    # Select the top face (assuming the cube is upright)
    top_face = None
    for face in bm.faces:
        if face.normal.z > 0.9: # Check if normal points upwards
            top_face = face
            break
    
    if top_face:
        bmesh.ops.inset_region(bm, faces=[top_face], thickness=kwargs.get("tray_inset_thickness", cookie_scale * 0.2))
        
        # Extrude the newly created inner face downwards
        # The inset operation adds new faces, the inner one will be the last created face
        inner_face = bm.faces[-1] # Assuming it's the last face after inset
        bmesh.ops.extrude_faces(bm, faces=[inner_face], depth=-kwargs.get("tray_extrude_depth", cookie_scale * 0.1))

    bmesh.update_edit_mesh(tray_obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()

    # Apply tray material
    tray_material = bpy.data.materials.new(name="TrayMaterial")
    tray_material.use_nodes = True
    bsdf_node_tray = tray_material.node_tree.nodes["Principled BSDF"]
    bsdf_node_tray.inputs["Base Color"].default_value = tray_color_rgb + (1.0,)
    bsdf_node_tray.inputs["Roughness"].default_value = kwargs.get("tray_roughness", 0.4)
    tray_obj.data.materials.append(tray_material)

    # --- 4. Lighting Setup ---
    # Delete default light (if it exists)
    default_light = bpy.data.objects.get("Light")
    if default_light:
        bpy.data.objects.remove(default_light, do_unlink=True)

    bpy.ops.object.light_add(type='AREA', location=light_location)
    area_light_obj = bpy.context.active_object
    area_light_obj.name = light_name
    area_light = area_light_obj.data
    area_light.energy = light_power
    area_light.color = (1.0, 1.0, 1.0) # White light, temperature adjusts hue
    area_light.use_nodes = True # Enable nodes for temperature control
    
    # Adjust temperature if using nodes
    if area_light.use_nodes:
        light_node_tree = area_light.node_tree
        emission_node = light_node_tree.nodes.get('Emission')
        if emission_node:
            emission_node.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0) # Reset to white
            
            # Add a Blackbody node to control temperature
            blackbody_node = light_node_tree.nodes.new(type='ShaderNodeBlackbody')
            blackbody_node.location = (-200, 0)
            blackbody_node.inputs['Temperature'].default_value = light_temperature
            
            # Link Blackbody output to Emission Color input
            light_node_tree.links.new(blackbody_node.outputs['Color'], emission_node.inputs['Color'])

    created_objects.append(area_light_obj)


    # --- 5. Camera Setup ---
    camera_obj = bpy.data.objects.get("Camera")
    if camera_obj:
        camera_obj.location = Vector(camera_location)
        camera_obj.rotation_euler = Euler(camera_rotation_euler, 'XYZ')
        # Set render engine to Cycles for better quality as seen in the tutorial
        scene.render.engine = 'CYCLES'
        # Set the device to GPU if available and preferred
        if bpy.context.preferences.addons['cycles'].preferences.compute_device_type == 'CUDA': # Or 'OPTIX', 'HIP', etc.
            bpy.context.preferences.addons['cycles'].preferences.get_devices()
            for d in bpy.context.preferences.addons['cycles'].preferences.devices:
                if d.type == 'CUDA': # Or 'OPTIX', 'HIP', etc.
                    d.use = True
                    break
            scene.cycles.device = 'GPU'
        else:
            scene.cycles.device = 'CPU'
        
        # Set samples for final render
        scene.cycles.samples = kwargs.get("render_samples", 128) # Higher for better quality
        # Set samples for viewport preview
        scene.cycles.preview_samples = kwargs.get("viewport_samples", 32)
        
        # Set film transparency (useful for renders with alpha background)
        # scene.render.film_transparent = False

    return f"Created '{cookie_name}' scene with {len(created_objects)} objects."

