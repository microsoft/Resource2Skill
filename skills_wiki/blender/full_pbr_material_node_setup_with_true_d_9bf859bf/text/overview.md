### 1. High-level Design Pattern Extraction

> **Skill Name**: Full PBR Material Node Setup with True Displacement

* **Core Visual Mechanism**: The core pattern is the physical simulation of a real-world material by separating its properties into distinct data maps. The technique routes a single texture coordinate space through multiple specific channels: Base Color, Roughness (using an inverted Gloss map), Normal (for light bending/fake detail), and Displacement (for actual geometric depth). The hallmark of this specific setup is the use of **True Displacement** via Cycles' Experimental Adaptive Subdivision, which physically pushes vertices at render time.

* **Why Use This Skill (Rationale)**: Photorealism cannot be achieved by color alone. Light needs to interact with micro-surface imperfections (Roughness), bounce off angular indentations (Normals), and cast physical self-shadows across macro-details (Displacement). This node architecture is the industry standard for translating flat data into a physically accurate 3D surface.

* **Overall Applicability**: This workflow is mandatory for any high-fidelity, photorealistic scene. It is used for architectural visualizations (brick walls, hardwood floors), environment design (muddy terrain, rocky surfaces), and hero product rendering. 

* **Value Addition**: Compared to a flat Principled BSDF, a full PBR setup adds crucial tactile realism. The inclusion of True Adaptive Displacement breaks the perfectly flat silhouette of standard 3D primitives, adding organic, believable depth that reacts accurately to dynamic lighting.


### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A simple 2D Plane primitive.
  - **Modifiers**: A Subdivision Surface modifier is applied. Crucially, Cycles' "Adaptive Subdivision" is enabled. This intelligently tessellates the mesh at render time based on how close the camera is, providing enough geometry for the displacement map to physically push the surface without crashing the viewport.

* **Step B: Materials & Shading**
  - **Shader Model**: Principled BSDF.
  - **Mapping Logic**: A `Texture Coordinate (UV)` node feeds into a `Mapping` node to control global tiling and scale.
  - **Procedural Substitution**: *(Note: To keep this reproducible without downloading external images, the tutorial's downloaded image maps are simulated using a procedural Voronoi texture).*
  - **Roughness/Gloss Inversion**: The tutorial explicitly demonstrates fixing a "Gloss" map by running it through an `Invert` node to properly feed the Principled BSDF's "Roughness" socket.
  - **Normal & Displacement**: The texture data is fed into a `Bump/Normal` node to affect lighting, and a `Displacement` node (with `midlevel` specifically set to `0.0` as taught in the video) plugged directly into the Material Output.

* **Step C: Lighting & Rendering Context**
  - **Render Engine**: **Cycles is strictly required.**
  - **Feature Set**: Must be set to **Experimental** to unlock Adaptive Subdivision.
  - **Material Property**: The material's specific displacement method must be manually changed from "Bump Only" to "Displacement and Bump".


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base Geometry & Tessellation | `bpy.ops.mesh` + Subdivision Modifier | Requires a mesh with adaptive subdivision for true displacement to function. |
| Material Architecture | Shader Node Tree | Direct programmatic construction of the node graph to replicate the video's exact routing (Mapping, Invert, Hue/Sat, Displacement). |
| Image Textures | Procedural Substitution | Procedural textures (Voronoi) are used in place of external JPGs to ensure the code executes cleanly without external file dependencies. |

> **Feasibility Assessment**: 100% of the *architectural logic* of the tutorial is reproduced. The specific visual output will look like a procedural cobblestone/organic surface rather than a downloaded brick texture, but the PBR node routing, gloss inversion, and experimental true displacement setup are identical to the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Surface",
    location: tuple = (0, 0, 0),
    scale: float = 2.0,
    material_color: tuple = (0.6, 0.2, 0.15),
    **kwargs,
) -> str:
    """
    Create a Full PBR Material Node Setup with True Displacement.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color mapping for the procedural texture.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Ensure Cycles is enabled, as True Displacement requires it
    if not bpy.context.preferences.addons.get('cycles'):
        bpy.ops.preferences.addon_enable(module='cycles')
    
    # === Step 1: Render Engine Setup ===
    # True displacement requires Cycles and the Experimental feature set
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface modifier
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'CATMULL_CLARK'
    
    # Enable Adaptive Subdivision (Only works when Cycles is Experimental)
    obj.cycles.use_adaptive_subdivision = True

    # === Step 3: Material Architecture ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    
    # CRITICAL: Tell the material to use True Displacement, not just bump
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'
    obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Material Output
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (1000, 0)

    # Principled BSDF
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.location = (600, 0)
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])

    # Mapping & Coordinates (Mimicking Ctrl+T from Node Wrangler)
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)

    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-600, 0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])

    # Procedural Texture (Substituting external downloaded maps)
    # Using Voronoi to simulate a stony/cobble height map
    texture = nodes.new(type='ShaderNodeTexVoronoi')
    texture.location = (-400, 0)
    texture.inputs['Scale'].default_value = 5.0
    links.new(mapping.outputs['Vector'], texture.inputs['Vector'])

    # 1. Base Color Setup
    # Simulates the Albedo map. Adds Hue/Saturation node as shown in video tips.
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (-100, 250)
    color_ramp.color_ramp.elements[0].color = (0.02, 0.02, 0.02, 1)
    color_ramp.color_ramp.elements[1].color = (*material_color, 1)
    links.new(texture.outputs['Distance'], color_ramp.inputs['Fac'])

    hue_sat = nodes.new(type='ShaderNodeHueSat')
    hue_sat.location = (200, 250)
    hue_sat.inputs['Saturation'].default_value = 1.1 # Slight boost
    links.new(color_ramp.outputs['Color'], hue_sat.inputs['Color'])
    links.new(hue_sat.outputs['Color'], principled.inputs['Base Color'])

    # 2. Roughness Setup
    # Simulates the video's technique of converting a Gloss map to Roughness via Invert
    invert = nodes.new(type='ShaderNodeInvert')
    invert.location = (200, 50)
    links.new(texture.outputs['Distance'], invert.inputs['Color'])
    links.new(invert.outputs['Color'], principled.inputs['Roughness'])

    # 3. Normal Setup
    # Converts grayscale data to Normal data
    bump = nodes.new(type='ShaderNodeBump')
    bump.location = (200, -150)
    bump.inputs['Strength'].default_value = 0.5
    links.new(texture.outputs['Distance'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], principled.inputs['Normal'])

    # 4. True Displacement Setup
    # Plugs directly into output. Midlevel set to 0.0 as explicitly warned in tutorial.
    displacement = nodes.new(type='ShaderNodeDisplacement')
    displacement.location = (600, -300)
    displacement.inputs['Midlevel'].default_value = 0.0
    displacement.inputs['Scale'].default_value = 0.15 # Kept subtle to prevent tearing
    links.new(texture.outputs['Distance'], displacement.inputs['Height'])
    links.new(displacement.outputs['Displacement'], output.inputs['Displacement'])

    return f"Created '{object_name}' with PBR node setup, True Displacement, and Adaptive Subdivision enabled."
```