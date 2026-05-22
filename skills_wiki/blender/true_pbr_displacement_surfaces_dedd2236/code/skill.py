def create_pbr_displacement_plane(
    scene_name: str = "Scene",
    object_name: str = "DisplacedTerrain",
    location: tuple = (0, 0, 0),
    scale: float = 2.0,
    material_color: tuple = (0.35, 0.25, 0.2),
    **kwargs,
) -> str:
    """
    Creates a highly subdivided plane with a procedural true-displacement PBR material.
    Forces the scene into Cycles to render the physical geometric offset.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the rock/terrain.
        **kwargs: Optional overrides (e.g., disp_scale, subdivisions).

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Ensure Cycles Render Engine ===
    # True displacement only works in Cycles
    if bpy.context.preferences.addons.get('cycles') is None:
        bpy.ops.preferences.addon_enable(module='cycles')
    scene.render.engine = 'CYCLES'

    # === Step 2: Geometry & Subdivision ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    plane = bpy.context.active_object
    plane.name = object_name
    plane.scale = (scale, scale, scale)
    
    # Subdivide heavily to provide vertices for displacement
    subsurf = plane.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    sub_level = kwargs.get('subdivisions', 6)
    subsurf.levels = sub_level
    subsurf.render_levels = sub_level
    
    # === Step 3: Material & True Displacement Setup ===
    mat = bpy.data.materials.new(name=f"{object_name}_Displacement_Mat")
    mat.use_nodes = True
    
    # CRITICAL: Tell Cycles to use true displacement, not just bump
    mat.cycles.displacement_method = 'DISPLACEMENT' 
    plane.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Output & Principled BSDF
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    if 'Roughness' in bsdf.inputs:
        bsdf.inputs['Roughness'].default_value = 0.85
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    # Displacement Node Setup
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (-100, -300)
    disp_node.inputs['Midlevel'].default_value = 0.5
    disp_node.inputs['Scale'].default_value = kwargs.get('disp_scale', 0.15)
    links.new(disp_node.outputs['Displacement'], output.inputs['Displacement'])
    
    # Procedural Height Map (Simulating the PBR Height Texture)
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-800, -200)
    voronoi.feature = 'F1'
    voronoi.distance = 'EUCLIDEAN'
    voronoi.inputs['Scale'].default_value = 3.0
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-800, -500)
    noise.inputs['Scale'].default_value = 15.0
    noise.inputs['Detail'].default_value = 10.0
    
    # Mix the textures for varied height
    math_mul = nodes.new('ShaderNodeMath')
    math_mul.operation = 'MULTIPLY'
    math_mul.location = (-600, -500)
    math_mul.inputs[1].default_value = 0.3  # Scale down noise influence
    links.new(noise.outputs['Fac'], math_mul.inputs[0])
    
    math_add = nodes.new('ShaderNodeMath')
    math_add.operation = 'ADD'
    math_add.location = (-400, -300)
    links.new(voronoi.outputs['Distance'], math_add.inputs[0])
    links.new(math_mul.outputs['Value'], math_add.inputs[1])
    
    # Plug height data into displacement
    links.new(math_add.outputs['Value'], disp_node.inputs['Height'])
    
    # Micro-detail Bump (Simulating the PBR Normal Map)
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-300, -100)
    bump.inputs['Distance'].default_value = 0.05
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    
    # Base Color Variation (Simulating the PBR Albedo)
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (-300, 150)
    ramp.color_ramp.elements[0].color = (*material_color, 1.0)
    ramp.color_ramp.elements[1].color = (
        max(0.0, material_color[0] - 0.2),
        max(0.0, material_color[1] - 0.2),
        max(0.0, material_color[2] - 0.2),
        1.0
    )
    ramp.color_ramp.elements[1].position = 0.8
    links.new(voronoi.outputs['Distance'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    
    # === Step 4: Add Angled Lighting (Crucial for Displacement Shadows) ===
    sun_found = any(o.type == 'LIGHT' and o.data.type == 'SUN' for o in scene.objects)
    if not sun_found:
        bpy.ops.object.light_add(type='SUN', location=(location[0] + 5, location[1] - 5, location[2] + 5))
        sun = bpy.context.active_object
        sun.name = f"{object_name}_SunLight"
        sun.data.energy = 5.0
        # Angle at roughly 45 degrees to cast long shadows across the uneven terrain
        sun.rotation_euler = (math.radians(45), 0, math.radians(60))
        
    return f"Created '{object_name}' with procedural true displacement at {location}. Switch Viewport to Rendered mode (Cycles) to view."
