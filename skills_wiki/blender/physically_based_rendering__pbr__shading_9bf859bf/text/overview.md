### 1. High-level Design Pattern Extraction

> **Skill Name**: Physically Based Rendering (PBR) Shading & True Displacement Setup

* **Core Visual Mechanism**: The core pattern is a multi-channel material workflow that separates different physical properties of a surface into dedicated texture maps. It routes Base Color, Reflection (Specular), Gloss (inverted to Roughness), and micro-details (Normal maps) into a `Principled BSDF`, while routing macro-details (Displacement maps) into a true mesh displacement setup using Cycles' Experimental Adaptive Subdivision.
* **Why Use This Skill (Rationale)**: PBR workflows are the industry standard for achieving photorealism. By defining a material through physical properties (how rough it is, how it reflects light, its microscopic and macroscopic surface variations) rather than just a flat image, the material will react accurately to any lighting environment. True displacement pushes this further by physically altering the mesh silhouette, avoiding the "painted on" look of standard normal maps at grazing angles.
* **Overall Applicability**: This technique is mandatory for any photorealistic asset, including architectural visualization, product rendering, environment design, and character art. 
* **Value Addition**: Compared to a basic shaded primitive, this setup transforms a flat plane into a rich, tactile surface with physical depth, dynamic light reaction, and realistic physical imperfections.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  * **Base Mesh**: A simple flat Plane.
  * **Modifiers**: A Subdivision Surface modifier is applied. For true displacement in Cycles, the scene must be set to `Experimental` Feature Set, allowing the use of **Adaptive Subdivision**. Adaptive subdivision dynamically subdivides the mesh more heavily closer to the camera, optimizing memory while providing massive geometry detail for the displacement map to push around.
* **Step B: Materials & Shading**
  * **Workflow Selection**: The tutorial uses a Specular/Gloss workflow translated into Blender's Metalness/Roughness standard.
  * **Data vs. Color**: Base Color maps are set to `sRGB` Color Space. All physical property maps (Reflection, Gloss, Normal, Displacement) must be set to `Non-Color` data, otherwise, Blender will apply a gamma curve to them, ruining the mathematical values.
  * **Gloss Inversion**: Because Blender's Principled BSDF uses "Roughness" (0 = smooth, 1 = rough), and the downloaded map is "Gloss" (0 = rough, 1 = smooth), an `Invert Color` node is placed between the texture and the BSDF.
  * **Displacement Activation**: The `Displacement` node is connected to the Material Output. Crucially, the material's internal settings (Properties Panel -> Material -> Settings -> Surface) must have Displacement set to **"Displacement and Bump"** (it defaults to "Bump Only", which ignores true geometry displacement).
* **Step C: Lighting & Rendering Context**
  * **Render Engine**: Cycles is required for true mesh displacement. EEVEE will only interpret displacement maps as a bump effect.
  * **Lighting**: A strong angled light (like a Sun or Area light) is highly recommended to highlight the shadows cast by the newly displaced geometry and the micro-details of the normal map.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Geometry & Topology | `bpy.ops.mesh.primitive` + Subdivision Modifier | We need a base mesh with high-density geometry to support true physical displacement. |
| PBR Texturing Workflow | Shader Node Tree (Procedural Stand-ins) | To guarantee reproducibility without relying on external downloaded image files, I am using procedural textures (Brick, Noise) wired into the **exact same logical framework** taught in the tutorial (Invert nodes for gloss, Bump/Normal routing, and True Displacement nodes). |
| True Displacement | Cycles Settings + Material Displacement API | Modifying scene render engines and material property settings via Python is the only way to activate actual geometry displacement. |

> **Feasibility Assessment**: 100% of the *technical workflow* is reproduced. While we cannot use the specific downloaded Poliiigon textures from the video without local files, the generated code builds the exact node architecture (Gloss inversion, Normal/Bump routing, Displacement mapping) and render settings required for the PBR workflow, swapping external images for procedural generators.

#### 3b. Complete Reproduction Code

