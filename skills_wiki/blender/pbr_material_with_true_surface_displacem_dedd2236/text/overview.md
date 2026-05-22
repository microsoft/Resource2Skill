### 1. High-level Design Pattern Extraction

> **Skill Name**: PBR Material with True Surface Displacement

* **Core Visual Mechanism**: The defining technique is the use of a **Displacement Node** combined with Cycles' native material displacement settings (`Displacement Only` or `Displacement and Bump`). Unlike standard normal or bump mapping which only fakes light interaction, this technique physically deforms the mesh geometry at render time based on a grayscale height map, creating real silhouettes, self-occlusion, and deep shadows.
* **Why Use This Skill (Rationale)**: Bump and Normal maps break down at grazing angles because the underlying geometry remains flat. True displacement pushes vertices in 3D space, making surfaces like rocky terrain, brick walls, or tree bark look photorealistic from any camera angle.
* **Overall Applicability**: Essential for close-up architectural visualization, realistic landscape rendering, and hero props where surface silhouette and deep texture details are critical.
* **Value Addition**: Transforms a simple, flat 2D plane into complex, high-resolution 3D geometry entirely through shading data, keeping the viewport lightweight while delivering cinematic render quality.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A simple planar mesh.
  - **Modifiers**: A Subdivision Surface modifier set to 'Simple' with high iteration levels (6-7) to provide enough vertex density for the displacement map to physically push around. 
  - **Topology**: Dense, evenly spaced quads are strictly required.
* **Step B: Materials & Shading**
  - **Shader Model**: Principled BSDF.
  - **Displacement**: A grayscale height map (in the tutorial, an external image; in our code, procedural Voronoi/Noise) is fed into a `Displacement` node, which is then connected to the Material Output's Displacement socket.
  - **Critical Setting**: The material's property must be explicitly set from the default "Bump Only" to `Displacement Only` or `Displacement and Bump`.
* **Step C: Lighting & Rendering Context**
  - **Render Engine**: **Cycles is strictly required.** EEVEE (prior to Blender 4.2) does not support true material displacement.
  - **Lighting**: A Sun light with a relatively high angle (11.4° in the video) and strong intensity to cast soft but distinct micro-shadows within the displaced crevices.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

Since automated agents cannot reliably browse web pages, extract specific `.zip` files, and load local file paths dynamically, the tutorial's reliance on downloading external textures from Poly Haven must be adapted. 

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **High-Res Geometry** | `bpy.ops.mesh.primitive_plane_add` + Subsurf Modifier | Recreates the manual edit-mode subdivisions shown in the video, keeping the base mesh clean. |
| **PBR Textures** | Procedural Shader Nodes (Voronoi + Noise) | **Adaptation:** Replaces the downloaded image textures with procedural math nodes that generate a rocky heightmap, Albedo, and Roughness map without external dependencies. |
| **True Displacement** | `mat.cycles.displacement_method` + Cycles Engine | Directly reproduces the crucial "Settings -> Surface -> Displacement" workflow taught in the tutorial. |
| **Lighting Context** | `bpy.data.lights.new(type='SUN')` | Replicates the Sun light added at 1:16 in the video to showcase the displacement shadows. |

