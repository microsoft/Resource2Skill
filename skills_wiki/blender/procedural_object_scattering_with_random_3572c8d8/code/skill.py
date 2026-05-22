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
        material_color: (R, G, B) base color for the candy.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create the Instance Object (Sugar Crystal) ===
    # Creating with size=0.05 natively applies the scale as 1.0, avoiding the
    # scale mismatch issue highlighted in the tutorial.
    bpy.ops.mesh.primitive_cube_add(size=0.05, location=(location[0], location[1], location[2] - 5))
    sugar_obj = bpy.context.active_object
    sugar_obj.name = f"{object_name}_Crystal"
    
    # Hide the original instance object from view and render
    sugar_obj.hide_viewport = True
    sugar_obj.hide_render = True
    
    # Sugar Material (Glassy/White)
    sugar_mat = bpy.data.materials.new(name=f"{object_name}_SugarMat")
    sugar_mat.use_nodes = True
    bsdf = sugar_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.95, 0.95, 0.95, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.1
        # Handle API differences between Blender 4.0+ and older versions
        if 'Transmission Weight' in bsdf.inputs:
            bsdf.inputs['Transmission Weight'].default_value = 0.8
        elif 'Transmission' in bsdf.inputs:
            bsdf.inputs['Transmission'].default_value = 0.8
    sugar_obj.data.materials.append(sugar_mat)

    # === Step 2: Create the Base Mesh (Candy Torus) ===
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.0, 
        minor_radius=0.4, 
        major_segments=64, 
        minor_segments=32,
        location=location
    )
    candy_obj = bpy.context.active_object
    candy_obj.name = object_name
    bpy.ops.object.shade_smooth()

    # Candy Material
    candy_mat = bpy.data.materials.new(name=f"{object_name}_BaseMat")
    candy_mat.use_nodes = True
    candy_bsdf = candy_mat.node_tree.nodes.get("Principled BSDF")
    if candy_bsdf:
        color_with_alpha = (*material_color, 1.0) if len(material_color) == 3 else material_color
        candy_bsdf.inputs['Base Color'].default_value = color_with_alpha
        candy_bsdf.inputs['Roughness'].default_value = 0.4
    candy_obj.data.materials.append(candy_mat)

    # === Step 3: Geometry Nodes Setup ===
    modifier = candy_obj.modifiers.new(name="SugarCoating", type='NODES')
    tree = bpy.data.node_groups.new(name=f"{object_name}_GeoNodes", type='GeometryNodeTree')
    modifier.node_group = tree

    # Define interface safely across Blender versions
    if hasattr(tree, "interface"):
        tree.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        tree.inputs.new('NodeSocketGeometry', "Geometry")
        tree.outputs.new('NodeSocketGeometry', "Geometry")

    nodes = tree.nodes
    links = tree.links

    # Create Nodes
    group_in = nodes.new('NodeGroupInput')
    group_out = nodes.new('NodeGroupOutput')
    
    distribute = nodes.new('GeometryNodeDistributePointsOnFaces')
    distribute.inputs['Density'].default_value = 3500.0  # High density for coating

    instance = nodes.new('GeometryNodeInstanceOnPoints')
    join = nodes.new('GeometryNodeJoinGeometry')
    
    obj_info = nodes.new('GeometryNodeObjectInfo')
    obj_info.inputs['Object'].default_value = sugar_obj
    obj_info.transform_space = 'RELATIVE'

    # Random Rotation Vector (Max set to Tau / 2*Pi for full 360 degree randomization)
    rand_rot = nodes.new('FunctionNodeRandomValue')
    rand_rot.data_type = 'FLOAT_VECTOR'
    tau = math.pi * 2
    rand_rot.inputs['Max'].default_value = (tau, tau, tau)

    # Random Scale Float
    rand_scale = nodes.new('FunctionNodeRandomValue')
    rand_scale.data_type = 'FLOAT'
    rand_scale.inputs['Min'].default_value = 0.4
    rand_scale.inputs['Max'].default_value = 1.6

    # Node Placement (Cosmetic for graph editor)
    group_in.location = (-600, 0)
    distribute.location = (-400, 100)
    obj_info.location = (-400, -100)
    rand_rot.location = (-400, -300)
    rand_scale.location = (-400, -500)
    instance.location = (-200, 0)
    join.location = (0, 0)
    group_out.location = (200, 0)

    # Link Nodes
    links.new(group_in.outputs['Geometry'], join.inputs['Geometry'])  # Keep original mesh
    links.new(group_in.outputs['Geometry'], distribute.inputs['Mesh']) # Generate points
    links.new(distribute.outputs['Points'], instance.inputs['Points'])
    links.new(obj_info.outputs['Geometry'], instance.inputs['Instance'])
    links.new(rand_rot.outputs['Value'], instance.inputs['Rotation'])
    links.new(rand_scale.outputs['Value'], instance.inputs['Scale'])
    links.new(instance.outputs['Instances'], join.inputs['Geometry'])  # Combine instances
    links.new(join.outputs['Geometry'], group_out.inputs['Geometry'])  # Output to viewport

    # === Step 4: Finalize Scale ===
    candy_obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' (Sugar-Coated Candy) at {location} utilizing Geometry Nodes for procedural scattering."
