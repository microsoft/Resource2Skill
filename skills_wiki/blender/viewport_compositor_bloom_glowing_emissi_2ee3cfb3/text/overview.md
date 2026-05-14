# Viewport Compositor Bloom & Glowing Emission Material

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Viewport Compositor Bloom & Glowing Emission Material

* **Core Visual Mechanism**: Coupling a high-strength Emission material with a "Glare" node in the Compositor, and enabling the Viewport Compositor to see the glowing halo effect (Bloom) in real-time. 
* **Why Use This Skill (Rationale)**: Physically, very bright objects scatter light within a camera lens or the atmosphere, creating a "bloom" or "halo" effect. Without this compositing step, emission materials simply look like flat, unshaded colors regardless of how high their strength is. The Compositor Glare node translates mathematical light intensity into a perceptual glow.
* **Overall Applicability**: Essential for sci-fi elements (neon lights, thrusters, holograms), magical effects, UI elements integrated into 3D scenes, and dramatic, high-contrast lighting setups. 
* **Value Addition**: Turns a visually flat, unlit surface into a striking, realistic light source. Crucially, starting in Blender 4.2, the standalone "Bloom" checkbox was removed from EEVEE, making this Compositor-based approach the required, unified standard for both EEVEE and Cycles.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A standard Cube primitive (or any geometry).
  - **Topology**: Topology is irrelevant for emission surfaces unless they are deformed, as the shader overrides all surface shading.
* **Step B: Materials & Shading**
  - **Shader Model**: Principled BSDF.
  - **Emission Properties**: 
    - `Emission Color`: Target color, e.g., Blue `(0.1, 0.4, 1.0)`.
    - `Emission Strength`: Pushed well beyond 1.0 (e.g., `10.0` to `20.0`) to trigger the glare threshold in the compositor.
* **Step C: Lighting & Rendering Context**
  - **Compositor**: `scene.use_nodes` must be enabled. A `CompositorNodeGlare` is inserted between the Render Layers and Composite nodes.
  - **Glare Mode**: Set to `BLOOM` (Blender 4.2+) or `FOG_GLOW` (Blender 4.1 and older).
  - **Viewport**: 3D Viewport Shading is set to `RENDERED`, and Viewport Compositor is set to `ALWAYS` to visualize the glow in real-time while modeling.
* **Step D: Animation & Dynamics (if applicable)**
  - The `Emission Strength` can be keyframed or driven by a noise modifier to create pulsing, flickering neon or fire effects.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base Object & Material | `bpy.ops.mesh` + Shader Nodes | Standard setup for assigning an emission color and intensity. |
| Glow/Halo Effect | Compositor Node Tree | Blender 4.2+ mandates the Compositor Glare node for Bloom effects. |
| Real-time Preview | Viewport Settings via `bpy.context.screen` | Allows the user/agent to see the composited glow directly in the 3D viewport without rendering. |

> **Feasibility Assessment**: 100% — This code perfectly replicates the glowing cube and the required compositor routing demonstrated in the Blender 4.2 workflow tutorial.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "GlowingCube",
    location: tuple = (0, 0, 1),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.4, 1.0),
    emission_strength: float = 10.0,
    **kwargs,
) -> str:
    """
    Create a glowing object using Emission and Viewport Compositor (Blender 4.2+ standard).

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created glowing object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) emission color in 0-1 range.
        emission_strength: Intensity of the light/glow.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # === Step 2: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_GlowMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    
    if bsdf:
        # Compatibility handling for Blender 4.0+ vs older versions
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (*material_color, 1.0)
        elif "Emission" in bsdf.inputs:
            bsdf.inputs["Emission"].default_value = (*material_color, 1.0)
            
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = emission_strength
            
    obj.data.materials.append(mat)

    # === Step 3: Setup Compositor for Glow ===
    scene.use_nodes = True
    tree = scene.node_tree
    
    # Find existing necessary nodes
    comp_node = next((n for n in tree.nodes if n.type == 'COMPOSITE'), None)
    rl_node = next((n for n in tree.nodes if n.type == 'R_LAYERS'), None)
    glare_node = next((n for n in tree.nodes if n.type == 'GLARE'), None)

    if not comp_node:
        comp_node = tree.nodes.new('CompositorNodeComposite')
        comp_node.location = (400, 0)
    if not rl_node:
        rl_node = tree.nodes.new('CompositorNodeRLayers')
        rl_node.location = (0, 0)

    # If glare node doesn't exist, create and link it additively
    if not glare_node:
        glare_node = tree.nodes.new('CompositorNodeGlare')
        glare_node.location = (200, 0)
        
        # Set to BLOOM (Blender 4.2+) or fallback to FOG_GLOW (older versions)
        try:
            glare_node.glare_type = 'BLOOM'
        except TypeError:
            glare_node.glare_type = 'FOG_GLOW'
            
        # Insert Glare node between Render Layers and Composite
        if rl_node.outputs['Image'].links:
            # Clear existing direct links to insert the glare node cleanly
            for link in rl_node.outputs['Image'].links:
                tree.links.remove(link)
                
        tree.links.new(rl_node.outputs['Image'], glare_node.inputs['Image'])
        tree.links.new(glare_node.outputs['Image'], comp_node.inputs['Image'])

    # === Step 4: Enable Viewport Compositor for Real-time Preview ===
    # Check if UI is available (prevents crash in headless background execution)
    if bpy.context.screen:
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'RENDERED'
                        try:
                            # Enable Viewport Compositor (Available in Blender 3.5+)
                            space.shading.use_compositor = 'ALWAYS'
                        except AttributeError:
                            pass

    return f"Created glowing object '{object_name}' at {location} and configured Viewport Compositor."
```