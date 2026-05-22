def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    trunk_color: tuple = (0.2, 0.1, 0.05, 1.0), # R, G, B, A
    leaves_color: tuple = (0.1, 0.4, 0.1, 1.0), # R, G, B, A
    trunk_verts: int = 8,
    leaves_verts: int = 12,
    num_leaf_layers: int = 5,
    leaf_height_scale: float = 0.5, # Vertical spacing between layers
    leaf_base_scale: float = 1.5, # Initial scale for bottom leaf layer
    leaf_taper_factor: float = 0.8, # Scale factor for each subsequent leaf layer
    leaf_rotation_offset: float = math.pi / 6, # Z-axis rotation offset per layer
    **kwargs,
) -> str:
    """
    Create a low-poly stylized pine tree in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created tree object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        trunk_color: (R, G, B, A) base color for the trunk.
        leaves_color: (R, G, B, A) base color for the leaves.
        trunk_verts: Number of vertices for the trunk cylinder.
        leaves_verts: Number of vertices for the leaf circles.
        num_leaf_layers: Number of distinct leaf layers.
        leaf_height_scale: Vertical spacing between leaf layers.
        leaf_base_scale: Initial scale for the bottom leaf layer relative to trunk.
        leaf_taper_factor: Scale factor for each subsequent leaf layer.
        leaf_rotation_offset: Z-axis rotation offset per layer in radians.
        **kwargs: Additional overrides (not used in this skill but for compatibility).

    Returns:
        Status string, e.g., "Created 'LowPolyTree' at (0, 0, 0) with 2 objects"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Clear current selection
    bpy.ops.object.select_all(action='DESELECT')

    # --- Materials ---
    trunk_mat = bpy.data.materials.new(name=f"{object_name}_TrunkMat")
    trunk_mat.use_nodes = True
    bsdf = trunk_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = trunk_color
    trunk_mat.use_auto_smooth = True
    trunk_mat.auto_smooth_angle = math.radians(60)

    leaves_mat = bpy.data.materials.new(name=f"{object_name}_LeavesMat")
    leaves_mat.use_nodes = True
    bsdf = leaves_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = leaves_color
    leaves_mat.use_auto_smooth = True
    leaves_mat.auto_smooth_angle = math.radians(60)

    # --- Trunk ---
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=trunk_verts,
        radius=0.1 * scale,
        depth=0.5 * scale,
        location=location
    )
    trunk_obj = bpy.context.active_object
    trunk_obj.name = f"{object_name}_Trunk"

    # Apply material
    if trunk_obj.data.materials:
        trunk_obj.data.materials[0] = trunk_mat
    else:
        trunk_obj.data.materials.append(trunk_mat)

    # Taper the trunk in Edit Mode
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(trunk_obj.data)
    
    # Select top face
    top_face = None
    for face in bm.faces:
        face.select = False # Deselect all faces first
        if face.normal.z > 0.9: # Identify top face
            face.select = True
            top_face = face
            break
    
    if top_face:
        # Extrude up
        extrude_dist = 0.5 * scale # Original depth was 0.5, so extrude by that much
        bmesh.ops.extrude_region_split(bm, geom=[top_face])
        new_face = bm.faces[-1] # The newly extruded face
        bmesh.ops.translate(bm, verts=new_face.verts, vec=Vector((0, 0, extrude_dist)))

        # Scale the new top face down
        bmesh.ops.scale(bm, geom=new_face.verts, vec=(0.5, 0.5, 1.0))
        
        # Extrude again for a finer tip
        bmesh.ops.extrude_region_split(bm, geom=[new_face])
        final_face = bm.faces[-1]
        bmesh.ops.translate(bm, verts=final_face.verts, vec=Vector((0, 0, extrude_dist * 0.5)))
        bmesh.ops.scale(bm, geom=final_face.verts, vec=(0.2, 0.2, 1.0))


    bmesh.update_edit_mesh(trunk_obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()


    # --- Leaves ---
    leaf_objects = []
    parent_obj = None

    for i in range(num_leaf_layers):
        # Calculate current layer's position, scale, and rotation
        current_z = location[2] + (1.0 * scale) + (i * leaf_height_scale * scale)
        current_scale_factor = leaf_base_scale * (leaf_taper_factor ** (num_leaf_layers - 1 - i)) * scale
        current_rotation_z = i * leaf_rotation_offset

        bpy.ops.mesh.primitive_circle_add(
            vertices=leaves_verts,
            radius=0.5 * current_scale_factor,
            fill_type='NGON',
            location=(location[0], location[1], current_z)
        )
        leaf_obj = bpy.context.active_object
        leaf_obj.name = f"{object_name}_LeafLayer_{i+1}"
        leaf_objects.append(leaf_obj)

        # Apply rotation
        leaf_obj.rotation_euler.z = current_rotation_z

        # Apply material
        if leaf_obj.data.materials:
            leaf_obj.data.materials[0] = leaves_mat
        else:
            leaf_obj.data.materials.append(leaves_mat)
        
        # Shape the leaf layers (extrude and scale)
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(leaf_obj.data)
        
        # Select all faces for initial extrusion
        for face in bm.faces:
            face.select = True

        # Extrude down
        extrude_dist_leaf = -0.2 * scale # Extrude downwards
        bmesh.ops.extrude_region_split(bm, geom=bm.faces)
        new_faces = [f for f in bm.faces if not f.select] # Newly extruded faces
        
        # Translate the new faces downwards
        bmesh.ops.translate(bm, verts=[v for f in new_faces for v in f.verts], vec=Vector((0, 0, extrude_dist_leaf)))
        
        # Scale the bottom faces
        bmesh.ops.scale(bm, geom=[v for f in new_faces for v in f.verts], vec=(0.5, 0.5, 1.0))

        bmesh.update_edit_mesh(leaf_obj.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.shade_smooth()

        # Set parent for all leaf layers to the trunk
        if parent_obj is None:
            parent_obj = trunk_obj
        leaf_obj.parent = parent_obj

    # Select all created objects and group them under an empty (optional, for scene organization)
    all_created_objects = [trunk_obj] + leaf_objects
    bpy.ops.object.select_all(action='DESELECT')
    for obj in all_created_objects:
        obj.select_set(True)
    
    # Create an empty as the parent for all tree components
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    main_empty = bpy.context.active_object
    main_empty.name = f"{object_name}_Container"
    
    # Parent all tree components to the empty
    bpy.ops.object.parent_set(type='OBJECT')

    return f"Created '{object_name}' at {location} with {len(all_created_objects) + 1} objects"

