def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Metal_Prop",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.6, 0.6),
    **kwargs,
) -> str:
    """
    Create a Beveled Metal Prop with a fully procedural PBR grunge material.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the metal.
        **kwargs: Overrides for metallic, grunge_scale, or bump_strength.

    Returns:
        Status string describing the creation.
    """
    import bpy
    from mathutils import Vector

    # Ensure we are in the correct scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Enable Screen Space Reflections for Eevee (Crucial for metals as noted in tutorial)
    if scene.render.engine == 'BLENDER_EEVEE':
        scene.eevee.use_ssr = True

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = Vector((scale, scale, scale))

    # Add bevel to catch specular highlights realistically
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.05 * scale
    bevel.segments = 4
    
    bpy.ops.object.shade_smooth()

    # === Step 2: Build Procedural PBR Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes to rebuild cleanly
    for node in nodes:
        nodes.remove(node)

    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (800, 0)

    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (400, 0)
    links.new(bsdf.outputs['BSDF'], output_node.inputs['Surface'])

    # Set Base Properties (Handles Blender 3.x and 4.0+ socket naming)
    if 'Base Color' in bsdf.inputs: 
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
    else: 
        bsdf.inputs[0].default_value = (*material_color, 1.0)
        
    # Force Metallic behavior
    if 'Metallic' in bsdf.inputs:
        bsdf.inputs['Metallic'].default_value = kwargs.get('metallic', 1.0)
    else:
        # Blender 4.0 renamed Metallic -> Metallic
        bsdf.inputs[1].default_value = kwargs.get('metallic', 1.0)

    # Procedural Noise for Imperfections (Substituting Image Maps)
    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.location = (-400, 0)
    noise.inputs['Scale'].default_value = kwargs.get('grunge_scale', 8.0)
    noise.inputs['Detail'].default_value = 15.0
    noise.inputs['Roughness'].default_value = 0.6

    # Color Ramp for Roughness Mapping (Black = Shiny, White = Rough)
    ramp = nodes.new(type='ShaderNodeValToRGB')
    ramp.location = (0, 100)
    
    # Tweak sliders to create contrast between shiny metal and dull smudges
    ramp.color_ramp.elements[0].position = 0.3
    ramp.color_ramp.elements[0].color = (0.15, 0.15, 0.15, 1.0) 
    ramp.color_ramp.elements[1].position = 0.7
    ramp.color_ramp.elements[1].color = (0.5, 0.5, 0.5, 1.0)    

    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], bsdf.inputs['Roughness'])

    # Bump Node for Micro-surface Detail
    bump = nodes.new(type='ShaderNodeBump')
    bump.location = (0, -200)
    # Keep distance intentionally small to avoid fake-looking depth
    bump.inputs['Distance'].default_value = 0.05 
    bump.inputs['Strength'].default_value = kwargs.get('bump_strength', 0.2)
    
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    # Assign material to the object
    obj.data.materials.append(mat)

    return f"Created '{object_name}' at {location} with Procedural PBR Metal material."
