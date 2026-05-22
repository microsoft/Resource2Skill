def create_object(
    scene_name: str = "Scene",
    object_name: str = "DistanceMatrix",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.8, 0.4),
    **kwargs,
) -> str:
    """
    Create a procedural grid of objects scaled by their distance from the origin.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created Geometry Nodes container object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the overall container.
        material_color: (R, G, B) base color for the instanced objects.
        **kwargs: Additional parameters. Options include:
            - grid_size (float): The width/height of the grid (default 10.0)
            - grid_density (int): Subdivisions of the grid (default 16)
            - scale_factor (float): Multiplier for the distance effect (default 0.25)

    Returns:
        Status string.
    """
    import bpy
    import mathutils

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Optional kwargs
    grid_size = kwargs.get("grid_size", 10.0)
    grid_density = kwargs.get("grid_density", 16)
    scale_factor = kwargs.get("scale_factor", 0.25)

    # === Step 1: Create the Target Instance Object (Suzanne) ===
    bpy.ops.mesh.primitive_monkey_add(location=(0, 0, 0))
    instance_obj = bpy.context.active_object
    instance_obj.name = f"{object_name}_InstanceMesh"
    
    # Smooth shade the monkey
    for poly in instance_obj.data.polygons:
        poly.use_smooth = True
        
    # Hide the source instance from the viewport and render
    instance_obj.hide_set(True)
    instance_obj.hide_render = True

    # === Step 2: Build Material for the Instances ===
    mat_name = f"{object_name}_Material"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.3
    
    # Assign material to the instance source
    instance_obj.data.materials.append(mat)

    # === Step 3: Create the Main Container Object ===
    # Using a simple plane as the host for the Geometry Nodes modifier
    bpy.ops.mesh.primitive_plane_add(location=location)
    main_obj = bpy.context.active_object
    main_obj.name = object_name
    main_obj.scale = (scale, scale, scale)

    # === Step 4: Build the Geometry Nodes Tree ===
    modifier = main_obj.modifiers.new(name="GeoNodes_SpatialScatter", type='NODES')
    node_group = bpy.data.node_groups.new(name=f"{object_name}_Tree", type='GeometryNodeTree')
    modifier.node_group = node_group

    # Compatibility for adding input/output sockets (Blender 4.0+ vs 3.x)
    if hasattr(node_group, 'interface'):
        node_group.interface.new_socket(name="Geometry", in_out='IN', socket_type='NodeSocketGeometry')
        node_group.interface.new_socket(name="Geometry", in_out='OUT', socket_type='NodeSocketGeometry')
    else:
        node_group.inputs.new('NodeSocketGeometry', "Geometry")
        node_group.outputs.new('NodeSocketGeometry', "Geometry")

    nodes = node_group.nodes
    links = node_group.links

    # Create Nodes
    node_in = nodes.new('NodeGroupInput')
    node_in.location = (-800, 0)
    
    node_out = nodes.new('NodeGroupOutput')
    node_out.location = (400, 0)

    # 1. Grid Generation
    node_grid = nodes.new('GeometryNodeMeshGrid')
    node_grid.location = (-600, 0)
    node_grid.inputs['Size X'].default_value = grid_size
    node_grid.inputs['Size Y'].default_value = grid_size
    node_grid.inputs['Vertices X'].default_value = grid_density
    node_grid.inputs['Vertices Y'].default_value = grid_density

    # 2. Convert Grid Faces to Points
    node_m2p = nodes.new('GeometryNodeMeshToPoints')
    node_m2p.location = (-400, 0)
    node_m2p.mode = 'FACES'

    # 3. Import Suzanne Object Data
    node_obj_info = nodes.new('GeometryNodeObjectInfo')
    node_obj_info.location = (-400, -200)
    node_obj_info.inputs['Object'].default_value = instance_obj

    # 4. Instance on Points
    node_iop = nodes.new('GeometryNodeInstanceOnPoints')
    node_iop.location = (100, 0)

    # 5. Spatial Math (Distance from Center)
    node_pos = nodes.new('GeometryNodeInputPosition')
    node_pos.location = (-400, -450)

    node_dist = nodes.new('ShaderNodeVectorMath')
    node_dist.location = (-200, -450)
    node_dist.operation = 'DISTANCE'
    node_dist.inputs[1].default_value = (0.0, 0.0, 0.0) # Target point for distance

    node_math = nodes.new('ShaderNodeMath')
    node_math.location = (0, -450)
    node_math.operation = 'MULTIPLY'
    node_math.inputs[1].default_value = scale_factor # Controls how aggressive the scaling is

    # Link Everything Together
    links.new(node_grid.outputs['Mesh'], node_m2p.inputs['Mesh'])
    links.new(node_m2p.outputs['Points'], node_iop.inputs['Points'])
    links.new(node_obj_info.outputs['Geometry'], node_iop.inputs['Instance'])
    
    links.new(node_pos.outputs['Position'], node_dist.inputs[0])
    links.new(node_dist.outputs['Value'], node_math.inputs[0])
    links.new(node_math.outputs['Value'], node_iop.inputs['Scale'])
    
    links.new(node_iop.outputs['Instances'], node_out.inputs['Geometry'])

    # Deselect all and select only the main object
    bpy.ops.object.select_all(action='DESELECT')
    main_obj.select_set(True)
    bpy.context.view_layer.objects.active = main_obj

    return f"Created procedural instancer '{object_name}' with {grid_density**2} instances at {location}"
