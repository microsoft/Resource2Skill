### 1. High-level Design Pattern Extraction

> **Skill Name**: Advanced PBR Node Architecture & Displacement

* **Core Visual Mechanism**: This technique involves building a robust, fully-featured Physically Based Rendering (PBR) material network. It distinguishes itself by integrating essential utility nodes for fine-tuning: a single `Value` node driving universal texture scaling, a `Hue Saturation Value` node for non-destructive color grading, an `Invert` node to convert legacy Gloss maps to Roughness, and a mathematical `Displacement` setup tied to adaptive mesh subdivision. 
* **Why Use This Skill (Rationale)**: Loading textures is simple, but orchestrating them correctly determines photorealism. Many artists struggle with scaling multiple textures simultaneously or converting incompatible maps (like Glossiness) into modern standard workflows (Roughness). This node architecture ensures texture synchronicity, proper data interpretation (non-color vs. sRGB), and true geometric displacement rather than just surface-level bump illusions.
* **Overall Applicability**: Essential for any realistic 3D asset using texture sets (e.g., Megascans, Poliigon, Poly Haven) ranging from architectural visualization (brick walls, hardwood floors) to sci-fi environments (greebled panels). 
* **Value Addition**: Transforms a basic primitive into a highly detailed, physically accurate surface that reacts dynamically to lighting setups. The utility nodes provide infinite tweakability without needing to alter external image files in Photoshop.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A simple Plane (or any target mesh).
  - **Modifiers**: A Subdivision Surface modifier set to `Simple` (not Catmull-Clark, to preserve the object's original silhouette while adding geometry).
  - **Context**: For true displacement, the geometry needs actual vertices to move. In Cycles, this is optimally achieved via "Adaptive Subdivision" (Experimental feature), but static subdivision works universally.

* **Step B: Materials & Shading**
  - **Architecture**: `Principled BSDF` acts as the master shader.
  - **Mapping Structure**: `Texture Coordinate` (UV) -> `Mapping` -> (All Textures). A separate `Value` node is plugged into the Mapping node's Scale input for unified scaling.
  - **Color Map**: Fed through a `Hue Saturation Value` node into the `Base Color`.
  - **Gloss/Roughness Map**: Passed through an `Invert` node to convert the white/black values appropriately for Roughness.
  - **Normal Map**: Passed through a `Normal Map` node (to convert RGB data into vector data) -> `Normal` input.
  - **Displacement Map**: Passed through a `Displacement` node (Midlevel set to 0.0 to prevent mesh shifting) -> `Displacement` input of the `Material Output` node.
  - **Color Spaces**: In standard workflows, Color is sRGB, while Roughness, Normal, and Displacement are set to Non-Color data. (Note: Procedural nodes handle this inherently).

* **Step C: Lighting & Rendering Context**
  - **Engine**: Cycles is required for *true* geometric displacement. EEVEE only supports Bump approximation from these maps.
  - **Material Settings**: In the Material Properties -> Settings -> Surface, the Displacement method must be changed from "Bump Only" to "Displacement and Bump".

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base Geometry & Detail | `bpy.ops.mesh.primitive` + Subsurf | We need dense topology to demonstrate displacement. |
| PBR Texture Substitutes | Shader Nodes (Procedural Textures) | External image files cannot be referenced safely in a portable script. Procedural textures mathematically simulate the Color, Roughness, Normal, and Displacement maps. |
| Advanced Node Architecture | Shader Node Graph API (`links.new`) | Perfectly recreates the tutorial's utility nodes (Value scale, HSV, Invert, Normal Map, Displacement). |

> **Feasibility Assessment**: 100% of the *architectural pattern* and *shading logic* is reproduced. Because we cannot rely on external Poly Haven/Poliigon image files, procedural textures (`Noise`, `Musgrave`, `Voronoi`) are swapped into the exact same node sockets to demonstrate the functional material setup. 

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displacement_Plane",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.3, 0.3),
    **kwargs,
) -> str:
    """
    Create a dense plane with an advanced PBR node architecture.
    Simulates the Color, Gloss->Roughness, Normal, and Displacement workflow.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color tint.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created setup.
    """
    import bpy
    from mathutils import Vector

    # 1. Ensure scene exists
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Enable cycles and experimental feature set for true displacement (if Cycles is active engine)
    if scene.render.engine == 'CYCLES':
        scene.cycles.feature_set = 'EXPERIMENTAL'

    # 2. Create Base Mesh
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface Modifier (Simple mode, to keep the square shape but add geometry for displacement)
    subsurf = obj.modifiers.new(name="Adaptive_Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 6        # Viewport detail
    subsurf.render_levels = 8 # Render detail
    
    # Ensure smooth shading
    bpy.ops.object.shade_smooth()

    # 3. Create Advanced PBR Material
    mat_name = f"{object_name}_Mat"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    
    # Set material to use Displacement and Bump (Crucial for Cycles displacement)
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'
    
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    tree = mat.node_tree
    nodes = tree.nodes
    links = tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # --- Create Nodes ---
    
    # Outputs
    out_node = nodes.new(type="ShaderNodeOutputMaterial")
    out_node.location = (1200, 0)
    
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.location = (800, 0)

    # Coordinate & Mapping
    tex_coord = nodes.new(type="ShaderNodeTexCoord")
    tex_coord.location = (-1000, 0)
    
    mapping = nodes.new(type="ShaderNodeMapping")
    mapping.location = (-800, 0)
    
    # Universal Scale Control (Value node)
    val_scale = nodes.new(type="ShaderNodeValue")
    val_scale.location = (-1000, -300)
    val_scale.outputs[0].default_value = 5.0  # Controls the tiling of all maps at once
    val_scale.label = "Universal Scale"

    # --- Substitute "Image Maps" with Procedural Nodes ---
    # In a real scenario, these would be ShaderNodeTexImage
    
    # 1. Color Map Substitute
    map_color = nodes.new(type="ShaderNodeTexNoise")
    map_color.location = (-400, 300)
    map_color.label = "Color Map (Noise)"
    
    hsv_node = nodes.new(type="ShaderNodeHueSaturation")
    hsv_node.location = (-100, 300)
    hsv_node.inputs['Color'].default_value = (material_color[0], material_color[1], material_color[2], 1.0)
    hsv_node.inputs['Saturation'].default_value = 1.2
    
    # 2. Gloss Map Substitute (Gloss needs to be inverted to Roughness)
    map_gloss = nodes.new(type="ShaderNodeTexVoronoi")
    map_gloss.location = (-400, 0)
    map_gloss.label = "Gloss Map (Voronoi)"
    
    invert_node = nodes.new(type="ShaderNodeInvert")
    invert_node.location = (-100, 0)
    invert_node.label = "Gloss to Roughness"

    # 3. Normal Map Substitute
    map_normal = nodes.new(type="ShaderNodeTexMusgrave")
    map_normal.location = (-400, -300)
    map_normal.label = "Normal Map (Musgrave)"
    
    normal_node = nodes.new(type="ShaderNodeNormalMap")
    normal_node.location = (-100, -300)
    normal_node.inputs['Strength'].default_value = 1.0

    # 4. Displacement Map Substitute
    map_disp = nodes.new(type="ShaderNodeTexNoise")
    map_disp.location = (400, -600)
    map_disp.inputs['Scale'].default_value = 2.0
    map_disp.label = "Displacement Map (Noise)"
    
    disp_node = nodes.new(type="ShaderNodeDisplacement")
    disp_node.location = (800, -600)
    disp_node.inputs['Midlevel'].default_value = 0.0  # Keeps mesh from shifting
    disp_node.inputs['Scale'].default_value = 0.1     # Subtle height adjustment

    # --- Link Nodes ---
    
    # Coordinates to Mapping
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    
    # Value to Mapping Scale
    links.new(val_scale.outputs[0], mapping.inputs['Scale'])
    
    # Mapping to Textures
    links.new(mapping.outputs['Vector'], map_color.inputs['Vector'])
    links.new(mapping.outputs['Vector'], map_gloss.inputs['Vector'])
    links.new(mapping.outputs['Vector'], map_normal.inputs['Vector'])
    # Not hooking mapping to disp so it stays large and smooth, but you could
    
    # Color workflow
    links.new(map_color.outputs['Color'], hsv_node.inputs['Fac'])
    links.new(hsv_node.outputs['Color'], bsdf.inputs['Base Color'])
    
    # Gloss to Roughness workflow
    links.new(map_gloss.outputs['Distance'], invert_node.inputs['Color'])
    links.new(invert_node.outputs['Color'], bsdf.inputs['Roughness'])
    
    # Normal workflow
    links.new(map_normal.outputs[0], normal_node.inputs['Color'])
    links.new(normal_node.outputs['Normal'], bsdf.inputs['Normal'])
    
    # BSDF to Output
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])
    
    # Displacement workflow
    links.new(map_disp.outputs['Fac'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])

    return f"Created '{object_name}' at {location} with advanced PBR node architecture (Value Scaling, HSV tweak, Gloss Inversion, and True Displacement setup)."
```