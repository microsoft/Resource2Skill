def create_object(
    scene_name: str = "Scene",
    object_name: str = "SugarCandy",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.05, 0.1),
    **kwargs,
) -> str:
    """
    Create a procedural sugar-coated gummy candy using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the main candy object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the gummy candy.
        **kwargs: Additional parameters (e.g., scatter_density).

    Returns:
        Status string describing the created objects.
    """
    import bpy
    import math
    from mathutils import Vector

    scatter_density = kwargs.get("scatter_density", 2000.0)

    # === Step 1: Create Instance Object (Sugar Crystal) ===
    # We create it slightly below the origin and hide it, as it only serves as a reference
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=(location[0], location[1], location[2] - 5.0))
    sugar_crystal = bpy.context.active_object
    sugar_crystal.name = f"{object_name}_Crystal"
    
    # Material for sugar (Refractive, highly transmissive)
    sugar_mat = bpy.data.materials.new(name=f"{object_name}_SugarMat")
    sugar_mat.use_nodes = True
    sugar_bsdf = sugar_mat.node_tree.nodes.get("Principled BSDF")
    if sugar_bsdf:
        sugar_bsdf.inputs["Base Color"].default_value = (0.9, 0.9, 0.9, 1.0)
        sugar_bsdf.inputs["Roughness"].default_value = 0.2
        sugar_bsdf.inputs["IOR"].default_value = 1.5
        # Handle API differences for transmission
        if "Transmission Weight" in sugar_bsdf.inputs:  # Blender 4.0+
            sugar_bsdf.inputs["Transmission Weight"].default_value = 0.9
        elif "Transmission" in sugar_bsdf.inputs:       # Blender 3.x
            sugar_bsdf.inputs["Transmission"].default_value = 0.9
            
    sugar_crystal.data.materials.append(sugar_mat)
    # Hide the source instance from the viewport and render
    sugar_crystal.hide_set(True)
    sugar_crystal.hide_render = True

    # === Step 2: Create Base Mesh (Gummy Candy) ===
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.45, location=location)
    candy_obj = bpy.context.active_object
    candy_obj.name = object_name
    bpy.ops.object.shade_smooth()
    
    # Subdivide for smoother surface
    subsurf = candy_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # Material for gummy candy (Translucent, colored SSS)
    candy_mat = bpy.data.materials.new(name=f"{object_name}_CandyMat")
    candy_mat.use_nodes = True
    candy_bsdf = candy_mat.node_tree.nodes.get("Principled BSDF")
    if candy_bsdf:
        candy_bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        candy_bsdf.inputs["Roughness"].default_value = 0.25
        
        # Handle API differences for Subsurface and Transmission
        if "Transmission Weight" in candy_bsdf.inputs:  # Blender 4.0+
            candy_bsdf.inputs["Transmission Weight"].default_value = 0.8
            candy_bsdf.inputs["Subsurface Weight"].default_value = 1.0
            candy_bsdf.inputs["Subsurface Scale"].default_value = 0.1
            candy_bsdf.inputs["Subsurface Radius"].default_value = (1.0, 0.2, 0.1)
        elif "Transmission" in candy_bsdf.inputs:       # Blender 3.x
            candy_bsdf.inputs["Transmission"].default_value = 0.8
            candy_bsdf.inputs["Subsurface"].default_value = 1.0
            candy_bsdf.inputs["Subsurface Color"].default_value = (*material_color, 1.0)
            candy_bsdf.inputs["Subsurface Radius"].default_value = (1.0, 0.2, 0.1)
            
    candy_obj.data.materials.append(candy_mat)

    # === Step 3: Procedural Geometry Nodes (Sugar Coating) ===
    gn_mod = candy_obj.modifiers.new(name="SugarCoating", type='NODES')
    
    # Create the Geometry Node Tree
    tree_name = f"{object_name}_GeoTree"
    if tree_name in bpy.data.node_groups:
        geo_tree = bpy.data.node_groups[tree_name]
    else:
        geo_tree = bpy.data.node_groups.new(name=tree_name, type="GeometryNodeTree")
        
        # Setup Group Input/Output interfaces gracefully across Blender versions
        if hasattr(geo_tree, "interface"): # Blender 4.0+
            geo_tree.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
            geo_tree.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
        else: # Blender 3.x
            geo_tree.inputs.new("NodeSocketGeometry", "Geometry")
            geo_tree.outputs.new("NodeSocketGeometry", "Geometry")
            
        # Add Nodes
        in_node = geo_tree.nodes.new('NodeGroupInput')
        in_node.location = (-400, 0)
        
        distribute_node = geo_tree.nodes.new('GeometryNodeDistributePointsOnFaces')
        distribute_node.inputs['Density'].default_value = scatter_density
        distribute_node.location = (-200, 100)
        
        obj_info_node = geo_tree.nodes.new('GeometryNodeObjectInfo')
        obj_info_node.inputs['Object'].default_value = sugar_crystal
        obj_info_node.transform_space = 'RELATIVE'
        obj_info_node.location = (-200, -200)
        
        rand_rot_node = geo_tree.nodes.new('FunctionNodeRandomValue')
        rand_rot_node.data_type = 'FLOAT_VECTOR'
        rand_rot_node.inputs['Max'].default_value = (math.tau, math.tau, math.tau) # 360 deg in radians
        rand_rot_node.location = (-200, -400)
        
        rand_scale_node = geo_tree.nodes.new('FunctionNodeRandomValue')
        rand_scale_node.data_type = 'FLOAT'
        rand_scale_node.inputs['Min'].default_value = 0.05
        rand_scale_node.inputs['Max'].default_value = 0.18
        rand_scale_node.location = (-200, -600)
        
        instance_node = geo_tree.nodes.new('GeometryNodeInstanceOnPoints')
        instance_node.location = (100, 100)
        
        join_node = geo_tree.nodes.new('GeometryNodeJoinGeometry')
        join_node.location = (300, 0)
        
        out_node = geo_tree.nodes.new('NodeGroupOutput')
        out_node.location = (500, 0)
        
        # Connect Nodes
        links = geo_tree.links
        links.new(in_node.outputs['Geometry'], distribute_node.inputs['Mesh'])
        links.new(in_node.outputs['Geometry'], join_node.inputs['Geometry']) # Preserve base mesh
        
        links.new(distribute_node.outputs['Points'], instance_node.inputs['Points'])
        
        # Link Instance object
        if 'Geometry' in obj_info_node.outputs:
            links.new(obj_info_node.outputs['Geometry'], instance_node.inputs['Instance'])
            
        # Link Randomizers
        links.new(rand_rot_node.outputs['Value'], instance_node.inputs['Rotation'])
        links.new(rand_scale_node.outputs['Value'], instance_node.inputs['Scale'])
        
        # Merge and Output
        links.new(instance_node.outputs['Instances'], join_node.inputs['Geometry'])
        links.new(join_node.outputs['Geometry'], out_node.inputs['Geometry'])

    # Assign tree to modifier
    gn_mod.node_group = geo_tree

    # === Step 4: Finalize Position & Scale ===
    candy_obj.location = Vector(location)
    candy_obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' (procedurally scattered sugar candy) at {location}"
