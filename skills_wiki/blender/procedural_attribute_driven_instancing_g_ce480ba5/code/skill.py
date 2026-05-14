def create_object(
    scene_name: str = "Scene",
    object_name: str = "GeoInstanceGrid",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.6, 0.8),
    **kwargs,
) -> str:
    """
    Create Procedural Attribute-Driven Instancing Grid in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the generated geometry nodes host object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: 
            grid_size: Size of the generated grid (default 10.0)
            grid_verts: Density of the grid (default 20)
            max_scale_distance: Falloff distance for the scaling effect (default 8.0)

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    # Configuration kwargs
    grid_size = kwargs.get("grid_size", 10.0)
    grid_verts = kwargs.get("grid_verts", 20)
    max_scale_distance = kwargs.get("max_scale_distance", 8.0)

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection

    # === Step 1: Create the Instance Object (Suzanne blueprint) ===
    # We create it, assign a material, and hide it so it only appears via instancing.
    instance_name = f"{object_name}_InstanceMesh"
    mesh = bpy.data.meshes.new(instance_name)
    instance_obj = bpy.data.objects.new(instance_name, mesh)
    collection.objects.link(instance_obj)
    
    # Generate Suzanne geometry into the mesh
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_monkey(bm)
    bm.to_mesh(mesh)
    bm.free()
    
    # Hide the blueprint object
    instance_obj.hide_viewport = True
    instance_obj.hide_render = True

    # Material Setup
    mat = bpy.data.materials.new(name=f"{object_name}_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.4
    mesh.materials.append(mat)

    # === Step 2: Create Host Object for Geometry Nodes ===
    host_mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    host_obj = bpy.data.objects.new(object_name, host_mesh)
    collection.objects.link(host_obj)
    
    host_obj.location = Vector(location)
    host_obj.scale = Vector((scale, scale, scale))

    # === Step 3: Build Geometry Nodes Tree ===
    mod = host_obj.modifiers.new(name="GeometryNodes", type='NODES')
    tree = bpy.data.node_groups.new(name=f"{object_name}_NodeTree", type='GeometryNodeTree')
    mod.node_group = tree

    # Handle API differences for outputs (Blender 4.0+ vs older)
    if hasattr(tree, "interface"):
        tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        tree.outputs.new('NodeSocketGeometry', "Geometry")

    # Clear default nodes
    tree.nodes.clear()

    # Create Nodes
    out_node = tree.nodes.new("NodeGroupOutput")
    out_node.location = (800, 0)

    # Generate the base plane
    grid_node = tree.nodes.new("GeometryNodeMeshGrid")
    grid_node.location = (-400, 0)
    grid_node.inputs['Size X'].default_value = grid_size
    grid_node.inputs['Size Y'].default_value = grid_size
    grid_node.inputs['Vertices X'].default_value = grid_verts
    grid_node.inputs['Vertices Y'].default_value = grid_verts

    # Convert Grid Faces to Points (as shown in the tutorial)
    m2p_node = tree.nodes.new("GeometryNodeMeshToPoints")
    m2p_node.location = (-200, 0)
    m2p_node.mode = 'FACES'

    # Instance on the generated points
    iop_node = tree.nodes.new("GeometryNodeInstanceOnPoints")
    iop_node.location = (400, 0)

    # Bring in the Suzanne instance object
    obj_info = tree.nodes.new("GeometryNodeObjectInfo")
    obj_info.location = (200, 200)
    obj_info.inputs['Object'].default_value = instance_obj

    # --- Procedural Rotation (Random Chaotic) ---
    rand_rot = tree.nodes.new("FunctionNodeRandomValue")
    rand_rot.location = (200, -100)
    rand_rot.data_type = 'FLOAT_VECTOR'
    rand_rot.inputs['Min'].default_value = (0.0, 0.0, 0.0)
    rand_rot.inputs['Max'].default_value = (math.pi * 2, math.pi * 2, math.pi * 2)

    # --- Procedural Scale (Distance from origin) ---
    pos_node = tree.nodes.new("GeometryNodeInputPosition")
    pos_node.location = (-200, -300)

    dist_node = tree.nodes.new("ShaderNodeVectorMath")
    dist_node.location = (0, -300)
    dist_node.operation = 'DISTANCE'
    dist_node.inputs[1].default_value = (0, 0, 0)

    # Math node to invert distance: (max_distance - distance), so origin is largest
    math_node = tree.nodes.new("ShaderNodeMath")
    math_node.location = (200, -300)
    math_node.operation = 'SUBTRACT'
    math_node.inputs[0].default_value = max_scale_distance
    math_node.use_clamp = True # Prevent negative scale

    # Scale multiplier to make them fit nicely
    scale_mult = tree.nodes.new("ShaderNodeMath")
    scale_mult.location = (350, -300)
    scale_mult.operation = 'MULTIPLY'
    scale_mult.inputs[1].default_value = 0.15 * (10.0 / grid_verts) # Auto-adjust scale based on density

    # === Step 4: Link Nodes ===
    links = tree.links
    # Geometry flow
    links.new(grid_node.outputs['Mesh'], m2p_node.inputs['Mesh'])
    links.new(m2p_node.outputs['Points'], iop_node.inputs['Points'])
    links.new(obj_info.outputs['Geometry'], iop_node.inputs['Instance'])
    links.new(iop_node.outputs['Instances'], out_node.inputs['Geometry'])
    
    # Rotation flow
    links.new(rand_rot.outputs['Value'], iop_node.inputs['Rotation'])
    
    # Scale flow
    links.new(pos_node.outputs['Position'], dist_node.inputs[0])
    links.new(dist_node.outputs['Value'], math_node.inputs[1])
    links.new(math_node.outputs['Value'], scale_mult.inputs[0])
    links.new(scale_mult.outputs['Value'], iop_node.inputs['Scale'])

    # Force view layer update
    bpy.context.view_layer.update()

    return f"Created '{object_name}' at {location} with procedural distance-based scale and random rotation."
