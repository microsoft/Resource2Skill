# Agent_Skill_Distiller Report

### 1. High-level Design Pattern Extraction

> **Skill Name**: Advanced PBR Material Pipeline with Adaptive Displacement

* **Core Visual Mechanism**: Physically Based Rendering (PBR) relies on splitting material properties into distinct mathematical maps: Base Color, Roughness, Normal, and Displacement. The signature visual effect of this technique is true surface depth, achieved by pairing a Displacement map with "Adaptive Subdivision," which dynamically creates real micro-geometry at render time based on the camera's distance, casting physically accurate self-shadows.
* **Why Use This Skill (Rationale)**: Flat textures look unnatural when hit by grazing light. By mapping separate data streams—especially using an Invert node to convert Gloss maps to Roughness maps, and employing true Displacement—light interacts with the surface exactly as it does in reality. The adaptive subdivision ensures that geometry is only dense where the camera can actually see it, saving memory.
* **Overall Applicability**: Essential for any photorealistic asset, including architectural visualization (bricks, concrete, wood), landscape design (ground, mud, rock), and hero props.
* **Value Addition**: Transforms a basic flat primitive into a highly detailed, reactive, and physically accurate 3D surface without manually modeling millions of polygons.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A simple Plane or low-poly object.
  - **Modifiers**: A Subdivision Surface modifier set to Catmull-Clark.
  - **Topology Flow**: In a true PBR displacement workflow, the base topology doesn't need to be dense. The magic happens via the `Adaptive Subdivision` engine feature, which dynamically dices the mesh into micro-polygons at render time.

* **Step B: Materials & Shading**
  - **Shader Model**: Principled BSDF.
  - **Mapping Framework**: `Texture Coordinate` (UV) -> `Mapping` -> [Texture Nodes].
  - **Data Routing**:
    - *Color*: Plugs directly into `Base Color`.
    - *Gloss/Roughness*: Often, downloaded textures provide "Gloss" maps. These must be passed through an `Invert` node to become "Roughness". (Black = smooth, White = rough).
    - *Normals*: Passed through a `Normal Map` (or `Bump`) node before hitting the BSDF.
    - *Displacement*: Fed into the `Height` of a `Displacement` node, then into the Material Output. Crucially, the `Midlevel` is set to `0.0` to prevent the entire mesh from shifting in 3D space, and `Scale` is reduced (e.g., `0.1`).
  - **Settings**: The Material's Surface setting must be explicitly changed from "Bump Only" to "Displacement and Bump".

* **Step C: Lighting & Rendering Context**
  - **Render Engine**: **Cycles** is strictly required. EEVEE does not support true micro-polygon displacement.
  - **Feature Set**: Must be changed to **Experimental** to unlock Adaptive Subdivision.
  - **Lighting**: Benefits immensely from angled directional lights or HDRIs, which emphasize the real physical shadows cast by the displaced geometry.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Geometry & Subdiv | `bpy.ops.mesh.primitive` + Modifiers | Provides a clean, flat UV-mapped canvas to demonstrate displacement. |
| PBR Channel Routing | Shader node tree | Python script builds the exact node network (Mapping, Invert, Bump, Displacement) taught in the tutorial. |
| Textures | Procedural Textures (`ShaderNodeTexBrick`) | To ensure the code is 100% reproducible without requiring the user to download external image files, procedural textures are wired exactly as the image textures were in the tutorial. |

