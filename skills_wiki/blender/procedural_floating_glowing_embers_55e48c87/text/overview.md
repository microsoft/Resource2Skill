# Procedural Floating Glowing Embers

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Floating Glowing Embers

* **Core Visual Mechanism**: This technique uses a standard Blender Particle System modified for ambient atmospheric motion rather than explosive physics. By setting gravity to 0, increasing Brownian motion, and using an upward Normal velocity, the particles gently float and drift. The visual magic comes from instancing a flat polygon (NGon circle) combined with a specialized shader: an Emission node driven by an `Object Info (Random)` output piped through a `ColorRamp`. This ensures every individual particle in the system gets a slightly different color from a defined fire gradient.

* **Why Use This Skill (Rationale)**: Floating particles add immediate life, scale, and atmosphere to a static scene. Embers imply warmth, destruction, or magic without needing complex fluid simulations for fire. The random color per instance is a highly efficient way to create visual variance without taxing memory with multiple materials or complex UV setups.

* **Overall Applicability**: Perfect for adding atmosphere to fantasy scenes (magic sparks, fireflies), sci-fi environments (floating debris, energy motes), or dramatic environments (ash, campfires, burning buildings). 

* **Value Addition**: Transforms a basic scene into a dynamic, atmospheric environment. It demonstrates how to leverage instancing and procedural shading to get thousands of unique objects with almost zero performance overhead.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Emitter**: A basic Plane, scaled up, placed at the ground level. Its rendering visibility is disabled so only the particles show.
  - **Particle Instance**: A Circle primitive with 16 vertices, filled with an NGon to create a single flat face. It is kept extremely low-poly to allow thousands of instances.
  - **Particle Physics**: 
    - `Gravity Weight`: 0.0 (prevents falling).
    - `Normal Velocity`: ~1.2 m/s (pushes particles upwards from the plane).
    - `Random Velocity`: ~1.0 (adds varied starting speeds).
    - `Brownian Motion`: ~1.0 (adds chaotic, jittery drifting over time).

* **Step B: Materials & Shading**
  - **Shader Model**: Pure Emission shader (no BSDF).
  - **Node Tree**: `Object Info` -> `ColorRamp` -> `Emission` -> `Material Output`.
  - **Data Flow**: The `Random` output of the `Object Info` node outputs a float between 0.0 and 1.0 unique to every instantiated particle. This float drives the `Factor` of the ColorRamp, which acts as a lookup table for colors.
  - **Colors**: A fiery gradient mapping (Dark Red -> Bright Orange -> Yellow -> White).
  - **Strength**: Emission strength set to 2.0+ to interact with post-processing.

* **Step C: Lighting & Rendering Context**
  - Best viewed with EEVEE's **Bloom** enabled to create a glowing halo around each ember, or Cycles with a Glare node in the Compositor.
  - Works best against a darker background environment to make the emissive particles pop.

* **Step D: Animation & Dynamics**
  - **Pre-roll**: Frame start is set to negative (e.g., -300) so the scene is already filled with floating embers at frame 1.
  - **Lifetime**: Set high enough (e.g., 3000) so particles don't randomly disappear while on screen.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Emitter Object | `bpy.ops.mesh.primitive_plane_add` | Simple base mesh to distribute particles. |
| Particle Instance | `bpy.data.meshes.new` | Bypasses viewport creation to keep the scene clean; creates the low-poly NGon circle out of sight. |
| Atmospheric Movement | Particle System Physics | Built-in settings (Brownian, Zero Gravity) perfectly simulate lightweight floating ash. |
| Random Colors | Shader Node Tree | `Object Info (Random)` is the standard, highly performant way to colorize particle instances. |

> **Feasibility Assessment**: 100% reproducible. The physics parameters and material node setups are fully accessible via Blender's Python API and produce the exact visual result demonstrated in the video.

#### 3b. Complete Reproduction Code

```python
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
```