### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural PBR Shader Setup with True Micro-Displacement

* **Core Visual Mechanism**: The defining technique is routing multiple texture channels (Base Color, Roughness, Normal, Height) into a single `Principled BSDF` and `Displacement` node, combined with enabling Cycles' true material displacement. This physically deforms the mesh geometry at render time based on the height map, creating highly realistic, self-shadowing silhouettes that normal mapping alone cannot achieve.

* **Why Use This Skill (Rationale)**: True displacement is essential for photorealistic close-ups of rough surfaces (terrain, rock walls, bark, brick). By subdividing the mesh heavily and using a displacement map, the surface interacts with grazing light naturally, casting realistic micro-shadows and breaking up the perfectly straight polygonal edges of base primitives.

* **Overall Applicability**: Used extensively for environmental storytelling, nature renders, architectural visualization, and hero props where surface tactile quality is paramount. It bridges the gap between low-poly modeling and high-poly sculpting.

* **Value Addition**: Transforms a completely flat, featureless plane into a highly detailed, physically tactile surface without requiring manual sculpting. It establishes a robust, reusable pipeline for applying any PBR texture set (or procedural equivalent) to geometry.


### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A simple flat plane or low-resolution grid.
  - **Modifiers**: A `Subdivision Surface` modifier is applied with high levels (e.g., 5 or 6). True displacement requires dense vertex topology to deform; a low-poly mesh will look jagged even with displacement enabled.
  - **Topology**: Simple grid-like quads are ideal to ensure uniform subdivision and predictable displacement artifacts.

* **Step B: Materials & Shading**
  - **Shader Model**: `Principled BSDF` handles the core lighting calculations.
  - **Displacement Setup**: A `Displacement` node is connected directly to the Material Output's Displacement socket. Crucially, the material's settings must be changed from the default "Bump Only" to "Displacement and Bump" (`mat.cycles.displacement_method = 'BOTH'`).
  - **Procedural Implementation**: Because external image files cannot be guaranteed, the script uses a complex procedural `Noise Texture` to simulate the PBR maps. The single noise source drives the Color (via ColorRamp), Roughness (via ColorRamp), Normal (via Bump node), and Displacement, mimicking how an image-based PBR set correlates these channels.

* **Step C: Lighting & Rendering Context**
  - **Render Engine**: **Cycles is strictly required** for true material displacement. EEVEE will only render the height map as a bump effect, leaving the mesh silhouette completely flat.
  - **Lighting**: A strong directional light (like a Sun light with strength 5.0, angled at 45 degrees) is best to highlight the physical self-shadowing created by the displaced peaks and valleys.

* **Step D: Animation & Dynamics**
  - While typically static, procedural displacement can be animated by changing the Noise Texture from 3D to 4D and animating the `W` value, creating rippling or morphing terrain effects.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Geometry & Topology | `bmesh.ops.create_grid` + Subdivision Modifier | Creates a clean, safe topological base with high non-destructive vertex density for the displacement to act upon. |
| PBR Channel Mapping | Shader Node Tree (`Principled BSDF`) | Mirrors the Node Wrangler `Ctrl+Shift+T` workflow from the tutorial, explicitly routing color, roughness, and normal data. |
| True Displacement | `mat.cycles.displacement_method` + `Displacement` Node | This is the core secret of the tutorial: moving beyond bump maps to physically alter geometry at render time. |
| Image Textures | Procedural Textures (`Noise`) | **Adaptation**: External downloaded images break automated reproducibility. I emulate the PBR texture set using procedural noise to ensure the script runs standalone anywhere. |

> **Feasibility Assessment**: 100% of the *technical setup* is reproduced (the node architecture, the modifier stack, and the render engine configuration for true displacement). About 60% of the *specific visual look* of the video is reproduced, because a photo-scanned rock image texture is replaced by an adaptable procedural rock/dirt generator to guarantee the code executes without missing file errors.

#### 3b. Complete Reproduction Code

