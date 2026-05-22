def create_rigid_body_demolition(
    scene_name: str = "Scene",
    object_name: str = "RBDemo",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.1, 0.1),
    **kwargs,
) -> str:
    """
    Create a Rigid Body demolition scene with a slide, ball, and block stack.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated collection and objects.
        location: (x, y, z) world-space offset for the entire setup.
        scale: Uniform scale factor for all elements.
        material_color: (R, G, B) color for the custom physics slide.
        
    Returns:
        Status string describing the generated scene.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Initialization & Helpers ===
    collection = bpy.data.collections.new(object_name)
    scene.collection.children.link(collection)
    
    loc_offset = Vector(location)
    
    def add_rb(obj, rb_type='ACTIVE', shape='CONVEX_HULL', mass=1.0):
        """Safely assign Rigid Body physics to an object."""
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        if obj.rigid_body is None:
            try:
                bpy.ops.rigidbody.object_add()
            except Exception as e:
                print(f"Warning: Could not add rigid body: {e}")
                return
                
        if obj.rigid_body:
            obj.rigid_body.type = rb_type
            obj.rigid_body.collision_shape = shape
            if rb_type == 'ACTIVE':
                obj.rigid_body.mass = mass

    def make_material(name, color, metallic=0.0, roughness=0.5):
        """Create a simple Principled BSDF material."""
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (*color, 1.0)
            bsdf.inputs['Metallic'].default_value = metallic
            bsdf.inputs['Roughness'].default_value = roughness
        return mat

    # Create Materials
    mat_ramp = make_material(f"{object_name}_Mat_Ramp", material_color, roughness=0.3)
    mat_blocks = make_material(f"{object_name}_Mat_Blocks", (0.8, 0.6, 0.05), roughness=0.7)
    mat_ball = make_material(f"{object_name}_Mat_Ball", (0.9, 0.9, 0.9), metallic=1.0, roughness=0.1)

    # === Step 2: Ground Plane ===
    bpy.ops.mesh.primitive_plane_add(size=30 * scale)
    ground = bpy.context.active_object
    ground.name = f"{object_name}_Ground"
    ground.location = loc_offset
    
    collection.objects.link(ground)
    for coll in ground.users_collection:
        if coll != collection:
            coll.objects.unlink(ground)
            
    add_rb(ground, rb_type='PASSIVE', shape='CONVEX_HULL')

    # === Step 3: Custom Curved Slide ===
    bpy.ops.mesh.primitive_cube_add(size=2.0)
    ramp = bpy.context.active_object
    ramp.name = f"{object_name}_Slide"
    ramp.location = loc_offset + Vector((3.0 * scale, 0, 1.0 * scale))
    
    # Enter Edit mode to bevel the top-left edge
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(ramp.data)
    for e in bm.edges:
        e.select = False
        
    # Isolate the specific edge (-X, +Z) to create the downward slope
    target_edges = [e for e in bm.edges if all(v.co.x < -0.9 and v.co.z > 0.9 for v in e.verts)]
    if target_edges:
        bmesh.ops.bevel(bm, geom=target_edges, offset=1.8, segments=24, profile=0.5, affect_type=0)
        
    bmesh.update_edit_mesh(ramp.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Apply scale after modeling for correct physics bounds
    ramp.scale = (scale, scale, scale)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    ramp.data.materials.append(mat_ramp)
    for poly in ramp.data.polygons:
        poly.use_smooth = True
        
    collection.objects.link(ramp)
    for coll in ramp.users_collection:
        if coll != collection:
            coll.objects.unlink(ramp)
            
    # CRITICAL: Concave objects MUST use 'MESH' collision shape
    add_rb(ramp, rb_type='PASSIVE', shape='MESH')

    # === Step 4: Destructible Block Stack ===
    cube_size = 0.4 * scale
    gap = 0.02 * scale
    x_count, y_count, z_count = 3, 5, 5
    block_count = 0
    
    for z in range(z_count):
        for y in range(y_count):
            for x in range(x_count):
                bpy.ops.mesh.primitive_cube_add(size=cube_size)
                cube = bpy.context.active_object
                cube.name = f"{object_name}_Block_{x}_{y}_{z}"
                
                # Center the array on the Y axis, position it in front of the ramp
                y_pos = (y - y_count/2 + 0.5) * (cube_size + gap)
                x_pos = 0.5 * scale + x * (cube_size + gap)
                z_pos = cube_size/2 + z * (cube_size + gap)
                
                cube.location = loc_offset + Vector((x_pos, y_pos, z_pos))
                cube.data.materials.append(mat_blocks)
                
                collection.objects.link(cube)
                for coll in cube.users_collection:
                    if coll != collection:
                        coll.objects.unlink(cube)
                
                # Active, lightweight
                add_rb(cube, rb_type='ACTIVE', shape='CONVEX_HULL', mass=0.05)
                block_count += 1

    # === Step 5: Heavy Projectile Sphere ===
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4 * scale)
    ball = bpy.context.active_object
    ball.name = f"{object_name}_Ball"
    # Position the ball directly above the upper curve of the slide
    ball.location = loc_offset + Vector((3.6 * scale, 0, 3.5 * scale))
    ball.data.materials.append(mat_ball)
    bpy.ops.object.shade_smooth()
    
    collection.objects.link(ball)
    for coll in ball.users_collection:
        if coll != collection:
            coll.objects.unlink(ball)
            
    # Active, heavy, explicit Sphere collision
    add_rb(ball, rb_type='ACTIVE', shape='SPHERE', mass=2.0)
    
    # === Step 6: Presentation Light ===
    bpy.ops.object.light_add(type='AREA', location=loc_offset + Vector((2.0 * scale, 0, 8.0 * scale)))
    light = bpy.context.active_object
    light.name = f"{object_name}_Light"
    light.data.energy = 1000 * (scale ** 2)
    light.data.size = 10.0 * scale
    
    collection.objects.link(light)
    for coll in light.users_collection:
        if coll != collection:
            coll.objects.unlink(light)

    # === Finalize ===
    # Ensure timeline is long enough and rewind to frame 1 to reset physics cache
    scene.frame_end = max(scene.frame_end, 200)
    scene.frame_set(1)

    return f"Created '{object_name}' with 1 slide, 1 heavy ball, {block_count} blocks, and ready-to-play physics."
