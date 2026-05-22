def create_worn_rusted_painted_object(
    scene_name: str = "Scene",
    object_name: str = "SeamlessTexturedObject",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    subdivision_level: int = 3,
    bevel_amount: float = 0.03, # Slightly reduced for subtler bevel
    blend_factor: float = 0.07, # Adjusted blend for initial subtle effect
    **kwargs,
) -> str:
    """
    Create a 3D object with seamless box-projected PBR-like textures using object coordinates and blending,
    demonstrating adaptive texturing without UV unwrapping.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        subdivision_level: Level for the Subdivision Surface modifier.
        bevel_amount: Amount for the Bevel modifier.
        blend_factor: Blend factor for box projection (0.0 to 1.0).
        **kwargs: Additional overrides (not used in this version).

    Returns:
        Status string, e.g., "Created 'SeamlessTexturedObject' at (0, 0, 0)"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 1. Create Base Geometry (Cylinder) ---
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=64,
        radius=1,
        depth=1,
        location=(0,0,0) # Create at origin first, then move after shaping
    )
    obj = bpy.context.object
    obj.name = object_name
    
    # Apply initial scale from parameters before shaping
    obj.scale = (scale, scale, scale * 0.5) # Initial Z scaling from video setup
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # --- 2. Build the tutorial's custom shape using bmesh ---
    bpy.ops.object.editmode_toggle()
    
    bm = bmesh.from_edit_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    
    # Select top face
    top_face = None
    for f in bm.faces:
        if abs(f.normal.z - 1.0) < 0.001: # Check for normal pointing straight up
            top_face = f
            break
    
    if top_face:
        # Inset top face (corresponds to I in video)
        inset_result = bmesh.ops.inset_faces(bm, faces=[top_face], thickness=0.1, depth=0)
        new_face_after_inset = inset_result['faces'][0]

        # Extrude up (corresponds to E in video)
        extruded_geom = bmesh.ops.extrude_face_region(bm, geom=[new_face_after_inset])
        extruded_verts = [v for v in extruded_geom['geom'] if isinstance(v, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, verts=extruded_verts, vec=Vector((0,0,0.2)))
        
        # Get the new top face after extrusion
        current_top_face = [f for f in extruded_geom['geom'] if isinstance(f, bmesh.types.BMFace)][0]
            
        # Inset again (corresponds to I in video)
        inset_result2 = bmesh.ops.inset_faces(bm, faces=[current_top_face], thickness=0.1, depth=0)
        new_face_after_inset2 = inset_result2['faces'][0]

        # Extrude down (corresponds to E in video)
        extruded_geom2 = bmesh.ops.extrude_face_region(bm, geom=[new_face_after_inset2])
        extruded_verts2 = [v for v in extruded_geom2['geom'] if isinstance(v, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, verts=extruded_verts2, vec=Vector((0,0,-0.2)))
    
    # --- Demonstrate dynamic mapping with a side extrusion (like in video) ---
    # Select a side face (e.g., one facing positive X, roughly centered vertically)
    side_face = None
    center_z = obj.dimensions.z / 2 # Midpoint of the object
    for f in bm.faces:
        if abs(f.normal.z) < 0.001 and abs(f.normal.x - 1.0) < 0.001:
            # Check if face is roughly in the middle height to avoid top/bottom rings
            if f.calc_center_median().z > -0.1 and f.calc_center_median().z < 0.1:
                side_face = f
                break

    if side_face:
        # Ensure only this face is selected
        for f in bm.faces: f.select = False
        side_face.select = True
        
        # Inset the side face
        inset_side_result = bmesh.ops.inset_faces(bm, faces=[side_face], thickness=0.08, depth=0)
        new_face_after_side_inset = inset_side_result['faces'][0]
        
        # Extrude the new inset face outwards
        extruded_side_geom = bmesh.ops.extrude_face_region(bm, geom=[new_face_after_side_inset])
        new_extruded_verts = [v for v in extruded_side_geom['geom'] if isinstance(v, bmesh.types.BMVert)]
        
        # Get the normal of the new face to extrude along its local axis
        new_extruded_face = [f for f in extruded_side_geom['geom'] if isinstance(f, bmesh.types.BMFace)][0]
        bmesh.ops.translate(bm, verts=new_extruded_verts, vec=new_extruded_face.normal * 0.2)
        
        # Extrude again
        extruded_side_geom2 = bmesh.ops.extrude_face_region(bm, geom=[new_extruded_face])
        new_extruded_verts2 = [v for v in extruded_side_geom2['geom'] if isinstance(v, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, verts=new_extruded_verts2, vec=new_extruded_face.normal * 0.2)
        
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.editmode_toggle()

    # --- 3. Add Modifiers ---
    subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.levels = subdivision_level
    subdiv.render_levels = subdivision_level

    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = bevel_amount
    bevel.segments = 2
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(60) # Default is good, or 30-60 degrees

    bpy.ops.object.shade_smooth()

    # --- 4. Create Material with Box Projection ---
    mat = bpy.data.materials.new(name=f"{object_name}_Material")
    mat.use_nodes = True
    obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Create Principled BSDF and Material Output nodes
    principled_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled_bsdf.location = (200, 0)
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    material_output.location = (400, 0)
    links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])

    # Create Texture Coordinate and Mapping nodes
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-400, 0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # Create dummy images (cannot include actual files, so we make basic ones)
    # The actual textures would be: albedo, roughness, metallic, normal, height
    
    # Dummy Albedo: Rusty/worn blue-green (as seen in video preview)
    dummy_albedo = bpy.data.images.new(name="dummy_albedo", width=1024, height=1024, alpha=True)
    pixels_albedo = [0.2, 0.5, 0.5, 1.0] * (1024 // 2 * 1024) + [0.4, 0.2, 0.1, 1.0] * (1024 // 2 * 1024) # Basic pattern
    dummy_albedo.pixels = pixels_albedo
    
    # Dummy Roughness: Simple gradient for variation
    dummy_roughness = bpy.data.images.new(name="dummy_roughness", width=1024, height=1024)
    pixels_roughness = [((x / 1024) + (y / 1024)) / 2 * 0.5 + 0.3 for y in range(1024) for x in range(1024)]
    dummy_roughness.pixels = [p for p in pixels_roughness for _ in range(4)]
    
    # Dummy Metallic: Partial metallicity
    dummy_metallic = bpy.data.images.new(name="dummy_metallic", width=1024, height=1024)
    pixels_metallic = [0.2 + (math.sin(x*0.1) + math.cos(y*0.1)) * 0.1 for y in range(1024) for x in range(1024)]
    dummy_metallic.pixels = [p for p in pixels_metallic for _ in range(4)]
    
    # Dummy Normal: Flat normal with some subtle bumps
    dummy_normal = bpy.data.images.new(name="dummy_normal", width=1024, height=1024)
    pixels_normal = []
    for y in range(1024):
        for x in range(1024):
            val_x = 0.5 + math.sin(x * 0.05) * 0.1
            val_y = 0.5 + math.cos(y * 0.05) * 0.1
            pixels_normal.extend([val_x, val_y, 1.0, 1.0])
    dummy_normal.pixels = pixels_normal
    
    # Dummy Height: Simple height variation
    dummy_height = bpy.data.images.new(name="dummy_height", width=1024, height=1024)
    pixels_height = [0.5 + (math.sin(x * 0.02) * math.cos(y * 0.02)) * 0.1 for y in range(1024) for x in range(1024)]
    dummy_height.pixels = [p for p in pixels_height for _ in range(4)]

    # Function to create and link image texture nodes with box projection settings
    def create_and_link_image_texture(
        node_name, image, location_offset, colorspace, output_socket, input_socket,
        mapping_node, nodes_list, links_list, principled_bsdf_node
    ):
        img_tex = nodes_list.new(type='ShaderNodeTexImage')
        img_tex.name = node_name
        img_tex.label = node_name
        img_tex.image = image
        img_tex.location = (-200, location_offset)
        img_tex.image_user.interpolation = 'Linear'
        img_tex.extension = 'REPEAT'
        img_tex.projection = 'BOX' # Crucial setting for box projection
        img_tex.interpolation = 'Linear' # This controls the blend type for box projection
        img_tex.blend = blend_factor # Blending factor between projections

        links_list.new(mapping_node.outputs['Vector'], img_tex.inputs['Vector'])
        if input_socket: # Direct connection to principled BSDF
            links_list.new(img_tex.outputs[output_socket], input_socket)
        return img_tex

    # --- Setup Image Texture Nodes and Connections ---
    # Albedo (Base Color)
    albedo_tex = create_and_link_image_texture(
        "Albedo", dummy_albedo, 200, 'sRGB', 'Color', principled_bsdf.inputs['Base Color'],
        mapping, nodes, links, principled_bsdf
    )

    # Roughness
    roughness_tex = create_and_link_image_texture(
        "Roughness", dummy_roughness, 0, 'Non-Color', 'Color', principled_bsdf.inputs['Roughness'],
        mapping, nodes, links, principled_bsdf
    )
    
    # Metallic
    metallic_tex = create_and_link_image_texture(
        "Metallic", dummy_metallic, -200, 'Non-Color', 'Color', principled_bsdf.inputs['Metallic'],
        mapping, nodes, links, principled_bsdf
    )

    # Normal Map Setup (Image Texture -> Normal Map Node -> Principled BSDF)
    normal_map_node = nodes.new(type='ShaderNodeNormalMap')
    normal_map_node.location = (0, -400)
    links.new(normal_map_node.outputs['Normal'], principled_bsdf.inputs['Normal'])
    
    normal_tex = create_and_link_image_texture(
        "Normal", dummy_normal, -400, 'Non-Color', 'Color', normal_map_node.inputs['Color'],
        mapping, nodes, links, principled_bsdf
    )

    # Height Map Setup (Image Texture -> Bump Node -> Normal Map Node)
    bump_node = nodes.new(type='ShaderNodeBump')
    bump_node.location = (0, -600)
    bump_node.inputs['Strength'].default_value = 0.5
    links.new(bump_node.outputs['Normal'], normal_map_node.inputs['Normal']) # Connect bump to normal map input
    
    height_tex = create_and_link_image_texture(
        "Height", dummy_height, -600, 'Non-Color', 'Color', bump_node.inputs['Height'],
        mapping, nodes, links, principled_bsdf
    )
    
    # Set object location from parameters
    obj.location = Vector(location)

    # Ensure active object is selected for good measure
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    return f"Created '{object_name}' at {location} with seamless textured material."

