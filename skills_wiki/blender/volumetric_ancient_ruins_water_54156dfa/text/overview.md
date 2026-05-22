# Volumetric Ancient Ruins Water

## Analysis

Here is the extraction of the 3D modeling pattern and the reproducible bpy code based on the provided tutorial.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Volumetric Ancient Ruins Water

* **Core Visual Mechanism**: This technique uses a dual-component material to simulate realistic water. On the **Surface**, it mixes a bumb-mapped Glass BSDF with a Transparent BSDF using a "Light Path (Is Shadow Ray)" factor. This allows light to pass directly through the surface without casting opaque shadows. Inside the **Volume**, it uses a Volume Absorption node paired with a slight Emission (via Principled Volume) to create a sense of depth, where the water becomes darker and more richly colored the deeper it gets, while maintaining a slight ambient glow.
* **Why Use This Skill (Rationale)**: Default glass shaders often cast unrealistically dark shadows and lack depth. By explicitly managing the shadow rays and using volume absorption, this shader creates a highly physically accurate body of water. The applied scale ensures that the procedural noise ripples remain uniformly distributed rather than stretched.
* **Overall Applicability**: Perfect for architectural visualization, ancient ruins, pools, flooded scenes, and large bodies of water where seeing the ground beneath the water's surface is crucial for the composition.
* **Value Addition**: It transforms a simple stretched cube into a volumetric fluid body that realistically refracts light, absorbs color over distance, and interacts beautifully with environment lighting.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Geometry**: A simple default Cube primitive.
  - **Transformation**: Scaled widely on the X and Y axes, but squashed on the Z-axis to form a bounding volume for the water.
  - **Crucial Step**: The scale is applied (`Ctrl+A`) before shading. This is mandatory; otherwise, the procedural noise texture used for the ripples will stretch out, destroying the illusion of water.
* **Step B: Materials & Shading**
  - **Surface**: Mix Shader using `Light Path -> Is Shadow Ray`. 
    - True (Shadows): Transparent BSDF.
    - False (Camera/Reflections): Glass BSDF (IOR = 1.333).
  - **Ripples**: Noise Texture (Scale ~120) fed into a Bump Node (Strength ~0.05, Distance 1.0) into the Glass Normal.
  - **Volume**: An Add Shader combines `Volume Absorption` (Density 0.3, Teal color) and `Principled Volume` (Emission Strength 0.1, Teal color) to simulate deep water scattering and light absorption.
* **Step C: Lighting & Rendering Context**
  - Works best in **Cycles** to accurately calculate the glass refractions and volume absorption.
  - Requires a strong directional light source (like a Sun light with Strength 10.0) hitting the water at an angle to highlight the refractive ripples.
  - *Context Note*: Volume absorption is invisible if there is no geometry underneath the water. A "pool floor" must be present.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Water Volume | `bpy.ops.mesh.primitive_cube_add` | A basic bounding box is all that is required to hold volumetric shader data. |
| Surface Ripples | Procedural Shader Nodes (Noise + Bump) | Procedural noise provides infinite resolution without needing dense geometry or displacement modifiers. |
| Shadow Ray Hack | `ShaderNodeLightPath` | Prevents the glass from casting solid black shadows, essential for clear water pools. |

