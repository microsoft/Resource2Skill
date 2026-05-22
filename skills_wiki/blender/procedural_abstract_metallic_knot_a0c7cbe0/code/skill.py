def create_object(
    scene_name: str = "Scene",
    object_name: str = "AbstractKnot",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.4, 0.9),  # Vibrant Blue
    **kwargs,
) -> str:
    """
    Create a procedural abstract twisted knot in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created knot object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) primary bright color for the procedural material.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    import colorsys
    from mathutils import Vector

    # Get target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    # Add a relatively high-poly torus to support smooth deformation
    bpy.ops.mesh.primitive_torus_add(
        major_segments=128, 
        minor_segments=64, 
        major_radius=1.0, 
        minor_radius=0.35,
        location=location
    )
    obj = bpy.context.active_object
    obj.name = object_name
    
    # Enable Smooth Shading
    for poly in obj.data.polygons:
        poly.use_smooth = True

    # === Step 2: Apply Modifier Stack ===
    # 1. Subdivision Surface for perfect smoothness
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # 2. First Twist (X Axis) - Creates the infinity loop
    twist_x = obj.modifiers.new(name="Twist_X", type='SIMPLE_DEFORM')
    twist_x.deform_method = 'TWIST'
    twist_x.angle = math.radians(360)
    twist_x.deform_axis = 'X'

    # 3. Second Twist (Y Axis) - Warps the loop into 3D space
    twist_y = obj.modifiers.new(name="Twist_Y", type='SIMPLE_DEFORM')
    twist_y.deform_method = 'TWIST'
    twist_y.angle = math.radians(-360)
    twist_y.deform_axis = 'Y'

    # 4. Third Twist (Z Axis) - Tightens the overall knot
    twist_z = obj.modifiers.new(name="Twist_Z", type='SIMPLE_DEFORM')
    twist_z.deform_method = 'TWIST'
    twist_z.angle = math.radians(360)
    twist_z.deform_axis = 'Z'

    # === Step 3: Build Procedural Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Output Node
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (300, 0)

    # Principled BSDF
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    # Handle API change for Base Color in newer Blender versions vs old
    base_color_input = bsdf.inputs.get("Base Color") or bsdf.inputs[0]
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = 0.2

    # Calculate a darker, saturated version of the input color for the crevices
    r, g, b = material_color[:3]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    dark_r, dark_g, dark_b = colorsys.hsv_to_rgb(h, min(1.0, s * 1.2), v * 0.15)

    # Color Ramp
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (-300, 0)
    color_ramp.color_ramp.elements[0].color = (dark_r, dark_g, dark_b, 1.0)
    color_ramp.color_ramp.elements[0].position = 0.35
    color_ramp.color_ramp.elements[1].color = (r, g, b, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.65

    # Base Noise Texture
    noise_main = nodes.new(type='ShaderNodeTexNoise')
    noise_main.location = (-500, 0)
    noise_main.inputs['Scale'].default_value = 5.0
    noise_main.inputs['Detail'].default_value = 4.0

    # Domain Warping Noise (acts like Musgrave distortion)
    noise_warp = nodes.new(type='ShaderNodeTexNoise')
    noise_warp.location = (-700, 0)
    noise_warp.inputs['Scale'].default_value = 3.0
    noise_warp.inputs['Detail'].default_value = 2.0

    # Link nodes
    links.new(noise_warp.outputs['Color'], noise_main.inputs['Vector'])
    links.new(noise_main.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], base_color_input)
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Assign material
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    # === Step 4: Finalize Scale ===
    obj.scale = (scale, scale, scale)
    
    # Ensure it updates in viewport
    bpy.context.view_layer.update()

    return f"Created '{object_name}' abstract knot at {location}."
