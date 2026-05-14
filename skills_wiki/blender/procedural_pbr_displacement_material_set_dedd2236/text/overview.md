### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural PBR Displacement Material Setup

* **Core Visual Mechanism**: Transforming a flat plane into a highly detailed, physically bumpy surface using shader-driven geometric displacement. The core technique involves feeding height data (via a `Displacement` node) into the `Material Output` node, combined with changing the Material Settings from "Bump Only" to "Displacement Only". This physically moves the mesh vertices at render time.
* **Why Use This Skill (Rationale)**: Manually modeling high-frequency details like cobblestones, rock faces, or rough tree bark is computationally expensive and difficult to iterate on. Displacement materials allow you to keep the base geometry simple (a flat plane or low-poly object) while deferring the complex geometric detail to the render engine.
* **Overall Applicability**: Essential for realistic environments. Used for ground terrain, brick walls, ocean waves, and close-up product shots requiring micro-surface details.
* **Value Addition**: Compared to a default primitive, this adds immense photorealism and dynamic silhouette changes without requiring manual sculpting.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A simple flat grid or plane.
  - **Topology Requirement**: True displacement requires a high density of vertices to move. The video does this by manually subdividing a plane multiple times. In code, a `Grid` primitive with many subdivisions (e.g., 100x100) paired with a `Subdivision Surface` modifier (set to 'Simple') provides the necessary resolution.
* **Step B: Materials & Shading**
  - **Shader Model**: Principled BSDF.
  - **Texture Maps**: While the video uses downloaded image textures (Color, Roughness, Normal, Height), a self-contained code snippet must simulate this procedurally. We use `Noise Texture` nodes to generate procedural maps that mimic these images.
  - **Node Routing**:
    - Procedural Noise -> `ColorRamp` -> BSDF `Base Color`
    - Procedural Noise -> `ColorRamp` -> BSDF `Roughness`
    - High-frequency Procedural Noise -> `Bump` -> BSDF `Normal`
    - Procedural Noise -> `Displacement` (Scale: 0.2) -> Material Output `Displacement`
  - **Critical Setting**: Under Material Properties -> Settings -> Surface, `Displacement` must be set to `DISPLACEMENT` (or `BOTH`).
* **Step C: Lighting & Rendering Context**
  - **Render Engine**: **Cycles is strictly required** for the material displacement setting to actually move geometry. EEVEE will only render it as a bump map.
  - **Lighting**: A strong, angled `Sun` light (Strength 5.0, as shown in the video) is necessary to cast deep shadows across the displaced geometry, revealing the depth.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Dense Base Geometry | `bpy.ops.mesh.primitive_grid_add` + Subsurf | Provides the high vertex count needed for the displacement to have physical effect without destructive editing. |
| PBR Texture Setup | Shader Node Tree | Procedurally re-creates the Color, Roughness, Normal, and Height map logic shown in the video using Noise instead of external files. |
| True Displacement | Material `cycles.displacement_method` | The required toggle to switch from standard bump mapping to actual vertex displacement. |

> **Feasibility Assessment**: 95%. The code reproduces the exact technical workflow, node architecture, and material settings from the tutorial. Because external image textures cannot be reliably downloaded via a standalone script, it substitutes them with advanced procedural noise networks that map to the exact same sockets, achieving a highly similar rocky terrain effect.

#### 3b. Complete Reproduction Code

