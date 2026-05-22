# Advanced HDRI Environment Lighting & Compositing

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Advanced HDRI Environment Lighting & Compositing

* **Core Visual Mechanism**: Image-based lighting (IBL) using an equirectangular HDRI map to provide 360-degree, physically accurate illumination and reflections. The core signature of this technique is the presence of rich, multi-colored reflections and soft, realistic ambient shadows that ground objects in a believable space.

* **Why Use This Skill (Rationale)**: Default 3D lighting often looks artificial and sterile. Using an HDRI instantly provides a complex array of light sources, color temperatures, and bounce light captured from the real world. It is the fastest and most effective way to achieve photorealism, especially when working with highly reflective materials like metals or glass.

* **Overall Applicability**: Essential for almost all realistic renders, product visualizations, architectural visualizations, and look-development (lookdev). It serves as the base lighting layer, upon which additional local lights can be added. 

* **Value Addition**: Replaces the default uniform gray background with a high-dynamic-range light source. By incorporating a node-based control system (Mapping, HSV, RGB Curves) and Film Transparency, it allows the user to harness the realistic light while completely customizing the background visibility, contrast, and color tint.


### 2. Technical Breakdown

* **Step A: Environment Mapping**
  - **Node Setup**: An `Environment Texture` node is used instead of a standard `Image Texture`.
  - **Coordinates**: A `Texture Coordinate` node (Generated) is passed through a `Mapping` node. This allows the Z-rotation parameter to act as a "turntable" for the sky, altering the direction of the dominant light source (like the sun) without rotating the 3D objects.

* **Step B: Color Correction & Control**
  - **Hue/Saturation/Value (HSV)**: Placed after the Environment Texture to control overall brightness (Value), remove color casts (lowering Saturation to create pure white/grey light), or tint the lighting environment (Hue).
  - **RGB Curves**: Used to adjust the contrast of the HDRI. Boosting the highlights and crushing the darks in the RGB curve creates sharper, more dramatic shadows.

* **Step C: Rendering Context (Transparent Film)**
  - **Film Transparency**: Enabled in the Render Properties (`Render -> Film -> Transparent`). 
  - **Purpose**: This crucial step allows the HDRI to illuminate the scene and appear in reflections, but makes the actual background pixels transparent. This is ideal for rendering objects with an alpha channel so they can be composited over a different backdrop later.

* **Step D: Geometry & Shading (The Subject)**
  - To properly visualize the HDRI, a subject with a glossy or metallic Principled BSDF material is required. Roughness should be kept low (`0.05` to `0.2`) to clearly see the environment reflections.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| World Node Tree | `bpy.data.worlds.new()` + `node_tree` | Allows programmatic construction of the HDRI shading network (Mapping, HSV, Background) without destroying the existing world setup. |
| Fallback Lighting | `ShaderNodeTexSky` (Nishita) | Ensures the agent receives realistic lighting even if a local HDRI image file is not provided in the parameters. |
| Film Transparency | `scene.render.film_transparent` | Perfectly reproduces the tutorial's step for isolating the subject from the background environment. |
| Subject Generation | `bpy.ops.mesh.primitive_uv_sphere_add` | Provides a physical 3D object to fulfill the `location`, `scale`, and `material_color` parameter requirements while acting as a reflection probe to demonstrate the lighting. |

> **Feasibility Assessment**: 100%. The code fully replicates the World shading node setup demonstrated in the tutorial. To make the code robust and self-contained, it includes a procedural Sky Texture fallback in case a valid HDRI file path is not supplied, and generates a metallic reflection sphere to actively visualize the lighting results.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "HDRI_Reflection_Probe",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.8, 0.8),
    hdri_filepath: str = "",
    rotation_z: float = 45.0,
    strength: float = 1.0,
    transparent_background: bool = True,
    **kwargs,
) -> str:
    """
    Create an advanced HDRI World Lighting setup and a metallic reflection sphere.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the generated reflection sphere.
        location: (x, y, z) world-space position for the reflection sphere.
        scale: Uniform scale factor for the reflection sphere.
        material_color: (R, G, B) base color for the sphere's material.
        hdri_filepath: Path to an .exr or .hdr file. If empty, falls back to Procedural Sky.
        rotation_z: Rotation of the environment map in degrees.
        strength: Emission strength of the environment lighting.
        transparent_background: If True, makes the world background transparent in renders.

    Returns:
        Status string confirming creation.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create World Shading Environment ===
    # We create a new world to be strictly additive and avoid clearing existing setups
    world = bpy.data.worlds.new(f"World_Lighting_{object_name}")
    scene.world = world
    world.use_nodes = True
    
    tree = world.node_tree
    nodes = tree.nodes
    links = tree.links
    nodes.clear() # Clear default nodes in the *new* world

    # Build node pipeline
    node_tex_coord = nodes.new(type="ShaderNodeTexCoord")
    node_tex_coord.location = (-800, 0)
    
    node_mapping = nodes.new(type="ShaderNodeMapping")
    node_mapping.location = (-600, 0)
    node_mapping.inputs['Rotation'].default_value[2] = math.radians(rotation_z)
    
    node_hsv = nodes.new(type="ShaderNodeHueSaturation")
    node_hsv.location = (-100, 0)
    node_hsv.inputs['Saturation'].default_value = 1.0
    
    node_rgb_curves = nodes.new(type="ShaderNodeRGBCurve")
    node_rgb_curves.location = (100, 0)
    
    node_bg = nodes.new(type="ShaderNodeBackground")
    node_bg.location = (400, 0)
    node_bg.inputs['Strength'].default_value = strength
    
    node_output = nodes.new(type="ShaderNodeOutputWorld")
    node_output.location = (600, 0)

    # Determine lighting source (HDRI file vs Procedural Fallback)
    if hdri_filepath:
        node_env_tex = nodes.new(type="ShaderNodeTexEnvironment")
        node_env_tex.location = (-400, 0)
        try:
            img = bpy.data.images.load(hdri_filepath)
            node_env_tex.image = img
        except Exception as e:
            print(f"Could not load HDRI: {e}. Environment will be untextured.")
            
        links.new(node_tex_coord.outputs['Generated'], node_mapping.inputs['Vector'])
        links.new(node_mapping.outputs['Vector'], node_env_tex.inputs['Vector'])
        links.new(node_env_tex.outputs['Color'], node_hsv.inputs['Color'])
    else:
        # Procedural fallback: Nishita Sky Texture
        node_sky = nodes.new(type="ShaderNodeTexSky")
        node_sky.sky_type = 'NISHITA'
        node_sky.location = (-400, 0)
        links.new(node_sky.outputs['Color'], node_hsv.inputs['Color'])

    # Connect color correction and output links
    links.new(node_hsv.outputs['Color'], node_rgb_curves.inputs['Color'])
    links.new(node_rgb_curves.outputs['Color'], node_bg.inputs['Color'])
    links.new(node_bg.outputs['Background'], node_output.inputs['Surface'])

    # === Step 2: Configure Render Properties ===
    if transparent_background:
        scene.render.film_transparent = True

    # === Step 3: Create Reflection Sphere (To visualize the lighting) ===
    # Fulfills object, location, scale, and material parameters
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.0)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    bpy.ops.object.shade_smooth()
    
    # Create glossy metallic material to catch HDRI reflections
    mat = bpy.data.materials.new(name=f"Mat_Chrome_{object_name}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Metallic"].default_value = 1.0
        bsdf.inputs["Roughness"].default_value = 0.05
        
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    return f"Created World Lighting '{world.name}' and reflection probe '{obj.name}' at {location}."
```