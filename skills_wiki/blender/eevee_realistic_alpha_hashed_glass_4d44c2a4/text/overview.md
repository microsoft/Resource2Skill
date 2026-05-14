# EEVEE Realistic Alpha-Hashed Glass

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: EEVEE Realistic Alpha-Hashed Glass

* **Core Visual Mechanism**: By enabling Screen Space Refraction in both the Render Engine and Material settings, and blending a Transparent BSDF with a transmissive Principled BSDF using a Fresnel-driven mask, this shader achieves realistic thickness-aware glass. Crucially, it resolves EEVEE's notorious depth-sorting issues when viewing glass through glass by utilizing the Alpha Hashed blend mode.
* **Why Use This Skill (Rationale)**: By default, EEVEE struggles to correctly render overlapping transparent objects, resulting in "invisible" backfaces or background objects disappearing. This technique circumvents these limitations, converting the transparency calculation into an Alpha Hashed dithered blend that allows multiple layers of glass to composite correctly. Adding a Solidify modifier ensures the refraction algorithm has an inner and outer surface boundary to bounce light accurately.
* **Overall Applicability**: Essential for real-time interior visualizations, product renders (bottles, cups, liquids), and architectural scenes where EEVEE is the chosen render engine and complex transparent objects overlap.
* **Value Addition**: Transforms a basic opaque primitive into a convincing, real-time refractive surface that properly layers with other transparent objects, avoiding the visual errors common in standard EEVEE glass setups.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A standard mesh primitive (e.g., Suzanne monkey head).
  - **Modifiers**: A **Solidify modifier** is applied to give the mesh real physical thickness, which is mathematically required for Screen Space Refraction to calculate the entry and exit points of light. A **Subdivision Surface modifier** is added to smooth out the reflections.
  - **Topology**: Clean quad topology is preferred to ensure smooth refraction warping.

* **Step B: Materials & Shading**
  - **Shader Model**: A Mix Shader blending a `Transparent BSDF` (Top) and `Principled BSDF` (Bottom).
  - **Principled BSDF**: Transmission is set to `1.0`, Roughness to `0.0`. Base Color dictates the glass tint.
  - **Mixing Factor**: A `Fresnel` node (IOR = 1.45) dictates the blend, ensuring facing angles are more transparent and grazing angles are more reflective. This is passed through a `ColorRamp`.
  - **ColorRamp**: The black stop (Position 0.0) is changed to Hex `#A7A7A7` (approx RGB `(0.395, 0.395, 0.395)` in linear space) to reduce the intensity of the pure transparency at facing angles, keeping some refractive properties visible.
  - **Material Settings**: Blend Mode = `Alpha Hashed`, Shadow Mode = `Alpha Hashed`, Screen Space Refraction = `True`.

* **Step C: Lighting & Rendering Context**
  - **Render Engine**: EEVEE.
  - **Render Settings**: `Screen Space Reflections` must be enabled, and the `Refraction` checkbox within it must also be enabled.
  - **Rendering Quality**: Because `Alpha Hashed` uses dithering, higher render samples (100+) or the use of a Denoise node in the Compositor is recommended to clean up the noise.

* **Step D: Animation & Dynamics (if applicable)**
  - Fully real-time and animatable without baking. The material will dynamically react to scene lighting and object movement.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base Object & Thickness | `bpy.ops.mesh` + Modifiers | `primitive_monkey_add` with `SOLIDIFY` efficiently provides the necessary dual-sided geometry for accurate refraction. |
| Overlapping Glass Logic | Shader Node Tree | Procedural node networks are required to mix Transparency and Refraction using Fresnel math. |
| Real-time Refraction | EEVEE Scene & Mat Properties | Directly mutating `scene.eevee.use_ssr` and `mat.blend_method` enables the specific engine features required for the effect. |

