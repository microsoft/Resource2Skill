def create_object(
    scene_name: str = "Scene",
    object_name: str = "SugarCandy",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.05, 0.1),
    **kwargs,
) -> str:
    """
    Create a procedural sugar-coated candy using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the gummy candy.
        **kwargs: Optional overrides (e.g., density=5000).

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Create Materials ===
    # 1A. Gummy Base Material
    gummy_mat = bpy.data.materials.new(name=f"{object_name}_Gummy")
    gummy_mat.use_nodes = True
    g_bsdf = gummy_mat.node_tree.nodes.get("Principled BSDF")
    if g_bsdf:
        g_bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        if bpy.app.version >= (4, 0, 0):
            g_bsdf.inputs['Roughness'].default_value = 0.4
            g_bsdf.inputs['Subsurface Weight'].default_value = 1.0
            g_bsdf.inputs['Subsurface Radius'].default_value = (0.2, 0.2, 0.2)
            g_bsdf.inputs['Subsurface Scale'].default_value = 0.1
        else:
            g_bsdf.inputs['Roughness'].default_value = 0.4
            g_bsdf.inputs['Subsurface'].default_value = 1.0
            g_bsdf.inputs['Subsurface Radius'].default_value = (0.2, 0.2, 0.2)
            g_bsdf.inputs['Subsurface Color'].default_value = (*material_color, 1.0)

    # 1B. Sugar Crystal Material
    sugar_mat = bpy.data.materials.new(name=f"{object_name}_Sugar")
    sugar_mat.use_nodes = True
    s_bsdf = sugar_mat.node_tree.nodes.get("Principled BSDF")
    if s_bsdf:
        s_bsdf.inputs['Base Color'].default_value = (0.95, 0.95, 0.95, 1.0)
        if bpy.app.version >= (4, 0, 0):
            s_bsdf.inputs['Transmission Weight'].default_value = 1.0
            s_bsdf.inputs['Roughness'].default_value = 0.1
            s_bsdf.inputs['IOR'].default_value = 1.5
        else:
            s_bsdf.inputs['Transmission'].default_value = 1.0
            s_bsdf.inputs['Roughness'].default_value = 0.1
            s_bsdf.inputs['IOR'].default_value = 1.5

    # === Step 2: Create Instance Object (Sugar Crystal) ===
    bpy.ops.mesh.primitive_cube_add(size=0.03, location=(0, 0, 0))
    crystal_obj = bpy.context.active_object
    crystal_obj.name = f"{object_name}_CrystalRef"
    crystal_obj.data.materials.append(sugar_mat)
    # Hide the reference crystal from the viewport and render
    crystal_obj.hide_viewport = True
    crystal_obj.hide_render = True

    # === Step 3: Create Base Object (Candy Ring) ===
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.0, 
        minor_radius=0.4, 
        major_segments=48, 
        minor_segments=24,
        location=location
    )
    base_obj = bpy.context.active_object
    base_obj.name = object_name
    base_obj.data.materials.append(gummy_mat)
    
    # Shade smooth
    for poly in base_obj.data.polygons:
        poly.use_smooth = True

    # === Step 4: Build Geometry Nodes Setup ===
    node_tree = bpy.data.node_groups.new(name=f"{object_name}_GeoNodes", type='GeometryNodeTree')
    
    # Handle interface creation for different Blender versions
    if bpy.app.version >= (4, 0, 0):
        node_tree.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        node_tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        node_tree.inputs.new('NodeSocketGeometry', "Geometry")
        node_tree.outputs.new('NodeSocketGeometry', "Geometry")

    nodes = node_tree.nodes
    links = node_tree.links

    # Create Nodes
    group_in = nodes.new('NodeGroupInput')
    group_out = nodes.new('NodeGroupOutput')
    
    distribute = nodes.new('GeometryNodeDistributePointsOnFaces')
    distribute.inputs['Density'].default_value = kwargs.get('density', 4000.0)
    
    instance = nodes.new('GeometryNodeInstanceOnPoints')
    
    obj_info = nodes.new('GeometryNodeObjectInfo')
    obj_info.inputs['Object'].default_value = crystal_obj
    
    # Rotation Randomizer (Vector mode, 0 to 2*PI radians for full spherical rotation)
    rand_rot = nodes.new('FunctionNodeRandomValue')
    rand_rot.data_type = 'FLOAT_VECTOR'
    rand_rot.inputs['Min'].default_value = (0.0, 0.0, 0.0)
    rand_rot.inputs['Max'].default_value = (math.tau, math.tau, math.tau)
    
    # Scale Randomizer (Float mode)
    rand_scale = nodes.new('FunctionNodeRandomValue')
    rand_scale.data_type = 'FLOAT'
    rand_scale.inputs['Min'].default_value = 0.4
    rand_scale.inputs['Max'].default_value = 1.6
    
    join = nodes.new('GeometryNodeJoinGeometry')
    
    # Link Nodes
    links.new(group_in.outputs[0], distribute.inputs[0]) 
    links.new(distribute.outputs['Points'], instance.inputs['Points'])
    links.new(obj_info.outputs['Geometry'], instance.inputs['Instance'])
    links.new(rand_rot.outputs['Value'], instance.inputs['Rotation'])
    links.new(rand_scale.outputs['Value'], instance.inputs['Scale'])
    
    # Join original mesh and the scattered instances
    links.new(group_in.outputs[0], join.inputs['Geometry'])
    links.new(instance.outputs[0], join.inputs['Geometry'])
    
    links.new(join.outputs['Geometry'], group_out.inputs[0])

    # === Step 5: Finalize & Apply Modifiers ===
    mod = base_obj.modifiers.new(name="Sugar Scatter", type='NODES')
    mod.node_group = node_tree
    
    base_obj.scale = (scale, scale, scale)
    
    # Optional: Subdivide to make the base smoother before points are scattered
    subdiv = base_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.levels = 2
    bpy.ops.object.modifier_move_up(modifier="Subdivision") # Move before GeoNodes

    return f"Created '{object_name}' with procedural sugar coating at {location}"
