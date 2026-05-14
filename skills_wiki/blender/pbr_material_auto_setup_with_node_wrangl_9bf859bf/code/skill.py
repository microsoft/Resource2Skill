def create_pbr_material_auto_setup(
    scene_name: str = "Scene",
    object_name: str = "PBR_Plane",
    texture_directory: str = "",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_name: str = "PBR_Material",
    displacement_scale: float = 0.02,
    normal_strength: float = 1.0,
    **kwargs,
) -> str:
    """
    Automates the setup of a PBR material using image textures from a specified directory,
    mimicking the Node Wrangler's Ctrl+Shift+T functionality.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created plane object.
        texture_directory: Absolute path to the directory containing PBR texture maps.
                           Files should follow common PBR naming conventions (e.g., _COL_, _NRM_, _GLOSS_, _DISP_).
        location: (x, y, z) world-space position for the created plane.
        scale: Uniform scale factor for the created plane and its texture mapping.
        material_name: Name for the new PBR material.
        displacement_scale: Strength of the displacement effect.
        normal_strength: Strength of the normal map effect.
        **kwargs: Additional overrides (e.g., subdivision_level).

    Returns:
        Status string, e.g., "Created 'PBR_Plane' at (0, 0, 0) with PBR_Material"
    """
    import bpy
    import os
    from mathutils import Vector

    if not texture_directory or not os.path.isdir(texture_directory):
        return f"Error: Texture directory '{texture_directory}' is invalid or not found."

    # Ensure Node Wrangler is enabled (informational, not blocking)
    if 'node_wrangler' not in bpy.context.preferences.addons:
        print("Warning: Node Wrangler add-on is not enabled. Automatic setup relies on its principles.")
        # bpy.ops.preferences.addon_enable(module='node_wrangler') # Uncomment if you want to force-enable

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Create a new plane to apply the material (additive) ---
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # --- Create or get the material ---
    mat = bpy.data.materials.get(material_name)
    if not mat:
        mat = bpy.data.materials.new(name=material_name)
        mat.use_nodes = True
    else:
        # Clear existing nodes for a clean PBR setup
        mat.node_tree.nodes.clear()

    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # --- Create essential nodes ---
    principled_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    mapping = nodes.new(type='ShaderNodeMapping')

    # Position nodes for better readability
    principled_bsdf.location = (400, 0)
    material_output.location = (700, 0)
    tex_coord.location = (-600, 0)
    mapping.location = (-300, 0)

    # Link Texture Coordinate to Mapping
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])

    # Map file suffixes to Principled BSDF inputs and helper nodes
    map_types = {
        '_COL_': {'input': 'Base Color', 'colorspace': 'sRGB'},
        '_DIF_': {'input': 'Base Color', 'colorspace': 'sRGB'},
        '_ALB_': {'input': 'Base Color', 'colorspace': 'sRGB'},
        '_GLOSS_': {'input': 'Roughness', 'colorspace': 'Non-Color', 'invert': True},
        '_REFL_': {'input': 'Specular', 'colorspace': 'Non-Color'}, # Specular not Roughness
        '_ROUGH_': {'input': 'Roughness', 'colorspace': 'Non-Color'},
        '_NRM_': {'input': 'Normal', 'colorspace': 'Non-Color', 'normal_map': True},
        '_NORM_': {'input': 'Normal', 'colorspace': 'Non-Color', 'normal_map': True},
        '_DISP_': {'input': 'Displacement', 'colorspace': 'Non-Color', 'displacement_map': True},
        '_HEIGHT_': {'input': 'Displacement', 'colorspace': 'Non-Color', 'displacement_map': True},
    }

    # Frame to group textures
    textures_frame = nodes.new(type='NodeFrame')
    textures_frame.label = "Textures"
    textures_frame.location = (-100, -300) # Adjust as more textures are added

    # --- Load and link textures ---
    texture_nodes = []
    re_route_node = None # For mapping connections to individual textures

    for root, _, files in os.walk(texture_directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            
            # Find matching map type
            map_info = None
            for suffix, info in map_types.items():
                if suffix in file_name.upper():
                    map_info = info
                    break
            
            if not map_info:
                continue

            img_node = nodes.new(type='ShaderNodeTexImage')
            img_node.label = file_name # Set node label to filename for easy identification
            img_node.image = bpy.data.images.load(file_path, check_existing=True)
            img_node.image.colorspace_settings.name = map_info['colorspace']
            
            img_node.parent = textures_frame # Add to frame
            img_node.location = (0, -100 * len(texture_nodes)) # Arrange vertically within frame
            texture_nodes.append(img_node)

            # Link mapping to image texture
            links.new(mapping.outputs['Vector'], img_node.inputs['Vector'])

            # Handle specific map types
            if map_info.get('normal_map'):
                normal_map_node = nodes.new(type='ShaderNodeNormalMap')
                normal_map_node.location = (principled_bsdf.location.x - 200, principled_bsdf.location.y - 150)
                normal_map_node.inputs['Strength'].default_value = normal_strength
                links.new(img_node.outputs['Color'], normal_map_node.inputs['Color'])
                links.new(normal_map_node.outputs['Normal'], principled_bsdf.inputs['Normal'])
            elif map_info.get('displacement_map'):
                displacement_node = nodes.new(type='ShaderNodeDisplacement')
                displacement_node.location = (material_output.location.x - 200, material_output.location.y - 150)
                displacement_node.inputs['Midlevel'].default_value = 0.0 # As recommended in video
                displacement_node.inputs['Scale'].default_value = displacement_scale
                links.new(img_node.outputs['Color'], displacement_node.inputs['Height'])
                links.new(displacement_node.outputs['Displacement'], material_output.inputs['Displacement'])
            else:
                target_input = principled_bsdf.inputs[map_info['input']]
                output_link = img_node.outputs['Color']

                if map_info.get('invert'):
                    invert_node = nodes.new(type='ShaderNodeInvert')
                    invert_node.location = (principled_bsdf.location.x - 200, principled_bsdf.location.y - 300)
                    links.new(output_link, invert_node.inputs['Color'])
                    output_link = invert_node.outputs['Color']
                
                links.new(output_link, target_input)

    # Link Principled BSDF to Material Output
    links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])

    # --- Finalize ---
    # Optionally, set object's material displace method for true displacement in Cycles
    # Requires Cycles and Experimental feature set for Adaptive Subdivision
    if 'displacement_map' in [info for map_key, info in map_types.items() if map_key in file_name.upper()]: # Check if any disp map was added
        if mat.cycles.displacement_method == 'BUMP': # Default is BUMP, change to DISPLACE
            mat.cycles.displacement_method = 'DISPLACE_AND_BUMP' # As recommended in the video for realism
            print(f"Set material '{material_name}' displacement method to 'Displace and Bump'.")
            print("Note: For true displacement, ensure Cycles is enabled and 'Experimental' feature set is active in Render Properties, and add a Subdivision Surface modifier to the object with 'Adaptive Subdivision' checked.")

    return f"Created '{object_name}' at {location} with material '{material_name}' and PBR textures."

