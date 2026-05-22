def create_object(
    scene_name: str = "Scene",
    object_name: str = "CandyDonut",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.05, 0.1),
    **kwargs,
) -> str:
    """
    Create a Procedural Sugar-Coated Candy using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
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

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Create Materials ===
    
    # 1a. Candy Material (Transmissive)
    mat_candy = bpy.data.materials.new(name=f"{object_name}_CandyMat")
    mat_candy.use_nodes = True
    bsdf_candy = mat_candy.node_tree.nodes.get("Principled BSDF")
    if bsdf_candy:
        # Support for both Blender 3.x and 4.x BSDF socket names
        if 'Transmission Weight' in bsdf_candy.inputs:
            bsdf_candy.inputs['Base Color'].default_value = (*material_color, 1.0)
            bsdf_candy.inputs['Transmission Weight'].default_value = 1.0
            bsdf_candy.inputs['Roughness'].default_value = 0.15
            bsdf_candy.inputs['IOR'].default_value = 1.45
        else:
            bsdf_candy.inputs['Base Color'].default_value = (*material_color, 1.0)
            bsdf_candy.inputs['Transmission'].default_value = 1.0
            bsdf_candy.inputs['Roughness'].default_value = 0.15
            bsdf_candy.inputs['IOR'].default_value = 1.45

    # 1b. Sugar Crystal Material (Rough Transmissive)
    mat_sugar = bpy.data.materials.new(name=f"{object_name}_SugarMat")
    mat_sugar.use_nodes = True
    bsdf_sugar = mat_sugar.node_tree.nodes.get("Principled BSDF")
    if bsdf_sugar:
        if 'Transmission Weight' in bsdf_sugar.inputs:
            bsdf_sugar.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)
            bsdf_sugar.inputs['Transmission Weight'].default_value = 0.9
            bsdf_sugar.inputs['Roughness'].default_value = 0.3
        else:
            bsdf_sugar.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)
            bsdf_sugar.inputs['Transmission'].default_value = 0.9
            bsdf_sugar.inputs['Roughness'].default_value = 0.3

    # === Step 2: Create Instance Object (Sugar Crystal) ===
    bpy.ops.mesh.primitive_cube_add(size=0.05, location=(0, 0, 0))
    sugar_crystal = bpy.context.active_object
    sugar_crystal.name = f"{object_name}_SugarCrystal"
    sugar_crystal.data.materials.append(mat_sugar)
    # Hide the source instance from the viewport and render
    sugar_crystal.hide_set(True)
    sugar_crystal.hide_render = True

    # === Step 3: Create Base Object (Candy Donut) ===
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.4, location=location)
    main_obj = bpy.context.active_object
    main_obj.name = object_name
    main_obj.scale = (scale, scale, scale)
    main_obj.data.materials.append(mat_candy)
    
    # Smooth base geometry
    subsurf = main_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2
    bpy.ops.object.shade_smooth()

    # === Step 4: Build Geometry Nodes Tree ===
    gn_tree = bpy.data.node_groups.new(name=f"{object_name}_SugarCoating", type="GeometryNodeTree")
    
    # Initialize Tree Interface (Compatible with 3.x and 4.x)
    if hasattr(gn_tree, "interface"):
        gn_tree.interface.new_socket(name="Geometry", in_out="IN", socket_type="NodeSocketGeometry")
        gn_tree.interface.new_socket(name="Geometry", in_out="OUT", socket_type="NodeSocketGeometry")
    else:
        gn_tree.inputs.new("NodeSocketGeometry", "Geometry")
        gn_tree.outputs.new("NodeSocketGeometry", "Geometry")

    nodes = gn_tree.nodes
    links = gn_tree.links

    node_in = nodes.new("NodeGroupInput")
    node_out = nodes.new("NodeGroupOutput")

    # Core scattering nodes
    node_distribute = nodes.new("GeometryNodeDistributePointsOnFaces")
    node_distribute.inputs["Density"].default_value = 2000.0  # High density for sugar
    
    node_instance = nodes.new("GeometryNodeInstanceOnPoints")
    node_join = nodes.new("GeometryNodeJoinGeometry")
    
    # Object reference node
    node_obj_info = nodes.new("GeometryNodeObjectInfo")
    node_obj_info.inputs["Object"].default_value = sugar_crystal
    node_obj_info.transform_space = 'RELATIVE'

    # Randomization nodes
    node_rand_rot = nodes.new("FunctionNodeRandomValue")
    node_rand_rot.data_type = 'FLOAT_VECTOR'
    node_rand_rot.inputs[0].default_value = (0.0, 0.0, 0.0) # Min
    # math.tau gives full 360 degree randomization on all axes
    node_rand_rot.inputs[1].default_value = (math.tau, math.tau, math.tau) # Max

    node_rand_scale = nodes.new("FunctionNodeRandomValue")
    node_rand_scale.data_type = 'FLOAT'
    node_rand_scale.inputs[0].default_value = 0.05  # Min scale
    node_rand_scale.inputs[1].default_value = 0.15  # Max scale

    # Connect the network
    links.new(node_in.outputs["Geometry"], node_distribute.inputs["Mesh"])
    links.new(node_distribute.outputs["Points"], node_instance.inputs["Points"])
    
    links.new(node_obj_info.outputs["Geometry"], node_instance.inputs["Instance"])
    links.new(node_rand_rot.outputs["Value"], node_instance.inputs["Rotation"])
    links.new(node_rand_scale.outputs["Value"], node_instance.inputs["Scale"])
    
    # Join original mesh with the new instances
    links.new(node_in.outputs["Geometry"], node_join.inputs["Geometry"])
    links.new(node_instance.outputs["Instances"], node_join.inputs["Geometry"])
    
    links.new(node_join.outputs["Geometry"], node_out.inputs["Geometry"])

    # === Step 5: Assign Modifier ===
    gn_mod = main_obj.modifiers.new(name="SugarCoating", type='NODES')
    gn_mod.node_group = gn_tree

    # Link to scene collection if not already handled by context
    if main_obj.name not in scene.collection.objects:
        scene.collection.objects.link(main_obj)
    if sugar_crystal.name not in scene.collection.objects:
        scene.collection.objects.link(sugar_crystal)

    return f"Created procedural sugar-coated '{object_name}' at {location}."