> **Feasibility Assessment**: 90% — The code perfectly reproduces the technical workflow (Nodes + Displacement Settings + Cycles + Subdivision). The only difference is the use of generated procedural textures instead of the specific downloaded Poly Haven rock image.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_RockWall",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.35, 0.25, 0.20),
    **kwargs,
) -> str:
    """
    Creates a highly subdivided plane with true PBR material displacement in Cycles.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the procedural rock.
        
    Returns:
        Status string describing the created setup.
    """
    import bpy
    import math
    from mathutils import Vector

    # Get scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Engine Setup ===
    # True material displacement requires Cycles
    scene.render.engine = 'CYCLES'

    # === Step 2: Create Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    plane = bpy.context.active_object
    plane.name = object_name
    plane.scale = (scale, scale, scale)

    # Subdivide heavily to provide vertices for displacement
    subsurf = plane.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 7        # Viewport subdivision
    subsurf.render_levels = 7 # Render subdivision

    # === Step 3: Build PBR Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    plane.data.materials.append(mat)

    # CRITICAL: Enable true displacement in material settings
    mat.cycles.displacement_method = 'DISPLACEMENT'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Output & BSDF Nodes
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (1000, 0)

    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf_node.location = (600, 100)

    # -- Procedural Texture Generation (Replacing external downloaded images) --
    # Voronoi for chunky rock shapes and cracks
    voronoi = nodes.new(type='ShaderNodeTexVoronoi')
    voronoi.feature = 'DISTANCE_TO_EDGE'
    voronoi.inputs['Scale'].default_value = 3.5
    voronoi.location = (-600, 200)

    # Noise for surface grit/detail
    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 25.0
    noise.inputs['Detail'].default_value = 15.0
    noise.location = (-600, -100)

    # Combine them for the height map
    mix_height = nodes.new(type='ShaderNodeMath')
    mix_height.operation = 'ADD'
    mix_height.location = (-200, 50)
    links.new(voronoi.outputs['Distance'], mix_height.inputs[0])
    
    # Scale down noise impact
    mult_noise = nodes.new(type='ShaderNodeMath')
    mult_noise.operation = 'MULTIPLY'
    mult_noise.inputs[1].default_value = 0.15
    mult_noise.location = (-400, -100)
    links.new(noise.outputs['Fac'], mult_noise.inputs[0])
    links.new(mult_noise.outputs['Value'], mix_height.inputs[1])

    # Displacement Node
    disp_node = nodes.new(type='ShaderNodeDisplacement')
    disp_node.inputs['Scale'].default_value = 0.2 * scale
    disp_node.inputs['Midlevel'].default_value = 0.0
    disp_node.location = (600, -200)

    # Color Ramp for Albedo (Base Color)
    ramp_color = nodes.new(type='ShaderNodeValToRGB')
    ramp_color.color_ramp.elements[0].position = 0.0
    ramp_color.color_ramp.elements[0].color = (0.02, 0.02, 0.02, 1.0) # Dark cracks
    ramp_color.color_ramp.elements[1].position = 0.4
    ramp_color.color_ramp.elements[1].color = (*material_color, 1.0)  # Main rock color
    ramp_color.location = (200, 300)

    # Color Ramp for Roughness
    ramp_rough = nodes.new(type='ShaderNodeValToRGB')
    ramp_rough.color_ramp.elements[0].position = 0.0
    ramp_rough.color_ramp.elements[0].color = (0.9, 0.9, 0.9, 1.0) # Rough rock
    ramp_rough.color_ramp.elements[1].position = 1.0
    ramp_rough.color_ramp.elements[1].color = (0.5, 0.5, 0.5, 1.0) # Slightly smoother edges
    ramp_rough.location = (200, 0)

    # -- Connect the PBR Network --
    # Drive color and roughness from the combined height map
    links.new(mix_height.outputs['Value'], ramp_color.inputs['Fac'])
    links.new(mix_height.outputs['Value'], ramp_rough.inputs['Fac'])

    # Plug into Principled BSDF
    links.new(ramp_color.outputs['Color'], bsdf_node.inputs['Base Color'])
    links.new(ramp_rough.outputs['Color'], bsdf_node.inputs['Roughness'])

    # Plug Height into Displacement
    links.new(mix_height.outputs['Value'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], output_node.inputs['Displacement'])
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])

    # === Step 4: Add Complementary Lighting ===
    # Add Sun light to showcase displacement shadows (as shown in tutorial)
    light_data = bpy.data.lights.new(name=f"{object_name}_Sun", type='SUN')
    light_data.energy = 5.0
    light_data.angle = math.radians(11.4) # Soft shadow angle from video
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_Sun", object_data=light_data)
    scene.collection.objects.link(light_obj)
    
    # Position sun slightly offset and angled down
    light_obj.location = (location[0] + 5, location[1] - 5, location[2] + 10)
    light_obj.rotation_euler = (math.radians(45), 0, math.radians(45))

    return f"Created PBR displaced plane '{object_name}' with procedural texture and Sun light in Cycles."
```