def create_displaced_surface(
    scene_name: str = "Scene",
    object_name: str = "DisplacedTerrain",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.35, 0.25, 0.18),
    **kwargs,
) -> str:
    """
    Create a procedural physically displaced terrain utilizing Cycles True Displacement.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the terrain plane.
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Overrides like 'subdiv_levels' (default 6) and 'displacement_scale' (default 0.2).

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Render Engine Context ===
    # True displacement requires Cycles to render properly.
    scene.render.engine = 'CYCLES'

    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    plane = bpy.context.active_object
    plane.name = object_name
    plane.scale = (scale, scale, scale)

    # Add heavy subdivision to provide vertices for the displacement
    subdiv_levels = kwargs.get("subdiv_levels", 6)
    subsurf = plane.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = subdiv_levels
    subsurf.render_levels = subdiv_levels

    # === Step 3: Build Material & Displacement Logic ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    # CRITICAL: Enable true displacement in the material settings
    mat.cycles.displacement_method = 'DISPLACEMENT'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output & Shader
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)
    
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (400, 0)

    # Procedural Texture setup
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-400, 0)
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-200, 0)
    noise.inputs['Scale'].default_value = 4.0
    noise.inputs['Detail'].default_value = 15.0
    noise.inputs['Roughness'].default_value = 0.65

    # Color mapping for visual interest
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (100, 150)
    dark_color = (material_color[0] * 0.4, material_color[1] * 0.4, material_color[2] * 0.4, 1.0)
    color_ramp.color_ramp.elements[0].color = dark_color
    color_ramp.color_ramp.elements[1].color = (*material_color, 1.0)

    # Displacement Node Setup
    displacement = nodes.new('ShaderNodeDisplacement')
    displacement.location = (100, -200)
    displacement_scale = kwargs.get("displacement_scale", 0.2)
    displacement.inputs['Scale'].default_value = displacement_scale * scale
    displacement.inputs['Midlevel'].default_value = 0.5

    # Node Connections
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
    
    # Drive roughness using noise to make peaks smoother/valleys rougher (or vice versa)
    links.new(noise.outputs['Fac'], principled.inputs['Roughness'])
    
    # Drive the physical displacement height using the noise factor
    links.new(noise.outputs['Fac'], displacement.inputs['Height'])
    
    # Connect to Output
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    links.new(displacement.outputs['Displacement'], output.inputs['Displacement'])

    # Assign material to the plane
    if len(plane.data.materials) == 0:
        plane.data.materials.append(mat)
    else:
        plane.data.materials[0] = mat

    # === Step 4: Ensure Complementary Lighting ===
    # True displacement shadows are best viewed with a strong directional light
    sun_exists = any(light.type == 'SUN' for light in bpy.data.lights)
    if not sun_exists:
        light_data = bpy.data.lights.new(name=f"{object_name}_Sun", type='SUN')
        light_data.energy = 5.0
        light_obj = bpy.data.objects.new(name=f"{object_name}_Sun", object_data=light_data)
        bpy.context.collection.objects.link(light_obj)
        
        # Position Sun off to the side and angle it down
        light_obj.location = (location[0] - 5 * scale, location[1] - 5 * scale, location[2] + 10 * scale)
        light_obj.rotation_euler = (math.radians(45), 0, math.radians(-45))

    return f"Created '{object_name}' with True Displacement at {location}. Note: Render engine automatically switched to Cycles."
