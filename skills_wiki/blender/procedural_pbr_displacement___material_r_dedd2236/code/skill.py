def create_pbr_displacement_setup(
    scene_name: str = "Scene",
    object_name: str = "PBR_DisplacedRock",
    location: tuple = (0, 0, 0),
    scale: float = 3.0,
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with a procedural PBR rock displacement material.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    # Get target scene
    scene = bpy.data.scenes.get(scene_name) or getattr(bpy.context, 'scene', bpy.data.scenes[0])

    # === Step 1: Create and Subdivide Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    plane = bpy.context.active_object
    plane.name = object_name
    plane.scale = (scale, scale, scale)

    # Base destructive subdivision for even grid density
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=50) # Creates a dense 51x51 grid
    bpy.ops.object.mode_set(mode='OBJECT')

    # Non-destructive Subdivision modifier for final render resolution
    subdiv = plane.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.subdivision_type = 'SIMPLE' # Keeps plane edges sharp
    subdiv.levels = 2
    subdiv.render_levels = 4

    # === Step 2: Build Procedural PBR Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    plane.data.materials.append(mat)
    
    # CRITICAL: Enable true displacement in Cycles material settings
    mat.cycles.displacement_method = 'DISPLACEMENT'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Clear default nodes

    # Core Nodes
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1000, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (600, 0)
    bsdf.inputs['Roughness'].default_value = 0.85 # Rocks are rough
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    # Displacement Node
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (600, -250)
    disp_node.inputs['Midlevel'].default_value = 0.0
    disp_node.inputs['Scale'].default_value = 0.15 * scale # Scale relative to object size
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])

    # Procedural Textures (Replicating external image maps)
    # Voronoi provides the large structural rock blocks
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (0, 0)
    voronoi.feature = 'DISTANCE_TO_EDGE' # Creates crack-like structures
    voronoi.inputs['Scale'].default_value = 4.0

    # Noise provides high-frequency surface detail
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (0, -250)
    noise.inputs['Scale'].default_value = 25.0
    noise.inputs['Detail'].default_value = 15.0

    # Combine textures for height map
    mult_noise = nodes.new('ShaderNodeMath')
    mult_noise.operation = 'MULTIPLY'
    mult_noise.location = (200, -250)
    mult_noise.inputs[1].default_value = 0.1 # Dampen noise intensity
    links.new(noise.outputs['Fac'], mult_noise.inputs[0])

    add_disp = nodes.new('ShaderNodeMath')
    add_disp.operation = 'ADD'
    add_disp.location = (400, -200)
    links.new(voronoi.outputs['Distance'], add_disp.inputs[0])
    links.new(mult_noise.outputs['Value'], add_disp.inputs[1])
    links.new(add_disp.outputs['Value'], disp_node.inputs['Height'])

    # Colorization (Grays and Browns)
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (300, 100)
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (0.015, 0.012, 0.01, 1.0) # Deep dirt cracks
    
    elem_mid = color_ramp.color_ramp.elements.new(0.15)
    elem_mid.color = (0.15, 0.13, 0.11, 1.0) # Midtone rock
    
    color_ramp.color_ramp.elements[-1].position = 1.0
    color_ramp.color_ramp.elements[-1].color = (0.45, 0.40, 0.35, 1.0) # Highlight rock peaks
    
    links.new(voronoi.outputs['Distance'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])

    # Bump map (for micro detail interacting with light)
    bump = nodes.new('ShaderNodeBump')
    bump.location = (350, -450)
    bump.inputs['Distance'].default_value = 0.05
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    # === Step 3: Lighting & Engine Setup ===
    # True displacement requires Cycles
    scene.render.engine = 'CYCLES'
    if hasattr(scene.cycles, 'feature_set'):
        scene.cycles.feature_set = 'SUPPORTED'
    
    # Add strong directional Sun light to cast shadows from the displacement
    light_data = bpy.data.lights.new(name=f"{object_name}_Sun", type='SUN')
    light_data.energy = 5.0 # Match tutorial intensity
    light_data.angle = 0.05 # Hard shadows
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_Sun", object_data=light_data)
    scene.collection.objects.link(light_obj)
    
    # Position sun offset from the plane and angle it downward
    sun_loc = Vector(location) + Vector((5, -5, 8))
    light_obj.location = sun_loc
    
    direction = Vector(location) - sun_loc
    rot_quat = direction.to_track_quat('-Z', 'Y')
    light_obj.rotation_euler = rot_quat.to_euler()

    return f"Created PBR displaced '{object_name}' and directional Sun lighting at {location} (Engine set to Cycles)."
