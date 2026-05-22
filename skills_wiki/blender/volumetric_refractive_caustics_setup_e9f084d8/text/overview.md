# Volumetric Refractive Caustics Setup

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Volumetric Refractive Caustics Setup

* **Core Visual Mechanism**: The physical simulation of light rays passing through a refractive medium (like glass or water) and subsequently scattering through a particulate volume (fog, smoke, or oceanic depths). This creates complex, patterned 3D light shafts (god rays) that bend and focus based on the geometry of the refractive object.
* **Why Use This Skill (Rationale)**: Standard volumetric lighting produces uniform, straight light shafts. Volumetric caustics project the optical distortion of an object into the air itself. This dramatically enhances realism, atmosphere, and cinematic quality, providing a strong sense of spatial depth and physical light interaction.
* **Overall Applicability**: Cinematic underwater environments (sunlight focusing through waves), product visualization for glass/jewelry, moody sci-fi or magical scenes where glowing crystals cast intricate light patterns into a foggy room.
* **Value Addition**: Transforms a flat, basic lighting setup into a rich, atmospheric scene by leveraging modern path-tracing capabilities. It provides a ready-to-use domain and lighting rig optimized for a notoriously difficult rendering effect.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Receiver**: A simple floor plane marked to receive shadow caustics.
  - **Caster**: A moderately dense mesh (Suzanne with Level 2 Subdivision Surface) to bend the light rays smoothly. Marked to cast shadow caustics.
  - **Domain**: A non-rendering wireframe bounding box that contains the volumetric media.
* **Step B: Materials & Shading**
  - **Glass Caster**: `Principled BSDF` (Transmission = 1.0) or `Glass BSDF` with an IOR of 1.45 and very low roughness (0.02) to ensure sharp caustic patterns.
  - **Volume Domain**: `Volume Scatter` shader. Density is kept low (e.g., 0.1) to allow light to penetrate. 
  - **Anisotropy (Henyey-Greenstein)**: The `g` parameter is exposed. `0` = isotropic (even scatter), `>0` = forward scattering (light punches through), `<0` = backward scattering (light bounces back toward the source).
  - **Inhomogeneous Volume**: Optional procedural `Noise Texture` piped through a `ColorRamp` into the density to simulate uneven fog/smoke.
* **Step C: Lighting & Rendering Context**
  - **Light Source**: A highly energetic `Spot Light` (e.g., 50,000W) focused directly on the glass object. It must be powerful enough to survive both refraction and volumetric scattering.
  - **Render Engine**: **Cycles is mandatory**. Path tracing is required to calculate the light bounces. Modern Blender (3.2+) "Shadow Caustics" properties are toggled via the API to drastically speed up convergence.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Base Scene Rig** | `bpy.ops.mesh.primitive_*_add` | Quickly establishes the required floor-object-light spatial relationship. |
| **Material Setup** | Shader Node Tree | Direct control over BSDF parameters and procedurally linking noise to volume density. |
| **Caustics Optimization** | `obj.cycles` API properties | Tracing volumetric caustics is extremely noisy. Enabling MNEE (Manifold Next Event Estimation) caustics in Cycles makes it viable. |

> **Feasibility Assessment**: 85%. While Blender's standard Cycles engine can reproduce the *look* of the interactive volume caustics shown in the specialized academic paper, standard path tracing is slightly slower and noisier than their custom single-scattering algorithm. The code builds the exact physical setup required.

#### 3b. Complete Reproduction Code

