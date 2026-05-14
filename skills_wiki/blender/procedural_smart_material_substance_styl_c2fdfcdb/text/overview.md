# Procedural "Smart Material" (Substance-Style Edge Wear & Dirt)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural "Smart Material" (Substance-Style Edge Wear & Dirt)

* **Core Visual Mechanism**: This technique brings the procedural texturing workflow of applications like Substance Painter directly into Blender's shader editor. By using mesh data nodes (`Geometry`, `Bevel`, `Ambient Occlusion`), the material dynamically generates masks for edges (to reveal bare metal), convex curves (to add highlights), and crevices (to accumulate dirt). 

* **Why Use This Skill (Rationale)**: Hand-painting wear and tear on complex hard-surface models is time-consuming and destructive. A "Smart Material" adapts automatically to the underlying geometry. If you change the mesh, extrude a face, or add a boolean cut, the edge wear and dirt will automatically recalculate and appear in the correct new locations.

* **Overall Applicability**: Essential for hard-surface modeling, sci-fi props, industrial visualization, and game asset creation. It is perfect for crates, mechs, weapons, and vehicles that require a weathered, lived-in look without relying on UV unwrapping or external texturing software.

* **Value Addition**: Transforms a basic, flat-colored mesh into a highly realistic, story-rich asset. The dynamic masks drive not only base color but also roughness and metallicity, making the asset react to lighting with physical accuracy (e.g., exposed metal edges catch bright highlights, while dirt-filled crevices are diffuse and rough).

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: Can be applied to any mesh. For the demonstration, a simple beveled cube with some inset faces works perfectly.
  - **Topology Requirement**: The `Pointiness` output relies on vertex data, so the mesh needs moderate vertex density to calculate smooth curvature. 

* **Step B: Materials & Shading**
  - **Shader Model**: Principled BSDF driven by a complex node network.
  - **Mask 1: Color Split**: Uses `Object` texture coordinates rotated 90 degrees on the Y-axis into a `Gradient Texture` to split the object into top and bottom colors.
  - **Mask 2: Ambient Occlusion (Dirt)**: A `Noise Texture` is plugged into the Color input of an `Ambient Occlusion` node to create procedural, patchy dirt that only accumulates in crevices.
  - **Mask 3: Curvature (Highlight)**: The `Pointiness` attribute is clamped via a `ColorRamp` and `Gamma` node to find convex curves, which are then used to lighten the base color.
  - **Mask 4: Edge Mask (Metal Wear)**: A `Vector Math` node calculates the `Dot Product` between the flat `Geometry` normal and a `Bevel` node normal. Where the normal bends (the edges), the dot product decreases. A `Map Range` node isolates this difference to create a perfect edge mask.
  - **PBR Routing**: The Edge Mask drives the `Metallic` input and lowers the `Roughness`. The AO dirt mask drives a `Bump` node and increases the `Roughness`.

* **Step C: Lighting & Rendering Context**
  - **Engine**: **Cycles is mandatory** for this specific setup, as the `Bevel` shader node (crucial for the edge mask) is only supported in Cycles. 
  - **Lighting**: HDRI lighting or a strong 3-point light setup is recommended so the metallic edges can catch specular highlights.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base Mesh generation | `bpy.ops.mesh` + bmesh insets | Creates instant crevices and edges for the shader masks to react to. |
| Mask Generation & Blending | Shader Node Tree | Procedural nodes (`Bevel`, `AO`, `Geometry`) are the only way to dynamically read mesh topology for texturing. |

