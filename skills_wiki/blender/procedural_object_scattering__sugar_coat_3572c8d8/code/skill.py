def create_sugar_coated_candy(
    scene_name: str = "Scene",
    object_name: str = "SugarCandy",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.05, 0.05),
    **kwargs,
) -> str:
    """
    Create a procedural sugar-coated candy using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created candy object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the gummy candy.
        **kwargs: Additional overrides (e.g., density).

    Returns:
        Status string confirming creation.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    crystal_density = kwargs.get("density", 2500.0)

    # === Step 1: Create the Source Crystal Geometry ===
    # This is the object that will be scattered (instanced)
    bpy.ops.mesh.primitive_cube_add(size=0.03, location=(0, 0, 0))
    crystal = bpy.context.active_object
    crystal.name = f"{object_name}_SugarCrystal"
    
    # Bevel for a realistic crystal look
    bevel = crystal.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.005
    bevel.segments = 2
    bpy.ops.object.shade_smooth()
    
    # Hide the source object
    crystal.hide_set(True)
    crystal.hide_render = True

    # === Step 2: Create the Base Candy Geometry ===
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.0, 
        minor_radius=0.45, 
        major_segments=64, 
        minor_segments=32,
        location=location
    )
    candy = bpy.context.active_object
    candy.name = object_name
    candy.scale = (scale, scale, scale)
    bpy.ops.object.shade_smooth()

    # Subsurf modifier to make the candy base smooth
    subsurf = candy.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # === Step 3: Build Geometry Nodes System ===
    geonodes_mod = candy.modifiers.new(name="SugarCoating", type='NODES')
    node_group = bpy.data.node_groups.new(name=f"{object_name}_GeoNodes", type='GeometryNodeTree')
    geonodes_mod.node_group = node_group

    # Compatibility for Node Group I/O in Blender 4.0+ vs 3.x
    if hasattr(node_group, "interface"):
        node_group.interface.new_socket(name="Geometry", in_out='IN', socket_type='NodeSocketGeometry')
        node_group.interface.new_socket(name="Geometry", in_out='OUT', socket_type='NodeSocketGeometry')
    else:
        node_group.inputs.new('NodeSocketGeometry', "Geometry")
        node_group.outputs.new('NodeSocketGeometry', "Geometry")

    nodes = node_group.nodes
    links = node_group.links

    # Create Nodes
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-400, 0)
    
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (400, 0)

    distribute = nodes.new('GeometryNodeDistributePointsOnFaces')
    distribute.location = (-200, 100)
    distribute.inputs['Density'].default_value = crystal_density

    instance = nodes.new('GeometryNodeInstanceOnPoints')
    instance.location = (0, 100)

    join = nodes.new('GeometryNodeJoinGeometry')
    join.location = (200, 0)

    obj_info = nodes.new('GeometryNodeObjectInfo')
    obj_info.location = (-200, -100)
    obj_info.inputs['Object'].default_value = crystal
    obj_info.transform_space = 'ORIGINAL'  # Use local geometry data without moving it

    rand_rot = nodes.new('FunctionNodeRandomValue')
    rand_rot.location = (-200, -300)
    rand_rot.data_type = 'FLOAT_VECTOR'
    # Use math.tau (2 * pi) for full 360-degree rotation in radians
    rand_rot.inputs['Min'].default_value = (0.0, 0.0, 0.0)
    rand_rot.inputs['Max'].default_value = (math.tau, math.tau, math.tau)

    rand_scale = nodes.new('FunctionNodeRandomValue')
    rand_scale.location = (-200, -500)
    rand_scale.data_type = 'FLOAT'
    rand_scale.inputs['Min'].default_value = 0.2
    rand_scale.inputs['Max'].default_value = 1.0

    # Link Nodes together
    links.new(input_node.outputs['Geometry'], distribute.inputs['Mesh'])
    links.new(distribute.outputs['Points'], instance.inputs['Points'])
    links.new(obj_info.outputs['Geometry'], instance.inputs['Instance'])
    links.new(rand_rot.outputs['Value'], instance.inputs['Rotation'])
    links.new(rand_scale.outputs['Value'], instance.inputs['Scale'])
    
    # Join original mesh with the new instances
    links.new(input_node.outputs['Geometry'], join.inputs['Geometry'])
    links.new(instance.outputs['Instances'], join.inputs['Geometry'])
    links.new(join.outputs['Geometry'], output_node.inputs['Geometry'])

    # === Step 4: Build & Assign Materials ===
    
    # 1. Candy Base Material (Red, Subsurface Gummy)
    mat_candy = bpy.data.materials.new(name=f"{object_name}_CandyMat")
    mat_candy.use_nodes = True
    bsdf_c = mat_candy.node_tree.nodes.get('Principled BSDF')
    if bsdf_c:
        base_color = (material_color[0], material_color[1], material_color[2], 1.0)
        bsdf_c.inputs['Base Color'].default_value = base_color
        bsdf_c.inputs['Roughness'].default_value = 0.3
        
        # Handle Subsurface differences between Blender 4.0+ and 3.x
        if 'Subsurface Weight' in bsdf_c.inputs: 
            bsdf_c.inputs['Subsurface Weight'].default_value = 1.0
            bsdf_c.inputs['Subsurface Radius'].default_value = (1.0, 0.2, 0.1)
        elif 'Subsurface' in bsdf_c.inputs:
            bsdf_c.inputs['Subsurface'].default_value = 1.0
            bsdf_c.inputs['Subsurface Radius'].default_value = (1.0, 0.2, 0.1)
            bsdf_c.inputs['Subsurface Color'].default_value = base_color

    candy.data.materials.append(mat_candy)

    # 2. Sugar Crystal Material (Glassy, Transparent)
    mat_sugar = bpy.data.materials.new(name=f"{object_name}_SugarMat")
    mat_sugar.use_nodes = True
    bsdf_s = mat_sugar.node_tree.nodes.get('Principled BSDF')
    if bsdf_s:
        bsdf_s.inputs['Base Color'].default_value = (0.95, 0.95, 0.95, 1.0)
        bsdf_s.inputs['Roughness'].default_value = 0.1
        bsdf_s.inputs['IOR'].default_value = 1.45
        
        if 'Transmission Weight' in bsdf_s.inputs:
            bsdf_s.inputs['Transmission Weight'].default_value = 1.0
        elif 'Transmission' in bsdf_s.inputs:
            bsdf_s.inputs['Transmission'].default_value = 1.0
            
    crystal.data.materials.append(mat_sugar)

    return f"Created '{candy.name}' (Sugar-Coated Candy) at {location} populated with ~{int(crystal_density)} crystals."