> **Feasibility Assessment**: 100% reproduction. The code successfully configures the EEVEE engine, constructs the specific Fresnel-based shader tree, and applies the necessary geometry thickness modifiers.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "GlassMonkey",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (1.0, 1.0, 1.0),
    **kwargs,
) -> str:
    """
    Create an Alpha-Hashed EEVEE Glass Object in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color of the glass in 0-1 range.
        **kwargs: Additional overrides (e.g., roughness, thickness).

    Returns:
        Status string.
    """
    import bpy

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Configure EEVEE Render Settings ===
    scene.render.engine = 'BLENDER_EEVEE'
    scene.eevee.use_ssr = True
    scene.eevee.use_ssr_refraction = True
    
    # === Step 2: Create Base Geometry & Modifiers ===
    bpy.ops.mesh.primitive_monkey_add(location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Apply smooth shading
    for poly in obj.data.polygons:
        poly.use_smooth = True
        
    # Add Subdivision Surface for smooth reflections
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2
    
    # Add Solidify for refractive thickness
    solidify = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = kwargs.get('thickness', 0.03)
    
    # === Step 3: Build Material & Shader Node Tree ===
    mat = bpy.data.materials.new(name=f"{object_name}_EEVEE_Glass")
    mat.use_nodes = True
    
    # Material-level EEVEE settings
    mat.blend_method = 'HASHED'
    mat.shadow_method = 'HASHED'
    mat.use_screen_refraction = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Create Nodes
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (400, 0)
    
    mix_node = nodes.new(type='ShaderNodeMixShader')
    mix_node.location = (200, 0)
    
    transp_node = nodes.new(type='ShaderNodeBsdfTransparent')
    transp_node.location = (0, 100)
    
    princ_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    princ_node.location = (0, -100)
    
    ramp_node = nodes.new(type='ShaderNodeValToRGB')
    ramp_node.location = (0, 300)
    
    fresnel_node = nodes.new(type='ShaderNodeFresnel')
    fresnel_node.location = (-200, 300)
    
    # Configure Node Values
    fresnel_node.inputs[0].default_value = 1.45  # IOR
    
    # Adjust ColorRamp (Stop 0 to A7A7A7 for reduced transparency at facing angles)
    ramp_node.color_ramp.elements[0].position = 0.0
    ramp_node.color_ramp.elements[0].color = (0.395, 0.395, 0.395, 1.0)
    ramp_node.color_ramp.elements[1].position = 1.0
    ramp_node.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    
    # Configure Principled BSDF (Safe across Blender versions)
    if 'Transmission Weight' in princ_node.inputs: # Blender 4.0+
        princ_node.inputs['Transmission Weight'].default_value = 1.0
    elif 'Transmission' in princ_node.inputs: # Blender 3.x
        princ_node.inputs['Transmission'].default_value = 1.0
        
    if 'Roughness' in princ_node.inputs:
        princ_node.inputs['Roughness'].default_value = kwargs.get('roughness', 0.0)
        
    if 'Base Color' in princ_node.inputs:
        # Base Color dictates the glass tint
        color_rgba = (material_color[0], material_color[1], material_color[2], 1.0)
        princ_node.inputs['Base Color'].default_value = color_rgba
        
    # Link Nodes (Using index paths for deep backwards compatibility)
    links.new(fresnel_node.outputs[0], ramp_node.inputs[0])    # Fresnel Fac -> Ramp Fac
    links.new(ramp_node.outputs[0], mix_node.inputs[0])        # Ramp Color -> Mix Fac
    links.new(transp_node.outputs[0], mix_node.inputs[1])      # Transparent -> Mix Top
    links.new(princ_node.outputs[0], mix_node.inputs[2])       # Principled -> Mix Bottom
    links.new(mix_node.outputs[0], out_node.inputs[0])         # Mix Shader -> Material Output
    
    # === Step 4: Finalize ===
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
        
    return f"Created '{object_name}' at {location} configured with an EEVEE Alpha-Hashed glass material."
```