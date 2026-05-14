def create_object(
    scene_name: str = "Scene",
    object_name: str = "SnowEmitter",
    location: tuple = (0, 0, 10),
    scale: float = 1.0,
    emitter_size: tuple = (20.0, 20.0),
    loop_length: int = 250,
    particle_count: int = 1800,
    **kwargs,
) -> str:
    """
    Create Procedural Looping Falling Snow in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created emitter object.
        location: (x, y, z) world-space position of the emitter plane.
        scale: Uniform scale factor for the emitter.
        emitter_size: Width and length of the snowfall area.
        loop_length: Total frames for the perfect animation loop.
        particle_count: Number of particles per system (double this for total).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Snowflake Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_SnowMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (100, 0)
    bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
    
    if 'Roughness' in bsdf.inputs:
        bsdf.inputs['Roughness'].default_value = 0.0
        
    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.location = (-500, -200)
    noise.inputs['Scale'].default_value = 3.0
    noise.inputs['Detail'].default_value = 10.0
    
    bump = nodes.new(type='ShaderNodeBump')
    bump.location = (-200, -200)
    bump.inputs['Strength'].default_value = 1.0
    
    tc = nodes.new(type='ShaderNodeTexCoord')
    tc.location = (-700, -200)
    
    links.new(tc.outputs['Object'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # === Step 2: Create Snow Instances ===
    snow_col_name = f"{object_name}_Instances"
    snow_col = bpy.data.collections.get(snow_col_name)
    if not snow_col:
        snow_col = bpy.data.collections.new(snow_col_name)
        scene.collection.children.link(snow_col)
        snow_col.hide_viewport = True
        snow_col.hide_render = True

    snowflakes = []
    # Base scales for variations: uniform, elongated, squashed
    variants = [
        (1.0, 1.0, 1.0),
        (1.5, 0.8, 0.8),
        (0.8, 1.5, 1.2)
    ]

    for i, scale_vec in enumerate(variants):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0)
        obj = bpy.context.active_object
        obj.name = f"{object_name}_Flake_{i}"
        bpy.ops.object.shade_smooth()
        
        # Organic vertex displacement
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        for v in bm.verts:
            v.co.x += random.uniform(-0.1, 0.1)
            v.co.y += random.uniform(-0.1, 0.1)
            v.co.z += random.uniform(-0.1, 0.1)
        bm.to_mesh(obj.data)
        bm.free()
        
        # Apply shaping scale
        obj.scale = (scale_vec[0] * 0.1, scale_vec[1] * 0.1, scale_vec[2] * 0.1)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        obj.data.materials.append(mat)
        
        # Link to hidden collection and unlink from main scene
        snow_col.objects.link(obj)
        bpy.context.scene.collection.objects.unlink(obj)
        snowflakes.append(obj)

    # === Step 3: Create Emitter ===
    bpy.ops.mesh.primitive_plane_add(size=1.0)
    emitter = bpy.context.active_object
    emitter.name = object_name
    emitter.location = Vector(location)
    emitter.scale = (emitter_size[0] * scale, emitter_size[1] * scale, 1.0)
    
    # Hide the emitter plane
    emitter.show_instancer_for_viewport = False
    emitter.show_instancer_for_render = False

    # Define particle system helper
    def setup_snow_ps(ps_name, f_start, f_end):
        ps = emitter.modifiers.new(name=ps_name, type='PARTICLE_SYSTEM')
        settings = ps.particle_system.settings
        
        settings.count = particle_count
        settings.frame_start = f_start
        settings.frame_end = f_end
        settings.lifetime = loop_length * 4  # Ensure particles do not die on screen
        
        settings.render_type = 'COLLECTION'
        settings.instance_collection = snow_col
        settings.particle_size = 0.4
        settings.size_random = 0.6
        
        # Rotation Settings
        try:
            settings.use_rotations = True
            settings.rotation_factor_random = 1.0
            settings.phase_factor = 1.0
            settings.phase_factor_random = 2.0
            settings.use_dynamic_rotation = True
            settings.angular_velocity_mode = 'VELOCITY'
            settings.angular_velocity_factor = 4.0
        except AttributeError:
            pass # Failsafe for older/future API changes
            
        # Velocity Settings
        try:
            settings.normal_factor = 0.0
            settings.object_align_factor = (0.0, 0.0, -2.0)
            settings.factor_random = 3.4
        except AttributeError:
            pass
            
        # Custom Slow Integration Physics
        try:
            settings.effector_weights.gravity = 0.1
            settings.physics_type = 'NEWTONIAN'
            settings.integration_timestep = 0.02
        except AttributeError:
            pass
            
        return ps

    # === Step 4: Setup Overlapping Looping Systems ===
    # System 1 drives the first loop cycle
    setup_snow_ps(f"{object_name}_Loop1", 1, loop_length)
    # System 2 overlaps perfectly to make the loop seamless
    setup_snow_ps(f"{object_name}_Loop2", -loop_length + 1, 0)
    
    # === Step 5: Final Scene Context ===
    scene.frame_start = 1
    scene.frame_end = loop_length
    scene.render.film_transparent = True
    
    # Add a Sun Light for high-contrast icy glints
    sun_data = bpy.data.lights.new(name=f"{object_name}_Sun", type='SUN')
    sun_data.energy = 5.0
    sun_obj = bpy.data.objects.new(name=f"{object_name}_Sun", object_data=sun_data)
    scene.collection.objects.link(sun_obj)
    sun_obj.location = (location[0], location[1], location[2] + 5.0)
    sun_obj.rotation_euler = (math.radians(45), math.radians(45), 0)

    return f"Created seamless looping snow '{object_name}' with {particle_count * 2} particles over {loop_length} frames."
