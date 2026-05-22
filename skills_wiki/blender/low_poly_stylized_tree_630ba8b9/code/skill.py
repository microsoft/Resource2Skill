def create_low_poly_stylized_tree(
    scene_name: str = "Scene",
    object_name: str = "LowPolyTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    trunk_color: tuple = (0.3, 0.15, 0.05),  # Dark brown
    leaf_color: tuple = (0.1, 0.4, 0.1),  # Dark green
    trunk_height: float = 2.0,
    trunk_radius: float = 0.2,
    trunk_vertices: int = 8,
    leaf_layers: int = 5,
    leaf_height_multiplier: float = 0.8,
    leaf_base_radius_multiplier: float = 0.8,
    leaf_top_radius_multiplier: float = 0.2,
    leaf_rotation_step: float = 20.0, # Degrees
    smooth_angle_deg: float = 30.0, # Degrees for auto smooth
    **kwargs,
) -> str:
    """
    Create a low-poly stylized tree in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created tree components.
        location: (x, y, z) world-space position for the tree's base.
        scale: Uniform scale factor for the entire tree.
        trunk_color: (R, G, B) base color for the trunk in 0-1 range.
        leaf_color: (R, G, B) base color for the leaves in 0-1 range.
        trunk_height: Height of the tree trunk.
        trunk_radius: Radius of the tree trunk.
        trunk_vertices: Number of vertices for the trunk cylinder.
        leaf_layers: Number of distinct leaf layers.
        leaf_height_multiplier: Scales the height of each leaf layer relative to trunk_height.
        leaf_base_radius_multiplier: Scales the base radius of each leaf layer relative to trunk_radius.
        leaf_top_radius_multiplier: Scales the top radius of each leaf layer relative to leaf_base_radius.
        leaf_rotation_step: Z-axis rotation difference between successive leaf layers (in degrees).
        smooth_angle_deg: Angle threshold for auto smooth on generated meshes.
        **kwargs: Additional overrides (not used in this skill but for future expansion).

    Returns:
        Status string, e.g., "Created 'LowPolyTree' at (0, 0, 0) with 6 objects"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    # Get the scene, or use the first available
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Convert smooth angle to radians
    smooth_angle_rad = math.radians(smooth_angle_deg)

    # --- Materials ---
    trunk_mat_name = f"{object_name}_TrunkMat"
    leaf_mat_name = f"{object_name}_LeafMat"

    trunk_mat = bpy.data.materials.get(trunk_mat_name)
    if not trunk_mat:
        trunk_mat = bpy.data.materials.new(name=trunk_mat_name)
        trunk_mat.use_nodes = True
        principled_bsdf = trunk_mat.node_tree.nodes.get('Principled BSDF')
        if principled_bsdf:
            principled_bsdf.inputs['Base Color'].default_value = (*trunk_color, 1.0)
            principled_bsdf.inputs['Roughness'].default_value = 0.7

    leaf_mat = bpy.data.materials.get(leaf_mat_name)
    if not leaf_mat:
        leaf_mat = bpy.data.materials.new(name=leaf_mat_name)
        leaf_mat.use_nodes = True
        principled_bsdf = leaf_mat.node_tree.nodes.get('Principled BSDF')
        if principled_bsdf:
            principled_bsdf.inputs['Base Color'].default_value = (*leaf_color, 1.0)
            principled_bsdf.inputs['Roughness'].default_value = 0.5


    # --- Collection for the tree ---
    tree_collection_name = f"{object_name}_Collection"
    if tree_collection_name not in bpy.data.collections:
        tree_collection = bpy.data.collections.new(tree_collection_name)
        scene.collection.children.link(tree_collection)
    else:
        tree_collection = bpy.data.collections[tree_collection_name]
    
    # Remove existing objects with the same name from the collection to avoid duplicates
    for obj in tree_collection.objects:
        if obj.name.startswith(object_name):
            bpy.data.objects.remove(obj, do_unlink=True)


    # --- Trunk Creation ---
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=trunk_vertices,
        radius=trunk_radius,
        depth=trunk_height,
        location=(0, 0, trunk_height / 2) # Base at Z=0
    )
    trunk_obj = bpy.context.active_object
    trunk_obj.name = f"{object_name}_Trunk"
    
    # Assign trunk material
    if trunk_obj.data.materials:
        trunk_obj.data.materials[0] = trunk_mat
    else:
        trunk_obj.data.materials.append(trunk_mat)

    # Apply auto smooth
    trunk_obj.data.use_auto_smooth = True
    trunk_obj.data.auto_smooth_angle = smooth_angle_rad
    
    # Link to tree collection
    if trunk_obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(trunk_obj)
    tree_collection.objects.link(trunk_obj)


    # --- Leaf Layers Creation ---
    created_leaf_objects_count = 0
    for i in range(leaf_layers):
        # Calculate properties for the current layer
        current_leaf_height = trunk_height * leaf_height_multiplier * (1 - i * 0.1) # Taper height
        current_base_radius = trunk_radius * leaf_layers * leaf_base_radius_multiplier * (1 - i * 0.15) # Taper radius
        current_top_radius = current_base_radius * leaf_top_radius_multiplier
        
        # Vertical position for the layer
        z_pos = trunk_height + (i * current_leaf_height * 0.7)
        
        # Add a circle as the base for the leaf layer
        bpy.ops.mesh.primitive_circle_add(
            vertices=trunk_vertices, # Match trunk vertices for consistency
            radius=current_base_radius,
            fill_type='NGON', # Fill the circle
            location=(0, 0, z_pos)
        )
        leaf_obj = bpy.context.active_object
        leaf_obj.name = f"{object_name}_Leaf_{i + 1}"

        # Assign leaf material
        if leaf_obj.data.materials:
            leaf_obj.data.materials[0] = leaf_mat
        else:
            leaf_obj.data.materials.append(leaf_mat)

        # Enter Edit Mode to extrude and scale
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(leaf_obj.data)
        
        # Select the single face of the circle
        for face in bm.faces:
            face.select = True
        
        # Extrude the face upwards
        extrude_vec = Vector((0, 0, current_leaf_height))
        ret = bmesh.ops.extrude_face_region(bm, geom=bm.faces)
        
        # Get the new top face (the extruded part)
        extruded_faces = [f for f in ret['geom'] if isinstance(f, bmesh.types.BMFace)]
        if extruded_faces:
            top_face = extruded_faces[0]
            
            # Scale the top face down
            # Need to deselect previous faces and select only the top for scaling
            for face in bm.faces:
                face.select = False
            top_face.select = True
            
            bmesh.update_edit_mesh(leaf_obj.data) # Update bmesh to reflect selection for ops
            
            bpy.ops.transform.resize(value=(leaf_top_radius_multiplier, leaf_top_radius_multiplier, 1), 
                                     orient_type='NORMAL')
        
        # Re-select all for auto smooth
        for face in bm.faces:
            face.select = True
        
        bmesh.update_edit_mesh(leaf_obj.data)
        bmesh.free(bm)
        
        # Exit Edit Mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Apply auto smooth to leaf layer
        leaf_obj.data.use_auto_smooth = True
        leaf_obj.data.auto_smooth_angle = smooth_angle_rad

        # Rotate the leaf layer for variation
        leaf_obj.rotation_euler.z = math.radians(i * leaf_rotation_step)

        # Link to tree collection
        if leaf_obj.name in bpy.context.collection.objects:
            bpy.context.collection.objects.unlink(leaf_obj)
        tree_collection.objects.link(leaf_obj)
        created_leaf_objects_count += 1
        
    # --- Parent to an empty object for easier scene management (optional but good practice) ---
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    parent_empty = bpy.context.active_object
    parent_empty.name = f"{object_name}_Parent"
    
    # Link parent empty to the tree collection
    if parent_empty.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(parent_empty)
    tree_collection.objects.link(parent_empty)

    # Parent all tree components to the empty
    tree_components = [trunk_obj] + [obj for obj in bpy.data.objects if obj.name.startswith(f"{object_name}_Leaf_")]
    bpy.ops.object.select_all(action='DESELECT')
    for comp in tree_components:
        comp.select_set(True)
    parent_empty.select_set(True)
    bpy.context.view_layer.objects.active = parent_empty
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

    # Set location and scale of the parent empty
    parent_empty.location = Vector(location)
    parent_empty.scale = (scale, scale, scale)

    return f"Created '{object_name}' at {location} with {created_leaf_objects_count + 1} objects (plus parent empty)"

