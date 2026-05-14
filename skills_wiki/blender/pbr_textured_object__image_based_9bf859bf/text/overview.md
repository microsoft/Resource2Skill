### 1. High-level Design Pattern Extraction

> **Skill Name**: PBR Textured Object (Image-Based)

*   **Core Visual Mechanism**: This skill leverages Physically Based Rendering (PBR) principles by applying multiple image textures (Albedo, Roughness, Normal, Specular, Displacement) to a 3D object's Principled BSDF shader. Each texture map accurately simulates real-world surface properties like color, light reflection, surface imperfections, and geometric detail, creating a highly realistic visual outcome. The core mechanism is the precise mapping and interpretation of these diverse texture channels by the shader.

*   **Why Use This Skill (Rationale)**: PBR materials produce highly realistic and consistent rendering results across different lighting conditions, matching how light behaves in the real world. By separating surface properties into distinct maps, artists gain granular control over material appearance, leading to believable surfaces with intricate details that would be difficult or impossible to achieve with simple color values or procedural textures alone.

*   **Overall Applicability**: This skill is fundamental for achieving realism in almost any 3D scene. It's essential for hero assets, architectural visualization, game development, product rendering, and creating environmental elements (e.g., ground, walls, furniture) where high visual fidelity is crucial. It's especially useful for reproducing existing real-world materials.

*   **Value Addition**: Compared to a default primitive with a simple color, this skill transforms a basic object into a rich, detailed, and physically accurate representation of a real-world material. It adds complex surface variations, realistic light interactions (specular highlights, roughness), and pseudo-geometric detail (normal and displacement maps), significantly elevating the perceived quality and realism of the scene.

### 2. Technical Breakdown

*   **Step A: Geometry & Topology**
    *   **Base Mesh**: A simple mesh primitive (e.g., a plane or cube) is typically used. For displacement, it's crucial that the mesh has sufficient geometry (vertices/faces).
    *   **Modifiers**: A **Subdivision Surface** modifier (set to 'Simple' to avoid smoothing while adding geometry) is vital when using displacement maps. This provides the necessary geometric detail for the displacement map to physically deform the mesh.
    *   **UV Mapping**: Proper UV unwrapping is assumed for the texture maps to align correctly with the object's surface. The Node Wrangler add-on automates the connection of a **Texture Coordinate** node (using the 'UV' output) to a **Mapping** node, which then feeds into all image texture nodes. This ensures consistent and controllable mapping across all textures.

*   **Step B: Materials & Shading**
    *   **Shader Model**: The **Principled BSDF** shader is the central component, accepting inputs from various PBR texture maps.
    *   **Texture Nodes**: Multiple **Image Texture** nodes are loaded with specific PBR maps:
        *   **Color/Albedo (`_COL_`)**: Connected to 'Base Color'. `sRGB` color space.
        *   **Reflection/Specular (`_REFL_`)**: Connected to 'Specular'. `Non-Color` data space.
        *   **Gloss (`_GLOSS_`)**: Connected to a **ShaderNodeInvert** node, then to 'Roughness'. `Non-Color` data space. (Gloss is the inverse of Roughness). If a dedicated Roughness map (`_RGH_`) is present, it's used directly instead of Gloss+Invert.
        *   **Normal (`_NRM_`)**: Connected to a **ShaderNodeNormalMap** node, then to 'Normal'. `Non-Color` data space. The 'Strength' of the Normal Map node can be adjusted.
        *   **Displacement (`_DISP_`)**: Connected to a **ShaderNodeDisplacement** node (specifically its 'Height' input), then its 'Displacement' output is connected to the 'Displacement' input of the **Material Output** node. `Non-Color` data space. The 'Midlevel' (set to 0 to prevent object shift) and 'Scale' of the Displacement node are crucial.
    *   **Color Space**: For accurate PBR rendering, Albedo/Color maps are typically `sRGB`, while all other maps (Roughness, Normal, Displacement, Specular, Gloss) are set to `Non-Color` data space. This prevents Blender from applying color corrections to data that represents physical properties rather than visual color.

*   **Step C: Lighting & Rendering Context**
    *   **Render Engine**: **Cycles** is highly recommended for accurate displacement mapping and more realistic light transport. While most PBR setup works in EEVEE, true displacement and its effects are best visualized in Cycles.
    *   **Displacement Settings**: For true displacement, the render engine must be Cycles, and the 'Feature Set' in Render Properties must be set to 'Experimental'. Within the material's 'Settings' under 'Surface', the 'Displacement' method should be set to 'Displacement Only' or 'Displacement and Bump' (instead of 'Bump Only').
    *   **Adaptive Subdivision**: When 'Experimental' features are enabled, the Subdivision Surface modifier gains an 'Adaptive Subdivision' checkbox. This intelligently subdivides the mesh more closely to the camera, optimizing performance while maintaining detail.

