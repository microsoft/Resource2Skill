def create_object(
    scene_name: str = "Scene",
    object_name: str = "RealisticGlass_Monkey",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (1.0, 1.0, 1.0),
    **kwargs,
) -> str:
    """
    Create a highly realistic Eevee glass object using Fresnel-mixed transparency and solidify.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) tint of the glass.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Engine Setup for Eevee Glass ===
    if scene.render.engine == 'BLENDER_EEVEE':
        # Support for Blender 4.2+ Eevee Next Raytracing
        if hasattr(scene.eevee, "use_raytracing"):
            scene.eevee.use_raytracing = True
        # Support for older Eevee Screen Space Reflections/Refractions
        elif hasattr(scene.eevee, "use_ssr"):
            scene.eevee.use_ssr = True
            scene.eevee.use_ssr_refraction = True

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_monkey_add(location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Apply smooth shading
    for poly in obj.data.polygons:
        poly.use_smooth = True

    # Add Subdivision Surface
    subsurf = obj.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # Add Solidify for glass wall thickness
    solidify = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = 0.02 * scale

    # === Step 2: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_GlassMat")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'
    mat.shadow_method = 'HASHED'
    
    # Enable Material Refraction for older Eevee
    if hasattr(mat, "use_screen_refraction"):
        mat.use_screen_refraction = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create Nodes
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (800, 0)

    mix_node = nodes.new('ShaderNodeMixShader')
    mix_node.location = (600, 0)

    transparent_node = nodes.new('ShaderNodeBsdfTransparent')
    transparent_node.location = (300, 150)

    principled_node = nodes.new('ShaderNodeBsdfPrincipled')
    principled_node.location = (300, -150)
    principled_node.inputs['Base Color'].default_value = (*material_color, 1.0)
    principled_node.inputs['Roughness'].default_value = 0.0
    
    # Handle Transmission API changes across Blender versions
    if 'Transmission Weight' in principled_node.inputs:
        principled_node.inputs['Transmission Weight'].default_value = 1.0
    elif 'Transmission' in principled_node.inputs:
        principled_node.inputs['Transmission'].default_value = 1.0

    ramp_node = nodes.new('ShaderNodeValToRGB')
    ramp_node.location = (300, 400)
    # Change the black value to a dark gray to prevent total invisibility at the center
    ramp_node.color_ramp.elements[0].color = (0.18, 0.18, 0.18, 1.0)
    ramp_node.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)

    fresnel_node = nodes.new('ShaderNodeFresnel')
    fresnel_node.location = (100, 400)
    fresnel_node.inputs['IOR'].default_value = 1.12

    # Connect Nodes
    links.new(fresnel_node.outputs['Fac'], ramp_node.inputs['Fac'])
    links.new(ramp_node.outputs['Color'], mix_node.inputs['Fac'])
    links.new(transparent_node.outputs['BSDF'], mix_node.inputs[1]) # Top input
    links.new(principled_node.outputs['BSDF'], mix_node.inputs[2]) # Bottom input
    links.new(mix_node.outputs['Shader'], out_node.inputs['Surface'])

    # Assign material
    obj.data.materials.append(mat)

    # === Step 3: Add Lighting (Optional but necessary to see glass) ===
    # Glass requires light/environment reflections to be visible, so we add an Area Light above it
    light_data = bpy.data.lights.new(name=f"{object_name}_RimLight", type='AREA')
    light_data.energy = 500.0 * (scale ** 2)
    light_data.shape = 'RECTANGLE'
    light_data.size = 5.0 * scale
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_RimLight", object_data=light_data)
    scene.collection.objects.link(light_obj)
    light_obj.location = (location[0], location[1] - (2.0 * scale), location[2] + (3.0 * scale))
    # Point light at the object
    direction = Vector(location) - light_obj.location
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    return f"Created '{object_name}' (Realistic Eevee Glass) at {location}."
