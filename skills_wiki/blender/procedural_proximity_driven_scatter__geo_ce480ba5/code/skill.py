def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProximityScatter",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.6, 0.8, 1.0),
    **kwargs,
) -> str:
    """
    Create a Procedural Proximity-Driven Scatter using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created GN object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the entire assembly.
        material_color: (R, G, B, A) base color for the instanced objects.
        **kwargs: 
            grid_size (float): Dimensions of the grid (default 10.0).
            resolution (int): Number of vertices per side (default 20).
            falloff_radius (float): Distance at which instances scale to 0 (default 5.0).

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector
    import math

    # Handle scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Parameters
    grid_size = kwargs.get("grid_size", 10.0)
    resolution = kwargs.get("resolution", 20)
    falloff_radius = kwargs.get("falloff_radius", 5.0)

    # === Step 1: Create the Instance Target Object ===
    # Create a Suzanne (Monkey) to instance, matching the tutorial's aesthetic
    bpy.ops.mesh.primitive_monkey_add(size=1.0, location=(0, 0, 0))
    target_obj = bpy.context.active_object
    target_obj.name = f"{object_name}_Target"
    
    # Hide the target object so only the instances are visible
    target_obj.hide_viewport = True
    target_obj.hide_render = True

    # Add Material to Target
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = material_color
        bsdf.inputs["Metallic"].default_value = 0.8
        bsdf.inputs["Roughness"].default_value = 0.3
    if len(target_obj.data.materials) == 0:
        target_obj.data.materials.append(mat)

    # === Step 2: Create the Base Object for Geometry Nodes ===
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=location)
    base_obj = bpy.context.active_object
    base_obj.name = object_name
    base_obj.scale = (scale, scale, scale)

    # === Step 3: Build the Geometry Nodes Tree ===
    mod = base_obj.modifiers.new(name="GeoNodes_ProximityScatter", type='NODES')
    tree = bpy.data.node_groups.new(name=f"{object_name}_NodeTree", type='GeometryNodeTree')
    mod.node_group = tree

    # Set up outputs based on Blender version (3.x vs 4.x API)
    if hasattr(tree, "interface"):
        tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        tree.outputs.new('NodeSocketGeometry', "Geometry")

    # Clear default nodes
    for node in tree.nodes:
        tree.nodes.remove(node)

    # Output Node
    node_out = tree.nodes.new('NodeGroupOutput')
    node_out.location = (800, 0)

    # 1. Grid Node
    node_grid = tree.nodes.new('GeometryNodeMeshGrid')
    node_grid.location = (-400, 0)
    node_grid.inputs['Size X'].default_value = grid_size
    node_grid.inputs['Size Y'].default_value = grid_size
    node_grid.inputs['Vertices X'].default_value = resolution
    node_grid.inputs['Vertices Y'].default_value = resolution

    # 2. Mesh to Points Node (Domain: Faces)
    node_m2p = tree.nodes.new('GeometryNodeMeshToPoints')
    node_m2p.location = (-200, 0)
    node_m2p.mode = 'FACES'

    # 3. Object Info Node (Fetch the hidden target)
    node_obj_info = tree.nodes.new('GeometryNodeObjectInfo')
    node_obj_info.location = (-200, -200)
    node_obj_info.inputs['Object'].default_value = target_obj
    node_obj_info.transform_space = 'RELATIVE'

    # 4. Instance on Points Node
    node_inst = tree.nodes.new('GeometryNodeInstanceOnPoints')
    node_inst.location = (400, 0)

    # 5. Position & Distance Logic (Proximity Scaling)
    node_pos = tree.nodes.new('GeometryNodeInputPosition')
    node_pos.location = (-200, -400)

    node_dist = tree.nodes.new('ShaderNodeVectorMath')
    node_dist.location = (0, -400)
    node_dist.operation = 'DISTANCE'
    node_dist.inputs[1].default_value = (0.0, 0.0, 0.0) # Center point

    node_map = tree.nodes.new('ShaderNodeMapRange')
    node_map.location = (200, -400)
    node_map.inputs['From Min'].default_value = 0.0
    node_map.inputs['From Max'].default_value = falloff_radius
    node_map.inputs['To Min'].default_value = 1.0  # Big at the center
    node_map.inputs['To Max'].default_value = 0.0  # Shrink to 0 at the edge

    # 6. Random Rotation Logic
    node_rand_rot = tree.nodes.new('FunctionNodeRandomValue')
    node_rand_rot.location = (200, -600)
    node_rand_rot.data_type = 'FLOAT_VECTOR'
    node_rand_rot.inputs['Min'].default_value = (0, 0, 0)
    node_rand_rot.inputs['Max'].default_value = (math.pi*2, math.pi*2, math.pi*2)

    # === Step 4: Link the Nodes ===
    links = tree.links
    
    # Geometry flow
    links.new(node_grid.outputs['Mesh'], node_m2p.inputs['Mesh'])
    links.new(node_m2p.outputs['Points'], node_inst.inputs['Points'])
    links.new(node_obj_info.outputs['Geometry'], node_inst.inputs['Instance'])
    links.new(node_inst.outputs['Instances'], node_out.inputs['Geometry'])

    # Attribute flow
    links.new(node_pos.outputs['Position'], node_dist.inputs[0])
    links.new(node_dist.outputs['Value'], node_map.inputs['Value'])
    links.new(node_map.outputs['Result'], node_inst.inputs['Scale'])
    links.new(node_rand_rot.outputs['Value'], node_inst.inputs['Rotation'])

    # Ensure smooth shading on the generated instances
    bpy.ops.object.select_all(action='DESELECT')
    base_obj.select_set(True)
    bpy.context.view_layer.objects.active = base_obj

    return f"Created Procedural Grid '{object_name}' at {location} instancing '{target_obj.name}' on {resolution*resolution} faces."
