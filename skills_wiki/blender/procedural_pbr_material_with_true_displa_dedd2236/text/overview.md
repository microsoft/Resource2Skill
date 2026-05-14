### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural PBR Material with True Displacement

* **Core Visual Mechanism**: True geometry micro-displacement in rendering. This technique utilizes a heavily subdivided mesh, a material configured with `Displacement Only` settings, and the Cycles render engine to physically alter the geometry silhouette based on a height map, casting physically accurate shadows.
* **Why Use This Skill (Rationale)**: While normal and bump maps fake depth by changing how light bounces off flat polygons, true displacement pushes actual vertices. This creates realistic self-shadowing, accurate silhouettes, and high-fidelity surface details essential for close-up shots of natural surfaces like rock, bark, or ground. 
* **Overall Applicability**: Terrains, rock walls, close-up architectural details (brick, cobblestone), and photorealistic product/environment renders where silhouette detail matters.
* **Value Addition**: Transforms a flat, low-polygon plane into a complex, high-resolution 3D surface without requiring manual sculpting or destructive high-poly modeling.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A simple flat Plane.
  - **Modifiers**: A Subdivision Surface modifier (set to `Simple` or `Catmull-Clark`) with a high subdivision level (e.g., 6) is applied to provide enough vertex density for the displacement map to move.
* **Step B: Materials & Shading**
  - **Shader Model**: Principled BSDF.
  - **Displacement**: A `ShaderNodeDisplacement` node connected to the Material Output's Displacement socket. 
  - **Material Settings**: Under Material Properties > Settings > Surface, the Displacement method *must* be changed from "Bump Only" to "Displacement Only" or "Displacement and Bump".
  - **Maps**: Instead of relying on external downloaded images (which break self-containment), this implementation uses built-in procedural `Noise` and `ColorRamp` nodes to generate Base Color, Roughness, and Height maps on the fly.
* **Step C: Lighting & Rendering Context**
  - **Engine**: **Cycles is mandatory.** True material displacement does not work the same way in EEVEE.
  - **Lighting**: A strong, angled directional light (Sun light with energy ~5.0) is crucial to showcase the self-shadowing created by the physical displacement.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base Geometry | `bpy.ops.mesh.primitive_plane_add` + Subdivision Modifier | Fast generation; Subdivision modifier provides the non-destructive topological density required for displacement. |
| Material Definition | Shader node tree | Generates procedural maps (Noise/Musgrave) instead of external images to ensure self-contained, crash-free execution. |
| Displacement Engine | Cycles Material Settings | Setting `mat.cycles.displacement_method = 'DISPLACEMENT'` and switching to Cycles is the only way to achieve true silhouette-altering displacement. |

> **Feasibility Assessment**: 90%. The code accurately reproduces the core technical pipeline of true displacement (dense mesh + displacement nodes + Cycles settings + Sun light). However, because automated agents cannot reliably download and unpack `.zip` files from external sites, the downloaded PolyHaven image textures are substituted with a robust procedural shader tree that mimics a rocky surface.

#### 3b. Complete Reproduction Code

```python
def create_procedural_displacement_surface(
    scene_name: str = "Scene",
    object_name: str = "DisplacedRockWall",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.35, 0.25, 0.20),
    add_sun_light: bool = True,
    **kwargs,
) -> str:
    """
    Creates a highly subdivided plane with a procedural PBR material utilizing True Displacement.
    Automatically switches the render engine to Cycles to enable the displacement effect.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created mesh object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the rock/surface in 0-1 range.
        add_sun_light: If True, adds a Sun light to showcase the displacement shadows.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # 1. Enable Cycles (True Displacement requires Cycles)
    scene.render.engine = 'CYCLES'
    
    # Enable experimental feature set for adaptive subdivision (optional but recommended for true micro-poly)
    scene.cycles.feature_set = 'SUPPORTED' 

    # 2. Create Base Geometry
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    plane = bpy.context.active_object
    plane.name = object_name
    plane.scale = (scale, scale, scale)

    # Add Subdivision Surface modifier for geometry density
    subsurf = plane.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 6  # Viewport levels
    subsurf.render_levels = 6 # Render levels

    # 3. Build Procedural PBR Material
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    plane.data.materials.append(mat)
    
    # VERY IMPORTANT: Enable true displacement in material settings
    mat.cycles.displacement_method = 'DISPLACEMENT'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes safely
    for node in nodes:
        nodes.remove(node)

    # Add output and BSDF
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (400, 0)

    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    
    # Add Displacement Node
    disp = nodes.new(type='ShaderNodeDisplacement')
    disp.location = (0, -300)
    disp.inputs['Scale'].default_value = 0.2 * scale  # Adjust height amount based on object scale
    disp.inputs['Midlevel'].default_value = 0.5

    # Add Texture Map Generator (Procedural Noise)
    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.location = (-600, 0)
    noise.inputs['Scale'].default_value = 5.0
    noise.inputs['Detail'].default_value = 15.0
    noise.inputs['Roughness'].default_value = 0.6

    # Add Color mapping
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (-300, 150)
    color_ramp.color_ramp.elements[0].color = (*material_color, 1.0)
    # Darker variant for recesses
    dark_color = (max(0, material_color[0]-0.15), max(0, material_color[1]-0.15), max(0, material_color[2]-0.15), 1.0)
    color_ramp.color_ramp.elements[1].color = dark_color
    color_ramp.color_ramp.elements[1].position = 0.7

    # Add Roughness mapping
    rough_ramp = nodes.new(type='ShaderNodeValToRGB')
    rough_ramp.location = (-300, -100)
    rough_ramp.color_ramp.elements[0].position = 0.3
    rough_ramp.color_ramp.elements[0].color = (0.6, 0.6, 0.6, 1.0)
    rough_ramp.color_ramp.elements[1].position = 0.8
    rough_ramp.color_ramp.elements[1].color = (0.9, 0.9, 0.9, 1.0)

    # Link everything together
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(noise.outputs['Fac'], rough_ramp.inputs['Fac'])
    
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(rough_ramp.outputs['Color'], bsdf.inputs['Roughness'])
    
    # Link Height to Displacement
    links.new(noise.outputs['Fac'], disp.inputs['Height'])
    
    # Link BSDF and Displacement to Output
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])
    links.new(disp.outputs['Displacement'], out_node.inputs['Displacement'])

    # 4. Add Lighting to showcase shadows (Optional but matches tutorial)
    if add_sun_light:
        bpy.ops.object.light_add(
            type='SUN', 
            location=(location[0] + 5, location[1] - 5, location[2] + 5)
        )
        sun = bpy.context.active_object
        sun.name = f"{object_name}_Sun"
        sun.data.energy = 5.0
        # Angle low on the horizon to highlight bumps
        sun.rotation_euler = (math.radians(60), 0, math.radians(45))
        
        # Deselect sun, reselect plane
        sun.select_set(False)
        plane.select_set(True)
        bpy.context.view_layer.objects.active = plane

    return f"Created '{object_name}' with True PBR Displacement (Cycles Render Engine enabled). Scene contains N+{'2' if add_sun_light else '1'} new objects."
```