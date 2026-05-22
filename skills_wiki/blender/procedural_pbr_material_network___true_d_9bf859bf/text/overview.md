# Agent_Skill_Distiller Report: PBR Material Routing & Displacement

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural PBR Material Network & True Displacement

* **Core Visual Mechanism**: The core principle is correctly routing Physically Based Rendering (PBR) data streams (Color, Roughness, Normal, and Height/Displacement) into the `Principled BSDF` and `Material Output` nodes. Specifically, it involves mathematical conversions of non-color data: using an `Invert` node to convert Gloss maps to Roughness maps, translating black-and-white height data into physical mesh manipulation via the `Displacement` node, and using the `Normal Map` node to fake micro-detail lighting.
* **Why Use This Skill (Rationale)**: Understanding proper PBR routing is the foundation of photorealism in modern 3D. While the tutorial focuses on downloaded image textures, the *mathematical routing* (e.g., Gloss = 1.0 - Roughness, Normal maps require Tangent space translation) is identical whether the source is a downloaded JPEG or a procedural noise generation. True displacement literally alters the geometry at render time, providing silhouette changes and realistic self-shadowing that normal maps cannot achieve.
* **Overall Applicability**: This is universally applicable for creating realistic materials (stone, metal, brick, wood) in any scene. The displacement logic is specifically excellent for terrain, brick walls, and highly textured macro-shots where silhouette details matter.
* **Value Addition**: Transforms a flat, mathematically perfect primitive into a physically believable object with micro-surface imperfections (Roughness/Normal) and macro-surface variations (Displacement).

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base**: Any mesh, but typically a subdivided plane or sphere to test displacement.
  - **Modifiers**: A `Subdivision Surface` modifier is required for True Displacement. In Cycles, activating "Experimental" feature sets allows for "Adaptive Subdivision" (dicing the mesh dynamically based on camera distance).
* **Step B: Materials & Shading**
  - **Shader**: `Principled BSDF`.
  - **Color**: Routed through a `Hue/Saturation/Value` node to allow global adjustments to the base texture.
  - **Roughness**: The video notes that some texture packs provide "Gloss" instead of "Roughness". Since Gloss is the mathematical inverse of Roughness, an `Invert` node is used before plugging the data into the Roughness socket. A `ColorRamp` is often added to clamp the values.
  - **Normals**: Black-and-white or procedural bump data is fed through a `Normal Map` node to convert it into vector data for the shader.
  - **Displacement**: Height data is fed into the `Height` socket of a `Displacement` node. The `Midlevel` is typically set to 0.0 or 0.5 to prevent the entire mesh from shifting globally, and `Scale` is lowered to ~0.1 to keep the effect realistic. The material settings must be changed from "Bump Only" to "Displacement" or "Displacement and Bump".
* **Step C: Lighting & Rendering Context**
  - **Engine**: Cycles is strictly required to see the *True Displacement* effect. EEVEE will only render the Bump mapping.
  - **Lighting**: Requires directional lighting (Sun or Spot) to reveal the shadows cast by the normal maps and displaced geometry.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Geometry Base | `bpy.ops.mesh.primitive_uv_sphere_add` | Provides a rounded surface to clearly observe displacement silhouettes. |
| Topology | Subdivision Surface Modifier | Provides the vertices necessary for physical displacement to push/pull. |
| PBR Texture Generation | Procedural Shader Nodes (Noise/Voronoi) | The tutorial utilizes downloaded image textures (Poliigon). To make this skill 100% reproducible without external file dependencies, we generate procedural textures that *act* as the image maps, applying the exact same routing, inversion, and displacement logic taught in the video. |
| Node Logic | `material.node_tree` API | Allows explicit mapping of the Gloss inversion, Normal mapping, and Displacement math discussed in the video. |

