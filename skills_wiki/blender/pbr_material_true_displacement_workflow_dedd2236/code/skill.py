def create_pbr_displacement_surface(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Plane",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.35, 0.25, 0.20),
    **kwargs
) -> str:
    """
    Create a highly subdivided plane with true PBR displacement in Cycles.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created mesh.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the rock/surface.
        **kwargs: 
            subdivision_level (int): Default 6. Density of the mesh.
            displacement_scale (float): Default 0.2. Height of the displacement.
            
    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Euler
    
    # Extract optional kwargs
    subdiv_level = kwargs.get('subdivision_level', 6)
    disp_scale = kwargs.get('displacement_scale', 0.2)

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry & Topology ===
    # Create a plane
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface for vertex density (Simple mode keeps square edges)
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = subdiv_level
    subsurf.render_levels = subdiv_level

    # === Step 2: Build Material & PBR Nodes ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    
    # CRITICAL: Enable true displacement in Cycles Material Settings
    mat.cycles.displacement_method = 'DISPLACEMENT'
    obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Shader Nodes
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (400, 0)

    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf_node.location = (0, 0)

    disp_node = nodes.new(type='ShaderNodeDisplacement')
    disp_node.location = (0, -200)
    disp_node.inputs['Scale'].default_value = disp_scale

    # Procedural Texture Setup (Substituting external image downloads)
    noise_node = nodes.new(type='ShaderNodeTexNoise')
    noise_node.location = (-400, 0)
    noise_node.inputs['Scale'].default_value = 4.0
    noise_node.inputs['Detail'].default_value = 15.0
    noise_node.inputs['Roughness'].default_value = 0.6

    # Color Ramp for Base Color mapping
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (-200, 100)
    color_ramp.color_ramp.elements[0].color = (material_color[0]*0.4, material_color[1]*0.4, material_color[2]*0.4, 1.0)
    color_ramp.color_ramp.elements[1].color = (material_color[0], material_color[1], material_color[2], 1.0)

    # Map the procedural noise to Color, Roughness, and Displacement Height
    links.new(noise_node.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf_node.inputs['Base Color'])
    links.new(noise_node.outputs['Fac'], bsdf_node.inputs['Roughness'])
    links.new(noise_node.outputs['Fac'], disp_node.inputs['Height'])

    # Connect Principled and Displacement to Output
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
    links.new(disp_node.outputs['Displacement'], output_node.inputs['Displacement'])

    # === Step 3: Scene Context & Lighting ===
    # Switch engine to Cycles as required by true shader displacement
    scene.render.engine = 'CYCLES'

    # Add dramatic Sun light (Strength 5) as specified in tutorial
    bpy.ops.object.light_add(
        type='SUN', 
        radius=1.0, 
        location=(location[0], location[1], location[2] + 5.0)
    )
    sun = bpy.context.active_object
    sun.name = f"{object_name}_SunLight"
    sun.data.energy = 5.0
    # Angle the sun to show off the displacement shadows
    sun.rotation_euler = Euler((math.radians(45), 0, math.radians(45)), 'XYZ')

    # Deselect all and select the main object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    return f"Created displaced surface '{object_name}' with sub-div level {subdiv_level} and Cycles settings enabled."
