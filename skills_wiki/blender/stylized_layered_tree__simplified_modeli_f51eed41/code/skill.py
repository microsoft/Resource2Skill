def create_stylized_tree(
    scene_name: str = "Scene",
    object_name: str = "StylizedTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    trunk_color: tuple = (0.4, 0.2, 0.0, 1.0),  # RGBA
    leaf_color: tuple = (0.1, 0.5, 0.1, 1.0),  # RGBA
    num_leaf_layers: int = 4,
    leaf_spacing_factor: float = 0.5,
    leaf_scale_factor: float = 0.7,
    leaf_rotation_offset: float = 15.0,  # degrees
) -> str:
    """
    Create a stylized low-poly Christmas tree using core Blender operations.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created tree object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        trunk_color: (R, G, B, A) color for the trunk.
        leaf_color: (R, G, B, A) color for the leaves.
        num_leaf_layers: Number of leaf layers.
        leaf_spacing_factor: Vertical spacing between leaf layers.
        leaf_scale_factor: How much each subsequent leaf layer scales down.
        leaf_rotation_offset: Degrees to rotate each leaf layer for a spiral effect.

    Returns:
        Status string, e.g., "Created 'StylizedTree' at (0, 0, 0) with 2 objects"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Materials ---
    # Trunk Material
    trunk_mat = bpy.data.materials.new(name=f"{object_name}_TrunkMat")
    trunk_mat.use_nodes = True
    if "Principled BSDF" in trunk_mat.node_tree.nodes:
        bsdf_trunk = trunk_mat.node_tree.nodes["Principled BSDF"]
        bsdf_trunk.inputs["Base Color"].default_value = trunk_color
        bsdf_trunk.inputs["Roughness"].default_value = 0.7

    # Leaf Material
    leaf_mat = bpy.data.materials.new(name=f"{object_name}_LeafMat")
    leaf_mat.use_nodes = True
    if "Principled BSDF" in leaf_mat.node_tree.nodes:
        bsdf_leaf = leaf_mat.node_tree.nodes["Principled BSDF"]
        bsdf_leaf.inputs["Base Color"].default_value = leaf_color
        bsdf_leaf.inputs["Roughness"].default_value = 0.5

    # --- Create Parent Object for the entire tree ---
    tree_parent_obj = bpy.data.objects.new(object_name, None)
    scene.collection.objects.link(tree_parent_obj)

    # --- Trunk ---
    # Add initial cylinder for trunk
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16, radius=0.2, depth=1.5,
        location=(0, 0, 0)
    )
    trunk_obj = bpy.context.active_object
    trunk_obj.name = f"{object_name}_Trunk"
    trunk_obj.data.materials.append(trunk_mat)
    trunk_obj.parent = tree_parent_obj

    # Scale the trunk (S then Z, then S overall)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.resize(value=(0.5, 0.5, 1.0), orient_type='GLOBAL', constraint_axis=(False, False, True)) # S Z
    bpy.ops.transform.resize(value=(0.5, 0.5, 0.5), orient_type='GLOBAL') # S overall
    
    # Add a loop cut and scale top/bottom faces
    bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts":1}, TRANSFORM_OT_edge_slide={"value":0})
    
    bm = bmesh.from_edit_mesh(trunk_obj.data)
    bpy.ops.mesh.select_mode(type="FACE")
    
    # Select and scale top face
    bpy.ops.mesh.select_all(action='DESELECT')
    top_face_verts = [v for v in bm.verts if v.co.z > 0.6] # Select verts near top
    bpy.ops.mesh.select_face_by_verts() # Select face from verts (won't work directly if face isn't selected)
    
    # Simpler way to select top/bottom faces programmatically
    top_face = None
    bottom_face = None
    for face in bm.faces:
        face.select = False # Deselect all faces first
        if face.normal.z > 0.9: 
            top_face = face
        elif face.normal.z < -0.9: 
            bottom_face = face
    
    if top_face:
        top_face.select = True
        bmesh.update_edit_mesh(trunk_obj.data)
        bpy.ops.transform.resize(value=(0.7, 0.7, 1.0), orient_type='NORMAL') # S on top face
        top_face.select = False
        
    if bottom_face:
        bottom_face.select = True
        bmesh.update_edit_mesh(trunk_obj.data)
        bpy.ops.transform.resize(value=(1.3, 1.3, 1.0), orient_type='NORMAL') # S on bottom face
        bottom_face.select = False

    bmesh.update_edit_mesh(trunk_obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    # --- Leaf Layers ---
    current_leaf_base_radius = 0.5 * scale # Starting size for first leaf layer
    current_z_pos = trunk_obj.dimensions.z / 2 # Start from top of trunk, adjusted for trunk_obj's scale
    
    for i in range(num_leaf_layers):
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16, radius=current_leaf_base_radius * 1.5, depth=0.2, # Start with a cylinder base
            location=(0, 0, current_z_pos)
        )
        leaf_obj = bpy.context.active_object
        leaf_obj.name = f"{object_name}_Leaf_{i}"
        leaf_obj.data.materials.append(leaf_mat)
        leaf_obj.parent = tree_parent_obj # Parent to main tree object

        # Scale flat (S then Z) and shape into a cone
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.resize(value=(1.0, 1.0, 0.2), orient_type='GLOBAL', constraint_axis=(False, False, True)) # S Z (flatten)
        
        bm = bmesh.from_edit_mesh(leaf_obj.data)
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.mesh.select_all(action='DESELECT')
        
        top_face_leaf = None
        bottom_face_leaf = None
        for face in bm.faces:
            if face.normal.z > 0.9: top_face_leaf = face
            elif face.normal.z < -0.9: bottom_face_leaf = face
            
        if top_face_leaf:
            top_face_leaf.select = True
            bmesh.update_edit_mesh(leaf_obj.data)
            bpy.ops.transform.resize(value=(0.5, 0.5, 1.0), orient_type='NORMAL') # S on top face (make conical)
            top_face_leaf.select = False
            
        if bottom_face_leaf:
            bottom_face_leaf.select = True
            bmesh.update_edit_mesh(leaf_obj.data)
            bpy.ops.transform.resize(value=(1.0, 1.0, 1.0), orient_type='NORMAL') # S on bottom face (no change, but keeps consistency)
            bottom_face_leaf.select = False
        
        bmesh.update_edit_mesh(leaf_obj.data)

        # Extrude base of leaf down and scale out for flare (E Z S)
        # This replicates the visual of the tutorial's interactive "leaf detail"
        bpy.ops.mesh.select_all(action='DESELECT') # Deselect previous
        if bottom_face_leaf:
            bottom_face_leaf.select = True
            bmesh.update_edit_mesh(leaf_obj.data)
            
            # E (extrude), Z (constrain to Z), move down
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0,0,-0.05)})
            
            # S (scale out)
            bpy.ops.transform.resize(value=(1.2, 1.2, 1.0), orient_type='GLOBAL')
            
            bottom_face_leaf.select = False # Deselect for next op
        
        bmesh.update_edit_mesh(leaf_obj.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rotate leaf layer for spiral effect
        leaf_obj.rotation_euler.z = math.radians(i * leaf_rotation_offset)

        # Prepare for next layer
        current_z_pos += leaf_obj.dimensions.z * leaf_spacing_factor * (i + 1) / 2 # Adjust spacing
        current_leaf_base_radius *= leaf_scale_factor
        
    # Finalize tree_parent_obj location and scale
    tree_parent_obj.location = Vector(location)
    tree_parent_obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' at {location} with {num_leaf_layers + 1} objects"

