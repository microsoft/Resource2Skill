def create_basic_low_poly_pine_tree(
    scene_name: str = "Scene",
    object_name: str = "LowPolyPineTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    trunk_color_rgb: tuple = (0.3, 0.15, 0.05),  # Brown
    leaf_color_rgb: tuple = (0.1, 0.4, 0.1),     # Green
    leaf_layers: int = 4,
    leaf_segments_verts: int = 12,
    trunk_segments_verts: int = 8,
    **kwargs,
) -> str:
    """
    Create a basic low-poly pine tree in the active Blender scene,
    mimicking the techniques demonstrated in the tutorial.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created tree object(s).
        location: (x, y, z) world-space position for the tree's base.
        scale: Uniform scale factor for the entire tree (1.0 = default size).
        trunk_color_rgb: (R, G, B) base color for the trunk in 0-1 range.
        leaf_color_rgb: (R, G, B) base color for the leaves in 0-1 range.
        leaf_layers: Number of stacked leaf layers.
        leaf_segments_verts: Number of vertices for each leaf layer circle.
        trunk_segments_verts: Number of vertices for the trunk cylinder.
        **kwargs: Additional overrides (not used in this specific implementation).

    Returns:
        Status string, e.g., "Created 'LowPolyPineTree' at (0, 0, 0) with 5 objects"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Materials ---
    # Create Trunk Material
    trunk_mat_name = f"{object_name}_TrunkMat"
    trunk_mat = bpy.data.materials.new(name=trunk_mat_name)
    trunk_mat.use_nodes = True
    if trunk_mat.node_tree.nodes.get("Principled BSDF"):
        trunk_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*trunk_color_rgb, 1.0)
    
    # Create Leaf Material
    leaf_mat_name = f"{object_name}_LeafMat"
    leaf_mat = bpy.data.materials.new(name=leaf_mat_name)
    leaf_mat.use_nodes = True
    if leaf_mat.node_tree.nodes.get("Principled BSDF"):
        leaf_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*leaf_color_rgb, 1.0)

    # --- Trunk Creation ---
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=trunk_segments_verts,
        radius=0.2 * scale,
        depth=1.0 * scale,
        location=location
    )
    trunk_obj = bpy.context.active_object
    trunk_obj.name = f"{object_name}_Trunk"

    # Edit mode for trunk tapering
    bpy.context.view_layer.objects.active = trunk_obj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(trunk_obj.data)

    # Select top face
    top_face = None
    for face in bm.faces:
        if face.normal.z > 0.9: # Assuming cylinder is aligned with Z
            top_face = face
            break
    
    if top_face:
        top_face.select = True
        
        # Extrude top face up (G Z)
        extruded_geom = bmesh.ops.extrude_face_region(bm, geom=[top_face])
        top_extruded_face = [ele for ele in extruded_geom['geom'] if isinstance(ele, bmesh.types.BMFace)][0]
        
        bmesh.ops.translate(bm, verts=top_extruded_face.verts, vec=Vector((0, 0, 0.5 * scale)))
        
        # Scale top face (S)
        bmesh.ops.scale(bm, verts=top_extruded_face.verts, vec=Vector((0.5, 0.5, 1.0)))

    bmesh.update_edit_mesh(trunk_obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    trunk_obj.data.materials.append(trunk_mat)
    trunk_obj.data.use_auto_smooth = True
    trunk_obj.data.auto_smooth_angle = math.radians(30) # Default auto smooth angle
    bpy.ops.object.shade_smooth()

    # --- Leaf Layers Creation ---
    leaf_objects = []
    initial_leaf_height = location[2] + 0.5 * scale # Start slightly above trunk base

    for i in range(leaf_layers):
        current_layer_scale = scale * (1 - i * 0.15) # Scale down successive layers
        current_layer_height = initial_leaf_height + (i * 0.4 * scale)
        current_layer_rotation_z = math.radians(i * 30) # Rotate layers

        bpy.ops.mesh.primitive_circle_add(
            vertices=leaf_segments_verts,
            radius=0.7 * current_layer_scale,
            fill_type='NGON',
            location=(location[0], location[1], current_layer_height)
        )
        leaf_obj = bpy.context.active_object
        leaf_obj.name = f"{object_name}_Leaf_{i+1}"

        # Edit mode for leaf frustum shape
        bpy.context.view_layer.objects.active = leaf_obj
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(leaf_obj.data)

        # Select all faces (the NGON)
        for face in bm.faces:
            face.select = True
        
        # Extrude up and scale inwards
        extruded_geom = bmesh.ops.extrude_face_region(bm, geom=bm.faces)
        top_extruded_face = [ele for ele in extruded_geom['geom'] if isinstance(ele, bmesh.types.BMFace)][0]
        
        bmesh.ops.translate(bm, verts=top_extruded_face.verts, vec=Vector((0, 0, 0.2 * current_layer_scale)))
        bmesh.ops.scale(bm, verts=top_extruded_face.verts, vec=Vector((0.5, 0.5, 1.0)))

        bmesh.update_edit_mesh(leaf_obj.data)
        bpy.ops.object.mode_set(mode='OBJECT')

        leaf_obj.data.materials.append(leaf_mat)
        leaf_obj.data.use_auto_smooth = True
        leaf_obj.data.auto_smooth_angle = math.radians(30)
        bpy.ops.object.shade_smooth()
        
        leaf_obj.rotation_euler.z = current_layer_rotation_z
        leaf_objects.append(leaf_obj)

    # --- Parenting ---
    bpy.ops.object.select_all(action='DESELECT')
    for obj in leaf_objects:
        obj.select_set(True)
    trunk_obj.select_set(True)
    bpy.context.view_layer.objects.active = trunk_obj
    bpy.ops.object.parent_set(type='OBJECT')

    return f"Created '{object_name}' at {location} with {1 + leaf_layers} objects"

