def create_cookie_scene(
    scene_name: str = "Scene",
    base_object_name: str = "Cookie",
    tray_object_name: str = "Tray",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    cookie_color: tuple = (0.482, 0.231, 0.046, 1.0),  # RGB A values
    chip_color: tuple = (0.180, 0.098, 0.035, 1.0),
    tray_color: tuple = (0.019, 0.066, 0.449, 1.0),
    light_power: float = 850.0,
    light_temperature: float = 4000.0,
    **kwargs,
) -> str:
    """
    Create a basic 3D cookie and tray scene with materials and lighting in Blender.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        base_object_name: Name for the created cookie object.
        tray_object_name: Name for the created tray object.
        location: (x, y, z) world-space position for the scene.
        scale: Uniform scale factor for the entire scene.
        cookie_color: (R, G, B, A) base color for the cookie.
        chip_color: (R, G, B, A) base color for the chocolate chips.
        tray_color: (R, G, B, A) base color for the tray.
        light_power: Power of the area light in Watts.
        light_temperature: Color temperature of the area light in Kelvin.
        **kwargs: Additional overrides for specific parameters.

    Returns:
        Status string, e.g., "Created 'CookieScene' at (0, 0, 0) with 3 objects"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import random
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    bpy.context.window.scene = scene

    # --- Materials ---
    # Cookie Material
    cookie_mat = bpy.data.materials.new(name=f"{base_object_name}_Material")
    cookie_mat.use_nodes = True
    bsdf = cookie_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = cookie_color
    bsdf.inputs["Roughness"].default_value = 0.6
    
    # Chocolate Chip Material
    chip_mat = bpy.data.materials.new(name=f"ChocolateChip_Material")
    chip_mat.use_nodes = True
    bsdf_chip = chip_mat.node_tree.nodes["Principled BSDF"]
    bsdf_chip.inputs["Base Color"].default_value = chip_color
    bsdf_chip.inputs["Roughness"].default_value = 0.6

    # Tray Material
    tray_mat = bpy.data.materials.new(name=f"{tray_object_name}_Material")
    tray_mat.use_nodes = True
    bsdf_tray = tray_mat.node_tree.nodes["Principled BSDF"]
    bsdf_tray.inputs["Base Color"].default_value = tray_color
    bsdf_tray.inputs["Roughness"].default_value = 0.3 # Slightly less rough for a polished look

    # --- Cookie Base ---
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=64, radius=0.75 * scale, depth=0.2 * scale,
        location=(location[0], location[1], location[2] + 0.1 * scale)
    )
    cookie_obj = bpy.context.active_object
    cookie_obj.name = base_object_name
    bpy.ops.object.shade_smooth()
    cookie_obj.data.materials.append(cookie_mat)

    # --- Chocolate Chips ---
    num_chips = 15
    chips_parent_obj = bpy.data.objects.new(f"{base_object_name}_Chips", None)
    scene.collection.objects.link(chips_parent_obj)
    chips_parent_obj.parent = cookie_obj # Parent chips to cookie

    for i in range(num_chips):
        random_radius = random.uniform(0.1 * scale, 0.6 * scale)
        random_angle = random.uniform(0, 2 * math.pi)
        
        chip_loc_x = random_radius * math.cos(random_angle)
        chip_loc_y = random_radius * math.sin(random_angle)
        chip_loc_z = 0.1 * scale  # Sit on top of the cookie

        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.08 * scale, segments=16, ring_count=8,
            location=(location[0] + chip_loc_x, location[1] + chip_loc_y, location[2] + chip_loc_z)
        )
        chip_obj = bpy.context.active_object
        chip_obj.name = f"ChocolateChip_{i:03d}"
        bpy.ops.object.shade_smooth()
        chip_obj.data.materials.append(chip_mat)
        chip_obj.parent = chips_parent_obj

    # --- Tray ---
    bpy.ops.mesh.primitive_cube_add(
        size=2.0 * scale,
        location=(location[0], location[1], location[2] - 0.15 * scale) # Slightly below cookie
    )
    tray_obj = bpy.context.active_object
    tray_obj.name = tray_object_name
    
    # Scale flat
    tray_obj.scale.z = 0.1 * scale # Flatten it
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) # Apply scale for proper edit mode ops

    # Edit mode for inset and extrude
    bpy.context.view_layer.objects.active = tray_obj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(tray_obj.data)
    
    # Select top face
    top_face = None
    for face in bm.faces:
        if face.normal.z > 0.9: # Assuming Z is up
            top_face = face
            break
            
    if top_face:
        top_face.select = True
        
        # Inset
        bpy.ops.mesh.inset(thickness=0.1 * scale, depth=0.0) # Inset by 10% of base size
        
        # Extrude down
        bpy.ops.mesh.extrude_region_move(
            MESH_OT_extrude_region={"use_normals_face": False, "use_individual_faces": False, "foward_only": False},
            TRANSFORM_OT_translate={"value": (0, 0, -0.05 * scale)} # Extrude downwards
        )

    bmesh.update_edit_mesh(tray_obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()
    tray_obj.data.materials.append(tray_mat)
    
    # --- Lighting ---
    # Delete default lights (if any, but skill is additive, so only delete those we create in this context)
    for obj in scene.objects:
        if obj.type == 'LIGHT' and obj.name.startswith("Light"): # Default light names
            bpy.data.objects.remove(obj, do_unlink=True)
            
    bpy.ops.object.light_add(type='AREA', radius=1.0 * scale, location=(location[0] + 3*scale, location[1] - 3*scale, location[2] + 4*scale))
    area_light = bpy.context.active_object
    area_light.data.energy = light_power
    area_light.data.color_temperature_type = 'KELVIN'
    area_light.data.temperature = light_temperature
    area_light.rotation_euler.x = math.radians(45)
    area_light.rotation_euler.z = math.radians(-45)

    # --- Camera Setup ---
    camera_obj = bpy.data.objects['Camera']
    camera_obj.location = (location[0] + 4.5*scale, location[1] - 4.5*scale, location[2] + 3*scale)
    # Point camera towards the center of the scene/cookie
    look_at_target = Vector((location[0], location[1], location[2] + 0.1 * scale)) 
    direction = look_at_target - camera_obj.location
    # Point camera using 'track to' constraint temporarily
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera_obj.rotation_euler = rot_quat.to_euler()

    # --- Rendering Settings ---
    scene.render.engine = 'CYCLES'
    # Optional: set render samples for final quality
    scene.cycles.samples = 128
    scene.cycles.max_bounces = 4

    return f"Created '{base_object_name}' scene at {location} with {num_chips + 2} objects (cookie, tray, chips)."

