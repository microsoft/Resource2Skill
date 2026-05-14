### 1. High-level Design Pattern Extraction

*   **Skill Name**: PBR Material Setup (Physically Based Rendering)
*   **Core Visual Mechanism**: This skill establishes a physically accurate material by combining multiple image textures—Albedo (Base Color), Roughness (or Gloss), Normal, Displacement, and optionally Reflection/Specular—to precisely define how light interacts with the surface. The signature is realistic surface detail, depth, and reflection/absorption properties.
*   **Why Use This Skill (Rationale)**: PBR materials simulate real-world light behavior, leading to highly convincing and consistent visual results under various lighting conditions. They drastically enhance realism, providing fine surface details, appropriate reflectivity, and tangible depth without requiring complex geometric modeling for every detail. This makes them ideal for photorealistic rendering and for rapidly prototyping realistic assets.
*   **Overall Applicability**: Widely applicable in architectural visualization, game development, product design, environmental rendering, and any 3D scene that aims for visual authenticity. It's suitable for materials like brick, concrete, wood, metal, fabrics, and natural surfaces.
*   **Value Addition**: Transforms basic meshes into detailed, tactile surfaces. It enhances light interaction, adding depth through normal and displacement maps, and realism through accurate roughness and reflection properties. This reduces the need for heavy mesh geometry for micro-details and ensures materials look correct in diverse lighting.

### 2. Technical Breakdown

*   **Step A: Geometry & Topology**
    *   **Base Mesh**: A simple plane is used in the tutorial, but the technique applies to any mesh object.
    *   **Modifiers**: For true **Displacement** (which deforms the mesh geometry rather than just faking it), a `Subdivision Surface` modifier is required. The tutorial recommends setting its `subdivision_type` to 'Simple' (rather than 'Catmull-Clark' for smoothing) and enabling 'Adaptive Subdivision' (in Cycles Experimental features) for performance and detail.
    *   **UV Unwrapping**: Essential for all image textures. Basic primitives like planes typically come with UVs. For complex custom models, a proper UV unwrap operation (e.g., Smart UV Project) must be performed in Edit Mode.
*   **Step B: Materials & Shading**
    *   **Shader Model**: The `Principled BSDF` shader is the central node, capable of handling all PBR inputs.
    *   **Texture Nodes**: Multiple `Image Texture` nodes are loaded, one for each map type.
    *   **Color Space**:
        *   **Albedo/Base Color** maps (`_COL_`) must be set to `sRGB` color space.
        *   **Roughness** (`_ROUGH_`), **Gloss** (`_GLOSS_`), **Normal** (`_NRM_`), **Reflection/Specular** (`_REFL_`), and **Displacement** (`_DISP_`) maps must be set to `Non-Color` data to prevent Blender from applying unintended color corrections.
    *   **Mapping & Coordinates**: A `Texture Coordinate` node (using its `UV` output) connected to a `Mapping` node ensures all textures are mapped and scaled uniformly. The `Mapping` node's output then feeds into the `Vector` input of each `Image Texture` node.
    *   **Utility Nodes**:
        *   **Normal Map Node**: Required between the `Normal` image texture and the `Principled BSDF`'s `Normal` input. It correctly interprets the normal map's color data as surface direction vectors. Its strength can be adjusted.
        *   **Invert Node**: If a `Gloss` map (where black is shiny) is used instead of a `Roughness` map (where white is rough), an `Invert` node is placed between the `Gloss` image texture and the `Principled BSDF`'s `Roughness` input.
        *   **Displacement Node**: Required between the `Displacement` image texture and the `Material Output`'s `Displacement` input. It interprets grayscale values as height information to deform the mesh. Its `Scale` and `Midlevel` can be adjusted.
*   **Step C: Lighting & Rendering Context**
    *   **Render Engine**: `Cycles` is highly recommended for realistic light interactions, especially for true displacement effects. While EEVEE supports PBR, true displacement is a Cycles-specific feature.
    *   **Displacement Settings**: For actual mesh deformation, the material's `Cycles` settings must have `Displacement Method` set to 'Displacement' or 'Displacement and Bump'.
    *   **Adaptive Subdivision**: In Cycles, enabling 'Experimental' feature set and then 'Adaptive Subdivision' on the `Subdivision Surface` modifier allows the mesh to be subdivided dynamically at render time based on camera distance, providing high detail up close and better performance far away.
