# Advanced HDRI Environment Setup (Split Lighting & Background)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Advanced HDRI Environment Setup (Split Lighting & Background)

* **Core Visual Mechanism**: This technique uses a custom World Shader node tree to decouple scene lighting from the visible background. By using a `Light Path` node's `Is Camera Ray` output to drive a `Mix Shader`, it feeds high dynamic range (HDRI) image data into the global illumination and reflections of the scene, while simultaneously projecting a completely different solid color (or a transparent alpha channel) directly to the camera view. 

* **Why Use This Skill (Rationale)**: HDRI images provide incredibly realistic, physically accurate lighting and complex reflections that are essential for metallic, glassy, or glossy materials. However, the actual photographs used in HDRIs are often messy, low-resolution, or visually distracting. This pattern allows 3D artists to get the "best of both worlds": the pristine, photorealistic lighting of an HDRI, combined with a clean, distraction-free graphic background (or transparency for compositing).

* **Overall Applicability**: Essential for product visualization, studio lookdev, portfolio prop rendering, and any scenario where an object needs realistic lighting but the final output requires a flat color backdrop or a transparent background for UI/web integration.

* **Value Addition**: Compared to a default Blender point light and grey world, this skill instantly elevates the realism of PBR materials (especially metals and glass) by providing complex 360-degree reflection data, while maintaining absolute control over the final render's composition and background styling.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - *Not directly applicable to the core skill*, but a highly subdivided `UV Sphere` with smooth shading is typically used to test and visualize the reflection quality of the environment.

* **Step B: Materials & Shading (World Node Tree)**
  - **Node 1: Background (Lighting)**: Connects to an `Environment Texture` (or a procedural `Sky Texture` as a fallback) to provide high dynamic range color values.
  - **Node 2: Background (Visible)**: Uses a standard RGB color tuple, e.g., `(0.05, 0.05, 0.05, 1.0)` for a dark studio grey.
  - **Node 3: Light Path**: The `Is Camera Ray` output outputs `1.0` if the ray is hitting the camera directly, and `0.0` if the ray is bouncing off an object (diffuse, glossy, transmission).
  - **Node 4: Mix Shader**: Uses the `Is Camera Ray` as the factor. Socket 1 (Lighting) evaluates for reflections/illumination. Socket 2 (Visible) evaluates for the background pixels.

* **Step C: Lighting & Rendering Context**
  - **Render Engine**: Works perfectly in both EEVEE and Cycles.
  - **Film Settings**: To achieve a transparent background (instead of a solid color), navigate to `Render Properties -> Film -> Transparent`.

* **Step D: Animation & Dynamics**
  - N/A

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Split Background/Lighting | World Shader Nodes (`Light Path` + `Mix Shader`) | The mathematically exact way to route different world shaders based on ray types. |
| Transparent Background | `scene.render.film_transparent` | Blender's native API hook for rendering the world background as an alpha channel. |
| HDRI Source | `ShaderNodeTexSky` (Fallback) | Ensures the script is self-contained and reproducible without requiring the user to have a specific `.exr` file on their hard drive, while still providing true HDR lighting data. |
| Visualization | `bpy.ops.mesh.primitive` + PBR Material | Adds a chrome sphere to immediately prove the environment reflections are working. |

> **Feasibility Assessment**: 100% reproduction of the technique. The code sets up the exact World Shader node tree demonstrated in the tutorial, handles the transparent film toggle, and includes a fallback procedural HDR sky to guarantee it works standalone.

#### 3b. Complete Reproduction Code

