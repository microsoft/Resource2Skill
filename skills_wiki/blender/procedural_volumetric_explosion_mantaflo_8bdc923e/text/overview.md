# Procedural Volumetric Explosion (Mantaflow)

## Analysis

# 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Volumetric Explosion (Mantaflow)

* **Core Visual Mechanism**: This technique uses rapid, high-velocity particle systems as invisible "inflow" sources for a Mantaflow fluid simulation. The distinct shape of the explosion (a mushroom cloud with rolling ground smoke) is achieved by emitting particles from multiple custom-shaped meshes: upward from a displaced hemisphere and downward from an inverted circle against a collision plane. A custom `Principled Volume` shader converts the simulation's `flame` and `density` attributes into vivid, emissive fire and thick smoke.

* **Why Use This Skill (Rationale)**: Volumetric explosions provide true 3D depth, self-shadowing, and physical interactions with scene lighting that flat 2D cards or simple meshes cannot match. By driving the fluid with particles, the user gains exact control over the timing, direction, and shape of the blast before the fluid solver takes over to add natural turbulence and rolling details.

* **Overall Applicability**: Essential for VFX, action-oriented animation, and high-fidelity environment destruction. It serves perfectly as a hero visual effect in cinematic scenes, vehicle crashes, or sci-fi combat visualizations.

* **Value Addition**: Transforms a basic scene by introducing dynamic, physically simulated pyrotechnics. It adds critical atmospheric depth and acts as an intense, dynamic light source that grounds the action in the scene's lighting environment.

# 2. Technical Breakdown

* **Step A: Geometry & Topology**
  * **Emitters**:
    * **Hemispheres**: Two Icospheres (Subdivision 3) with their bottom halves removed via `bmesh`. Displaced using a Procedural Cloud texture to prevent perfectly spherical uniform emission.
    * **Downward Blast**: A filled circle rotated 180 degrees to shoot particles downwards.
  * **Collider**: A flat plane acting as the ground, giving the downward blast a surface to roll outward from.
  * **Domain**: A large bounding box Cube encapsulating the entire explosion area.

* **Step B: Materials & Shading**
  * **Shader Model**: `Principled Volume` applied solely to the Domain object (the emitters are hidden from render).
  * **Attributes**:
    * The `density` attribute is multiplied by a high value (e.g., 30) to make the smoke highly opaque.
    * The `flame` attribute drives the emission via a ColorRamp, creating the gradient of cooling fire.
  * **ColorRamp Values**:
    * Pos 0.0: Black `(0.0, 0.0, 0.0)`
    * Pos 0.3: Dark Red `(0.4, 0.05, 0.0)`
    * Pos 0.6: Orange `(1.0, 0.4, 0.05)`
    * Pos 1.0: Bright Yellow/White `(1.0, 0.9, 0.5)`
  * **Emission**: The flame attribute is also multiplied by a high factor (e.g., 50.0) and fed into `Emission Strength`.

* **Step C: Lighting & Rendering Context**
  * Since the explosion is heavily emissive, it acts as a primary light source.
  * **Render Engine**: Works beautifully in Cycles (true volume scattering/bounces) and EEVEE (requires Volumetric Shadows and a small Tile Size like 2px to resolve the fire detail).

* **Step D: Animation & Dynamics**
  * **Particle Systems**: Bursts lasting only 5 frames (e.g., Frame 10-15) with high normal velocity (`4.0 - 7.0`) to establish the initial blast shape.
  * **Mantaflow Settings**: Domain set to `GAS`. Adaptive Domain enabled. Noise enabled for extra detail. Dissolve Fire Reaction Speed set to `0.4` for lingering flames. Cache set to `REPLAY` so it automatically calculates when the timeline plays.

# 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Emitter Shapes | `bpy.ops.mesh.primitive` + `bmesh` | Efficiently cuts the icosphere in half via Python to direct the upward blast exactly as shown. |
| Blast Velocity | Particle Systems | Translates the face normals of the custom shapes into rapid, directional initial velocity for the fluid solver. |
| Volumetrics | Mantaflow Modifiers (`FLUID`) | The native, physically-based way to simulate convective fire and rolling smoke. |
| Shading | Shader Node Tree | Crucial for intercepting Mantaflow attributes (`flame`, `density`) to map custom colors and opacity levels. |