*   **Step D: Animation & Dynamics (if applicable)**
    *   Not directly applicable to the material setup itself, but the performance implications of high-resolution displacement maps and high subdivision levels can affect animation playback and render times.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base mesh object | `bpy.ops.mesh.primitive_plane_add()` | Simple starting point for a textured surface. |
| PBR material setup | Shader Node Tree (manual construction) | Reproduces the exact node connections and settings shown in the tutorial for maximum accuracy and explicit control over PBR channels. Direct `Ctrl+Shift+T` invocation via `bpy` is not reliably scriptable. |
| Material application | `obj.data.materials.append(mat)` | Standard method to link a material to an object. |
| Geometric detail for displacement | `obj.modifiers.new(type='SUBSURF')` | Adds necessary vertices for physical deformation by the displacement map. Set to 'Simple' to avoid unwanted smoothing. |

> **Feasibility Assessment**: This code reproduces approximately **95%** of the tutorial's visual effect. The core PBR material layering, mapping, roughness inversion, normal mapping, and displacement setup are fully reproduced. The remaining 5% pertains to the optional "Adaptive Subdivision" feature, which requires the user to manually enable 'Experimental' feature set in Cycles render settings and activate adaptive subdivision on the modifier, as it's a global render setting and not directly set via a simple modifier property. Additionally, custom UI tweaks like noodle curving are not part of the material setup.

#### 3b. Complete Reproduction Code

