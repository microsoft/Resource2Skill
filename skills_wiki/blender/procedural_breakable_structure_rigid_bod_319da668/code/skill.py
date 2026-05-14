def create_breakable_wall(
    scene_name: str = "Scene",
    object_name: str = "BreakableWall",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a staggered brick wall bound by breakable rigid body constraints, 
    complete with an animated projectile to smash it.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the collections and objects.
        location: (x, y, z) world-space position of the wall base.
        scale: Uniform scale factor for the wall and bricks.
        material_color: (R, G, B) color of the bricks.
        **kwargs: Optional 'rows' (int), 'cols' (int), and 'break_threshold' (float).

    Returns:
        Status string describing the generated physics system.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    bpy.context.window.scene = scene  # Ensure context is correct for physics ops

    rows = kwargs.get("rows", 10)
    cols = kwargs.get("cols", 10)
    break_threshold = kwargs.get("break_threshold", 250.0) * scale

    # === Step 1: Setup Rigid Body World ===
    if scene.rigidbody_world is None:
        bpy.ops.rigidbody.world_add()

    # Create Collections for organization
    wall_col = bpy.data.collections.new(f"{object_name}_Bricks")
    constraint_col = bpy.data.collections.new(f"{object_name}_Constraints")
    scene.collection.children.link(wall_col)
    scene.collection.children.link(constraint_col)

    # === Step 2: Build Materials ===
    brick_mat = bpy.data.materials.new(name=f"{object_name}_BrickMat")
    brick_mat.use_nodes = True
    bsdf = brick_mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.9

    proj_mat = bpy.data.materials.new(name=f"{object_name}_ProjectileMat")
    proj_mat.use_nodes = True
    p_bsdf = proj_mat.node_tree.nodes.get("Principled BSDF")
    p_bsdf.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1.0)
    p_bsdf.inputs['Metallic'].default_value = 1.0
    p_bsdf.inputs['Roughness'].default_value = 0.4

    # === Step 3: Create Master Brick Geometry ===
    b_w = 0.4 * scale
    b_d = 0.2 * scale
    b_h = 0.2 * scale
    gap = 0.02 * scale

    mesh = bpy.data.meshes.new(f"{object_name}_BrickData")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(b_w, b_d, b_h), verts=bm.verts)
    
    # Bevel the brick edges for realism
    bmesh.ops.bevel(bm, geom=bm.edges, offset=0.01*scale, segments=2, profile=0.5)
    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.append(brick_mat)

    # === Step 4: Assemble the Wall ===
    brick_objs = []
    
    for row in range(rows):
        z = location[2] + row * (b_h + gap) + (b_h / 2)
        # Stagger every other row
        offset = (b_w / 2) if row % 2 != 0 else 0
        for col in range(cols):
            x = location[0] + col * (b_w + gap) + offset - (cols * b_w / 2)
            y = location[1]
            
            # Instance the mesh
            brick = bpy.data.objects.new(f"{object_name}_Brick_{row}_{col}", mesh)
            brick.location = (x, y, z)
            wall_col.objects.link(brick)
            
            # Setup Rigid Body
            bpy.context.view_layer.objects.active = brick
            brick.select_set(True)
            bpy.ops.rigidbody.object_add()
            brick.rigid_body.mass = 2.0
            brick.rigid_body.friction = 0.8
            brick.rigid_body.collision_margin = 0.001
            brick.select_set(False)
            
            brick_objs.append(brick)

    # === Step 5: Generate Breakable Constraints ===
    # Connect adjacent bricks by measuring distance
    search_radius = max(b_w, b_h) * 1.5 
    constraints_created = 0

    for i in range(len(brick_objs)):
        b1 = brick_objs[i]
        for j in range(i + 1, len(brick_objs)):
            b2 = brick_objs[j]
            dist = (b1.location - b2.location).length
            
            if dist <= search_radius:
                # Create an Empty to hold the constraint
                empty = bpy.data.objects.new(f"{object_name}_Constraint_{i}_{j}", None)
                empty.empty_display_type = 'ARROWS'
                empty.empty_display_size = 0.1 * scale
                empty.location = (b1.location + b2.location) / 2
                constraint_col.objects.link(empty)
                
                # Apply Rigid Body Constraint
                bpy.context.view_layer.objects.active = empty
                empty.select_set(True)
                bpy.ops.rigidbody.constraint_add()
                
                rbc = empty.rigid_body_constraint
                rbc.type = 'FIXED'
                rbc.object1 = b1
                rbc.object2 = b2
                rbc.use_breaking = True
                rbc.breaking_threshold = break_threshold
                
                empty.select_set(False)
                constraints_created += 1

    # === Step 6: Add Ground Plane ===
    bpy.ops.mesh.primitive_plane_add(size=20*scale, location=location)
    ground = bpy.context.active_object
    ground.name = f"{object_name}_Ground"
    
    bpy.ops.rigidbody.object_add()
    ground.rigid_body.type = 'PASSIVE'
    ground.rigid_body.friction = 1.0

    # === Step 7: Add Animated Projectile ===
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.6*scale, location=(0,0,0))
    projectile = bpy.context.active_object
    projectile.name = f"{object_name}_Projectile"
    projectile.data.materials.append(proj_mat)
    
    bpy.ops.rigidbody.object_add()
    projectile.rigid_body.type = 'ACTIVE'
    projectile.rigid_body.kinematic = True  # Allows us to animate it overriding physics
    projectile.rigid_body.mass = 500.0
    
    # Animate projectile crashing through the wall
    start_y = location[1] - (6.0 * scale)
    end_y = location[1] + (3.0 * scale)
    hit_z = location[2] + (rows * b_h * 0.4) # Aim slightly below center
    
    projectile.location = (location[0], start_y, hit_z)
    projectile.keyframe_insert(data_path="location", frame=1)
    
    projectile.location = (location[0], end_y, hit_z)
    projectile.keyframe_insert(data_path="location", frame=12) # High speed impact

    # Make sure scene starts at frame 1 for simulation
    scene.frame_set(1)

    return f"Created breakable structure '{object_name}' with {len(brick_objs)} bricks and {constraints_created} structural constraints."
