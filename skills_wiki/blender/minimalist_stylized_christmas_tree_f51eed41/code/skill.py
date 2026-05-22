def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedChristmasTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    trunk_color: tuple = (0.4, 0.2, 0.05),  # Brown
    foliage_color: tuple = (0.1, 0.4, 0.1),  # Green
    num_foliage_layers: int = 4,
    layer_scale_factor: float = 0.8,
    layer_spacing: float = 0.6,
    layer_rotation_step: float = 0.5, # Radians
    **kwargs,
) -> str:
    """
    Create a minimalist stylized Christmas tree in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created tree object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the entire tree (1.0 = default size).
        trunk_color: (R, G, B) base color for the trunk in 0-1 range.
        foliage_color: (R, G, B) base color for the foliage in 0-1 range.
        num_foliage_layers: Number of green conical layers for the tree.
        layer_scale_factor: How much each subsequent layer scales down.
        layer_spacing: Vertical distance between foliage layers.
        layer_rotation_step: Z-axis rotation increment for each foliage layer (in radians).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'StylizedChristmasTree' at (0, 0, 0) with 5 objects"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Set Blender to Object Mode to ensure operations are in the correct context
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # Create a new collection for the tree parts
    tree_collection_name = f"{object_name}_Collection"
    if tree_collection_name not in bpy.data.collections:
        tree_collection = bpy.data.collections.new(name=tree_collection_name)
        scene.collection.children.link(tree_collection)
    else:
        tree_collection = bpy.data.collections[tree_collection_name]

    # --- Materials ---
    trunk_mat = bpy.data.materials.new(name=f"{object_name}_TrunkMat")
    trunk_mat.use_nodes = True
    bsdf = trunk_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*trunk_color, 1) # Add alpha

    foliage_mat = bpy.data.materials.new(name=f"{object_name}_FoliageMat")
    foliage_mat.use_nodes = True
    bsdf = foliage_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*foliage_color, 1) # Add alpha

    # --- Trunk ---
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16, radius=0.2 * scale, depth=1.5 * scale,
        location=location
    )
    trunk_obj = bpy.context.object
    trunk_obj.name = f"{object_name}_Trunk"
    trunk_obj.data.materials.append(trunk_mat)

    # Scale trunk on Z and taper slightly in Edit Mode
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(trunk_obj.data)

    # Select top face
    bm.faces.ensure_lookup_table()
    top_face = None
    for face in bm.faces:
        if face.normal.z > 0.9: # Identify top face by normal
            face.select = True
            top_face = face
            break
    
    if top_face:
        bpy.ops.transform.resize(value=(0.8 * scale, 0.8 * scale, 1)) # Scale top face
    
    bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts":1, "point_offset":0}, TRANSFORM_OT_edge_slide={"value":0})

    bpy.ops.mesh.select_all(action='DESELECT')

    # Select bottom face
    bottom_face = None
    for face in bm.faces:
        if face.normal.z < -0.9: # Identify bottom face
            face.select = True
            bottom_face = face
            break

    if bottom_face:
        bpy.ops.transform.resize(value=(1.2 * scale, 1.2 * scale, 1)) # Scale bottom face
    
    bpy.ops.object.mode_set(mode='OBJECT')

    # --- Foliage Layers ---
    foliage_objects = []
    base_foliage_radius = 1.0 * scale
    base_foliage_height = 0.8 * scale
    current_layer_scale = 1.0

    for i in range(num_foliage_layers):
        layer_loc_z = location[2] + (trunk_obj.dimensions.z / 2) + (i * layer_spacing * scale) + (base_foliage_height * current_layer_scale / 2)
        
        # Create a cone for the layer
        bpy.ops.mesh.primitive_cone_add(
            vertices=16, radius=base_foliage_radius * current_layer_scale, depth=base_foliage_height * current_layer_scale,
            location=(location[0], location[1], layer_loc_z)
        )
        foliage_obj = bpy.context.object
        foliage_obj.name = f"{object_name}_FoliageLayer_{i+1}"
        foliage_obj.data.materials.append(foliage_mat)

        # Parent to trunk
        foliage_obj.parent = trunk_obj
        foliage_obj.matrix_parent_inverse = trunk_obj.matrix_world.inverted()

        # Rotate layer
        bpy.ops.object.select_all(action='DESELECT')
        foliage_obj.select_set(True)
        bpy.context.view_layer.objects.active = foliage_obj
        bpy.ops.transform.rotate(value=(i * layer_rotation_step), orient_axis='Z',
                                  constraint_axis=(False, False, True),
                                  center_determinant='ORIGIN')
        
        foliage_objects.append(foliage_obj)

        current_layer_scale *= layer_scale_factor

    # Adjust final tree position based on its origin
    # (The trunk's origin is at its center, tree built upwards)
    # We might want the bottom of the trunk at the 'location'
    bpy.ops.object.select_all(action='DESELECT')
    trunk_obj.select_set(True)
    bpy.context.view_layer.objects.active = trunk_obj
    
    # Move the entire tree down so the bottom of the trunk is at the given location Z
    bpy.ops.transform.translate(value=(0, 0, -trunk_obj.dimensions.z / 2))

    # Link all objects to the new collection
    for obj in [trunk_obj] + foliage_objects:
        if obj.name in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.unlink(obj)
        if obj.name not in tree_collection.objects:
            tree_collection.objects.link(obj)

    return f"Created '{object_name}' at {location} with {1 + num_foliage_layers} objects"

