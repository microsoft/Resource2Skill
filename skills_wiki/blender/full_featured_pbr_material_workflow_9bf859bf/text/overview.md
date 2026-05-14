# Agent_Skill_Distiller: 3D Modeling & Scene Design Pattern Extraction

### 1. High-level Design Pattern Extraction

> **Skill Name**: Full-Featured PBR Material Workflow

* **Core Visual Mechanism**: Physically Based Rendering (PBR) relies on separating material properties into distinct data channels (maps). Instead of just applying a color image, this technique uses non-color data maps to dictate how light scatters (Roughness), how micro-details catch light (Normal/Bump), and how the silhouette of the geometry actually extrudes and deforms (True Displacement). 

* **Why Use This Skill (Rationale)**: A flat color texture looks inherently fake in 3D because real-world surfaces interact dynamically with light. By mapping Roughness, light correctly diffuses over dull areas and sharpens over glossy areas. By applying True Displacement with Adaptive Subdivision, the geometry physically deforms to match the texture, creating realistic self-shadowing and silhouette breaking that a simple bump map cannot achieve.

* **Overall Applicability**: This is the fundamental, mandatory workflow for achieving photorealism in architectural visualization, prop design, and environment art. Whether building a cracked concrete floor, a muddy terrain, or rusted metal panels, this PBR node topology is the universal standard.

* **Value Addition**: Transforms a mathematically perfectly flat, featureless 3D plane into a highly detailed, physically tactile surface without requiring the artist to manually sculpt millions of polygons.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A standard plane.
  - **Modifiers**: A Subdivision Surface modifier set to 'Simple' mode. 
  - **Adaptive Subdivision**: Requires the Cycles rendering engine and the 'Experimental' feature set. This dynamically increases polygon density only where the camera can see it, allowing for extremely dense micro-geometry for displacement without crashing the viewport.

* **Step B: Materials & Shading**
  - **Shader Model**: Principled BSDF.
  - **Base Color**: Image/Procedural texture passed through a Hue/Saturation node to allow non-destructive tweaking of the color values within the shader.
  - **Roughness**: The tutorial demonstrates a common scenario where a texture pack provides a "Gloss" map instead of a "Roughness" map. Because Gloss is the mathematical inverse of Roughness, an `Invert` node is placed between the texture and the Roughness input.
  - **Normal**: Texture data passed through a `Normal Map` node to convert scalar height/angle data into vector data the BSDF can read.
  - **Displacement**: Texture data passed through a `Displacement` node. The `Midlevel` is often set to `0.0` to prevent the entire object from shifting incorrectly in 3D space.
  - **Data Type Rule**: *All* maps except the Base Color must be treated as "Non-Color Data" (scalar/math data), otherwise Blender will apply sRGB gamma curves and ruin the physics math.

* **Step C: Lighting & Rendering Context**
  - **Render Engine**: Cycles is strictly required for True Displacement. EEVEE will only render the Normal map and treat Displacement as a standard bump map.
  - **Material Settings**: In the Material Properties -> Settings -> Surface, the Displacement method must be changed from "Bump Only" (default) to "Displacement and Bump".
  - **Lighting**: PBR requires directional lighting to reveal surface variations. A point light or strong HDRI is highly recommended.

* **Step D: Animation & Dynamics (if applicable)**
  - N/A. This is a static material setup.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| PBR Node Topology | Shader Node Tree via Python | Replicates the exact node wiring (Invert, Normal Map, Displacement) taught in the tutorial. |
| Texture Data | Procedural Nodes (`ShaderNodeTexNoise`, etc.) | *Feasibility Note*: The tutorial uses downloaded external image files. To make this code 100% self-contained and immediately reproducible without external file dependencies, procedural noise nodes are substituted in place of the Image Texture nodes. The PBR logic remains identical. |
| True Displacement | Subdivision Modifier + Cycles Settings | Only way to physically displace geometry at render time based on shader data. |

