def create_adaptive_textured_object(
    scene_name: str = "Scene",
    object_name: str = "WornMetalObject",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    base_color_rgba: tuple = (0.2, 0.7, 0.6, 1.0), # Example color, PBR textures will largely override
    blend_factor: float = 0.1,
    subdivision_level: int = 3, # Viewport and Render levels
    bevel_segments: int = 2,
    bevel_width: float = 0.02,
    texture_paths: dict = None, # Dictionary for PBR texture file paths
) -> str:
    """
    Creates a complex cylindrical object with adaptive box-projected PBR textures
    that automatically adjust to mesh edits without explicit UV unwrapping.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the object.
        base_color_rgba: (R, G, B, A) base color for the Principled BSDF.
                         Note: PBR textures will largely override this for color if loaded.
        blend_factor: Amount of blend between box projections (0.0 to 1.0).
        subdivision_level: Levels for the Subdivision Surface modifier.
        bevel_segments: Segments for the Bevel modifier to sharpen edges.
        bevel_width: Width of the Bevel modifier.
        texture_paths: A dictionary containing paths to PBR texture images.
                       Keys should be "albedo", "normal", "roughness", "metallic".
                       Example: {"albedo": "C:/textures/worn_albedo.png", ...}
                       If not provided or paths are invalid, the material might not fully
                       reflect the PBR texture from the tutorial.
    Returns:
        Status string describing the creation.
    """
    import bpy
    from mathutils import Vector
    import math

    # Ensure Node Wrangler is enabled for expected behavior (e.g., blend_distance on Image Texture)
    # This is usually done once in preferences, but checking here ensures compatibility.
    # Note: `blend_distance` exists without Node Wrangler, but it's often associated.
    # if 'node_wrangler' not in bpy.context.preferences.addons:
    #     bpy.ops.preferences.addon_enable(module='node_wrangler')

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 1. Create Base Geometry ---
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.5 * scale,
        depth=0.5 * scale,
        vertices=32,
        location=(0,0,0) # Create at origin, then move later
    )
    obj = bpy.context.active_object
    obj.name = object_name

    # Apply initial Z-scaling as shown in video (making it thin)
    obj.scale = (1.0, 1.0, 0.262) # Relative to the initial primitive's depth
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # --- 2. Edit Mesh to Create Shape (mimicking video's steps using bpy.ops) ---
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="FACE")

    # Select initial top face
    bpy.ops.mesh.select_all(action='DESELECT')
    # Use bmesh for more reliable face selection within script context
    bm = bmesh.from_edit_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    initial_top_face = max(bm.faces, key=lambda f: f.calc_center_median().z)
    initial_top_face.select = True
    bmesh.update_edit_mesh(obj.data) # Update mesh for ops to see selection

    # Step 1: Inset top face
    bpy.ops.mesh.inset(thickness=0.15 * scale, depth=0)
    # Step 2: Extrude up (first tier)
    bpy.ops.mesh.extrude_region_and_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 0.2 * scale)})

    # Step 3: Inset new top face (automatically selected after extrude)
    bpy.ops.mesh.inset(thickness=0.15 * scale, depth=0)
    # Step 4: Extrude down for hole
    bpy.ops.mesh.extrude_region_and_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -0.2 * scale)})

    # Select initial bottom face
    bpy.ops.mesh.select_all(action='DESELECT')
    bm = bmesh.from_edit_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    initial_bottom_face = min(bm.faces, key=lambda f: f.calc_center_median().z)
    initial_bottom_face.select = True
    bmesh.update_edit_mesh(obj.data)

    # Step 5: Extrude down for base flange
    bpy.ops.mesh.extrude_region_and_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -0.1 * scale)})
    # Step 6: Inset the new bottom face (for outer edge)
    bpy.ops.mesh.inset(thickness=0.05 * scale, depth=0)
    # Step 7: Extrude up slightly for outer edge
    bpy.ops.mesh.extrude_region_and_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 0.05 * scale)})

    # Create a side protrusion/handle (similar to video's final edit)
    bpy.ops.mesh.select_all(action='DESELECT')
    bm = bmesh.from_edit_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    
    side_face_index = -1
    # Find a polygon on the side, near the middle height of the main body (after initial extrusions)
    current_dimensions = obj.dimensions
    target_z_height = current_dimensions.z / 4 # Roughly middle of the main body after operations

    # Iterate through faces to find a suitable side face
    for i, face in enumerate(bm.faces):
        # Check if the face is mostly vertical (normal.z is small)
        # and its center is roughly around the target Z height.
        if abs(face.normal.z) < 0.1 and abs(face.calc_center_median().z - target_z_height) < 0.1 * scale:
            # Pick a face oriented towards +Y for consistent protrusion
            if face.normal.y > 0.8: 
                side_face_index = i
                break
    
    if side_face_index != -1:
        bm.faces[side_face_index].select = True
        bmesh.update_edit_mesh(obj.data) # Update mesh for ops to see selection
        
        # Extrude out
        bpy.ops.mesh.extrude_region_and_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0.3 * scale, 0)})
        # Scale down the end face of the extrusion
        bpy.ops.transform.resize(value=(1.0, 0.5, 0.5), orient_type='GLOBAL', orient_axis_ortho='Y') # Scale in X and Z
        # Extrude again
        bpy.ops.mesh.extrude_region_and_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0.3 * scale, 0)})
        
    else:
        print("Warning: Could not reliably select a side face for protrusion. Skipping this detail.")
    
    # Clean up selection and exit edit mode
    bpy.ops.mesh.select_all(action='DESELECT')
    bmesh.update_edit_mesh(obj.data) # Final update from bmesh
    bpy.ops.object.mode_set(mode='OBJECT')

    # --- 3. Add Modifiers ---
    # Subdivision Surface
    subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.levels = subdivision_level
    subdiv.render_levels = subdivision_level

    # Bevel (to sharpen edges)
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = bevel_width * scale
    bevel.segments = bevel_segments
    bevel.limit_method = 'ANGLE' # Limit to edges sharper than a certain angle
    bevel.angle_limit = math.radians(30) # Default angle for bevel
    bevel.loop_slide = True # Helps maintain better shape with subdivision

    bpy.ops.object.shade_smooth() # Apply smooth shading

    # --- 4. Create Material and Setup Node Tree for Box Projection ---
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    obj.data.materials.append(mat)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes except Principled BSDF and Material Output
    for node in nodes:
        if node.type != 'BSDF_PRINCIPLED' and node.type != 'OUTPUT_MATERIAL':
            nodes.remove(node)

    principled_bsdf = nodes.get("Principled BSDF") or nodes.new(type='ShaderNodeBsdfPrincipled')
    material_output = nodes.get("Material Output") or nodes.new(type='ShaderNodeOutputMaterial')

    # Ensure Principled BSDF is linked to Material Output
    if not principled_bsdf.outputs['BSDF'].is_linked:
        links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])

    # Set base color (will be overridden by texture if present)
    principled_bsdf.inputs['Base Color'].default_value = base_color_rgba

    # Texture Coordinate and Mapping nodes
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    mapping = nodes.new(type='ShaderNodeMapping')
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # Default texture paths for example (user should replace with actual paths)
    default_texture_paths = {
        "albedo": "C:/Your/Path/To/worn_rusted_painted_albedo.png", # Base Color
        "normal": "C:/Your/Path/To/worn_rusted_painted_normal_ogl.png", # Normal Map
        "roughness": "C:/Your/Path/To/worn_rusted_painted_roughness.png", # Roughness Map
        "metallic": "C:/Your/Path/To/worn_rusted_painted_metallic.png", # Metallic Map
        # "height": "C:/Your/Path/To/worn_rusted_painted_height.png" # Optional for displacement
    }
    # If custom paths are not provided, use the defaults.
    if texture_paths is None:
        texture_paths = default_texture_paths

    pbr_map_details = {
        "albedo": ("Base Color", None),
        "normal": ("Normal", 'ShaderNodeNormalMap'),
        "roughness": ("Roughness", None),
        "metallic": ("Metallic", None),
    }

    # Load and connect PBR textures
    for map_type, (principled_input, extra_node_type) in pbr_map_details.items():
        tex_path = texture_paths.get(map_type)
        if tex_path and bpy.path.abspath(tex_path): # Check if path exists and is valid
            try:
                img = bpy.data.images.load(tex_path, check_existing=True)
                tex_node = nodes.new(type='ShaderNodeTexImage')
                tex_node.image = img
                tex_node.projection = 'BOX'
                tex_node.interpolation = 'Cubic'
                tex_node.blend_distance = blend_factor

                # Set color space (Non-Color for non-color data)
                if map_type in ["normal", "roughness", "metallic"]:
                    tex_node.image.colorspace_settings.name = 'Non-Color'
                else: # Albedo
                    tex_node.image.colorspace_settings.name = 'sRGB'

                links.new(mapping.outputs['Vector'], tex_node.inputs['Vector'])

                if extra_node_type == 'ShaderNodeNormalMap':
                    normal_map_node = nodes.new(type='ShaderNodeNormalMap')
                    links.new(tex_node.outputs['Color'], normal_map_node.inputs['Color'])
                    links.new(normal_map_node.outputs['Normal'], principled_bsdf.inputs[principled_input])
                else:
                    links.new(tex_node.outputs['Color'], principled_bsdf.inputs[principled_input])
            except RuntimeError as e:
                print(f"Warning: Could not load texture for {map_type} from '{tex_path}': {e}")
        else:
            print(f"Info: No valid texture path provided for {map_type} or file not found. Using default or principled fallback.")

    # Position nodes for better readability
    tex_coord.location = (-800, 0)
    mapping.location = (-600, 0)
    principled_bsdf.location = (0, 0)
    material_output.location = (200, 0)

    y_offset_tex = 250
    for node in nodes:
        if node.type == 'TEX_IMAGE':
            node.location = (-300, y_offset_tex)
            y_offset_tex -= 150
        elif node.type == 'NORMAL_MAP':
            node.location = (-100, -200)

    # --- 5. Finalize ---
    obj.location = Vector(location)

    return f"Created '{object_name}' with adaptive box projection material at {location}"

