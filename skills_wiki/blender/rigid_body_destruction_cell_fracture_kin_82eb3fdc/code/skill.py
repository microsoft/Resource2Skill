def create_object(
    scene_name: str = "Scene",
    object_name: str = "DestructibleWall",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.3, 0.1),
    **kwargs,
) -> str:
    """
    Creates a fractured rigid body wall and an animated kinematic smasher.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated objects.
        location: (x, y, z) world-space position of the center base of the simulation.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the wall's exterior.
        **kwargs: Additional parameters.

    Returns:
        Status string describing the creation of the simulation.
    """
    import bpy
    import addon_utils
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # 1. Enable the Cell Fracture add-on (built into Blender)
    addon_utils.enable("object_fracture_cell")
    
    # 2. Setup Rigid Body World if it doesn't exist
    if not scene.rigidbody_world:
        # We need to call this contextually
        override = bpy.context.copy()
        override['scene'] = scene
        with bpy.context.temp_override(**override):
            bpy.ops.rigidbody.world_add()
            
    # 3. Create Materials
    mat_outer = bpy.data.materials.new(name=f"{object_name}_Outer")
    mat_outer.use_nodes = True
    mat_outer.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*material_color, 1.0)
    
    mat_inner = bpy.data.materials.new(name=f"{object_name}_Inner")
    mat_inner.use_nodes = True
    mat_inner.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (max(0, material_color[0]-0.2), max(0, material_color[1]-0.2), max(0, material_color[2]-0.2), 1.0)
    mat_inner.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95

    mat_smasher = bpy.data.materials.new(name=f"{object_name}_Smasher_Mat")
    mat_smasher.use_nodes = True
    mat_smasher.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.1, 0.1, 0.1, 1.0)
    mat_smasher.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 1.0

    # 4. Create the target wall to be fractured
    wall_z_height = location[2] + (1.5 * scale)
    bpy.ops.mesh.primitive_cube_add(size=2, location=(location[0], location[1], wall_z_height))
    target_obj = bpy.context.active_object
    target_obj.name = f"{object_name}_Base"
    target_obj.scale = (scale, scale * 0.2, scale * 1.5)
    
    # Apply scale so the fracture algorithm works correctly
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Assign materials (Index 0: Outer, Index 1: Inner)
    target_obj.data.materials.append(mat_outer)
    target_obj.data.materials.append(mat_inner)
    
    # Subdivide target object for better, more complex fracture points
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=3)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Track existing objects to isolate the new fractured shards
    existing_objects = set(scene.objects)
    fragments = []
    
    # 5. Apply Cell Fracture (with fallback mechanism)
    try:
        # The add-on operator creates the fragments and automatically assigns the inner material
        bpy.ops.object.add_fracture_cell_objects(
            source_limit=40,
            source_noise=1.0,
            material_index=0,
            interior_material_index=1,
            use_sharp_edges=False,
            margin=0.005
        )
        
        # Hide the original unfractured object
        target_obj.hide_viewport = True
        target_obj.hide_render = True
        
        # Collect new fragments
        fragments = [obj for obj in scene.objects if obj not in existing_objects]
        
    except Exception as e:
        print(f"Cell fracture failed (likely due to context). Using manual brick fallback. Error: {e}")
        target_obj.hide_viewport = True
        target_obj.hide_render = True
        
        # Fallback: Create a procedural brick wall if add-on fails
        for x in range(5):
            for z in range(6):
                bpy.ops.mesh.primitive_cube_add(
                    size=1, 
                    location=(location[0] + (x - 2) * scale * 0.6, location[1], location[2] + z * scale * 0.5 + 0.25)
                )
                brick = bpy.context.active_object
                brick.scale = (scale * 0.29, scale * 0.2, scale * 0.24)
                brick.data.materials.append(mat_outer)
                fragments.append(brick)
    
    # 6. Configure Rigid Bodies for all Fragments
    for frag in fragments:
        bpy.context.view_layer.objects.active = frag
        
        if not frag.rigid_body:
            bpy.ops.rigidbody.object_add()
            
        frag.rigid_body.type = 'ACTIVE'
        frag.rigid_body.mass = 1.5
        frag.rigid_body.collision_shape = 'CONVEX_HULL'
        frag.rigid_body.friction = 0.8
        
        # CRITICAL: Start deactivated so the wall holds its shape until hit
        frag.rigid_body.use_deactivation = True
        frag.rigid_body.use_start_deactivated = True

    # 7. Create Ground Plane (Passive Collider)
    bpy.ops.mesh.primitive_plane_add(size=20 * scale, location=(location[0], location[1], location[2]))
    ground = bpy.context.active_object
    ground.name = f"{object_name}_Ground"
    bpy.ops.rigidbody.object_add()
    ground.rigid_body.type = 'PASSIVE'
    ground.rigid_body.collision_shape = 'MESH'
    ground.rigid_body.friction = 1.0
    
    # 8. Create Kinematic Smasher (The Projectile)
    smasher_z = location[2] + 1.5 * scale
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.4 * scale, 
        depth=3 * scale, 
        location=(location[0] - 6 * scale, location[1], smasher_z)
    )
    smasher = bpy.context.active_object
    smasher.name = f"{object_name}_Smasher"
    smasher.rotation_euler[1] = math.radians(90) # Rotate horizontally
    smasher.data.materials.append(mat_smasher)
    
    # Configure Smasher physics
    bpy.ops.rigidbody.object_add()
    smasher.rigid_body.type = 'PASSIVE'
    smasher.rigid_body.kinematic = True # 'Animated' property in UI
    
    # Animate the Smasher passing through the wall
    smasher.location[0] = location[0] - 6 * scale
    smasher.keyframe_insert(data_path="location", frame=1)
    
    smasher.location[0] = location[0] + 6 * scale
    smasher.keyframe_insert(data_path="location", frame=25)
    
    # 9. Set Animation Range
    scene.frame_start = 1
    scene.frame_end = 120
    scene.frame_set(1)
    
    return f"Created '{object_name}' rigid body simulation with {len(fragments)} fragments. Play animation to trigger destruction."
