def create_object(
    scene_name: str = "Scene",
    object_name: str = "SugarGummyCandy",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.05, 0.05),
    **kwargs,
) -> str:
    """
    Create a Procedural Sugar Coated Gummy Candy using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created candy object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the gummy candy.
        **kwargs: 
            crystal_density (float): Density of the sugar crystals (default: 800.0).

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    crystal_density = kwargs.get('crystal_density', 800.0)

    # === Step 1: Create the Instance Object (Sugar Crystal) ===
    bpy.ops.mesh.primitive_cube_add(size=0.03, location=(0, 0, 0))
    crystal_obj = bpy.context.active_object
    crystal_obj.name = f"{object_name}_Crystal"
    crystal_obj.hide_viewport = True
    crystal_obj.hide_render = True  # Hide the source object

    # Crystal Material (Rough Glass/Sugar)
    mat_sugar = bpy.data.materials.new(name=f"{object_name}_SugarMat")
    mat_sugar.use_nodes = True
    bsdf_sugar = mat_sugar.node_tree.nodes.get("Principled BSDF")
    if bsdf_sugar:
        bsdf_sugar.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)
        bsdf_sugar.inputs['Roughness'].default_value = 0.35
        # Handle Blender 4.0+ vs older versions for Transmission
        if 'Transmission Weight' in bsdf_sugar.inputs:
            bsdf_sugar.inputs['Transmission Weight'].default_value = 1.0
        elif 'Transmission' in bsdf_sugar.inputs:
            bsdf_sugar.inputs['Transmission'].default_value = 1.0
        bsdf_sugar.inputs['IOR'].default_value = 1.45
    crystal_obj.data.materials.append(mat_sugar)

    # === Step 2: Create the Host Object (Gummy Candy) ===
    bpy.ops.mesh.primitive_torus_add(major_radius=0.8, minor_radius=0.35, location=location)
    candy_obj = bpy.context.active_object
    candy_obj.name = object_name
    bpy.ops.object.shade_smooth()
    
    candy_obj.scale = (scale, scale, scale)

    # Gummy Material
    mat_gummy = bpy.data.materials.new(name=f"{object_name}_GummyMat")
    mat_gummy.use_nodes = True
    bsdf_gummy = mat_gummy.node_tree.nodes.get("Principled BSDF")
    if bsdf_gummy:
        bsdf_gummy.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf_gummy.inputs['Roughness'].default_value = 0.15
        if 'Transmission Weight' in bsdf_gummy.inputs:
            bsdf_gummy.inputs['Transmission Weight'].default_value = 1.0
        elif 'Transmission' in bsdf_gummy.inputs:
            bsdf_gummy.inputs['Transmission'].default_value = 1.0
    candy_obj.data.materials.append(mat_gummy)

    # === Step 3: Build Geometry Nodes Modifier ===
    modifier = candy_obj.modifiers.new(name="SugarCoating", type='NODES')
    node_tree = bpy.data.node_groups.new(name=f"{object_name}_GeoTree", type='GeometryNodeTree')
    modifier.node_group = node_tree

    # Setup tree inputs/outputs dynamically (handles Blender 3.x and 4.x API changes)
    if hasattr(node_tree, 'interface'):
        node_tree.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        node_tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        node_tree.inputs.new('NodeSocketGeometry', "Geometry")
        node_tree.outputs.new('NodeSocketGeometry', "Geometry")

    nodes = node_tree.nodes
    links = node_tree.links

    # Create Nodes
    node_in = nodes.new('NodeGroupInput')
    node_in.location = (-400, 0)

    node_out = nodes.new('NodeGroupOutput')
    node_out.location = (600, 0)

    distribute = nodes.new('GeometryNodeDistributePointsOnFaces')
    distribute.location = (-200, 100)
    distribute.inputs['Density'].default_value = crystal_density

    instancer = nodes.new('GeometryNodeInstanceOnPoints')
    instancer.location = (200, 100)

    join = nodes.new('GeometryNodeJoinGeometry')
    join.location = (400, 0)

    obj_info = nodes.new('GeometryNodeObjectInfo')
    obj_info.location = (-200, -100)
    obj_info.inputs['Object'].default_value = crystal_obj
    obj_info.transform_space = 'RELATIVE'

    rand_rot = nodes.new('FunctionNodeRandomValue')
    rand_rot.location = (-200, -300)
    rand_rot.data_type = 'FLOAT_VECTOR'
    # Use math.tau (6.283) to get a full 360-degree rotation on all axes in radians
    rand_rot.inputs['Max'].default_value = (math.tau, math.tau, math.tau)

    rand_scale = nodes.new('FunctionNodeRandomValue')
    rand_scale.location = (-200, -500)
    rand_scale.data_type = 'FLOAT'
    rand_scale.inputs['Min'].default_value = 0.5
    rand_scale.inputs['Max'].default_value = 1.2

    # Link Nodes
    links.new(node_in.outputs['Geometry'], distribute.inputs['Mesh'])
    links.new(node_in.outputs['Geometry'], join.inputs['Geometry'])  # Keep original mesh
    
    links.new(distribute.outputs['Points'], instancer.inputs['Points'])
    links.new(obj_info.outputs['Geometry'], instancer.inputs['Instance'])
    links.new(rand_rot.outputs['Value'], instancer.inputs['Rotation'])
    links.new(rand_scale.outputs['Value'], instancer.inputs['Scale'])
    
    links.new(instancer.outputs['Instances'], join.inputs['Geometry']) # Add instances
    links.new(join.outputs['Geometry'], node_out.inputs['Geometry'])

    # Ensure the scene is updated
    bpy.context.view_layer.update()

    return f"Created '{object_name}' at {location} with Geometry Nodes scattering ({crystal_density} density)."
