def create_rigid_body_destruction(
    scene_name: str = "Scene",
    object_name: str = "RBD_Tower",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.5, 0.8),
    **kwargs
) -> str:
    """
    Creates a dynamic Rigid Body simulation featuring a circular tower of blocks
    and a heavy sphere that drops to demolish it in slow motion.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated objects.
        location: (x, y, z) base world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the tower blocks.
        **kwargs: Overrides for 'num_columns' and 'tower_height'.

    Returns:
        Status string.
    """
    import bpy
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Ensure context is targeting our scene for the ops
    bpy.context.window.scene = scene

    # Helper function to reliably add rigid body physics to an object
    def add_rigid_body(obj, rb_type='ACTIVE'):
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        # Instantiate the Rigid Body World if it doesn't exist yet
        if scene.rigidbody_world is None:
            bpy.ops.rigidbody.world_add()
            
        bpy.ops.rigidbody.object_add()
        obj.rigid_body.type = rb_type

    # === Step 1: Create Passive Floor ===
    bpy.ops.mesh.primitive_plane_add(size=50 * scale, location=location)
    floor = bpy.context.active_object
    floor.name = f"{object_name}_Floor"
    add_rigid_body(floor, 'PASSIVE')
    floor.rigid_body.collision_shape = 'MESH'
    
    # === Step 2: Create Materials ===
    mat_cube = bpy.data.materials.new(name=f"{object_name}_CubeMat")
    mat_cube.use_nodes = True
    bsdf_cube = mat_cube.node_tree.nodes.get("Principled BSDF")
    if bsdf_cube:
        bsdf_cube.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf_cube.inputs["Roughness"].default_value = 0.4

    mat_trigger = bpy.data.materials.new(name=f"{object_name}_TriggerMat")
    mat_trigger.use_nodes = True
    bsdf_trigger = mat_trigger.node_tree.nodes.get("Principled BSDF")
    if bsdf_trigger:
        bsdf_trigger.inputs["Base Color"].default_value = (0.9, 0.7, 0.1, 1.0) # Gold
        bsdf_trigger.inputs["Metallic"].default_value = 1.0
        bsdf_trigger.inputs["Roughness"].default_value = 0.2

    mat_floor = bpy.data.materials.new(name=f"{object_name}_FloorMat")
    mat_floor.use_nodes = True
    bsdf_floor = mat_floor.node_tree.nodes.get("Principled BSDF")
    if bsdf_floor:
        bsdf_floor.inputs["Base Color"].default_value = (0.05, 0.05, 0.05, 1.0)
        bsdf_floor.inputs["Roughness"].default_value = 0.8
    floor.data.materials.append(mat_floor)

    # === Step 3: Build Circular Rigid Body Tower ===
    num_columns = kwargs.get("num_columns", 14)
    tower_height = kwargs.get("tower_height", 12)
    cube_size = 0.5 * scale
    radius = 2.0 * scale
    
    tower_objs = []
    
    for col in range(num_columns):
        angle = col * (2 * math.pi / num_columns)
        x = location[0] + math.cos(angle) * radius
        y = location[1] + math.sin(angle) * radius

        for z_idx in range(tower_height):
            # Calculate height ensuring blocks sit perfectly on each other and the floor
            z = location[2] + (cube_size / 2) + z_idx * cube_size
            
            bpy.ops.mesh.primitive_cube_add(size=cube_size, location=(x, y, z))
            cube = bpy.context.active_object
            cube.name = f"{object_name}_Block_{col}_{z_idx}"
            cube.rotation_euler = (0, 0, angle) # Face the center
            
            add_rigid_body(cube, 'ACTIVE')
            cube.rigid_body.mass = 1.0
            
            # CRITICAL: Prevents the tower from collapsing before the impact
            cube.rigid_body.use_deactivation = True
            cube.rigid_body.use_start_deactivated = True
            
            cube.data.materials.append(mat_cube)
            tower_objs.append(cube)

    # === Step 4: Create Trigger Sphere (Wrecking Ball) ===
    # Positioned above the tower to fall directly into the center
    trigger_z = location[2] + tower_height * cube_size + 5.0 * scale
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius * 0.8, location=(location[0], location[1], trigger_z))
    trigger = bpy.context.active_object
    trigger.name = f"{object_name}_TriggerSphere"
    
    add_rigid_body(trigger, 'ACTIVE')
    # High mass ensures it easily smashes through the 1kg blocks
    trigger.rigid_body.mass = 25.0  
    trigger.rigid_body.collision_shape = 'SPHERE'
    trigger.data.materials.append(mat_trigger)

    # === Step 5: Cinematic Slow Motion (Time Scale Keyframing) ===
    rb_world = scene.rigidbody_world
    if rb_world:
        # Assuming 24fps, the sphere takes roughly 12-15 frames to fall this distance
        rb_world.time_scale = 1.0
        rb_world.keyframe_insert(data_path="time_scale", frame=1)
        rb_world.keyframe_insert(data_path="time_scale", frame=12) # Just before impact
        
        # Drop time scale drastically for slow-mo destruction
        rb_world.time_scale = 0.1
        rb_world.keyframe_insert(data_path="time_scale", frame=15)
        rb_world.keyframe_insert(data_path="time_scale", frame=70) # Hold slow-mo
        
        # Ease back to normal speed
        rb_world.time_scale = 1.0
        rb_world.keyframe_insert(data_path="time_scale", frame=90)

    # Clean up selection
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created '{object_name}' Demolition Setup at {location} with {len(tower_objs)} blocks. Hit SPACE to play animation."
