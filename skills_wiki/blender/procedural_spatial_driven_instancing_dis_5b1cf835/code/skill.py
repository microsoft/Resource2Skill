def create_distance_scaled_instances(
    scene_name: str = "Scene",
    object_name: str = "DistanceRippleGrid",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    grid_size: float = 10.0,
    grid_resolution: int = 25,
    material_color: tuple = (0.05, 0.6, 0.8),
    **kwargs
) -> str:
    """
    Create a procedural grid of instances whose scale is driven by their distance from the origin.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created base object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the base object.
        grid_size: The overall X/Y size of the generated grid.
        grid_resolution: Number of vertices along the X and Y axes.
        material_color: (R, G, B) base color for the instances.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy

    # Ensure scene exists
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Create Base Object ===
    # We create a dummy mesh object to host the Geometry Nodes modifier
    mesh = bpy.data.meshes.new(f"{object_name}_mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    obj.location = location
    obj.scale = (scale, scale, scale)
    
    # === Step 2: Set up Geometry Nodes Modifier ===
    modifier = obj.modifiers.new(name="GeoNodes", type='NODES')
    
    # Create a new node tree
    tree_name = f"{object_name}_NodeTree"
    if tree_name in bpy.data.node_groups:
        node_tree = bpy.data.node_groups[tree_name]
        node_tree.nodes.clear()
    else:
        node_tree = bpy.data.node_groups.new(name=tree_name, type='GeometryNodeTree')
    
    modifier.node_group = node_tree
    
    # Ensure standard interface socket for output exists
    if not node_tree.interface.items_tree.get("Geometry"):
        node_tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
        
    nodes = node_tree.nodes
    links = node_tree.links
    
    # === Step 3: Build Node Tree ===
    
    # Group Output
    out_node = nodes.new('NodeGroupOutput')
    out_node.location = (1000, 0)
    
    # Base Grid
    grid = nodes.new('GeometryNodeMeshGrid')
    grid.location = (-400, 0)
    grid.inputs['Size X'].default_value = grid_size
    grid.inputs['Size Y'].default_value = grid_size
    grid.inputs['Vertices X'].default_value = grid_resolution
    grid.inputs['Vertices Y'].default_value = grid_resolution
    
    # Convert Grid Faces to Points
    mesh_to_points = nodes.new('GeometryNodeMeshToPoints')
    mesh_to_points.location = (-200, 0)
    mesh_to_points.mode = 'FACES'
    
    # The Primitive to Instance (Cube)
    instance_mesh = nodes.new('GeometryNodeMeshCube')
    instance_mesh.location = (-400, -200)
    # Calculate a base cell size slightly smaller than the actual grid cells
    cell_size = (grid_size / grid_resolution) * 0.8
    instance_mesh.inputs['Size'].default_value = (cell_size, cell_size, cell_size)
    
    # Instance on Points node
    instancer = nodes.new('GeometryNodeInstanceOnPoints')
    instancer.location = (0, 0)
    
    # Spatial Logic: Position -> Distance -> Map Range -> Scale
    position = nodes.new('GeometryNodeInputPosition')
    position.location = (-200, -400)
    
    distance = nodes.new('ShaderNodeVectorMath')
    distance.operation = 'DISTANCE'
    distance.location = (0, -400)
    # input 0 gets the Position, input 1 defaults to (0,0,0)
    
    map_range = nodes.new('ShaderNodeMapRange')
    map_range.location = (200, -400)
    map_range.inputs[1].default_value = 0.0                    # From Min (Center)
    map_range.inputs[2].default_value = grid_size / 2.0        # From Max (Outer Edge)
    map_range.inputs[3].default_value = 0.1                    # To Min (Scale at Center)
    map_range.inputs[4].default_value = 1.0                    # To Max (Scale at Edge)
    
    scale_inst = nodes.new('GeometryNodeScaleInstances')
    scale_inst.location = (400, 0)
    
    # Realize Instances (converts instances to actual mesh data for correct shading)
    realize = nodes.new('GeometryNodeRealizeInstances')
    realize.location = (600, 0)
    
    # Material Node
    set_mat = nodes.new('GeometryNodeSetMaterial')
    set_mat.location = (800, 0)
    
    # === Step 4: Create & Assign Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Metallic"].default_value = 0.8
        bsdf.inputs["Roughness"].default_value = 0.3
    set_mat.inputs['Material'].default_value = mat
    
    # === Step 5: Connect Links ===
    links.new(grid.outputs['Mesh'], mesh_to_points.inputs['Mesh'])
    links.new(mesh_to_points.outputs['Points'], instancer.inputs['Points'])
    links.new(instance_mesh.outputs['Mesh'], instancer.inputs['Instance'])
    
    links.new(position.outputs['Position'], distance.inputs[0])
    links.new(distance.outputs['Value'], map_range.inputs[0]) # Input 0 is 'Value'
    links.new(map_range.outputs['Result'], scale_inst.inputs['Scale'])
    
    links.new(instancer.outputs['Instances'], scale_inst.inputs['Instances'])
    links.new(scale_inst.outputs['Instances'], realize.inputs['Geometry'])
    links.new(realize.outputs['Geometry'], set_mat.inputs['Geometry'])
    links.new(set_mat.outputs['Geometry'], out_node.inputs['Geometry'])
    
    # Make object active and selected
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    return f"Created '{object_name}' with procedural distance-based scaling at {location}."