> **Feasibility Assessment**: 95%. The Python script fully replicates the meshes, the particle logic, the physics modifiers, and the material nodes. Because Mantaflow caches dynamically, the python script cannot instantly show the final frame — the user (or automated agent) *must* play the timeline (Spacebar) from Frame 1 to generate the fluid cache.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "VolumetricExplosion",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (1.0, 0.4, 0.05), # Base orange/red fire tint
    **kwargs,
) -> str:
    """
    Create a Mantaflow Volumetric Explosion in the active Blender scene.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) tint for the fire emission.
        
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector
    
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    bpy.context.window.scene = scene
    
    # Ensure start frame is 1 to catch the simulation
    scene.frame_start = 1
    scene.frame_set(1)

    # Root Empty for easy moving
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    root = bpy.context.active_object
    root.name = object_name
    root.scale = (scale, scale, scale)

    emitters = []

    # === Helper to create Hemisphere Emitters ===
    def create_hemisphere(name, start_frame, end_frame):
        bpy.ops.mesh.primitive_icosphere_add(subdivisions=3, radius=1.0)
        hemi = bpy.context.active_object
        hemi.name = name
        
        # Delete bottom half using bmesh
        bm = bmesh.new()
        bm.from_mesh(hemi.data)
        verts_to_delete = [v for v in bm.verts if v.co.z < 0]
        bmesh.ops.delete(bm, geom=verts_to_delete, context='VERTS')
        bm.to_mesh(hemi.data)
        bm.free()
        
        # Add slight displacement for randomness
        disp_tex = bpy.data.textures.new(f"{name}_Tex", 'CLOUDS')
        disp_tex.noise_scale = 0.5
        disp_mod = hemi.modifiers.new("Displace", 'DISPLACE')
        disp_mod.texture = disp_tex
        disp_mod.strength = 0.4
        
        # Add Particle System
        hemi.modifiers.new("Particles", 'PARTICLE_SYSTEM')
        psys = hemi.particle_systems[0]
        pset = psys.settings
        pset.count = 5000
        pset.frame_start = start_frame
        pset.frame_end = end_frame
        pset.lifetime = 5
        pset.normal_factor = 4.0
        pset.factor_random = 1.0
        
        hemi.parent = root
        hemi.hide_render = True
        hemi.hide_viewport = True
        return hemi

    # 1. Main upward blast
    emitters.append(create_hemisphere(f"{object_name}_Emi_Up1", 10, 15))
    
    # 2. Secondary upward blast (delayed, rotated)
    emi2 = create_hemisphere(f"{object_name}_Emi_Up2", 13, 17)
    emi2.rotation_euler = (0.5, 0.5, 1.0)
    emitters.append(emi2)

    # 3. Downward ground blast
    bpy.ops.mesh.primitive_circle_add(vertices=32, radius=1.5, fill_type='NGON')
    emi3 = bpy.context.active_object
    emi3.name = f"{object_name}_Emi_Down"
    emi3.rotation_euler[1] = math.pi # Point normals straight down
    emi3.location.z = 0.5
    
    emi3.modifiers.new("Particles", 'PARTICLE_SYSTEM')
    psys3 = emi3.particle_systems[0]
    pset3 = psys3.settings
    pset3.count = 4000
    pset3.frame_start = 11
    pset3.frame_end = 16
    pset3.lifetime = 5
    pset3.normal_factor = 6.0 # Shoot down fast
    
    emi3.parent = root
    emi3.hide_render = True
    emi3.hide_viewport = True
    emitters.append(emi3)

    # === Configure Emitters for Mantaflow Inflow ===
    for e in emitters:
        fmod = e.modifiers.new("FluidFlow", 'FLUID')
        fmod.fluid_type = 'FLOW'
        fmod.flow_settings.flow_type = 'BOTH' # Fire + Smoke
        fmod.flow_settings.flow_behavior = 'INFLOW'
        fmod.flow_settings.flow_source = 'PARTICLES'
        fmod.flow_settings.particle_system = e.particle_systems[0]
        fmod.flow_settings.use_initial_velocity = True
        if hasattr(fmod.flow_settings, 'velocity_factor'):
            fmod.flow_settings.velocity_factor = 3.0

    # === Ground Collider ===
    bpy.ops.mesh.primitive_plane_add(size=15.0)
    ground = bpy.context.active_object
    ground.name = f"{object_name}_Collider"
    cmod = ground.modifiers.new("FluidCollision", 'FLUID')
    cmod.fluid_type = 'EFFECTOR'
    cmod.effector_settings.effector_type = 'COLLISION'
    ground.parent = root
    ground.hide_render = True

    # === Fluid Domain ===
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    domain = bpy.context.active_object
    domain.name = f"{object_name}_Domain"
    domain.scale = (12, 12, 16)
    domain.location = (0, 0, 7) # Shift up to encompass explosion
    
    dmod = domain.modifiers.new("FluidDomain", 'FLUID')
    dmod.fluid_type = 'DOMAIN'
    dmod.domain_settings.domain_type = 'GAS'
    # 64 is fast for preview. Increase to 128-256 for final render quality.
    dmod.domain_settings.resolution_max = 64 
    dmod.domain_settings.use_adaptive_domain = True
    dmod.domain_settings.use_noise = True
    
    # Configure Fire Reaction
    if hasattr(dmod.domain_settings, 'fire_reaction_speed'):
        dmod.domain_settings.fire_reaction_speed = 0.4
        
    dmod.domain_settings.cache_type = 'REPLAY' # Allows playback to cache dynamically
    domain.parent = root

    # === Volumetric Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_VolumeMat")
    mat.use_nodes = True
    tree = mat.node_tree
    tree.nodes.clear()

    output = tree.nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    vol = tree.nodes.new('ShaderNodeVolumePrincipled')
    vol.location = (100, 0)
    
    # Density manipulation
    dens_attr = tree.nodes.new('ShaderNodeAttribute')
    dens_attr.attribute_name = "density"
    dens_attr.location = (-400, 100)
    
    dens_math = tree.nodes.new('ShaderNodeMath')
    dens_math.operation = 'MULTIPLY'
    dens_math.inputs[1].default_value = 30.0 # Thicken smoke
    dens_math.location = (-200, 100)
    
    # Flame manipulation
    flame_attr = tree.nodes.new('ShaderNodeAttribute')
    flame_attr.attribute_name = "flame"
    flame_attr.location = (-400, -100)
    
    cramp = tree.nodes.new('ShaderNodeValToRGB')
    cramp.location = (-200, -100)
    
    # Setup color stops
    cramp.color_ramp.elements[0].position = 0.0
    cramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    
    el1 = cramp.color_ramp.elements.new(0.15)
    el1.color = (material_color[0]*0.4, material_color[1]*0.05, material_color[2]*0.0, 1.0)
    
    el2 = cramp.color_ramp.elements.new(0.5)
    el2.color = (material_color[0], material_color[1], material_color[2], 1.0)
    
    cramp.color_ramp.elements[-1].position = 1.0
    cramp.color_ramp.elements[-1].color = (1.0, 0.9, 0.6, 1.0) # Hot core
    
    emis_math = tree.nodes.new('ShaderNodeMath')
    emis_math.operation = 'MULTIPLY'
    emis_math.inputs[1].default_value = 80.0 # Brightness multiplier
    emis_math.location = (-200, -350)
    
    # Link Nodes
    tree.links.new(dens_attr.outputs['Fac'], dens_math.inputs[0])
    tree.links.new(dens_math.outputs['Value'], vol.inputs['Density'])
    
    tree.links.new(flame_attr.outputs['Fac'], cramp.inputs['Fac'])
    tree.links.new(cramp.outputs['Color'], vol.inputs['Emission Color'])
    
    tree.links.new(flame_attr.outputs['Fac'], emis_math.inputs[0])
    tree.links.new(emis_math.outputs['Value'], vol.inputs['Emission Strength'])
    
    tree.links.new(vol.outputs['Volume'], output.inputs['Volume'])
    
    domain.data.materials.append(mat)

    return f"Created Volumetric Explosion '{object_name}' at {location}. **NOTE: Press Play (Spacebar) from Frame 1 to let Mantaflow simulate and build the explosion!**"
```