```python
def create_hdri_environment_setup(
    scene_name: str = "Scene",
    use_transparent_bg: bool = False,
    visible_bg_color: tuple = (0.1, 0.1, 0.1, 1.0),
    hdri_filepath: str = "",
    lighting_strength: float = 1.0,
    **kwargs,
) -> str:
    """
    Create an Advanced World Environment that splits HDRI lighting from the visible background.

    Args:
        scene_name: Name of the target scene.
        use_transparent_bg: If True, the background will render as transparent (alpha).
        visible_bg_color: (R, G, B, A) color for the background if transparency is False.
        hdri_filepath: Optional path to an .exr or .hdr file. If empty, uses procedural Sky.
        lighting_strength: Intensity of the HDRI lighting.

    Returns:
        Status string describing the created world setup.
    """
    import bpy

    # === Step 1: Target Scene & Render Settings ===
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    
    # Handle Transparent Film setting (Render Properties)
    scene.render.film_transparent = use_transparent_bg

    # === Step 2: Create a New World (Additive approach) ===
    new_world = bpy.data.worlds.new(name="Advanced_HDRI_World")
    scene.world = new_world
    new_world.use_nodes = True
    tree = new_world.node_tree
    nodes = tree.nodes
    links = tree.links

    # Clear default nodes
    nodes.clear()

    # === Step 3: Build World Node Tree ===
    # Output node
    node_output = nodes.new(type='ShaderNodeOutputWorld')
    node_output.location = (600, 0)

    # Mix Shader
    node_mix = nodes.new(type='ShaderNodeMixShader')
    node_mix.location = (400, 0)

    # Light Path
    node_light_path = nodes.new(type='ShaderNodeLightPath')
    node_light_path.location = (0, 300)

    # Background for Lighting (Reflections & GI)
    node_bg_lighting = nodes.new(type='ShaderNodeBackground')
    node_bg_lighting.name = "BG_Lighting"
    node_bg_lighting.label = "HDRI Lighting"
    node_bg_lighting.inputs['Strength'].default_value = lighting_strength
    node_bg_lighting.location = (200, 100)

    # Background for Visibility (Camera View)
    node_bg_visible = nodes.new(type='ShaderNodeBackground')
    node_bg_visible.name = "BG_Visible"
    node_bg_visible.label = "Visible Background"
    node_bg_visible.inputs['Color'].default_value = visible_bg_color
    node_bg_visible.location = (200, -100)

    # Setup HDRI Texture (or fallback to procedural Sky Texture)
    if hdri_filepath:
        node_env = nodes.new(type='ShaderNodeTexEnvironment')
        try:
            img = bpy.data.images.load(hdri_filepath)
            node_env.image = img
        except Exception as e:
            print(f"Warning: Could not load HDRI: {e}. Defaulting to purple missing texture.")
        node_env.location = (0, 100)
        links.new(node_env.outputs['Color'], node_bg_lighting.inputs['Color'])
    else:
        # Fallback to Procedural Sky to ensure self-contained HDR lighting works out of the box
        node_sky = nodes.new(type='ShaderNodeTexSky')
        node_sky.sky_type = 'NISHITA'
        # Tweak sky settings for a nice sunset look with good reflections
        node_sky.sun_elevation = 0.2
        node_sky.sun_rotation = 2.5
        node_sky.location = (0, 100)
        links.new(node_sky.outputs['Color'], node_bg_lighting.inputs['Color'])

    # Link Everything Together
    # Is Camera Ray = 1 (True) -> Uses Mix Shader Input[2] (Visible Background)
    # Is Camera Ray = 0 (False) -> Uses Mix Shader Input[1] (Lighting Background)
    links.new(node_light_path.outputs['Is Camera Ray'], node_mix.inputs['Fac'])
    links.new(node_bg_lighting.outputs['Background'], node_mix.inputs[1])
    links.new(node_bg_visible.outputs['Background'], node_mix.inputs[2])
    links.new(node_mix.outputs['Shader'], node_output.inputs['Surface'])

    # === Step 4: Create a Test Object (Chrome Sphere) to visualize the effect ===
    # This proves the lighting setup is working by creating a highly reflective surface
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.0, location=(0, 0, 1.0))
    sphere = bpy.context.active_object
    sphere.name = "HDRI_Test_Chrome_Sphere"
    bpy.ops.object.shade_smooth()

    # Create Chrome Material
    mat = bpy.data.materials.new(name="Chrome_Test_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1.0)
        bsdf.inputs["Metallic"].default_value = 1.0
        bsdf.inputs["Roughness"].default_value = 0.02
    
    if sphere.data.materials:
        sphere.data.materials[0] = mat
    else:
        sphere.data.materials.append(mat)

    return f"Created new World '{new_world.name}' with split HDRI lighting/background and a test chrome sphere."
```