> **Feasibility Assessment**: 100% of the *technical workflow and node logic* is reproduced. Visually, it produces a procedural rocky/concrete surface that perfectly demonstrates the physics taught in the video (color tinting, inverted roughness, bump, and true displacement).

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Surface",
    location: tuple = (0, 0, 0),
    scale: float = 2.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a PBR material workflow demonstration on an actively displaced plane.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color tint.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Render Engine & Experimental Features ===
    # True displacement requires Cycles and Experimental features
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'

    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Add Subdivision Modifier for Adaptive Subdivision
    subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.subdivision_type = 'SIMPLE'
    # Enable adaptive subdivision in the object's cycles settings
    obj.cycles.use_adaptive_subdivision = True

    # === Step 3: Build PBR Material (Node Topology) ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    # Crucial step: Tell the material to actually displace the geometry
    mat.cycles.displacement_method = 'BOTH' # Displacement and Bump

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output & BSDF
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1200, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (800, 0)
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    # Coordinates & Mapping
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-800, 0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])

    # --- Channel 1: Base Color ---
    color_tex = nodes.new('ShaderNodeTexNoise')
    color_tex.location = (-500, 300)
    color_tex.inputs['Scale'].default_value = 5.0
    links.new(mapping.outputs['Vector'], color_tex.inputs['Vector'])

    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-300, 300)
    color_ramp.color_ramp.elements[0].color = (0.05, 0.05, 0.05, 1.0)
    color_ramp.color_ramp.elements[1].color = (*material_color, 1.0)
    links.new(color_tex.outputs['Fac'], color_ramp.inputs['Fac'])

    hue_sat = nodes.new('ShaderNodeHueSaturation')
    hue_sat.location = (0, 300)
    hue_sat.inputs['Saturation'].default_value = 1.1
    links.new(color_ramp.outputs['Color'], hue_sat.inputs['Color'])
    links.new(hue_sat.outputs['Color'], bsdf.inputs.get('Base Color'))

    # --- Channel 2: Specular / Reflection ---
    spec_tex = nodes.new('ShaderNodeTexNoise')
    spec_tex.location = (-500, 100)
    spec_tex.inputs['Scale'].default_value = 25.0
    links.new(mapping.outputs['Vector'], spec_tex.inputs['Vector'])
    
    # Handle API changes between Blender 3.x and 4.0+ for Specular
    specular_socket = bsdf.inputs.get('Specular IOR Level') or bsdf.inputs.get('Specular')
    if specular_socket:
        links.new(spec_tex.outputs['Fac'], specular_socket)

    # --- Channel 3: Roughness (Inverted from Gloss) ---
    gloss_tex = nodes.new('ShaderNodeTexNoise')
    gloss_tex.location = (-500, -100)
    gloss_tex.inputs['Scale'].default_value = 15.0
    links.new(mapping.outputs['Vector'], gloss_tex.inputs['Vector'])

    invert_node = nodes.new('ShaderNodeInvert')
    invert_node.location = (-100, -100)
    links.new(gloss_tex.outputs['Fac'], invert_node.inputs['Color'])
    links.new(invert_node.outputs['Color'], bsdf.inputs.get('Roughness'))

    # --- Channel 4: Normal / Bump ---
    norm_tex = nodes.new('ShaderNodeTexVoronoi')
    norm_tex.location = (-500, -300)
    norm_tex.inputs['Scale'].default_value = 20.0
    links.new(mapping.outputs['Vector'], norm_tex.inputs['Vector'])

    normal_map = nodes.new('ShaderNodeNormalMap')
    normal_map.location = (-100, -300)
    normal_map.inputs['Strength'].default_value = 1.5
    links.new(norm_tex.outputs['Distance'], normal_map.inputs['Color'])
    links.new(normal_map.outputs['Normal'], bsdf.inputs.get('Normal'))

    # --- Channel 5: True Displacement ---
    disp_tex = nodes.new('ShaderNodeTexNoise')
    disp_tex.location = (-500, -600)
    disp_tex.inputs['Scale'].default_value = 3.0
    links.new(mapping.outputs['Vector'], disp_tex.inputs['Vector'])

    displacement = nodes.new('ShaderNodeDisplacement')
    displacement.location = (800, -300)
    displacement.inputs['Midlevel'].default_value = 0.0  # Prevents object from floating/shifting
    displacement.inputs['Scale'].default_value = 0.15
    links.new(disp_tex.outputs['Fac'], displacement.inputs['Height'])
    links.new(displacement.outputs['Displacement'], out_node.inputs['Displacement'])

    # === Step 4: Add Lighting to Reveal Material Properties ===
    light_data = bpy.data.lights.new(name=f"{object_name}_Light", type='POINT')
    light_data.energy = 500.0
    light_obj = bpy.data.objects.new(name=f"{object_name}_LightObj", object_data=light_data)
    bpy.context.collection.objects.link(light_obj)
    
    # Place light just above the surface to cast harsh, revealing shadows on the displacement
    light_obj.location = (location[0] + 1.0, location[1] - 1.0, location[2] + 1.0)

    return f"Created '{object_name}' PBR surface at {location} with adaptive displacement enabled. (Requires Cycles rendering to view displacement)."
```