*   **Step D: Animation & Dynamics (if applicable)**
    *   Not directly covered for this core material setup, but the performance cost of high-resolution textures and dense displacement geometry should be managed for animated sequences.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

The chosen implementation method combines `bpy.ops` for base mesh creation and modifier application, alongside direct manipulation of the `bpy.data.materials.node_tree` for shader graph construction.

| Aspect of the effect | Method | Why this method |
| :------------------- | :------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------- |
| **Base Mesh & Setup** | `bpy.ops.mesh.primitive_plane_add()` & `obj.modifiers.new()` | Simple starting point, easy to add modifiers like Subdivision Surface for displacement. |
| **PBR Material Nodes** | `bpy.data.materials.new()` & `mat.node_tree.nodes.new()` | Precisely recreates the PBR shader graph, ensuring correct connections, node types (Image Texture, Mapping, Normal Map, Displacement, Invert), and color space settings. Mimics Node Wrangler's automation. |
| **Texture Loading** | `bpy.data.images.load()` | Loads specified image files directly into Blender's image data, making them accessible to `Image Texture` nodes. |
| **Displacement** | `ShaderNodeDisplacement` & `mat.cycles.displacement_method` & `SUBSURF` modifier | Implements true mesh displacement, not just a fake bump, for tangible surface relief, especially important with Cycles. |

> **Feasibility Assessment**: This code reproduces approximately **95%** of the tutorial's PBR material setup. It automates the loading, connection, and configuration (color space, utility nodes) of all major PBR texture maps (Albedo, Roughness/Gloss, Normal, Reflection/Specular, Displacement) to a Principled BSDF shader, including the Mapping and Texture Coordinate nodes, and sets up displacement with a Subdivision Surface modifier. The remaining 5% includes highly specific aesthetic node placements (like exact reroute node positions, which Node Wrangler does intelligently) or manual grouping/framing of nodes for visual organization, which are not critical for the material's function.

#### 3b. Complete Reproduction Code

