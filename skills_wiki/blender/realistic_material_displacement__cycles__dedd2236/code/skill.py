def create_object(
    scene_name: str = "Scene",
    object_name: str = "DisplacedTerrain",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.25, 0.20, 0.15),
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with real geometric displacement in Cycles.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created grid object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color in 0-1 range.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Render Engine Setup ===
    # Cycles is REQUIRED for material node displacement to physically move geometry
    scene.render.engine = 'CYCLES'

    # === Step 2: Create High-Density Geometry ===
    # A 200x200 grid provides 40,000 faces, giving the displacement map plenty of vertices to work with
    bpy.ops.mesh.primitive_grid_add(
        x_subdivisions=200, 
        y_subdivisions=200, 
        size=10, 
        location=location
    )
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    bpy.ops.object.shade_smooth()

    # === Step 3: Build the PBR Displacement Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Displacement_Mat")
    mat.use_nodes = True
    
    # CRITICAL: Tell Cycles to use actual displacement, not just bump
    mat.cycles.displacement_method = 'DISPLACEMENT'
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Output & Shader
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)

    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (0, 0)
    links.new(principled.outputs[0], output.inputs['Surface'])

    # Procedural Texture Generator (Substitutes external image files)
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 3.0
    noise.inputs['Detail'].default_value = 15.0  # High detail for micro-displacement
    noise.inputs['Roughness'].default_value = 0.6
    noise.location = (-600, 0)

    # Base Color Setup
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-300, 200)
    color_ramp.color_ramp.elements[0].color = (0.02, 0.02, 0.02, 1.0) # Dark crevices
    color_ramp.color_ramp.elements[1].color = (*material_color, 1.0)  # Main color
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])

    # Roughness Setup (Varying roughness based on texture)
    math_roughness = nodes.new('ShaderNodeMath')
    math_roughness.operation = 'MULTIPLY'
    math_roughness.inputs[1].default_value = 0.8
    math_roughness.location = (-300, 0)
    links.new(noise.outputs['Fac'], math_roughness.inputs[0])
    links.new(math_roughness.outputs[0], principled.inputs['Roughness'])

    # Displacement Node Setup
    disp = nodes.new('ShaderNodeDisplacement')
    disp.location = (0, -300)
    disp.inputs['Midlevel'].default_value = 0.5
    disp.inputs['Scale'].default_value = 1.0  # Strength of the displacement
    
    links.new(noise.outputs['Fac'], disp.inputs['Height'])
    links.new(disp.outputs['Displacement'], output.inputs['Displacement'])

    # Assign material to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    # === Step 4: Add Complementary Lighting ===
    # Add a Sun light to cast strong shadows across the displaced bumps
    sun_name = f"{object_name}_Sun"
    if sun_name not in bpy.data.objects:
        sun_data = bpy.data.lights.new(name=sun_name, type='SUN')
        sun_data.energy = 5.0
        
        sun_obj = bpy.data.objects.new(name=sun_name, object_data=sun_data)
        bpy.context.collection.objects.link(sun_obj)
        
        sun_obj.location = Vector(location) + Vector((0, 0, 10))
        # Angle the sun to highlight the displacement shadows
        sun_obj.rotation_euler = (math.radians(60), math.radians(30), 0)

    return f"Created highly subdivided '{object_name}' with procedural PBR displacement and a Sun light. Engine set to Cycles."
