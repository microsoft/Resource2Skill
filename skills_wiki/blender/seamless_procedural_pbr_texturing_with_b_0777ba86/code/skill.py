def create_box_projected_pbr_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjectedPBR_Object",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1), # Default fallback color for Base Color
    albedo_path: str = None,
    roughness_path: str = None,
    metallic_path: str = None,
    normal_path: str = None,
    height_path: str = None,
    subdivision_level: int = 3,
    blend_factor: float = 0.1,
    bevel_segments: int = 2,
    bevel_width: float = 0.05,
    add_arm: bool = False, # Optional parameter to add the side extrusion
    **kwargs,
) -> str:
    """
    Creates a multi-tiered cylindrical object with a seamless PBR material using box projection.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the object.
        material_color: (R, G, B) base color for the Principled BSDF (0-1 range).
        albedo_path: File path to the Albedo/Base Color texture.
        roughness_path: File path to the Roughness texture.
        metallic_path: File path to the Metallic texture.
        normal_path: File path to the Normal texture.
        height_path: File path to the Height/Displacement texture.
        subdivision_level: Levels for the Subdivision Surface modifier.
        blend_factor: Amount of blending between box projections (0-1 range).
        bevel_segments: Number of segments for the Bevel modifier.
        bevel_width: Width of the Bevel modifier.
        add_arm: If True, adds an extruded "arm" feature to the side of the object.
        **kwargs: Additional overrides for future extensions.

    Returns:
        Status string, e.g., "Created 'PBR_Demo_Object' at (0, 0, 0) with Box Projected PBR Material"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Geometry Creation ---
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=1.0 * scale,
        depth=0.5 * scale,
        location=location,
        enter_editmode=False,
        align='WORLD',
    )
    obj = bpy.context.active_object
    obj.name = object_name

    # Apply initial scale for correct modifier behavior and projection
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj.data)

    # Get initial top face
    top_face = None
    for face in bm.faces:
        if face.normal.z > 0.9:  # Assuming cylinder is upright
            top_face = face
            break
    
    if top_face:
        # Extrusions and Insets for tiered shape
        top_face.select = True
        bmesh.update_edit_mesh(obj.data) # Update selection state for ops

        # Tier 1 (wider base)
        bpy.ops.mesh.inset(thickness=0.3 * scale, depth=0.0)
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value":(0, 0, 0.4*scale), "orient_type":'NORMAL', "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True)}
        )
        # Tier 2 (middle section)
        bpy.ops.mesh.inset(thickness=0.2 * scale, depth=0.0)
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value":(0, 0, 0.3*scale), "orient_type":'NORMAL', "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True)}
        )
        # Top piece (smallest cylinder)
        bpy.ops.mesh.inset(thickness=0.1 * scale, depth=0.0)
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value":(0, 0, 0.2*scale), "orient_type":'NORMAL', "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True)}
        )
    
    # Optional arm extrusion (as shown at the end of the video)
    if add_arm:
        bm.faces.ensure_lookup_table()
        # Find a side face on the second tier for extrusion (e.g., closest to +X, Y=0)
        side_face_target_z = location[2] + 0.5 * scale + 0.4 * scale / 2 # Approx middle of second tier
        closest_face = None
        min_dist_to_center = float('inf')

        for face in bm.faces:
            if abs(face.normal.x) > 0.9 or abs(face.normal.y) > 0.9: # Check for primary side normals
                face_center = obj.matrix_world @ face.calc_center_median()
                dist_z = abs(face_center.z - side_face_target_z)
                dist_xy_to_center = (face_center.x**2 + face_center.y**2)**0.5 # Distance from global Z-axis
                
                # Prioritize faces around the desired Z height and further out
                if dist_z < 0.1 * scale and dist_xy_to_center > 0.5 * scale and dist_xy_to_center < min_dist_to_center:
                    min_dist_to_center = dist_xy_to_center
                    closest_face = face
        
        if closest_face:
            bm.select_flush(False) # Deselect all
            closest_face.select = True
            bmesh.update_edit_mesh(obj.data)
            
            normal = closest_face.normal.copy()
            
            # Extrude outwards
            bpy.ops.mesh.extrude_region_move(
                TRANSFORM_OT_translate={"value": (normal.x * 0.5 * scale, normal.y * 0.5 * scale, normal.z * 0.5 * scale), "orient_type":'NORMAL', "orient_matrix_type":'NORMAL', "constraint_axis": (normal.x != 0, normal.y != 0, normal.z != 0)}
            )
            # Resize (squash) the newly extruded part slightly
            bpy.ops.transform.resize(value=(1.0, 0.5, 0.5), orient_type='NORMAL')
            # Extrude again
            bpy.ops.mesh.extrude_region_move(
                TRANSFORM_OT_translate={"value": (normal.x * 0.5 * scale, normal.y * 0.5 * scale, normal.z * 0.5 * scale), "orient_type":'NORMAL', "orient_matrix_type":'NORMAL', "constraint_axis": (normal.x != 0, normal.y != 0, normal.z != 0)}
            )
    
    bpy.ops.object.mode_set(mode='OBJECT')

    # --- Modifiers ---
    # Bevel modifier to sharpen edges
    bevel_mod = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel_mod.segments = bevel_segments
    bevel_mod.width = bevel_width * scale
    bevel_mod.limit_method = 'ANGLE' # Limit by angle to only affect sharp edges

    # Subdivision Surface modifier for smoothing
    subdiv_mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv_mod.levels = subdivision_level
    subdiv_mod.render_levels = subdivision_level

    # Shade Smooth
    bpy.ops.object.shade_smooth()

    # --- Material Creation and Setup ---
    mat = bpy.data.materials.new(name=f"{object_name}_Material")
    obj.data.materials.append(mat)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Create Principled BSDF node
    principled_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled_bsdf.location = (600, 0)
    principled_bsdf.inputs["Base Color"].default_value = material_color + (1,) # Add alpha

    # Create Material Output node
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    material_output.location = (800, 0)
    links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])

    # Create Texture Coordinate and Mapping nodes
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-400, 0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # Helper function to add image texture nodes and connect them
    def _add_image_texture(name, file_path, color_space, node_location, connect_to_input, blend_factor, is_normal_map=False):
        img_node = nodes.new(type='ShaderNodeTexImage')
        img_node.name = name
        img_node.label = name
        img_node.location = node_location

        img = None
        if file_path:
            abs_file_path = bpy.path.abspath(file_path)
            if abs_file_path:
                try:
                    img = bpy.data.images.load(abs_file_path)
                    img_node.image = img
                except RuntimeError as e:
                    print(f"Warning: Could not load image '{abs_file_path}' for '{name}': {e}. Node will be empty.")
            else:
                print(f"Warning: Provided file path '{file_path}' for '{name}' could not be resolved. Node will be empty.")

        if img_node.image: # Only set color space if image was loaded
            img_node.image.colorspace_settings.name = color_space
        
        img_node.projection = 'BOX' # Key for box projection
        img_node.interpolation = 'Cubic' # Better quality
        img_node.extension = 'REPEAT' # Repeat texture if necessary
        img_node.blend = blend_factor # Key for blend
        img_node.inputs['Vector'].default_value = Vector((0,0,0)) # Ensure default value is set even without link

        links.new(mapping.outputs['Vector'], img_node.inputs['Vector'])
        
        if is_normal_map:
            normal_map_node = nodes.new(type='ShaderNodeNormalMap')
            normal_map_node.location = (node_location[0] + 150, node_location[1] - 50)
            if img_node.image:
                links.new(img_node.outputs['Color'], normal_map_node.inputs['Color'])
            links.new(normal_map_node.outputs['Normal'], principled_bsdf.inputs['Normal'])
        else:
            if img_node.image and connect_to_input in principled_bsdf.inputs:
                links.new(img_node.outputs['Color'], principled_bsdf.inputs[connect_to_input])
        return img_node

    # Add PBR textures
    _add_image_texture("Albedo", albedo_path, 'sRGB', (-200, 300), 'Base Color', blend_factor)
    _add_image_texture("Roughness", roughness_path, 'Non-Color', (-200, 150), 'Roughness', blend_factor)
    _add_image_texture("Metallic", metallic_path, 'Non-Color', (-200, 0), 'Metallic', blend_factor)
    _add_image_texture("Normal", normal_path, 'Non-Color', (-200, -150), 'Normal', blend_factor, is_normal_map=True)

    # Displacement setup (if height map is provided)
    if height_path:
        height_img_node = nodes.new(type='ShaderNodeTexImage')
        height_img_node.name = "Height"
        height_img_node.label = "Height"
        height_img_node.location = (-200, -300)
        
        img = None
        if height_path:
            abs_file_path = bpy.path.abspath(height_path)
            if abs_file_path:
                try:
                    img = bpy.data.images.load(abs_file_path)
                    height_img_node.image = img
                except RuntimeError as e:
                    print(f"Warning: Could not load image '{abs_file_path}' for 'Height': {e}. Node will be empty.")
            else:
                print(f"Warning: Provided file path '{height_path}' for 'Height' could not be resolved. Node will be empty.")

        if height_img_node.image:
            height_img_node.image.colorspace_settings.name = 'Non-Color'
        
        height_img_node.projection = 'BOX'
        height_img_node.interpolation = 'Cubic'
        height_img_node.extension = 'REPEAT'
        height_img_node.blend = blend_factor
        links.new(mapping.outputs['Vector'], height_img_node.inputs['Vector'])

        displacement_node = nodes.new(type='ShaderNodeDisplacement')
        displacement_node.location = (400, -300)
        displacement_node.inputs['Midlevel'].default_value = 0.5
        displacement_node.inputs['Scale'].default_value = kwargs.get('displacement_scale', 0.05)

        if height_img_node.image:
            links.new(height_img_node.outputs['Color'], displacement_node.inputs['Height'])
        links.new(displacement_node.outputs['Displacement'], material_output.inputs['Displacement'])
        
        # Enable Cycles render engine if not already, for displacement to work fully
        # if scene.render.engine == 'BLENDER_EEVEE':
        #     scene.render.engine = 'CYCLES'
        #     # Ensure adaptive subdivision is enabled for displacement
        #     obj.cycles.use_adaptive_subdivision = True
        #     if 'Subdivision' in obj.modifiers:
        #         obj.modifiers['Subdivision'].subdivision_type = 'CATMULL_CLARK'
        #         obj.modifiers['Subdivision'].render_levels = 6 # or higher for displacement details
        #         obj.modifiers['Subdivision'].use_adaptive_subdivision = True

    return f"Created '{object_name}' at {location} with Subdivision Surface and Box Projected PBR Material"

