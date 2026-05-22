def create_object(
    scene_name: str = "Scene",
    object_name: str = "SciFiDoor",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.25, 0.3),
    **kwargs,
) -> str:
    """
    Create a mechanical Sci-Fi Door rigged with an Action constraint controller.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Door Geometry ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()

    # Upper Panel
    bmesh.ops.create_cube(bm, size=1.0)
    bm.verts.ensure_lookup_table()
    top_verts = bm.verts[:]
    for v in top_verts:
        v.co.x *= 2.0
        v.co.y *= 0.2
        v.co.z *= 1.9
        v.co.z += 1.05 # Shift upwards, leaving a small gap at origin

    # Lower Panel
    bmesh.ops.create_cube(bm, size=1.0)
    bm.verts.ensure_lookup_table()
    bot_verts = [v for v in bm.verts if v not in top_verts]
    for v in bot_verts:
        v.co.x *= 2.0
        v.co.y *= 0.2
        v.co.z *= 1.9
        v.co.z -= 1.05 # Shift downwards

    bm.to_mesh(mesh)
    bm.free()

    # Add Bevel for Sci-Fi panel lines
    bev = obj.modifiers.new(type='BEVEL', name="Bevel")
    bev.width = 0.05
    bev.segments = 3

    # === Step 2: Assign Materials ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Metallic"].default_value = 0.8
        bsdf.inputs["Roughness"].default_value = 0.3
    obj.data.materials.append(mat)

    # === Step 3: Weight Painting (Vertex Groups) ===
    vg_top = obj.vertex_groups.new(name="Upper")
    vg_bot = obj.vertex_groups.new(name="Lower")

    for v in mesh.vertices:
        if v.co.z > 0:
            vg_top.add([v.index], 1.0, 'REPLACE')
        else:
            vg_bot.add([v.index], 1.0, 'REPLACE')

    # === Step 4: Create Armature ===
    arm_data = bpy.data.armatures.new(f"{object_name}_Armature")
    arm_obj = bpy.data.objects.new(f"{object_name}_Rig", arm_data)
    scene.collection.objects.link(arm_obj)

    # Parent Mesh to Armature
    obj.parent = arm_obj
    mod = obj.modifiers.new(type='ARMATURE', name="Armature")
    mod.object = arm_obj

    # Create Pose Bones at hinge points
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='EDIT')

    bone_top = arm_data.edit_bones.new("Upper")
    bone_top.head = (0, 0, 2)
    bone_top.tail = (0, 0, 0)
    bone_top.roll = 0

    bone_bot = arm_data.edit_bones.new("Lower")
    bone_bot.head = (0, 0, -2)
    bone_bot.tail = (0, 0, 0)
    bone_bot.roll = 0

    bpy.ops.object.mode_set(mode='OBJECT')

    # === Step 5: Create Controller Empty ===
    empty = bpy.data.objects.new(f"{object_name}_Control", None)
    empty.empty_display_type = 'ARROWS'
    empty.empty_display_size = 0.8
    scene.collection.objects.link(empty)

    # Parent empty to rig so it moves with the asset
    empty.parent = arm_obj
    empty.location = (2.5, 0, 0) 

    # === Step 6: Create Action Constraints ===
    
    # Action for Top Bone (+90 deg pitch around X to swing outward)
    action_top = bpy.data.actions.new(name=f"{object_name}_TopAction")
    fc_top = action_top.fcurves.new(data_path="rotation_euler", index=0)
    fc_top.keyframe_points.insert(1, 0.0)
    fc_top.keyframe_points.insert(100, 1.5708) # 90 degrees in radians
    action_top.use_fake_user = True

    # Action for Bottom Bone (-90 deg pitch around X to swing outward)
    action_bot = bpy.data.actions.new(name=f"{object_name}_BotAction")
    fc_bot = action_bot.fcurves.new(data_path="rotation_euler", index=0)
    fc_bot.keyframe_points.insert(1, 0.0)
    fc_bot.keyframe_points.insert(100, -1.5708) # -90 degrees in radians
    action_bot.use_fake_user = True

    # Assign Constraint to Top Bone
    pose_top = arm_obj.pose.bones["Upper"]
    pose_top.rotation_mode = 'XYZ'
    con_top = pose_top.constraints.new('ACTION')
    con_top.target = empty
    con_top.transform_channel = 'LOCATION_Z'
    con_top.target_space = 'LOCAL'
    con_top.action = action_top
    con_top.frame_start = 1
    con_top.frame_end = 100
    con_top.min = 0.0
    con_top.max = 2.0

    # Assign Constraint to Bottom Bone
    pose_bot = arm_obj.pose.bones["Lower"]
    pose_bot.rotation_mode = 'XYZ'
    con_bot = pose_bot.constraints.new('ACTION')
    con_bot.target = empty
    con_bot.transform_channel = 'LOCATION_Z'
    con_bot.target_space = 'LOCAL'
    con_bot.action = action_bot
    con_bot.frame_start = 1
    con_bot.frame_end = 100
    con_bot.min = 0.0
    con_bot.max = 2.0

    # === Step 7: Finalize Transforms ===
    arm_obj.location = Vector(location)
    arm_obj.scale = (scale, scale, scale)

    # Highlight the controller for the user
    bpy.ops.object.select_all(action='DESELECT')
    empty.select_set(True)
    bpy.context.view_layer.objects.active = empty

    return f"Created rigged mechanical door '{object_name}' at {location}. Move the selected Empty on its Local Z axis to open/close."
