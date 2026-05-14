# Procedural Sequential Text Reveal (UV Island Masking)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Sequential Text Reveal (UV Island Masking)

* **Core Visual Mechanism**: The defining mechanism here is transforming 3D text into a mesh, isolating each letter as a geometric "island", and mathematically collapsing all UV coordinates of a single letter into one specific point on the U-axis based on its horizontal position. In the shader, a sweeping mathematical threshold (`Less Than` node evaluating the U coordinate) acts as an animated mask, snapping the material state from glassy to emissive sequentially, letter-by-letter.
* **Why Use This Skill (Rationale)**: Traditionally, animating text revealing letter-by-letter requires separating each letter into its own object and manually offsetting keyframes. This technique encapsulates the entire effect within a single mesh and a single material. It is computationally cheaper, easier to edit, and perfectly uniform. 
* **Overall Applicability**: This pattern is highly valuable for 3D motion graphics, cyberpunk/sci-fi title sequences, holographic UI elements, and neon sign reveals. 
* **Value Addition**: By leveraging BMesh programmatic UV manipulation combined with a threshold shader, it turns a static mesh into a smart, self-animating asset without relying on complex rig setups or Geometry Nodes.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: Standard Blender Text object (Font Curve), given slight extrusion and beveling for light-catching edges.
  - **Conversion**: Converted to a polygon mesh (`MESH` target).
  - **BMesh UV Manipulation**: A programmatic flood-fill algorithm identifies disconnected face groups (letters/dots). The average X-coordinate of each group is calculated. All vertices in that group are mapped to the exact same U-coordinate (normalized 0 to 1). This ensures a letter lights up instantaneously as a whole, rather than the gradient sliding across it smoothly.
* **Step B: Materials & Shading**
  - **Shader Model**: A `Mix Shader` transitioning between a dark Glass material (Principled BSDF with high transmission, low roughness) and a high-intensity Emission material.
  - **Procedural Mask**: `UV Map` -> `Separate XYZ` (extracts U) -> `Math (Less Than)`. 
  - **Material Properties**: 
    - Base Glass: `(0.01, 0.01, 0.01)`, Roughness `0.1`, Transmission `1.0`.
    - Emission: Variable color (e.g., Fiery Orange), Strength `50.0`.
* **Step C: Lighting & Rendering Context**
  - **Lighting**: Best accompanied by a dark environment or contrasting area lights (e.g., deep blue) to highlight the glowing emission.
  - **Render Engine**: Cycles is strongly recommended for accurate glass transmission and emission bounces, though it works perfectly in EEVEE.
* **Step D: Animation & Dynamics**
  - The animation is driven entirely by two keyframes in the shader node tree. The threshold value of the `Less Than` node is keyframed from `-0.1` to `1.1` over a set duration, causing the boolean mask to sweep from left to right.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base Typography | `bpy.data.curves.new(type='FONT')` | Native text generation with built-in beveling and kerning. |
| Per-Letter UV Grouping | BMesh (Island detection) | The most robust way to find disconnected letters programmatically, perfectly replicating the tutorial's "scale individual origins to 0" trick without relying on UI operators. |
| Sequential Reveal Mask | Shader node tree (Math nodes) | Avoids manual keyframing of multiple objects; mathematically precise and infinitely scalable regardless of string length. |

> **Feasibility Assessment**: 100% reproduction of the core sequential glowing text effect. The code dynamically handles any text string, calculates the bounding box to normalize UVs, and sets up the exact node-based animation logic described in the video.

#### 3b. Complete Reproduction Code

