def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    trunk_color: tuple = (0.35, 0.2, 0.05, 1.0),  # RGBa
    foliage_color: tuple = (0.1, 0.4, 0.1, 1.0), # RGBa
    num_foliage_layers: int = 4,
    foliage_base_radius: float = 0.5,
    foliage_layer_height: float = 0.7,
    foliage_scale_factor: float = 0.75, # Scales radius and height of subsequent layers
    foliage_vertical_offset: float = 0.6, # Vertical distance between layers
    foliage_rotation_offset: float = 15.0, # Degrees to rotate each successive foliage layer
    foliage_bevel_segments: int = 1,
    foliage_extrude_depth_factor: float = 0.05, # Relative depth of the inner extrusion
    foliage_extrude_scale_factor: float = 0.8, # Scale factor for the inner extrusion
    **kwargs,
) -> str:
    """
    Create a stylized low-poly tree in the active Blender scene using basic modeling operations.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created tree object group.
        location: (x, y, z) world-space position for the tree.
        scale: Uniform scale factor for the entire tree.
        trunk_color: (R, G, B, A) base color for the trunk.
        foliage_color: (R, G, B, A) base color for the foliage.
        num_foliage_layers: Number of stacked foliage cones.
        foliage_base_radius: Base radius of the bottom foliage layer.
        foliage_layer_height: Base height of the bottom foliage layer.
        foliage_scale_factor: How much each subsequent foliage layer scales down (radius & height).
        foliage_vertical_offset: Vertical spacing between foliage layers (relative to layer height).
        foliage_rotation_offset: Degrees to rotate each successive foliage layer.
        foliage_bevel_segments: Number of segments for bevelling foliage edges.
        foliage_extrude_depth_factor: Depth of the inner extrusion for foliage detail (relative to layer height).
        foliage_extrude_scale_factor: Scale factor for the inner extrusion.
        **kwargs: Additional overrides (not used in this skill but for future expansion).

    Returns:
        Status string, e.g., "Created 'StylizedTree' at (0, 0, 0) with 5 objects"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    # Get the scene or use the default one
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Deselect all objects to ensure clean selection for creation
    bpy.ops.object.select_all(action='DESELECT')

    # Create a new collection for the tree
    tree_collection_name = f"{object_name}_Collection"
    if tree_collection_name not in bpy.data.collections:
        tree_collection = bpy.data.collections.new(tree_collection_name)
        scene.collection.children.link(tree_collection)
    else:
        tree_collection = bpy.data.collections[tree_collection_name]

    created_objects = []

    # --- Materials ---
    # Trunk Material
    trunk_mat_name = f"{object_name}_TrunkMat"
    trunk_mat = bpy.data.materials.get(trunk_mat_name)
    if not trunk_mat:
        trunk_mat = bpy.data.materials.new(name=trunk_mat_name)
        trunk_mat.use_nodes = True
        bsdf = trunk_mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = trunk_color
        bsdf.inputs["Roughness"].default_value = 0.7

    # Foliage Material
    foliage_mat_name = f"{object_name}_FoliageMat"
    foliage_mat = bpy.data.materials.get(foliage_mat_name)
    if not foliage_mat:
        foliage_mat = bpy.data.materials.new(name=foliage_mat_name)
        foliage_mat.use_nodes = True
        bsdf = foliage_mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = foliage_color
        bsdf.inputs["Roughness"].default_value = 0.7

    # --- Trunk ---
    trunk_radius = 0.1 * scale
    trunk_depth = 0.5 * scale
    bpy.ops.mesh.primitive_cylinder_add(
        radius=trunk_radius,
        depth=trunk_depth,
        location=Vector(location)
    )
    trunk_obj = bpy.context.object
    trunk_obj.name = f"{object_name}_Trunk"
    trunk_obj.data.materials.append(trunk_mat)
    created_objects.append(trunk_obj)

    # Scale the top face of the trunk to be slightly narrower
    bpy.context.view_layer.objects.active = trunk_obj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(trunk_obj.data)

    # Select the top face by finding verts at the highest Z-coordinate
    # (using a slight tolerance for floating point precision)
    top_z = location[2] + trunk_depth / 2
    top_face_verts = [v for v in bm.verts if abs(v.co.z - top_z) < 0.001]
    
    selected_top_face = None
    for face in bm.faces:
        if all(v in top_face_verts for v in face.verts):
            face.select = True
            selected_top_face = face
            break
    
    if selected_top_face:
        bmesh.update_edit_mesh(trunk_obj.data)
        bpy.ops.transform.resize(value=(0.7, 0.7, 1.0)) # Scale top face 70% on X and Y
        # Ensure only the top face is selected for scaling
        for v in bm.verts:
            v.select = False
        for e in bm.edges:
            e.select = False
        for f in bm.faces:
            if f != selected_top_face:
                f.select = False
        selected_top_face.select = True

    bmesh.update_edit_mesh(trunk_obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Adjust trunk origin to its base for easier positioning
    trunk_obj.location.z += trunk_depth / 2


    # --- Foliage Layers ---
    # Initial position above the trunk
    current_z = trunk_obj.location.z + trunk_depth * 0.8
    current_foliage_radius = foliage_base_radius * scale
    current_foliage_height = foliage_layer_height * scale

    foliage_objs = []
    for i in range(num_foliage_layers):
        bpy.ops.mesh.primitive_cone_add(
            radius1=current_foliage_radius,
            depth=current_foliage_height,
            location=Vector((location[0], location[1], current_z))
        )
        foliage_obj = bpy.context.object
        foliage_obj.name = f"{object_name}_Foliage_{i+1}"
        foliage_obj.data.materials.append(foliage_mat)
        
        # Apply bevel modifier for softer edges
        bevel_mod = foliage_obj.modifiers.new(name=f"Bevel_{i}", type='BEVEL')
        bevel_mod.segments = foliage_bevel_segments 
        bevel_mod.width = 0.02 * scale # Small fixed bevel amount
        
        # Smooth shading
        bpy.ops.object.shade_smooth()

        # Rotate each layer slightly
        foliage_obj.rotation_euler.z = math.radians(foliage_rotation_offset * i)

        # Detailed foliage shaping (like in the video)
        bpy.context.view_layer.objects.active = foliage_obj
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(foliage_obj.data)
        
        # Select bottom face
        bottom_z_foliage = current_z - current_foliage_height / 2
        bottom_face_verts = [v for v in bm.verts if abs(v.co.z - bottom_z_foliage) < 0.001]
        
        selected_bottom_face = None
        for face in bm.faces:
            if all(v in bottom_face_verts for v in face.verts):
                face.select = True
                selected_bottom_face = face
                break
        
        if selected_bottom_face:
            bmesh.update_edit_mesh(foliage_obj.data)
            
            # E then S - Extrude and Scale Inwards
            bpy.ops.mesh.extrude_faces_move(MESH_OT_extrude_faces_indiv={"mirror":False})
            bpy.ops.transform.resize(value=(foliage_extrude_scale_factor, foliage_extrude_scale_factor, foliage_extrude_scale_factor), constraint_axis=(True, True, False))
            
            # Alt E - Extrude along normals (using a small negative value to extrude inwards)
            bpy.ops.mesh.extrude_region_shrink_fatten(MESH_OT_extrude_region={"use_normals_face":True}, TRANSFORM_OT_shrink_fatten={"value": -foliage_extrude_depth_factor * current_foliage_height}) 
            
            # S - Scale inwards again for the final 'point'
            bpy.ops.transform.resize(value=(foliage_extrude_scale_factor * 0.8, foliage_extrude_scale_factor * 0.8, foliage_extrude_scale_factor * 0.8), constraint_axis=(True, True, False)) # Smaller scale for sharper point
            
            # Deselect all mesh elements
            for v in bm.verts: v.select = False
            for e in bm.edges: e.select = False
            for f in bm.faces: f.select = False
            bmesh.update_edit_mesh(foliage_obj.data)

        bpy.ops.object.mode_set(mode='OBJECT')
        created_objects.append(foliage_obj)
        foliage_objs.append(foliage_obj)

        # Update for next layer
        current_z += current_foliage_height * foliage_vertical_offset # Move up for next layer
        current_foliage_radius *= foliage_scale_factor # Scale down radius for next layer
        current_foliage_height *= foliage_scale_factor # Scale down height for next layer


    # --- Parent foliage to trunk ---
    # Ensure trunk_obj is the active object before parenting
    bpy.context.view_layer.objects.active = trunk_obj
    for f_obj in foliage_objs:
        f_obj.select_set(True) # Select foliage object
    
    # Parent selected foliage objects to the active trunk object
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

    # Link all created objects to the new collection and unlink from scene collection
    for obj in created_objects:
        if obj.name not in tree_collection.objects:
            tree_collection.objects.link(obj)
        if obj.name in scene.collection.objects:
            scene.collection.objects.unlink(obj) # Unlink from primary scene collection

    return f"Created '{object_name}' at {location} with {len(created_objects)} objects"
