def create_stylized_eevee_lighting(
    scene_name: str = "Scene",
    object_name: str = "EEVEE_LightRig",
    location: tuple = (0, 0, 2),
    scale: float = 1.0,
    main_color: tuple = (1.0, 0.9, 0.8),
    main_energy: float = 3.0,
    bleed_color: tuple = (1.0, 0.2, 0.0), 
    bleed_energy: float = 5.0,
    bleed_offset_degrees: float = 3.0,
    bounce_color: tuple = (0.8, 0.6, 0.4), 
    bounce_energy: float = 0.5,
    **kwargs,
) -> str:
    """
    Create a Stylized EEVEE Lighting Rig (Terminator Bleed + Fake Bounce) in the active scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the rig and lights.
        location: (x, y, z) world-space position for the rig parent.
        scale: Influences the custom distance falloff of the local spot bounce.
        main_color: (R, G, B) primary sunlight color.
        main_energy: Intensity of primary sunlight.
        bleed_color: (R, G, B) highly saturated color for the shadow edge.
        bleed_energy: Intensity of the terminator bleed effect.
        bleed_offset_degrees: Angular offset to shift the shadow edge.
        bounce_color: (R, G, B) color of the ground/ambient bounce.
        bounce_energy: Intensity of the global ambient bounce.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection

    # === Step 1: Create Rig Parent (Empty) ===
    rig_empty = bpy.data.objects.new(name=object_name, object_data=None)
    rig_empty.empty_display_size = scale * 2.0
    rig_empty.empty_display_type = 'ARROWS'
    rig_empty.location = Vector(location)
    collection.objects.link(rig_empty)

    # Base sunlight angle (e.g., coming from upper-left front)
    base_rot_x = math.radians(50)
    base_rot_y = math.radians(0)
    base_rot_z = math.radians(45)

    # === Step 2: Main Sun Light ===
    main_data = bpy.data.lights.new(name=f"{object_name}_MainSun", type='SUN')
    main_data.color = main_color
    main_data.energy = main_energy
    main_data.use_shadow = True

    main_obj = bpy.data.objects.new(name=f"{object_name}_MainSun", object_data=main_data)
    main_obj.parent = rig_empty
    main_obj.location = (0, 0, 0)
    main_obj.rotation_euler = (base_rot_x, base_rot_y, base_rot_z)
    collection.objects.link(main_obj)

    # === Step 3: Bleed Sun Light (Terminator Effect) ===
    # Offset the rotation slightly to shift the shadow edge and reveal the saturated color
    bleed_data = bpy.data.lights.new(name=f"{object_name}_BleedSun", type='SUN')
    bleed_data.color = bleed_color
    bleed_data.energy = bleed_energy
    bleed_data.use_shadow = True

    bleed_obj = bpy.data.objects.new(name=f"{object_name}_BleedSun", object_data=bleed_data)
    bleed_obj.parent = rig_empty
    bleed_obj.location = (0, 0, 0)
    offset_rad = math.radians(bleed_offset_degrees)
    bleed_obj.rotation_euler = (base_rot_x, base_rot_y + offset_rad, base_rot_z + offset_rad)
    collection.objects.link(bleed_obj)

    # === Step 4: Global Bounce Sun Light (Fake GI) ===
    # Points UP, NO shadows. Uniformly illuminates all downward-facing polygons.
    gbounce_data = bpy.data.lights.new(name=f"{object_name}_GlobalBounce", type='SUN')
    gbounce_data.color = bounce_color
    gbounce_data.energy = bounce_energy
    gbounce_data.use_shadow = False  # CRITICAL: allows light to pass through geometry

    gbounce_obj = bpy.data.objects.new(name=f"{object_name}_GlobalBounce", object_data=gbounce_data)
    gbounce_obj.parent = rig_empty
    gbounce_obj.location = (0, 0, 0)
    gbounce_obj.rotation_euler = (math.radians(180), 0, 0) # 180x = Point straight up
    collection.objects.link(gbounce_obj)

    # === Step 5: Local Bounce Spot Light (Fake localized GI) ===
    # Soft, upward pointing spot with a strict cutoff distance to fake local ground scattering.
    lbounce_data = bpy.data.lights.new(name=f"{object_name}_LocalBounce", type='SPOT')
    lbounce_data.color = bounce_color
    lbounce_data.energy = bounce_energy * 200.0  # Spots need significantly higher wattage than suns
    lbounce_data.use_shadow = False              # CRITICAL for fake bounce
    lbounce_data.spot_blend = 1.0                # Maximum edge softness
    lbounce_data.spot_size = math.radians(120)
    lbounce_data.use_custom_distance = True
    lbounce_data.cutoff_distance = scale * 15.0  # Limit bounce height

    lbounce_obj = bpy.data.objects.new(name=f"{object_name}_LocalBounce", object_data=lbounce_data)
    lbounce_obj.parent = rig_empty
    lbounce_obj.location = (0, 0, -scale * 2.0) # Placed slightly below rig center
    lbounce_obj.rotation_euler = (math.radians(180), 0, 0)
    collection.objects.link(lbounce_obj)

    return f"Created stylized lighting rig '{object_name}' (Main, Bleed, Global Bounce, Local Bounce) at {location}."
