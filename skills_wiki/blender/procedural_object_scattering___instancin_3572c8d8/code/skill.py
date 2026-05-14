def create_object(
    scene_name: str = "Scene",
    object_name: str = "SugarCandy",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.02, 0.05),
    crystal_density: float = 2500.0,
    **kwargs,
) -> str:
    """
    Create a procedural scattered object (Sugar Coated Candy) using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created candy object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the candy base.
        material_color: (R, G, B) base color for the candy.
        crystal_density: Number of points to scatter (higher = more sugar).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    # Safely get scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Helper function to reliably fetch sockets by name across Blender versions
    def get_socket(node, name, is_output=False):
        sockets = node.outputs if is_output else node.inputs
        for s in sockets:
            if s.name == name:
                return s
        return sockets[0]  # Safe fallback

    # ==========================================
    # 1. CREATE INSTANCE OBJECT (SUGAR CRYSTAL)
    # ==========================================
    # Placed slightly below the scene, hidden from render/viewport
    bpy.ops.mesh.primitive_cube_add(size=0.03, location=(location[0], location[1], location[2] - 5.0))
    crystal_obj = bpy.context.active_object
    crystal_obj.name = f"{object_name}_Crystal"
    
    # Crystal Material (Transmissive Glass)
    mat_cryst = bpy.data.materials.new(name=f"{object_name}_CrystalMat")
    mat_cryst.use_nodes = True
    bsdf_c = mat_cryst.node_tree.nodes.get("Principled BSDF")
    if bsdf_c:
        bsdf_c.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0)
        bsdf_c.inputs["Roughness"].default_value = 0.05
        bsdf_c.inputs["IOR"].default_value = 1.53  # IOR of sugar/glass
        
        if "Transmission Weight" in bsdf_c.inputs:  # Blender 4.0+
            bsdf_c.inputs["Transmission Weight"].default_value = 1.0
        elif "Transmission" in bsdf_c.inputs:       # Blender 3.x
            bsdf_c.inputs["Transmission"].default_value = 1.0

    crystal_obj.data.materials.append(mat_cryst)
    
    # Hide the source crystal
    crystal_obj.hide_viewport = True
    crystal_obj.hide_render = True

    # ==========================================
    # 2. CREATE BASE MESH (GUMMY CANDY)
    # ==========================================
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.0 * scale, 
        minor_radius=0.4 * scale, 
        location=location
    )
    candy_obj = bpy.context.active_object
    candy_obj.name = object_name
    bpy.ops.object.shade_smooth()

    # Candy Material (Subsurface Scattering)
    mat_candy = bpy.data.materials.new(name=f"{object_name}_CandyMat")
    mat_candy.use_nodes = True
    bsdf_candy = mat_candy.node_tree.nodes.get("Principled BSDF")
    if bsdf_candy:
        bsdf_candy.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf_candy.inputs["Roughness"].default_value = 0.3
        
        if "Subsurface Weight" in bsdf_candy.inputs:  # Blender 4.0+
            bsdf_candy.inputs["Subsurface Weight"].default_value = 1.0
            bsdf_candy.inputs["Subsurface Radius"].default_value = (0.2, 0.2, 0.2)
            if "Subsurface Color" in bsdf_candy.inputs:
                bsdf_candy.inputs["Subsurface Color"].default_value = (*material_color, 1.0)
        elif "Subsurface" in bsdf_candy.inputs:       # Blender 3.x
            bsdf_candy.inputs["Subsurface"].default_value = 1.0
            if "Subsurface Radius" in bsdf_candy.inputs:
                bsdf_candy.inputs["Subsurface Radius"].default_value = (0.2, 0.2, 0.2)
            if "Subsurface Color" in bsdf_candy.inputs:
                bsdf_candy.inputs["Subsurface Color"].default_value = (*material_color, 1.0)
                
    candy_obj.data.materials.append(mat_candy)

    # Subsurf Modifier for smooth base
    subsurf = candy_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # ==========================================
    # 3. BUILD GEOMETRY NODES TREE
    # ==========================================
    tree = bpy.data.node_groups.new(name=f"{object_name}_Scattering", type='GeometryNodeTree')
    
    # Init tree interface sockets safely (compatible with 3.x and 4.0+)
    if hasattr(tree, "interface"):
        tree.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        tree.inputs.new('NodeSocketGeometry', "Geometry")
        tree.outputs.new('NodeSocketGeometry', "Geometry")

    # Add Nodes
    nodes = tree.nodes
    in_node = nodes.new('NodeGroupInput')
    out_node = nodes.new('NodeGroupOutput')
    
    distribute = nodes.new('GeometryNodeDistributePointsOnFaces')
    get_socket(distribute, 'Density').default_value = crystal_density
    
    instance = nodes.new('GeometryNodeInstanceOnPoints')
    join = nodes.new('GeometryNodeJoinGeometry')
    
    obj_info = nodes.new('GeometryNodeObjectInfo')
    get_socket(obj_info, 'Object').default_value = crystal_obj
    obj_info.transform_space = 'RELATIVE'
    
    rand_rot = nodes.new('FunctionNodeRandomValue')
    rand_rot.data_type = 'FLOAT_VECTOR'
    get_socket(rand_rot, 'Min').default_value = (0.0, 0.0, 0.0)
    # Use math.tau for full 360 degree (2 pi radians) rotation on all axes
    get_socket(rand_rot, 'Max').default_value = (math.tau, math.tau, math.tau)
    
    rand_scale = nodes.new('FunctionNodeRandomValue')
    rand_scale.data_type = 'FLOAT'
    get_socket(rand_scale, 'Min').default_value = 0.4
    get_socket(rand_scale, 'Max').default_value = 1.2

    # Link Nodes
    links = tree.links
    
    # Route input mesh to point distributor
    links.new(get_socket(in_node, 'Geometry', True), get_socket(distribute, 'Mesh'))
    
    # Route points to instancer
    links.new(get_socket(distribute, 'Points', True), get_socket(instance, 'Points'))
    
    # Route crystal object data into instancer
    links.new(get_socket(obj_info, 'Geometry', True), get_socket(instance, 'Instance'))
    
    # Route random math into instancer attributes
    links.new(get_socket(rand_rot, 'Value', True), get_socket(instance, 'Rotation'))
    links.new(get_socket(rand_scale, 'Value', True), get_socket(instance, 'Scale'))
    
    # Join original smooth base mesh + generated crystal instances
    links.new(get_socket(in_node, 'Geometry', True), get_socket(join, 'Geometry'))
    links.new(get_socket(instance, 'Instances', True), get_socket(join, 'Geometry'))
    
    # Route to output
    links.new(get_socket(join, 'Geometry', True), get_socket(out_node, 'Geometry'))

    # ==========================================
    # 4. APPLY MODIFIER AND FINALIZE
    # ==========================================
    gn_mod = candy_obj.modifiers.new(name="SugarCoating", type='NODES')
    gn_mod.node_group = tree

    # Clean up selection state
    bpy.ops.object.select_all(action='DESELECT')
    candy_obj.select_set(True)
    bpy.context.view_layer.objects.active = candy_obj

    return f"Created '{object_name}' with procedural sugar scattering at {location}."
