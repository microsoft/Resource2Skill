def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralMonkeyScatter",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a procedural Geometry Nodes scatter setup based on the tutorial.
    
    Args:
        scene_name: Name of the active scene.
        object_name: Base name for the generated objects.
        location: (x, y, z) placement of the procedural setup.
        scale: Overall scale multiplier.
        material_color: (R, G, B) color applied to the instanced objects.
        **kwargs: 
            grid_size (float): The X/Y dimension of the scatter grid.
            grid_vertices (int): The density of the grid (number of instances = (vertices-1)^2).
            
    Returns:
        Status string confirming creation.
    """
    import bpy
    import math
    from mathutils import Vector

    # Determine Scene
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # Extracted kwargs
    grid_size = kwargs.get("grid_size", 5.0)
    grid_vertices = kwargs.get("grid_vertices", 8)

    # === Step 1: Create the Instance Object (Suzanne) ===
    instance_name = f"{object_name}_SourceInstance"
    if instance_name in bpy.data.objects:
        instance_obj = bpy.data.objects[instance_name]
    else:
        # Create base monkey
        bpy.ops.mesh.primitive_monkey_add(location=(0, 0, -10))
        instance_obj = bpy.context.active_object
        instance_obj.name = instance_name
        
        # Build and assign material
        mat_name = f"{object_name}_InstanceMat"
        mat = bpy.data.materials.get(mat_name)
        if not mat:
            mat = bpy.data.materials.new(name=mat_name)
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                # Support for Blender 4.0+ Base Color socket
                color_socket = bsdf.inputs.get("Base Color") or bsdf.inputs.get("Base Color")
                color_socket.default_value = (*material_color, 1.0)
                bsdf.inputs["Roughness"].default_value = 0.4
        
        if len(instance_obj.data.materials) == 0:
            instance_obj.data.materials.append(mat)
        else:
            instance_obj.data.materials[0] = mat
            
        # Hide the source instance from rendering and viewport
        instance_obj.hide_viewport = True
        instance_obj.hide_render = True

    # === Step 2: Create Host Object & Modifier ===
    bpy.ops.mesh.primitive_plane_add(location=location)
    host_obj = bpy.context.active_object
    host_obj.name = object_name
    host_obj.scale = (scale, scale, scale)

    # Add Geometry Nodes Modifier
    mod = host_obj.modifiers.new(name="GeoScatter", type='NODES')
    
    # Create Node Group
    node_group = bpy.data.node_groups.new(name=f"{object_name}_NodeTree", type='GeometryNodeTree')
    mod.node_group = node_group
    
    # Setup Output Interface (handles Blender 3.x and 4.x API differences)
    if hasattr(node_group, "interface"):
        node_group.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        node_group.outputs.new('NodeSocketGeometry', 'Geometry')

    nodes = node_group.nodes
    links = node_group.links
    
    # === Step 3: Build the Node Tree ===
    
    # Output Node
    out_node = nodes.new('NodeGroupOutput')
    out_node.location = (400, 0)
    
    # Grid Node (Generates the base domain)
    grid_node = nodes.new('GeometryNodeMeshGrid')
    grid_node.location = (-600, 0)
    grid_node.inputs['Size X'].default_value = grid_size
    grid_node.inputs['Size Y'].default_value = grid_size
    grid_node.inputs['Vertices X'].default_value = grid_vertices
    grid_node.inputs['Vertices Y'].default_value = grid_vertices
    
    # Mesh to Points Node (Converts faces to point domain)
    m2p_node = nodes.new('GeometryNodeMeshToPoints')
    m2p_node.location = (-400, 0)
    m2p_node.mode = 'FACES' 
    
    # Object Info Node (Pulls the hidden Suzanne into the node tree)
    obj_info_node = nodes.new('GeometryNodeObjectInfo')
    obj_info_node.location = (-400, -200)
    obj_info_node.inputs['Object'].default_value = instance_obj
    
    # Random Value Node (Generates 0-360 degree Euler rotations per point)
    rand_rot_node = nodes.new('FunctionNodeRandomValue')
    rand_rot_node.data_type = 'FLOAT_VECTOR'
    rand_rot_node.location = (-400, -400)
    rand_rot_node.inputs['Min'].default_value = (0.0, 0.0, 0.0)
    rand_rot_node.inputs['Max'].default_value = (math.pi * 2, math.pi * 2, math.pi * 2) 
    
    # Instance on Points Node (Combines points, instances, and rotation)
    iop_node = nodes.new('GeometryNodeInstanceOnPoints')
    iop_node.location = (-100, 0)
    # Scale instances down slightly so they fit cleanly on the grid
    iop_node.inputs['Scale'].default_value = (0.3, 0.3, 0.3)
    
    # === Step 4: Link the Nodes ===
    links.new(grid_node.outputs['Mesh'], m2p_node.inputs['Mesh'])
    links.new(m2p_node.outputs['Points'], iop_node.inputs['Points'])
    links.new(obj_info_node.outputs['Geometry'], iop_node.inputs['Instance'])
    links.new(rand_rot_node.outputs['Value'], iop_node.inputs['Rotation'])
    links.new(iop_node.outputs['Instances'], out_node.inputs['Geometry'])

    return f"Created '{object_name}' at {location}. Generated procedural grid instancing '{instance_name}' with randomized rotations."