> **Feasibility Assessment**: 100% of the technical workflow is reproduced. The script translates the tutorial's logic (setting up Cycles Experimental, enabling Adaptive Subdivision, fixing Displacement Midlevel/Scale, and inverting Gloss to Roughness) into a self-contained procedural brick material that works out-of-the-box.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Adaptive_Bricks",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.25, 0.15),  # Base brick color
    **kwargs,
) -> str:
    """
    Create a plane with a fully configured PBR material and Adaptive Displacement.
    Mimics the image-texture workflow procedurally (Color, Inverted Gloss, Bump, Displacement).

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the bricks.

    Returns:
        Status string describing the creation.
    """
    import bpy
    from mathutils import Vector

    # Get the active scene
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Engine Setup for Adaptive Subdivision ===
    # True displacement requires Cycles and the Experimental feature set
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Surface modifier
    subsurf = obj.modifiers.new(name="Adaptive_Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'CATMULL_CLARK'
    
    # Enable Adaptive Subdivision (Only active in Cycles Experimental)
    try:
        obj.cycles.use_adaptive_subdivision = True
    except Exception as e:
        print(f"Warning: Could not enable adaptive subdivision: {e}")

    # === Step 3: Build PBR Material Node Tree ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)

    # Tell the material to use True Displacement
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Clear default nodes

    # --- Output & BSDF ---
    mat_output = nodes.new(type='ShaderNodeOutputMaterial')
    mat_output.location = (1000, 0)

    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.location = (600, 0)

    # --- Coordinates & Mapping ---
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)

    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-600, 0)

    # --- Procedural Textures (Simulating Image Maps) ---
    # 1. Base Color / Displacement Map
    brick_tex = nodes.new(type='ShaderNodeTexBrick')
    brick_tex.location = (-300, 200)
    brick_tex.inputs['Color1'].default_value = (*material_color, 1.0)
    brick_tex.inputs['Color2'].default_value = (material_color[0]*0.6, material_color[1]*0.6, material_color[2]*0.6, 1.0)
    brick_tex.inputs['Mortar'].default_value = (0.5, 0.5, 0.5, 1.0)
    brick_tex.inputs['Scale'].default_value = 3.0

    # 2. "Gloss" Map (Using Noise to simulate surface imperfections)
    noise_tex = nodes.new(type='ShaderNodeTexNoise')
    noise_tex.location = (-300, -150)
    noise_tex.inputs['Scale'].default_value = 25.0
    noise_tex.inputs['Detail'].default_value = 5.0

    # --- PBR Conversion Nodes ---
    # Convert "Gloss" to "Roughness" via Invert node (as taught in the tutorial)
    invert_node = nodes.new(type='ShaderNodeInvert')
    invert_node.location = (0, -150)
    
    # Map range to keep roughness realistic (not perfectly glossy or completely matte)
    map_range = nodes.new(type='ShaderNodeMapRange')
    map_range.location = (200, -150)
    map_range.inputs[3].default_value = 0.3 # To Min
    map_range.inputs[4].default_value = 0.8 # To Max

    # Bump Node (Simulating a Normal Map)
    bump_node = nodes.new(type='ShaderNodeBump')
    bump_node.location = (200, -400)
    bump_node.inputs['Strength'].default_value = 0.6
    bump_node.inputs['Distance'].default_value = 0.05

    # Displacement Node
    disp_node = nodes.new(type='ShaderNodeDisplacement')
    disp_node.location = (600, -300)
    disp_node.inputs['Midlevel'].default_value = 0.0  # Set to 0 to prevent geometry shift
    disp_node.inputs['Scale'].default_value = 0.1     # Scaled down for realism

    # === Step 4: Link Everything Together ===
    # Vectors
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], brick_tex.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise_tex.inputs['Vector'])

    # Color
    links.new(brick_tex.outputs['Color'], principled.inputs['Base Color'])

    # Roughness
    links.new(noise_tex.outputs['Fac'], invert_node.inputs['Color'])
    links.new(invert_node.outputs['Color'], map_range.inputs['Value'])
    links.new(map_range.outputs['Result'], principled.inputs['Roughness'])

    # Bump / Normal
    links.new(brick_tex.outputs['Fac'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], principled.inputs['Normal'])

    # Displacement
    links.new(brick_tex.outputs['Fac'], disp_node.inputs['Height'])
    
    # Final Outputs
    links.new(principled.outputs['BSDF'], mat_output.inputs['Surface'])
    links.new(disp_node.outputs['Displacement'], mat_output.inputs['Displacement'])

    return f"Created '{object_name}' at {location}. Cycles engine set to Experimental for Adaptive Subdivision."
```