```python
def create_volumetric_caustics_setup(
    scene_name: str = "Scene",
    base_name: str = "VolCaustics",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    glass_color: tuple = (0.8, 0.9, 1.0),
    volume_density: float = 0.05,
    anisotropy: float = 0.7,
    **kwargs
) -> str:
    """
    Create a Volumetric Caustics lighting rig in the active Blender scene.
    Requires Cycles render engine to view the effect.

    Args:
        scene_name: Name of the target scene.
        base_name: Prefix for created objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the entire rig.
        glass_color: (R, G, B) base color of the refractive object.
        volume_density: Density of the volumetric fog.
        anisotropy: Henyey-Greenstein g-value (-1.0 to 1.0).
        **kwargs: 
            use_inhomogeneous_volume (bool): Add procedural noise to the fog.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    
    # Force Cycles as it is required for volumetric caustics
    scene.render.engine = 'CYCLES'
    
    base_loc = Vector(location)
    
    # --- 1. Floor (Caustics Receiver) ---
    bpy.ops.mesh.primitive_plane_add(size=10*scale, location=base_loc)
    floor = bpy.context.active_object
    floor.name = f"{base_name}_Floor"
    
    # Enable shadow caustics receiver (Blender 3.2+)
    try:
        floor.cycles.is_caustics_receiver = True
    except AttributeError:
        pass
        
    mat_floor = bpy.data.materials.new(name=f"{base_name}_FloorMat")
    mat_floor.use_nodes = True
    mat_floor.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.05, 0.05, 0.05, 1)
    mat_floor.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.8
    floor.data.materials.append(mat_floor)
    
    # --- 2. Refractive Object (Caustics Caster) ---
    monkey_loc = base_loc + Vector((0, 0, 1.5 * scale))
    bpy.ops.mesh.primitive_monkey_add(size=1.5*scale, location=monkey_loc)
    monkey = bpy.context.active_object
    monkey.name = f"{base_name}_RefractiveMonkey"
    
    bpy.ops.object.modifier_add(type='SUBSURF')
    monkey.modifiers["Subdivision"].levels = 2
    monkey.modifiers["Subdivision"].render_levels = 3
    bpy.ops.object.shade_smooth()
    
    # Enable shadow caustics caster (Blender 3.2+)
    try:
        monkey.cycles.is_caustics_caster = True
    except AttributeError:
        pass
        
    mat_glass = bpy.data.materials.new(name=f"{base_name}_GlassMat")
    mat_glass.use_nodes = True
    nodes = mat_glass.node_tree.nodes
    links = mat_glass.node_tree.links
    nodes.clear()
    
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = (400, 0)
    
    node_glass = nodes.new(type='ShaderNodeBsdfGlass')
    node_glass.location = (200, 0)
    node_glass.inputs["Color"].default_value = (*glass_color, 1.0)
    node_glass.inputs["IOR"].default_value = 1.45
    node_glass.inputs["Roughness"].default_value = 0.01  # Keep low for sharp caustics
    
    links.new(node_glass.outputs[0], node_output.inputs[0])
    monkey.data.materials.append(mat_glass)
    
    # --- 3. Light Source ---
    light_loc = base_loc + Vector((0, -4 * scale, 5 * scale))
    bpy.ops.object.light_add(type='SPOT', location=light_loc)
    light_obj = bpy.context.active_object
    light_obj.name = f"{base_name}_SpotLight"
    
    # Aim light at the monkey
    direction = monkey_loc - light_loc
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    
    light = light_obj.data
    light.energy = 100000 * (scale ** 2)  # Extreme energy needed to penetrate volume and glass
    light.spot_size = math.radians(35)
    light.spot_blend = 0.2
    light.shadow_soft_size = 0.05 * scale # Small radius for sharper caustics
    
    # Enable shadow caustics on light (Blender 3.2+)
    try:
        light.cycles.cast_shadow_caustics = True
    except AttributeError:
        pass
        
    # --- 4. Volumetric Domain ---
    bpy.ops.mesh.primitive_cube_add(size=12*scale, location=base_loc + Vector((0,0,3*scale)))
    volume_box = bpy.context.active_object
    volume_box.name = f"{base_name}_VolumeDomain"
    volume_box.display_type = 'WIRE'
    
    mat_vol = bpy.data.materials.new(name=f"{base_name}_VolumeMat")
    mat_vol.use_nodes = True
    nodes = mat_vol.node_tree.nodes
    links = mat_vol.node_tree.links
    nodes.clear()
    
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = (400, 0)
    
    node_scatter = nodes.new(type='ShaderNodeVolumeScatter')
    node_scatter.location = (200, 0)
    node_scatter.inputs["Anisotropy"].default_value = anisotropy
    
    if kwargs.get('use_inhomogeneous_volume', False):
        node_noise = nodes.new(type='ShaderNodeTexNoise')
        node_noise.location = (-400, 0)
        node_noise.inputs["Scale"].default_value = 2.0 / scale
        
        node_ramp = nodes.new(type='ShaderNodeValToRGB')
        node_ramp.location = (-200, 0)
        node_ramp.color_ramp.elements[0].position = 0.3
        node_ramp.color_ramp.elements[1].position = 0.7
        
        node_math = nodes.new(type='ShaderNodeMath')
        node_math.operation = 'MULTIPLY'
        node_math.location = (0, 0)
        node_math.inputs[1].default_value = volume_density * 3.0 
        
        links.new(node_noise.outputs["Fac"], node_ramp.inputs[0])
        links.new(node_ramp.outputs[0], node_math.inputs[0])
        links.new(node_math.outputs[0], node_scatter.inputs["Density"])
    else:
        node_scatter.inputs["Density"].default_value = volume_density
        
    links.new(node_scatter.outputs[0], node_output.inputs[1]) # Link to Volume socket
    volume_box.data.materials.append(mat_vol)
    
    # --- 5. Hierarchy Organization ---
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=base_loc)
    parent = bpy.context.active_object
    parent.name = f"{base_name}_Root"
    
    for obj in [floor, monkey, light_obj, volume_box]:
        obj.parent = parent
        
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')
        
    return f"Created Volumetric Caustics rig '{parent.name}' at {location}. Note: Render engine must be set to CYCLES."
```