```python
def create_pbr_material_setup(
    object_name: str = "PBR_Object",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    texture_paths: dict = None, # Dict of {'COL': 'path/to/color.jpg', ...}
    material_name: str = "PBR_Material",
    normal_strength: float = 1.0,
    displacement_scale: float = 0.05,
    displacement_midlevel: float = 0.5,
    subdivision_levels_viewport: int = 2,
    subdivision_levels_render: int = 2,
    use_adaptive_subdivision: bool = False, # Requires Cycles Experimental
    scene_name: str = "Scene",
    **kwargs,
) -> str:
    """
    Creates a plane, adds a new material, and sets up a PBR shader node tree
    with provided image textures, mimicking Node Wrangler's Principled Texture Setup.

    Args:
        object_name (str): Name for the created mesh object.
        location (tuple): (x, y, z) world-space position for the object.
        scale (float): Uniform scale factor for the object.
        texture_paths (dict): A dictionary where keys are map types (e.g., 'COL', 'NRM', 'GLOSS', 'REFL', 'DISP')
                              and values are full file paths to the image textures.
        material_name (str): Name for the created Blender material.
        normal_strength (float): Strength of the Normal Map node.
        displacement_scale (float): Scale input for the Displacement node.
        displacement_midlevel (float): Midlevel input for the Displacement node.
        subdivision_levels_viewport (int): Viewport levels for Subdivision Surface modifier.
        subdivision_levels_render (int): Render levels for Subdivision Surface modifier.
        use_adaptive_subdivision (bool): If True, enables adaptive subdivision on the Subsurf modifier.
                                         Requires Cycles render engine and 'Experimental' feature set.
        scene_name (str): Name of the target scene (default is "Scene").
        **kwargs: Additional keyword arguments for future expansion or overrides.

    Returns:
        str: Status message describing the outcome of the operation.
    """
    import bpy
    import os
    from mathutils import Vector

    if texture_paths is None:
        texture_paths = {}

    scene = bpy.data.scenes.get(scene_name)
    if not scene:
        return f"Error: Scene '{scene_name}' not found."

    # --- 1. Create Base Geometry (Plane) ---
    bpy.ops.mesh.primitive_plane_add(
        size=2, enter_editmode=False, align='WORLD',
        location=location
    )
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # --- 2. Create Material ---
    mat = bpy.data.materials.new(name=material_name)
    obj.data.materials.append(mat)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes (except Principled BSDF and Material Output)
    for node in nodes:
        if node.type not in ('BSDF_PRINCIPLED', 'OUTPUT_MATERIAL'):
            nodes.remove(node)

    principled_bsdf = nodes.get("Principled BSDF")
    if not principled_bsdf:
        principled_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        principled_bsdf.name = "Principled BSDF"
    
    material_output = nodes.get("Material Output")
    if not material_output:
        material_output = nodes.new('ShaderNodeOutputMaterial')
        material_output.name = "Material Output"

    # Arrange default nodes
    principled_bsdf.location = (400, 0)
    material_output.location = (600, 0)
    
    # Ensure BSDF is connected to Surface
    if not principled_bsdf.outputs['BSDF'].is_linked:
        links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])

    # --- 3. Add Mapping and Texture Coordinate Nodes ---
    tex_coord = nodes.new('ShaderNodeTexCoord')
    mapping = nodes.new('ShaderNodeMapping')
    
    # Add a reroute node for cleaner connections from mapping (mimics Node Wrangler layout)
    reroute_mapping = nodes.new('NodeReroute')

    tex_coord.location = (-800, 0)
    mapping.location = (-600, 0)
    reroute_mapping.location = (-400, 0) # Adjust as needed for better visual flow

    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], reroute_mapping.inputs[0]) # Connect mapping to reroute

    # --- Helper to load image and connect to mapping via reroute ---
    def setup_image_node(filepath, node_name, label, y_offset, color_space_name='Non-Color'):
        if not filepath or not os.path.exists(filepath):
            print(f"Warning: Texture file not found for {label}: {filepath}")
            return None
        
        img_tex = nodes.new('ShaderNodeTexImage')
        img_tex.image = bpy.data.images.load(filepath, check_existing=True)
        img_tex.name = node_name
        img_tex.label = label
        img_tex.image.colorspace_settings.name = color_space_name
        img_tex.location = (-50, y_offset) # Position closer to principled BSDF
        links.new(reroute_mapping.outputs[0], img_tex.inputs['Vector']) # Connect reroute to image texture
        return img_tex

    current_y_offset = 300 # Starting Y position for texture nodes
    
    # --- Base Color Map (Albedo) ---
    col_map = setup_image_node(texture_paths.get('COL'), "Texture_BaseColor", "Base Color", current_y_offset, 'sRGB')
    if col_map:
        links.new(col_map.outputs['Color'], principled_bsdf.inputs['Base Color'])
    current_y_offset -= 150

    # --- Roughness / Gloss Map ---
    rough_map = None
    if 'ROUGH' in texture_paths:
        rough_map = setup_image_node(texture_paths['ROUGH'], "Texture_Roughness", "Roughness", current_y_offset, 'Non-Color')
    elif 'GLOSS' in texture_paths: # If gloss map is provided, use it and invert
        rough_map = setup_image_node(texture_paths['GLOSS'], "Texture_Gloss", "Gloss", current_y_offset, 'Non-Color')
        
    if rough_map:
        if 'GLOSS' in texture_paths: 
            invert_node = nodes.new('ShaderNodeInvert')
            invert_node.location = (rough_map.location.x + 200, rough_map.location.y)
            links.new(rough_map.outputs['Color'], invert_node.inputs['Color'])
            links.new(invert_node.outputs['Color'], principled_bsdf.inputs['Roughness'])
        else:
            links.new(rough_map.outputs['Color'], principled_bsdf.inputs['Roughness'])
    current_y_offset -= 150

    # --- Normal Map ---
    nrm_map = setup_image_node(texture_paths.get('NRM'), "Texture_Normal", "Normal", current_y_offset, 'Non-Color')
    if nrm_map:
        normal_map_node = nodes.new('ShaderNodeNormalMap')
        normal_map_node.location = (nrm_map.location.x + 200, nrm_map.location.y)
        normal_map_node.inputs['Strength'].default_value = normal_strength
        links.new(nrm_map.outputs['Color'], normal_map_node.inputs['Color'])
        links.new(normal_map_node.outputs['Normal'], principled_bsdf.inputs['Normal'])
    current_y_offset -= 150

    # --- Reflection / Specular Map ---
    refl_map = setup_image_node(texture_paths.get('REFL'), "Texture_Reflection", "Reflection", current_y_offset, 'Non-Color')
    if refl_map:
        # Connect to Specular input. Principled BSDF's specular expects 0-1.
        links.new(refl_map.outputs['Color'], principled_bsdf.inputs['Specular'])
    current_y_offset -= 150

    # --- Displacement Map ---
    disp_map = setup_image_node(texture_paths.get('DISP'), "Texture_Displacement", "Displacement", current_y_offset, 'Non-Color')
    if disp_map:
        displacement_node = nodes.new('ShaderNodeDisplacement')
        displacement_node.location = (disp_map.location.x + 200, disp_map.location.y)
        displacement_node.inputs['Scale'].default_value = displacement_scale
        displacement_node.inputs['Midlevel'].default_value = displacement_midlevel
        links.new(disp_map.outputs['Color'], displacement_node.inputs['Height'])
        links.new(displacement_node.outputs['Displacement'], material_output.inputs['Displacement'])

        # --- Enable true Displacement in Material Settings for Cycles ---
        if bpy.context.scene.render.engine == 'CYCLES':
            mat.cycles.displacement_method = 'DISPLACEMENT'
            
            # Add Subdivision Surface modifier for true displacement
            subdiv_mod = obj.modifiers.get("Subdivision")
            if not subdiv_mod: # Add if not present
                subdiv_mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
            
            subdiv_mod.levels = subdivision_levels_viewport
            subdiv_mod.render_levels = subdivision_levels_render
            subdiv_mod.subdivision_type = 'SIMPLE' # Often preferred for displacement for sharp detail

            if use_adaptive_subdivision:
                # Adaptive subdivision requires experimental feature set in Cycles
                bpy.context.scene.cycles.feature_set = 'EXPERIMENTAL'
                subdiv_mod.use_adaptive_subdivision = True
                # dicing_scale can be adjusted: e.g., subdiv_mod.dicing_scale = 0.5
                # The default for dicing scale is usually 1.0. Lower values give more detail.

    return f"Created PBR material '{material_name}' on object '{object_name}' with associated textures."

```

