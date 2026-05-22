def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    trunk_color: tuple = (0.3, 0.15, 0.05, 1.0), # RGBA
    leaf_color: tuple = (0.1, 0.4, 0.1, 1.0), # RGBA
    num_layers: int = 4,
    layer_spacing: float = 0.5,
    trunk_height: float = 0.8,
    trunk_radius: float = 0.1,
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Christmas Tree in the active Blender scene.
    Reproduces the basic modeling techniques (extrude, scale, rotate, duplicate, loop cut)
    demonstrated in the tutorial using bpy.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created main tree object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the entire tree.
        trunk_color: (R, G, B, A) base color for the trunk.
        leaf_color: (R, G, B, A) base color for the leaf layers.
        num_layers: Number of stacked leaf layers.
        layer_spacing: Vertical distance between leaf layers.
        trunk_height: Height of the tree trunk.
        trunk_radius: Radius of the tree trunk.
        **kwargs: Additional overrides (e.g., top_cone_scale, base_cone_radius_factor).

    Returns:
        Status string, e.g., "Created 'StylizedTree' at (0, 0, 0) with 5 objects"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Materials ---
    trunk_mat = bpy.data.materials.new(name=f"{object_name}_TrunkMat")
    trunk_mat.use_nodes = True
    bsdf = trunk_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = trunk_color
    trunk_mat.diffuse_color = trunk_color # For viewport display

    leaf_mat = bpy.data.materials.new(name=f"{object_name}_LeafMat")
    leaf_mat.use_nodes = True
    bsdf = leaf_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = leaf_color
    leaf_mat.diffuse_color = leaf_color # For viewport display

    # --- Create Trunk ---
    bpy.ops.mesh.primitive_cylinder_add(
        radius=trunk_radius,
        depth=trunk_height,
        enter_editmode=False,
        align='WORLD',
        location=location,
        scale=(1, 1, 1) # Scale will be applied later
    )
    trunk_obj = bpy.context.active_object
    trunk_obj.name = f"{object_name}_Trunk"
    trunk_obj.data.materials.append(trunk_mat)

    # Apply initial transformations for trunk base shape
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(trunk_obj.data)
    
    # Scale top face of trunk
    bm.faces.ensure_lookup_table()
    top_face = None
    for face in bm.faces:
        if any(v.co.z > trunk_obj.location.z + trunk_height/2 - 0.01 for v in face.verts):
            top_face = face
            break
    if top_face:
        # Select top face
        top_face.select = True
        bpy.ops.mesh.select_mode(type='FACE') # Ensure face select mode
        bpy.ops.transform.resize(value=(0.7, 0.7, 1.0), orient_type='LOCAL_NORMAL')
        top_face.select = False # Deselect
    
    # Scale bottom face of trunk
    bottom_face = None
    for face in bm.faces:
        if any(v.co.z < trunk_obj.location.z - trunk_height/2 + 0.01 for v in face.verts):
            bottom_face = face
            break
    if bottom_face:
        bottom_face.select = True
        bpy.ops.transform.resize(value=(1.2, 1.2, 1.0), orient_type='LOCAL_NORMAL')
        bottom_face.select = False # Deselect
        
    bmesh.update_edit_mesh(trunk_obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    # --- Create Leaf Layers ---
    leaf_objects = []
    
    # Calculate starting Z for leaves (above trunk)
    current_z = location[2] + trunk_height/2 + layer_spacing / 2
    
    base_radius = kwargs.get('base_cone_radius_factor', 0.8) * scale
    top_radius = kwargs.get('top_cone_radius_factor', 0.2) * scale
    cone_height = layer_spacing * 1.5 # Overlap slightly
    
    for i in range(num_layers):
        # Scale decreases for higher layers
        layer_scale_factor = 1 - (i / num_layers) * 0.7
        current_radius = base_radius * layer_scale_factor
        
        # Add cone for current layer
        bpy.ops.mesh.primitive_cone_add(
            radius1=current_radius,
            depth=cone_height,
            vertices=16, # Lower poly count for stylized look
            enter_editmode=False,
            align='WORLD',
            location=(location[0], location[1], current_z),
            rotation=(0, 0, math.radians(i * (360 / num_layers / 2))), # Rotate each layer slightly
            scale=(1, 1, 1)
        )
        leaf_obj = bpy.context.active_object
        leaf_obj.name = f"{object_name}_LeafLayer_{i+1}"
        leaf_obj.data.materials.append(leaf_mat)
        
        # --- Add detail to the bottom of the cone (mimic E+S, Alt+E, S) ---
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(leaf_obj.data)
        
        # Select the outer edge loop of the bottom face
        bm.edges.ensure_lookup_table()
        bottom_edge_loop = [edge for edge in bm.edges if edge.verts[0].co.z < current_z - cone_height/2 + 0.01 and edge.verts[1].co.z < current_z - cone_height/2 + 0.01 and edge.is_boundary]
        
        if bottom_edge_loop:
            for edge in bottom_edge_loop:
                edge.select = True
            
            bpy.ops.mesh.select_mode(type='EDGE')
            # E (extrude) then S (scale) inwards
            bpy.ops.mesh.extrude_edges_move(
                MESH_OT_extrude_individual={"dissolve_and_vert_create": False}, 
                TRANSFORM_OT_resize={"value":(0.85, 0.85, 1.0), "orient_type":'LOCAL_NORMAL'}
            )
            
            # Alt+E -> Extrude Faces Along Normals (outwards)
            bpy.ops.mesh.extrude_faces_along_normals(
                TRANSFORM_OT_shrink_fatten={"value":0.05} # Positive value for outwards
            )

            # S (scale) inwards again
            bpy.ops.transform.resize(value=(0.9, 0.9, 1.0), orient_type='LOCAL_NORMAL')
            
            # Deselect all
            bpy.ops.mesh.select_all(action='DESELECT')

        bmesh.update_edit_mesh(leaf_obj.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        leaf_objects.append(leaf_obj)
        current_z += layer_spacing
        
    # --- Parent objects to a main empty for easy manipulation ---
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=location, scale=(1, 1, 1))
    main_empty = bpy.context.active_object
    main_empty.name = object_name
    main_empty.scale = (scale, scale, scale) # Apply overall scale

    # Parent trunk to empty
    trunk_obj.parent = main_empty

    # Parent leaf layers to empty
    for leaf_obj in leaf_objects:
        leaf_obj.parent = main_empty

    # Select the main empty
    bpy.context.view_layer.objects.active = main_empty
    main_empty.select_set(True)

    return f"Created '{object_name}' at {location} with {1 + num_layers} objects"

