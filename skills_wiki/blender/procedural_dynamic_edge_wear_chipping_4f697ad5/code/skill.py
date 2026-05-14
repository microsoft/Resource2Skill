def create_procedural_edge_wear(
    scene_name: str = "Scene",
    object_name: str = "Procedural_Worn_Part",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.05, 0.05),
    **kwargs,
) -> str:
    """
    Create a hard-surface object with dynamic, procedural chipped edge wear.
    Requires Cycles render engine to calculate the Bevel shader node.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base paint color in 0-1 range.
        **kwargs: Additional options.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    # Get scene and ensure Cycles is active (MANDATORY for Bevel node)
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    scene.render.engine = 'CYCLES'

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add a physical bevel so there are nice edges for the light to catch
    mod_bevel = obj.modifiers.new(name="Geometry_Bevel", type='BEVEL')
    mod_bevel.segments = 4
    mod_bevel.width = 0.05 * scale

    # === Step 2: Build Procedural Edge Wear Material ===
    mat_name = f"{object_name}_Wear_Mat"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Clear default nodes

    # Create Core Nodes
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (1200, 0)

    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (900, 0)

    # Bevel Node 1: Sharp (Radius = 0)
    bev_zero = nodes.new(type='ShaderNodeBevel')
    bev_zero.location = (-300, 200)
    bev_zero.samples = 4
    bev_zero.inputs['Radius'].default_value = 0.0

    # Bevel Node 2: Worn (Radius driven by noise)
    bev_wear = nodes.new(type='ShaderNodeBevel')
    bev_wear.location = (-300, -200)
    bev_wear.samples = 8

    # Noise Texture to simulate scratches and paint chips
    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.location = (-900, -200)
    noise.inputs['Scale'].default_value = 15.0
    noise.inputs['Detail'].default_value = 15.0
    noise.inputs['Roughness'].default_value = 0.65
    noise.inputs['Distortion'].default_value = 0.2

    # Map Range to control the min/max radius of the wear
    radius_map = nodes.new(type='ShaderNodeMapRange')
    radius_map.location = (-600, -200)
    radius_map.inputs[1].default_value = 0.4 # From Min (Clips noise to create distinct chips)
    radius_map.inputs[2].default_value = 0.6 # From Max
    radius_map.inputs[3].default_value = 0.0 # To Min (Radius 0 = no wear)
    radius_map.inputs[4].default_value = 0.1 # To Max (Maximum wear radius)

    # Vector Math: Subtract Normals to find the edges
    vec_sub = nodes.new(type='ShaderNodeVectorMath')
    vec_sub.location = (0, 0)
    vec_sub.operation = 'SUBTRACT'

    # Vector Math: Length (Converts vector difference to a scalar mask)
    vec_len = nodes.new(type='ShaderNodeVectorMath')
    vec_len.location = (200, 0)
    vec_len.operation = 'LENGTH'

    # ColorRamp to sharpen the mask to harsh black/white (Paint vs Metal)
    mask_ramp = nodes.new(type='ShaderNodeValToRGB')
    mask_ramp.location = (400, 0)
    mask_ramp.color_ramp.interpolation = 'CONSTANT'
    mask_ramp.color_ramp.elements[0].position = 0.015
    mask_ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    mask_ramp.color_ramp.elements[1].position = 0.02
    mask_ramp.color_ramp.elements[1].color = (1, 1, 1, 1)

    # Color Mixing (Base Paint vs Exposed Edge Metal)
    mix_color = nodes.new(type='ShaderNodeMix')
    mix_color.location = (700, 200)
    mix_color.data_type = 'RGBA'
    mix_color.blend_type = 'MIX'
    # Ensure inputs exist dynamically based on Blender version 
    fac_idx, a_idx, b_idx = 0, 4, 5
    mix_color.inputs[a_idx].default_value = (*material_color, 1.0) # A: Paint color
    mix_color.inputs[b_idx].default_value = (0.8, 0.8, 0.8, 1.0)   # B: Exposed Silver Metal

    # Roughness Map (Paint is rough, Metal edges are shiny)
    rough_map = nodes.new(type='ShaderNodeMapRange')
    rough_map.location = (700, -200)
    rough_map.inputs[3].default_value = 0.5 # To Min (Paint Roughness)
    rough_map.inputs[4].default_value = 0.2 # To Max (Metal Roughness)

    # === Step 3: Link Everything Together ===
    # Drive Bevel Wear radius with Noise
    links.new(noise.outputs['Fac'], radius_map.inputs['Value'])
    links.new(radius_map.outputs['Result'], bev_wear.inputs['Radius'])

    # Calculate Edge Mask
    links.new(bev_zero.outputs['Normal'], vec_sub.inputs[0])
    links.new(bev_wear.outputs['Normal'], vec_sub.inputs[1])
    links.new(vec_sub.outputs['Vector'], vec_len.inputs[0])
    links.new(vec_len.outputs['Value'], mask_ramp.inputs['Fac'])

    # Route Mask to Material Properties
    links.new(mask_ramp.outputs['Color'], mix_color.inputs[fac_idx]) # Mix Color
    links.new(mask_ramp.outputs['Color'], bsdf.inputs['Metallic']) # Mask -> Metallic
    links.new(mask_ramp.outputs['Color'], rough_map.inputs['Value']) # Mask -> Roughness
    
    # Route to BSDF and Output
    links.new(mix_color.outputs['Result'], bsdf.inputs['Base Color'])
    links.new(rough_map.outputs['Result'], bsdf.inputs['Roughness'])
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    # Optional: Apply smooth shading
    for poly in obj.data.polygons:
        poly.use_smooth = True

    return f"Created '{object_name}' with procedural edge wear at {location}. (Note: View in Rendered Mode with CYCLES active)."
