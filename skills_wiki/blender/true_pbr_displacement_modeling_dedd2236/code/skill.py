def create_object(
    scene_name: str = "Scene",
    object_name: str = "DisplacedRockWall",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 3.0,
    material_color: tuple = (0.25, 0.20, 0.15),
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with true procedural PBR displacement in Cycles.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created mesh.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the plane.
        material_color: (R, G, B) base color of the rock/ground.
        **kwargs: 
            subdiv_levels (int): Level of simple subdivision (default 7).
            disp_scale (float): Strength of the geometric displacement (default 0.25).

    Returns:
        Status string describing the creation and renderer switch.
    """
    import bpy
    import math
    from mathutils import Vector, Euler

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Force Cycles Engine for True Displacement ===
    # Displacement mapping only physically alters the mesh in Cycles.
    scene.render.engine = 'CYCLES'
    
    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # === Step 3: Add High-Density Subdivision ===
    # Displacement needs vertices to push around. 'SIMPLE' preserves the square shape.
    subdiv_levels = kwargs.get('subdiv_levels', 7)
    subdiv_mod = obj.modifiers.new(name="Displacement_Density", type='SUBSURF')
    subdiv_mod.subdivision_type = 'SIMPLE'
    subdiv_mod.levels = subdiv_levels
    subdiv_mod.render_levels = subdiv_levels

    # === Step 4: Build Procedural PBR Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    # *CRITICAL*: Tell the material to actually displace the geometry, not just bump.
    if hasattr(mat, 'cycles'):
        mat.cycles.displacement_method = 'DISPLACEMENT'
        
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    bsdf = nodes.get("Principled BSDF")
    output = nodes.get("Material Output")
    
    if bsdf:
        bsdf.inputs['Roughness'].default_value = 0.85 # Rocky/matte surface
        
    # Procedural Height/Detail Generator (Noise)
    noise = nodes.new(type="ShaderNodeTexNoise")
    noise.inputs['Scale'].default_value = 4.0
    noise.inputs['Detail'].default_value = 15.0
    noise.inputs['Roughness'].default_value = 0.65
    noise.inputs['Distortion'].default_value = 0.2
    
    # Color Ramp for Albedo (mapping noise to specific rock colors)
    ramp = nodes.new(type="ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.3
    ramp.color_ramp.elements[0].color = (material_color[0], material_color[1], material_color[2], 1.0)
    
    # Create a slightly darker variant for crevices
    dark_col = (max(0, material_color[0]-0.15), max(0, material_color[1]-0.15), max(0, material_color[2]-0.15), 1.0)
    ramp.color_ramp.elements[1].position = 0.7
    ramp.color_ramp.elements[1].color = dark_col

    # Displacement Node Setup
    disp_node = nodes.new(type="ShaderNodeDisplacement")
    disp_node.inputs['Midlevel'].default_value = 0.5
    disp_scale = kwargs.get('disp_scale', 0.25)
    disp_node.inputs['Scale'].default_value = disp_scale

    # Connect Nodes
    if bsdf and output:
        # Link Noise -> Ramp -> Albedo
        links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
        links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
        
        # Link Noise -> Displacement Height -> Material Output
        links.new(noise.outputs['Fac'], disp_node.inputs['Height'])
        links.new(disp_node.outputs['Displacement'], output.inputs['Displacement'])

    obj.data.materials.append(mat)

    # === Step 5: Add Sun Light (as per tutorial) ===
    # Create a strong directional light to cast shadows from the displaced geometry
    bpy.ops.object.light_add(type='SUN', location=(location[0] + 5, location[1] - 5, location[2] + 10))
    sun = bpy.context.active_object
    sun.name = f"{object_name}_Sun"
    sun.data.energy = 5.0
    
    # Point the sun diagonally at the ground plane
    sun.rotation_euler = Euler((math.radians(45), 0.0, math.radians(45)), 'XYZ')

    # De-select all and select the main object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    return f"Created '{object_name}' with True Cycles Displacement (Scale: {disp_scale}, Subdiv: {subdiv_levels}) and a Sun light."
