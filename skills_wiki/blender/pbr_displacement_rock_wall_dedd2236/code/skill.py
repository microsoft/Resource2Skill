def create_pbr_rock_wall(
    scene_name: str = "Scene",
    object_name: str = "PBRRockWall",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    subdivision_levels: int = 4, # Render subdivision levels for displacement
    displacement_scale: float = 0.2, # Scale of the displacement effect
    sun_strength: float = 5.0,
    **kwargs,
) -> str:
    """
    Creates a PBR rock wall plane with displacement in the active Blender scene.
    Assumes PBR image textures for albedo, roughness, normal, and displacement
    will be manually loaded by the user into the created Image Texture nodes.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created plane object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the plane.
        subdivision_levels: Number of subdivision levels for the Subdivision Surface modifier.
                            Higher values provide more detail for displacement.
        displacement_scale: Scale factor for the displacement map.
        sun_strength: Strength of the created Sun light.
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'PBRRockWall' at (0, 0, 0) with materials and light. Please load PBR image textures into the material's image nodes."
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # Ensure Cycles render engine is active for displacement
    if scene.render.engine != 'CYCLES':
        scene.render.engine = 'CYCLES'

    # === Step 1: Create Base Geometry (Plane) ===
    bpy.ops.mesh.primitive_plane_add(
        size=2, # Default size, will be scaled by 'scale' parameter
        enter_editmode=False,
        align='WORLD',
        location=(0,0,0), # Temporarily at origin, will be moved later
    )
    obj = bpy.context.active_object
    obj.name = object_name
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface modifier for displacement
    subd_modifier = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subd_modifier.levels = subdivision_levels # Viewport levels
    subd_modifier.render_levels = subdivision_levels # Render levels
    subd_modifier.subdivision_type = 'SIMPLE' # Simple subdivision preserves UVs better for displacement

    # === Step 2: Build Material ===
    mat_name = f"{object_name}_Material"
    material = bpy.data.materials.new(name=mat_name)
    material.use_nodes = True
    obj.data.materials.append(material)

    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Clear default nodes except Principled BSDF and Material Output
    for node in nodes:
        if node.type not in ('BSDF_PRINCIPLED', 'OUTPUT_MATERIAL'):
            nodes.remove(node)

    principled_bsdf = next((n for n in nodes if n.type == 'BSDF_PRINCIPLED'), None)
    material_output = next((n for n in nodes if n.type == 'OUTPUT_MATERIAL'), None)

    # Ensure Principled BSDF and Material Output exist and are linked
    if not principled_bsdf:
        principled_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    if not material_output:
        material_output = nodes.new(type='ShaderNodeOutputMaterial')
    
    if not any(link for link in links if link.from_node == principled_bsdf and link.to_node == material_output and link.to_socket == material_output.inputs['Surface']):
        links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])

    # Position nodes for better readability
    principled_bsdf.location = Vector((-200, 0))
    material_output.location = Vector((200, 0))

    # Add Image Texture nodes for PBR maps
    # IMPORTANT: User needs to manually load actual images into these nodes.
    # The 'image = None' lines are placeholders.

    # Albedo/Base Color
    tex_albedo = nodes.new(type='ShaderNodeTexImage')
    tex_albedo.name = "Image_Albedo"
    tex_albedo.label = "Albedo (Base Color)"
    tex_albedo.location = Vector([-800, 200])
    links.new(tex_albedo.outputs['Color'], principled_bsdf.inputs['Base Color'])
    tex_albedo.image = None # Placeholder, user to load image

    # Roughness Map
    tex_roughness = nodes.new(type='ShaderNodeTexImage')
    tex_roughness.name = "Image_Roughness"
    tex_roughness.label = "Roughness Map"
    tex_roughness.location = Vector([-800, -100])
    # Important for data maps: set colorspace to Non-Color
    tex_roughness.image = None # Placeholder, user to load image
    if tex_roughness.image: # Only if an image is loaded, otherwise it might error
        tex_roughness.image.colorspace_settings.name = 'Non-Color' 
    links.new(tex_roughness.outputs['Color'], principled_bsdf.inputs['Roughness'])

    # Normal Map
    tex_normal = nodes.new(type='ShaderNodeTexImage')
    tex_normal.name = "Image_Normal"
    tex_normal.label = "Normal Map"
    tex_normal.location = Vector([-800, -300])
    # Important for data maps: set colorspace to Non-Color
    tex_normal.image = None # Placeholder, user to load image
    if tex_normal.image:
        tex_normal.image.colorspace_settings.name = 'Non-Color' 

    normal_map_node = nodes.new(type='ShaderNodeNormalMap')
    normal_map_node.location = Vector([-400, -300])
    links.new(tex_normal.outputs['Color'], normal_map_node.inputs['Color'])
    links.new(normal_map_node.outputs['Normal'], principled_bsdf.inputs['Normal'])

    # Displacement Map
    tex_displacement = nodes.new(type='ShaderNodeTexImage')
    tex_displacement.name = "Image_Displacement"
    tex_displacement.label = "Displacement Map"
    tex_displacement.location = Vector([-800, -500])
    # Important for data maps: set colorspace to Non-Color
    tex_displacement.image = None # Placeholder, user to load image
    if tex_displacement.image:
        tex_displacement.image.colorspace_settings.name = 'Non-Color' 

    displacement_node = nodes.new(type='ShaderNodeDisplacement')
    displacement_node.location = Vector([-400, -500])
    displacement_node.inputs['Midlevel'].default_value = 0.5 # Default for most displacement maps
    displacement_node.inputs['Scale'].default_value = displacement_scale
    links.new(tex_displacement.outputs['Color'], displacement_node.inputs['Height'])
    links.new(displacement_node.outputs['Displacement'], material_output.inputs['Displacement'])

    # Set Material settings for actual displacement (not just bump)
    material.cycles.displacement_method = 'DISPLACEMENT' # Or 'DISPLACEMENT_AND_BUMP' as preferred

    # === Step 3: Lighting ===
    light_name = f"{object_name}_SunLight"
    
    # Check if a sun light with this name already exists in data and objects
    existing_light_data = bpy.data.lights.get(light_name)
    existing_light_object = bpy.data.objects.get(light_name)

    if existing_light_object:
        bpy.data.objects.remove(existing_light_object, do_unlink=True)
    if existing_light_data:
        bpy.data.lights.remove(existing_light_data, do_unlink=True)

    light_data = bpy.data.lights.new(name=light_name, type='SUN')
    light_data.energy = sun_strength
    light_object = bpy.data.objects.new(name=light_name, object_data=light_data)
    scene.collection.objects.link(light_object)
    light_object.location = Vector((5, -5, 5)) # Example sun position
    # Rotate light to cast shadows from an angle
    light_object.rotation_euler = (math.radians(30), math.radians(-30), math.radians(135))

    # Set render engine to Cycles and enable GPU if available (good practice for performance)
    scene.render.engine = 'CYCLES'
    if bpy.context.preferences.addons['cycles'].preferences.has_active_device():
        scene.cycles.device = 'GPU'
        # Set all available devices (CUDA/OPTIX) to use for Cycles rendering
        for device in bpy.context.preferences.addons['cycles'].preferences.devices:
            if device.type in ('CUDA', 'OPTIX'):
                device.use = True
            else:
                device.use = False
    else:
        scene.cycles.device = 'CPU'

    return f"Created '{object_name}' at {location} with material '{mat_name}' and Sun light '{light_name}'. Please load PBR image textures into the material's image nodes."

