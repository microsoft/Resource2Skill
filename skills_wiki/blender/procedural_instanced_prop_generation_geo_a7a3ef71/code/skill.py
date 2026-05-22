def create_object(
    scene_name: str = "Scene",
    object_name: str = "Procedural_Lego_Brick",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.05, 0.05),
    **kwargs,
) -> str:
    """
    Create a procedural, parametric Lego brick using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) color for the plastic material.
        **kwargs: 
            studs_x (int): Number of studs along the X axis (default: 2).
            studs_y (int): Number of studs along the Y axis (default: 4).

    Returns:
        Status string confirming creation.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    studs_x = kwargs.get('studs_x', 2)
    studs_y = kwargs.get('studs_y', 4)

    # Standard Lego proportions in meters
    PITCH = 0.008       # 8mm between studs
    HEIGHT = 0.0096     # 9.6mm standard brick height
    STUD_R = 0.0024     # 2.4mm stud radius
    STUD_H = 0.0017     # 1.7mm stud height

    # === Step 1: Create Plastic Material ===
    mat_name = f"{object_name}_Plastic"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Set base color and shiny plastic properties
            bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.15
            
            # Subsurface is great for plastic, handle gracefully across Blender versions
            if 'Subsurface Weight' in bsdf.inputs: # Blender 4.0+
                bsdf.inputs['Subsurface Weight'].default_value = 0.1
            elif 'Subsurface' in bsdf.inputs: # Blender 3.x
                bsdf.inputs['Subsurface'].default_value = 0.1

    # === Step 2: Build Geometry Node Group ===
    group_name = "GN_LegoBrick"
    group = bpy.data.node_groups.get(group_name)
    if not group:
        group = bpy.data.node_groups.new(name=group_name, type='GeometryNodeTree')
        
        # Setup Inputs/Outputs based on Blender version
        if hasattr(group, "interface"): # 4.0+
            in_x = group.interface.new_socket(name="Studs X", in_out='INPUT', socket_type='NodeSocketInt')
            in_y = group.interface.new_socket(name="Studs Y", in_out='INPUT', socket_type='NodeSocketInt')
            group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
            in_x.default_value = studs_x
            in_y.default_value = studs_y
        else: # 3.x
            in_x = group.inputs.new('NodeSocketInt', "Studs X")
            in_y = group.inputs.new('NodeSocketInt', "Studs Y")
            group.outputs.new('NodeSocketGeometry', "Geometry")
            in_x.default_value = studs_x
            in_y.default_value = studs_y

        nodes = group.nodes
        links = group.links
        
        node_in = nodes.new('NodeGroupInput')
        node_out = nodes.new('NodeGroupOutput')

        # Calculate Base Width/Length (Count * Pitch)
        math_x_pitch = nodes.new('ShaderNodeMath')
        math_x_pitch.operation = 'MULTIPLY'
        math_x_pitch.inputs[1].default_value = PITCH
        links.new(node_in.outputs['Studs X'], math_x_pitch.inputs[0])

        math_y_pitch = nodes.new('ShaderNodeMath')
        math_y_pitch.operation = 'MULTIPLY'
        math_y_pitch.inputs[1].default_value = PITCH
        links.new(node_in.outputs['Studs Y'], math_y_pitch.inputs[0])

        comb_size = nodes.new('ShaderNodeCombineXYZ')
        links.new(math_x_pitch.outputs[0], comb_size.inputs[0])
        links.new(math_y_pitch.outputs[0], comb_size.inputs[1])
        comb_size.inputs[2].default_value = HEIGHT

        # Base Cube
        cube = nodes.new('GeometryNodeMeshCube')
        links.new(comb_size.outputs[0], cube.inputs['Size'])

        # Translate Cube so bottom rests at Z=0
        trans_cube = nodes.new('GeometryNodeTransform')
        trans_cube.inputs['Translation'].default_value = (0, 0, HEIGHT / 2)
        links.new(cube.outputs['Mesh'], trans_cube.inputs['Geometry'])

        # Calculate Grid Size ((Count - 1) * Pitch)
        sub_x = nodes.new('ShaderNodeMath')
        sub_x.operation = 'SUBTRACT'
        sub_x.inputs[1].default_value = 1.0
        links.new(node_in.outputs['Studs X'], sub_x.inputs[0])

        grid_sz_x = nodes.new('ShaderNodeMath')
        grid_sz_x.operation = 'MULTIPLY'
        grid_sz_x.inputs[1].default_value = PITCH
        links.new(sub_x.outputs[0], grid_sz_x.inputs[0])

        sub_y = nodes.new('ShaderNodeMath')
        sub_y.operation = 'SUBTRACT'
        sub_y.inputs[1].default_value = 1.0
        links.new(node_in.outputs['Studs Y'], sub_y.inputs[0])

        grid_sz_y = nodes.new('ShaderNodeMath')
        grid_sz_y.operation = 'MULTIPLY'
        grid_sz_y.inputs[1].default_value = PITCH
        links.new(sub_y.outputs[0], grid_sz_y.inputs[0])

        # Grid for Stud Placement
        grid = nodes.new('GeometryNodeMeshGrid')
        links.new(grid_sz_x.outputs[0], grid.inputs['Size X'])
        links.new(grid_sz_y.outputs[0], grid.inputs['Size Y'])
        links.new(node_in.outputs['Studs X'], grid.inputs['Vertices X'])
        links.new(node_in.outputs['Studs Y'], grid.inputs['Vertices Y'])

        # Stud Cylinder Primitive
        cyl = nodes.new('GeometryNodeMeshCylinder')
        cyl.inputs['Radius'].default_value = STUD_R
        cyl.inputs['Depth'].default_value = STUD_H
        cyl.inputs['Vertices'].default_value = 32

        # Smooth Cylinder Sides
        smooth = nodes.new('GeometryNodeSetShadeSmooth')
        links.new(cyl.outputs['Mesh'], smooth.inputs['Geometry'])
        # Link cylinder 'Side' selection to smoothing
        if 'Side' in cyl.outputs:
            links.new(cyl.outputs['Side'], smooth.inputs['Selection'])

        # Instance Studs on Grid
        inst = nodes.new('GeometryNodeInstanceOnPoints')
        links.new(grid.outputs['Mesh'], inst.inputs['Points'])
        links.new(smooth.outputs['Geometry'], inst.inputs['Instance'])

        # Translate Studs to sit exactly on top of the base cube
        trans_inst = nodes.new('GeometryNodeTransform')
        trans_inst.inputs['Translation'].default_value = (0, 0, HEIGHT + (STUD_H / 2))
        links.new(inst.outputs['Instances'], trans_inst.inputs['Geometry'])

        # Realize Instances (CRITICAL for Bevel modifier to work later)
        realize = nodes.new('GeometryNodeRealizeInstances')
        links.new(trans_inst.outputs['Geometry'], realize.inputs['Geometry'])

        # Join Base and Studs
        join = nodes.new('GeometryNodeJoinGeometry')
        links.new(trans_cube.outputs['Geometry'], join.inputs['Geometry'])
        links.new(realize.outputs['Geometry'], join.inputs['Geometry'])

        # Assign Material
        set_mat = nodes.new('GeometryNodeSetMaterial')
        set_mat.inputs['Material'].default_value = mat
        links.new(join.outputs['Geometry'], set_mat.inputs['Geometry'])

        # Final Output
        links.new(set_mat.outputs['Geometry'], node_out.inputs[0])

    # === Step 3: Create Host Object ===
    # Start with an empty mesh; GN will overwrite it entirely
    mesh = bpy.data.meshes.new(object_name)
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # Attach the Procedural Logic
    mod_gn = obj.modifiers.new(name="Lego_Gen", type='NODES')
    mod_gn.node_group = group

    # === Step 4: Apply Edge Polishing ===
    # The Bevel modifier runs AFTER Geometry Nodes to round all generated edges
    mod_bevel = obj.modifiers.new(name="Plastic_Edge_Bevel", type='BEVEL')
    mod_bevel.segments = 3
    mod_bevel.width = 0.0003  # 0.3mm chamfer
    mod_bevel.limit_method = 'ANGLE'
    mod_bevel.angle_limit = math.radians(35)

    # Set external positioning
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created procedural {studs_x}x{studs_y} '{object_name}' at {location}."
