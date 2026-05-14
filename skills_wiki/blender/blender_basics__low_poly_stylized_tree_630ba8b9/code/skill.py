def create_blender_basics_tree(
    scene_name: str = "Scene",
    object_name: str = "LowPolyTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    trunk_color: tuple = (0.4, 0.2, 0.05, 1.0),  # RGBA
    foliage_color: tuple = (0.1, 0.5, 0.1, 1.0), # RGBA
    trunk_vertices: int = 8,
    foliage_vertices: int = 12,
    foliage_layers: int = 4,
    auto_smooth_angle: float = 0.523599, # Approx 30 degrees in radians
    **kwargs,
) -> str:
    """
    Create a low-polygon stylized tree using basic Blender modeling operations.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created tree object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the entire tree.
        trunk_color: (R, G, B, A) base color for the trunk.
        foliage_color: (R, G, B, A) base color for the foliage.
        trunk_vertices: Number of vertices for the trunk cylinder.
        foliage_vertices: Number of vertices for the foliage circles.
        foliage_layers: Number of stacked foliage layers.
        auto_smooth_angle: Angle threshold (in radians) for auto smooth shading.
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
    trunk_mat = bpy.data.materials.new(name=f"{object_name}_TrunkMat")
    trunk_mat.use_nodes = True
    principled_bsdf_trunk = trunk_mat.node_tree.nodes["Principled BSDF"]
    principled_bsdf_trunk.inputs['Base Color'].default_value = trunk_color

    foliage_mat = bpy.data.materials.new(name=f"{object_name}_FoliageMat")
    foliage_mat.use_nodes = True
    principled_bsdf_foliage = foliage_mat.node_tree.nodes["Principled BSDF"]
    principled_bsdf_foliage.inputs['Base Color'].default_value = foliage_color

    # --- Create Trunk ---
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=trunk_vertices,
        radius=0.5 * scale,
        depth=2.0 * scale,
        location=location,
        rotation=(0, 0, 0)
    )
    trunk_obj = bpy.context.active_object
    trunk_obj.name = f"{object_name}_Trunk"
    trunk_obj.data.materials.append(trunk_mat)

    # Enter Edit Mode for trunk manipulation
    bpy.context.view_layer.objects.active = trunk_obj
    bpy.ops.object.editmode_toggle()

    # Select top face
    bpy.ops.mesh.select_mode(type='FACE')
    bm = bmesh.from_edit_mesh(trunk_obj.data)
    top_face = None
    for face in bm.faces:
        if all(v.co.z > trunk_obj.location.z + (1.0 * scale) - 0.1 for v in face.verts): # Check if it's the highest face
            face.select = True
            top_face = face
            break
    
    if top_face:
        # Extrude top face upwards (along Z axis relative to object)
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value": (0, 0, 1.5 * scale)}
        )
        # Scale the new top face
        bpy.ops.transform.resize(value=(0.3, 0.3, 0.3)) # Scale down to taper

    # Exit Edit Mode
    bpy.ops.object.editmode_toggle()

    # Apply smooth shading to trunk
    bpy.ops.object.shade_smooth()
    trunk_obj.data.use_auto_smooth = True
    trunk_obj.data.auto_smooth_angle = auto_smooth_angle

    # --- Create Foliage Layers ---
    foliage_objects = []
    base_foliage_z = trunk_obj.location.z + (1.5 * scale) # Starting height for first foliage layer
    layer_height = 0.5 * scale # Height of each cone segment
    layer_scale_factor = 0.9 # Each layer is slightly smaller

    for i in range(foliage_layers):
        current_z = base_foliage_z + (i * (layer_height * 0.7)) # Slightly overlapping
        current_scale = scale * (layer_scale_factor ** i)

        bpy.ops.mesh.primitive_circle_add(
            vertices=foliage_vertices,
            radius=1.0 * current_scale,
            location=(location[0], location[1], current_z),
            rotation=(math.pi / 2, 0, 0) # Rotate to stand upright
        )
        foliage_obj = bpy.context.active_object
        foliage_obj.name = f"{object_name}_Foliage_{i+1}"
        foliage_obj.data.materials.append(foliage_mat)

        # Enter Edit Mode for foliage layer manipulation
        bpy.context.view_layer.objects.active = foliage_obj
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Extrude first segment up and scale out
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value": (0, 0, layer_height)}
        )
        bpy.ops.transform.resize(value=(1.5, 1.5, 1.0)) # Scale outwards

        # Extrude second segment up and scale in (to form cone top)
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value": (0, 0, layer_height)}
        )
        bpy.ops.transform.resize(value=(0.1, 0.1, 1.0)) # Scale inwards to a point

        # Exit Edit Mode
        bpy.ops.object.editmode_toggle()

        # Apply smooth shading
        bpy.ops.object.shade_smooth()
        foliage_obj.data.use_auto_smooth = True
        foliage_obj.data.auto_smooth_angle = auto_smooth_angle

        # Randomize rotation for variety
        foliage_obj.rotation_euler.z += math.radians(i * 45 + (kwargs.get('random_seed', 0) * 10)) # Simple rotation based on layer index

        foliage_objects.append(foliage_obj)

    # --- Parenting and Final Positioning ---
    # Parent foliage layers to the trunk
    bpy.context.view_layer.objects.active = trunk_obj
    for obj in foliage_objects:
        obj.select_set(True)
    trunk_obj.select_set(True)
    bpy.ops.object.parent_set(type='OBJECT')

    # Apply overall transform
    # The initial primitive adds already set location.
    # The scale on primitives might override, better to adjust the created trunk/foliage.
    # However, for simplicity and matching video interaction, individual component scale is already done.

    return f"Created '{object_name}' at {location} with {1 + len(foliage_objects)} objects"

