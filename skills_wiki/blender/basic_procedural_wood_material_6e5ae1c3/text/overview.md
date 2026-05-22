# Basic Procedural Wood Material

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Basic Procedural Wood Material

* **Core Visual Mechanism**: The defining technique is the use of a **Procedural Noise Texture** that is heavily distorted and stretched along specific axes using a **Mapping Node**. This stretched, high-contrast noise mimics the directional flow of wood grain. The grayscale noise values are then remapped into brown, woody tones using a **ColorRamp**, and the same noise data is fed into a **Bump Node** to generate matching physical surface detail (normal mapping) without adding actual geometry.

* **Why Use This Skill (Rationale)**: Procedural texturing is a fundamental 3D workflow because it is resolution-independent and requires no UV unwrapping. By manipulating coordinate spaces (stretching, scaling) before they hit a procedural generator (like noise), you can create structured patterns (like wood, brushed metal, or scratches) from purely chaotic mathematical noise. 

* **Overall Applicability**: This specific technique is universally applicable for generating background props, furniture, floors, or natural elements where basic wood grain is needed but the overhead of sourcing, importing, and UV-mapping image textures is unnecessary. It serves as the foundational logic for almost all procedural material creation in Blender.

* **Value Addition**: Compared to a default primitive with a flat color, this skill adds immediate realism and physical texture. It teaches the agent how to compose a shader network where a single procedural data source (the noise) drives multiple material properties (color and bump) simultaneously, ensuring visual consistency.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: The technique is topology-independent and works on any base mesh. A standard cube is used for demonstration.
  - **Modifiers**: No modifiers are strictly necessary, though Bevel can help catch the light on the bump map edges.

* **Step B: Materials & Shading**
  - **Shader Model**: Principled BSDF.
  - **Node Tree Hierarchy**:
    1. `Texture Coordinate (Object)` -> `Mapping (Vector)`
    2. `Mapping (Vector)` -> `Noise Texture (Vector)`
    3. `Noise Texture (Fac)` -> `ColorRamp (Fac)` -> `Principled BSDF (Base Color)`
    4. `Noise Texture (Fac)` -> `Bump (Height)` -> `Principled BSDF (Normal)`
  - **Specific Values**:
    - **Mapping Scale**: `(X: 3.0, Y: 1.0, Z: 0.1)` — This squishes the noise on X and stretches it significantly on Z, creating the "grain" direction.
    - **Noise Texture**: Scale `5.0`, Detail `15.0` (maximum for crispness), Roughness `0.6`, Distortion `2.0` (creates the wavy, knot-like patterns).
    - **ColorRamp**: Stop 0 at position `0.2` with dark brown `(0.1, 0.05, 0.02)`. Stop 1 at position `0.8` with a lighter brown.
    - **Bump**: Strength `0.1` to `0.2` (subtle surface imperfection).

* **Step C: Lighting & Rendering Context**
  - **Lighting**: Standard three-point lighting or an HDRI works best to highlight the procedural bump map detail.
  - **Engine**: Fully compatible with both EEVEE and Cycles.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base Object | `bpy.ops.mesh.primitive_cube_add` | Simple canvas to demonstrate the material. |
| Procedural Grain | Shader Node Tree (`ShaderNodeTexNoise`) | Core technique from the tutorial; provides infinite resolution. |
| Grain Direction | Shader Node Tree (`ShaderNodeMapping`) | Manipulating the vector input is required to stretch noise into wood grain. |
| Surface Detail | Shader Node Tree (`ShaderNodeBump`) | Reuses the noise data to create surface depth efficiently without geometry. |

> **Feasibility Assessment**: 100% of the procedural wood grain and basic bump texturing shown in the middle section of the tutorial is reproduced here. It encapsulates the core logic of chaining Texture Coordinates -> Mapping -> Noise -> ColorRamp/Bump -> Principled BSDF.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralWoodBlock",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.4, 0.2, 0.05),
    **kwargs,
) -> str:
    """
    Create a mesh with a basic procedural wood material in the active scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) color used for the lighter part of the wood grain.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy

    # Ensure we are in object mode
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # === Step 2: Build Procedural Material ===
    mat_name = f"{object_name}_WoodMaterial"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes just in case, though standard adds Principled + Output
    for node in nodes:
        nodes.remove(node)

    # Add required nodes
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (300, 0)

    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf_node.location = (0, 0)

    bump_node = nodes.new(type='ShaderNodeBump')
    bump_node.location = (-300, -200)
    bump_node.inputs['Strength'].default_value = 0.15
    bump_node.inputs['Distance'].default_value = 0.1

    color_ramp_node = nodes.new(type='ShaderNodeValToRGB')
    color_ramp_node.location = (-300, 100)
    
    # Configure wood colors (Dark stop and Light stop)
    color_ramp_node.color_ramp.elements[0].position = 0.2
    color_ramp_node.color_ramp.elements[0].color = (0.05, 0.02, 0.01, 1.0) # Very dark brown
    
    color_ramp_node.color_ramp.elements[1].position = 0.8
    # Map the requested material color to the lighter wood grain
    color_ramp_node.color_ramp.elements[1].color = (material_color[0], material_color[1], material_color[2], 1.0)

    noise_node = nodes.new(type='ShaderNodeTexNoise')
    noise_node.location = (-550, 0)
    noise_node.inputs['Scale'].default_value = 5.0
    noise_node.inputs['Detail'].default_value = 15.0
    noise_node.inputs['Roughness'].default_value = 0.6
    noise_node.inputs['Distortion'].default_value = 2.0 # Creates the wavy wood look

    mapping_node = nodes.new(type='ShaderNodeMapping')
    mapping_node.location = (-750, 0)
    # Stretch the noise significantly along Z, and compress slightly on X
    mapping_node.inputs['Scale'].default_value = (3.0, 1.0, 0.1)

    tex_coord_node = nodes.new(type='ShaderNodeTexCoord')
    tex_coord_node.location = (-950, 0)

    # === Step 3: Link Nodes ===
    # Coordinate system -> Mapping -> Noise
    links.new(tex_coord_node.outputs['Object'], mapping_node.inputs['Vector'])
    links.new(mapping_node.outputs['Vector'], noise_node.inputs['Vector'])
    
    # Noise -> ColorRamp -> Base Color
    links.new(noise_node.outputs['Fac'], color_ramp_node.inputs['Fac'])
    links.new(color_ramp_node.outputs['Color'], bsdf_node.inputs['Base Color'])
    
    # Noise -> Bump -> Normal
    links.new(noise_node.outputs['Fac'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], bsdf_node.inputs['Normal'])

    # BSDF -> Output
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])

    # Set some base BSDF properties for wood
    bsdf_node.inputs['Roughness'].default_value = 0.65
    bsdf_node.inputs['Specular IOR Level'].default_value = 0.3

    # Assign material to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    return f"Created '{object_name}' at {location} with Procedural Wood Material."
```