> **Feasibility Assessment**: 100% reproduction of the *PBR node logic and displacement mechanism*. Because we cannot dynamically download the user's specific image textures, procedural textures (Noise/Voronoi) are swapped in to generate the data streams. The mathematical node routing (Invert, Displacement, Normal Map, Hue/Sat) exactly mirrors the video.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Sphere",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a mesh demonstrating proper PBR node routing and True Displacement.
    Simulates image textures using procedural noise to demonstrate the video's node setup.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color modifier.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=scale, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    bpy.ops.object.shade_smooth()

    # Add Subdivision Surface for Displacement to have geometry to work with
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 3
    subsurf.render_levels = 4

    # Setup Cycles for True Displacement (as explicitly highlighted in the video)
    scene.render.engine = 'CYCLES'
    try:
        scene.cycles.feature_set = 'EXPERIMENTAL'
        subsurf.use_adaptive_subdivision = True
    except AttributeError:
        pass # Fallback gracefully if running on standard feature set or older versions

    # === Step 2: Build the PBR Material Network ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Material")
    mat.use_nodes = True
    
    # Video Tip: Enable true displacement in material settings
    if hasattr(mat, 'cycles'):
        mat.cycles.displacement_method = 'DISPLACEMENT'
        
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Output Nodes
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (1200, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (900, 0)
    links.new(bsdf.outputs[0], output.inputs['Surface'])

    # Coordinate Mapping (Video Tip: Ctrl+T Mapping Setup)
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-400, 0)
    links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])

    # --- BASE COLOR STREAM ---
    # Simulating a downloaded Color map
    noise_col = nodes.new('ShaderNodeTexNoise')
    noise_col.location = (-100, 300)
    noise_col.inputs['Scale'].default_value = 5.0
    links.new(mapping.outputs['Vector'], noise_col.inputs['Vector'])

    col_ramp = nodes.new('ShaderNodeValToRGB')
    col_ramp.location = (100, 300)
    col_ramp.color_ramp.elements[0].color = (0.05, 0.05, 0.05, 1.0)
    col_ramp.color_ramp.elements[1].color = (*material_color, 1.0)
    links.new(noise_col.outputs['Fac'], col_ramp.inputs['Fac'])

    # Video Tip: Tweaking downloaded color textures with Hue/Saturation
    hue_sat = nodes.new('ShaderNodeHueSaturation')
    hue_sat.location = (400, 300)
    hue_sat.inputs['Saturation'].default_value = 1.1
    links.new(col_ramp.outputs['Color'], hue_sat.inputs['Color'])
    links.new(hue_sat.outputs['Color'], bsdf.inputs['Base Color'])

    # --- ROUGHNESS STREAM (Handling "Gloss" maps) ---
    # Simulating a downloaded Gloss map
    voronoi_gloss = nodes.new('ShaderNodeTexVoronoi')
    voronoi_gloss.location = (-100, 0)
    voronoi_gloss.inputs['Scale'].default_value = 15.0
    links.new(mapping.outputs['Vector'], voronoi_gloss.inputs['Vector'])

    # Video Tip: If you have a Gloss map, use an INVERT node to make it a Roughness map
    invert_gloss = nodes.new('ShaderNodeInvert')
    invert_gloss.location = (100, 0)
    links.new(voronoi_gloss.outputs['Distance'], invert_gloss.inputs['Color'])

    # Video Tip: Use a ColorRamp to clamp/tweak the roughness values
    rough_ramp = nodes.new('ShaderNodeValToRGB')
    rough_ramp.location = (400, 0)
    rough_ramp.color_ramp.elements[0].position = 0.2
    rough_ramp.color_ramp.elements[1].position = 0.8
    links.new(invert_gloss.outputs['Color'], rough_ramp.inputs['Fac'])
    links.new(rough_ramp.outputs['Color'], bsdf.inputs['Roughness'])

    # --- NORMAL STREAM ---
    # Simulating a Normal/Bump detail map
    noise_norm = nodes.new('ShaderNodeTexNoise')
    noise_norm.location = (100, -300)
    noise_norm.inputs['Scale'].default_value = 25.0
    links.new(mapping.outputs['Vector'], noise_norm.inputs['Vector'])

    # Video Tip: Normal Map Node
    norm_map = nodes.new('ShaderNodeNormalMap')
    norm_map.location = (400, -300)
    norm_map.inputs['Strength'].default_value = 0.6
    links.new(noise_norm.outputs['Color'], norm_map.inputs['Color'])
    links.new(norm_map.outputs['Normal'], bsdf.inputs['Normal'])

    # --- DISPLACEMENT STREAM ---
    # Simulating a Height/Displacement map
    disp_noise = nodes.new('ShaderNodeTexNoise')
    disp_noise.location = (400, -600)
    disp_noise.inputs['Scale'].default_value = 2.0
    disp_noise.inputs['Detail'].default_value = 4.0
    links.new(mapping.outputs['Vector'], disp_noise.inputs['Vector'])

    # Video Tip: Displacement Node setup (Midlevel and Scale adjustment)
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (900, -600)
    disp_node.inputs['Midlevel'].default_value = 0.5  # Prevents object from expanding/shifting globally
    disp_node.inputs['Scale'].default_value = 0.15    # Kept low for realism
    links.new(disp_noise.outputs['Fac'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], output.inputs['Displacement'])

    # === Step 3: Assign Material ===
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    # === Step 4: Add Lighting to view the effect ===
    # Displacement and Normals require light to cast shadows
    light_data = bpy.data.lights.new(name=f"{object_name}_Sun", type='SUN')
    light_data.energy = 3.0
    light_data.angle = 0.1 # Sharp shadows to reveal displacement
    light_obj = bpy.data.objects.new(name=f"{object_name}_Sun", object_data=light_data)
    scene.collection.objects.link(light_obj)
    light_obj.location = Vector(location) + Vector((5, -5, 5))
    # Point light at the object
    direction = Vector(location) - light_obj.location
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    return f"Created PBR Object '{object_name}' at {location} configured for True Displacement."
```