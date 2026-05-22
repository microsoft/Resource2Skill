def create_object(
    scene_name: str = "Scene",
    object_name: str = "Pavement_With_Grime",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.5, 0.45, 0.4),
    **kwargs,
) -> str:
    """
    Create a ground plane with a procedural grime/dirt layering material.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created plane object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the clean paving/bricks.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=10.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # === Step 2: Build Material Node Tree ===
    mat = bpy.data.materials.new(name=f"{object_name}_Material")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Output and BSDF
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1200, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (900, 0)
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])
    
    # Coordinates
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1200, 0)
    
    # --- 2a. Base Texture (Procedural Bricks representing clean pavement) ---
    mapping_base = nodes.new('ShaderNodeMapping')
    mapping_base.location = (-900, 200)
    mapping_base.inputs['Scale'].default_value = (5.0, 5.0, 5.0)
    links.new(tex_coord.outputs['UV'], mapping_base.inputs['Vector'])
    
    brick_tex = nodes.new('ShaderNodeTexBrick')
    brick_tex.location = (-600, 200)
    base_rgba = (material_color[0], material_color[1], material_color[2], 1.0)
    brick_tex.inputs['Color1'].default_value = base_rgba
    brick_tex.inputs['Color2'].default_value = (base_rgba[0]*0.8, base_rgba[1]*0.8, base_rgba[2]*0.8, 1.0)
    brick_tex.inputs['Mortar'].default_value = (0.05, 0.05, 0.05, 1.0)
    brick_tex.inputs['Scale'].default_value = 4.0
    links.new(mapping_base.outputs['Vector'], brick_tex.inputs['Vector'])
    
    # --- 2b. Procedural Dirt/Grime Mask ---
    mapping_noise = nodes.new('ShaderNodeMapping')
    mapping_noise.location = (-900, -200)
    links.new(tex_coord.outputs['Object'], mapping_noise.inputs['Vector'])
    
    noise_tex = nodes.new('ShaderNodeTexNoise')
    noise_tex.location = (-600, -200)
    noise_tex.inputs['Scale'].default_value = 3.0
    noise_tex.inputs['Detail'].default_value = 15.0
    noise_tex.inputs['Roughness'].default_value = 0.65
    noise_tex.inputs['Distortion'].default_value = 0.1
    links.new(mapping_noise.outputs['Vector'], noise_tex.inputs['Vector'])
    
    # High contrast ColorRamp to isolate dirt patches
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-300, -200)
    color_ramp.color_ramp.elements[0].position = 0.35
    color_ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    color_ramp.color_ramp.elements[1].position = 0.65
    color_ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
    links.new(noise_tex.outputs['Fac'], color_ramp.inputs['Fac'])
    
    # --- 2c. Mixing Properties ---
    
    # Base Color Mix (Clean Base vs Dark Dirt)
    # Using legacy MixRGB for maximum backwards/forwards API compatibility
    mix_color = nodes.new('ShaderNodeMixRGB')
    mix_color.blend_type = 'MIX'
    mix_color.location = (200, 200)
    links.new(color_ramp.outputs['Color'], mix_color.inputs['Fac'])
    links.new(brick_tex.outputs['Color'], mix_color.inputs['Color1'])
    mix_color.inputs['Color2'].default_value = (0.1, 0.08, 0.06, 1.0) # Dark brown/grey dirt
    
    # Roughness Map Range (Clean = smooth/reflective, Dirt = rough/matte)
    map_roughness = nodes.new('ShaderNodeMapRange')
    map_roughness.location = (200, -50)
    links.new(color_ramp.outputs['Color'], map_roughness.inputs['Value'])
    map_roughness.inputs['To Min'].default_value = 0.15 # Clean surface roughness
    map_roughness.inputs['To Max'].default_value = 0.95 # Dirty surface roughness
    
    # Bump Overlay
    bump = nodes.new('ShaderNodeBump')
    bump.location = (200, -300)
    bump.inputs['Distance'].default_value = 0.05
    bump.inputs['Strength'].default_value = 0.4
    links.new(color_ramp.outputs['Color'], bump.inputs['Height'])
    
    # Connect to Principled BSDF
    links.new(mix_color.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(map_roughness.outputs['Result'], bsdf.inputs['Roughness'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    
    obj.data.materials.append(mat)
    
    # === Step 3: Add Lighting Setup ===
    # Add a point light at a grazing angle to highlight the roughness map
    light_data = bpy.data.lights.new(name=f"{object_name}_Highlight", type='POINT')
    light_data.energy = 2500
    light_data.color = (1.0, 0.95, 0.8)
    light_obj = bpy.data.objects.new(name=f"{object_name}_Highlight", object_data=light_data)
    bpy.context.collection.objects.link(light_obj)
    
    light_obj.location = Vector(location) + Vector((3.0, -3.0, 1.5))
    
    return f"Created '{object_name}' with procedural grime material and grazing light at {location}."
