def create_object(
    scene_name: str = "Scene",
    object_name: str = "SugarCandy",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.05, 0.05),
    **kwargs,
) -> str:
    """
    Create a procedurally sugar-coated object using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created base object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color in 0-1 range for the gummy core.
        **kwargs: 'density' can be passed to control the number of sugar crystals (default 5000).

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Instance Object (Sugar Crystal) ===
    crystal_name = f"{object_name}_Crystal"
    bpy.ops.mesh.primitive_cube_add(size=0.1)
    crystal_obj = bpy.context.active_object
    crystal_obj.name = crystal_name
    
    # Hide crystal from the viewport and render, as it's only used as a source instance
    crystal_obj.hide_viewport = True
    crystal_obj.hide_render = True
    crystal_obj.hide_set(True)

    # Crystal Material (Transmissive/Glassy)
    crystal_mat = bpy.data.materials.new(name=f"{crystal_name}_Mat")
    crystal_mat.use_nodes = True
    c_bsdf = crystal_mat.node_tree.nodes.get("Principled BSDF")
    if c_bsdf:
        c_bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
        if 'Roughness' in c_bsdf.inputs:
            c_bsdf.inputs['Roughness'].default_value = 0.1
        # Handle Blender version differences for Transmission
        if 'Transmission Weight' in c_bsdf.inputs: # 4.0+
            c_bsdf.inputs['Transmission Weight'].default_value = 0.9
        elif 'Transmission' in c_bsdf.inputs: # < 4.0
            c_bsdf.inputs['Transmission'].default_value = 0.9
            
    if crystal_obj.data.materials:
        crystal_obj.data.materials[0] = crystal_mat
    else:
        crystal_obj.data.materials.append(crystal_mat)

    # === Step 2: Create Base Mesh (Candy Torus) ===
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.4, major_segments=48, minor_segments=24)
    candy_obj = bpy.context.active_object
    candy_obj.name = object_name
    bpy.ops.object.shade_smooth()

    # Apply Subdivision Surface
    subsurf = candy_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # Candy Material (Subsurface Gummy)
    candy_mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    candy_mat.use_nodes = True
    bsdf = candy_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        if 'Roughness' in bsdf.inputs:
            bsdf.inputs['Roughness'].default_value = 0.3
        
        # Handle Blender version differences for Subsurface Scattering
        if 'Subsurface Weight' in bsdf.inputs: # 4.0+
            bsdf.inputs['Subsurface Weight'].default_value = 1.0
            bsdf.inputs['Subsurface Radius'].default_value = (0.2, 0.05, 0.05)
        elif 'Subsurface' in bsdf.inputs: # < 4.0
            bsdf.inputs['Subsurface'].default_value = 1.0
            if 'Subsurface Radius' in bsdf.inputs:
                bsdf.inputs['Subsurface Radius'].default_value = (0.2, 0.05, 0.05)
            
    if candy_obj.data.materials:
        candy_obj.data.materials[0] = candy_mat
    else:
        candy_obj.data.materials.append(candy_mat)

    # === Step 3: Geometry Nodes Scattering Logic ===
    geo_mod = candy_obj.modifiers.new(name="SugarCoating", type='NODES')
    group = bpy.data.node_groups.new(f"{object_name}_GeoTree", 'GeometryNodeTree')
    geo_mod.node_group = group

    # Setup Interface
    if hasattr(group, "interface"): # Blender 4.0+
        group.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else: # Older versions
        group.inputs.new('NodeSocketGeometry', "Geometry")
        group.outputs.new('NodeSocketGeometry', "Geometry")

    nodes = group.nodes
    links = group.links

    # Create Nodes
    node_input = nodes.new('NodeGroupInput')
    node_input.location = (-400, 0)
    
    node_output = nodes.new('NodeGroupOutput')
    node_output.location = (600, 0)

    distribute = nodes.new('GeometryNodeDistributePointsOnFaces')
    distribute.location = (-200, 100)
    distribute.inputs['Density'].default_value = kwargs.get('density', 5000.0)

    instance = nodes.new('GeometryNodeInstanceOnPoints')
    instance.location = (200, 100)

    join = nodes.new('GeometryNodeJoinGeometry')
    join.location = (400, 0)

    obj_info = nodes.new('GeometryNodeObjectInfo')
    obj_info.location = (-200, -200)
    obj_info.inputs['Object'].default_value = crystal_obj
    obj_info.transform_space = 'RELATIVE'

    # Random Rotation (0 to Tau/2*Pi for full 360-degree chaos on all axes)
    random_rot = nodes.new('FunctionNodeRandomValue')
    random_rot.location = (-100, -400)
    random_rot.data_type = 'FLOAT_VECTOR'
    random_rot.inputs['Min'].default_value = (0.0, 0.0, 0.0)
    random_rot.inputs['Max'].default_value = (math.tau, math.tau, math.tau)

    # Random Scale
    random_scale = nodes.new('FunctionNodeRandomValue')
    random_scale.location = (-100, -600)
    random_scale.data_type = 'FLOAT'
    random_scale.inputs['Min'].default_value = 0.05
    random_scale.inputs['Max'].default_value = 0.15

    # Connect Node Logic
    links.new(node_input.outputs[0], distribute.inputs['Mesh'])
    links.new(node_input.outputs[0], join.inputs['Geometry'])  # Connect original mesh to output
    links.new(distribute.outputs['Points'], instance.inputs['Points'])
    
    # Safely connect instance geometry
    inst_geo_out = obj_info.outputs.get('Geometry') or obj_info.outputs[0]
    links.new(inst_geo_out, instance.inputs['Instance'])
    
    links.new(random_rot.outputs['Value'], instance.inputs['Rotation'])
    links.new(random_scale.outputs['Value'], instance.inputs['Scale'])
    
    links.new(instance.outputs['Instances'], join.inputs['Geometry'])
    links.new(join.outputs['Geometry'], node_output.inputs[0])

    # === Step 4: Finalize Position & Scale ===
    candy_obj.location = Vector(location)
    candy_obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' at {location} configured with a Procedural Scattering Node Tree."
