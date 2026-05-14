def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    trunk_color: tuple = (0.3, 0.15, 0.05, 1.0),  # RGB alpha
    foliage_color: tuple = (0.1, 0.4, 0.1, 1.0), # RGB alpha
    num_foliage_layers: int = 4,
    foliage_layer_base_scale: float = 0.5,
    foliage_layer_height_offset: float = 0.5,
    foliage_extrude_in_factor: float = 0.8,
    foliage_extrude_normal_amount: float = 0.1,
    **kwargs,
) -> str:
    """
    Create a stylized low-poly tree in the active Blender scene using fundamental modeling operations.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the main tree collection/trunk.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        trunk_color: (R, G, B, A) base color for the tree trunk.
        foliage_color: (R, G, B, A) base color for the tree foliage.
        num_foliage_layers: Number of foliage cone sections.
        foliage_layer_base_scale: Initial scale for the largest foliage layer.
        foliage_layer_height_offset: Vertical spacing between foliage layers.
        foliage_extrude_in_factor: Factor for extruding bottom faces of foliage inwards.
        foliage_extrude_normal_amount: Amount for extruding faces along normals on foliage.
        **kwargs: Additional overrides (e.g., trunk_segments for cylinder detail).

    Returns:
        Status string, e.g., "Created 'StylizedTree' at (0, 0, 0) with 1 trunk and 4 foliage objects."
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Deselect all objects to ensure clean selection for operations
    bpy.ops.object.select_all(action='DESELECT')

    # --- Materials ---
    trunk_mat = bpy.data.materials.new(name=f"{object_name}_TrunkMat")
    trunk_mat.use_nodes = True
    bsdf = trunk_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = trunk_color
    trunk_mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.7 # Roughness

    foliage_mat = bpy.data.materials.new(name=f"{object_name}_FoliageMat")
    foliage_mat.use_nodes = True
    bsdf = foliage_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = foliage_color
    foliage_mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.7 # Roughness

    # --- Create Trunk ---
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16, radius=0.1 * scale, depth=1.5 * scale,
        enter_editmode=False, align='WORLD',
        location=location
    )
    trunk_obj = bpy.context.active_object
    trunk_obj.name = f"{object_name}_Trunk"
    trunk_obj.data.materials.append(trunk_mat)
    
    # Scale trunk for more natural shape
    bpy.context.view_layer.objects.active = trunk_obj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(trunk_obj.data)
    
    # Select top face
    top_face = None
    for face in bm.faces:
        if face.normal.z > 0.9: # Check for upward normal
            top_face = face
            break
    if top_face:
        top_face.select = True
        bmesh.update_edit_mesh(trunk_obj.data)
        bpy.ops.transform.resize(value=(0.7, 0.7, 1), orient_type='NORMAL') # Scale top face inwards
        top_face.select = False # Deselect after operation

    # Select bottom face
    bottom_face = None
    for face in bm.faces:
        if face.normal.z < -0.9: # Check for downward normal
            bottom_face = face
            break
    if bottom_face:
        bottom_face.select = True
        bmesh.update_edit_mesh(trunk_obj.data)
        bpy.ops.transform.resize(value=(1.2, 1.2, 1), orient_type='NORMAL') # Scale bottom face outwards
        bottom_face.select = False # Deselect after operation

    bmesh.update_edit_mesh(trunk_obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    trunk_obj.location = Vector(location)
    trunk_obj.scale = (scale, scale, scale) # Apply overall scale last

    # --- Create Foliage Layers ---
    foliage_objects = []
    for i in range(num_foliage_layers):
        current_layer_scale_factor = foliage_layer_base_scale * (1 - (i / num_foliage_layers) * 0.4) # Smaller upwards
        
        layer_loc_z = location[2] + trunk_obj.dimensions.z * trunk_obj.scale.z / 2 + (i * foliage_layer_height_offset * scale)
        if i == 0: # First layer starts lower
            layer_loc_z = location[2] + trunk_obj.dimensions.z * trunk_obj.scale.z / 2 * 0.5
        
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16, radius=0.5 * current_layer_scale_factor * scale, depth=0.7 * scale,
            enter_editmode=False, align='WORLD',
            location=(location[0], location[1], layer_loc_z)
        )
        foliage_obj = bpy.context.active_object
        foliage_obj.name = f"{object_name}_Foliage_{i+1}"
        foliage_obj.data.materials.append(foliage_mat)
        
        # Scale top face to make it conical
        bpy.context.view_layer.objects.active = foliage_obj
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(foliage_obj.data)
        
        top_face = None
        for face in bm.faces:
            if face.normal.z > 0.9:
                top_face = face
                break
        if top_face:
            top_face.select = True
            bmesh.update_edit_mesh(foliage_obj.data)
            bpy.ops.transform.resize(value=(0.2, 0.2, 1), orient_type='NORMAL')
            top_face.select = False

        # --- Extrude Inwards then Extrude Along Normals (mimics video 5:39) ---
        bottom_face = None
        for face in bm.faces:
            if face.normal.z < -0.9:
                bottom_face = face
                break
        if bottom_face:
            bottom_face.select = True
            bmesh.update_edit_mesh(foliage_obj.data)
            
            # Extrude inwards (E then S)
            bpy.ops.mesh.extrude_region_shrink_fatten(TRANSFORM_OT_resize={"value":(foliage_extrude_in_factor, foliage_extrude_in_factor, foliage_extrude_in_factor), "orient_type":'LOCAL'})
            
            # Extrude faces along normals (Alt+E -> Along Normals)
            bpy.ops.mesh.extrude_faces_along_normals(TRANSFORM_OT_translate={"value":(0,0,-foliage_extrude_normal_amount*scale)})
            
            # Scale inwards after normal extrusion
            bpy.ops.transform.resize(value=(0.7, 0.7, 1), orient_type='NORMAL')
            
            bottom_face.select = False

        bmesh.update_edit_mesh(foliage_obj.data)
        bpy.ops.object.mode_set(mode='OBJECT')

        # Random rotation for variation
        foliage_obj.rotation_euler.z = math.radians(i * (360 / num_foliage_layers) * 0.618)
        
        # Parent to trunk
        foliage_obj.parent = trunk_obj
        foliage_objects.append(foliage_obj)
        
    # --- Finalize ---
    # Put all tree parts into a new collection
    tree_collection = bpy.data.collections.new(object_name)
    scene.collection.children.link(tree_collection)
    
    tree_collection.objects.link(trunk_obj)
    for f_obj in foliage_objects:
        tree_collection.objects.link(f_obj)

    # Move all objects in the scene into the new collection (they were already parented to the trunk)
    # The trunk itself is moved when linked, and its children follow.
    
    # Deselect everything at the end
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created '{object_name}' at {location} with {1 + num_foliage_layers} objects."

