def create_procedural_abstract_loop(
    scene_name: str = "Scene",
    object_name: str = "AbstractGeoLoop",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.3, 1.0), # Purple glow
    **kwargs,
) -> str:
    """
    Create a procedurally animated, abstract geometric loop using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) color for the glowing crevices.

    Returns:
        Status string.
    """
    import bpy
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Eevee Render Settings for Visual Fidelity ===
    scene.render.engine = 'BLENDER_EEVEE_NEXT' if bpy.app.version >= (4, 2, 0) else 'BLENDER_EEVEE'
    if hasattr(scene.eevee, "use_gtao"): scene.eevee.use_gtao = True
    if hasattr(scene.eevee, "use_bloom"): scene.eevee.use_bloom = True
    if hasattr(scene.eevee, "use_ssr"): scene.eevee.use_ssr = True
    scene.render.film_transparent = True
    scene.view_settings.look = 'Very High Contrast'
    
    # Set animation loop length
    scene.frame_end = 100

    # === Step 2: Create Base Object ===
    mesh = bpy.data.meshes.new(name=object_name)
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    obj.location = location
    obj.scale = (scale, scale, scale)

    # === Step 3: Material Setup (AO-Driven Crevice Glow) ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (600, 0)

    mix_shader = nodes.new('ShaderNodeMixShader')
    mix_shader.location = (400, 0)
    links.new(mix_shader.outputs[0], out_node.inputs['Surface'])

    # Metallic Base
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (100, -200)
    principled.inputs['Metallic'].default_value = 1.0
    principled.inputs['Roughness'].default_value = 0.0
    links.new(principled.outputs['BSDF'], mix_shader.inputs[2])

    # Emission Core
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (100, 100)
    emission.inputs['Strength'].default_value = 7.4
    links.new(emission.outputs['Emission'], mix_shader.inputs[1])

    # AO 1 -> Emission Color
    ao1 = nodes.new('ShaderNodeAmbientOcclusion')
    ao1.location = (-500, 100)

    cr1 = nodes.new('ShaderNodeValToRGB')
    cr1.location = (-200, 100)
    cr1.color_ramp.elements[0].position = 0.2
    cr1.color_ramp.elements[0].color = (0, 0, 0, 1.0)
    cr1.color_ramp.elements[1].position = 0.8
    cr1.color_ramp.elements[1].color = (*material_color, 1.0) # Apply dynamic color
    links.new(ao1.outputs['Color'], cr1.inputs['Fac'])
    links.new(cr1.outputs['Color'], emission.inputs['Color'])

    # AO 2 (Inside) -> Mix Factor
    ao2 = nodes.new('ShaderNodeAmbientOcclusion')
    ao2.location = (-500, 400)
    ao2.inside = True

    cr2 = nodes.new('ShaderNodeValToRGB')
    cr2.location = (-200, 400)
    cr2.color_ramp.elements[0].position = 0.0
    cr2.color_ramp.elements[0].color = (1, 1, 1, 1) # Flipped
    cr2.color_ramp.elements[1].position = 1.0
    cr2.color_ramp.elements[1].color = (0, 0, 0, 1)
    links.new(ao2.outputs['Color'], cr2.inputs['Fac'])
    links.new(cr2.outputs['Color'], mix_shader.inputs['Fac'])

    # === Step 4: Geometry Nodes Setup ===
    mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
    group = bpy.data.node_groups.new(name=f"{object_name}_GeoNodes", type='GeometryNodeTree')
    mod.node_group = group
    gn_nodes = group.nodes
    gn_links = group.links

    # Setup Output Socket
    group_out = gn_nodes.new('NodeGroupOutput')
    group_out.location = (1200, 0)
    if bpy.app.version >= (4, 0, 0):
        group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        group.outputs.new('NodeSocketGeometry', 'Geometry')

    # Main Flow Nodes
    grid = gn_nodes.new('GeometryNodeMeshGrid')
    grid.location = (-1000, 0)
    grid.inputs['Size X'].default_value = 35.0
    grid.inputs['Size Y'].default_value = 35.0
    grid.inputs['Vertices X'].default_value = 100
    grid.inputs['Vertices Y'].default_value = 100

    tri = gn_nodes.new('GeometryNodeTriangulate')
    tri.location = (-800, 0)

    scale_el = gn_nodes.new('GeometryNodeScaleElements')
    scale_el.location = (-600, 0)
    scale_el.inputs['Scale'].default_value = 0.8 

    set_pos = gn_nodes.new('GeometryNodeSetPosition')
    set_pos.location = (-400, 0)

    extrude = gn_nodes.new('GeometryNodeExtrudeMesh')
    extrude.location = (-200, 0)
    if 'Individual' in extrude.inputs:
        extrude.inputs['Individual'].default_value = True

    transform = gn_nodes.new('GeometryNodeTransform')
    transform.location = (0, 0)
    
    # Animate Transform (Looping 180 degrees over 100 frames)
    transform.inputs['Rotation'].default_value = (0, 0, 0)
    transform.inputs['Rotation'].keyframe_insert(data_path="default_value", frame=1)
    transform.inputs['Rotation'].default_value = (0, 0, math.pi)
    transform.inputs['Rotation'].keyframe_insert(data_path="default_value", frame=100)
    
    # Ensure linear interpolation for seamless loop
    if group.animation_data and group.animation_data.action:
        for fcurve in group.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'

    set_mat = gn_nodes.new('GeometryNodeSetMaterial')
    set_mat.location = (200, 0)
    set_mat.inputs['Material'].default_value = mat

    # Main Link Connections
    gn_links.new(grid.outputs['Mesh'], tri.inputs['Mesh'])
    gn_links.new(tri.outputs['Mesh'], scale_el.inputs['Geometry'])
    gn_links.new(scale_el.outputs['Geometry'], set_pos.inputs['Geometry'])
    gn_links.new(set_pos.outputs['Geometry'], extrude.inputs['Mesh'])
    gn_links.new(extrude.outputs['Mesh'], transform.inputs['Geometry'])
    gn_links.new(transform.outputs['Geometry'], set_mat.inputs['Geometry'])
    gn_links.new(set_mat.outputs['Geometry'], group_out.inputs[0])

    # === Step 5: Vector Math Displacement Logic ===
    pos = gn_nodes.new('GeometryNodeInputPosition')
    pos.location = (-1000, -300)
    
    norm = gn_nodes.new('GeometryNodeInputNormal')
    norm.location = (-1000, -400)
    
    noise = gn_nodes.new('ShaderNodeTexNoise')
    noise.location = (-1000, -600)
    noise.inputs['Scale'].default_value = 0.2
    noise.inputs['Detail'].default_value = 15.0

    vm_add_pos = gn_nodes.new('ShaderNodeVectorMath')
    vm_add_pos.operation = 'ADD'
    vm_add_pos.location = (-800, -300)
    gn_links.new(pos.outputs[0], vm_add_pos.inputs[0])
    gn_links.new(norm.outputs[0], vm_add_pos.inputs[1])

    vm_norm_pos = gn_nodes.new('ShaderNodeVectorMath')
    vm_norm_pos.operation = 'NORMALIZE'
    vm_norm_pos.location = (-600, -300)
    gn_links.new(vm_add_pos.outputs[0], vm_norm_pos.inputs[0])

    vm_add_noise = gn_nodes.new('ShaderNodeVectorMath')
    vm_add_noise.operation = 'ADD'
    vm_add_noise.location = (-800, -500)
    gn_links.new(noise.outputs['Color'], vm_add_noise.inputs[0])
    gn_links.new(norm.outputs[0], vm_add_noise.inputs[1])

    vm_norm_noise = gn_nodes.new('ShaderNodeVectorMath')
    vm_norm_noise.operation = 'NORMALIZE'
    vm_norm_noise.location = (-600, -500)
    gn_links.new(vm_add_noise.outputs[0], vm_norm_noise.inputs[0])

    # Cross Product 1 -> Set Position Offset
    vm_cross1 = gn_nodes.new('ShaderNodeVectorMath')
    vm_cross1.operation = 'CROSS_PRODUCT'
    vm_cross1.location = (-400, -400)
    gn_links.new(vm_norm_noise.outputs[0], vm_cross1.inputs[0])
    gn_links.new(vm_norm_pos.outputs[0], vm_cross1.inputs[1])
    gn_links.new(vm_cross1.outputs[0], set_pos.inputs['Offset'])

    # Cross Product 2 -> Clamping -> Extrude Offset
    vm_cross2 = gn_nodes.new('ShaderNodeVectorMath')
    vm_cross2.operation = 'CROSS_PRODUCT'
    vm_cross2.location = (-200, -500)
    gn_links.new(vm_norm_noise.outputs[0], vm_cross2.inputs[0])
    gn_links.new(vm_cross1.outputs[0], vm_cross2.inputs[1])

    vm_min = gn_nodes.new('ShaderNodeVectorMath')
    vm_min.operation = 'MINIMUM'
    vm_min.location = (0, -500)
    vm_min.inputs[1].default_value = (0.07, 0.07, 0.07)
    gn_links.new(vm_cross2.outputs[0], vm_min.inputs[0])

    vm_max = gn_nodes.new('ShaderNodeVectorMath')
    vm_max.operation = 'MAXIMUM'
    vm_max.location = (200, -500)
    vm_max.inputs[1].default_value = (-0.5, -0.5, -0.5)
    gn_links.new(vm_min.outputs[0], vm_max.inputs[0])
    gn_links.new(vm_max.outputs[0], extrude.inputs['Offset'])

    return f"Created '{object_name}' with 100-frame looping animation at {location}"
