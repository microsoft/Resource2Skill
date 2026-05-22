def create_object(
    scene_name: str = "Scene",
    object_name: str = "SugarCoatedGummy",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.02, 0.05), # Cherry Red by default
    **kwargs,
) -> str:
    """
    Create a procedural Sugar-Coated Candy object using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created gummy object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the gummy candy.
        **kwargs: Additional options (e.g., 'density' for sugar crystals).

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector
    
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    crystal_density = kwargs.get("density", 2000.0)

    # === Step 1: Create the Gummy Base (Torus) ===
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.0, 
        minor_radius=0.4, 
        major_segments=48, 
        minor_segments=24,
        location=location
    )
    base_obj = bpy.context.active_object
    base_obj.name = object_name
    base_obj.scale = (scale, scale, scale)
    
    # Smooth the base geometry
    bpy.ops.object.shade_smooth()
    subsurf = base_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2

    # === Step 2: Create the Sugar Crystal Instance ===
    bpy.ops.mesh.primitive_cube_add(size=0.05, location=(0, 0, -100))
    crystal_obj = bpy.context.active_object
    crystal_obj.name = f"{object_name}_SugarCrystal"
    
    # Add a slight bevel to the crystal for better specular highlights
    bevel = crystal_obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.01
    bevel.segments = 2
    bpy.ops.object.shade_smooth()
    
    # Hide crystal from direct rendering/viewport (it will only be instanced)
    crystal_obj.hide_viewport = True
    crystal_obj.hide_render = True

    # === Step 3: Geometry Nodes Scattering System ===
    gn_mod = base_obj.modifiers.new(name="Sugar_Coating", type='NODES')
    tree = bpy.data.node_groups.new(name="GN_SugarScatter", type='GeometryNodeTree')
    gn_mod.node_group = tree

    # Setup GN Interface (Compatible with Blender 3.x and 4.x)
    if hasattr(tree, "interface"):
        tree.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        tree.inputs.new('NodeSocketGeometry', "Geometry")
        tree.outputs.new('NodeSocketGeometry', "Geometry")

    nodes = tree.nodes
    links = tree.links

    # Create Nodes
    node_in = nodes.new('NodeGroupInput')
    node_in.location = (-600, 0)
    
    node_out = nodes.new('NodeGroupOutput')
    node_out.location = (600, 0)

    distribute = nodes.new('GeometryNodeDistributePointsOnFaces')
    distribute.location = (-400, 100)
    distribute.inputs['Density'].default_value = crystal_density

    instance = nodes.new('GeometryNodeInstanceOnPoints')
    instance.location = (200, 100)

    obj_info = nodes.new('GeometryNodeObjectInfo')
    obj_info.location = (-100, -100)
    obj_info.inputs['Object'].default_value = crystal_obj
    obj_info.transform_space = 'RELATIVE' # Ensures scaling applies correctly

    join = nodes.new('GeometryNodeJoinGeometry')
    join.location = (400, 0)

    # Random Rotation (Vector, 0 to Tau)
    rand_rot = nodes.new('FunctionNodeRandomValue')
    rand_rot.location = (-100, -300)
    rand_rot.data_type = 'FLOAT_VECTOR'
    rand_rot.inputs['Max'].default_value = (math.tau, math.tau, math.tau)

    # Random Scale (Float, 0.5 to 1.5)
    rand_scale = nodes.new('FunctionNodeRandomValue')
    rand_scale.location = (-100, -500)
    rand_scale.data_type = 'FLOAT'
    rand_scale.inputs['Min'].default_value = 0.5
    rand_scale.inputs['Max'].default_value = 1.5

    # Link Nodes (Using output/input index arrays to ensure cross-version compatibility)
    links.new(node_in.outputs[0], distribute.inputs[0]) # Geometry -> Mesh
    links.new(distribute.outputs[0], instance.inputs[0]) # Points -> Points
    links.new(obj_info.outputs[0], instance.inputs[2]) # Geometry -> Instance
    
    # Instance transforms
    links.new(rand_rot.outputs[0], instance.inputs[5]) # Vector -> Rotation
    links.new(rand_scale.outputs[0], instance.inputs[6]) # Value -> Scale
    
    # Combine original mesh and instances
    links.new(node_in.outputs[0], join.inputs[0]) # Original Geometry
    links.new(instance.outputs[0], join.inputs[0]) # Instances
    
    # Output
    links.new(join.outputs[0], node_out.inputs[0])

    # === Step 4: Materials ===
    
    # 4a. Gummy Base Material
    gummy_mat = bpy.data.materials.new(name=f"{object_name}_GummyMat")
    gummy_mat.use_nodes = True
    gummy_bsdf = gummy_mat.node_tree.nodes.get("Principled BSDF")
    if gummy_bsdf:
        gummy_bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        gummy_bsdf.inputs["Roughness"].default_value = 0.15
        
        # Subsurface scattering for gummy translucency
        if "Subsurface Weight" in gummy_bsdf.inputs: # Blender 4.x
            gummy_bsdf.inputs["Subsurface Weight"].default_value = 1.0
            gummy_bsdf.inputs["Subsurface Radius"].default_value = (0.2, 0.2, 0.2)
        elif "Subsurface" in gummy_bsdf.inputs: # Blender 3.x
            gummy_bsdf.inputs["Subsurface"].default_value = 1.0
            gummy_bsdf.inputs["Subsurface Color"].default_value = (*material_color, 1.0)

    base_obj.data.materials.append(gummy_mat)

    # 4b. Sugar Crystal Material
    sugar_mat = bpy.data.materials.new(name=f"{object_name}_SugarMat")
    sugar_mat.use_nodes = True
    sugar_bsdf = sugar_mat.node_tree.nodes.get("Principled BSDF")
    if sugar_bsdf:
        sugar_bsdf.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0)
        sugar_bsdf.inputs["Roughness"].default_value = 0.1
        sugar_bsdf.inputs["IOR"].default_value = 1.5
        
        if "Transmission Weight" in sugar_bsdf.inputs: # Blender 4.x
            sugar_bsdf.inputs["Transmission Weight"].default_value = 0.9
        elif "Transmission" in sugar_bsdf.inputs: # Blender 3.x
            sugar_bsdf.inputs["Transmission"].default_value = 0.9

    crystal_obj.data.materials.append(sugar_mat)

    return f"Created '{object_name}' (Gummy Base) at {location} with procedural Sugar Coating Geometry Nodes modifier."