```python
def create_sequential_glowing_text(
    scene_name: str = "Scene",
    object_name: str = "SequentialGlowText",
    text_string: str = "BLEND",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    glow_color: tuple = (1.0, 0.2, 0.0), # Fiery Orange
    animation_duration: int = 60
) -> str:
    """
    Creates a 3D text object that sequentially reveals from left to right,
    transitioning from dark glass to bright emission using UV masking.

    Args:
        scene_name: Target scene name.
        object_name: Name of the generated mesh object.
        text_string: The word/phrase to animate.
        location: World-space position.
        scale: Uniform scale.
        glow_color: RGB tuple for the emission color.
        animation_duration: Number of frames for the reveal to complete.
        
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    if not text_string:
        text_string = "TEXT"

    # === Step 1: Create Extruded & Beveled Text ===
    curve_data = bpy.data.curves.new(name=f"{object_name}_Curve", type='FONT')
    curve_data.body = text_string
    curve_data.extrude = 0.1
    curve_data.bevel_depth = 0.015
    curve_data.bevel_resolution = 3
    curve_data.align_x = 'CENTER'
    curve_data.align_y = 'BOTTOM_BASELINE'

    text_obj = bpy.data.objects.new(object_name, curve_data)
    scene.collection.objects.link(text_obj)
    
    # Position and scale before conversion
    text_obj.location = Vector(location)
    text_obj.scale = (scale, scale, scale)

    # === Step 2: Convert to Mesh ===
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = text_obj
    text_obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    mesh = text_obj.data

    # === Step 3: BMesh UV Island Grouping ===
    # This identifies each letter (island) and collapses its UVs to a single point
    # based on its X-position, allowing the shader to light them up sequentially.
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.faces.ensure_lookup_table()
    
    uv_layer = bm.loops.layers.uv.verify()
    
    visited = set()
    islands = []
    
    # Flood-fill to find disconnected face islands (letters)
    for f in bm.faces:
        if f not in visited:
            island = []
            stack = [f]
            while stack:
                curr = stack.pop()
                if curr not in visited:
                    visited.add(curr)
                    island.append(curr)
                    for e in curr.edges:
                        for linked_f in e.link_faces:
                            if linked_f not in visited:
                                stack.append(linked_f)
            islands.append(island)

    if bm.verts:
        min_x = min(v.co.x for v in bm.verts)
        max_x = max(v.co.x for v in bm.verts)
        width = max_x - min_x
        if width == 0: 
            width = 1.0

        for island in islands:
            # Calculate average local X position of the letter
            verts = set(v for f in island for v in f.verts)
            avg_x = sum(v.co.x for v in verts) / len(verts)
            
            # Normalize to 0-1 U coordinate
            u = (avg_x - min_x) / width
            
            # Collapse all UVs for this letter to the same point
            for f in island:
                for loop in f.loops:
                    loop[uv_layer].uv = (u, 0.5)

    bm.to_mesh(mesh)
    bm.free()

    # === Step 4: Create the Sequential Shader ===
    mat = bpy.data.materials.new(name=f"{object_name}_GlowMat")
    mat.use_nodes = True
    tree = mat.node_tree
    nodes = tree.nodes
    links = tree.links
    nodes.clear()

    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (800, 0)

    mix_node = nodes.new('ShaderNodeMixShader')
    mix_node.location = (600, 0)

    # State 0: Dark Glass
    glass_node = nodes.new('ShaderNodeBsdfPrincipled')
    glass_node.location = (300, 150)
    glass_node.inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1)
    glass_node.inputs['Roughness'].default_value = 0.1
    # Handle Blender 4.x transmission naming vs older versions
    if 'Transmission Weight' in glass_node.inputs:
        glass_node.inputs['Transmission Weight'].default_value = 1.0
    elif 'Transmission' in glass_node.inputs:
        glass_node.inputs['Transmission'].default_value = 1.0

    # State 1: Bright Emission
    emit_node = nodes.new('ShaderNodeEmission')
    emit_node.location = (300, -100)
    emit_node.inputs['Color'].default_value = (*glow_color, 1.0)
    emit_node.inputs['Strength'].default_value = 50.0

    # Masking Logic
    uv_node = nodes.new('ShaderNodeUVMap')
    uv_node.location = (-300, 300)

    sep_node = nodes.new('ShaderNodeSeparateXYZ')
    sep_node.location = (-100, 300)

    # Less Than node acts as a sharp threshold sweeper
    math_node = nodes.new('ShaderNodeMath')
    math_node.operation = 'LESS_THAN'
    math_node.location = (100, 300)
    
    # Wire it up
    links.new(uv_node.outputs['UV'], sep_node.inputs['Vector'])
    links.new(sep_node.outputs['X'], math_node.inputs[0])
    links.new(math_node.outputs['Value'], mix_node.inputs['Fac'])
    links.new(glass_node.outputs['BSDF'], mix_node.inputs[1])
    links.new(emit_node.outputs['Emission'], mix_node.inputs[2])
    links.new(mix_node.outputs['Shader'], out_node.inputs['Surface'])

    # === Step 5: Animate the Reveal ===
    # Frame 1: Threshold < 0 (All U coords are larger, so all resolve to False/Glass)
    math_node.inputs[1].default_value = -0.1
    math_node.inputs[1].keyframe_insert(data_path="default_value", frame=1)
    
    # End Frame: Threshold > 1 (All U coords are smaller, so all resolve to True/Emission)
    math_node.inputs[1].default_value = 1.1
    math_node.inputs[1].keyframe_insert(data_path="default_value", frame=animation_duration)

    # Assign material
    text_obj.data.materials.append(mat)
    
    # Smooth shading
    for poly in text_obj.data.polygons:
        poly.use_smooth = True

    return f"Created animatable text mesh '{object_name}' displaying '{text_string}' at {location}. Press play to see the reveal."
```