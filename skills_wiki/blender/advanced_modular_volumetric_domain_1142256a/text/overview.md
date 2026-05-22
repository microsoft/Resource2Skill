# Advanced Modular Volumetric Domain

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Advanced Modular Volumetric Domain

* **Core Visual Mechanism**: Instead of relying on the "all-in-one" `Principled Volume` shader (which can be bloated and computationally heavy), this technique builds a custom volumetric material by mathematically adding the core building blocks: `Volume Scatter` (for fog and light rays), `Volume Absorption` (to tint shadows and block specific wavelengths), and `Emission` (for glowing particles). This allows for highly specific effects, like forward-scattering colored god rays that cast complementary-colored shadows.
* **Why Use This Skill (Rationale)**: Volumetrics are essential for grounding a 3D scene, providing depth cues, and revealing the shape of light sources (god rays/light shafts). By separating the scattering and absorption nodes, a 3D artist gains explicit control over *Anisotropy* (directing light forward or backward) and can create stylized color-blocking effects that the default Principled Volume struggles to achieve elegantly.
* **Overall Applicability**: Cinematic scene lighting, sci-fi environments, moody and atmospheric renders, underwater scenes, or anywhere "thick" air is needed to interact with spotlights or emission sources.
* **Value Addition**: Transforms a sterile, empty 3D space into a physical atmosphere. It makes light sources feel tangible and creates natural gradient falloffs in the background.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - Uses a standard primitive bounding box (Cube) scaled up to encompass the entire scene or specific areas where fog is needed.
  - No complex topology is required.
  - **Crucial Viewport Setup**: The object's viewport display type must be set to `BOUNDS`. If left as `SOLID`, the cube will block the user's view while working in the 3D viewport.

* **Step B: Materials & Shading**
  - **Shader Model**: A custom node tree connected *only* to the `Volume` input of the Material Output (the `Surface` input is left empty).
  - **Volume Scatter**: Controls the fog. `Anisotropy` is the key parameter here. A value of `0` scatters light equally everywhere. A positive value (e.g., `0.8`) scatters light forward (like light through dusty air), while a negative value scatters it backward.
  - **Volume Absorption**: Acts as a color filter. If set to Green, it absorbs Red and Blue light, meaning white light passing through it will turn Green, but shadows will take on complementary hues.
  - **Shader Addition**: The Scatter, Absorption, and Emission nodes are combined using `Add Shader` nodes, combining their mathematical properties without overriding each other.

* **Step C: Lighting & Rendering Context**
  - **Lighting**: Absolutely requires light sources (Spotlights, Point lights, or strong Sun lights) intersecting the volume to be visible.
  - **Render Engine**: Works best in **Cycles** for physically accurate light scattering and multiple light bounces. EEVEE supports it, but requires tweaking the Volumetric Tile Size and Samples in the render properties for good quality.

* **Step D: Animation & Dynamics (if applicable)**
  - For procedural animation, noise textures can be plugged into the `Density` inputs to create rolling clouds or patchy fog, combined with a Mapping node driven by `#frame` for wind movement.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Domain Geometry | `bpy.ops.mesh.primitive_cube_add` | A simple bounding volume is all that is needed to contain the shader. |
| Viewport Usability | `obj.display_type = 'BOUNDS'` | Prevents the massive cube from occluding the scene while modeling. |
| Volumetric Material | Shader node tree (bmesh/data API) | Bypasses the Principled Volume to create the modular Scatter + Absorption + Emission setup demonstrated in the tutorial. |

> **Feasibility Assessment**: 100% of the modular volumetric shading technique can be reproduced via code. Note that for the fog to look visually impressive, the user will need to place lights inside or shining through this domain.

#### 3b. Complete Reproduction Code

```python
def create_custom_volumetric_domain(
    scene_name: str = "Scene",
    object_name: str = "Volumetric_Fog_Domain",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 10.0,
    scatter_color: tuple = (0.8, 0.9, 1.0),
    scatter_density: float = 0.02,
    anisotropy: float = 0.7,
    absorption_color: tuple = (1.0, 1.0, 1.0),
    absorption_density: float = 0.0,
    emission_color: tuple = (0.0, 0.0, 0.0),
    emission_strength: float = 0.0,
    **kwargs,
) -> str:
    """
    Creates a large bounding box with a modular, highly customizable volumetric material.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name of the domain object.
        location: (x, y, z) center of the domain.
        scale: Uniform scale. Larger scale means it covers more of the scene.
        scatter_color: (R, G, B) color of the scattered light (fog color).
        scatter_density: Thickness of the fog. Keep very low (0.01 - 0.05) for large scales!
        anisotropy: -1.0 to 1.0. High positive values scatter light forward (god rays).
        absorption_color: (R, G, B) color to absorb.
        absorption_density: Thickness of the absorption effect.
        emission_color: (R, G, B) color of glowing ambient fog.
        emission_strength: Brightness of the ambient fog.
        
    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (The Domain) ===
    bpy.ops.mesh.primitive_cube_add(size=2.0)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))

    # Crucial for volumetrics: set viewport display to bounds so it doesn't block vision
    obj.display_type = 'BOUNDS'

    # === Step 2: Build the Modular Volumetric Material ===
    mat_name = f"{object_name}_ModularVolMaterial"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Add necessary nodes
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (400, 0)

    # We use Add Shader nodes to mathematically combine the volume effects
    add_node_final = nodes.new(type='ShaderNodeAddShader')
    add_node_final.location = (200, 0)

    add_node_base = nodes.new(type='ShaderNodeAddShader')
    add_node_base.location = (0, 0)

    scatter_node = nodes.new(type='ShaderNodeVolumeScatter')
    scatter_node.location = (-250, 150)
    scatter_node.inputs['Color'].default_value = (*scatter_color, 1.0)
    scatter_node.inputs['Density'].default_value = scatter_density
    scatter_node.inputs['Anisotropy'].default_value = anisotropy

    absorp_node = nodes.new(type='ShaderNodeVolumeAbsorption')
    absorp_node.location = (-250, -50)
    absorp_node.inputs['Color'].default_value = (*absorption_color, 1.0)
    absorp_node.inputs['Density'].default_value = absorption_density

    emission_node = nodes.new(type='ShaderNodeEmission')
    emission_node.location = (-250, -250)
    emission_node.inputs['Color'].default_value = (*emission_color, 1.0)
    emission_node.inputs['Strength'].default_value = emission_strength

    # === Step 3: Link the Nodes ===
    # Link Scatter and Absorption together
    links.new(scatter_node.outputs['Volume'], add_node_base.inputs[0])
    links.new(absorp_node.outputs['Volume'], add_node_base.inputs[1])

    # Add Emission to the mix
    links.new(add_node_base.outputs['Shader'], add_node_final.inputs[0])
    links.new(emission_node.outputs['Emission'], add_node_final.inputs[1])

    # Connect to the Volume output (Surface must remain empty)
    links.new(add_node_final.outputs['Shader'], out_node.inputs['Volume'])

    # Ensure it's assigned to the scene collection
    if obj.name not in scene.collection.objects:
        scene.collection.objects.link(obj)

    return f"Created Volumetric Domain '{object_name}' at {location} with scale {scale}. Add lights to the scene to see the scattering effect."
```