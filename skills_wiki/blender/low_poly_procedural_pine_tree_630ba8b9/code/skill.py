def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.5, 0.1),  # Default green for branches
    trunk_color: tuple = (0.4, 0.2, 0.1),  # Default brown for trunk
    num_trunk_verts: int = 8,
    num_branch_verts: int = 12,
    num_branch_layers: int = 5,
    layer_height_offset: float = 0.5,
    layer_scale_factor: float = 0.8,
    layer_rotation_offset: float = 30.0,  # Degrees for rotational variation
    **kwargs,
) -> str:
    """
    Create a low-poly pine tree model using basic mesh operations.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created tree object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the tree branches in 0-1 range.
        trunk_color: (R, G, B) base color for the tree trunk in 0-1 range.
        num_trunk_verts: Number of vertices for the trunk cylinder.
        num_branch_verts: Number of vertices for each branch layer circle.
        num_branch_layers: Number of branch layers in the tree.
        layer_height_offset: Vertical distance between branch layers.
        layer_scale_factor: Scaling factor for subsequent branch layers.
        layer_rotation_offset: Degrees to rotate each subsequent layer for variety.
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'LowPolyTree' at (0, 0, 0) with 6 objects"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Create Collection for the tree ---
    tree_collection_name = f"{object_name}_Collection"
    if tree_collection_name not in bpy.data.collections:
        tree_collection = bpy.data.collections.new(name=tree_collection_name)
        scene.collection.children.link(tree_collection)
    else:
        tree_collection = bpy.data.collections[tree_collection_name]

    # --- Create Materials ---
    trunk_mat_name = f"{object_name}_Trunk_Material"
    if trunk_mat_name not in bpy.data.materials:
        trunk_mat = bpy.data.materials.new(name=trunk_mat_name)
        trunk_mat.use_nodes = True
        bsdf = trunk_mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = trunk_color + (1.0,)
        trunk_mat.use_backface_culling = True
    else:
        trunk_mat = bpy.data.materials[trunk_mat_name]

    branches_mat_name = f"{object_name}_Branches_Material"
    if branches_mat_name not in bpy.data.materials:
        branches_mat = bpy.data.materials.new(name=branches_mat_name)
        branches_mat.use_nodes = True
        bsdf = branches_mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = material_color + (1.0,)
        branches_mat.use_backface_culling = True
    else:
        branches_mat = bpy.data.materials[branches_mat_name]

    # --- Create Trunk ---
    # Start with a cylinder
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=num_trunk_verts,
        radius=0.15 * scale,
        depth=1.0 * scale,
        location=location
    )
    trunk_obj = bpy.context.active_object
    trunk_obj.name = f"{object_name}_Trunk"
    tree_collection.objects.link(trunk_obj)
    scene.collection.objects.unlink(trunk_obj) # Unlink from default scene collection

    # Assign trunk material
    if trunk_obj.data.materials:
        trunk_obj.data.materials[0] = trunk_mat
    else:
        trunk_obj.data.materials.append(trunk_mat)

    # Taper the trunk using bmesh (Extrude top face up and scale)
    bpy.context.view_layer.objects.active = trunk_obj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(trunk_obj.data)

    top_face = None
    for face in bm.faces:
        if face.normal.z > 0.9:  # Identify top face by normal direction
            top_face = face
            break

    if top_face:
        # Extrude the top face upwards
        extruded_geom = bmesh.ops.extrude_face_region(bm, geom=[top_face])
        new_verts = [v for v in extruded_geom["geom"] if isinstance(v, bmesh.types.BMVert)]
        
        # Move the newly extruded vertices up
        bmesh.ops.translate(bm, verts=new_verts, vec=(0, 0, 0.3 * scale))
        
        # Scale the new top face inwards to taper
        bmesh.ops.scale(bm, verts=new_verts, vec=(0.5, 0.5, 1.0))
    
    bmesh.update_edit_mesh(trunk_obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Shade smooth auto smooth for the trunk
    bpy.ops.object.shade_smooth()
    trunk_obj.data.use_auto_smooth = True
    trunk_obj.data.auto_smooth_angle = math.radians(30)


    # --- Create Branch Layers ---
    current_z = location[2] + (0.8 * scale)  # Start slightly above trunk top
    
    for i in range(num_branch_layers):
        # Calculate scale and rotation for each layer
        layer_overall_scale = (1.0 - i * (1.0 / num_branch_layers / 1.5)) * scale * layer_scale_factor
        if layer_overall_scale < 0.1: # Prevent layers from becoming too small
            layer_overall_scale = 0.1

        # Add a circle for the current branch layer
        bpy.ops.mesh.primitive_circle_add(
            vertices=num_branch_verts,
            radius=0.4 * layer_overall_scale,  # Base radius for the layer
            location=(location[0], location[1], current_z)
        )
        layer_obj = bpy.context.active_object
        layer_obj.name = f"{object_name}_BranchLayer_{i+1}"
        tree_collection.objects.link(layer_obj)
        scene.collection.objects.unlink(layer_obj) # Unlink from default scene collection
        
        # Assign branches material
        if layer_obj.data.materials:
            layer_obj.data.materials[0] = branches_mat
        else:
            layer_obj.data.materials.append(branches_mat)

        bpy.context.view_layer.objects.active = layer_obj
        bpy.ops.object.mode_set(mode='EDIT')
        bm_layer = bmesh.from_edit_mesh(layer_obj.data)

        # Extrude downwards and scale to create the conical frustum shape
        # Select all edges of the circle (bottom perimeter if cap_ends=False)
        outer_edges = [e for e in bm_layer.edges]
        
        # Extrude down and scale outwards
        extruded_geom_1 = bmesh.ops.extrude_edge_only(bm_layer, edges=outer_edges)
        verts_extruded_1 = [v for v in extruded_geom_1["geom"] if isinstance(v, bmesh.types.BMVert)]
        
        bmesh.ops.translate(bm_layer, verts=verts_extruded_1, vec=(0, 0, -0.2 * layer_overall_scale)) # Move down
        bmesh.ops.scale(bm_layer, verts=verts_extruded_1, vec=(1.2, 1.2, 1.0)) # Scale outwards slightly

        # Extrude again further down, and scale to a point
        extruded_geom_2 = bmesh.ops.extrude_edge_only(bm_layer, edges=[e for e in bm_layer.edges if e.is_manifold])
        verts_extruded_2 = [v for v in extruded_geom_2["geom"] if isinstance(v, bmesh.types.BMVert)]
        
        bmesh.ops.translate(bm_layer, verts=verts_extruded_2, vec=(0, 0, -0.3 * layer_overall_scale)) # Move down more
        bmesh.ops.scale(bm_layer, verts=verts_extruded_2, vec=(0.1, 0.1, 1.0)) # Scale to a point

        bmesh.update_edit_mesh(layer_obj.data)
        bpy.ops.object.mode_set(mode='OBJECT')

        # Rotate layer for variation
        layer_obj.rotation_euler.z += math.radians(i * layer_rotation_offset)

        # Shade smooth auto smooth for the branch layer
        bpy.ops.object.shade_smooth()
        layer_obj.data.use_auto_smooth = True
        layer_obj.data.auto_smooth_angle = math.radians(30)

        # Parent to trunk
        layer_obj.parent = trunk_obj
        layer_obj.matrix_parent_inverse = trunk_obj.matrix_world.inverted()

        current_z += layer_height_offset * scale

    # Deselect all objects at the end
    bpy.ops.object.select_all(action='DESELECT')
    trunk_obj.select_set(True) # Select the trunk for reference
    bpy.context.view_layer.objects.active = trunk_obj # Make trunk active

    return f"Created '{object_name}' at {location} with {num_branch_layers + 1} objects"