```python
def create_pbr_displacement_setup(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Surface",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 2.0,
    base_color_1: tuple = (0.6, 0.2, 0.1, 1.0), # Brick red
    base_color_2: tuple = (0.4, 0.1, 0.05, 1.0), # Dark brick
    **kwargs,
) -> str:
    """
    Creates a surface demonstrating a complete PBR material setup with true displacement.
    Uses procedural nodes to mimic the workflow of mapping Color, Gloss, Reflection, 
    Normal, and Displacement maps.
    
    Args:
        scene_name: Name of the scene.
        object_name: Name of the created mesh.
        location: World-space coordinates.
        scale: Size of the surface plane.
        base_color_1/2: Primary colors for the procedural texture.
        
    Returns:
        Status string.
    """
    import bpy
    
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    
    # 1. Ensure Cycles is active and Experimental feature set is ON for Adaptive Subdivision
    scene.render.engine = 'CYCLES'
    try:
        scene.cycles.feature_set = 'EXPERIMENTAL'
    except AttributeError:
        pass # Fallback if experimental is not available in specific branch
        
    # 2. Create the Geometry
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Apply scale to ensure displacement math is accurate
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # 3. Add Subdivision Surface modifier for displacement
    subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.subdivision_type = 'CATMULL_CLARK'
    subdiv.levels = 5        # Fallback for EEVEE/Solid view
    subdiv.render_levels = 5 # Fallback for Cycles
    try:
        # Enable adaptive subdivision if Cycles Experimental is active
        subdiv.use_adaptive_subdivision = True
    except AttributeError:
        pass

    # 4. Create the PBR Material
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    # CRITICAL: Enable True Displacement in material settings
    mat.cycles.displacement_method = 'DISPLACEMENT_BUMP'
    
    # 5. Build the PBR Node Tree
    tree = mat.node_tree
    nodes = tree.nodes
    links = tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
        
    # Add core output and shader nodes
    output_node = nodes.new('ShaderNodeOutputMaterial')
    output_node.location = (1000, 0)
    
    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (600, 200)
    
    # Add Mapping setup (Ctrl+T in Node Wrangler)
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 200)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 200)
    # Tweak scale slightly for better procedural look
    mapping.inputs['Scale'].default_value = (2.0, 2.0, 2.0)
    
    # Add Procedural Textures to act as our downloaded Image Maps
    # A. "Base Color" & "Displacement" Map Stand-in
    mock_color_map = nodes.new('ShaderNodeTexBrick')
    mock_color_map.name = "Mock_Color_Map"
    mock_color_map.location = (-200, 400)
    mock_color_map.inputs['Color1'].default_value = base_color_1
    mock_color_map.inputs['Color2'].default_value = base_color_2
    
    # B. "Gloss" and "Reflection" Map Stand-in
    mock_gloss_map = nodes.new('ShaderNodeTexNoise')
    mock_gloss_map.name = "Mock_Gloss_Map"
    mock_gloss_map.location = (-200, 0)
    mock_gloss_map.inputs['Scale'].default_value = 15.0
    mock_gloss_map.inputs['Detail'].default_value = 15.0
    
    # --- PBR Workflow Logic Nodes ---
    
    # Gloss to Roughness Inversion
    invert_node = nodes.new('ShaderNodeInvert')
    invert_node.location = (200, 50)
    invert_node.label = "Gloss -> Roughness Invert"
    
    # Reflection to Specular mapping (adding contrast to noise)
    specular_ramp = nodes.new('ShaderNodeValToRGB')
    specular_ramp.location = (200, -100)
    specular_ramp.color_ramp.elements[0].position = 0.4
    specular_ramp.color_ramp.elements[1].position = 0.6
    
    # Normal Mapping
    bump_node = nodes.new('ShaderNodeBump')
    bump_node.location = (200, -300)
    bump_node.inputs['Distance'].default_value = 0.05
    bump_node.label = "Normal/Bump Map"
    
    # True Displacement Setup
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (600, -200)
    disp_node.inputs['Midlevel'].default_value = 0.0
    disp_node.inputs['Scale'].default_value = 0.1 # Crucial: default 1.0 is usually way too high
    
    # --- Connect Everything ---
    
    # Mapping
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], mock_color_map.inputs['Vector'])
    links.new(mapping.outputs['Vector'], mock_gloss_map.inputs['Vector'])
    
    # Base Color
    links.new(mock_color_map.outputs['Color'], bsdf_node.inputs['Base Color'])
    
    # Gloss -> Roughness
    links.new(mock_gloss_map.outputs['Fac'], invert_node.inputs['Color'])
    links.new(invert_node.outputs['Color'], bsdf_node.inputs['Roughness'])
    
    # Reflection -> Specular
    links.new(mock_gloss_map.outputs['Fac'], specular_ramp.inputs['Fac'])
    links.new(specular_ramp.outputs['Color'], bsdf_node.inputs['Specular IOR Level']) # 'Specular' in older versions
    
    # Normal/Bump
    links.new(mock_color_map.outputs['Fac'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], bsdf_node.inputs['Normal'])
    
    # True Displacement
    links.new(mock_color_map.outputs['Fac'], disp_node.inputs['Height'])
    links.new(disp_node.outputs['Displacement'], output_node.inputs['Displacement'])
    
    # Final Output
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
    
    # Add a strong light to show off the displacement and normals
    bpy.ops.object.light_add(type='SUN', radius=1.0, location=(location[0] + 5, location[1] - 5, location[2] + 10))
    sun = bpy.context.active_object
    sun.data.energy = 3.0
    sun.data.angle = 0.1 # Sharp shadows to highlight displacement
    # Aim sun at the surface
    import math
    from mathutils import Euler
    sun.rotation_euler = Euler((math.radians(45), 0, math.radians(45)), 'XYZ')

    # Deselect all and set active to main object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    return f"Created '{object_name}' PBR workflow demonstration with True Displacement in Cycles."
```