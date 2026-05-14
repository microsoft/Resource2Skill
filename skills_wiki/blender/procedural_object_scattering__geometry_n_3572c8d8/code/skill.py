def create_object(
    scene_name: str = "Scene",
    object_name: str = "SugarCandy",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.05, 0.1),
    **kwargs,
) -> str:
    """
    Create a procedurally sugar-coated candy using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created candy object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the jelly candy.
        **kwargs: 'density' (float) to control the amount of sugar (default 5000.0).

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    density = kwargs.get("density", 5000.0)

    # === Step 1: Create the Instance Object (Sugar Crystal) ===
    bpy.ops.mesh.primitive_icosphere_add(radius=0.015, subdivisions=1, location=(0, 0, 0))
    crystal_obj = bpy.context.active_object
    crystal_obj.name = f"{object_name}_Crystal"
    
    # Material for Crystal (Glassy/Transmissive)
    crystal_mat = bpy.data.materials.new(name=f"{object_name}_Crystal_Mat")
    crystal_mat.use_nodes = True
    c_bsdf = crystal_mat.node_tree.nodes.get("Principled BSDF")
    if c_bsdf:
        c_bsdf.inputs['Base Color'].default_value = (0.95, 0.95, 0.95, 1.0)
        c_bsdf.inputs['Roughness'].default_value = 0.05
        # Handle Blender 4.0+ vs older API for Transmission
        if 'Transmission Weight' in c_bsdf.inputs:
            c_bsdf.inputs['Transmission Weight'].default_value = 1.0
        elif 'Transmission' in c_bsdf.inputs:
            c_bsdf.inputs['Transmission'].default_value = 1.0
    crystal_obj.data.materials.append(crystal_mat)
    crystal_obj.hide_viewport = True
    crystal_obj.hide_render = True

    # === Step 2: Create the Base Mesh (Candy Body) ===
    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.5, minor_radius=0.25, 
        major_segments=48, minor_segments=24, 
        location=location
    )
    candy_obj = bpy.context.active_object
    candy_obj.name = object_name
    bpy.ops.object.shade_smooth()
    candy_obj.scale = (scale, scale, scale)

    # Material for Candy (Gummy/Jelly)
    candy_mat = bpy.data.materials.new(name=f"{object_name}_Candy_Mat")
    candy_mat.use_nodes = True
    b_bsdf = candy_mat.node_tree.nodes.get("Principled BSDF")
    if b_bsdf:
        b_bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        b_bsdf.inputs['Roughness'].default_value = 0.15
        if 'Transmission Weight' in b_bsdf.inputs:
            b_bsdf.inputs['Transmission Weight'].default_value = 0.95
        elif 'Transmission' in b_bsdf.inputs:
            b_bsdf.inputs['Transmission'].default_value = 0.95
    candy_obj.data.materials.append(candy_mat)

    # === Step 3: Geometry Nodes Modifier ===
    mod = candy_obj.modifiers.new(name="Sugar_Coating", type='NODES')
    gn_group = bpy.data.node_groups.new(f"{object_name}_GN", 'GeometryNodeTree')
    mod.node_group = gn_group

    # Robust IO creation (Supports 4.0+ and older APIs)
    if hasattr(gn_group, "interface"):
        gn_group.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        gn_group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        gn_group.inputs.new('NodeSocketGeometry', "Geometry")
        gn_group.outputs.new('NodeSocketGeometry', "Geometry")

    nodes = gn_group.nodes
    links = gn_group.links

    # Spawn Nodes
    group_in = nodes.new("NodeGroupInput")
    group_out = nodes.new("NodeGroupOutput")
    distribute = nodes.new("GeometryNodeDistributePointsOnFaces")
    instance = nodes.new("GeometryNodeInstanceOnPoints")
    join = nodes.new("GeometryNodeJoinGeometry")
    obj_info = nodes.new("GeometryNodeObjectInfo")
    rand_rot = nodes.new("FunctionNodeRandomValue")
    rand_scale = nodes.new("FunctionNodeRandomValue")

    # Configure Node Settings
    distribute.inputs['Density'].default_value = density
    
    obj_info.inputs[0].default_value = crystal_obj  # Assign Target Object
    
    rand_rot.data_type = 'FLOAT_VECTOR'
    for inp in rand_rot.inputs:
        if inp.name == 'Min' and inp.type == 'VECTOR':
            inp.default_value = (0.0, 0.0, 0.0)
        elif inp.name == 'Max' and inp.type == 'VECTOR':
            inp.default_value = (math.tau, math.tau, math.tau) # 360 degree random rotation
            
    rand_scale.data_type = 'FLOAT'
    for inp in rand_scale.inputs:
        if inp.name == 'Min' and inp.type == 'VALUE':
            inp.default_value = 0.5
        elif inp.name == 'Max' and inp.type == 'VALUE':
            inp.default_value = 1.5

    # Helper function for safe socket linking across Blender versions
    def get_sock(sockets, name, fallback_index):
        return sockets[name] if name in sockets else sockets[fallback_index]

    # Create Node Connections
    links.new(get_sock(group_in.outputs, "Geometry", 0), get_sock(distribute.inputs, "Mesh", 0))
    links.new(get_sock(distribute.outputs, "Points", 0), get_sock(instance.inputs, "Points", 0))
    links.new(get_sock(obj_info.outputs, "Geometry", 0), get_sock(instance.inputs, "Instance", 2))
    links.new(get_sock(rand_rot.outputs, "Value", 0), get_sock(instance.inputs, "Rotation", 5))
    links.new(get_sock(rand_scale.outputs, "Value", 0), get_sock(instance.inputs, "Scale", 6))
    
    # Join original mesh with generated sugar crystals
    links.new(get_sock(group_in.outputs, "Geometry", 0), get_sock(join.inputs, "Geometry", 0))
    links.new(get_sock(instance.outputs, "Instances", 0), get_sock(join.inputs, "Geometry", 0))
    
    links.new(get_sock(join.outputs, "Geometry", 0), get_sock(group_out.inputs, "Geometry", 0))

    return f"Created '{object_name}' (Sugar-coated candy) at {location}. Generated {density} points for GN scattering."