> **Feasibility Assessment**: 100% reproduction of the core texturing logic. The code accurately recreates the exact node math (dot product of normals for edges, pointiness for curvature, AO for dirt) demonstrated in the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_smart_material_crate(
    scene_name: str = "Scene",
    object_name: str = "SmartCrate",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    top_color: tuple = (0.8, 0.5, 0.05, 1.0),
    bottom_color: tuple = (0.05, 0.1, 0.15, 1.0),
    **kwargs,
) -> str:
    """
    Creates a detailed mesh with a procedural "Smart Material" that automatically 
    detects edges for metal wear and crevices for dirt.
    
    NOTE: This material relies on the Bevel shader node, which requires the Cycles render engine.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Ensure Cycles is active, as the Bevel shader node is Cycles-only
    scene.render.engine = 'CYCLES'

    # === Step 1: Create Test Geometry ===
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Subdivide and inset to create crevices/edges for the material to detect
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj.data)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=3)
    # Inset all faces slightly to create a paneling effect
    bmesh.ops.inset_individual(bm, faces=bm.faces, thickness=0.1, depth=-0.05)
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Add a physical bevel modifier for macroscopic edges
    bev_mod = obj.modifiers.new(name="Bevel", type='BEVEL')
    bev_mod.width = 0.03
    bev_mod.segments = 3

    # === Step 2: Build the Smart Material Node Tree ===
    mat = bpy.data.materials.new(name=f"{object_name}_SmartMat")
    mat.use_nodes = True
    obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Nodes
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (2000, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (1700, 0)
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    # --- Mask 1: Gradient Base Color Split ---
    tc = nodes.new('ShaderNodeTexCoord')
    tc.location = (-1200, 800)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-1000, 800)
    mapping.inputs['Rotation'].default_value[1] = math.radians(90) # Rotate 90deg on Y
    links.new(tc.outputs['Object'], mapping.inputs['Vector'])

    gradient = nodes.new('ShaderNodeTexGradient')
    gradient.location = (-800, 800)
    links.new(mapping.outputs['Vector'], gradient.inputs['Vector'])

    ramp_split = nodes.new('ShaderNodeValToRGB')
    ramp_split.location = (-600, 800)
    ramp_split.color_ramp.interpolation = 'CONSTANT'
    ramp_split.color_ramp.elements[0].position = 0.5
    links.new(gradient.outputs['Color'], ramp_split.inputs['Fac'])

    mix_base = nodes.new('ShaderNodeMixRGB')
    mix_base.location = (-300, 800)
    mix_base.inputs['Color1'].default_value = bottom_color
    mix_base.inputs['Color2'].default_value = top_color
    links.new(ramp_split.outputs['Color'], mix_base.inputs['Fac'])

    # --- Mask 2: Ambient Occlusion (Dirt) ---
    noise_ao = nodes.new('ShaderNodeTexNoise')
    noise_ao.location = (-1200, 500)
    noise_ao.inputs['Scale'].default_value = 15.0

    ao = nodes.new('ShaderNodeAmbientOcclusion')
    ao.location = (-1000, 500)
    ao.inputs['Distance'].default_value = 0.2
    links.new(noise_ao.outputs['Color'], ao.inputs['Color'])

    ramp_ao = nodes.new('ShaderNodeValToRGB')
    ramp_ao.location = (-800, 500)
    # Flipped ramp to isolate crevices as white
    ramp_ao.color_ramp.elements[0].color = (1, 1, 1, 1)
    ramp_ao.color_ramp.elements[1].color = (0, 0, 0, 1)
    ramp_ao.color_ramp.elements[0].position = 0.3
    ramp_ao.color_ramp.elements[1].position = 0.7
    links.new(ao.outputs['Color'], ramp_ao.inputs['Fac'])

    mix_dirt = nodes.new('ShaderNodeMixRGB')
    mix_dirt.location = (0, 600)
    mix_dirt.inputs['Color2'].default_value = (0.05, 0.04, 0.03, 1.0) # Dark brown dirt
    links.new(ramp_ao.outputs['Color'], mix_dirt.inputs['Fac'])
    links.new(mix_base.outputs['Color'], mix_dirt.inputs['Color1'])

    # --- Mask 3: Curvature (Highlights) ---
    geo = nodes.new('ShaderNodeNewGeometry')
    geo.location = (-1200, 200)

    ramp_curv = nodes.new('ShaderNodeValToRGB')
    ramp_curv.location = (-1000, 200)
    ramp_curv.color_ramp.elements[0].position = 0.48
    ramp_curv.color_ramp.elements[1].position = 0.52
    links.new(geo.outputs['Pointiness'], ramp_curv.inputs['Fac'])

    gamma = nodes.new('ShaderNodeGamma')
    gamma.location = (-700, 200)
    gamma.inputs['Gamma'].default_value = 2.0
    links.new(ramp_curv.outputs['Color'], gamma.inputs['Color'])

    noise_curv = nodes.new('ShaderNodeTexNoise')
    noise_curv.location = (-1000, 0)
    noise_curv.inputs['Scale'].default_value = 5.0

    math_curv = nodes.new('ShaderNodeMath')
    math_curv.operation = 'MULTIPLY'
    math_curv.location = (-500, 100)
    links.new(gamma.outputs['Color'], math_curv.inputs[0])
    links.new(noise_curv.outputs['Fac'], math_curv.inputs[1])

    mix_curv = nodes.new('ShaderNodeMixRGB')
    mix_curv.blend_type = 'SCREEN'
    mix_curv.location = (300, 500)
    mix_curv.inputs['Color2'].default_value = (0.5, 0.5, 0.5, 1.0) # Highlight amount
    links.new(math_curv.outputs['Value'], mix_curv.inputs['Fac'])
    links.new(mix_dirt.outputs['Color'], mix_curv.inputs['Color1'])

    # --- Mask 4: Edge Mask (Metal Wear) ---
    noise_edge = nodes.new('ShaderNodeTexNoise')
    noise_edge.location = (-1200, -300)
    noise_edge.inputs['Scale'].default_value = 8.0

    map_noise_edge = nodes.new('ShaderNodeMapRange')
    map_noise_edge.location = (-1000, -300)
    map_noise_edge.inputs[1].default_value = 0.2
    map_noise_edge.inputs[2].default_value = 0.8
    map_noise_edge.inputs[3].default_value = 0.01  # Min bevel radius
    map_noise_edge.inputs[4].default_value = 0.08  # Max bevel radius
    links.new(noise_edge.outputs['Fac'], map_noise_edge.inputs[0])

    bevel = nodes.new('ShaderNodeBevel')
    bevel.location = (-700, -300)
    bevel.samples = 6
    links.new(map_noise_edge.outputs['Result'], bevel.inputs['Radius'])

    # Dot product between Flat Normal and Beveled Normal
    dot_prod = nodes.new('ShaderNodeVectorMath')
    dot_prod.operation = 'DOT_PRODUCT'
    dot_prod.location = (-500, -300)
    links.new(bevel.outputs['Normal'], dot_prod.inputs[0])
    links.new(geo.outputs['Normal'], dot_prod.inputs[1])

    # Map Range to isolate the difference (edges)
    map_edge = nodes.new('ShaderNodeMapRange')
    map_edge.location = (-300, -300)
    map_edge.inputs[1].default_value = 0.69 # From Min
    map_edge.inputs[2].default_value = 1.0  # From Max
    map_edge.inputs[3].default_value = 1.0  # To Min (Inverts the output)
    map_edge.inputs[4].default_value = 0.0  # To Max
    links.new(dot_prod.outputs['Value'], map_edge.inputs[0])

    mix_edge = nodes.new('ShaderNodeMixRGB')
    mix_edge.location = (600, 400)
    mix_edge.inputs['Color2'].default_value = (0.7, 0.7, 0.75, 1.0) # Bare metal color
    links.new(map_edge.outputs['Result'], mix_edge.inputs['Fac'])
    links.new(mix_curv.outputs['Color'], mix_edge.inputs['Color1'])

    # --- PBR Attribute Routing ---
    # Color
    links.new(mix_edge.outputs['Color'], bsdf.inputs['Base Color'])

    # Metallic
    links.new(map_edge.outputs['Result'], bsdf.inputs['Metallic'])

    # Roughness (Dirt is rough, Metal edges are shiny)
    mix_rough_dirt = nodes.new('ShaderNodeMixRGB')
    mix_rough_dirt.location = (1100, 100)
    mix_rough_dirt.inputs['Color1'].default_value = (0.5, 0.5, 0.5, 1.0) # Base roughness
    mix_rough_dirt.inputs['Color2'].default_value = (0.9, 0.9, 0.9, 1.0) # Dirt roughness
    links.new(ramp_ao.outputs['Color'], mix_rough_dirt.inputs['Fac'])

    mix_rough_edge = nodes.new('ShaderNodeMixRGB')
    mix_rough_edge.location = (1400, 100)
    mix_rough_edge.inputs['Color2'].default_value = (0.2, 0.2, 0.2, 1.0) # Metal edge roughness
    links.new(map_edge.outputs['Result'], mix_rough_edge.inputs['Fac'])
    links.new(mix_rough_dirt.outputs['Color'], mix_rough_edge.inputs['Color1'])
    
    links.new(mix_rough_edge.outputs['Color'], bsdf.inputs['Roughness'])

    # Bump (Physical depth for dirt)
    bump = nodes.new('ShaderNodeBump')
    bump.location = (1400, -200)
    bump.inputs['Distance'].default_value = 0.05
    bump.inputs['Strength'].default_value = 0.4
    links.new(ramp_ao.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    return f"Created '{object_name}' at {location}. Switch viewport shading to Rendered (Cycles) to see dynamic edge wear and AO dirt."
```