> **Feasibility Assessment**: 100% reproducible. The core technique is entirely shader-based and procedural, making it perfectly suited for precise reproduction via the Blender Python API.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "AncientRuinsWater",
    location: tuple = (0, 0, 0),
    scale: float = 10.0,
    material_color: tuple = (0.1, 0.7, 0.6),
    **kwargs,
) -> str:
    """
    Create a volumetric body of water using the Light Path Shadow hack and Volume Absorption.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the pool area.
        material_color: (R, G, B) water absorption color (teal/cyan by default).

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Pool Floor Context ===
    # Volume absorption needs a surface underneath to be visually apparent
    floor_z = location[2] - (scale * 0.2)
    bpy.ops.mesh.primitive_plane_add(size=scale*2.2, location=(location[0], location[1], floor_z))
    floor = bpy.context.active_object
    floor.name = f"{object_name}_Floor"
    
    floor_mat = bpy.data.materials.new(name=f"{object_name}_Floor_Mat")
    floor_mat.use_nodes = True
    if floor_mat.node_tree.nodes.get("Principled BSDF"):
        floor_mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.6, 0.5, 0.4, 1.0)
    floor.data.materials.append(floor_mat)

    # === Step 2: Create Water Volume Geometry ===
    bpy.ops.mesh.primitive_cube_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    
    # Scale to create a wide, flat body of water and APPLY scale (crucial for uniform noise)
    obj.scale = (scale, scale, scale * 0.2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # === Step 3: Build Water Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    # Eevee-specific settings for transparency (fallback, though Cycles is recommended)
    mat.blend_method = 'HASHED'
    mat.shadow_method = 'NONE'
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create Nodes
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)

    # --- Surface Shader Network ---
    mix_surface = nodes.new('ShaderNodeMixShader')
    mix_surface.location = (600, 200)

    light_path = nodes.new('ShaderNodeLightPath')
    light_path.location = (200, 400)

    glass = nodes.new('ShaderNodeBsdfGlass')
    glass.location = (200, 200)
    glass.inputs['IOR'].default_value = 1.33 # Water Index of Refraction
    
    transparent = nodes.new('ShaderNodeBsdfTransparent')
    transparent.location = (200, 0)

    bump = nodes.new('ShaderNodeBump')
    bump.location = (0, 100)
    bump.inputs['Strength'].default_value = 0.05
    bump.inputs['Distance'].default_value = 1.0

    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-200, 100)
    noise.inputs['Scale'].default_value = 120.0

    # --- Volume Shader Network ---
    add_vol = nodes.new('ShaderNodeAddShader')
    add_vol.location = (600, -200)

    vol_absorp = nodes.new('ShaderNodeVolumeAbsorption')
    vol_absorp.location = (400, -200)
    vol_absorp.inputs['Color'].default_value = (*material_color, 1.0)
    vol_absorp.inputs['Density'].default_value = 0.3

    prin_vol = nodes.new('ShaderNodeVolumePrincipled')
    prin_vol.location = (400, -400)
    prin_vol.inputs['Color'].default_value = (*material_color, 1.0)
    
    # Safely handle Blender API changes for Emission in Principled Volume
    if 'Emission Color' in prin_vol.inputs:
        prin_vol.inputs['Emission Color'].default_value = (*material_color, 1.0)
    elif 'Emission' in prin_vol.inputs:
        prin_vol.inputs['Emission'].default_value = (*material_color, 1.0)
        
    if 'Emission Strength' in prin_vol.inputs:
        prin_vol.inputs['Emission Strength'].default_value = 0.1

    # --- Connect the Graph ---
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], glass.inputs['Normal'])
    
    # Shadow Ray Hack: If shadow ray (1), use Transparent. If not (0), use Glass.
    links.new(light_path.outputs['Is Shadow Ray'], mix_surface.inputs['Fac'])
    links.new(glass.outputs['BSDF'], mix_surface.inputs[1])      
    links.new(transparent.outputs['BSDF'], mix_surface.inputs[2]) 
    links.new(mix_surface.outputs['Shader'], output.inputs['Surface'])

    # Volumes combined
    links.new(vol_absorp.outputs['Volume'], add_vol.inputs[0])
    links.new(prin_vol.outputs['Volume'], add_vol.inputs[1])
    links.new(add_vol.outputs['Shader'], output.inputs['Volume'])

    # Assign Material
    obj.data.materials.append(mat)

    # === Step 4: Environment Context ===
    # Add a Sun light to ensure the glass ripples refract properly
    sun = bpy.data.lights.new(name=f"{object_name}_Sun", type='SUN')
    sun.energy = 10.0
    sun.angle = math.radians(2.0)
    sun_obj = bpy.data.objects.new(name=f"{object_name}_SunObj", object_data=sun)
    scene.collection.objects.link(sun_obj)
    sun_obj.location = (location[0], location[1], location[2] + 10)
    sun_obj.rotation_euler = (math.radians(45), math.radians(30), math.radians(45))

    return f"Created '{object_name}' with volumetric water shader, pool floor, and sun light at {location}"
```