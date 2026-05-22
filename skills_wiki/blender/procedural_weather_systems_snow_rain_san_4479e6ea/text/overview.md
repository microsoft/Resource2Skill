# Procedural Weather Systems (Snow, Rain, Sandstorm)

## Analysis

Here is the strategy document and reproducible code for the procedural weather effects pattern.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Weather Systems (Snow, Rain, Sandstorm)

* **Core Visual Mechanism**: This technique uses a single particle emitter plane combined with physics force fields (Wind, Turbulence) to simulate chaotic, organic weather elements. The defining signature is the procedural variation: by swapping the instanced particle mesh (deformed icospheres vs. stretched droplets) and tweaking physical parameters (gravity weight, velocity, turbulence scale), the exact same setup seamlessly transitions between a gentle snowfall, a driving rainstorm, or a sweeping desert sandstorm.
* **Why Use This Skill (Rationale)**: Static scenes often feel lifeless. Introducing atmospheric movement instantly conveys scale, mood, and environmental context. Procedural physics simulation ensures the movement feels natural and chaotic without requiring tedious manual keyframing.
* **Overall Applicability**: Cinematic environment renders, background atmosphere for architectural or character visualization, and establishing shots.
* **Value Addition**: Transforms a static 3D layout into a dynamic environment. The heavy lifting is done by Blender's built-in physics engine, allowing you to "art direct" the weather by simply adjusting sliders for wind and turbulence.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Emitter**: A scaled-up plane placed above the camera frustum.
  - **Snowflakes**: Low-poly icospheres with randomized vertex offsets (via BMesh) to create irregular clump shapes.
  - **Raindrops**: An icosphere severely scaled along the Y-axis to form a long streak, mimicking motion-blurred water.
  - **Sand Grains**: Tiny, unmodified low-poly icospheres multiplied via Interpolated Children to create massive volume.
* **Step B: Materials & Shading**
  - **Snow**: High roughness white Principled BSDF.
  - **Rain**: A custom mixed shader. It blends a Transparent BSDF and a Glossy BSDF, then mixes in a white Emission shader driven by a Fresnel node. This edge-glow ensures the thin rain streaks remain visible against dark backgrounds.
  - **Sand**: A simple matte orange/brown Principled BSDF.
* **Step C: Lighting & Rendering Context**
  - Requires **Motion Blur** to visually sell the effect (stretching fast-moving particles into streaks).
  - For EEVEE, **Bloom** should be enabled so the rain's emission material produces a slight atmospheric glow.
* **Step D: Animation & Dynamics**
  - The particle system uses a **negative start frame** (e.g., `-200`). This "pre-rolls" the simulation so the weather is already fully falling through the scene when the animation begins at frame 1.
  - **Force Fields**: A Wind field pushes particles directionally, while a Turbulence field adds organic swirling. Sand requires massive turbulence size/strength to mimic sweeping dunes, while snow requires smaller, jittery turbulence.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Emitter & Particles | `bpy.ops.mesh.primitive_plane_add` + `PARTICLE_SYSTEM` modifier | Core mechanism for spawning and gravity-based falling. |
| Organic Swirling | `bpy.ops.object.effector_add` (Wind, Turbulence) | Applies procedural physics to the particles dynamically. |
| Rain Visibility | Custom Node Tree (Glass + Emission + Fresnel) | Guarantees rain is visible regardless of environment lighting. |
| Instanced Meshes | `bmesh` randomization + Particle `COLLECTION` render | Infinite variety of snowflake shapes without manual modeling. |

> **Feasibility Assessment**: 100% reproducible. The tutorial relies entirely on standard Blender physics and node systems, which map perfectly to the Python API. 

#### 3b. Complete Reproduction Code

