def create_pbr_displacement_material(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Surface",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.2, 0.1),
    texture_scale: float = 3.0,
    displacement_strength: float = 0.1,
    **kwargs,
) -> str:
    """
    Create a highly detailed PBR surface demonstrating True Displacement and PBR mapping.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the object.
        material_color: (R, G, B) base color for the procedural brick/stone.
        texture_scale: Global scale for the mapping node.
        displacement_strength: Intensity of the actual physical displacement.
        
    Returns:
        Status string describing the created object.
    """
    import bpy
    from mathutils import Vector

    # Get scene context
    scene = bpy.data.scenes.get(scene_name)
    if not scene:
        scene = bpy.context.scene
        
    # === Step 1: Engine & Render Settings for True Displacement ===
    scene.render.engine = 'CYCLES'
    try:
        scene.cycles.feature_set = 'EXPERIMENTAL'
    except AttributeError:
        pass # Fallback if specific Blender version handles this differently

    # === Step 2: Create Base Geometry ===
    # Using a grid instead of a plane gives better baseline topology for displacement
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=20, y_subdivisions=20, size=2.0)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))

    # Add Subdivision Surface Modifier
    mod = obj.modifiers.new(name="Adaptive_Subdiv", type='SUBSURF')
    mod.subdivision_type = 'CATMULL_CLARK'
    try:
        mod.use_adaptive_subdivision = True
    except AttributeError:
        # Fallback for older/newer API where adaptive subdiv might be a scene/object prop
        pass 

    # === Step 3: Create PBR Material ===
    mat_name = f"{object_name}_Mat"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    # Enable True Displacement on Material
    mat.cycles.displacement_method = 'BOTH' # "Displacement and Bump"

    # === Step 4: Construct Shader Node Architecture ===
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Output & Shader
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1200, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (800, 0)
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    # True Displacement Node
    disp = nodes.new('ShaderNodeDisplacement')
    disp.location = (800, -300)
    disp.inputs['Midlevel'].default_value = 0.0
    disp.inputs['Scale'].default_value = displacement_strength
    links.new(disp.outputs['Displacement'], out_node.inputs['Displacement'])

    # Global Mapping Framework (Texture Coord -> Mapping)
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-400, 0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    
    val_node = nodes.new('ShaderNodeValue')
    val_node.location = (-600, -200)
    val_node.outputs[0].default_value = texture_scale
    links.new(val_node.outputs[0], mapping.inputs['Scale'])

    # Procedural Brick (Simulating Base Color and Height map)
    brick = nodes.new('ShaderNodeTexBrick')
    brick.location = (0, 100)
    brick.inputs['Color1'].default_value = (*material_color, 1.0)
    brick.inputs['Color2'].default_value = (material_color[0]*0.8, material_color[1]*0.8, material_color[2]*0.8, 1.0)
    links.new(mapping.outputs['Vector'], brick.inputs['Vector'])
    
    # Route Albedo (Color)
    links.new(brick.outputs['Color'], bsdf.inputs['Base Color'])
    
    # Route Height to Displacement (Grayscale)
    links.new(brick.outputs['Fac'], disp.inputs['Height'])

    # Procedural Noise (Simulating Roughness and Normal maps)
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (0, -200)
    noise.inputs['Scale'].default_value = 15.0
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])

    # Route Roughness (Grayscale map simulation via ColorRamp)
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (400, -100)
    ramp.color_ramp.elements[0].position = 0.3
    ramp.color_ramp.elements[0].color = (0.2, 0.2, 0.2, 1.0)
    ramp.color_ramp.elements[1].position = 0.7
    ramp.color_ramp.elements[1].color = (0.8, 0.8, 0.8, 1.0)
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], bsdf.inputs['Roughness'])

    # Route Normals (Vector map simulation via Bump Node)
    bump = nodes.new('ShaderNodeBump')
    bump.location = (400, -400)
    bump.inputs['Strength'].default_value = 0.4
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    
    # Ensure smooth shading on the generated geometry
    bpy.ops.object.shade_smooth()

    return f"Created '{object_name}' PBR architecture at {location} with True Displacement enabled (Cycles Experimental)."
