def create_object(
    scene_name: str = "Scene",
    object_name: str = "Stylized_Asset",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.4, 0.2, 0.8, 1.0), # Default Stylized Purple
    **kwargs,
) -> str:
    """
    Create a Stylized Anime Object using the Real-Fake Shadow & Edge Highlight pattern.
    Must be rendered in EEVEE.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    # Step 0: Ensure Scene & EEVEE Engine
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    scene.render.engine = 'BLENDER_EEVEE'
    
    # Ensure there is at least one light in the scene for the shaders to react to
    if not any(obj.type == 'LIGHT' for obj in scene.objects):
        bpy.ops.object.light_add(type='SUN', location=(5, -5, 5))
        scene.objects.active.data.energy = 2.0

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_cube_add(size=2)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # === Step 2: Geometry Nodes for Edge Angle Extraction ===
    geo_group = bpy.data.node_groups.new(name="EdgeAngleGen", type='GeometryNodeTree')
    
    # Handle version differences for Geometry Node Interface (Blender 4.0+ vs 3.x)
    if hasattr(geo_group, "interface"): 
        geo_group.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        geo_group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
        geo_group.interface.new_socket(name="Unsigned Angle", in_out='OUTPUT', socket_type='NodeSocketFloat')
    else: 
        geo_group.inputs.new('NodeSocketGeometry', "Geometry")
        geo_group.outputs.new('NodeSocketGeometry', "Geometry")
        geo_group.outputs.new('NodeSocketFloat', "Unsigned Angle")

    in_node = geo_group.nodes.new('NodeGroupInput')
    out_node = geo_group.nodes.new('NodeGroupOutput')
    angle_node = geo_group.nodes.new('GeometryNodeInputMeshEdgeAngle')

    geo_group.links.new(in_node.outputs[0], out_node.inputs[0])
    # Link Unsigned Angle to Output
    geo_group.links.new(angle_node.outputs['Unsigned Angle'], out_node.inputs[1])

    geo_mod = obj.modifiers.new(name="Edge Data", type='NODES')
    geo_mod.node_group = geo_group

    # Dynamically find the internal output identifier to map the attribute
    out_identifier = None
    if hasattr(geo_group, "interface"):
        for item in geo_group.interface.items_tree:
            if item.name == "Unsigned Angle":
                out_identifier = item.identifier
                break
    else:
        for out in geo_group.outputs:
            if out.name == "Unsigned Angle":
                out_identifier = out.identifier
                break
    
    if out_identifier:
        geo_mod[out_identifier + "_attribute_name"] = "edge"

    # === Step 3: Add Bevel Modifier for Highlight Surface ===
    bev_mod = obj.modifiers.new(name="Smooth Corners", type='BEVEL')
    bev_mod.limit_method = 'ANGLE'
    bev_mod.width = 0.05 * scale
    bev_mod.segments = 3

    # === Step 4: Build Stylized Material (The "Comfee" Shader) ===
    mat = bpy.data.materials.new(name="StylizedAnimeMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create Material Nodes
    node_out = nodes.new('ShaderNodeOutputMaterial')
    node_out.location = (1600, 0)
    
    node_emiss = nodes.new('ShaderNodeEmission')
    node_emiss.location = (1400, 0)
    links.new(node_emiss.outputs[0], node_out.inputs[0])

    # -- Base Procedural Texture --
    tex_noise = nodes.new('ShaderNodeTexNoise')
    tex_noise.location = (0, 200)
    tex_noise.inputs['Scale'].default_value = 5.0

    ramp_base = nodes.new('ShaderNodeValToRGB')
    ramp_base.location = (200, 200)
    ramp_base.color_ramp.elements[0].color = (0.05, 0.05, 0.05, 1.0)
    ramp_base.color_ramp.elements[1].color = material_color
    links.new(tex_noise.outputs['Fac'], ramp_base.inputs['Fac'])

    # -- Tip 1: Real-Fake Shadow Mix (Diffuse -> S2RGB) --
    bsdf_diff = nodes.new('ShaderNodeBsdfDiffuse')
    bsdf_diff.location = (0, -100)
    
    s2rgb_diff = nodes.new('ShaderNodeShaderToRGB')
    s2rgb_diff.location = (200, -100)
    links.new(bsdf_diff.outputs['BSDF'], s2rgb_diff.inputs['Shader'])

    mix_shadow = nodes.new('ShaderNodeMix')
    mix_shadow.location = (500, 100)
    mix_shadow.data_type = 'RGBA'
    mix_shadow.blend_type = 'MULTIPLY'
    mix_shadow.inputs[0].default_value = 0.65 # Factor
    links.new(ramp_base.outputs['Color'], mix_shadow.inputs['A'])
    links.new(s2rgb_diff.outputs['Color'], mix_shadow.inputs['B'])

    # -- Tip 3: Environment Integration (Glossy -> S2RGB) --
    bsdf_glossy = nodes.new('ShaderNodeBsdfGlossy')
    bsdf_glossy.location = (0, -300)
    bsdf_glossy.inputs['Roughness'].default_value = 0.4
    
    s2rgb_glossy = nodes.new('ShaderNodeShaderToRGB')
    s2rgb_glossy.location = (200, -300)
    links.new(bsdf_glossy.outputs['BSDF'], s2rgb_glossy.inputs['Shader'])

    ramp_glossy = nodes.new('ShaderNodeValToRGB')
    ramp_glossy.location = (400, -300)
    ramp_glossy.color_ramp.elements[1].color = (0.5, 0.5, 0.5, 1.0) # Grey to tame highlight
    links.new(s2rgb_glossy.outputs['Color'], ramp_glossy.inputs['Fac'])

    mix_glossy = nodes.new('ShaderNodeMix')
    mix_glossy.location = (800, 0)
    mix_glossy.data_type = 'RGBA'
    mix_glossy.blend_type = 'OVERLAY'
    mix_glossy.inputs[0].default_value = 0.35 # Factor
    links.new(mix_shadow.outputs['Result'], mix_glossy.inputs['A'])
    links.new(ramp_glossy.outputs['Color'], mix_glossy.inputs['B'])

    # -- Tip 2: Highlighted Edges (GeoNode Attribute 'edge') --
    attr_edge = nodes.new('ShaderNodeAttribute')
    attr_edge.location = (700, 300)
    attr_edge.attribute_name = "edge"

    ramp_edge = nodes.new('ShaderNodeValToRGB')
    ramp_edge.location = (900, 300)
    ramp_edge.color_ramp.interpolation = 'LINEAR'
    ramp_edge.color_ramp.elements[0].position = 0.14
    ramp_edge.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp_edge.color_ramp.elements[1].position = 0.15 # Strict threshold for sharp edges
    ramp_edge.color_ramp.elements[1].color = (1, 1, 1, 1)
    links.new(attr_edge.outputs['Fac'], ramp_edge.inputs['Fac'])

    mix_edge = nodes.new('ShaderNodeMix')
    mix_edge.location = (1200, 100)
    mix_edge.data_type = 'RGBA'
    mix_edge.blend_type = 'MIX'
    mix_edge.inputs['B'].default_value = (1.0, 1.0, 1.0, 1.0) # Pure white highlight
    links.new(ramp_edge.outputs['Color'], mix_edge.inputs[0]) # Factor
    links.new(mix_glossy.outputs['Result'], mix_edge.inputs['A'])

    # Final connect to Emission
    links.new(mix_edge.outputs['Result'], node_emiss.inputs['Color'])

    # Assign material to object
    obj.data.materials.append(mat)

    return f"Created '{object_name}' at {location} with Cel-Shaded Anime material and Edge Geometry Node."