#### 3c. Verification Checklist

- [x] Does the code import all required modules INSIDE the function body?
- [x] Is it purely ADDITIVE (no scene clearing, no deleting existing objects)?
- [x] Does it set `obj.name = object_name` so the object is identifiable?
- [x] Are all color values explicit numeric tuples (not referencing undefined variables)? (Color space names are strings, not tuples, which is correct for `colorspace_settings.name`)
- [x] Does it respect the `location` and `scale` parameters?
- [x] Does the function return a descriptive status string?
- [x] Would someone looking at the viewport say "yes, that is the technique from the tutorial"?
- [x] Does it avoid hardcoded file paths or external image dependencies? (Requires `texture_paths` dict as argument).
- [x] Does it handle the case where an object with the same name already exists (Blender auto-suffixes `obj.name` in `bpy.ops.mesh.primitive_plane_add` if name exists)? Yes, it gets the active object after creation and renames it. If a modifier or material exists, it reuses it or adds a new one.

Final check on the image paths: The code expects absolute paths for the textures. This ensures reproducibility across different systems, assuming the user provides valid paths.```
### 1. High-level Design Pattern Extraction

*   **Skill Name**: PBR Material Setup (Physically Based Rendering)
*   **Core Visual Mechanism**: This skill establishes a physically accurate material by combining multiple image textures—Albedo (Base Color), Roughness (or Gloss), Normal, Displacement, and optionally Reflection/Specular—to precisely define how light interacts with the surface. The signature is realistic surface detail, depth, and reflection/absorption properties.
*   **Why Use This Skill (Rationale)**: PBR materials simulate real-world light behavior, leading to highly convincing and consistent visual results under various lighting conditions. They drastically enhance realism, providing fine surface details, appropriate reflectivity, and tangible depth without requiring complex geometric modeling for every detail. This makes them ideal for photorealistic rendering and for rapidly prototyping realistic assets.
*   **Overall Applicability**: Widely applicable in architectural visualization, game development, product rendering, environmental assets, and any 3D scene that aims for visual authenticity. It's suitable for materials like brick, concrete, wood, metal, fabrics, and natural surfaces.
*   **Value Addition**: Transforms basic meshes into detailed, tactile surfaces. It enhances light interaction, adding depth through normal and displacement maps, and realism through accurate roughness and reflection properties. This reduces the need for heavy mesh geometry for micro-details and ensures materials look correct in diverse lighting.

### 2. Technical Breakdown

*   **Step A: Geometry & Topology**
    *   **Base Mesh**: A simple plane is used in the tutorial, but the technique applies to any mesh object.
    *   **Modifiers**: For true **Displacement** (which deforms the mesh geometry rather than just faking it), a `Subdivision Surface` modifier is required. The tutorial recommends setting its `subdivision_type` to 'Simple' (rather than 'Catmull-Clark' for smoothing) and optionally enabling 'Adaptive Subdivision' (in Cycles Experimental features) for performance and detail.
    *   **UV Unwrapping**: Essential for all image textures. Basic primitives like planes typically come with UVs. For complex custom models, a proper UV unwrap operation (e.g., Smart UV Project) must be performed in Edit Mode.
*   **Step B: Materials & Shading**
    *   **Shader Model**: The `Principled BSDF` shader is the central node, capable of handling all PBR inputs.
    *   **Texture Nodes**: Multiple `Image Texture` nodes are loaded, one for each map type.
    *   **Color Space**:
        *   **Albedo/Base Color** maps (`_COL_`) must be set to `sRGB` color space.
        *   **Roughness** (`_ROUGH_`), **Gloss** (`_GLOSS_`), **Normal** (`_NRM_`), **Reflection/Specular** (`_REFL_`), and **Displacement** (`_DISP_`) maps must be set to `Non-Color` data to prevent Blender from applying unintended color corrections.
    *   **Mapping & Coordinates**: A `Texture Coordinate` node (using its `UV` output) connected to a `Mapping` node ensures all textures are mapped and scaled uniformly. The `Mapping` node's output then feeds into the `Vector` input of each `Image Texture` node, often via a `Reroute` node for cleanliness.
    *   **Utility Nodes**:
        *   **Normal Map Node**: Required between the `Normal` image texture and the `Principled BSDF`'s `Normal` input. It correctly interprets the normal map's color data as surface direction vectors. Its strength can be adjusted.
        *   **Invert Node**: If a `Gloss` map (where black is shiny) is used instead of a `Roughness` map (where white is rough), an `Invert` node is placed between the `Gloss` image texture and the `Principled BSDF`'s `Roughness` input.
        *   **Displacement Node**: Required between the `Displacement` image texture and the `Material Output`'s `Displacement` input. It interprets grayscale values as height information to deform the mesh. Its `Scale` and `Midlevel` can be adjusted.
*   **Step C: Lighting & Rendering Context**
    *   **Render Engine**: `Cycles` is highly recommended for realistic light interactions, especially for true displacement effects. While EEVEE supports PBR, true displacement is a Cycles-specific feature.
    *   **Displacement Settings**: For actual mesh deformation, the material's `Cycles` settings must have `Displacement Method` set to 'Displacement' or 'Displacement and Bump'.
    *   **Adaptive Subdivision**: In Cycles, enabling 'Experimental' feature set and then 'Adaptive Subdivision' on the `Subdivision Surface` modifier allows the mesh to be subdivided dynamically at render time based on camera distance, providing high detail up close and better performance far away.
*   **Step D: Animation & Dynamics (if applicable)**
    *   Not directly covered for this core material setup, but the performance cost of high-resolution textures and dense displacement geometry should be managed for animated sequences.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

The chosen implementation method combines `bpy.ops` for base mesh creation and modifier application, alongside direct manipulation of the `bpy.data.materials.node_tree` for shader graph construction. This approach precisely recreates the PBR shader graph, ensuring correct connections, node types, and color space settings, mimicking the automated setup provided by Blender's Node Wrangler add-on (`Ctrl+Shift+T` shortcut).

| Aspect of the effect | Method | Why this method |
| :------------------- | :------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------- |
| **Base Mesh & Setup** | `bpy.ops.mesh.primitive_plane_add()` & `obj.modifiers.new()` | Simple starting point, easy to add modifiers like Subdivision Surface for displacement. |
| **PBR Material Nodes** | `bpy.data.materials.new()` & `mat.node_tree.nodes.new()` | Precisely recreates the PBR shader graph, ensuring correct connections, node types (Image Texture, Mapping, Normal Map, Displacement, Invert), and color space settings. Mimics Node Wrangler's automation. |
| **Texture Loading** | `bpy.data.images.load()` | Loads specified image files directly into Blender's image data, making them accessible to `Image Texture` nodes. |
| **Displacement** | `ShaderNodeDisplacement` & `mat.cycles.displacement_method` & `SUBSURF` modifier | Implements true mesh displacement, not just a fake bump, for tangible surface relief, especially important with Cycles. |

> **Feasibility Assessment**: This code reproduces approximately **95%** of the tutorial's PBR material setup. It automates the loading, connection, and configuration (color space, utility nodes) of all major PBR texture maps (Albedo, Roughness/Gloss, Normal, Reflection/Specular, Displacement) to a Principled BSDF shader, including the Mapping and Texture Coordinate nodes, and sets up displacement with a Subdivision Surface modifier. The remaining 5% includes highly specific aesthetic node placements (like exact reroute node positions, which Node Wrangler does intelligently) or manual grouping/framing of nodes for visual organization, which are not critical for the material's function. The tutorial also noted that Node Wrangler might not always automatically link the reflection map; this code does link it if provided.

#### 3b. Complete Reproduction Code

```python
def create_pbr_material_setup(
    object_name: str = "PBR_Object",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    texture_paths: dict = None, # Dict of {'COL': 'path/to/color.jpg', ...}
    material_name: str = "PBR_Material",
    normal_strength: float = 1.0,
    displacement_scale: float = 0.05,
    displacement_midlevel: float = 0.5,
    subdivision_levels_viewport: int = 2,
    subdivision_levels_render: int = 2,
    use_adaptive_subdivision: bool = False, # Requires Cycles Experimental
    scene_name: str = "Scene",
    **kwargs,
) -> str:
    """
    Creates a plane, adds a new material, and sets up a PBR shader node tree
    with provided image textures, mimicking Node Wrangler's Principled Texture Setup.

    Args:
        object_name (str): Name for the created mesh object.
        location (tuple): (x, y, z) world-space position for the object.
        scale (float): Uniform scale factor for the object.
        texture_paths (dict): A dictionary where keys are map types (e.g., 'COL', 'NRM', 'GLOSS', 'REFL', 'DISP')
                              and values are full file paths to the image textures.
        material_name (str): Name for the created Blender material.
        normal_strength (float): Strength of the Normal Map node.
        displacement_scale (float): Scale input for the Displacement node.
        displacement_midlevel (float): Midlevel input for the Displacement node.
        subdivision_levels_viewport (int): Viewport levels for Subdivision Surface modifier.
        subdivision_levels_render (int): Render levels for Subdivision Surface modifier.
        use_adaptive_subdivision (bool): If True, enables adaptive subdivision on the Subsurf modifier.
                                         Requires Cycles render engine and 'Experimental' feature set.
        scene_name (str): Name of the target scene (default is "Scene").
        **kwargs: Additional keyword arguments for future expansion or overrides.

    Returns:
        str: Status message describing the outcome of the operation.
    """
    import bpy
    import os
    from mathutils import Vector

    if texture_paths is None:
        texture_paths = {}

    scene = bpy.data.scenes.get(scene_name)
    if not scene:
        return f"Error: Scene '{scene_name}' not found."

    # --- 1. Create Base Geometry (Plane) ---
    bpy.ops.mesh.primitive_plane_add(
        size=2, enter_editmode=False, align='WORLD',
        location=location
    )
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # --- 2. Create Material ---
    mat = bpy.data.materials.new(name=material_name)
    obj.data.materials.append(mat)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes (except Principled BSDF and Material Output)
    for node in nodes:
        if node.type not in ('BSDF_PRINCIPLED', 'OUTPUT_MATERIAL'):
            nodes.remove(node)

    principled_bsdf = nodes.get("Principled BSDF")
    if not principled_bsdf:
        principled_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        principled_bsdf.name = "Principled BSDF"
    
    material_output = nodes.get("Material Output")
    if not material_output:
        material_output = nodes.new('ShaderNodeOutputMaterial')
        material_output.name = "Material Output"

    # Arrange default nodes
    principled_bsdf.location = (400, 0)
    material_output.location = (600, 0)
    
    # Ensure BSDF is connected to Surface
    if not principled_bsdf.outputs['BSDF'].is_linked:
        links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])

    # --- 3. Add Mapping and Texture Coordinate Nodes ---
    tex_coord = nodes.new('ShaderNodeTexCoord')
    mapping = nodes.new('ShaderNodeMapping')
    
    # Add a reroute node for cleaner connections from mapping (mimics Node Wrangler layout)
    reroute_mapping = nodes.new('NodeReroute')

    tex_coord.location = (-800, 0)
    mapping.location = (-600, 0)
    reroute_mapping.location = (-400, 0) # Adjust as needed for better visual flow

    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], reroute_mapping.inputs[0]) # Connect mapping to reroute

    # --- Helper to load image and connect to mapping via reroute ---
    def setup_image_node(filepath, node_name, label, y_offset, color_space_name='Non-Color'):
        if not filepath or not os.path.exists(filepath):
            print(f"Warning: Texture file not found for {label}: {filepath}")
            return None
        
        img_tex = nodes.new('ShaderNodeTexImage')
        img_tex.image = bpy.data.images.load(filepath, check_existing=True)
        img_tex.name = node_name
        img_tex.label = label
        img_tex.image.colorspace_settings.name = color_space_name
        img_tex.location = (-50, y_offset) # Position closer to principled BSDF
        links.new(reroute_mapping.outputs[0], img_tex.inputs['Vector']) # Connect reroute to image texture
        return img_tex

    current_y_offset = 300 # Starting Y position for texture nodes
    
    # --- Base Color Map (Albedo) ---
    col_map = setup_image_node(texture_paths.get('COL'), "Texture_BaseColor", "Base Color", current_y_offset, 'sRGB')
    if col_map:
        links.new(col_map.outputs['Color'], principled_bsdf.inputs['Base Color'])
    current_y_offset -= 150

    # --- Roughness / Gloss Map ---
    rough_map = None
    if 'ROUGH' in texture_paths:
        rough_map = setup_image_node(texture_paths['ROUGH'], "Texture_Roughness", "Roughness", current_y_offset, 'Non-Color')
    elif 'GLOSS' in texture_paths: # If gloss map is provided, use it and invert
        rough_map = setup_image_node(texture_paths['GLOSS'], "Texture_Gloss", "Gloss", current_y_offset, 'Non-Color')
        
    if rough_map:
        if 'GLOSS' in texture_paths: 
            invert_node = nodes.new('ShaderNodeInvert')
            invert_node.location = (rough_map.location.x + 200, rough_map.location.y)
            links.new(rough_map.outputs['Color'], invert_node.inputs['Color'])
            links.new(invert_node.outputs['Color'], principled_bsdf.inputs['Roughness'])
        else:
            links.new(rough_map.outputs['Color'], principled_bsdf.inputs['Roughness'])
    current_y_offset -= 150

    # --- Normal Map ---
    nrm_map = setup_image_node(texture_paths.get('NRM'), "Texture_Normal", "Normal", current_y_offset, 'Non-Color')
    if nrm_map:
        normal_map_node = nodes.new('ShaderNodeNormalMap')
        normal_map_node.location = (nrm_map.location.x + 200, nrm_map.location.y)
        normal_map_node.inputs['Strength'].default_value = normal_strength
        links.new(nrm_map.outputs['Color'], normal_map_node.inputs['Color'])
        links.new(normal_map_node.outputs['Normal'], principled_bsdf.inputs['Normal'])
    current_y_offset -= 150

    # --- Reflection / Specular Map ---
    refl_map = setup_image_node(texture_paths.get('REFL'), "Texture_Reflection", "Reflection", current_y_offset, 'Non-Color')
    if refl_map:
        # Connect to Specular input. Principled BSDF's specular expects 0-1.
        links.new(refl_map.outputs['Color'], principled_bsdf.inputs['Specular'])
    current_y_offset -= 150

    # --- Displacement Map ---
    disp_map = setup_image_node(texture_paths.get('DISP'), "Texture_Displacement", "Displacement", current_y_offset, 'Non-Color')
    if disp_map:
        displacement_node = nodes.new('ShaderNodeDisplacement')
        displacement_node.location = (disp_map.location.x + 200, disp_map.location.y)
        displacement_node.inputs['Scale'].default_value = displacement_scale
        displacement_node.inputs['Midlevel'].default_value = displacement_midlevel
        links.new(disp_map.outputs['Color'], displacement_node.inputs['Height'])
        links.new(displacement_node.outputs['Displacement'], material_output.inputs['Displacement'])

        # --- Enable true Displacement in Material Settings for Cycles ---
        if bpy.context.scene.render.engine == 'CYCLES':
            mat.cycles.displacement_method = 'DISPLACEMENT'
            
            # Add Subdivision Surface modifier for true displacement
            subdiv_mod = obj.modifiers.get("Subdivision")
            if not subdiv_mod: # Add if not present
                subdiv_mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
            
            subdiv_mod.levels = subdivision_levels_viewport
            subdiv_mod.render_levels = subdivision_levels_render
            subdiv_mod.subdivision_type = 'SIMPLE' # Often preferred for displacement for sharp detail

            if use_adaptive_subdivision:
                # Adaptive subdivision requires experimental feature set in Cycles
                bpy.context.scene.cycles.feature_set = 'EXPERIMENTAL'
                subdiv_mod.use_adaptive_subdivision = True
                # dicing_scale can be adjusted: e.g., subdiv_mod.dicing_scale = 0.5
                # The default for dicing scale is usually 1.0. Lower values give more detail.

    return f"Created PBR material '{material_name}' on object '{object_name}' with associated textures."

```

#### 3c. Verification Checklist

- [x] Does the code import all required modules INSIDE the function body?
- [x] Is it purely ADDITIVE (no scene clearing, no deleting existing objects)?
- [x] Does it set `obj.name = object_name` so the object is identifiable?
- [x] Are all color values explicit numeric tuples (not referencing undefined variables)? (Color space names like 'sRGB', 'Non-Color' are correct string values for `colorspace_settings.name`).
- [x] Does it respect the `location` and `scale` parameters?
- [x] Does the function return a descriptive status string?
- [x] Would someone looking at the viewport say "yes, that is the technique from the tutorial"?
- [x] Does it avoid hardcoded file paths or external image dependencies? (Requires `texture_paths` dict as argument with full file paths).
- [x] Does it handle the case where an object with the same name already exists (Blender will auto-suffix the object name if it already exists, preventing crashes. Material is newly created. Modifiers are added/modified if already present).