```python
def create_pbr_displacement_terrain(
    scene_name: str = "Scene",
    object_name: str = "PBR_Terrain_Plane",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 5.0,
    base_color_dark: tuple = (0.05, 0.03, 0.02, 1.0),
    base_color_light: tuple = (0.35, 0.25, 0.18, 1.0),
    displacement_scale: float = 0.25,
    **kwargs,
) -> str:
    """
    Creates a highly subdivided plane with a procedural PBR material featuring true displacement.
    Note: Automatically switches the scene render engine to CYCLES to enable true displacement.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created mesh.
        location: (x, y, z) world-space position.
        scale: Size of the terrain grid.
        base_color_dark: (R, G, B, A) dark color for deep crevices.
        base_color_light: (R, G, B, A) light color for peaks.
        displacement_scale: How intense the physical displacement height is.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # 1. Force Cycles render engine (required for true displacement)
    scene.render.engine = 'CYCLES'
    # Optional: Enable experimental feature set for adaptive subdivision
    # scene.cycles.feature_set = 'EXPERIMENTAL'

    # 2. Create Dense Base Geometry
    # A 100x100 grid provides 10,000 faces, good base for displacement
    bpy.ops.mesh.primitive_grid_add(
        x_subdivisions=100, 
        y_subdivisions=100, 
        size=scale, 
        location=location
    )
    obj = bpy.context.active_object
    obj.name = object_name
    
    # Add Subdivision Surface modifier for even smoother displacement resolution
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE' # Keeps the grid square
    subsurf.levels = 2
    subsurf.render_levels = 3

    # 3. Create Material & Enable Displacement Setting
    mat = bpy.data.materials.new(name=f"M_{object_name}_PBR")
    mat.use_nodes = True
    
    # CRITICAL: Tell the material to actually move vertices, not just fake lighting
    mat.cycles.displacement_method = 'DISPLACEMENT' 
    obj.data.materials.append(mat)

    # 4. Build Procedural PBR Node Tree
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Output Nodes
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (1200, 0)

    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf_node.location = (800, 200)
    links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])

    # Coordinates
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    
    # Main Height/Structure Noise (acting as the Displacement/Height Map)
    macro_noise = nodes.new(type='ShaderNodeTexNoise')
    macro_noise.location = (-200, 0)
    macro_noise.inputs['Scale'].default_value = 3.0
    macro_noise.inputs['Detail'].default_value = 15.0
    macro_noise.inputs['Roughness'].default_value = 0.6
    links.new(tex_coord.outputs['Object'], macro_noise.inputs['Vector'])

    # Micro Detail Noise (acting as the specific Normal map)
    micro_noise = nodes.new(type='ShaderNodeTexNoise')
    micro_noise.location = (-200, -300)
    micro_noise.inputs['Scale'].default_value = 50.0
    micro_noise.inputs['Detail'].default_value = 5.0
    links.new(tex_coord.outputs['Object'], micro_noise.inputs['Vector'])

    # A. Color Map Routing
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (200, 300)
    color_ramp.color_ramp.elements[0].position = 0.35
    color_ramp.color_ramp.elements[0].color = base_color_dark
    color_ramp.color_ramp.elements[1].position = 0.65
    color_ramp.color_ramp.elements[1].color = base_color_light
    links.new(macro_noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf_node.inputs['Base Color'])

    # B. Roughness Map Routing
    rough_ramp = nodes.new(type='ShaderNodeValToRGB')
    rough_ramp.location = (200, 0)
    rough_ramp.color_ramp.elements[0].position = 0.2
    rough_ramp.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1.0) # Medium rough
    rough_ramp.color_ramp.elements[1].position = 0.8
    rough_ramp.color_ramp.elements[1].color = (0.9, 0.9, 0.9, 1.0) # Very rough
    links.new(macro_noise.outputs['Fac'], rough_ramp.inputs['Fac'])
    links.new(rough_ramp.outputs['Color'], bsdf_node.inputs['Roughness'])

    # C. Normal/Bump Map Routing
    bump_node = nodes.new(type='ShaderNodeBump')
    bump_node.location = (400, -200)
    bump_node.inputs['Strength'].default_value = 0.6
    bump_node.inputs['Distance'].default_value = 0.1
    links.new(micro_noise.outputs['Fac'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], bsdf_node.inputs['Normal'])

    # D. Displacement Map Routing
    disp_node = nodes.new(type='ShaderNodeDisplacement')
    disp_node.location = (800, -200)
    disp_node.inputs['Midlevel'].default_value = 0.5
    disp_node.inputs['Scale'].default_value = displacement_scale
    links.new(macro_noise.outputs['Fac'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])
    
    # 5. Add a Sun Light to highlight the displacement (as done in the video)
    # Check if a sun already exists, if not, create one
    if not any(l.type == 'SUN' for l in bpy.data.lights):
        sun_data = bpy.data.lights.new(name="Displacement_Sun", type='SUN')
        sun_data.energy = 5.0 # High strength to show shadows
        sun_obj = bpy.data.objects.new(name="Displacement_Sun_Obj", object_data=sun_data)
        scene.collection.objects.link(sun_obj)
        sun_obj.location = (0, 0, 10)
        sun_obj.rotation_euler = (0.785, 0.5, 0) # Angled to cast shadows across bumps

    return f"Created PBR terrain '{object_name}' with Cycles displacement enabled. Mesh is sub-divided grid at {location}."
```