```python
def create_weather_system(
    scene_name: str = "Scene",
    object_name: str = "WeatherSystem",
    location: tuple = (0.0, 0.0, 15.0),
    scale: float = 20.0,
    weather_type: str = "SNOW",  # Choose from: "SNOW", "RAIN", "SANDSTORM"
    **kwargs
) -> str:
    """
    Creates a procedural weather particle system (Snow, Rain, or Sandstorm).
    
    Args:
        scene_name: Target scene.
        object_name: Base name for the emitter and components.
        location: (x,y,z) position for the emitter plane (place high above scene).
        scale: Size multiplier for the emitter plane.
        weather_type: The type of weather to generate ("SNOW", "RAIN", "SANDSTORM").
        **kwargs: Additional overrides.
        
    Returns:
        Status string confirming creation.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    weather_type = weather_type.upper()
    if weather_type not in ["SNOW", "RAIN", "SANDSTORM"]:
        weather_type = "SNOW"

    # === Step 1: Create Instance Collection ===
    coll_name = f"{object_name}_{weather_type}_Instances"
    inst_coll = bpy.data.collections.new(coll_name)
    scene.collection.children.link(inst_coll)

    # === Step 2: Create Materials & Particle Instances ===
    if weather_type == "SNOW":
        mat = bpy.data.materials.new(f"{object_name}_SnowMat")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0) # White
            bsdf.inputs['Roughness'].default_value = 0.9

        # Create 3 slightly deformed icospheres for variety
        for i in range(3):
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, location=(0,0,-100))
            flake = bpy.context.active_object
            flake.name = f"{object_name}_Flake_{i}"
            
            # Randomize vertices using BMesh
            bm = bmesh.new()
            bm.from_mesh(flake.data)
            for v in bm.verts:
                v.co += Vector((
                    random.uniform(-0.2, 0.2), 
                    random.uniform(-0.2, 0.2), 
                    random.uniform(-0.2, 0.2)
                ))
            bm.to_mesh(flake.data)
            bm.free()
            
            bpy.ops.object.shade_smooth()
            flake.data.materials.append(mat)
            
            for c in flake.users_collection:
                c.objects.unlink(flake)
            inst_coll.objects.link(flake)

    elif weather_type == "RAIN":
        mat = bpy.data.materials.new(f"{object_name}_RainMat")
        mat.use_nodes = True
        mat.blend_method = 'BLEND'
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        # Shader Network: (Glossy + Transp) mixed with (Emission) via Fresnel
        out = nodes.new('ShaderNodeOutputMaterial')
        mix1 = nodes.new('ShaderNodeMixShader')
        glossy = nodes.new('ShaderNodeBsdfGlossy')
        glossy.inputs['Roughness'].default_value = 0.0
        transp = nodes.new('ShaderNodeBsdfTransparent')
        
        mix2 = nodes.new('ShaderNodeMixShader')
        emission = nodes.new('ShaderNodeEmission')
        emission.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
        emission.inputs['Strength'].default_value = 2.0
        
        fresnel = nodes.new('ShaderNodeFresnel')
        fresnel.inputs['IOR'].default_value = 1.33
        math_node = nodes.new('ShaderNodeMath')
        math_node.operation = 'MULTIPLY'
        math_node.inputs[1].default_value = 0.5
        
        links.new(glossy.outputs[0], mix1.inputs[1])
        links.new(transp.outputs[0], mix1.inputs[2])
        links.new(mix1.outputs[0], mix2.inputs[1])
        links.new(emission.outputs[0], mix2.inputs[2])
        links.new(fresnel.outputs[0], math_node.inputs[0])
        links.new(math_node.outputs[0], mix2.inputs[0])
        links.new(mix2.outputs[0], out.inputs['Surface'])
        
        # Stretched Teardrop Mesh
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, location=(0,0,-100))
        drop = bpy.context.active_object
        drop.name = f"{object_name}_Drop"
        drop.scale = (0.05, 0.4, 0.05) # Stretched along Y axis for velocity alignment
        bpy.ops.object.transform_apply(scale=True)
        bpy.ops.object.shade_smooth()
        drop.data.materials.append(mat)
        
        for c in drop.users_collection:
            c.objects.unlink(drop)
        inst_coll.objects.link(drop)

    elif weather_type == "SANDSTORM":
        mat = bpy.data.materials.new(f"{object_name}_SandMat")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs[0].default_value = (0.7, 0.35, 0.1, 1.0) # Dusty orange/brown
            bsdf.inputs['Roughness'].default_value = 0.95
            
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, location=(0,0,-100))
        sand = bpy.context.active_object
        sand.name = f"{object_name}_Grain"
        bpy.ops.object.shade_smooth()
        sand.data.materials.append(mat)
        
        for c in sand.users_collection:
            c.objects.unlink(sand)
        inst_coll.objects.link(sand)

    # Hide the instances collection from view layer
    def exclude_collection(col_name, layer_col):
        if layer_col.name == col_name:
            layer_col.exclude = True
            return True
        for child in layer_col.children:
            if exclude_collection(col_name, child):
                return True
        return False
    exclude_collection(inst_coll.name, bpy.context.view_layer.layer_collection)

    # === Step 3: Create Emitter Plane ===
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=location)
    emitter = bpy.context.active_object
    emitter.name = object_name
    emitter.scale = (scale, scale, scale)
    bpy.ops.object.transform_apply(scale=True)
    
    # Hide emitter from render and viewport
    emitter.show_instancer_for_viewport = False
    emitter.show_instancer_for_render = False

    # === Step 4: Configure Particle System ===
    ps_mod = emitter.modifiers.new(name="WeatherParticles", type='PARTICLE_SYSTEM')
    ps = emitter.particle_systems[0]
    p_set = ps.settings
    
    p_set.type = 'EMITTER'
    p_set.frame_start = -200  # Pre-roll simulation
    p_set.frame_end = 250
    p_set.lifetime = 500
    p_set.render_type = 'COLLECTION'
    p_set.instance_collection = inst_coll

    # Base physics setup
    bpy.ops.object.effector_add(type='WIND', location=location)
    wind = bpy.context.active_object
    wind.name = f"{object_name}_Wind"
    wind.parent = emitter

    bpy.ops.object.effector_add(type='TURBULENCE', location=location)
    turb = bpy.context.active_object
    turb.name = f"{object_name}_Turbulence"
    turb.parent = emitter

    # Type-Specific Parameters
    if weather_type == "SNOW":
        p_set.count = 2000
        p_set.normal_factor = 0.0
        p_set.factor_random = 0.5
        p_set.particle_size = 0.1
        p_set.size_random = 0.8
        p_set.effector_weights.gravity = 0.05
        
        wind.field.strength = 1.5
        wind.rotation_euler = (0, math.radians(90), 0)
        turb.field.strength = 6.0
        turb.field.size = 1.0

    elif weather_type == "RAIN":
        p_set.count = 10000
        p_set.normal_factor = -2.0  # Force downwards
        p_set.factor_random = 0.0
        p_set.particle_size = 0.5
        p_set.size_random = 0.4
        p_set.effector_weights.gravity = 1.0
        
        p_set.use_rotations = True
        p_set.rotation_mode = 'VEL'
        p_set.use_dynamic_rotation = True
        
        wind.field.strength = 2.0
        wind.rotation_euler = (0, math.radians(10), 0)
        turb.field.strength = 1.0
        turb.field.size = 1.0

    elif weather_type == "SANDSTORM":
        p_set.count = 10000
        p_set.normal_factor = 0.0
        p_set.factor_random = 0.5
        p_set.particle_size = 0.02
        p_set.size_random = 0.8
        p_set.effector_weights.gravity = 0.05
        
        # Use children for massive particle counts
        p_set.child_type = 'INTERPOLATED'
        p_set.child_nbr = 5
        p_set.rendered_child_count = 5
        p_set.child_radius = 0.4
        
        wind.field.strength = 30.0
        wind.rotation_euler = (0, math.radians(90), 0) # Blow sideways
        turb.field.strength = 60.0
        turb.field.size = 10.0 # Large sweeping gusts

    # === Step 5: Render Engine Requirements ===
    scene.render.use_motion_blur = True
    if hasattr(scene, "eevee") and hasattr(scene.eevee, "use_bloom"):
        scene.eevee.use_bloom = True

    return f"Created {weather_type} system '{object_name}' at {location} with pre-rolled simulation."
```