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

