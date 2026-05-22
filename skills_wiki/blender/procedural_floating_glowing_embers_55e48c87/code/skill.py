def create_floating_embers(
    scene_name: str = "Scene",
    emitter_name: str = "EmberEmitter",
    location: tuple = (0, 0, 0),
    scale: float = 10.0,
    particle_count: int = 3000,
    emission_strength: float = 3.0,
    **kwargs,
) -> str:
    """
    Create a procedural glowing ember particle system.

    Args:
        scene_name: Name of the target scene.
        emitter_name: Name for the emitter plane object.
        location: (x, y, z) base location for the emitter plane.
        scale: Size of the emitter plane.
        particle_count: Total number of floating embers.
        emission_strength: Glow intensity of the embers.

    Returns:
        Status string.
    """
    import bpy
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Enable Bloom for Eevee to make the embers glow
    if scene.render.engine == 'BLENDER_EEVEE':
        scene.eevee.use_bloom = True
        scene.eevee.bloom_intensity = 0.05

    # === Step 1: Create the Instance Object (Ember Mesh) ===
    # We create a 16-vert NGon circle programmatically and hide it
    ember_mesh = bpy.data.meshes.new(name="EmberMesh")
    
    verts = []
    edges = []
    faces = [list(range(16))]
    
    for i in range(16):
        angle = (math.pi * 2.0 / 16) * i
        verts.append((math.cos(angle) * 0.05, math.sin(angle) * 0.05, 0.0))
        if i < 15:
            edges.append((i, i + 1))
        else:
            edges.append((15, 0))
            
    ember_mesh.from_pydata(verts, edges, faces)
    ember_mesh.update()
    
    ember_obj = bpy.data.objects.new("EmberInstance", ember_mesh)
    scene.collection.objects.link(ember_obj)
    
    # Hide the original instance object from viewport and render
    ember_obj.hide_viewport = True
    ember_obj.hide_render = True
    ember_obj.location = (0, 0, -50) # Bury it far below

    # === Step 2: Create Material with Random Per-Particle Color ===
    mat = bpy.data.materials.new(name="EmberMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Add nodes
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (400, 0)

    emission_node = nodes.new(type='ShaderNodeEmission')
    emission_node.location = (200, 0)
    emission_node.inputs['Strength'].default_value = emission_strength

    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (0, 0)

    object_info = nodes.new(type='ShaderNodeObjectInfo')
    object_info.location = (-200, 0)

    # Configure Color Ramp for fire/ember colors
    elements = color_ramp.color_ramp.elements
    # Default comes with 2 elements. Set ends first.
    elements[0].position = 0.0
    elements[0].color = (0.2, 0.0, 0.0, 1.0) # Dark red/cool ember
    
    elements[1].position = 1.0
    elements[1].color = (1.0, 1.0, 1.0, 1.0) # White hot
    
    # Add middle colors
    el1 = elements.new(0.3)
    el1.color = (0.8, 0.1, 0.0, 1.0) # Bright red
    
    el2 = elements.new(0.7)
    el2.color = (1.0, 0.6, 0.0, 1.0) # Orange/Yellow

    # Link nodes
    links.new(object_info.outputs['Random'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], emission_node.inputs['Color'])
    links.new(emission_node.outputs['Emission'], output_node.inputs['Surface'])

    # Assign material to the instance object
    ember_obj.data.materials.append(mat)

    # === Step 3: Create Emitter Plane ===
    bpy.ops.mesh.primitive_plane_add(size=1, location=location)
    emitter_obj = bpy.context.active_object
    emitter_obj.name = emitter_name
    emitter_obj.scale = (scale, scale, 1.0)

    # Hide the emitter plane itself
    emitter_obj.show_instancer_for_render = False
    emitter_obj.show_instancer_for_viewport = False

    # === Step 4: Configure Particle System ===
    ps_mod = emitter_obj.modifiers.new(name="EmberParticles", type='PARTICLE_SYSTEM')
    psys = ps_mod.particle_system
    pset = psys.settings

    # Emission rules
    pset.count = particle_count
    pset.frame_start = -300     # Pre-roll so scene is full of embers at frame 1
    pset.frame_end = 3000       # Emit continuously
    pset.lifetime = 3000        # Don't let them pop out of existence

    # Physics & Movement
    pset.physics_type = 'NEWTON'
    pset.effector_weights.gravity = 0.0  # Float instead of fall
    pset.normal_factor = 1.2             # Initial upward push
    pset.factor_random = 1.0             # Randomize initial speed
    pset.brownian_factor = 1.0           # Jittery, chaotic drifting

    # Rotation
    pset.use_rotations = True
    pset.rotation_mode = 'NOR'
    pset.rotation_factor_random = 1.0    # Randomize orientation
    
    # Render settings (Instance the Ember object)
    pset.render_type = 'OBJECT'
    pset.instance_object = ember_obj
    pset.particle_size = 0.1
    pset.size_random = 0.8               # High size variation (some tiny, some larger)

    # Ensure textures are properly evaluated for instances
    pset.use_render_emitter = False
    
    # Force viewport update
    bpy.context.view_layer.update()

    return f"Created procedural floating embers '{emitter_name}' at {location} with {particle_count} instances."
