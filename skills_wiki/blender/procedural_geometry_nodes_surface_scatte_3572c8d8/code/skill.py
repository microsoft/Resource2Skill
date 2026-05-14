def create_object(
    scene_name: str = "Scene",
    object_name: str = "SugarCandy",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.05, 0.1),
    **kwargs,
) -> str:
    """
    Create a procedurally sugar-coated candy (torus) using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created candy object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the jelly candy.
        **kwargs: density (int) to control the amount of sugar crystals.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    density = kwargs.get("density", 3000.0)

    # === Step 1: Create Materials ===
    
    # 1a. Candy Jelly Material
    jelly_mat = bpy.data.materials.new(name=f"{object_name}_JellyMat")
    jelly_mat.use_nodes = True
    jelly_bsdf = jelly_mat.node_tree.nodes.get("Principled BSDF")
    if jelly_bsdf:
        jelly_bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        jelly_bsdf.inputs["Roughness"].default_value = 0.15
        # Handle API change for Transmission in Blender 4.0+ vs 3.x
        if "Transmission Weight" in jelly_bsdf.inputs:
            jelly_bsdf.inputs["Transmission Weight"].default_value = 1.0
        elif "Transmission" in jelly_bsdf.inputs:
            jelly_bsdf.inputs["Transmission"].default_value = 1.0

    # 1b. Sugar Crystal Material
    sugar_mat = bpy.data.materials.new(name=f"{object_name}_SugarMat")
    sugar_mat.use_nodes = True
    sugar_bsdf = sugar_mat.node_tree.nodes.get("Principled BSDF")
    if sugar_bsdf:
        sugar_bsdf.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0)
        sugar_bsdf.inputs["Roughness"].default_value = 0.05
        sugar_bsdf.inputs["IOR"].default_value = 1.45
        if "Transmission Weight" in sugar_bsdf.inputs:
            sugar_bsdf.inputs["Transmission Weight"].default_value = 1.0
        elif "Transmission" in sugar_bsdf.inputs:
            sugar_bsdf.inputs["Transmission"].default_value = 1.0

    # === Step 2: Create Instance Object (Sugar Crystal) ===
    # Create a small cube to act as the crystal instance
    bpy.ops.mesh.primitive_cube_add(size=0.05, location=(0, 0, 0))
    crystal_obj = bpy.context.active_object
    crystal_obj.name = f"{object_name}_Crystal_Instance"
    crystal_obj.data.materials.append(sugar_mat)
    
    # Hide the source crystal from the render and viewport (it's only an instance source)
    crystal_obj.hide_viewport = True
    crystal_obj.hide_render = True
    
    # === Step 3: Create Base Object (Candy) ===
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.0, 
        minor_radius=0.4, 
        major_segments=48, 
        minor_segments=24, 
        location=location
    )
    candy_obj = bpy.context.active_object
    candy_obj.name = object_name
    candy_obj.scale = (scale, scale, scale)
    
    # Shade smooth
    for poly in candy_obj.data.polygons:
        poly.use_smooth = True
        
    candy_obj.data.materials.append(jelly_mat)
    
    # Add Subdivision Surface
    subsurf = candy_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # === Step 4: Build Geometry Nodes Tree ===
    gn_mod = candy_obj.modifiers.new(name="SugarCoating", type='NODES')
    gn_tree = bpy.data.node_groups.new(name=f"{object_name}_NodeTree", type='GeometryNodeTree')
    gn_mod.node_group = gn_tree
    
    # Create I/O interface (Blender 4.0+ vs 3.x compatibility)
    if hasattr(gn_tree, "interface"):
        gn_tree.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        gn_tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        gn_tree.inputs.new('NodeSocketGeometry', 'Geometry')
        gn_tree.outputs.new('NodeSocketGeometry', 'Geometry')

    nodes = gn_tree.nodes
    links = gn_tree.links

    # 4a. Add Nodes
    node_in = nodes.new('NodeGroupInput')
    node_out = nodes.new('NodeGroupOutput')
    
    distribute = nodes.new('GeometryNodeDistributePointsOnFaces')
    distribute.inputs['Density'].default_value = density
    
    instance = nodes.new('GeometryNodeInstanceOnPoints')
    join = nodes.new('GeometryNodeJoinGeometry')
    
    obj_info = nodes.new('GeometryNodeObjectInfo')
    obj_info.inputs['Object'].default_value = crystal_obj
    obj_info.transform_space = 'RELATIVE'
    
    rand_rot = nodes.new('FunctionNodeRandomValue')
    rand_rot.data_type = 'FLOAT_VECTOR'
    # Math.tau is ~6.283 (360 degrees in radians)
    tau = math.tau
    rand_rot.inputs['Max'].default_value = (tau, tau, tau)
    
    rand_scale = nodes.new('FunctionNodeRandomValue')
    rand_scale.data_type = 'FLOAT'
    rand_scale.inputs['Min'].default_value = 0.5
    rand_scale.inputs['Max'].default_value = 1.5

    # 4b. Position Nodes (Visual layout, mostly for user inspection)
    node_in.location = (-400, 0)
    distribute.location = (-200, 100)
    obj_info.location = (-200, -100)
    rand_rot.location = (-200, -300)
    rand_scale.location = (-200, -500)
    instance.location = (50, 100)
    join.location = (250, 0)
    node_out.location = (450, 0)

    # 4c. Link Nodes
    links.new(node_in.outputs[0], distribute.inputs['Mesh'])            # Input -> Distribute
    links.new(node_in.outputs[0], join.inputs['Geometry'])              # Input -> Join (Preserves Base Mesh)
    
    links.new(distribute.outputs['Points'], instance.inputs['Points'])  # Distribute -> Instance
    links.new(obj_info.outputs['Geometry'], instance.inputs['Instance'])# ObjInfo -> Instance
    
    links.new(rand_rot.outputs['Value'], instance.inputs['Rotation'])   # Rand Rot -> Instance Rot
    links.new(rand_scale.outputs['Value'], instance.inputs['Scale'])    # Rand Scale -> Instance Scale
    
    links.new(instance.outputs['Geometry'], join.inputs['Geometry'])    # Instance -> Join
    links.new(join.outputs['Geometry'], node_out.inputs[0])             # Join -> Output

    # Deselect all and make our primary object active
    bpy.ops.object.select_all(action='DESELECT')
    candy_obj.select_set(True)
    bpy.context.view_layer.objects.active = candy_obj

    return f"Created '{object_name}' (sugar-coated jelly) at {location} using Geometry Nodes for scattering."
