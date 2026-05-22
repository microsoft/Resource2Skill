def create_rain_system(
    scene_name: str = "Scene",
    object_name: str = "RainEmitter",
    location: tuple = (0.0, 0.0, 10.0),
    scale: float = 20.0,
    particle_count: int = 5000,
    rain_speed: float = 4.0,
    **kwargs
) -> str:
    """
    Create a Particle-Based Rain System in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created rain emitter object.
        location: (x, y, z) world-space position (should be placed high above scene).
        scale: The width and depth of the rain emitter plane.
        particle_count: Total number of raindrops.
        rain_speed: Downward Z-axis velocity modifier.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Raindrop Instance Mesh ===
    mesh_drop = bpy.data.meshes.new(f"{object_name}_DropMesh")
    obj_drop = bpy.data.objects.new(f"{object_name}_Drop", mesh_drop)
    scene.collection.objects.link(obj_drop)

    bm_drop = bmesh.new()
    bmesh.ops.create_icosphere(bm_drop, subdivisions=2, radius=1.0)
    for face in bm_drop.faces:
        face.smooth = True  # Auto-smooth shading
    bm_drop.to_mesh(mesh_drop)
    bm_drop.free()

    # Move instance out of the way and hide it
    obj_drop.location = (0, 0, -100)
    obj_drop.hide_viewport = True
    obj_drop.hide_render = True

    # === Step 2: Build Water Material (Refraction) ===
    mat = bpy.data.materials.new(name=f"{object_name}_WaterMat")
    mat.use_nodes = True
    mat.use_screen_refraction = True  # For EEVEE compatibility
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output_node = nodes.new('ShaderNodeOutputMaterial')
    output_node.location = (300, 0)
    
    refraction_node = nodes.new('ShaderNodeBsdfRefraction')
    refraction_node.location = (0, 0)
    refraction_node.inputs['IOR'].default_value = 1.333  # Physical IOR of water
    refraction_node.inputs['Roughness'].default_value = 0.0
    
    links.new(refraction_node.outputs['BSDF'], output_node.inputs['Surface'])
    obj_drop.data.materials.append(mat)

    # === Step 3: Create Emitter Plane ===
    mesh_emit = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj_emit = bpy.data.objects.new(object_name, mesh_emit)
    scene.collection.objects.link(obj_emit)

    bm_emit = bmesh.new()
    s = scale / 2.0
    v1 = bm_emit.verts.new((-s, -s, 0))
    v2 = bm_emit.verts.new(( s, -s, 0))
    v3 = bm_emit.verts.new(( s,  s, 0))
    v4 = bm_emit.verts.new((-s,  s, 0))
    bm_emit.faces.new((v1, v2, v3, v4))
    bm_emit.to_mesh(mesh_emit)
    bm_emit.free()

    obj_emit.location = Vector(location)

    # === Step 4: Particle System Setup ===
    mod = obj_emit.modifiers.new("RainParticles", 'PARTICLE_SYSTEM')
    psys = mod.particle_system
    psettings = psys.settings

    psettings.name = f"{object_name}_ParticleSettings"
    psettings.count = particle_count

    # Timing: start in the negative frames so it is fully raining at frame 1
    psettings.frame_start = -50
    psettings.frame_end = 250
    psettings.lifetime = 100

    # Physics & Velocity
    psettings.normal_factor = 0.0
    psettings.object_align_factor[2] = -rain_speed  # Push particles downwards
    psettings.factor_random = 0.4  # Randomize initial velocity slightly

    # Rendering Setup
    psettings.render_type = 'OBJECT'
    psettings.instance_object = obj_drop
    psettings.particle_size = 0.02
    psettings.size_random = 0.3

    # Visibility Setup: Hide the large emitter plane 
    psettings.use_render_emitter = False
    obj_emit.show_instancer_for_viewport = False
    obj_emit.show_instancer_for_render = False

    return f"Created Rain System '{object_name}' with {particle_count} particles at {location}. Press Play (Spacebar) to simulate the rain."