```python
def create_pbr_displaced_surface(
    scene_name: str = "Scene",
    object_name: str = "Displaced_PBR_Surface",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    base_color_dark: tuple = (0.15, 0.12, 0.1),  # Dark earthy brown
    base_color_light: tuple = (0.5, 0.45, 0.4),  # Light dusty stone
    displacement_scale: float = 0.25,
    subdivision_levels: int = 6,
    **kwargs,
) -> str:
    """
    Creates a highly subdivided plane with a fully routed procedural PBR material,
    configured for true mesh displacement in the Cycles render engine.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        base_color_dark: RGB base color for the "valleys" (0-1).
        base_color_light: RGB base color for the "peaks" (0-1).
        displacement_scale: Strength/height of the physical displacement.
        subdivision_levels: Number of subdivision levels (higher = more detail, slower).
        **kwargs: Additional options.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Force Cycles Engine for True Displacement ===
    # Displacement mapping physically moving vertices requires Cycles.
    scene.render.engine = 'CYCLES'

    # === Step 2: Create Base Geometry ===
    mesh = bpy.data.meshes.new(f"{object_name}_mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # Use bmesh to create a basic grid
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=4, y_segments=4, size=2.0)
    bm.to_mesh(mesh)
    bm.free()

    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))

    # Add Subdivision Surface modifier to provide geometry for displacement
    subdiv = obj.modifiers.new(name="Subdivision_for_Displacement", type='SUBSURF')
    subdiv.levels = subdivision_levels
    subdiv.render_levels = subdivision_levels
    subdiv.subdivision_type = 'SIMPLE' # Keep square edges

    # === Step 3: Build PBR Material Setup ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)

    # CRITICAL: Tell Cycles to use actual vertex displacement, not just bump
    mat.cycles.displacement_method = 'BOTH' # Displacement and Bump

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Nodes
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (1200, 0)

    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.location = (800, 0)

    disp_node = nodes.new(type='ShaderNodeDisplacement')
    disp_node.location = (800, -300)
    disp_node.inputs['Midlevel'].default_value = 0.5
    disp_node.inputs['Scale'].default_value = displacement_scale

    # Procedural Texture Generator (Acting as our downloaded PBR map)
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)

    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-400, 0)

    # Base noise for rocky height
    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.location = (-200, 0)
    noise.inputs['Scale'].default_value = 4.0
    noise.inputs['Detail'].default_value = 15.0
    noise.inputs['Roughness'].default_value = 0.65

    # Albedo / Base Color Map Simulation
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (300, 200)
    color_ramp.color_ramp.elements[0].color = (*base_color_dark, 1.0)
    color_ramp.color_ramp.elements[1].color = (*base_color_light, 1.0)
    color_ramp.color_ramp.elements[0].position = 0.35
    color_ramp.color_ramp.elements[1].position = 0.65

    # Roughness Map Simulation (peaks are drier/rougher, valleys are slightly smoother)
    rough_ramp = nodes.new(type='ShaderNodeValToRGB')
    rough_ramp.location = (300, -50)
    rough_ramp.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1.0)
    rough_ramp.color_ramp.elements[1].color = (0.95, 0.95, 0.95, 1.0)

    # Normal / Bump Map Simulation for micro details
    bump = nodes.new(type='ShaderNodeBump')
    bump.location = (300, -300)
    bump.inputs['Distance'].default_value = 0.05
    bump.inputs['Strength'].default_value = 0.8

    # === Step 4: Route the PBR Channels ===
    # Coordinates -> Noise
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])

    # Noise -> Color
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])

    # Noise -> Roughness
    links.new(noise.outputs['Fac'], rough_ramp.inputs['Fac'])
    links.new(rough_ramp.outputs['Color'], principled.inputs['Roughness'])

    # Noise -> Normal (Micro details)
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], principled.inputs['Normal'])

    # Noise -> True Displacement (Macro silhouette)
    links.new(noise.outputs['Fac'], disp_node.inputs['Height'])
    
    # Final connections to Output
    links.new(principled.outputs['BSDF'], out_node.inputs['Surface'])
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])

    return f"Created '{object_name}' with procedural PBR mapping and Cycles true displacement at {location}."
```