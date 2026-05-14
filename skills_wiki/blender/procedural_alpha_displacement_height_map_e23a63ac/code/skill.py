def create_alpha_displacement_surface(
    scene_name: str = "Scene",
    object_name: str = "AlphaDisplacedSurface",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.25, 0.4, 0.18),
    texture_type: str = 'SCALES', # Options: 'SCALES' or 'CRUMPLED'
    displacement_strength: float = 0.1,
    subdivision_level: int = 4,
    **kwargs
) -> str:
    """
    Create a procedural alpha-displaced surface mimicking sculpted height maps.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color in 0-1 range.
        texture_type: 'SCALES' (Voronoi distance) or 'CRUMPLED' (High-detail Noise).
        displacement_strength: How far the texture pushes the geometry.
        subdivision_level: Density of the mesh (higher = more detail, 4 is recommended).

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Create Base Geometry ===
    # Use a high-segment UV sphere to provide an excellent base for organic displacement
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.0)
    obj = bpy.context.active_object
    obj.name = object_name
    
    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))
    
    # === Step 2: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    
    if bsdf:
        # Handle API naming differences across Blender versions
        color_socket = bsdf.inputs.get('Base Color') or bsdf.inputs.get('Base_Color')
        if color_socket:
            color_socket.default_value = (*material_color, 1.0)
        
        roughness_socket = bsdf.inputs.get('Roughness')
        if roughness_socket:
            roughness_socket.default_value = 0.75 # High roughness for organic/dry look
            
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat
        
    # === Step 3: Geometry Nodes for Alpha Displacement ===
    modifier = obj.modifiers.new(name="AlphaDisplacement", type='NODES')
    node_tree = bpy.data.node_groups.new(name=f"{object_name}_GeoNodes", type='GeometryNodeTree')
    modifier.node_group = node_tree
    
    # Setup I/O Sockets (Compatible with both 3.x and 4.x APIs)
    if hasattr(node_tree, "interface"):
        node_tree.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        node_tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        node_tree.inputs.new('NodeSocketGeometry', "Geometry")
        node_tree.outputs.new('NodeSocketGeometry', "Geometry")
        
    input_node = node_tree.nodes.new("NodeGroupInput")
    output_node = node_tree.nodes.new("NodeGroupOutput")
    
    # Subdivide mesh to allow for micro-detail displacement
    subdiv_node = node_tree.nodes.new("GeometryNodeSubdivideMesh")
    subdiv_node.inputs['Level'].default_value = subdivision_level
    
    set_pos_node = node_tree.nodes.new("GeometryNodeSetPosition")
    smooth_node = node_tree.nodes.new("GeometryNodeSetShadeSmooth")
    
    # Get Vertex Normals
    normal_node = node_tree.nodes.new("GeometryNodeInputNormal")
    
    # Multiply Normal by the Height Map value
    vec_math_node = node_tree.nodes.new("ShaderNodeVectorMath")
    vec_math_node.operation = 'SCALE'
    scale_socket = vec_math_node.inputs.get('Scale') or vec_math_node.inputs[3]
    
    # Multiplier for overall strength
    strength_math = node_tree.nodes.new("ShaderNodeMath")
    strength_math.operation = 'MULTIPLY'
    strength_math.inputs[1].default_value = displacement_strength
    
    # --- Generate the Procedural "Alpha" Textures ---
    if texture_type.upper() == 'SCALES':
        # Voronoi Distance to Edge creates perfect interlocking scale/crack patterns
        tex_node = node_tree.nodes.new("ShaderNodeTexVoronoi")
        tex_node.feature = 'DISTANCE_TO_EDGE'
        
        scale_input = tex_node.inputs.get('Scale') or tex_node.inputs[2]
        scale_input.default_value = 12.0
        
        # Link texture output 'Distance' to strength multiplier
        node_tree.links.new(tex_node.outputs[0], strength_math.inputs[0])
        
    else: 
        # CRUMPLED / BARK: High frequency noise mimics paper creases or bark
        tex_node = node_tree.nodes.new("ShaderNodeTexNoise")
        
        scale_input = tex_node.inputs.get('Scale') or tex_node.inputs[2]
        scale_input.default_value = 4.0
        
        detail_input = tex_node.inputs.get('Detail') or tex_node.inputs[3]
        detail_input.default_value = 15.0
        
        rough_input = tex_node.inputs.get('Roughness') or tex_node.inputs[4]
        rough_input.default_value = 0.65
            
        # Shift Noise from (0 to 1) to (-0.5 to 0.5) so it displaces inwards and outwards
        shift_math = node_tree.nodes.new("ShaderNodeMath")
        shift_math.operation = 'SUBTRACT'
        shift_math.inputs[1].default_value = 0.5
        
        node_tree.links.new(tex_node.outputs[0], shift_math.inputs[0])
        node_tree.links.new(shift_math.outputs[0], strength_math.inputs[0])

    # --- Core Routing ---
    # Geometry flow
    node_tree.links.new(input_node.outputs[0], subdiv_node.inputs[0])
    node_tree.links.new(subdiv_node.outputs[0], set_pos_node.inputs[0])
    node_tree.links.new(set_pos_node.outputs[0], smooth_node.inputs[0])
    node_tree.links.new(smooth_node.outputs[0], output_node.inputs[0])
    
    # Displacement flow (Normal * Texture * Strength -> Offset)
    node_tree.links.new(normal_node.outputs[0], vec_math_node.inputs[0])
    node_tree.links.new(strength_math.outputs[0], scale_socket)
    
    offset_input = set_pos_node.inputs.get('Offset') or set_pos_node.inputs[3]
    node_tree.links.new(vec_math_node.outputs[0], offset_input)

    return f"Created '{obj.name}' at {location} utilizing procedural {texture_type} alpha displacement."
