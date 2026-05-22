def create_object(
    scene_name: str = "Scene",
    object_name: str = "SeamlessTexturedObject",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    subdivision_level: int = 3,
    blend_factor: float = 0.15,
    albedo_color: tuple = (0.5, 0.5, 0.5, 1.0),  # RGBA
    metallic_value: float = 0.0,
    roughness_value: float = 0.5,
) -> str:
    """
    Create a custom layered cylinder object with seamless box-projected PBR texturing.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        subdivision_level: Levels for the Subdivision Surface modifier.
        blend_factor: Blend amount for box projection to smooth seams (0.0-1.0).
        albedo_color: (R, G, B, A) base color for the placeholder image in 0-1 range.
        metallic_value: Metallic value for the placeholder image (0.0-1.0).
        roughness_value: Roughness value for the placeholder image (0.0-1.0).

    Returns:
        Status string, e.g., "Created 'SeamlessTexturedObject' at (0, 0, 0)"
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === GEOMETRY CREATION ===
    # 1. Add base cylinder
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=64,  # High resolution for smoother subsurf output
        radius=1.5 * scale,
        depth=0.5 * scale,
        enter_editmode=False,
        align='WORLD',
        location=location
    )
    obj = bpy.context.active_object
    obj.name = object_name
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Edit mode operations for the complex tiered shape and side protrusion
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.verts.ensure_lookup_table()

    # Find top face (face with normal pointing in +Z)
    top_face = None
    for face in bm.faces:
        if face.normal.z > 0.99:
            top_face = face
            break
    
    if top_face:
        # Create tiered structure (inset then extrude up repeatedly)
        current_face = top_face
        extrusions = [
            (0.15 * scale, 0.2 * scale), # First tier: Inset, Extrude Up
            (0.1 * scale, 0.2 * scale)   # Second tier (central pillar): Inset, Extrude Up
        ]

        for i, (inset_amount, extrude_amount) in enumerate(extrusions):
            # Inset the current top face
            bmesh.ops.inset_region(bm, faces=[current_face], thickness=inset_amount, depth=0)
            current_face = [f for f in bm.faces if f.is_valid and f.normal.z > 0.99 and f.calc_center_median().length < (current_face.calc_center_median().length - inset_amount)][0] # Get new inner face

            # Extrude Up
            extrude_ret = bmesh.ops.extrude_discrete_faces(bm, faces=[current_face])
            current_face = extrude_ret['faces'][0] # Get the newly extruded top face
            bmesh.ops.translate(bm, verts=current_face.verts, vec=(0, 0, extrude_amount))

        # Final inset and extrude down for the central hole
        bmesh.ops.inset_region(bm, faces=[current_face], thickness=0.08 * scale, depth=0)
        current_face_hole = [f for f in bm.faces if f.is_valid and f.normal.z > 0.99 and f.calc_center_median().length < (current_face.calc_center_median().length - 0.08 * scale)][0] # Get new inner face
        
        extrude_ret_hole = bmesh.ops.extrude_discrete_faces(bm, faces=[current_face_hole])
        extruded_hole_face = extrude_ret_hole['faces'][0]
        bmesh.ops.translate(bm, verts=extruded_hole_face.verts, vec=(0, 0, -0.4 * scale)) # Extrude downwards

    # Add a side protrusion (handle/spout) to demonstrate dynamic mapping
    side_face_to_extrude = None
    mid_z = location[2] + 0.25 * scale # Approximate Z-level of the middle tier
    for face in bm.faces:
        center = face.calc_center_median()
        # Look for a face on the side (normal.z close to 0), at a specific Z height, and on one side (e.g., +X)
        if abs(face.normal.z) < 0.1 and abs(center.z - mid_z) < 0.1 * scale and center.x > 0.5 * scale:
            side_face_to_extrude = face
            break
            
    if side_face_to_extrude:
        # Inset the side face slightly
        bmesh.ops.inset_region(bm, faces=[side_face_to_extrude], thickness=0.08 * scale, depth=0)
        inner_side_face = [f for f in bm.faces if f.is_valid and f.normal == side_face_to_extrude.normal and f.calc_center_median().length > 1.0 * scale][0]

        # Extrude outwards
        extrude_side_ret = bmesh.ops.extrude_discrete_faces(bm, faces=[inner_side_face])
        extruded_side_face = extrude_side_ret['faces'][0]
        bmesh.ops.translate(bm, verts=extruded_side_face.verts, vec=extruded_side_face.normal * 0.7 * scale) # Extrude along normal

        # Optional: Inset/extrude the end for a slightly more complex shape on the protrusion
        bmesh.ops.inset_region(bm, faces=[extruded_side_face], thickness=0.05 * scale, depth=0)
        inner_end_face = [f for f in bm.faces if f.is_valid and f.normal == extruded_side_face.normal and f.calc_center_median().length > extruded_side_face.calc_center_median().length + 0.05*scale][0]
        
        extrude_end_ret = bmesh.ops.extrude_discrete_faces(bm, faces=[inner_end_face])
        final_end_face = extrude_end_ret['faces'][0]
        bmesh.ops.translate(bm, verts=final_end_face.verts, vec=final_end_face.normal * 0.1 * scale)

    bmesh.update_edit_mesh(obj.data)
    bmesh.free(bm)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Add Subdivision Surface Modifier for smoothing
    subsurf_mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf_mod.levels = subdivision_level
    subsurf_mod.render_levels = subdivision_level

    # Shade Smooth for better visual appearance
    bpy.ops.object.shade_smooth()

    # === MATERIAL CREATION (PBR with Box Projection) ===
    mat = bpy.data.materials.new(name=f"{object_name}_Material")
    mat.use_nodes = True
    obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes except Principled BSDF and Material Output
    for node in nodes:
        if node.name not in ["Principled BSDF", "Material Output"]:
            nodes.remove(node)

    principled_bsdf = nodes["Principled BSDF"]
    material_output = nodes["Material Output"]

    # --- Helper function to create placeholder images ---
    def create_placeholder_image(img_name, width=1024, height=1024, color=(0.5, 0.5, 0.5, 1.0)):
        # Check if image already exists
        if img_name in bpy.data.images:
            return bpy.data.images[img_name]

        img = bpy.data.images.new(img_name, width=width, height=height, alpha=True)
        # Fill image with color
        pixels = [c for c in color for _ in range(width * height)]
        img.pixels = pixels
        return img

    # --- Texture Coordinate and Mapping Nodes ---
    tex_coord = nodes.new(type='TEX_COORD')
    mapping = nodes.new(type='MAPPING')
    mapping.vector_type = 'POINT' # Explicitly set vector type

    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # --- PBR Image Textures (Placeholders) ---
    # Albedo (Base Color)
    img_albedo_data = create_placeholder_image(f"{object_name}_Albedo_PH", color=albedo_color)
    node_albedo = nodes.new(type='TEX_IMAGE')
    node_albedo.image = img_albedo_data
    node_albedo.label = "Albedo"
    node_albedo.image.colorspace_settings.name = 'sRGB' # Standard for color textures
    node_albedo.projection = 'BOX'
    node_albedo.blend = blend_factor
    links.new(mapping.outputs['Vector'], node_albedo.inputs['Vector'])
    links.new(node_albedo.outputs['Color'], principled_bsdf.inputs['Base Color'])

    # Normal Map
    img_normal_data = create_placeholder_image(f"{object_name}_Normal_PH", color=(0.5, 0.5, 1.0, 1.0)) # Flat blue normal map
    node_normal_tex = nodes.new(type='TEX_IMAGE')
    node_normal_tex.image = img_normal_data
    node_normal_tex.label = "Normal Map Texture"
    node_normal_tex.image.colorspace_settings.name = 'Non-Color' # Important for normal maps
    node_normal_tex.projection = 'BOX'
    node_normal_tex.blend = blend_factor
    links.new(mapping.outputs['Vector'], node_normal_tex.inputs['Vector'])

    node_normal_map = nodes.new(type='SHADER_NODE_NORMAL_MAP')
    links.new(node_normal_tex.outputs['Color'], node_normal_map.inputs['Color'])

    # Roughness
    img_roughness_data = create_placeholder_image(f"{object_name}_Roughness_PH", color=(roughness_value, roughness_value, roughness_value, 1.0))
    node_roughness = nodes.new(type='TEX_IMAGE')
    node_roughness.image = img_roughness_data
    node_roughness.label = "Roughness"
    node_roughness.image.colorspace_settings.name = 'Non-Color' # Important for data textures
    node_roughness.projection = 'BOX'
    node_roughness.blend = blend_factor
    links.new(mapping.outputs['Vector'], node_roughness.inputs['Vector'])
    links.new(node_roughness.outputs['Color'], principled_bsdf.inputs['Roughness'])
    
    # Metallic
    img_metallic_data = create_placeholder_image(f"{object_name}_Metallic_PH", color=(metallic_value, metallic_value, metallic_value, 1.0))
    node_metallic = nodes.new(type='TEX_IMAGE')
    node_metallic.image = img_metallic_data
    node_metallic.label = "Metallic"
    node_metallic.image.colorspace_settings.name = 'Non-Color' # Important for data textures
    node_metallic.projection = 'BOX'
    node_metallic.blend = blend_factor
    links.new(mapping.outputs['Vector'], node_metallic.inputs['Vector'])
    links.new(node_metallic.outputs['Color'], principled_bsdf.inputs['Metallic'])

    # Height (for Bump mapping)
    img_height_data = create_placeholder_image(f"{object_name}_Height_PH", color=(0.5, 0.5, 0.5, 1.0)) # Mid-gray for neutral height
    node_height = nodes.new(type='TEX_IMAGE')
    node_height.image = img_height_data
    node_height.label = "Height"
    node_height.image.colorspace_settings.name = 'Non-Color'
    node_height.projection = 'BOX'
    node_height.blend = blend_factor
    links.new(mapping.outputs['Vector'], node_height.inputs['Vector'])
    
    node_bump = nodes.new(type='SHADER_NODE_BUMP')
    node_bump.inputs['Strength'].default_value = 0.5 # Default bump strength
    node_bump.inputs['Distance'].default_value = 0.05
    links.new(node_height.outputs['Color'], node_bump.inputs['Height'])
    
    # Combine Normal Map and Bump: Normal Map feeds into Bump's Normal input
    links.new(node_normal_map.outputs['Normal'], node_bump.inputs['Normal'])
    # Final Normal output to Principled BSDF
    links.new(node_bump.outputs['Normal'], principled_bsdf.inputs['Normal'])

    # --- Node Positioning for clarity ---
    tex_coord.location = Vector([-800, 0])
    mapping.location = Vector([-600, 0])
    node_albedo.location = Vector([-300, 300])
    node_normal_tex.location = Vector([-300, 100])
    node_normal_map.location = Vector([-100, 100])
    node_roughness.location = Vector([-300, -100])
    node_metallic.location = Vector([-300, -300])
    node_height.location = Vector([-300, -500])
    node_bump.location = Vector([-100, -500])
    principled_bsdf.location = Vector([100, 0])
    material_output.location = Vector([400, 0])

    return f"Created '{object_name}' with seamless PBR texturing at {location}"

