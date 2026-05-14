def create_object(
    scene_name: str = "Scene",
    object_name: str = "SnowEmitter",
    location: tuple = (0, 0, 10),
    scale: float = 10.0,
    material_color: tuple = (1.0, 1.0, 1.0, 1.0),
    **kwargs,
) -> str:
    """
    Create a Procedural Falling Snow Particle System.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the emitter object.
        location: (x, y, z) world-space position for the emitter plane (usually high up).
        scale: Size of the emitter plane (coverage area).
        material_color: (R, G, B, A) base color for the snow.
        **kwargs: Optional overrides: 'particle_count', 'snow_size', 'brownian', 'damping'.

    Returns:
        Status string describing the created setup.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    # Extract kwargs
    particle_count = kwargs.get('particle_count', 2000)
    snow_size = kwargs.get('snow_size', 0.05)
    brownian = kwargs.get('brownian', 10.0)
    damping = kwargs.get('damping', 0.15)

    # === Step 1: Create Snow Material ===
    mat_name = "Snow_Material"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            if "Base Color" in bsdf.inputs:
                bsdf.inputs["Base Color"].default_value = material_color
            if "Roughness" in bsdf.inputs:
                bsdf.inputs["Roughness"].default_value = 0.15  # Low roughness for glints
            # Handle API change for Specular in Blender 4.0+
            if "Specular IOR Level" in bsdf.inputs:
                bsdf.inputs["Specular IOR Level"].default_value = 1.0
            elif "Specular" in bsdf.inputs:
                bsdf.inputs["Specular"].default_value = 1.0

    # === Step 2: Create Instance Object (Low-poly Icosphere) ===
    mesh_snow = bpy.data.meshes.new("SnowflakeMesh")
    obj_snow = bpy.data.objects.new("SnowflakeInstance", mesh_snow)
    bpy.context.collection.objects.link(obj_snow)

    # Build icosphere using bmesh (Subdivisions=1 for low poly)
    bm_snow = bmesh.new()
    bmesh.ops.create_icosphere(bm_snow, subdivisions=1, radius=1.0)
    bm_snow.to_mesh(mesh_snow)
    bm_snow.free()

    # Assign material and set shade smooth
    obj_snow.data.materials.append(mat)
    for poly in obj_snow.data.polygons:
        poly.use_smooth = True

    # Move instance out of camera view and hide it (it's just a reference)
    obj_snow.location = Vector((0, 0, -100))
    obj_snow.hide_render = True
    obj_snow.hide_viewport = True

    # === Step 3: Create Emitter Plane ===
    mesh_emitter = bpy.data.meshes.new(object_name + "_Mesh")
    obj_emitter = bpy.data.objects.new(object_name, mesh_emitter)
    bpy.context.collection.objects.link(obj_emitter)

    # Build simple plane using bmesh
    bm_emit = bmesh.new()
    v1 = bm_emit.verts.new((-1.0, -1.0, 0.0))
    v2 = bm_emit.verts.new((1.0, -1.0, 0.0))
    v3 = bm_emit.verts.new((1.0, 1.0, 0.0))
    v4 = bm_emit.verts.new((-1.0, 1.0, 0.0))
    bm_emit.faces.new((v1, v2, v3, v4))
    bm_emit.to_mesh(mesh_emitter)
    bm_emit.free()

    obj_emitter.location = Vector(location)
    obj_emitter.scale = (scale, scale, 1.0)

    # === Step 4: Setup Particle System ===
    mod = obj_emitter.modifiers.new(name="SnowParticles", type='PARTICLE_SYSTEM')
    
    # Access the newly created particle system settings
    psys = obj_emitter.particle_systems[0]
    pset = psys.settings

    # Core Settings
    pset.count = particle_count
    pset.frame_start = 1
    pset.frame_end = 250
    pset.lifetime = 250

    # Rendering Setup
    pset.render_type = 'OBJECT'
    pset.instance_object = obj_snow
    pset.particle_size = snow_size
    pset.size_random = 0.8  # High randomness for natural variation

    # Physics (The key to the "snow" movement)
    pset.physics_type = 'NEWTON'
    pset.mass = 0.05
    pset.brownian_factor = brownian  # Wiggle/Turbulence
    pset.damping = damping           # Floaty air resistance

    # Hide emitter plane from final renders and viewport
    obj_emitter.show_instancer_for_render = False
    obj_emitter.show_instancer_for_viewport = False

    return f"Created '{object_name}' particle emitter at {location} scaled to {scale}x{scale}, simulating {particle_count} falling snowflakes."
