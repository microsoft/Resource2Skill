def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProximityScatter",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.6, 0.8),
    **kwargs,
) -> str:
    """
    Create Procedural Proximity Instancing in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created system object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color in 0-1 range for the instanced objects.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create the Source Instance Object ===
    instance_name = f"{object_name}_Instance"
    if instance_name not in bpy.data.objects:
        # Create a hidden monkey to act as the instance source
        bpy.ops.mesh.primitive_monkey_add(location=(0, 0, -50))
        instance_obj = bpy.context.active_object
        instance_obj.name = instance_name
        instance_obj.hide_viewport = True
        instance_obj.hide_render = True
    else:
        instance_obj = bpy.data.objects[instance_name]
    
    # Setup Material for the Instance
    mat_name = f"{object_name}_Mat"
    if mat_name not in bpy.data.materials:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.3
    else:
        mat = bpy.data.materials[mat_name]
    
    if len(instance_obj.data.materials) == 0:
        instance_obj.data.materials.append(mat)
    else:
        instance_obj.data.materials[0] = mat

    # === Step 2: Create the Generator Object ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    # Add a single vertex so the mesh is technically valid
    mesh.from_pydata([(0, 0, 0)], [], [])
    mesh.update()

    # === Step 3: Geometry Nodes Setup ===
    modifier = obj.modifiers.new(name="ProximityInstancer", type='NODES')
    node_tree = bpy.data.node_groups.new(name=f"{object_name}_Tree", type='GeometryNodeTree')
    modifier.node_group = node_tree
    node_tree.nodes.clear()
    
    # Create I/O Interface (Blender 4.0+)
    if hasattr(node_tree, "interface"):
        node_tree.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        
        sock_size_x = node_tree.interface.new_socket(name="Grid Size X", in_out='INPUT', socket_type='NodeSocketFloat')
        sock_size_x.default_value = 10.0
        
        sock_size_y = node_tree.interface.new_socket(name="Grid Size Y", in_out='INPUT', socket_type='NodeSocketFloat')
        sock_size_y.default_value = 10.0
        
        sock_verts_x = node_tree.interface.new_socket(name="Vertices X", in_out='INPUT', socket_type='NodeSocketInt')
        sock_verts_x.default_value = 16
        
        sock_verts_y = node_tree.interface.new_socket(name="Vertices Y", in_out='INPUT', socket_type='NodeSocketInt')
        sock_verts_y.default_value = 16
        
        node_tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        # Fallback for older API
        node_tree.inputs.new('NodeSocketGeometry', "Geometry")
        node_tree.inputs.new('NodeSocketFloat', "Grid Size X").default_value = 10.0
        node_tree.inputs.new('NodeSocketFloat', "Grid Size Y").default_value = 10.0
        node_tree.inputs.new('NodeSocketInt', "Vertices X").default_value = 16
        node_tree.inputs.new('NodeSocketInt', "Vertices Y").default_value = 16
        node_tree.outputs.new('NodeSocketGeometry', "Geometry")

    # Create Nodes
    group_in = node_tree.nodes.new("NodeGroupInput")
    group_in.location = (-800, 0)
    
    group_out = node_tree.nodes.new("NodeGroupOutput")
    group_out.location = (800, 0)

    node_grid = node_tree.nodes.new("GeometryNodeMeshGrid")
    node_grid.location = (-600, 0)
    
    node_mesh_to_points = node_tree.nodes.new("GeometryNodeMeshToPoints")
    node_mesh_to_points.mode = 'FACES'
    node_mesh_to_points.location = (-400, 0)
    
    node_obj_info = node_tree.nodes.new("GeometryNodeObjectInfo")
    node_obj_info.inputs["Object"].default_value = instance_obj
    node_obj_info.location = (-400, -200)
    
    node_random_rot = node_tree.nodes.new("FunctionNodeRandomValue")
    node_random_rot.data_type = 'FLOAT_VECTOR'
    node_random_rot.inputs["Max"].default_value = (math.pi*2, math.pi*2, math.pi*2)
    node_random_rot.location = (-200, -200)
    
    node_instance = node_tree.nodes.new("GeometryNodeInstanceOnPoints")
    node_instance.location = (0, 0)
    
    node_scale_base = node_tree.nodes.new("GeometryNodeScaleInstances")
    node_scale_base.inputs["Scale"].default_value = (0.2, 0.2, 0.2)
    node_scale_base.location = (200, 0)
    
    node_scale_prox = node_tree.nodes.new("GeometryNodeScaleInstances")
    node_scale_prox.location = (400, 0)
    
    node_position = node_tree.nodes.new("GeometryNodeInputPosition")
    node_position.location = (200, -200)
    
    node_dist = node_tree.nodes.new("ShaderNodeVectorMath")
    node_dist.operation = 'DISTANCE'
    node_dist.inputs[1].default_value = (0.0, 0.0, 0.0) # Central proximity effector point
    node_dist.location = (200, -100)
    
    # Link Nodes
    links = node_tree.links
    
    # Map modifier inputs to the internal Grid generator
    links.new(group_in.outputs["Grid Size X"], node_grid.inputs["Size X"])
    links.new(group_in.outputs["Grid Size Y"], node_grid.inputs["Size Y"])
    links.new(group_in.outputs["Vertices X"], node_grid.inputs["Vertices X"])
    links.new(group_in.outputs["Vertices Y"], node_grid.inputs["Vertices Y"])
    
    # Main geometry flow
    links.new(node_grid.outputs["Mesh"], node_mesh_to_points.inputs["Mesh"])
    links.new(node_mesh_to_points.outputs["Points"], node_instance.inputs["Points"])
    
    # Instancing logic
    links.new(node_obj_info.outputs["Geometry"], node_instance.inputs["Instance"])
    links.new(node_random_rot.outputs["Value"], node_instance.inputs["Rotation"])
    
    # Scaling logic
    links.new(node_instance.outputs["Instances"], node_scale_base.inputs["Instances"])
    links.new(node_scale_base.outputs["Instances"], node_scale_prox.inputs["Instances"])
    
    # Proximity math
    links.new(node_position.outputs["Position"], node_dist.inputs[0])
    links.new(node_dist.outputs["Value"], node_scale_prox.inputs["Scale"])
    
    # Output
    links.new(node_scale_prox.outputs["Instances"], group_out.inputs["Geometry"])

    # === Step 4: Finalize ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' setup at {location} with Geometry Nodes proximity scaling."
