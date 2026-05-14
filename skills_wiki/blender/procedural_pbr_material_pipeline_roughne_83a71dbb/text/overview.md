# Procedural PBR Material Pipeline (Roughness & Bump Mapping)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural PBR Material Pipeline (Roughness & Bump Mapping)

* **Core Visual Mechanism**: The defining technique is the procedural generation of surface imperfections. By feeding a single variation map (in this case, procedural noise) simultaneously into a **ColorRamp** (to compress and define the min/max Roughness values) and a **Bump node** (to generate micro-surface height variation), the material achieves physical realism. 

* **Why Use This Skill (Rationale)**: Real-world materials are rarely perfectly smooth or uniformly rough. Light interacts with dirt, smudges, and micro-scratches. By tying the Roughness and Normal maps to the same underlying texture data, you ensure that the physical "feel" of the surface (bumpiness) perfectly aligns with how it reflects light (roughness), creating a cohesive and believable Physically Based Rendering (PBR) material.

* **Overall Applicability**: This is the foundational shader network for creating realistic architectural materials (polished concrete, aged brick) and hard-surface props (scratched stainless steel, worn plastics).

* **Value Addition**: Compared to a default Principled BSDF with flat numeric sliders, this skill adds procedural localized variation. It breaks up perfectly CGI-looking specular highlights, making objects feel grounded and physically present in the scene.


### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A standard primitive (Cube).
  - **Modifiers**: A Subdivision Surface modifier (Level 3) is applied, and polygon shading is set to Smooth. This creates a high-resolution, curved surface that perfectly catches specular highlights, essential for demonstrating PBR roughness maps.

* **Step B: Materials & Shading**
  - **Shader Model**: Principled BSDF.
  - **Base Setup**: A `ShaderNodeTexNoise` acts as the base imperfection map (replacing the external image maps used in the tutorial for portability).
  - **Roughness Control**: The Noise texture feeds into a `ShaderNodeValToRGB` (ColorRamp). The black/white sliders are clamped to specific gray values (e.g., `0.1` and `0.4`), mapping the noise to a specific range of shininess/roughness without making it completely glossy or completely matte.
  - **Normal Control**: The same Noise texture feeds into a `ShaderNodeBump` (Height input), converting the grayscale data into simulated 3D vector normals.
  - **EEVEE Compatibility**: The material's `blend_method` is explicitly set to ensure compatibility with EEVEE's alpha and transparency handling, a critical step highlighted in the tutorial.

* **Step C: Lighting & Rendering Context**
  - The material responds best to High Dynamic Range (HDRI) environment lighting or Area lights, as broad light sources highlight the micro-variations in the roughness map.
  - Works natively in both EEVEE and Cycles.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base Showcase Object | `bpy.ops.mesh.primitive` + Subdiv Modifier | Provides a smooth, continuous surface ideal for catching reflections and showing off PBR shaders. |
| Base Imperfection Map | Shader Node: Noise Texture | Procedural generation avoids the need for external image files while perfectly mimicking the tutorial's grunge maps. |
| Roughness Tuning | Shader Node: ColorRamp | Exactly matches the tutorial's workflow for clamping and shifting roughness values visually. |
| Surface Height | Shader Node: Bump | Converts grayscale height data into standard vector normals for the Principled BSDF. |

> **Feasibility Assessment**: 100% reproduction of the PBR shader logic demonstrated in the video. While the video used specific photo-scanned textures (like a concrete floor image), this code substitutes them with procedural noise to achieve the exact same workflow and comparable visual result entirely within a self-contained script.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Material_Showcase",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.5, 0.5, 0.5),
    is_metallic: float = 0.0,
    roughness_min: float = 0.1,
    roughness_max: float = 0.4,
    bump_strength: float = 0.15,
    **kwargs,
) -> str:
    """
    Create a procedural PBR material showcasing Roughness and Bump mapping workflows.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created mesh.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color.
        is_metallic: 1.0 for metals (steel, brass), 0.0 for dielectrics (concrete, plastic).
        roughness_min: Minimum roughness (0.0 = mirror, 1.0 = matte).
        roughness_max: Maximum roughness limit.
        bump_strength: Intensity of the micro-surface bumps.

    Returns:
        Status string confirming creation.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Add Subdivision Surface modifier for smooth reflections
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 4
    subsurf.render_levels = 4
    
    # Apply smooth shading to all polygons
    for poly in obj.data.polygons:
        poly.use_smooth = True

    # === Step 2: Build PBR Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    
    # Ensure EEVEE transparency/blend mode settings are initialized correctly
    mat.blend_method = 'OPAQUE'
    mat.shadow_method = 'OPAQUE'
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Core Nodes
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (1000, 0)
    
    principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled_node.location = (600, 0)
    principled_node.inputs['Base Color'].default_value = (*material_color, 1.0)
    principled_node.inputs['Metallic'].default_value = is_metallic
    
    # Texture Node: Acts as our localized imperfection map
    noise_node = nodes.new(type='ShaderNodeTexNoise')
    noise_node.location = (0, 0)
    noise_node.inputs['Scale'].default_value = 15.0
    noise_node.inputs['Detail'].default_value = 5.0
    noise_node.inputs['Roughness'].default_value = 0.6
    
    # Converter Node: ColorRamp to control Roughness range
    ramp_node = nodes.new(type='ShaderNodeValToRGB')
    ramp_node.location = (300, 150)
    
    # Map the noise to specific grayscale values (Roughness mapping)
    ramp_node.color_ramp.elements[0].position = 0.3
    ramp_node.color_ramp.elements[0].color = (roughness_min, roughness_min, roughness_min, 1.0)
    ramp_node.color_ramp.elements[1].position = 0.7
    ramp_node.color_ramp.elements[1].color = (roughness_max, roughness_max, roughness_max, 1.0)
    
    # Vector Node: Bump to convert height map to normals
    bump_node = nodes.new(type='ShaderNodeBump')
    bump_node.location = (300, -150)
    bump_node.inputs['Strength'].default_value = bump_strength
    bump_node.inputs['Distance'].default_value = 0.1
    
    # === Step 3: Link Shader Network ===
    # Noise -> ColorRamp -> Principled BSDF Roughness
    links.new(noise_node.outputs['Fac'], ramp_node.inputs['Fac'])
    links.new(ramp_node.outputs['Color'], principled_node.inputs['Roughness'])
    
    # Noise -> Bump -> Principled BSDF Normal
    links.new(noise_node.outputs['Fac'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], principled_node.inputs['Normal'])
    
    # Principled BSDF -> Material Output
    links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])
    
    # === Step 4: Finalize ===
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
        
    return f"Created '{object_name}' with procedural PBR material at {location}"
```