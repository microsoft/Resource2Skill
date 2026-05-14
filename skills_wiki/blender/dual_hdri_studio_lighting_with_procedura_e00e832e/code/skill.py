def create_object(
    scene_name: str = "Scene",
    object_name: str = "Dual_HDRI_Lighting",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.4, 0.8), # Deep Blue Tint
    **kwargs,
) -> str:
    """
    Create a Dual HDRI World Lighting setup with a procedurally tinted rim light.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the World data block and showcase objects.
        location: (x, y, z) world-space position for the showcase objects.
        scale: Uniform scale factor for showcase objects.
        material_color: (R, G, B) color used to tint the secondary HDRI.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Create Showcase Geometry ===
    # A floor and a subject to visualize the reflections and rim lighting
    bpy.ops.mesh.primitive_plane_add(size=10 * scale, location=location)
    plane = bpy.context.active_object
    plane.name = f"{object_name}_Ground"
    
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=64, ring_count=32, 
        radius=1 * scale, 
        location=(location[0], location[1], location[2] + (1 * scale))
    )
    sphere = bpy.context.active_object
    sphere.name = f"{object_name}_Subject"
    bpy.ops.object.shade_smooth()
    
    # Showcase Material
    mat = bpy.data.materials.new(name=f"{object_name}_Glossy_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = 0.15
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1.0)
    
    plane.data.materials.append(mat)
    sphere.data.materials.append(mat)
    
    # === Step 2: Build World Node Tree ===
    world = bpy.data.worlds.new(name=object_name)
    scene.world = world
    world.use_nodes = True
    tree = world.node_tree
    tree.nodes.clear()
    
    out_node = tree.nodes.new(type="ShaderNodeOutputWorld")
    out_node.location = (800, 0)
    
    bg_node = tree.nodes.new(type="ShaderNodeBackground")
    bg_node.location = (600, 0)
    
    # Helper to find color sockets for the new Blender 3.4+ Mix node
    def get_color_sockets(node):
        return [inp for inp in node.inputs if inp.type == 'RGBA']
        
    # Robust node creation handling Blender API version changes
    try:
        add_node = tree.nodes.new(type="ShaderNodeMix")
        add_node.data_type = 'RGBA'
        add_node.blend_type = 'ADD'
        add_fac = add_node.inputs[0]
        add_in1 = get_color_sockets(add_node)[0]
        add_in2 = get_color_sockets(add_node)[1]
        add_out = add_node.outputs[0]
        
        tint_node = tree.nodes.new(type="ShaderNodeMix")
        tint_node.data_type = 'RGBA'
        tint_node.blend_type = 'COLOR'
        tint_fac = tint_node.inputs[0]
        tint_in1 = get_color_sockets(tint_node)[0]
        tint_in2 = get_color_sockets(tint_node)[1]
        tint_out = tint_node.outputs[0]
    except RuntimeError:
        # Fallback for Blender 3.3 and older
        add_node = tree.nodes.new(type="ShaderNodeMixRGB")
        add_node.blend_type = 'ADD'
        add_fac = add_node.inputs[0]
        add_in1 = add_node.inputs[1]
        add_in2 = add_node.inputs[2]
        add_out = add_node.outputs[0]
        
        tint_node = tree.nodes.new(type="ShaderNodeMixRGB")
        tint_node.blend_type = 'COLOR'
        tint_fac = tint_node.inputs[0]
        tint_in1 = tint_node.inputs[1]
        tint_in2 = tint_node.inputs[2]
        tint_out = tint_node.outputs[0]

    add_node.location = (400, 0)
    tint_node.location = (200, -200)

    env1 = tree.nodes.new(type="ShaderNodeTexEnvironment")
    env1.location = (0, 100)
    
    env2 = tree.nodes.new(type="ShaderNodeTexEnvironment")
    env2.location = (0, -200)
    
    map1 = tree.nodes.new(type="ShaderNodeMapping")
    map1.location = (-200, 100)
    
    map2 = tree.nodes.new(type="ShaderNodeMapping")
    map2.location = (-200, -200)
    # Rotate the second HDRI to cast light from the opposite side
    map2.inputs['Rotation'].default_value[2] = math.radians(140)
    
    tex_coord = tree.nodes.new(type="ShaderNodeTexCoord")
    tex_coord.location = (-400, 0)
    
    # Create internal placeholder images (Users should replace these with real .exr files)
    img1 = bpy.data.images.new("Placeholder_Key_HDRI", width=128, height=128)
    img1.generated_color = (1.0, 0.9, 0.8, 1.0)
    env1.image = img1
    
    img2 = bpy.data.images.new("Placeholder_Fill_HDRI", width=128, height=128)
    img2.generated_color = (0.5, 0.5, 0.5, 1.0)
    env2.image = img2
    
    # Configure mix and tint logic
    add_fac.default_value = 0.6  # How much of the rim light is added to the scene
    tint_fac.default_value = 1.0 # 100% Color Blend
    tint_in2.default_value = (*material_color, 1.0) # Apply the Tint Color
    
    # === Step 3: Wire Connections ===
    tree.links.new(tex_coord.outputs['Generated'], map1.inputs['Vector'])
    tree.links.new(tex_coord.outputs['Generated'], map2.inputs['Vector'])
    
    tree.links.new(map1.outputs['Vector'], env1.inputs['Vector'])
    tree.links.new(map2.outputs['Vector'], env2.inputs['Vector'])
    
    tree.links.new(env1.outputs['Color'], add_in1)          # Base Key Light
    
    tree.links.new(env2.outputs['Color'], tint_in1)         # Secondary Rim Light
    tree.links.new(tint_out, add_in2)                       # Pass tinted Rim Light to Add Node
    
    tree.links.new(add_out, bg_node.inputs['Color'])        # Combine
    tree.links.new(bg_node.outputs['Background'], out_node.inputs['Surface'])
    
    # Auto-switch viewport to Rendered mode to see the lighting
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'RENDERED'
    
    return f"Created '{object_name}' at {location} with 2 showcase objects and Dual HDRI world lighting setup."