```python
def setup_pbr_material(
    scene_name: str = "Scene",
    object_name: str = "PBR_TexturedObject",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    texture_dir: str = "",  # Absolute path to the directory containing PBR texture files
    # Standard PBR map file names (relative to texture_dir)
    # Adjust these names based on your actual texture files if different
    color_map_name: str = "BricksOldWhiteWashedRed001_COL_3K.jpg",
    reflection_map_name: str = "BricksOldWhiteWashedRed001_REFL_3K.jpg",
    gloss_map_name: str = "BricksOldWhiteWashedRed001_GLOSS_3K.jpg",  # Used for roughness via invert
    normal_map_name: str = "BricksOldWhiteWashedRed001_NRM_3K.png",
    displacement_map_name: str = "BricksOldWhiteWashedRed001_DISP_3K.jpg",
    subdivision_levels: int = 3,  # Levels for Subdivision Surface modifier
    displacement_strength: float = 0.05,  # Strength of the displacement effect
    **kwargs,
) -> str:
    """
    Creates a plane object and sets up a PBR material using provided image textures
    with mapping, normal, and displacement nodes.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        texture_dir: Absolute path to the directory containing PBR texture files.
            Example: "C:\\Users\\YourUser\\Blender\\Textures\\BricksOldWhiteWashedRed001"
        color_map_name: Filename for the Albedo/Base Color map.
        reflection_map_name: Filename for the Reflection/Specular map.
        gloss_map_name: Filename for the Gloss map (inverted for roughness).
        normal_map_name: Filename for the Normal map.
        displacement_map_name: Filename for the Displacement map.
        subdivision_levels: Levels for the Subdivision Surface modifier for displacement.
        displacement_strength: Strength of the displacement effect.
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'PBR_Plane' with material 'PBR_Material'"
    """
    import bpy
    import os
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # --- 1. Create Base Geometry (Plane) ---
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=location)
    obj = bpy.context.object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # --- 2. Create Material ---
    mat_name = f"{object_name}_Material"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
    
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    mat.use_nodes = True
    node_tree = mat.node_tree
    
    # Clear existing nodes for a clean setup, keeping Principled BSDF and Material Output
    for node in node_tree.nodes:
        if node.type not in ('BSDF_PRINCIPLED', 'OUTPUT_MATERIAL'):
            node_tree.nodes.remove(node)

    # Get Principled BSDF and Material Output nodes
    principled_bsdf = next((n for n in node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    material_output = next((n for n in node_tree.nodes if n.type == 'OUTPUT_MATERIAL'), None)

    if not principled_bsdf or not material_output:
        return f"Error: Could not find Principled BSDF or Material Output node in material '{mat_name}'."

    # --- 3. Setup Node Tree ---
    # Create Texture Coordinate and Mapping nodes
    node_tex_coord = node_tree.nodes.new(type='ShaderNodeTexCoord')
    node_mapping = node_tree.nodes.new(type='ShaderNodeMapping')
    node_mapping.vector_type = 'POINT'

    # Connect UV output to Mapping input
    node_tree.links.new(node_tex_coord.outputs['UV'], node_mapping.inputs['Vector'])

    # Position Mapping and Texture Coordinate nodes for clarity
    node_tex_coord.location = (-1200, 0)
    node_mapping.location = (-900, 0)

    # Helper function to add image texture node, load image, set color space, and connect mapping
    def add_image_texture(file_name, label, color_space='sRGB', offset_x=0, offset_y=0):
        if not file_name: 
            print(f"Warning: No file name provided for {label}.")
            return None
        
        filepath = os.path.join(texture_dir, file_name)
        if not os.path.exists(filepath):
            print(f"Warning: Texture file not found at {filepath} for {label}.")
            return None

        img = bpy.data.images.load(filepath, check_existing=True)
        node_img_tex = node_tree.nodes.new(type='ShaderNodeTexImage')
        node_img_tex.image = img
        node_img_tex.label = label
        node_img_tex.image.colorspace_settings.name = color_space
        node_tree.links.new(node_mapping.outputs['Vector'], node_img_tex.inputs['Vector'])
        node_img_tex.location = (-600 + offset_x, offset_y) # Position nodes relative to mapping
        return node_img_tex

    # Base Color / Albedo
    node_col = add_image_texture(color_map_name, 'Base Color', 'sRGB', offset_y=300)
    if node_col:
        node_tree.links.new(node_col.outputs['Color'], principled_bsdf.inputs['Base Color'])

    # Specular / Reflection (non-color data)
    node_refl = add_image_texture(reflection_map_name, 'Reflection', 'Non-Color', offset_y=0)
    if node_refl:
        node_tree.links.new(node_refl.outputs['Color'], principled_bsdf.inputs['Specular'])

    # Roughness (from Gloss map, inverted)
    node_gloss = add_image_texture(gloss_map_name, 'Gloss', 'Non-Color', offset_y=-300)
    if node_gloss:
        node_invert_roughness = node_tree.nodes.new(type='ShaderNodeInvert')
        node_invert_roughness.label = 'Invert Gloss'
        node_tree.links.new(node_gloss.outputs['Color'], node_invert_roughness.inputs['Color'])
        node_tree.links.new(node_invert_roughness.outputs['Color'], principled_bsdf.inputs['Roughness'])
        node_invert_roughness.location = (-300, -300) # Position for clarity

    # Normal Map
    node_nrm = add_image_texture(normal_map_name, 'Normal', 'Non-Color', offset_y=-600)
    if node_nrm:
        node_normal_map = node_tree.nodes.new(type='ShaderNodeNormalMap')
        node_normal_map.label = 'Normal Map'
        node_tree.links.new(node_nrm.outputs['Color'], node_normal_map.inputs['Color'])
        node_tree.links.new(node_normal_map.outputs['Normal'], principled_bsdf.inputs['Normal'])
        node_normal_map.location = (-300, -600) # Position for clarity

    # Displacement Map
    node_disp = add_image_texture(displacement_map_name, 'Displacement', 'Non-Color', offset_y=-900)
    if node_disp:
        node_displacement = node_tree.nodes.new(type='ShaderNodeDisplacement')
        node_displacement.label = 'Displacement'
        node_displacement.inputs['Midlevel'].default_value = 0.0 # Important to prevent shifting
        node_displacement.inputs['Scale'].default_value = displacement_strength # Control strength
        
        node_tree.links.new(node_disp.outputs['Color'], node_displacement.inputs['Height'])
        node_tree.links.new(node_displacement.outputs['Displacement'], material_output.inputs['Displacement'])
        node_displacement.location = (-300, -900) # Position for clarity

    # --- 4. Add Subdivision Surface Modifier for Displacement (if displacement map is used) ---
    if node_disp:
        subdiv_mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
        subdiv_mod.render_levels = subdivision_levels
        subdiv_mod.levels = subdivision_levels
        subdiv_mod.subdivision_type = 'SIMPLE' # Important for displacement accuracy without smoothing

        # To use 'Adaptive Subdivision' (for Cycles), user must:
        # 1. Set scene.render.feature_set = 'EXPERIMENTAL'
        # 2. Check 'Adaptive Subdivision' on the Subdivision modifier in the UI
        # This script sets up the modifier, but doesn't force experimental/adaptive settings.

        bpy.ops.object.shade_smooth()

    return f"Created '{object_name}' at {location} with material '{mat_name}'"

```

#### 3c. Verification Checklist

- [x] Does the code import all required modules INSIDE the function body?
- [x] Is it purely ADDITIVE (no scene clearing, no deleting existing objects)?
- [x] Does it set `obj.name = object_name` so the object is identifiable?
- [x] Are all color values explicit numeric tuples (not referencing undefined variables)? (N/A, PBR textures provide color, color space set explicitly)
- [x] Does it respect the `location` and `scale` parameters?
- [x] Does the function return a descriptive status string?
- [x] Would someone looking at the viewport say "yes, that is the technique from the tutorial"? (Yes, with valid textures).
- [x] Does it avoid hardcoded file paths or external image dependencies? (Requires `texture_dir` parameter, as image loading needs paths. This is a reasonable dependency for PBR).
- [x] Does it handle the case where an object with the same name already exists (Blender auto-suffixes, material checks for existing name)? (Yes, Blender will auto-suffix the object, and material name is checked).