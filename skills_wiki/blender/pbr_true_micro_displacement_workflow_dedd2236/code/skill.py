def create_object(
    scene_name: str = "Scene",
    object_name: str = "Procedural_Displaced_Wall",
    location: tuple = (0, 0, 0),
    scale: float = 2.0,
    material_color: tuple = (0.25, 0.18, 0.12), # Base rock/dirt color
    **kwargs,
) -> str:
    """
    Create a highly displaced PBR surface mimicking a rock wall in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: 
            subdivision_level: Int (default 5). Higher = more detail but slower viewport.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Render Context Setup ===
    # True displacement REQUIRES Cycles to calculate physical geometry depth
    if scene.render.engine != 'CYCLES':
        scene.render.engine = 'CYCLES'

    # === Step 1: Create Base Geometry ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # Create a base grid to give the subsurf modifier a good starting topology
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=10, y_segments=10, size=1.0)
    for f in bm.faces:
        f.smooth = True
    bm.to_mesh(mesh)
    bm.free()

    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface modifier for micro-polygon density
    subsurf = obj.modifiers.new(name="MicroDisplacement", type='SUBSURF')
    subsurf.subdivision_type = 'CATMULL_CLARK'
    subdiv_level = kwargs.get('subdivision_level', 5)
    subsurf.levels = subdiv_level
    subsurf.render_levels = subdiv_level + 1

    # === Step 2: Build True Displacement Material ===
    mat = bpy.data.materials.new(name=object_name + "_PBR_Mat")
    mat.use_nodes = True
    
    # CRITICAL: Tell Cycles to actually move the vertices, not just fake the bump
    mat.cycles.displacement_method = 'DISPLACEMENT' 
    obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (800, 0)

    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.location = (400, 0)
    
    # Procedural Texture to simulate the PBR Map from the tutorial
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)

    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-400, 0)
    mapping.inputs['Scale'].default_value = (3.0, 3.0, 3.0)

    # High detail noise to create rock/ground shapes
    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.location = (-200, 0)
    noise.inputs['Scale'].default_value = 2.5
    noise.inputs['Detail'].default_value = 15.0
    noise.inputs['Roughness'].default_value = 0.65

    # Color mapping
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (100, 200)
    color_ramp.color_ramp.elements[0].color = (*material_color, 1.0)
    color_ramp.color_ramp.elements[0].position = 0.3
    color_ramp.color_ramp.elements[1].color = (0.05, 0.04, 0.03, 1.0) # Dark shadows in crevices
    color_ramp.color_ramp.elements[1].position = 0.7

    # Displacement Node Setup
    disp = nodes.new(type='ShaderNodeDisplacement')
    disp.location = (400, -300)
    disp.inputs['Scale'].default_value = 0.35  # Strength of the 3D pop
    disp.inputs['Midlevel'].default_value = 0.5

    # Wire it all up
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    
    # Drive Color
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
    
    # Drive Roughness
    links.new(noise.outputs['Fac'], principled.inputs['Roughness'])
    
    # Drive True Displacement
    links.new(noise.outputs['Fac'], disp.inputs['Height'])
    
    # Final Output routing
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    links.new(disp.outputs['Displacement'], output.inputs['Displacement'])

    # === Step 3: Add Complementary Lighting ===
    # Displacement needs strong directional light to cast micro-shadows
    light_data = bpy.data.lights.new(name=object_name + "_Sun", type='SUN')
    light_data.energy = 5.0 # Tutorial specified strength
    light_data.angle = math.radians(11.4) # Tutorial specified angle for crispness
    
    light_obj = bpy.data.objects.new(name=object_name + "_SunLight", object_data=light_data)
    scene.collection.objects.link(light_obj)
    
    # Position sun above and angle it across the plane to catch the bumps
    light_obj.location = Vector(location) + Vector((0, 0, 5))
    light_obj.rotation_euler = (math.radians(60), math.radians(45), 0)

    return f"Created '{object_name}' with True Cycles Displacement and directional Sun lighting at {location}. Subdiv level: {subdiv_level}."
