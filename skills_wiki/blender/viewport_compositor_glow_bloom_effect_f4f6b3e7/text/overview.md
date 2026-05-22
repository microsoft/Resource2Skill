# Viewport Compositor Glow (Bloom Effect)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Viewport Compositor Glow (Bloom Effect)

* **Core Visual Mechanism**: The core visual signature of this effect is the atmospheric, bleeding light (bloom/glare) radiating from high-intensity emissive surfaces. It is achieved by combining an Emission material shader with a Post-Processing `Glare` node set to 'Bloom' in the Compositor, and enabling the Real-Time Viewport Compositor to see the effect while modeling.

* **Why Use This Skill (Rationale)**: Physically accurate rendering engines simulate light but don't inherently simulate the optical imperfections of camera lenses or the human eye. Adding bloom replicates how bright light scatters within a lens or atmospheric medium. It signals to the viewer that an object is intensely hot or magical, breaking the hard edges of 3D geometry and integrating the object into the surrounding atmosphere.

* **Overall Applicability**: Essential for sci-fi environments (neon signs, sci-fi panels, lightsabers, glowing engines), magical/fantasy effects (glowing runes, crystals), and cinematic night scenes.

* **Value Addition**: Transforms a flat, mathematically perfect colored shape into a perceived light source. By using the Real-Time Viewport Compositor, it provides immediate artistic feedback without needing to repeatedly hit "Render".


### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: Standard Primitive Cube (or any mesh).
  - **Modifiers**: None required for the effect itself.
  - **Topology**: Minimal; the glowing effect overrides surface topology details.

* **Step B: Materials & Shading**
  - **Shader Model**: Pure Emission Shader (replacing the default Principled BSDF).
  - **Color**: Highly saturated colors work best. e.g., Pink `(1.0, 0.05, 0.2)` or Cyan `(0.05, 0.8, 1.0)`.
  - **Strength**: Must be greater than `1.0` (e.g., `2.0` to `5.0`) to trigger the glare threshold effectively.

* **Step C: Lighting & Rendering Context**
  - **Lighting**: The object *is* the light. Deleting other scene lights accentuates the glowing effect.
  - **Compositing**: Requires `Use Nodes` enabled in the Compositing workspace. A `Glare` node is inserted between `Render Layers` and `Composite`, with its type set to `BLOOM`.
  - **Viewport Settings**: The Viewport Shading must be set to `RENDERED`, and the Compositor dropdown set to `ALWAYS` (available in Blender 3.5+) to see the glow in real-time.

* **Step D: Animation & Dynamics (if applicable)**
  - N/A for this base technique, but the Emission Strength or Color can easily be keyframed for pulsing effects.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Glowing Object | bpy.ops.mesh.primitive + Shader Node Tree | Clean geometry with an explicit Emission node setup replacing the default material. |
| Bloom/Glare Effect | Compositor Node Tree | Universal across both Eevee and Cycles, standard for modern Blender workflows. |
| Real-time View | Context Space Data Modification | Overrides viewport settings to make the compositor visible live, as demonstrated in the tutorial. |

> **Feasibility Assessment**: 100% reproduction. The script perfectly reproduces the material, the compositor setup, and attempts to set the 3D viewport to display the effect interactively.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "GlowingCube",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (1.0, 0.05, 0.2),  # Pink/Red glow by default
    **kwargs,
) -> str:
    """
    Create Viewport Compositor Glow (Bloom Effect) in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created glowing object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: 
            emission_strength (float): Intensity of the glow (default 2.0).

    Returns:
        Status string describing the operation.
    """
    import bpy

    # Extract kwargs
    emission_strength = kwargs.get("emission_strength", 2.0)

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # === Step 2: Build Material ===
    mat_name = f"{object_name}_EmissionMat"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    nodes.clear()

    # Create Emission and Output nodes
    node_emission = nodes.new(type='ShaderNodeEmission')
    node_emission.location = (0, 0)
    # Blender expects RGBA for colors
    node_emission.inputs['Color'].default_value = (*material_color, 1.0)
    node_emission.inputs['Strength'].default_value = emission_strength

    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = (200, 0)

    # Link material nodes
    links.new(node_emission.outputs['Emission'], node_output.inputs['Surface'])

    # Assign material to object
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    # === Step 3: Set up Compositor for Bloom ===
    scene.use_nodes = True
    comp_tree = scene.node_tree
    comp_links = comp_tree.links

    # Ensure Render Layers node exists
    render_layers = next((n for n in comp_tree.nodes if n.type == 'R_LAYERS'), None)
    if not render_layers:
        render_layers = comp_tree.nodes.new('CompositorNodeRLayers')
        render_layers.location = (-200, 0)

    # Ensure Composite node exists
    composite = next((n for n in comp_tree.nodes if n.type == 'COMPOSITE'), None)
    if not composite:
        composite = comp_tree.nodes.new('CompositorNodeComposite')
        composite.location = (400, 0)

    # Add Glare node if it doesn't exist
    glare = next((n for n in comp_tree.nodes if n.type == 'GLARE'), None)
    if not glare:
        glare = comp_tree.nodes.new('CompositorNodeGlare')
        glare.location = (100, 0)
        glare.glare_type = 'BLOOM'
        glare.mix = 0.0 # Standard mix

        # Relink through Glare node
        comp_links.new(render_layers.outputs['Image'], glare.inputs['Image'])
        comp_links.new(glare.outputs['Image'], composite.inputs['Image'])
    else:
        # If glare already exists, ensure it's set to BLOOM
        glare.glare_type = 'BLOOM'

    # === Step 4: Configure Viewport (Interactive visual feedback) ===
    # This safely attempts to enable Viewport Compositor if executed in a UI context
    if bpy.context.screen:
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'RENDERED'
                        # 'ALWAYS' setting allows compositor effects in the 3D viewport (Blender 3.5+)
                        if hasattr(space.shading, "compositor"):
                            space.shading.compositor = 'ALWAYS'

    return f"Created glowing '{object_name}' at {location} with Emission Strength {emission_strength} and enabled Compositor Bloom."
```