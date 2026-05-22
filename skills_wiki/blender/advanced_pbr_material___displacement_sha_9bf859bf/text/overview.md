### 1. High-level Design Pattern Extraction

> **Skill Name**: Advanced PBR Material & Displacement Shading Setup

* **Core Visual Mechanism**: This pattern defines the standard industry workflow for physically based rendering (PBR) shading in Blender. It revolves around wiring different texture maps (Base Color, Reflection/Specular, Gloss/Roughness, Normal, and Displacement) into a single `Principled BSDF` shader. The signature of this technique is the use of true micro-displacement to alter the actual geometry at render time, creating hyper-realistic depth that traditional normal maps cannot achieve.
* **Why Use This Skill (Rationale)**: Traditional modeling of microscopic surface details (like brick mortar, concrete pores, or rock crevices) is computationally impossible. PBR materials allow you to offload millions of polygons worth of detail into texture data. Furthermore, using specific mathematical converter nodes (like `Invert` for Gloss maps or `Hue/Saturation` for color tweaking) gives you ultimate art directability without needing to edit the raw image files externally.
* **Overall Applicability**: This is the foundational skill for photorealistic texturing. It applies to architectural visualization, hard-surface props, organic environments, and any scenario where physical accuracy of light bouncing off a surface is required. 
* **Value Addition**: Transforms a flat, mathematically perfect 3D primitive into a realistic, tactile surface with accurate light response, microsurface scattering, and physical depth via true displacement.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A standard plane or primitive mesh.
  - **Topology**: To use True Displacement, the mesh requires high vertex density. This is achieved using a `Subdivision Surface` modifier (set to `Simple` so the edges don't smooth into an oval).
  - **Advanced (Cycles)**: Using "Adaptive Subdivision" (an Experimental Cycles feature) automatically subdivides the mesh based on its distance from the camera, optimizing memory while maximizing detail.
* **Step B: Materials & Shading**
  - **Shader Model**: `Principled BSDF`.
  - **Mapping Architecture**: A `Texture Coordinate` node (UV or Generated) piped into a `Mapping` node ensures uniform scale adjustments across all texture maps simultaneously.
  - **Color Map**: Set to `sRGB` color space. Wired into `Base Color`. Can be routed through a `Hue/Saturation/Value` or `RGB Curves` node for non-destructive color grading.
  - **Gloss to Roughness**: Gloss maps are the inverse of Roughness maps. The workflow routes a `Non-Color` Gloss map through an `Invert` node before plugging it into the `Roughness` socket.
  - **Normal Map**: `Non-Color` data routed through a `Normal Map` (or `Bump`) node to dictate light scattering angles without changing actual geometry.
  - **True Displacement**: `Non-Color` height data routed through a `Displacement` node (Midlevel: 0.0, Scale: 0.1) and plugged directly into the `Material Output` node.
* **Step C: Lighting & Rendering Context**
  - **Engine**: Cycles is strictly recommended here. While EEVEE handles Base Color and Normals well, it cannot natively handle true material displacement without geometry nodes.
  - **Material Settings**: To enable true displacement, the material's properties must have `Settings > Surface > Displacement` changed from the default "Bump Only" to "Displacement and Bump".

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| True Displacement Geometry | `bpy.ops.mesh.primitive_plane_add` + `Subdivision Surface` Modifier | True displacement requires high-density geometry to physically push vertices. |
| Shading Architecture | Shader Node Tree (Principled BSDF) | Required to wire the complex PBR logic. |
| Textures | Procedural Textures (`ShaderNodeTexVoronoi`) | External image files (like the Poliigon textures in the video) break in standalone scripts. Procedural textures are used here to mimic the Color, Gloss, Normal, and Height map data completely natively. |

> **Feasibility Assessment**: 100% of the *architectural logic* is reproduced. Because we cannot safely download external PBR image sets in an isolated script, I have swapped the `Image Texture` nodes for a procedural `Voronoi` texture network. The *wiring structure* (Mapping, Hue/Sat, Gloss Inversion, Normal, Displacement, and Material Settings) strictly matches the tutorial's advanced PBR workflow.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Surface",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.7, 0.6),
    **kwargs,
) -> str:
    """
    Create a highly detailed PBR material setup demonstrating true displacement, 
    gloss inversion, and normal mapping on a subdivided plane.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created plane.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: Base tint for the procedural rock/paving surface.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import bpy

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Enable Cycles as it is required for True Displacement
    scene.render.engine = 'CYCLES'
    if scene.cycles.feature_set != 'EXPERIMENTAL':
        # Recommended for adaptive subdivision, but standard works too
        pass

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface for displacement geometry
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 6        # High level for viewport displacement
    subsurf.render_levels = 6 # High level for render displacement

    # === Step 2: Build PBR Material Architecture ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    
    # CRITICAL: Tell Blender to use true physical displacement, not just bump
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'
    
    obj.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Define Core Nodes
    output_node = nodes.new(type="ShaderNodeOutputMaterial")
    output_node.location = (1200, 0)
    
    bsdf_node = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf_node.location = (800, 200)
    
    # 1. Texture Coordinate & Mapping (Node Wrangler Ctrl+T logic)
    tex_coord = nodes.new(type="ShaderNodeTexCoord")
    tex_coord.location = (-800, 0)
    
    mapping = nodes.new(type="ShaderNodeMapping")
    mapping.location = (-600, 0)
    # Uniformly scale the texture across the surface
    mapping.inputs['Scale'].default_value = (3.0, 3.0, 3.0)
    
    # 2. Procedural Texture Generator (Acting as our downloaded Image Textures)
    # In a real workflow, this would be 5 separate Image Texture nodes.
    # We use Voronoi here to generate an interesting bumpy stone/paving pattern.
    texture = nodes.new(type="ShaderNodeTexVoronoi")
    texture.location = (-400, 0)
    
    # 3. BASE COLOR Workflow
    # Video tip: Tweak base colors using ColorRamp and Hue/Sat nodes
    color_ramp = nodes.new(type="ShaderNodeValToRGB")
    color_ramp.location = (-100, 300)
    color_ramp.color_ramp.elements[0].color = (0.05, 0.05, 0.05, 1.0)
    color_ramp.color_ramp.elements[1].color = (material_color[0], material_color[1], material_color[2], 1.0)
    
    hue_sat = nodes.new(type="ShaderNodeHueSaturation")
    hue_sat.location = (200, 300)
    hue_sat.inputs['Saturation'].default_value = 1.1 # Slight boost
    
    # 4. GLOSS TO ROUGHNESS Workflow
    # Video tip: If you download a Gloss map, you must Invert it for the Roughness socket
    invert_gloss = nodes.new(type="ShaderNodeInvert")
    invert_gloss.location = (200, 100)
    
    # 5. NORMAL MAP Workflow
    # Video tip: Non-color data into a Normal Map (or Bump) node
    bump_node = nodes.new(type="ShaderNodeBump")
    bump_node.location = (200, -100)
    bump_node.inputs['Strength'].default_value = 0.5
    
    # 6. DISPLACEMENT Workflow
    # Video tip: Midlevel 0.0, Scale adjusted low (e.g., 0.1)
    displacement_node = nodes.new(type="ShaderNodeDisplacement")
    displacement_node.location = (800, -200)
    displacement_node.inputs['Midlevel'].default_value = 0.0
    displacement_node.inputs['Scale'].default_value = 0.1
    
    # === Step 3: Wire Everything Together ===
    # Coordinate Mapping
    links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], texture.inputs['Vector'])
    
    # Color Branch
    links.new(texture.outputs['Distance'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], hue_sat.inputs['Color'])
    links.new(hue_sat.outputs['Color'], bsdf_node.inputs['Base Color'])
    
    # Specular / Reflection Branch (Using raw distance value)
    links.new(texture.outputs['Distance'], bsdf_node.inputs['Specular IOR Level'])
    
    # Roughness Branch (Demonstrating Gloss inversion)
    links.new(texture.outputs['Distance'], invert_gloss.inputs['Color'])
    links.new(invert_gloss.outputs['Color'], bsdf_node.inputs['Roughness'])
    
    # Normal Branch
    links.new(texture.outputs['Distance'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], bsdf_node.inputs['Normal'])
    
    # Displacement Branch
    links.new(texture.outputs['Distance'], displacement_node.inputs['Height'])
    
    # Final Output
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
    links.new(displacement_node.outputs['Displacement'], output_node.inputs['Displacement'])

    return f"Created '{object_name}' at {location} configured with advanced PBR shading and True Displacement. Switch viewport to Cycles Rendered view to see physical displacement."
```