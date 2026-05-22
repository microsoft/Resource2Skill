def create_procedural_worn_metal(
    scene_name: str = "Scene",
    object_name: str = "WornProp",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    paint_color: tuple = (0.8, 0.4, 0.05) # Default Orange/Yellow
) -> str:
    """
    Creates a prop with a procedural edge-wear and dirt shader (Requires Cycles).
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        paint_color: (R, G, B) base color of the paint layer.
        
    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # -------------------------------------------------------------------------
    # Engine Check: The Bevel shader node requires Cycles to function properly.
    # -------------------------------------------------------------------------
    scene.render.engine = 'CYCLES'
    if hasattr(scene.cycles, 'device'):
        scene.cycles.device = 'GPU' # Attempt to use GPU if available

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_monkey_add(location=location, size=2.0)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Add modifiers to create interesting edges to wear down
    mod_subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    mod_subsurf.levels = 2
    mod_subsurf.render_levels = 3
    
    bpy.ops.object.shade_smooth()

    # === Step 2: Build Procedural Material ===
    mat_name = f"{object_name}_Mat_WornMetal"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Start fresh

    # --- Shaders ---
    # Metal Base
    bsdf_metal = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_metal.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1.0)
    bsdf_metal.inputs['Metallic'].default_value = 1.0
    bsdf_metal.inputs['Roughness'].default_value = 0.3
    bsdf_metal.location = (0, 300)

    # Paint Layer
    bsdf_paint = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_paint.inputs['Base Color'].default_value = (*paint_color, 1.0)
    bsdf_paint.inputs['Metallic'].default_value = 0.0
    bsdf_paint.inputs['Roughness'].default_value = 0.5
    bsdf_paint.location = (0, 0)

    # Dirt Layer
    bsdf_dirt = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_dirt.inputs['Base Color'].default_value = (0.15, 0.1, 0.05, 1.0) # Dark brown
    bsdf_dirt.inputs['Metallic'].default_value = 0.0
    bsdf_dirt.inputs['Roughness'].default_value = 0.95
    bsdf_dirt.location = (0, -300)

    # Mixers
    mix_damage = nodes.new('ShaderNodeMixShader')
    mix_damage.location = (300, 150)
    
    mix_dirt = nodes.new('ShaderNodeMixShader')
    mix_dirt.location = (500, 0)
    
    output_node = nodes.new('ShaderNodeOutputMaterial')
    output_node.location = (700, 0)

    # --- Edge Wear Mask (Bevel Difference) ---
    bev1 = nodes.new('ShaderNodeBevel')
    bev1.inputs['Radius'].default_value = 0.05
    bev1.location = (-1200, 600)
    
    bev2 = nodes.new('ShaderNodeBevel')
    bev2.inputs['Radius'].default_value = 0.002
    bev2.location = (-1200, 450)

    mix_bev = nodes.new('ShaderNodeMix')
    mix_bev.data_type = 'RGBA'
    mix_bev.blend_type = 'DIFFERENCE'
    mix_bev.inputs['Factor'].default_value = 1.0
    mix_bev.location = (-1000, 500)

    ramp_edge = nodes.new('ShaderNodeValToRGB')
    ramp_edge.color_ramp.elements[0].position = 0.0
    ramp_edge.color_ramp.elements[1].position = 0.03 # Crush difference
    ramp_edge.location = (-800, 500)

    # Break up edges with noise
    noise_edge = nodes.new('ShaderNodeTexNoise')
    noise_edge.inputs['Scale'].default_value = 15.0
    noise_edge.inputs['Detail'].default_value = 15.0
    noise_edge.location = (-1000, 200)

    ramp_noise_edge = nodes.new('ShaderNodeValToRGB')
    ramp_noise_edge.color_ramp.elements[0].position = 0.4
    ramp_noise_edge.color_ramp.elements[1].position = 0.6
    ramp_noise_edge.location = (-800, 200)

    mix_edge_final = nodes.new('ShaderNodeMix')
    mix_edge_final.data_type = 'RGBA'
    mix_edge_final.blend_type = 'MULTIPLY'
    mix_edge_final.inputs['Factor'].default_value = 1.0
    mix_edge_final.location = (-500, 350)

    # --- Scratches / Cracks Mask ---
    voronoi_crack = nodes.new('ShaderNodeTexVoronoi')
    voronoi_crack.feature = 'DISTANCE_TO_EDGE'
    voronoi_crack.inputs['Scale'].default_value = 8.0
    voronoi_crack.location = (-1000, -100)

    ramp_crack = nodes.new('ShaderNodeValToRGB')
    # Flip to make lines white on black background
    ramp_crack.color_ramp.elements[0].position = 0.0
    ramp_crack.color_ramp.elements[0].color = (1, 1, 1, 1)
    ramp_crack.color_ramp.elements[1].position = 0.03
    ramp_crack.color_ramp.elements[1].color = (0, 0, 0, 1)
    ramp_crack.location = (-800, -100)

    # Combine Edges and Cracks into unified Damage Mask
    mix_all_damage = nodes.new('ShaderNodeMix')
    mix_all_damage.data_type = 'RGBA'
    mix_all_damage.blend_type = 'ADD'
    mix_all_damage.inputs['Factor'].default_value = 1.0
    mix_all_damage.location = (-200, 150)

    # --- Dirt Mask ---
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1200, -500)

    mapping_dirt = nodes.new('ShaderNodeMapping')
    mapping_dirt.inputs['Rotation'].default_value = (0, math.radians(-90), 0)
    mapping_dirt.location = (-1000, -500)

    grad_dirt = nodes.new('ShaderNodeTexGradient')
    grad_dirt.gradient_type = 'LINEAR'
    grad_dirt.location = (-800, -500)

    noise_dirt = nodes.new('ShaderNodeTexNoise')
    noise_dirt.inputs['Scale'].default_value = 5.0
    noise_dirt.inputs['Detail'].default_value = 15.0
    noise_dirt.location = (-800, -700)

    mix_dirt_mask = nodes.new('ShaderNodeMix')
    mix_dirt_mask.data_type = 'RGBA'
    mix_dirt_mask.blend_type = 'ADD'
    mix_dirt_mask.inputs['Factor'].default_value = 0.5
    mix_dirt_mask.location = (-600, -550)

    ramp_dirt = nodes.new('ShaderNodeValToRGB')
    ramp_dirt.color_ramp.elements[0].position = 0.4
    ramp_dirt.color_ramp.elements[1].position = 0.6
    ramp_dirt.location = (-400, -550)

    # --- Bump Mapping ---
    bump = nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.5
    bump.inputs['Distance'].default_value = 0.1
    bump.invert = True # We want paint to sit higher than exposed metal
    bump.location = (-200, -100)

    # === Step 3: Link Everything Together ===
    # Shaders
    links.new(bsdf_metal.outputs[0], mix_damage.inputs[1])
    links.new(bsdf_paint.outputs[0], mix_damage.inputs[2])
    links.new(mix_damage.outputs[0], mix_dirt.inputs[1])
    links.new(bsdf_dirt.outputs[0], mix_dirt.inputs[2])
    links.new(mix_dirt.outputs[0], output_node.inputs[0])

    # Edge Mask Logic
    links.new(bev1.outputs['Normal'], mix_bev.inputs[6]) # A
    links.new(bev2.outputs['Normal'], mix_bev.inputs[7]) # B
    links.new(mix_bev.outputs[2], ramp_edge.inputs['Fac'])
    links.new(noise_edge.outputs['Fac'], ramp_noise_edge.inputs['Fac'])
    links.new(ramp_edge.outputs['Color'], mix_edge_final.inputs[6]) # A
    links.new(ramp_noise_edge.outputs['Color'], mix_edge_final.inputs[7]) # B

    # Cracks Logic
    links.new(voronoi_crack.outputs['Distance'], ramp_crack.inputs['Fac'])

    # Combine Damage
    links.new(mix_edge_final.outputs[2], mix_all_damage.inputs[6])
    links.new(ramp_crack.outputs['Color'], mix_all_damage.inputs[7])
    
    # Drive Damage Mix Shader & Bump
    links.new(mix_all_damage.outputs[2], mix_damage.inputs['Fac'])
    links.new(mix_all_damage.outputs[2], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf_paint.inputs['Normal'])
    links.new(bump.outputs['Normal'], bsdf_metal.inputs['Normal'])

    # Dirt Mask Logic
    links.new(tex_coord.outputs['Object'], mapping_dirt.inputs['Vector'])
    links.new(mapping_dirt.outputs['Vector'], grad_dirt.inputs['Vector'])
    links.new(grad_dirt.outputs['Color'], mix_dirt_mask.inputs[6])
    links.new(noise_dirt.outputs['Color'], mix_dirt_mask.inputs[7])
    links.new(mix_dirt_mask.outputs[2], ramp_dirt.inputs['Fac'])
    
    # Drive Dirt Mix Shader
    links.new(ramp_dirt.outputs['Color'], mix_dirt.inputs['Fac'])

    return f"Created '{object_name}' with procedural edge wear at {location}. Switch to Rendered View in Cycles to view."
