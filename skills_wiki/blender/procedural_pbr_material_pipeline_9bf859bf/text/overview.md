# Agent_Skill_Distiller Strategy Document

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural PBR Material Pipeline

* **Core Visual Mechanism**: A complete Physically Based Rendering (PBR) shading pipeline. This pattern maps surface data (Base Color, Roughness, Normal, and Displacement) into a `Principled BSDF` and `Material Output`. It simulates the standard image-based texture workflow (Color, Gloss, Normal, Height) using procedural textures, utilizing inversion for roughness, bump/normal mapping for micro-details, and actual geometry displacement for macro-details.
* **Why Use This Skill (Rationale)**: PBR is the industry standard for realistic materials. Properly separating color, specular/roughness reflection data, and physical bump/displacement ensures that light interacts with the 3D surface accurately under any lighting condition. The inclusion of true displacement (via Adaptive Subdivision) breaks the perfect silhouette of a flat plane, adding immense realism.
* **Overall Applicability**: This is the foundational shading logic for almost every realistic object in a scene—from brick walls and cobblestone floors to rusted metals and organic surfaces.
* **Value Addition**: Transforms a flat, lifeless plane into a highly detailed, physically accurate surface that dynamically reacts to light, shadow, and camera angle.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A simple 2D Plane.
  - **Modifiers**: A `Subdivision Surface` modifier set to 'Simple'. To support true micro-polygon displacement, Adaptive Subdivision is enabled (requires Cycles feature set to 'Experimental').
* **Step B: Materials & Shading**
  - **Shader Model**: `Principled BSDF`.
  - **Texture Source**: A base `Noise Texture` drives all channels to simulate a downloaded texture pack.
  - **Base Color**: Noise mapped through a `ColorRamp` and a `Hue/Saturation` node to allow non-destructive tweaking of the brick/stone color.
  - **Roughness**: Simulates the "Gloss to Roughness" workflow. The texture is fed into an `Invert` node (since Roughness is the mathematical inverse of Glossiness), then plugged into the BSDF Roughness socket.
  - **Normals**: The texture is passed through a `Bump` node (acting in place of a Normal Map node) to generate fake lighting depth.
  - **Displacement**: The texture is passed through a `Displacement` node (converting scalar height to a displacement vector) and plugged directly into the `Material Output`. The material's surface setting is changed to 'Displacement and Bump'.
* **Step C: Lighting & Rendering Context**
  - **Render Engine**: Cycles is required. True displacement does not work in EEVEE.
  - **Settings**: Cycles `Feature Set` must be set to `Experimental` to unlock Adaptive Subdivision.
* **Step D: Animation & Dynamics (if applicable)**
  - N/A. This is a static material setup.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base Geometry | `bpy.ops.mesh.primitive_plane_add` + `Modifiers` | Provides a clean, flat canvas. Subsurf modifier allows the geometry to be displaced. |
| Material Pipeline | Shader Node Tree | Direct node-by-node construction perfectly replicates the PBR routing logic taught in the video. |
| Texture Generation | Procedural (`ShaderNodeTexNoise`) | Ensures the code is self-contained and avoids missing external image file errors, while maintaining the exact same routing architecture. |

> **Feasibility Assessment**: 95% — The code perfectly reproduces the PBR node mapping structure, material settings, and adaptive subdivision setup shown in the video. The only difference is the use of a procedural noise texture instead of downloaded external image files to ensure execution stability.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Surface",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.25, 0.25),
    **kwargs,
) -> str:
    """
    Create a highly detailed PBR material surface using true displacement.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created plane.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the surface.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy

    # Get scene and set up Render Engine for Displacement (Cycles Experimental)
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface modifier for Adaptive Displacement
    subdiv_mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv_mod.subdivision_type = 'SIMPLE'
    subdiv_mod.levels = 3
    subdiv_mod.render_levels = 3
    
    # Enable Adaptive Subdivision if Cycles is available on the object
    if hasattr(obj, 'cycles'):
        obj.cycles.use_adaptive_subdivision = True

    # === Step 2: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)

    # Enable Displacement and Bump in material settings
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'

    tree = mat.node_tree
    nodes = tree.nodes
    links = tree.links

    # Clear default nodes
    nodes.clear()

    # Output Node
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1000, 0)

    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (600, 0)
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    # Mapping Coordinates (Ctrl+T setup)
    tc_node = nodes.new('ShaderNodeTexCoord')
    tc_node.location = (-800, 0)

    map_node = nodes.new('ShaderNodeMapping')
    map_node.location = (-600, 0)
    links.new(tc_node.outputs['UV'], map_node.inputs['Vector'])

    # Base Procedural Texture (Acts as our downloaded Image files)
    noise_node = nodes.new('ShaderNodeTexNoise')
    noise_node.location = (-400, 0)
    noise_node.inputs['Scale'].default_value = 10.0
    noise_node.inputs['Detail'].default_value = 15.0
    links.new(map_node.outputs['Vector'], noise_node.inputs['Vector'])

    # --- Channel 1: Base Color ---
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-100, 200)
    color_ramp.color_ramp.elements[0].color = (0.05, 0.05, 0.05, 1.0)
    color_ramp.color_ramp.elements[1].color = (material_color[0], material_color[1], material_color[2], 1.0)
    links.new(noise_node.outputs['Fac'], color_ramp.inputs['Fac'])

    hue_sat = nodes.new('ShaderNodeHueSaturation')
    hue_sat.location = (200, 200)
    links.new(color_ramp.outputs['Color'], hue_sat.inputs['Color'])
    links.new(hue_sat.outputs['Color'], bsdf.inputs['Base Color'])

    # --- Channel 2: Roughness (Simulating the Gloss -> Invert workflow) ---
    invert_node = nodes.new('ShaderNodeInvert')
    invert_node.location = (200, 0)
    links.new(noise_node.outputs['Fac'], invert_node.inputs['Color'])
    links.new(invert_node.outputs['Color'], bsdf.inputs['Roughness'])

    # --- Channel 3: Normal Map ---
    bump_node = nodes.new('ShaderNodeBump')
    bump_node.location = (200, -200)
    bump_node.inputs['Strength'].default_value = 0.5
    links.new(noise_node.outputs['Fac'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], bsdf.inputs['Normal'])

    # --- Channel 4: Displacement ---
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (600, -400)
    disp_node.inputs['Scale'].default_value = 0.1
    disp_node.inputs['Midlevel'].default_value = 0.5
    links.new(noise_node.outputs['Fac'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])

    return f"Created '{object_name}' with Procedural PBR Material Pipeline at {location}"
```