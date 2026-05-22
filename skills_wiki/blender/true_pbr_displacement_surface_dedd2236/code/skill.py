def create_pbr_displacement_plane(
    scene_name: str = "Scene",
    object_name: str = "DisplacedRockPlane",
    location: tuple = (0, 0, 0),
    scale: float = 5.0,
    base_color_dark: tuple = (0.05, 0.04, 0.03, 1.0),
    base_color_light: tuple = (0.25, 0.20, 0.15, 1.0),
    displacement_scale: float = 0.2,
    subdivision_levels: int = 7,
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with true PBR geometric displacement in Cycles.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created plane.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the plane.
        base_color_dark: RGBA tuple for the dark crevices of the rock.
        base_color_light: RGBA tuple for the light peaks of the rock.
        displacement_scale: How strong the displacement effect is.
        subdivision_levels: How many times to subdivide (higher = more detail, slower render).

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # 1. Set engine to Cycles (Required for true material displacement)
    scene.render.engine = 'CYCLES'
    if scene.cycles:
        scene.cycles.feature_set = 'SUPPORTED' # Standard Cycles feature set

    # 2. Add Base Plane
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    plane = bpy.context.active_object
    plane.name = object_name
    plane.scale = (scale, scale, scale)
    
    # Apply scale so displacement calculates correctly
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # 3. Add Subdivision Surface Modifier
    subsurf = plane.modifiers.new(name="HighResSubdiv", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE' # Keeps corners sharp
    subsurf.levels = subdivision_levels
    subsurf.render_levels = subdivision_levels

    # 4. Create Material
    mat_name = f"{object_name}_Material"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    
    # IMPORTANT: Enable True Displacement in material settings
    mat.cycles.displacement_method = 'DISPLACEMENT'
    
    plane.data.materials.append(mat)

    # 5. Build Procedural PBR Nodes
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Clear default nodes to build clean

    # Output Node
    node_output = nodes.new(type="ShaderNodeOutputMaterial")
    node_output.location = (1000, 0)

    # Principled BSDF
    node_bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    node_bsdf.location = (700, 200)

    # Procedural Height/Texture Generation
    node_tex_coord = nodes.new(type="ShaderNodeTexCoord")
    node_tex_coord.location = (-600, 0)

    node_mapping = nodes.new(type="ShaderNodeMapping")
    node_mapping.location = (-400, 0)
    node_mapping.inputs['Scale'].default_value = (2.0, 2.0, 2.0)

    # Base Noise (Large details)
    node_noise = nodes.new(type="ShaderNodeTexNoise")
    node_noise.location = (-150, 0)
    node_noise.inputs['Scale'].default_value = 3.0
    node_noise.inputs['Detail'].default_value = 15.0
    node_noise.inputs['Roughness'].default_value = 0.65
    
    # Secondary Noise (Fine grit)
    node_noise_fine = nodes.new(type="ShaderNodeTexNoise")
    node_noise_fine.location = (-150, -300)
    node_noise_fine.inputs['Scale'].default_value = 25.0
    node_noise_fine.inputs['Detail'].default_value = 10.0
    
    # Mix Noises for varied height map
    node_mix_height = nodes.new(type="ShaderNodeMix")
    node_mix_height.data_type = 'FLOAT'
    node_mix_height.location = (100, -100)
    node_mix_height.inputs['Factor'].default_value = 0.2 # 20% fine grit

    # Color Ramp for Base Color
    node_color_ramp = nodes.new(type="ShaderNodeValToRGB")
    node_color_ramp.location = (400, 200)
    node_color_ramp.color_ramp.elements[0].position = 0.3
    node_color_ramp.color_ramp.elements[0].color = base_color_dark
    node_color_ramp.color_ramp.elements[1].position = 0.7
    node_color_ramp.color_ramp.elements[1].color = base_color_light

    # Color Ramp for Roughness
    node_roughness_ramp = nodes.new(type="ShaderNodeValToRGB")
    node_roughness_ramp.location = (400, -50)
    node_roughness_ramp.color_ramp.elements[0].position = 0.0
    node_roughness_ramp.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1.0)
    node_roughness_ramp.color_ramp.elements[1].position = 1.0
    node_roughness_ramp.color_ramp.elements[1].color = (0.9, 0.9, 0.9, 1.0)

    # Displacement Node
    node_displacement = nodes.new(type="ShaderNodeDisplacement")
    node_displacement.location = (700, -200)
    node_displacement.inputs['Scale'].default_value = displacement_scale
    node_displacement.inputs['Midlevel'].default_value = 0.5

    # Wire it all together
    links.new(node_tex_coord.outputs['Object'], node_mapping.inputs['Vector'])
    links.new(node_mapping.outputs['Vector'], node_noise.inputs['Vector'])
    links.new(node_mapping.outputs['Vector'], node_noise_fine.inputs['Vector'])
    
    links.new(node_noise.outputs['Fac'], node_mix_height.inputs['A'])
    links.new(node_noise_fine.outputs['Fac'], node_mix_height.inputs['B'])
    
    # Connect height to color/roughness
    links.new(node_mix_height.outputs['Result'], node_color_ramp.inputs['Fac'])
    links.new(node_mix_height.outputs['Result'], node_roughness_ramp.inputs['Fac'])
    
    # Connect height to displacement
    links.new(node_mix_height.outputs['Result'], node_displacement.inputs['Height'])
    
    # Connect to Principled BSDF (Blender 4.0+ uses 'Base Color', earlier uses identical)
    links.new(node_color_ramp.outputs['Color'], node_bsdf.inputs['Base Color'])
    links.new(node_roughness_ramp.outputs['Color'], node_bsdf.inputs['Roughness'])
    
    # Connect to Output
    links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])
    links.new(node_displacement.outputs['Displacement'], node_output.inputs['Displacement'])

    # 6. Add Sun Light (as shown in the tutorial)
    # We place it above and angle it to emphasize the displacement shadows
    bpy.ops.object.light_add(type='SUN', radius=1.0, location=(location[0], location[1], location[2] + 10.0))
    sun = bpy.context.active_object
    sun.name = f"{object_name}_SunLight"
    sun.data.energy = 5.0
    # Rotate the sun (about 45 degrees on X, 30 on Y) to cast shadows
    sun.rotation_euler = (math.radians(45), math.radians(30), 0)

    return f"Created '{object_name}' (PBR Displaced Plane) with subdivision level {subdivision_levels} and Sun light."
