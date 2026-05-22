def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    trunk_color: tuple = (0.25, 0.15, 0.05, 1.0), # RGBA
    foliage_color: tuple = (0.1, 0.4, 0.1, 1.0), # RGBA
    trunk_height_scale: float = 2.0,
    trunk_radius_scale: float = 0.5,
    trunk_vertices: int = 8,
    foliage_layers: int = 4,
    foliage_segments: int = 12,
    foliage_base_radius: float = 1.0,
    foliage_top_scale_factor: float = 0.1,
    foliage_vertical_spacing: float = 0.7,
    foliage_horizontal_scale_increment: float = 0.3,
    foliage_rotation_increment: float = 30.0, # degrees
    **kwargs,
) -> str:
    """
    Create a Low-Poly Layered Tree in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created tree object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the entire tree.
        trunk_color: (R, G, B, A) base color for the trunk in 0-1 range.
        foliage_color: (R, G, B, A) base color for the foliage in 0-1 range.
        trunk_height_scale: Factor to scale default cylinder height.
        trunk_radius_scale: Factor to scale default cylinder radius.
        trunk_vertices: Number of vertices for the trunk cylinder.
        foliage_layers: Number of foliage layers (cones).
        foliage_segments: Number of vertices for each foliage circle.
        foliage_base_radius: Base radius for the lowest foliage layer.
        foliage_top_scale_factor: Scale factor for the top of each extruded foliage cone.
        foliage_vertical_spacing: Z-distance between foliage layers.
        foliage_horizontal_scale_increment: How much each subsequent foliage layer scales horizontally.
        foliage_rotation_increment: Degrees to rotate each subsequent foliage layer around Z.
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'LowPolyTree' at (0, 0, 0) with 5 objects"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Materials ---
    trunk_mat = bpy.data.materials.new(name=f"{object_name}_Trunk_Mat")
    trunk_mat.use_nodes = True
    bsdf_trunk = trunk_mat.node_tree.nodes["Principled BSDF"]
    bsdf_trunk.inputs["Base Color"].default_value = trunk_color

    foliage_mat = bpy.data.materials.new(name=f"{object_name}_Foliage_Mat")
    foliage_mat.use_nodes = True
    bsdf_foliage = foliage_mat.node_tree.nodes["Principled BSDF"]
    bsdf_foliage.inputs["Base Color"].default_value = foliage_color

    # --- Trunk ---
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=trunk_vertices,
        radius=trunk_radius_scale,
        depth=trunk_height_scale,
        location=location
    )
    trunk_obj = bpy.context.active_object
    trunk_obj.name = f"{object_name}_Trunk"
    trunk_obj.data.materials.append(trunk_mat)
    bpy.ops.object.shade_smooth()
    trunk_obj.data.use_auto_smooth = True

    # --- Foliage Layers ---
    foliage_objects = []
    
    # Create the base cone shape once
    bpy.ops.mesh.primitive_circle_add(
        vertices=foliage_segments,
        radius=foliage_base_radius,
        location=(0, 0, location[2]) # Start at the base of the trunk for convenience
    )
    base_cone_obj = bpy.context.active_object
    base_cone_obj.name = f"{object_name}_BaseConeShape"
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.extrude_region_move(
        MESH_OT_extrude_region={"type":'NORMAL'},
        TRANSFORM_OT_translate={"value":(0, 0, foliage_vertical_spacing * foliage_top_scale_factor)}
    )
    bpy.ops.transform.resize(value=(foliage_top_scale_factor, foliage_top_scale_factor, foliage_top_scale_factor))
    bpy.ops.object.mode_set(mode='OBJECT')

    # Apply shading and material to the base cone before duplicating
    bpy.ops.object.select_all(action='DESELECT')
    base_cone_obj.select_set(True)
    bpy.context.view_layer.objects.active = base_cone_obj
    bpy.ops.object.shade_smooth()
    base_cone_obj.data.use_auto_smooth = True
    base_cone_obj.data.materials.append(foliage_mat)

    # Duplicate and transform layers
    for i in range(foliage_layers):
        if i == 0:
            # First layer is the base cone itself, positioned relative to trunk
            current_foliage_obj = base_cone_obj
            current_foliage_obj.location = Vector(location) + Vector((0, 0, trunk_height_scale * scale * 0.25 - (foliage_vertical_spacing * scale * (foliage_layers - 1 - i)))) # Adjust initial placement
        else:
            bpy.ops.object.select_all(action='DESELECT')
            base_cone_obj.select_set(True)
            bpy.context.view_layer.objects.active = base_cone_obj
            
            bpy.ops.object.duplicate_move(
                TRANSFORM_OT_translate={"value":(0, 0, 0)} # Duplicate at same location
            )
            current_foliage_obj = bpy.context.active_object
            current_foliage_obj.name = f"{object_name}_Foliage_{i}"
            current_foliage_obj.data.materials.append(foliage_mat) # Ensure material is on new obj too
            bpy.ops.object.shade_smooth()
            current_foliage_obj.data.use_auto_smooth = True
        
        # Calculate position, scale, and rotation for current layer
        layer_z_offset = (foliage_vertical_spacing * i)
        layer_scale_factor = scale * (foliage_base_radius + foliage_horizontal_scale_increment * (foliage_layers - 1 - i)) / foliage_base_radius
        layer_rotation_z = math.radians(foliage_rotation_increment * i)
        
        current_foliage_obj.location = Vector(location) + Vector((0, 0, trunk_height_scale * scale * 0.25 + (foliage_vertical_spacing * scale * i)))
        current_foliage_obj.scale = (layer_scale_factor, layer_scale_factor, layer_scale_factor)
        current_foliage_obj.rotation_euler.z = layer_rotation_z
        
        foliage_objects.append(current_foliage_obj)

    # Clean up the original base cone if it wasn't used as the first layer
    # If the first layer was the base_cone_obj itself, it's already in foliage_objects
    if base_cone_obj not in foliage_objects:
        bpy.data.objects.remove(base_cone_obj, do_unlink=True)


    # Parent foliage to trunk
    bpy.ops.object.select_all(action='DESELECT')
    trunk_obj.select_set(True)
    bpy.context.view_layer.objects.active = trunk_obj
    
    for fo in foliage_objects:
        fo.parent = trunk_obj
        # Keep transform: parent_obj.matrix_world.inverted()
        fo.matrix_parent_inverse = trunk_obj.matrix_world.inverted()
        
    # --- Finalize ---
    # Apply overall scale and location
    trunk_obj.location = Vector(location)
    trunk_obj.scale = (scale, scale, scale)

    bpy.ops.object.select_all(action='DESELECT')
    trunk_obj.select_set(True)
    for fo in foliage_objects:
        fo.select_set(True)
    bpy.context.view_layer.objects.active = trunk_obj # Make trunk active for potential further operations

    return f"Created '{object_name}' at {location} with {1 + len(foliage_objects)} objects"

