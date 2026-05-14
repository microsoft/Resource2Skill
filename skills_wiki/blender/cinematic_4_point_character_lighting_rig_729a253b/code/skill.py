def create_object(
    scene_name: str = "Scene",
    object_name: str = "CinematicLightRig",
    location: tuple = (0, 0, 1),
    scale: float = 1.0,
    material_color: tuple = (0.0, 0.8, 1.0), # Used for the cinematic accent lights (e.g., glowing blue props)
    **kwargs,
) -> str:
    """
    Create a Cinematic 4-Point Light Rig in the active Blender scene.
    Includes a Key, Rim, and two colored Accent lights, plus an optional test subject.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the rig collection and objects.
        location: (x, y, z) world-space position (center of the subject's head).
        scale: Uniform scale factor for light distance and radius.
        material_color: (R, G, B) color used for the shoulder accent lights.
        **kwargs: add_test_subject (bool) - Set to False to skip creating the monkey head.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    add_test_subject = kwargs.get("add_test_subject", True)
    
    # === Step 1: Configure Render Context ===
    scene.render.engine = 'BLENDER_EEVEE'
    if hasattr(scene.eevee, "use_bloom"):
        scene.eevee.use_bloom = True
        scene.eevee.bloom_intensity = 0.05
        scene.eevee.bloom_radius = 6.0
    
    # Darken world background for cinematic contrast
    if scene.world and scene.world.node_tree:
        bg_node = scene.world.node_tree.nodes.get("Background")
        if bg_node:
            bg_node.inputs[0].default_value = (0.01, 0.01, 0.01, 1.0)
            
    # Create a collection for the rig
    rig_coll = bpy.data.collections.new(object_name)
    scene.collection.children.link(rig_coll)
    
    center_loc = Vector(location)
    
    # Create an Empty to act as the parent/control for the rig
    rig_parent = bpy.data.objects.new(f"{object_name}_Control", None)
    rig_parent.empty_display_size = scale * 0.5
    rig_parent.empty_display_type = 'SPHERE'
    rig_parent.location = center_loc
    rig_coll.objects.link(rig_parent)

    # === Step 2: Create Lights ===
    def add_point_light(name, offset, power, color, radius):
        light_data = bpy.data.lights.new(name=name, type='POINT')
        light_data.energy = power * (scale ** 2)
        light_data.color = color
        light_data.shadow_soft_size = radius * scale
        
        light_obj = bpy.data.objects.new(name=name, object_data=light_data)
        light_obj.location = center_loc + (Vector(offset) * scale)
        light_obj.parent = rig_parent
        rig_coll.objects.link(light_obj)
        return light_obj

    # Key Light (Top Front)
    key_color = (1.0, 0.95, 0.9) # Warm white
    add_point_light(f"{object_name}_Key", (0.0, -1.2, 0.8), 75.0, key_color, 0.5)
    
    # Rim Light (Directly Behind, tight radius, high power)
    rim_color = (1.0, 1.0, 1.0) # Pure white
    add_point_light(f"{object_name}_Rim", (0.0, 1.0, 0.2), 150.0, rim_color, 0.1)
    
    # Accent Left (Shoulder height, colored)
    add_point_light(f"{object_name}_Accent_L", (-0.8, 0.0, -0.4), 20.0, material_color, 0.2)
    
    # Accent Right (Shoulder height, colored)
    add_point_light(f"{object_name}_Accent_R", (0.8, 0.0, -0.4), 20.0, material_color, 0.2)

    # === Step 3: Optional Test Subject ===
    if add_test_subject:
        # Generate Suzanne to visualize the lighting
        bpy.ops.mesh.primitive_monkey_add(location=center_loc, size=scale)
        monkey = bpy.context.active_object
        monkey.name = f"{object_name}_TestSubject"
        monkey.parent = rig_parent
        
        # Move from default collection to our rig collection
        for coll in monkey.users_collection:
            coll.objects.unlink(monkey)
        rig_coll.objects.link(monkey)
        
        # Apply Subdivision
        mod = monkey.modifiers.new(name="Subdivision", type='SUBSURF')
        mod.levels = 2
        mod.render_levels = 2
        
        # Apply Smooth Shading
        for poly in monkey.data.polygons:
            poly.use_smooth = True
            
        # Create Dark Metallic Material
        mat = bpy.data.materials.new(name=f"{object_name}_Subject_Mat")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            if 'Base Color' in bsdf.inputs:
                bsdf.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1.0)
            if 'Roughness' in bsdf.inputs:
                bsdf.inputs['Roughness'].default_value = 0.4
            if 'Metallic' in bsdf.inputs:
                bsdf.inputs['Metallic'].default_value = 0.8
        monkey.data.materials.append(mat)
        
        return f"Created '{object_name}' light rig at {location} with 4 lights and a test subject."

    return f"Created '{object_name}' light rig at {location} with 4 lights."
