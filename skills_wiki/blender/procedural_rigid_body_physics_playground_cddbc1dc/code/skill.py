def create_object(
    scene_name: str = "Scene",
    object_name: str = "RigidBodyPlayground",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a complete Rigid Body Physics setup demonstrating mass, bounciness, 
    mesh collisions, and kinematic keyframe handoffs.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects and collection.
        location: (x, y, z) world-space offset for the setup.
        scale: Uniform scale factor for the playground elements.
        material_color: Base color for the active dynamic objects.
        **kwargs: Additional overrides.

    Returns:
        Status string summarizing the created setup.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Ensure context is safe for bpy.ops.rigidbody
    if getattr(bpy.context.window, "scene", None) != scene:
        bpy.context.window.scene = scene

    # Create collection to organize the playground
    col = bpy.data.collections.new(object_name)
    scene.collection.children.link(col)
    
    def parent_to_col(obj):
        if obj.name not in col.objects:
            col.objects.link(obj)
        for c in obj.users_collection:
            if c != col:
                c.objects.unlink(obj)

    loc = Vector(location)

    # === Materials ===
    def make_mat(name, color):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = color
            bsdf.inputs['Roughness'].default_value = 0.6
        return mat

    mat_ground = make_mat(f"{object_name}_Ground", (0.05, 0.05, 0.05, 1))
    mat_passive = make_mat(f"{object_name}_Passive", (0.1, 0.3, 0.6, 1))
    mat_active = make_mat(f"{object_name}_Active", material_color + (1.0,))
    mat_heavy = make_mat(f"{object_name}_Heavy", (0.8, 0.5, 0.05, 1))

    # === Helper: Apply Rigid Body Properties ===
    def setup_rb(obj, rb_type='ACTIVE', shape='CONVEX_HULL', mass=1.0, bounciness=0.0, friction=0.5, kinematic=False, source='BASE'):
        bpy.context.view_layer.objects.active = obj
        for o in bpy.context.selected_objects:
            o.select_set(False)
        obj.select_set(True)
        
        # Add to Rigid Body World (creates it if it doesn't exist)
        bpy.ops.rigidbody.object_add()
        
        obj.rigid_body.type = rb_type
        obj.rigid_body.collision_shape = shape
        if rb_type == 'ACTIVE':
            obj.rigid_body.mass = mass
        obj.rigid_body.restitution = bounciness
        obj.rigid_body.friction = friction
        obj.rigid_body.kinematic = kinematic
        if shape == 'MESH':
            obj.rigid_body.mesh_source = source

    # === 1. Ground Plane (Passive) ===
    bpy.ops.mesh.primitive_plane_add(size=20 * scale, location=loc)
    ground = bpy.context.active_object
    ground.name = f"{object_name}_Ground"
    ground.data.materials.append(mat_ground)
    parent_to_col(ground)
    setup_rb(ground, rb_type='PASSIVE', shape='MESH', bounciness=0.3, friction=0.8)

    # === 2. Hollow Tub (Passive, Mesh Collision Source) ===
    mesh = bpy.data.meshes.new(name=f"{object_name}_TubMesh")
    tub = bpy.data.objects.new(f"{object_name}_Tub", mesh)
    scene.collection.objects.link(tub) # Temporarily link to scene to set active
    
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=32, 
                          radius1=2.0*scale, radius2=2.0*scale, depth=1.0*scale)
    # Remove top face to make it hollow
    top_faces = [f for f in bm.faces if f.normal.z > 0.9]
    bmesh.ops.delete(bm, geom=top_faces, context='FACES')
    bm.to_mesh(mesh)
    bm.free()
    
    solidify = tub.modifiers.new("Solidify", 'SOLIDIFY')
    solidify.thickness = 0.2 * scale
    
    tub.location = loc + Vector((4, 0, 0.5)) * scale
    tub.data.materials.append(mat_passive)
    parent_to_col(tub)
    
    # Crucial: Shape = MESH and Source = FINAL so physics calculates the inner hollow space
    setup_rb(tub, rb_type='PASSIVE', shape='MESH', source='FINAL')

    # === 3. Sphere falling into Tub ===
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5*scale, location=loc + Vector((4, 0, 4))*scale)
    sphere = bpy.context.active_object
    sphere.name = f"{object_name}_TubBall"
    sphere.data.materials.append(mat_active)
    parent_to_col(sphere)
    setup_rb(sphere, rb_type='ACTIVE', shape='SPHERE', mass=1.0)

    # === 4. Bouncy Cube (High Restitution) ===
    bpy.ops.mesh.primitive_cube_add(size=1.0*scale, location=loc + Vector((-4, -3, 5))*scale)
    b_cube = bpy.context.active_object
    b_cube.name = f"{object_name}_BouncyCube"
    b_cube.data.materials.append(mat_active)
    parent_to_col(b_cube)
    setup_rb(b_cube, rb_type='ACTIVE', shape='BOX', bounciness=0.85)

    # === 5. Kinematic (Animated) to Dynamic Cube ===
    bpy.ops.mesh.primitive_cube_add(size=1.0*scale, location=loc + Vector((0, -4, 4))*scale)
    a_cube = bpy.context.active_object
    a_cube.name = f"{object_name}_KinematicHandoffCube"
    a_cube.data.materials.append(mat_active)
    parent_to_col(a_cube)
    setup_rb(a_cube, rb_type='ACTIVE', shape='BOX', kinematic=True) # Start as animated
    
    # Keyframe manual animation
    a_cube.keyframe_insert(data_path="rigid_body.kinematic", frame=1)
    a_cube.keyframe_insert(data_path="location", frame=1)
    
    a_cube.location = loc + Vector((0, -1, 4))*scale
    a_cube.keyframe_insert(data_path="location", frame=30)
    
    # Hand off to physics engine at frame 30
    a_cube.rigid_body.kinematic = False
    a_cube.keyframe_insert(data_path="rigid_body.kinematic", frame=30)

    # === 6. Mass Demonstration: Ramp, Roller, Heavy Object ===
    # Ramp
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc + Vector((-3, 4, 1.5))*scale)
    ramp = bpy.context.active_object
    ramp.name = f"{object_name}_Ramp"
    ramp.scale = (4*scale, 2*scale, 0.2*scale)
    ramp.rotation_euler = (0, -0.3, 0)
    ramp.data.materials.append(mat_passive)
    parent_to_col(ramp)
    bpy.context.view_layer.objects.active = ramp
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    setup_rb(ramp, rb_type='PASSIVE', shape='BOX')

    # Roller
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5*scale, depth=1.5*scale, location=loc + Vector((-4.5, 4, 3.5))*scale)
    roller = bpy.context.active_object
    roller.name = f"{object_name}_Roller"
    roller.rotation_euler = (1.5708, 0, 0)
    roller.data.materials.append(mat_active)
    parent_to_col(roller)
    setup_rb(roller, rb_type='ACTIVE', shape='CYLINDER', mass=2.0)

    # Heavy Cube
    bpy.ops.mesh.primitive_cube_add(size=1.0*scale, location=loc + Vector((-1, 4, 1.0))*scale)
    h_cube = bpy.context.active_object
    h_cube.name = f"{object_name}_HeavyCube"
    h_cube.rotation_euler = (0, -0.3, 0)
    h_cube.data.materials.append(mat_heavy)
    parent_to_col(h_cube)
    setup_rb(h_cube, rb_type='ACTIVE', shape='BOX', mass=500.0) # Extreme mass, won't be pushed by the roller easily

    # === Finalizing Timeline and Cache ===
    scene.frame_start = 1
    scene.frame_end = 250
    if scene.rigidbody_world:
        scene.rigidbody_world.point_cache.frame_end = 250

    return f"Created Rigid Body Playground '{object_name}' with 7 interacting physics objects at {location}. Press 'Play' in the timeline to simulate."
