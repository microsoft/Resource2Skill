def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    trunk_color: tuple = (0.3, 0.15, 0.05, 1.0), # RGBA brown
    leaf_color: tuple = (0.1, 0.4, 0.1, 1.0), # RGBA green
    num_layers: int = 4, # Number of leafy sections
    trunk_height_ratio: float = 0.3, # Proportion of total tree height dedicated to the trunk
    layer_spacing: float = 0.15, # Spacing between leaf layers
    base_cone_radius: float = 0.8, # Radius of the bottommost cone
    top_cone_radius_factor: float = 0.4, # Factor for the topmost cone's radius relative to base_cone_radius
    cone_height_factor: float = 0.8, # Factor for cone height relative to its radius
    pine_needle_extrusion: float = 0.05, # How much to extrude down for "pine needles"
    pine_needle_scale_factor: float = 0.8, # How much to scale extruded "pine needles"
) -> str:
    """
    Create a stylized low-poly tree in the active Blender scene using iterative primitive transformations,
    demonstrating fundamental modeling operations like extrude, scale, and move.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the main parent empty of the tree.
        location: (x, y, z) world-space position.
        scale: Uniform overall scale factor (1.0 = default size).
        trunk_color: (R, G, B, A) base color for the trunk in 0-1 range.
        leaf_color: (R, G, B, A) base color for the leaves in 0-1 range.
        num_layers: Number of leafy sections of the tree.
        trunk_height_ratio: Ratio of trunk height to overall tree height (0 to 1).
        layer_spacing: Vertical spacing between leaf layers.
        base_cone_radius: Radius of the bottommost cone layer.
        top_cone_radius_factor: Factor for the topmost cone's radius relative to base_cone_radius (0 to 1).
        cone_height_factor: Factor controlling the height of each cone relative to its base radius.
        pine_needle_extrusion: Distance to extrude for the "pine needle" effect.
        pine_needle_scale_factor: Scale factor for the extruded "pine needle" region.

    Returns:
        Status string, e.g., "Created 'StylizedTree' at (0, 0, 0) with 5 objects."
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    # Get the active scene
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # --- Create Materials ---
    trunk_mat = bpy.data.materials.new(name=f"{object_name}_TrunkMat")
    trunk_mat.use_nodes = True
    bsdf = trunk_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = trunk_color
    bsdf.inputs["Roughness"].default_value = 0.8

    leaf_mat = bpy.data.materials.new(name=f"{object_name}_LeafMat")
    leaf_mat.use_nodes = True
    bsdf = leaf_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = leaf_color
    bsdf.inputs["Roughness"].default_value = 0.8

    # Create a parent empty to hold all tree parts and apply overall scale/location
    parent_empty = bpy.data.objects.new(object_name, None)
    scene.collection.objects.link(parent_empty)
    parent_empty.location = Vector(location)
    parent_empty.scale = (scale, scale, scale)

    # --- Create Trunk ---
    # Calculate overall tree height (approx)
    total_cone_height = sum([
        (base_cone_radius - (base_cone_radius - base_cone_radius * top_cone_radius_factor) * (i / (num_layers - 1))) * cone_height_factor
        for i in range(num_layers)
    ]) + (num_layers - 1) * layer_spacing
    
    trunk_base_radius = base_cone_radius * 0.25
    trunk_height_actual = total_cone_height * trunk_height_ratio

    bpy.ops.mesh.primitive_cylinder_add(
        vertices=12, radius=trunk_base_radius, depth=trunk_height_actual,
        location=(0, 0, trunk_height_actual / 2.0) # Position to sit on the ground at z=0
    )
    trunk_obj = bpy.context.active_object
    trunk_obj.name = f"{object_name}_Trunk"
    trunk_obj.data.materials.append(trunk_mat)
    trunk_obj.parent = parent_empty

    # Shape the trunk (slight taper) in Edit Mode
    bpy.context.view_layer.objects.active = trunk_obj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(trunk_obj.data)

    # Scale bottom face
    if len(bm.faces) > 0:
        bottom_face = min(bm.faces, key=lambda f: f.calc_center_median().z)
        bottom_face.select = True
        bmesh.update_edit_mesh(trunk_obj.data)
        bpy.ops.transform.resize(value=(1.2, 1.2, 1.0), orient_type='GLOBAL', orient_matrix_type='GLOBAL', constraint_axis=(True, True, False))
        bottom_face.select = False

    # Scale top face
    if len(bm.faces) > 0:
        top_face = max(bm.faces, key=lambda f: f.calc_center_median().z)
        top_face.select = True
        bmesh.update_edit_mesh(trunk_obj.data)
        bpy.ops.transform.resize(value=(0.8, 0.8, 1.0), orient_type='GLOBAL', orient_matrix_type='GLOBAL', constraint_axis=(True, True, False))
        top_face.select = False

    bpy.ops.object.mode_set(mode='OBJECT')

    # --- Create Leaf Layers ---
    leaf_count = 0
    current_z_offset = trunk_height_actual # Start placing cones on top of the trunk

    for i in range(num_layers):
        leaf_count += 1
        # Calculate radius for current layer, tapering from base_cone_radius to top_cone_radius_factor
        layer_radius = base_cone_radius - (base_cone_radius - base_cone_radius * top_cone_radius_factor) * (i / (num_layers - 1))
        cone_height_layer = layer_radius * cone_height_factor

        # Create a cone
        bpy.ops.mesh.primitive_cone_add(
            vertices=16, radius1=layer_radius, radius2=0.0, depth=cone_height_layer,
            location=(0, 0, current_z_offset + (cone_height_layer / 2.0))
        )
        cone_obj = bpy.context.active_object
        cone_obj.name = f"{object_name}_LeafLayer_{i+1}"
        cone_obj.data.materials.append(leaf_mat)
        cone_obj.parent = parent_empty
        
        # Apply "Pine Needle" effect - Extrude and scale bottom face inwards
        bpy.context.view_layer.objects.active = cone_obj
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(cone_obj.data)

        # Select the bottom face (smallest Z coordinate)
        if len(bm.faces) > 0:
            bottom_face = min(bm.faces, key=lambda f: f.calc_center_median().z)
            bottom_face.select = True
            bmesh.update_edit_mesh(cone_obj.data)
            
            # Extrude the face (E)
            bpy.ops.mesh.extrude_region_faces(RELEASE_CONFIRM=True)
            bpy.ops.transform.translate(value=(0, 0, -pine_needle_extrusion), orient_type='LOCAL') # Move slightly down along local Z

            # Scale the newly extruded face (S)
            bpy.ops.transform.resize(value=(pine_needle_scale_factor, pine_needle_scale_factor, 1.0), orient_type='LOCAL')
            
            bottom_face.select = False

        bpy.ops.object.mode_set(mode='OBJECT')

        current_z_offset += cone_height_layer + layer_spacing

    return f"Created '{object_name}' at {location} with {1 + leaf_count} objects."

