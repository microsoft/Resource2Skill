def create_object(
    scene_name: str = "Scene",
    object_name: str = "RigidBodyDrop",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a Rigid Body physics setup featuring falling active objects
    caught by a spinning passive concave bowl.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for created objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: Fallback parameter (overridden by procedural color ramp).
        **kwargs: Additional options (e.g., grid_size).

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Initialize Rigid Body World ===
    # Ensure context overrides allow world creation if it doesn't exist
    if scene.rigidbody_world is None:
        # Trick to safely add rigid body world without strict context
        override = bpy.context.copy()
        override['scene'] = scene
        with bpy.context.temp_override(**override):
            bpy.ops.rigidbody.world_add()
            
    scene.rigidbody_world.point_cache.frame_start = 1
    scene.rigidbody_world.point_cache.frame_end = 250
    scene.frame_set(1) # Reset timeline so physics objects position properly

    # Define parameters
    grid_size = kwargs.get("grid_size", 4)
    
    # === Step 2: Build Materials ===
    # Dark Metallic Bowl
    mat_bowl = bpy.data.materials.new(name=f"{object_name}_Bowl_Mat")
    mat_bowl.use_nodes = True
    bsdf_bowl = mat_bowl.node_tree.nodes.get("Principled BSDF")
    if bsdf_bowl:
        bsdf_bowl.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)
        bsdf_bowl.inputs['Metallic'].default_value = 0.8
        bsdf_bowl.inputs['Roughness'].default_value = 0.3

    # Procedural Multi-Color Debris
    mat_debris = bpy.data.materials.new(name=f"{object_name}_Debris_Mat")
    mat_debris.use_nodes = True
    tree = mat_debris.node_tree
    tree.nodes.clear()

    out_node = tree.nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (300, 0)

    bsdf_node = tree.nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (0, 0)
    bsdf_node.inputs['Roughness'].default_value = 0.4
    tree.links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])

    obj_info = tree.nodes.new('ShaderNodeObjectInfo')
    obj_info.location = (-600, 0)

    color_ramp = tree.nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-300, 0)
    color_ramp.color_ramp.elements[0].color = (0.8, 0.15, 0.15, 1.0)
    color_ramp.color_ramp.elements[1].color = (0.15, 0.4, 0.8, 1.0)
    el = color_ramp.color_ramp.elements.new(0.5)
    el.color = (0.8, 0.6, 0.15, 1.0)

    tree.links.new(obj_info.outputs['Random'], color_ramp.inputs['Fac'])
    tree.links.new(color_ramp.outputs['Color'], bsdf_node.inputs['Base Color'])

    # === Step 3: Create Passive Catcher (Animated Bowl) ===
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=5.0 * scale, location=location)
    bowl = bpy.context.active_object
    bowl.name = f"{object_name}_Passive_Bowl"
    bowl.data.materials.append(mat_bowl)
    bpy.ops.object.shade_smooth()

    # Slice upper half using bmesh
    bm = bmesh.new()
    bm.from_mesh(bowl.data)
    # v.co is local, so > 0 removes the top half of the sphere
    verts_to_delete = [v for v in bm.verts if v.co.z > 0.0]
    bmesh.ops.delete(bm, geom=verts_to_delete, context='VERTS')
    bm.to_mesh(bowl.data)
    bm.free()

    # Add thickness
    mod = bowl.modifiers.new("Solidify", 'SOLIDIFY')
    mod.thickness = 0.2 * scale
    mod.offset = 1.0  # Expand outward

    # Add Passive Rigid Body
    bpy.ops.rigidbody.object_add()
    bowl.rigid_body.type = 'PASSIVE'
    bowl.rigid_body.collision_shape = 'MESH' # Crucial for concave hollow objects
    bowl.rigid_body.kinematic = True         # Matches 'Animated' checkbox, allowing manual keyframes
    bowl.rigid_body.friction = 0.7
    bowl.rigid_body.restitution = 0.2

    # Keyframe slow rotation to stir the debris
    bowl.rotation_mode = 'XYZ'
    bowl.rotation_euler[2] = 0.0
    bowl.keyframe_insert(data_path="rotation_euler", index=2, frame=1)
    bowl.rotation_euler[2] = math.pi * 2 # 360 degrees
    bowl.keyframe_insert(data_path="rotation_euler", index=2, frame=250)
    bowl.rotation_euler[2] = 0.0 # Reset for viewport

    # === Step 4: Create Active Debris Grid ===
    spacing = 1.5 * scale
    offset = (grid_size * spacing) / 2.0
    start_z = location[2] + 7.0 * scale

    count = 0
    for x in range(grid_size):
        for y in range(grid_size):
            for z in range(grid_size):
                pos = (
                    location[0] + x * spacing - offset + spacing/2,
                    location[1] + y * spacing - offset + spacing/2,
                    start_z + z * spacing
                )
                
                # Randomly spawn cubes or spheres
                is_cube = random.random() > 0.5
                if is_cube:
                    bpy.ops.mesh.primitive_cube_add(size=0.8 * scale, location=pos)
                    shape = 'CONVEX_HULL'
                else:
                    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.4 * scale, subdivisions=2, location=pos)
                    shape = 'SPHERE'
                    
                obj = bpy.context.active_object
                obj.name = f"{object_name}_Active_Debris_{count}"
                count += 1
                
                obj.rotation_euler = (random.uniform(0, 6.28), random.uniform(0, 6.28), random.uniform(0, 6.28))
                obj.data.materials.append(mat_debris)
                
                if not is_cube:
                    bpy.ops.object.shade_smooth()
                    
                # Add Active Rigid Body
                bpy.ops.rigidbody.object_add()
                obj.rigid_body.type = 'ACTIVE'
                obj.rigid_body.mass = random.uniform(0.5, 2.0)
                obj.rigid_body.collision_shape = shape
                obj.rigid_body.friction = 0.5
                obj.rigid_body.restitution = random.uniform(0.2, 0.8) # Bounciness

    # === Step 5: Scene Lighting ===
    if not any(o.type == 'LIGHT' for o in scene.objects):
        bpy.ops.object.light_add(type='SUN', location=(location[0] + 10, location[1] - 10, location[2] + 10))
        sun = bpy.context.active_object
        sun.data.energy = 4.0
        sun.rotation_euler = (math.radians(45), 0, math.radians(45))

    bpy.ops.object.select_all(action='DESELECT')
    return f"Created '{object_name}' setup at {location} with 1 animated passive bowl and {count} active physics objects. Press Spacebar to simulate."
