def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedPineTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    trunk_color: tuple = (0.25, 0.15, 0.05, 1.0),
    foliage_color: tuple = (0.1, 0.4, 0.1, 1.0),
    num_foliage_layers: int = 5,
    layer_gap_factor: float = 0.5,  # Relative to foliage_height
    layer_taper_factor: float = 0.6,  # Top scale relative to base scale
    layer_rotation_step: float = 20.0, # Degrees
    trunk_subdivision_verts: int = 8,
    foliage_subdivision_verts: int = 12,
    trunk_height_factor: float = 3.0,
    trunk_base_radius_factor: float = 0.3,
    foliage_layer_height_factor: float = 0.7,
    foliage_base_radius_factor: float = 1.0,
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Pine Tree in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created tree (empty parent).
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the entire tree.
        trunk_color: (R, G, B, A) base color for the trunk material.
        foliage_color: (R, G, B, A) base color for the foliage material.
        num_foliage_layers: Number of foliage layers for the tree canopy.
        layer_gap_factor: Multiplier for the gap between foliage layers.
        layer_taper_factor: Scale factor for the top of each foliage layer.
        layer_rotation_step: Rotation in degrees applied to each subsequent foliage layer.
        trunk_subdivision_verts: Number of vertices for the trunk cylinder.
        foliage_subdivision_verts: Number of vertices for the foliage circles.
        trunk_height_factor: Relative height of the trunk.
        trunk_base_radius_factor: Relative base radius of the trunk.
        foliage_layer_height_factor: Relative height of each foliage layer.
        foliage_base_radius_factor: Relative base radius of the first foliage layer.
        **kwargs: Additional overrides (not used in this version).

    Returns:
        Status string, e.g., "Created 'StylizedPineTree' at (0, 0, 0) with 1 trunk and 5 foliage layers."
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Deselect all objects before starting
    bpy.ops.object.select_all(action='DESELECT')

    # Create parent empty for the whole tree
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=location)
    tree_parent = bpy.context.active_object
    tree_parent.name = object_name
    tree_parent.scale = (scale, scale, scale)

    # --- Materials ---
    trunk_mat = bpy.data.materials.new(name=f"{object_name}_TrunkMat")
    trunk_mat.use_nodes = True
    bsdf = trunk_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = trunk_color
    trunk_mat.node_tree.nodes["Material Output"].is_active_render = True

    foliage_mat = bpy.data.materials.new(name=f"{object_name}_FoliageMat")
    foliage_mat.use_nodes = True
    bsdf = foliage_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = foliage_color
    foliage_mat.node_tree.nodes["Material Output"].is_active_render = True

    # --- Trunk ---
    # Add cylinder for the trunk
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=trunk_subdivision_verts,
        radius=trunk_base_radius_factor,
        depth=trunk_height_factor,
        location=(0, 0, trunk_height_factor / 2),
        enter_editmode=True,
    )
    trunk_obj = bpy.context.active_object
    trunk_obj.name = f"{object_name}_Trunk"

    # Taper the trunk slightly (scale top face)
    bm = bmesh.from_edit_mesh(trunk_obj.data)
    top_face = None
    for face in bm.faces:
        if face.normal.z > 0.9: # Identify top face
            top_face = face
            break
    if top_face:
        top_face.select = True
        bmesh.update_edit_mesh(trunk_obj.data)
        bpy.ops.transform.resize(value=(layer_taper_factor, layer_taper_factor, 1)) # Scale top face
        bpy.ops.mesh.select_all(action='DESELECT')
        top_face.select = False # Deselect for later operations

    bmesh.update_edit_mesh(trunk_obj.data)
    bmesh.free(bm)
    bpy.ops.object.editmode_toggle() # Exit edit mode

    # Apply trunk material and shading
    trunk_obj.data.materials.append(trunk_mat)
    bpy.ops.object.select_all(action='DESELECT')
    trunk_obj.select_set(True)
    bpy.context.view_layer.objects.active = trunk_obj
    bpy.ops.object.shade_smooth()
    trunk_obj.data.use_auto_smooth = True
    trunk_obj.data.auto_smooth_angle = math.radians(30)
    trunk_obj.parent = tree_parent
    trunk_obj.location = (0,0,0) # Relative to parent

    # --- Foliage Layers ---
    foliage_layers = []
    current_z_offset = trunk_height_factor / 2 # Starting point for first layer
    current_scale = foliage_base_radius_factor

    for i in range(num_foliage_layers):
        # Add circle for a foliage layer
        bpy.ops.mesh.primitive_circle_add(
            vertices=foliage_subdivision_verts,
            radius=current_scale,
            fill_type='NGON', # Explicitly fill the circle
            location=(0, 0, current_z_offset),
            enter_editmode=True,
        )
        foliage_obj = bpy.context.active_object
        foliage_obj.name = f"{object_name}_FoliageLayer_{i+1}"
        foliage_layers.append(foliage_obj)

        # Extrude and scale to form a frustum
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.extrude_region_move(
            MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False},
            TRANSFORM_OT_translate={"value":(0,0,foliage_layer_height_factor)}
        )
        bpy.ops.transform.resize(value=(layer_taper_factor, layer_taper_factor, 1)) # Scale top face

        bpy.ops.object.editmode_toggle() # Exit edit mode

        # Apply foliage material and shading
        foliage_obj.data.materials.append(foliage_mat)
        bpy.ops.object.select_all(action='DESELECT')
        foliage_obj.select_set(True)
        bpy.context.view_layer.objects.active = foliage_obj
        bpy.ops.object.shade_smooth()
        foliage_obj.data.use_auto_smooth = True
        foliage_obj.data.auto_smooth_angle = math.radians(30)
        foliage_obj.parent = tree_parent
        foliage_obj.location = (0, 0, current_z_offset) # Relative to parent
        foliage_obj.rotation_euler.z = math.radians(i * layer_rotation_step)


        # Update for next layer
        current_z_offset += foliage_layer_height_factor + (foliage_layer_height_factor * layer_gap_factor)
        current_scale *= layer_taper_factor * 0.9 # Reduce scale for higher layers

    # Position the whole tree
    tree_parent.location = Vector(location)
    tree_parent.scale = (scale, scale, scale)

    return f"Created '{object_name}' at {location} with 1 trunk and {num_foliage_layers} foliage layers."

