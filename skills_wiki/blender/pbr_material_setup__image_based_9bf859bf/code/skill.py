def create_pbr_material_object(
    object_name: str = "PBR_Object",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    pbr_map_paths: dict = None,
    subdivision_levels_viewport: int = 2,
    subdivision_levels_render: int = 2,
    use_adaptive_subdivision: bool = False,
    displacement_midlevel: float = 0.0, # As per tutorial to prevent overall shift
    displacement_scale: float = 0.02, # Example value, usually small
    normal_strength: float = 1.0,
) -> str:
    """
    Creates a plane with a PBR material setup using provided image texture paths.
    Requires Node Wrangler addon enabled for proper node arrangement.

    Args:
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the object.
        pbr_map_paths: Dictionary where keys are map types (e.g., 'COL', 'REFL', 'GLOSS', 'NRM', 'DISP')
                       and values are absolute file paths to the image textures.
                       Example: {'COL': '/path/to/albedo.jpg', 'NRM': '/path/to/normal.png'}
        subdivision_levels_viewport: Subdivision level for viewport.
        subdivision_levels_render: Subdivision level for render.
        use_adaptive_subdivision: If True, enables adaptive subdivision (requires Cycles & Experimental feature set).
        displacement_midlevel: Midlevel for displacement node (0.0 often recommended).
        displacement_scale: Strength of the displacement effect.
        normal_strength: Strength of the normal map effect.

    Returns:
        Status string describing the created object.
    """
    import bpy
    from mathutils import Vector
    import os

    if pbr_map_paths is None:
        return "Error: PBR map paths dictionary is required."

    # --- 1. Create Base Geometry (Plane) ---
    bpy.ops.mesh.primitive_plane_add(
        size=2,
        enter_editmode=False,
        align='WORLD',
        location=location,
    )
    obj = bpy.context.object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # --- Add Subdivision Surface Modifier for potential displacement ---
    subdiv_mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv_mod.levels = subdivision_levels_viewport
    subdiv_mod.render_levels = subdivision_levels_render
    subdiv_mod.subdivision_type = 'SIMPLE' # Simple is used in tutorial's displacement example

    if use_adaptive_subdivision:
        if bpy.context.scene.render.engine == 'CYCLES':
            bpy.context.scene.cycles.feature_set = 'EXPERIMENTAL'
            subdiv_mod.use_adaptive_subdivision = True
            # subdiv_mod.dicing_scale = 1.0 # Default. Can be adjusted.
        else:
            print(f"Warning: Adaptive Subdivision requires Cycles render engine, but '{bpy.context.scene.render.engine}' is active. Falling back to regular subdivision.")

    # --- 2. Create Material ---
    mat_name = f"{object_name}_Material"
    material = bpy.data.materials.new(name=mat_name)
    material.use_nodes = True
    obj.data.materials.clear() # Clear default material slot
    obj.data.materials.append(material)

    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Clear default nodes if any (should only be Principled BSDF and Material Output)
    for node in nodes:
        if node.type == 'BSDF_PRINCIPLED':
            principled_bsdf = node
        elif node.type == 'OUTPUT_MATERIAL':
            material_output = node
        else:
            nodes.remove(node)

    # Ensure Principled BSDF and Material Output exist
    if not principled_bsdf:
        principled_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled_bsdf.location = (200, 0)
        links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])
    if not material_output: # Should already exist by default.
        material_output = nodes.new(type='ShaderNodeOutputMaterial')
        material_output.location = (400, 0)
        links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])
    
    # --- Texture Coordinate and Mapping Nodes ---
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-600, 0)

    # Connect UV output from Texture Coordinate to Vector input of Mapping
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])

    # Dictionary to store created image texture nodes for wiring
    # This section mimics Node Wrangler's Ctrl+Shift+T functionality
    # Arranging nodes vertically for readability.
    y_pos_counter = 0 
    node_offset_y = -200 # Vertical spacing between texture nodes

    # --- Load and Connect PBR Maps ---
    # COL - Base Color
    if 'COL' in pbr_map_paths and os.path.exists(pbr_map_paths['COL']):
        img_node_col = nodes.new(type='ShaderNodeTexImage')
        img_node_col.image = bpy.data.images.load(pbr_map_paths['COL'], check_existing=True)
        img_node_col.location = (-400, y_pos_counter)
        img_node_col.image.colorspace_settings.name = 'sRGB'
        links.new(mapping.outputs['Vector'], img_node_col.inputs['Vector'])
        links.new(img_node_col.outputs['Color'], principled_bsdf.inputs['Base Color'])
        y_pos_counter += node_offset_y

    # REFL - Reflection/Specular
    if 'REFL' in pbr_map_paths and os.path.exists(pbr_map_paths['REFL']):
        img_node_refl = nodes.new(type='ShaderNodeTexImage')
        img_node_refl.image = bpy.data.images.load(pbr_map_paths['REFL'], check_existing=True)
        img_node_refl.location = (-400, y_pos_counter)
        img_node_refl.image.colorspace_settings.name = 'Non-Color' # Specular expects non-color data
        links.new(mapping.outputs['Vector'], img_node_refl.inputs['Vector'])
        links.new(img_node_refl.outputs['Color'], principled_bsdf.inputs['Specular'])
        y_pos_counter += node_offset_y

    # GLOSS - Gloss (converted to Roughness)
    if 'GLOSS' in pbr_map_paths and os.path.exists(pbr_map_paths['GLOSS']):
        img_node_gloss = nodes.new(type='ShaderNodeTexImage')
        img_node_gloss.image = bpy.data.images.load(pbr_map_paths['GLOSS'], check_existing=True)
        img_node_gloss.location = (-400, y_pos_counter)
        img_node_gloss.image.colorspace_settings.name = 'Non-Color'

        invert_node = nodes.new(type='ShaderNodeInvert')
        invert_node.location = (-100, y_pos_counter) # Position invert node near roughness input
        links.new(img_node_gloss.outputs['Color'], invert_node.inputs['Color'])
        links.new(mapping.outputs['Vector'], img_node_gloss.inputs['Vector'])
        links.new(invert_node.outputs['Color'], principled_bsdf.inputs['Roughness'])
        y_pos_counter += node_offset_y

    # NRM - Normal Map
    if 'NRM' in pbr_map_paths and os.path.exists(pbr_map_paths['NRM']):
        img_node_nrm = nodes.new(type='ShaderNodeTexImage')
        img_node_nrm.image = bpy.data.images.load(pbr_map_paths['NRM'], check_existing=True)
        img_node_nrm.location = (-400, y_pos_counter)
        img_node_nrm.image.colorspace_settings.name = 'Non-Color'

        normal_map_node = nodes.new(type='ShaderNodeNormalMap')
        normal_map_node.location = (-100, y_pos_counter) # Position normal map node
        normal_map_node.inputs['Strength'].default_value = normal_strength
        links.new(img_node_nrm.outputs['Color'], normal_map_node.inputs['Color'])
        links.new(mapping.outputs['Vector'], img_node_nrm.inputs['Vector'])
        links.new(normal_map_node.outputs['Normal'], principled_bsdf.inputs['Normal'])
        y_pos_counter += node_offset_y

    # DISP - Displacement Map
    if 'DISP' in pbr_map_paths and os.path.exists(pbr_map_paths['DISP']):
        img_node_disp = nodes.new(type='ShaderNodeTexImage')
        img_node_disp.image = bpy.data.images.load(pbr_map_paths['DISP'], check_existing=True)
        img_node_disp.location = (-400, y_pos_counter)
        img_node_disp.image.colorspace_settings.name = 'Non-Color'

        displacement_node = nodes.new(type='ShaderNodeDisplacement')
        displacement_node.location = (-100, y_pos_counter - 50) # Position displacement node
        displacement_node.inputs['Midlevel'].default_value = displacement_midlevel
        displacement_node.inputs['Scale'].default_value = displacement_scale
        links.new(img_node_disp.outputs['Color'], displacement_node.inputs['Height'])
        links.new(mapping.outputs['Vector'], img_node_disp.inputs['Vector'])
        links.new(displacement_node.outputs['Displacement'], material_output.inputs['Displacement'])
        
        # Set displacement method for the material (requires Cycles)
        if bpy.context.scene.render.engine == 'CYCLES':
            material.cycles.displacement = 'DISPLACEMENT_AND_BUMP' # Use 'BOTH'
        y_pos_counter += node_offset_y

    # Arrange nodes for clarity (Node Wrangler often groups, but direct placement is fine for script)
    # The automatic placement is already done as nodes are created.

    return f"Created PBR object '{object_name}' at {location} with material '{mat_name}'"

