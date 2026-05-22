def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Material_Template",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.25, 0.15),  # Base color for the procedural stone/brick
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with a fully routed PBR Material Template.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the material.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface modifier for true displacement
    subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.levels = 4
    subdiv.render_levels = 4

    # === Step 2: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)

    # Enable Displacement & Bump for Cycles (Ignored in Eevee)
    mat.cycles.displacement_method = 'BOTH'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create Core Nodes
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = (1200, 0)

    node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_bsdf.location = (800, 0)
    links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])

    # Coordinates and Global Mapping
    node_tc = nodes.new(type='ShaderNodeTexCoord')
    node_tc.location = (-1000, 0)

    node_mapping = nodes.new(type='ShaderNodeMapping')
    node_mapping.location = (-800, 0)
    links.new(node_tc.outputs['UV'], node_mapping.inputs['Vector'])

    # Global Scale Control (Value Node)
    node_scale_val = nodes.new(type='ShaderNodeValue')
    node_scale_val.name = "Global Scale"
    node_scale_val.label = "Global Scale"
    node_scale_val.outputs[0].default_value = 5.0
    node_scale_val.location = (-1000, -200)
    links.new(node_scale_val.outputs[0], node_mapping.inputs['Scale'])

    # Procedural Texture Source (Acts as our image maps)
    node_tex = nodes.new(type='ShaderNodeTexVoronoi')
    node_tex.location = (-600, 0)
    links.new(node_mapping.outputs['Vector'], node_tex.inputs['Vector'])

    # Reroute Node (Demonstrating clean noodle management)
    node_reroute = nodes.new(type='NodeReroute')
    node_reroute.location = (-400, -50)
    links.new(node_tex.outputs['Distance'], node_reroute.inputs[0])

    # 1. Base Color Pipeline (Color Map -> HSV -> Base Color)
    node_colorramp = nodes.new(type='ShaderNodeValToRGB')
    node_colorramp.location = (-200, 200)
    node_colorramp.color_ramp.elements[0].position = 0.0
    node_colorramp.color_ramp.elements[0].color = (0.02, 0.02, 0.02, 1.0) # Dark cracks
    node_colorramp.color_ramp.elements[1].position = 0.15
    node_colorramp.color_ramp.elements[1].color = (*material_color, 1.0)  # Primary color
    links.new(node_reroute.outputs[0], node_colorramp.inputs['Fac'])

    node_hsv = nodes.new(type='ShaderNodeHueSaturation')
    node_hsv.location = (200, 200)
    node_hsv.inputs['Saturation'].default_value = 0.9
    links.new(node_colorramp.outputs['Color'], node_hsv.inputs['Color'])
    links.new(node_hsv.outputs['Color'], node_bsdf.inputs['Base Color'])

    # 2. Roughness Pipeline (Gloss Map -> Invert -> Roughness)
    node_invert = nodes.new(type='ShaderNodeInvert')
    node_invert.location = (200, 0)
    links.new(node_reroute.outputs[0], node_invert.inputs['Color'])
    links.new(node_invert.outputs['Color'], node_bsdf.inputs['Roughness'])

    # 3. Normal Pipeline (Height Map -> Bump -> Normal)
    node_bump = nodes.new(type='ShaderNodeBump')
    node_bump.location = (200, -200)
    node_bump.inputs['Strength'].default_value = 0.75
    node_bump.inputs['Distance'].default_value = 0.1
    links.new(node_reroute.outputs[0], node_bump.inputs['Height'])
    links.new(node_bump.outputs['Normal'], node_bsdf.inputs['Normal'])

    # 4. Displacement Pipeline (Displacement Map -> Displacement -> Output)
    node_disp = nodes.new(type='ShaderNodeDisplacement')
    node_disp.location = (800, -400)
    node_disp.inputs['Midlevel'].default_value = 0.0  # Tutorial specifically emphasizes 0.0
    node_disp.inputs['Scale'].default_value = 0.1     # Tutorial specifically emphasizes 0.1
    links.new(node_reroute.outputs[0], node_disp.inputs['Height'])
    links.new(node_disp.outputs['Displacement'], node_output.inputs['Displacement'])

    return f"Created '{object_name}' with a complete procedural PBR Material routing network at {location}."
