def create_blender_cookie_scene(
    scene_name: str = "Scene",
    cookie_name: str = "Cookie",
    tray_name: str = "Tray",
    light_name: str = "AreaLight",
    camera_name: str = "Camera",
    cookie_location: tuple = (0, 0, 0),
    scene_scale: float = 1.0,
    cookie_color: tuple = (0.53, 0.35, 0.16),  # Brown (eyedropped from video logo)
    chip_color: tuple = (0.2, 0.1, 0.05),     # Dark Brown (eyedropped from video logo)
    tray_color: tuple = (0.0, 0.18, 0.8),      # Blue (eyedropped from video logo)
    light_power: float = 850.0,
    light_temperature: float = 4000.0, # Kelvin for warmer light
    light_location: tuple = (5 * scene_scale, -5 * scene_scale, 8 * scene_scale),
    light_rotation_euler: tuple = (math.radians(45), math.radians(0), math.radians(-45)),
    camera_location: tuple = (7.29 * scene_scale, -6.95 * scene_scale, 4.95 * scene_scale),
    camera_rotation_euler: tuple = (math.radians(55.5), math.radians(0), math.radians(45.5)),
    **kwargs,
) -> str:
    """
    Create a 3D cookie scene with a cookie, chocolate chips, and a tray in Blender.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        cookie_name: Name for the created cookie object.
        tray_name: Name for the created tray object.
        light_name: Name for the created area light.
        camera_name: Name for the camera object.
        cookie_location: (x, y, z) world-space position for the cookie base.
        scene_scale: Uniform scale factor for the entire scene.
        cookie_color: (R, G, B) base color for the cookie.
        chip_color: (R, G, B) base color for the chocolate chips.
        tray_color: (R, G, B) base color for the tray.
        light_power: Power of the area light in Watts.
        light_temperature: Color temperature of the light in Kelvin.
        light_location: (x, y, z) world-space position for the area light.
        light_rotation_euler: (x, y, z) Euler rotation for the area light in radians.
        camera_location: (x, y, z) world-space position for the camera.
        camera_rotation_euler: (x, y, z) Euler rotation for the camera in radians.
        **kwargs: Additional overrides (e.g., num_chips for number of chips).

    Returns:
        Status string, e.g., "Created 'CookieScene' with N objects"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math
    import random

    # --- Scene Settings ---
    # Ensure Cycles renderer and GPU compute (if available)
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU' # Attempt to use GPU

    # Render output properties
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.film_transparent = False

    # Deselect all objects to start fresh
    bpy.ops.object.select_all(action='DESELECT')

    # --- Materials ---
    materials = {}

    # Cookie Material
    cookie_mat = bpy.data.materials.new(name=f"{cookie_name}Mat")
    cookie_mat.use_nodes = True
    bsdf_cookie = cookie_mat.node_tree.nodes["Principled BSDF"]
    bsdf_cookie.inputs["Base Color"].default_value = (*cookie_color, 1.0)
    bsdf_cookie.inputs["Roughness"].default_value = 0.7 
    materials["cookie"] = cookie_mat

    # Chocolate Chip Material
    chip_mat = bpy.data.materials.new(name=f"{cookie_name}ChipMat")
    chip_mat.use_nodes = True
    bsdf_chip = chip_mat.node_tree.nodes["Principled BSDF"]
    bsdf_chip.inputs["Base Color"].default_value = (*chip_color, 1.0)
    bsdf_chip.inputs["Roughness"].default_value = 0.5
    materials["chip"] = chip_mat

    # Tray Material
    tray_mat = bpy.data.materials.new(name=f"{tray_name}Mat")
    tray_mat.use_nodes = True
    bsdf_tray = tray_mat.node_tree.nodes["Principled BSDF"]
    bsdf_tray.inputs["Base Color"].default_value = (*tray_color, 1.0)
    bsdf_tray.inputs["Metallic"].default_value = 0.2
    bsdf_tray.inputs["Roughness"].default_value = 0.3
    materials["tray"] = tray_mat

    # --- Cookie Base ---
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=64, radius=1.0 * scene_scale, depth=0.2 * scene_scale,
        location=cookie_location
    )
    cookie_obj = bpy.context.object
    cookie_obj.name = cookie_name
    bpy.ops.object.shade_smooth()
    if cookie_obj.data.materials:
        cookie_obj.data.materials[0] = materials["cookie"]
    else:
        cookie_obj.data.materials.append(materials["cookie"])

    # --- Chocolate Chips ---
    num_chips = kwargs.get("num_chips", 15)
    chip_base_radius = 0.05 * scene_scale
    chip_z_offset_base = cookie_location[2] + (0.1 * scene_scale) # Base Z + half cookie height

    for i in range(num_chips):
        # Randomize position within cookie radius
        rand_radius_factor = random.uniform(0.3, 0.9)
        rand_angle = random.uniform(0, 2 * math.pi)
        
        chip_x = cookie_location[0] + (cookie_obj.dimensions.x / 2) * rand_radius_factor * math.cos(rand_angle)
        chip_y = cookie_location[1] + (cookie_obj.dimensions.y / 2) * rand_radius_factor * math.sin(rand_angle)
        chip_z = chip_z_offset_base + random.uniform(-0.02 * scene_scale, 0.02 * scene_scale) # Slight z-variation

        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=chip_base_radius * random.uniform(0.8, 1.2), # Randomize chip size slightly
            location=(chip_x, chip_y, chip_z)
        )
        chip_obj_single = bpy.context.object
        chip_obj_single.name = f"{cookie_name}Chip_{i:02d}"
        bpy.ops.object.shade_smooth()
        if chip_obj_single.data.materials:
            chip_obj_single.data.materials[0] = materials["chip"]
        else:
            chip_obj_single.data.materials.append(materials["chip"])

    # --- Tray ---
    # Create base cube for the tray
    tray_base_size = 3.0 * scene_scale
    tray_height = 0.1 * scene_scale
    bpy.ops.mesh.primitive_cube_add(
        size=tray_base_size,
        location=(cookie_location[0], cookie_location[1], cookie_location[2] - tray_height/2 - (cookie_obj.dimensions.z / 2)) # Below cookie
    )
    tray_obj = bpy.context.object
    tray_obj.name = tray_name
    
    # Apply initial scale for a thin tray
    tray_obj.scale = (1.0, 1.0, tray_height / tray_base_size)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Edit Mode for tray modifications
    bpy.context.view_layer.objects.active = tray_obj
    bpy.ops.object.mode_set(mode='EDIT')
    
    bm = bmesh.from_edit_mesh(tray_obj.data)
    bm.faces.ensure_lookup_table()
    
    # Select the top face (assuming the cube is upright)
    top_face = None
    for face in bm.faces:
        if abs(face.normal.z - 1.0) < 0.001: 
            top_face = face
            break
            
    if top_face:
        # Inset the top face to create the inner part of the tray
        bmesh.ops.inset_faces(bm, faces=[top_face], thickness=0.1 * scene_scale, depth=0.0)
        
        # After inset, the newly created inner face is usually selected.
        # Extrude this inner face downwards to create the tray's depth
        bpy.ops.mesh.extrude_region_move(
            MESH_OT_extrude_region={"type":'NORMAL'}, 
            TRANSFORM_OT_translate={"value":(0, 0, -0.05 * scene_scale)} # Extrude down by a small amount
        )

    bmesh.update_edit_mesh(tray_obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()
    
    if tray_obj.data.materials:
        tray_obj.data.materials[0] = materials["tray"]
    else:
        tray_obj.data.materials.append(materials["tray"])

    # --- Lighting ---
    # The video deletes the default light; for additive design, we'll just add a new one.
    bpy.ops.object.light_add(type='AREA', location=light_location)
    area_light = bpy.context.object
    area_light.name = light_name
    area_light.data.energy = light_power
    area_light.data.use_nodes = True
    
    # Access the Principled BSDF node in the light's node tree (for Area light, it's Emission)
    emission_node = area_light.data.node_tree.nodes.get("Emission")
    if emission_node:
        emission_node.inputs["Strength"].default_value = light_power
        # For temperature, a Blackbody node is usually connected to the color input.
        # For simple color, set it directly or use RGB approximating Kelvin.
        # Direct temperature setting is available in the UI but typically requires a node setup in Cycles.
        # Approximating 4000K: a warm white/yellowish color
        emission_node.inputs["Color"].default_value = (1.0, 0.85, 0.7, 1.0) # Approx warm white
        
    area_light.rotation_euler = light_rotation_euler
    area_light.data.size = 1.0 * scene_scale # Square light size

    # --- Camera ---
    camera_obj = bpy.data.objects.get(camera_name)
    if not camera_obj:
        bpy.ops.object.camera_add(location=camera_location)
        camera_obj = bpy.context.object
        camera_obj.name = camera_name
    
    camera_obj.location = Vector(camera_location)
    camera_obj.rotation_euler = camera_rotation_euler
    
    # Make sure this camera is the active scene camera
    bpy.context.scene.camera = camera_obj
    
    # Hide the sidebar for cleaner viewport (similar to N key)
    # This is a UI preference, not object creation.
    # bpy.ops.screen.region_toggle(region_type='UI')

    return f"Created cookie scene with '{cookie_name}' and '{tray_name}' at {cookie_location} with {num_chips} chips."

