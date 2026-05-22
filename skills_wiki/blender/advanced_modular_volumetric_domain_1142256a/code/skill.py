def create_custom_volumetric_domain(
    scene_name: str = "Scene",
    object_name: str = "Volumetric_Fog_Domain",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 10.0,
    scatter_color: tuple = (0.8, 0.9, 1.0),
    scatter_density: float = 0.02,
    anisotropy: float = 0.7,
    absorption_color: tuple = (1.0, 1.0, 1.0),
    absorption_density: float = 0.0,
    emission_color: tuple = (0.0, 0.0, 0.0),
    emission_strength: float = 0.0,
    **kwargs,
) -> str:
    """
    Creates a large bounding box with a modular, highly customizable volumetric material.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name of the domain object.
        location: (x, y, z) center of the domain.
        scale: Uniform scale. Larger scale means it covers more of the scene.
        scatter_color: (R, G, B) color of the scattered light (fog color).
        scatter_density: Thickness of the fog. Keep very low (0.01 - 0.05) for large scales!
        anisotropy: -1.0 to 1.0. High positive values scatter light forward (god rays).
        absorption_color: (R, G, B) color to absorb.
        absorption_density: Thickness of the absorption effect.
        emission_color: (R, G, B) color of glowing ambient fog.
        emission_strength: Brightness of the ambient fog.
        
    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (The Domain) ===
    bpy.ops.mesh.primitive_cube_add(size=2.0)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))

    # Crucial for volumetrics: set viewport display to bounds so it doesn't block vision
    obj.display_type = 'BOUNDS'

    # === Step 2: Build the Modular Volumetric Material ===
    mat_name = f"{object_name}_ModularVolMaterial"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Add necessary nodes
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (400, 0)

    # We use Add Shader nodes to mathematically combine the volume effects
    add_node_final = nodes.new(type='ShaderNodeAddShader')
    add_node_final.location = (200, 0)

    add_node_base = nodes.new(type='ShaderNodeAddShader')
    add_node_base.location = (0, 0)

    scatter_node = nodes.new(type='ShaderNodeVolumeScatter')
    scatter_node.location = (-250, 150)
    scatter_node.inputs['Color'].default_value = (*scatter_color, 1.0)
    scatter_node.inputs['Density'].default_value = scatter_density
    scatter_node.inputs['Anisotropy'].default_value = anisotropy

    absorp_node = nodes.new(type='ShaderNodeVolumeAbsorption')
    absorp_node.location = (-250, -50)
    absorp_node.inputs['Color'].default_value = (*absorption_color, 1.0)
    absorp_node.inputs['Density'].default_value = absorption_density

    emission_node = nodes.new(type='ShaderNodeEmission')
    emission_node.location = (-250, -250)
    emission_node.inputs['Color'].default_value = (*emission_color, 1.0)
    emission_node.inputs['Strength'].default_value = emission_strength

    # === Step 3: Link the Nodes ===
    # Link Scatter and Absorption together
    links.new(scatter_node.outputs['Volume'], add_node_base.inputs[0])
    links.new(absorp_node.outputs['Volume'], add_node_base.inputs[1])

    # Add Emission to the mix
    links.new(add_node_base.outputs['Shader'], add_node_final.inputs[0])
    links.new(emission_node.outputs['Emission'], add_node_final.inputs[1])

    # Connect to the Volume output (Surface must remain empty)
    links.new(add_node_final.outputs['Shader'], out_node.inputs['Volume'])

    # Ensure it's assigned to the scene collection
    if obj.name not in scene.collection.objects:
        scene.collection.objects.link(obj)

    return f"Created Volumetric Domain '{object_name}' at {location} with scale {scale}. Add lights to the scene to see the scattering effect."
