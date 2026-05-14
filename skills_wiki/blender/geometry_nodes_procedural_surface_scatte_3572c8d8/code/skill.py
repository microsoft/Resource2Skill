def create_object(
    scene_name: str = "Scene",
    object_name: str = "SugarCandyRing",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.05, 0.05),
    sugar_density: float = 3000.0,
    **kwargs,
) -> str:
    """
    Create a procedural sugar-coated candy using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created candy object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the jelly candy.
        sugar_density: Density of the scattered sugar crystals.
        **kwargs: Additional overrides.

    Returns:
        Status string confirming creation.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Materials ===
    
    # 1A. Sugar Crystal Material
    sugar_mat = bpy.data.materials.new(name=f"{object_name}_Sugar_Mat")
    sugar_mat.use_nodes = True
    sugar_bsdf = sugar_mat.node_tree.nodes.get("Principled BSDF")
    if sugar_bsdf:
        sugar_bsdf.inputs['Base Color'].default_value = (0.95, 0.95, 0.95, 1.0)
        sugar_bsdf.inputs['Roughness'].default_value = 0.4
        if 'Transmission Weight' in sugar_bsdf.inputs:  # Blender 4.0+
            sugar_bsdf.inputs['Transmission Weight'].default_value = 1.0
        elif 'Transmission' in sugar_bsdf.inputs:       # Blender 3.x
            sugar_bsdf.inputs['Transmission'].default_value = 1.0
        if 'IOR' in sugar_bsdf.inputs:
            sugar_bsdf.inputs['IOR'].default_value = 1.53

    # 1B. Base Candy Material
    candy_mat = bpy.data.materials.new(name=f"{object_name}_Jelly_Mat")
    candy_mat.use_nodes = True
    candy_bsdf = candy_mat.node_tree.nodes.get("Principled BSDF")
    if candy_bsdf:
        candy_bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        candy_bsdf.inputs['Roughness'].default_value = 0.15
        
        # Cross-version compatibility for Transmission & Subsurface
        if 'Transmission Weight' in candy_bsdf.inputs:
            candy_bsdf.inputs['Transmission Weight'].default_value = 0.9
        elif 'Transmission' in candy_bsdf.inputs:
            candy_bsdf.inputs['Transmission'].default_value = 0.9

        if 'Subsurface Weight' in candy_bsdf.inputs:
            candy_bsdf.inputs['Subsurface Weight'].default_value = 0.8
            candy_bsdf.inputs['Subsurface Radius'].default_value = (0.2, 0.05, 0.05)
        elif 'Subsurface' in candy_bsdf.inputs:
            candy_bsdf.inputs['Subsurface'].default_value = 0.8
            candy_bsdf.inputs['Subsurface Radius'].default_value = (0.2, 0.05, 0.05)

    # === Step 2: Create Instance Object (Sugar Crystal) ===
    bpy.ops.mesh.primitive_icosphere_add(subdivisions=1, radius=0.015, location=(0, 0, -10))
    crystal_obj = bpy.context.active_object
    crystal_obj.name = f"{object_name}_Crystal_Instance"
    crystal_obj.data.materials.append(sugar_mat)
    # Hide the source instance from viewport and render
    crystal_obj.hide_viewport = True
    crystal_obj.hide_render = True

    # === Step 3: Create Main Base Object (Candy Ring) ===
    bpy.ops.mesh.primitive_torus_add(major_radius=0.5, minor_radius=0.25, location=location)
    candy_obj = bpy.context.active_object
    candy_obj.name = object_name
    candy_obj.data.materials.append(candy_mat)
    bpy.ops.object.shade_smooth()
    
    # Apply global scale
    candy_obj.scale = (scale, scale, scale)

    # Add Subdivision Surface for a smooth candy look
    subsurf_mod = candy_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf_mod.levels = 2
    subsurf_mod.render_levels = 2

    # === Step 4: Build Geometry Nodes Modifier ===
    gn_mod = candy_obj.modifiers.new(name="Sugar_Coating_Scattering", type='NODES')
    gn_tree = bpy.data.node_groups.new(name=f"{object_name}_GN_Tree", type='GeometryNodeTree')
    gn_mod.node_group = gn_tree

    # Handle cross-version node interface creation (3.x vs 4.0+)
    if hasattr(gn_tree, "interface"):
        gn_tree.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        gn_tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        gn_tree.inputs.new('NodeSocketGeometry', "Geometry")
        gn_tree.outputs.new('NodeSocketGeometry', "Geometry")

    # Add nodes
    nodes = gn_tree.nodes
    node_input = nodes.new('NodeGroupInput')
    node_output = nodes.new('NodeGroupOutput')
    
    node_distribute = nodes.new('GeometryNodeDistributePointsOnFaces')
    node_distribute.inputs['Density'].default_value = sugar_density

    node_instance = nodes.new('GeometryNodeInstanceOnPoints')

    node_obj_info = nodes.new('GeometryNodeObjectInfo')
    node_obj_info.inputs['Object'].default_value = crystal_obj

    # Random Rotation Vector (0 to Tau/360 degrees)
    node_rand_rot = nodes.new('GeometryNodeRandomValue')
    node_rand_rot.data_type = 'FLOAT_VECTOR'
    # Use index-based assignment to ensure cross-version stability (Min = 0, Max = 1 for Vector)
    node_rand_rot.inputs[0].default_value = (0.0, 0.0, 0.0) 
    node_rand_rot.inputs[1].default_value = (math.tau, math.tau, math.tau)

    # Random Scale Float (0.4 to 1.2 relative size variance)
    node_rand_scale = nodes.new('GeometryNodeRandomValue')
    node_rand_scale.data_type = 'FLOAT'
    # Float index inputs: Min = 2, Max = 3
    node_rand_scale.inputs[2].default_value = 0.4
    node_rand_scale.inputs[3].default_value = 1.2

    node_join = nodes.new('GeometryNodeJoinGeometry')

    # Link the Node Tree
    links = gn_tree.links
    in_geom = node_input.outputs[0]
    out_geom = node_output.inputs[0]

    # Distribute and Instance
    links.new(in_geom, node_distribute.inputs['Mesh'])
    links.new(node_distribute.outputs['Points'], node_instance.inputs['Points'])
    links.new(node_obj_info.outputs['Geometry'], node_instance.inputs['Instance'])

    # Randomization links
    links.new(node_rand_rot.outputs[0], node_instance.inputs['Rotation'])
    links.new(node_rand_scale.outputs[0], node_instance.inputs['Scale'])

    # Join the instances onto the original underlying mesh
    links.new(in_geom, node_join.inputs['Geometry'])
    links.new(node_instance.outputs['Instances'], node_join.inputs['Geometry'])
    
    # Output to the modifier
    links.new(node_join.outputs['Geometry'], out_geom)

    return f"Created '{object_name}' (sugar-coated candy) at {location} with procedural scattering."
