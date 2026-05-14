def create_object(
    scene_name: str = "Scene",
    object_name: str = "SeamlessTexturedObject",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    base_color_rgb: tuple = (0.2, 0.5, 0.4), # Base color for procedural texture, 0-1 range
    blend_factor: float = 0.15, # Blend factor for box projection
    subdivision_levels: int = 3,
    **kwargs,
) -> str:
    """
    Create a tiered cylindrical object with seamless object-based box projection PBR texturing.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        base_color_rgb: (R, G, B) base color for the procedural texture in 0-1 range.
        blend_factor: Amount of blend between box projections (0.0 to 1.0).
        subdivision_levels: Levels for the Subdivision Surface modifier.
        **kwargs: Additional overrides (not used in this version).

    Returns:
        Status string, e.g., "Created 'SeamlessTexturedObject' at (0, 0, 0)"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Step 1: Create Base Geometry (Cylinder) ---
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=1,
        depth=0.5,
        location=(0, 0, 0)
    )
    obj = bpy.context.active_object
    obj.name = object_name

    # Scale in Z axis as in the video (before applying scale for correct bevels)
    obj.scale.z = 0.25

    # Apply scale to prevent distortion in subsequent operations
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # --- Step 2: Shape the Geometry using BMesh ---
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()

    # Select top face
    top_face = None
    for face in bm.faces:
        if face.normal.z > 0.9: # Check if normal points roughly up
            top_face = face
            break

    if top_face:
        # Inset top face
        bmesh.ops.inset_regions(bm, faces=[top_face], thickness=0.1, depth=0)
        
        # Extrude up (first tier)
        extruded_face = bm.faces.active # New face after inset
        if extruded_face:
            bmesh.ops.extrude_face_region(bm, geom=[extruded_face])
            extruded_verts_top_tier = [v for v in extruded_face.verts if v.select]
            bmesh.ops.translate(bm, verts=extruded_verts_top_tier, vec=(0, 0, 0.2))

            # Inset the new top face of the first tier
            top_face_tier1 = bm.faces.active
            bmesh.ops.inset_regions(bm, faces=[top_face_tier1], thickness=0.08, depth=0)

            # Extrude up (second tier)
            extruded_face_tier2 = bm.faces.active
            if extruded_face_tier2:
                bmesh.ops.extrude_face_region(bm, geom=[extruded_face_tier2])
                extruded_verts_top_tier2 = [v for v in extruded_face_tier2.verts if v.select]
                bmesh.ops.translate(bm, verts=extruded_verts_top_tier2, vec=(0, 0, 0.15))
                
                # Inset the new top face of the second tier
                top_face_tier2_final = bm.faces.active
                bmesh.ops.inset_regions(bm, faces=[top_face_tier2_final], thickness=0.05, depth=0)

                # Extrude down (inner hole)
                inner_hole_face = bm.faces.active
                if inner_hole_face:
                    bmesh.ops.extrude_face_region(bm, geom=[inner_hole_face])
                    inner_hole_verts = [v for v in inner_hole_face.verts if v.select]
                    bmesh.ops.translate(bm, verts=inner_hole_verts, vec=(0, 0, -0.2))


    # --- Bevel specific edges to sharpen corners ---
    # Find edge loops to bevel. This is done by looking for edges with two non-coplanar faces.
    # For a simple cylindrical shape, these are usually the horizontal edges at the tiers.
    edges_to_bevel = []
    
    # Select horizontal edges at the top of the base, first tier, and second tier
    for edge in bm.edges:
        if len(edge.link_faces) == 2:
            f1 = edge.link_faces[0]
            f2 = edge.link_faces[1]
            # Check if faces are roughly perpendicular to simulate sharp corners
            if abs(f1.normal.dot(f2.normal)) < 0.1: # Threshold for "perpendicular"
                # Check for horizontal edges (normal in Z is close to 0)
                edge_center = sum([v.co for v in edge.verts], Vector()) / len(edge.verts)
                if abs(edge.verts[0].co.z - edge.verts[1].co.z) < 0.01: # Check if edge is flat (horizontal)
                    # Exclude the inner bottom edge of the hole, it tends to cause issues with current setup.
                    # Or, just target specific heights known from creation
                    if edge_center.z > -0.1 and edge_center.z < 0.4: # Filter by approximate height
                        edges_to_bevel.append(edge)

    # Use a set to avoid duplicates and ensure unique edges
    unique_edges_to_bevel = set()
    for edge in edges_to_bevel:
        # Check if the edge is part of a horizontal loop that defines a sharp transition
        # This is a heuristic and might need tuning for different geometries.
        if edge.verts[0].co.z > 0.01 and edge.verts[1].co.z > 0.01: # Avoid bottom edge of cylinder
             # Find edge loops for the tiered structure's horizontal transitions
            if any(v.co.z > 0.49 for v in edge.verts) or \
               any(v.co.z > 0.28 and v.co.z < 0.32 for v in edge.verts) or \
               any(v.co.z > 0.09 and v.co.z < 0.12 for v in edge.verts):
                unique_edges_to_bevel.add(edge)
    
    # Try to get the very bottom edge as well
    bottom_edges = [edge for edge in bm.edges if any(v.co.z < -0.01 for v in edge.verts) and all(abs(v.co.z - bm.verts[0].co.z) < 0.01 for v in edge.verts)]
    for edge in bottom_edges:
        if any(f.normal.z < -0.9 for f in edge.link_faces): # faces pointing down (bottom)
            unique_edges_to_bevel.add(edge)

    # Convert set back to list for bmesh.ops
    edges_for_bevel = list(unique_edges_to_bevel)

    if edges_for_bevel:
        try:
            bmesh.ops.bevel(
                bm,
                geom=edges_for_bevel,
                offset=0.02,
                segments=2,
                profile=0.5,
                vertex_only=False
            )
        except RuntimeError as e:
            print(f"Bevel operation failed: {e}")
            # This can happen if edges are not suitable for bevel, often due to topology.
            # For robustness, might need more sophisticated edge selection or modifier.

    bm.to_mesh(obj.data)
    obj.data.update()
    bm.free()

    # --- Step 3: Add Modifiers (Subdivision Surface) ---
    subdiv_mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv_mod.levels = subdivision_levels
    subdiv_mod.render_levels = subdivision_levels

    # --- Step 4: Apply Material with Box Projection ---
    mat = bpy.data.materials.new(name=f"{object_name}_Material")
    obj.data.materials.append(mat)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes except Principled BSDF
    for node in nodes:
        if node.type == 'BSDF_PRINCIPLED':
            principled_bsdf = node
        elif node.type == 'MATERIAL_OUTPUT':
            material_output = node
        else:
            nodes.remove(node)

    # Get Principled BSDF and Material Output nodes
    # If they were removed by above loop (due to error), recreate them
    if 'principled_bsdf' not in locals():
        principled_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])
    if 'material_output' not in locals():
        material_output = nodes.new(type='ShaderNodeOutputMaterial')
        links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])


    # Create Texture Coordinate and Mapping nodes
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    mapping = nodes.new(type='ShaderNodeMapping')
    
    # Position nodes
    tex_coord.location = (-1000, 0)
    mapping.location = (-800, 0)
    principled_bsdf.location = (-200, 0)
    material_output.location = (200, 0)

    # Connect Object output to Mapping input
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # --- Use procedural textures to simulate PBR maps for Box Projection ---
    # Albedo / Base Color
    noise_color = nodes.new(type='ShaderNodeTexNoise')
    noise_color.location = (-600, 300)
    noise_color.noise_dimensions = '3D'
    noise_color.inputs['Scale'].default_value = 10.0
    noise_color.inputs['Detail'].default_value = 10.0
    noise_color.inputs['Roughness'].default_value = 0.5
    noise_color.inputs['Distortion'].default_value = 0.0

    # Configure for Box Projection
    noise_color.projection = 'BOX'
    noise_color.interpolation = 'CUBIC'
    noise_color.inputs['Blend'].default_value = blend_factor # Set blend factor

    links.new(mapping.outputs['Vector'], noise_color.inputs['Vector'])
    links.new(noise_color.outputs['Color'], principled_bsdf.inputs['Base Color'])

    # Roughness Map (using another noise texture)
    noise_roughness = nodes.new(type='ShaderNodeTexNoise')
    noise_roughness.location = (-600, 0)
    noise_roughness.noise_dimensions = '3D'
    noise_roughness.inputs['Scale'].default_value = 20.0
    noise_roughness.inputs['Detail'].default_value = 8.0
    noise_roughness.inputs['Roughness'].default_value = 0.7
    
    # Configure for Box Projection
    noise_roughness.projection = 'BOX'
    noise_roughness.interpolation = 'CUBIC'
    noise_roughness.inputs['Blend'].default_value = blend_factor # Set blend factor

    links.new(mapping.outputs['Vector'], noise_roughness.inputs['Vector'])
    links.new(noise_roughness.outputs['Fac'], principled_bsdf.inputs['Roughness'])

    # Normal Map (using a bump node from noise for demonstration)
    noise_bump = nodes.new(type='ShaderNodeTexNoise')
    noise_bump.location = (-600, -300)
    noise_bump.noise_dimensions = '3D'
    noise_bump.inputs['Scale'].default_value = 50.0
    noise_bump.inputs['Detail'].default_value = 12.0
    noise_bump.inputs['Roughness'].default_value = 0.5

    # Configure for Box Projection
    noise_bump.projection = 'BOX'
    noise_bump.interpolation = 'CUBIC'
    noise_bump.inputs['Blend'].default_value = blend_factor # Set blend factor

    bump_node = nodes.new(type='ShaderNodeBump')
    bump_node.location = (-400, -300)
    bump_node.inputs['Strength'].default_value = 0.5
    
    links.new(mapping.outputs['Vector'], noise_bump.inputs['Vector'])
    links.new(noise_bump.outputs['Fac'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], principled_bsdf.inputs['Normal'])

    # Set base color on Principled BSDF
    principled_bsdf.inputs['Base Color'].default_value = (base_color_rgb[0], base_color_rgb[1], base_color_rgb[2], 1.0)
    principled_bsdf.inputs['Metallic'].default_value = 0.2 # Example metallic value

    # --- Apply initial object location and global scale ---
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # --- Finalize ---
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.shade_smooth() # Set object shading to smooth

    return f"Created '{object_name}' at {location}"

