def create_pbr_rock_wall(
    scene_name: str = "Scene",
    object_name: str = "PBR_Rock_Wall",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    texture_folder_path: str = "",  # Path to the folder containing PBR textures
    displacement_scale: float = 0.15,
    subdivision_levels: int = 5,
    sun_strength: float = 5.0,
    sun_rotation_euler: tuple = (0.7, -0.7, 0.5), # (X, Y, Z) in radians
    **kwargs,
) -> str:
    """
    Create a PBR rock wall plane with displacement in the active Blender scene.

    This skill requires a folder with PBR textures named using common conventions
    (e.g., _Albedo, _Rough, _Nor_GL, _Disp).

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created plane object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the plane.
        texture_folder_path: Absolute path to the directory containing PBR textures.
                             Example: "/home/user/textures/rock_wall_10/"
                             Expected files: *_Albedo.jpg, *_Rough.jpg, *_Nor_GL.jpg, *_Disp.jpg
        displacement_scale: Strength of the displacement effect.
        subdivision_levels: Number of subdivision levels for the Subdivision Surface modifier.
        sun_strength: Energy of the Sun lamp.
        sun_rotation_euler: (X, Y, Z) Euler rotation for the Sun lamp in radians.
        **kwargs: Additional overrides (not used in this version).

    Returns:
        Status string, e.g., "Created 'PBR_Rock_Wall' at (0, 0, 0) with 2 objects"
    """
    import bpy
    import os
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 1. Create Base Geometry (Plane) ---
    bpy.ops.mesh.primitive_plane_add(
        size=2,
        enter_editmode=False,
        align='WORLD',
        location=location
    )
    plane_obj = bpy.context.object
    plane_obj.name = object_name
    plane_obj.scale = (scale, scale, scale)

    # --- 2. Add Subdivision Surface Modifier ---
    subdiv_mod = plane_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv_mod.levels = subdivision_levels
    subdiv_mod.render_levels = subdivision_levels
    bpy.ops.object.shade_smooth() # Smooth shading for better displacement visuals

    # --- 3. Create Material and Node Setup ---
    mat_name = f"{object_name}_Material"
    material = bpy.data.materials.new(name=mat_name)
    material.use_nodes = True
    plane_obj.data.materials.append(material)

    node_tree = material.node_tree
    # Clear default nodes
    for node in node_tree.nodes:
        node_tree.nodes.remove(node)

    # Create Principled BSDF and Material Output nodes
    principled_bsdf = node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
    material_output = node_tree.nodes.new(type='ShaderNodeOutputMaterial')
    principled_bsdf.location = (-300, 0)
    material_output.location = (200, 0)

    # Create Texture Coordinate and Mapping nodes
    tex_coord = node_tree.nodes.new(type='ShaderNodeTexCoord')
    mapping = node_tree.nodes.new(type='ShaderNodeMapping')
    tex_coord.location = (-1000, 0)
    mapping.location = (-750, 0)

    node_tree.links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])

    # Helper function to load texture and connect
    def load_and_connect_texture(suffix, input_socket, color_space='sRGB', is_normal_map=False, is_displacement_map=False):
        if not texture_folder_path:
            print(f"Warning: No texture folder path provided for {suffix}. Skipping texture.")
            return

        # Find file in folder by suffix (case-insensitive and flexible for naming)
        found_file = None
        base_filename = os.path.basename(texture_folder_path.rstrip(os.sep)).replace("_10", "") # Adjust for 'Rock_Wall_10' pattern
        
        # Define common PBR naming variants for robust matching
        variants = [
            f"{base_filename}{suffix}",
            f"{base_filename.replace('_4K', '')}{suffix}",
            f"Rock_Wall_10_{suffix}", # Specific for this tutorial's texture name
            f"rock_wall_10_{suffix.lower()}",
            f"{object_name}_{suffix}",
            f"{object_name}_{suffix.lower()}"
        ]
        
        # List files in the texture folder to find a match
        files_in_dir = os.listdir(texture_folder_path)
        for filename in files_in_dir:
            file_lower = filename.lower()
            if any(v.lower().strip('_') in file_lower for v in variants): # Check for variants in filename
                found_file = filename
                break

        if not found_file:
            print(f"Warning: No file found for suffix '{suffix}' in {texture_folder_path}. Skipping texture.")
            return

        filepath = os.path.join(texture_folder_path, found_file)
        if not os.path.exists(filepath):
            print(f"Error: Texture file not found at {filepath}. Skipping texture.")
            return

        img_node = node_tree.nodes.new(type='ShaderNodeTexImage')
        img_node.image = bpy.data.images.load(filepath)
        img_node.image.colorspace_settings.name = color_space
        img_node.location = (principled_bsdf.location.x - 400, input_socket.node.location.y - 100 * (len(node_tree.nodes) % 5))
        node_tree.links.new(mapping.outputs['Vector'], img_node.inputs['Vector'])

        if is_normal_map:
            normal_map_node = node_tree.nodes.new(type='ShaderNodeNormalMap')
            normal_map_node.location = (principled_bsdf.location.x - 200, input_socket.node.location.y - 100)
            node_tree.links.new(img_node.outputs['Color'], normal_map_node.inputs['Color'])
            node_tree.links.new(normal_map_node.outputs['Normal'], input_socket)
        elif is_displacement_map:
            displacement_node = node_tree.nodes.new(type='ShaderNodeDisplacement')
            displacement_node.inputs['Midlevel'].default_value = 0.5
            displacement_node.inputs['Scale'].default_value = displacement_scale
            displacement_node.location = (material_output.location.x - 300, material_output.location.y - 200)
            node_tree.links.new(img_node.outputs['Color'], displacement_node.inputs['Height'])
            node_tree.links.new(displacement_node.outputs['Displacement'], material_output.inputs['Displacement'])
        else:
            node_tree.links.new(img_node.outputs['Color'], input_socket)

    # Connect Principled BSDF to Material Output
    node_tree.links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])

    # Load and connect PBR textures
    # Common PBR texture suffixes used by Node Wrangler's principled setup (Shift+Ctrl+T)
    # The actual texture names often include '4K', '10', 'GL' etc.
    load_and_connect_texture("Albedo", principled_bsdf.inputs['Base Color'], 'sRGB')
    load_and_connect_texture("Rough", principled_bsdf.inputs['Roughness'], 'Non-Color')
    load_and_connect_texture("Nor_GL", principled_bsdf.inputs['Normal'], 'Non-Color', is_normal_map=True) # or just "Normal"
    load_and_connect_texture("Disp", None, 'Non-Color', is_displacement_map=True) # or "Height"

    # --- 4. Configure Material for Displacement ---
    material.cycles.displacement_method = 'DISPLACEMENT' # Or 'DISPLACEMENT_AND_BUMP' as per video
    # Note: 'DISPLACEMENT' implies DISPLACEMENT_AND_BUMP in Blender 4.0+ for Cycles.
    # For older versions, 'DISPLACEMENT_AND_BUMP' might be explicit.

    # --- 5. Add Sun Lamp for Clear Lighting ---
    light_name = f"{object_name}_Sun"
    # Delete existing sun if it has the same name prefix to avoid duplicates
    if bpy.data.objects.get(light_name):
        bpy.data.objects.remove(bpy.data.objects[light_name], do_unlink=True)

    bpy.ops.object.light_add(type='SUN', location=(0,0,0)) # Location doesn't matter for Sun
    sun_obj = bpy.context.object
    sun_obj.name = light_name
    sun_obj.data.energy = sun_strength
    sun_obj.rotation_euler = sun_rotation_euler

    # --- 6. Set Render Engine to Cycles ---
    scene.render.engine = 'CYCLES'
    # Optional: Set GPU compute if available
    # For Blender 4.0+
    if hasattr(bpy.context.preferences.addons['cycles'].preferences, 'get_devices'):
        cycles_prefs = bpy.context.preferences.addons['cycles'].preferences
        if cycles_prefs.compute_device_type == 'NONE':
            cycles_prefs.compute_device_type = 'CUDA' # or 'OPTIX', 'HIP', 'METAL'
            for device in cycles_prefs.devices:
                if device.type == 'GPU':
                    device.use = True
                else:
                    device.use = False
        
    return f"Created '{object_name}' at {location} with PBR material and Sun light."

