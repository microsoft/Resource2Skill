def create_stylized_layered_pine_tree(
    scene_name: str = "Scene",
    object_name: str = "StylizedPineTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    trunk_color: tuple = (0.25, 0.15, 0.05, 1.0),  # Brown
    foliage_color: tuple = (0.1, 0.4, 0.1, 1.0),  # Green
    num_foliage_layers: int = 4,
    layer_height_spacing: float = 0.8,
    layer_scale_factor: float = 0.7,
    layer_rotation_step: float = 20.0, # Degrees
    trunk_segments: int = 16,
    foliage_segments: int = 24,
    **kwargs,
) -> str:
    """
    Create a stylized layered pine tree in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created tree object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the entire tree.
        trunk_color: (R, G, B, A) base color for the trunk.
        foliage_color: (R, G, B, A) base color for the foliage.
        num_foliage_layers: Number of foliage layers.
        layer_height_spacing: Vertical distance between foliage layers.
        layer_scale_factor: Scale multiplier for each subsequent foliage layer.
        layer_rotation_step: Z-axis rotation step in degrees for each layer.
        trunk_segments: Number of vertices for the trunk cylinder.
        foliage_segments: Number of vertices for the foliage cylinders.
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'StylizedPineTree' at (0, 0, 0) with 5 objects"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Materials ---
    trunk_mat = bpy.data.materials.new(name=f"{object_name}_TrunkMat")
    trunk_mat.use_nodes = True
    bsdf = trunk_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = trunk_color
    bsdf.inputs["Roughness"].default_value = 0.8

    foliage_mat = bpy.data.materials.new(name=f"{object_name}_FoliageMat")
    foliage_mat.use_nodes = True
    bsdf = foliage_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = foliage_color
    bsdf.inputs["Roughness"].default_value = 0.7

    # --- Trunk ---
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=trunk_segments, radius=0.15 * scale, depth=1.5 * scale,
        location=(0, 0, 0.75 * scale), enter_editmode=False, align="WORLD"
    )
    trunk_obj = bpy.context.active_object
    trunk_obj.name = f"{object_name}_Trunk"
    if trunk_obj.data.materials:
        trunk_obj.data.materials[0] = trunk_mat
    else:
        trunk_obj.data.materials.append(trunk_mat)

    # Flare the trunk base (using bmesh for direct mesh manipulation)
    bpy.context.view_layer.objects.active = trunk_obj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(trunk_obj.data)
    
    # Select bottom face (assuming it's the 0th face of a cylinder if created at 0,0,0)
    # This might require more robust selection logic if geometry changes
    bottom_face = None
    for face in bm.faces:
        # Check if face's normal is pointing mostly down (negative Z)
        # and if its average Z coordinate is at the bottom of the object
        avg_z = sum([v.co.z for v in face.verts]) / len(face.verts)
        if face.normal.z < -0.9 and abs(avg_z - (-0.75 * scale)) < 0.01: # Check for default cylinder position
            bottom_face = face
            break
            
    if bottom_face:
        bottom_face.select = True
        bmesh.update_edit_mesh(trunk_obj.data)
        bpy.ops.transform.resize(value=(1.5, 1.5, 1), orient_type='LOCAL', constraint_axis=(True, True, False))
    else:
        print("Warning: Could not find bottom face for flaring trunk.")

    bpy.ops.object.mode_set(mode='OBJECT')

    # --- Foliage Layers ---
    foliage_objects = []
    base_foliage_radius = 0.6 * scale
    base_foliage_height = 0.8 * scale
    
    for i in range(num_foliage_layers):
        current_radius = base_foliage_radius * (layer_scale_factor ** i)
        current_height = base_foliage_height * (layer_scale_factor ** i)
        
        # Position slightly above the previous layer, adjust for smaller top layers
        layer_z_pos = (0.75 * scale) + (i * layer_height_spacing * scale) + (current_height / 2)

        bpy.ops.mesh.primitive_cylinder_add(
            vertices=foliage_segments, radius=current_radius, depth=current_height,
            location=(0, 0, layer_z_pos), enter_editmode=False, align="WORLD"
        )
        foliage_obj = bpy.context.active_object
        foliage_obj.name = f"{object_name}_Foliage_{i+1}"
        if foliage_obj.data.materials:
            foliage_obj.data.materials[0] = foliage_mat
        else:
            foliage_obj.data.materials.append(foliage_mat)
        
        foliage_objects.append(foliage_obj)

        bpy.context.view_layer.objects.active = foliage_obj
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(foliage_obj.data)

        # Scale top face to make it conical
        top_face = None
        for face in bm.faces:
            avg_z = sum([v.co.z for v in face.verts]) / len(face.verts)
            if face.normal.z > 0.9 and abs(avg_z - (layer_z_pos + current_height/2)) < 0.01:
                top_face = face
                break
        
        if top_face:
            top_face.select = True
            bmesh.update_edit_mesh(foliage_obj.data)
            bpy.ops.transform.resize(value=(0.2, 0.2, 1), orient_type='LOCAL', constraint_axis=(True, True, False)) # Make it conical
        else:
            print(f"Warning: Could not find top face for foliage layer {i+1}.")

        # Extrude and scale inward for concave effect at bottom of foliage (as shown in tutorial)
        bottom_face = None
        for face in bm.faces:
            avg_z = sum([v.co.z for v in face.verts]) / len(face.verts)
            if face.normal.z < -0.9 and abs(avg_z - (layer_z_pos - current_height/2)) < 0.01:
                bottom_face = face
                break
        
        if bottom_face:
            bottom_face.select = True
            bmesh.update_edit_mesh(foliage_obj.data)
            bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -0.05*scale), "orient_type":'LOCAL', "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True)})
            bpy.ops.transform.resize(value=(0.8, 0.8, 1), orient_type='LOCAL', constraint_axis=(True, True, False))
        else:
            print(f"Warning: Could not find bottom face for foliage layer {i+1} for indentation.")


        bpy.ops.object.mode_set(mode='OBJECT')

        # Rotate foliage layer
        foliage_obj.rotation_euler.z = math.radians(i * layer_rotation_step)

    # --- Parenting ---
    # Select all foliage objects and then the trunk
    for obj in foliage_objects:
        obj.select_set(True)
    trunk_obj.select_set(True)
    bpy.context.view_layer.objects.active = trunk_obj
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

    # Move the entire tree to the specified location
    trunk_obj.location = Vector(location)

    return f"Created '{object_name}' at {location} with {1 + len(foliage_objects)} objects"

