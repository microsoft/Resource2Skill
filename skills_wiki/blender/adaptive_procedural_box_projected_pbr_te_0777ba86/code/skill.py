def create_procedural_box_textured_object(
    scene_name: str = "Scene",
    object_name: str = "WornMetalObject",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    painted_color: tuple = (0.3, 0.6, 0.5, 1.0),  # Teal-ish, RGBA
    rust_color: tuple = (0.5, 0.2, 0.1, 1.0),    # Orange-brown, RGBA
    texture_scale: float = 3.0,
    subdivision_level: int = 3,
    bevel_width: float = 0.05,
    bevel_segments: int = 2,
    **kwargs,
) -> str:
    """
    Creates a multi-tiered cylindrical object with a procedural 'worn rusted painted' PBR material
    using object-space coordinate mapping, demonstrating seamless texturing without UVs.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        painted_color: (R, G, B, A) base paint color.
        rust_color: (R, G, B, A) rust color.
        texture_scale: Global scale factor for procedural textures.
        subdivision_level: Levels for the Subdivision Surface modifier.
        bevel_width: Width of the bevels applied to edges.
        bevel_segments: Number of segments in the bevels.
        **kwargs: Additional overrides (e.g., roughness for Principled BSDF).

    Returns:
        Status string, e.g., "Created 'WornMetalObject' at (0, 0, 0) with procedural box-projected material."
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Step 1: Create Base Geometry (Multi-tiered Cylinder) ---
    # Create initial cylinder
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=64, radius=1, depth=0.5,
        location=(0, 0, 0) # Create at origin first, then move
    )
    obj = bpy.context.active_object
    obj.name = object_name
    
    # Apply initial scaling and transform, crucial for correct bevel behavior
    obj.scale = (scale, scale, scale * 0.5) # Initial Z scaling from video's start
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.location = Vector(location) # Set final location

    # Enter Edit Mode for shaping
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    
    # Select top face using bmesh
    bm = bmesh.from_edit_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    
    top_face = None
    # Find face with normal pointing up and highest Z median
    max_z = -float('inf')
    for face in bm.faces:
        center = face.calc_center_median()
        if face.normal.z > 0.9 and center.z > max_z:
            top_face = face
            max_z = center.z
    
    if top_face:
        top_face.select = True
        
    bmesh.update_edit_mesh(obj.data) # Update to ensure selection
    
    # First tier: Inset and Extrude up
    bpy.ops.mesh.inset(thickness=0.2 * scale, depth=0)
    bpy.ops.mesh.extrude_region_move(
        MESH_OT_extrude_region={"mirror":False}, 
        TRANSFORM_OT_translate={"value":(0, 0, 0.2 * scale), "orient_type":'NORMAL', "constraint_axis":(False, False, True)}
    )

    # Second tier: Inset and Extrude down (creating a central hole)
    bpy.ops.mesh.inset(thickness=0.1 * scale, depth=0)
    bpy.ops.mesh.extrude_region_move(
        MESH_OT_extrude_region={"mirror":False}, 
        TRANSFORM_OT_translate={"value":(0, 0, -0.4 * scale), "orient_type":'NORMAL', "constraint_axis":(False, False, True)}
    )
    
    # Select relevant edge loops for beveling
    bpy.ops.mesh.select_mode(type='EDGE')
    bpy.ops.mesh.select_all(action='DESELECT') # Deselect all first
    
    bm = bmesh.from_edit_mesh(obj.data)
    bm.edges.ensure_lookup_table()
    bm.verts.ensure_lookup_table()
    
    # Select all horizontal edge loops, excluding top/bottom boundary loops of the object
    selected_edges = []
    # Identify loops based on typical Z coordinates after the complex extrusion.
    # These thresholds are relative to the object's local origin (0,0,0) after `transform_apply`.
    # Original cylinder was depth 0.5 (Z from -0.25 to 0.25 local).
    # After scale Z by 0.5, it's Z from -0.25*scale to 0.25*scale.
    # First extrude adds 0.2*scale on top: highest point at 0.25*scale + 0.2*scale = 0.45*scale.
    # Second extrude takes 0.4*scale down from this new top surface: inner hole bottom at 0.45*scale - 0.4*scale = 0.05*scale.

    # Loop 1: Top rim of central pillar (highest point)
    z_top_pillar_upper = 0.45 * scale
    z_top_pillar_lower = 0.43 * scale
    
    # Loop 2: Inner rim of central pillar (where it steps down)
    z_inner_step_upper = 0.27 * scale
    z_inner_step_lower = 0.25 * scale

    # Loop 3: Outer rim of middle tier (where it steps down)
    z_mid_tier_upper = -0.03 * scale
    z_mid_tier_lower = -0.05 * scale
    
    # Loop 4: Outer rim of lowest tier (just above the very bottom)
    z_low_tier_upper = -0.23 * scale
    z_low_tier_lower = -0.25 * scale

    for edge in bm.edges:
        is_horizontal_loop = all(abs(v.co.z - edge.verts[0].co.z) < 0.001*scale for v in edge.verts) # Check if all verts on edge have same Z
        is_boundary_edge = edge.is_boundary # Check if edge is on object boundary
        
        if is_horizontal_loop and not is_boundary_edge:
            avg_z = sum(v.co.z for v in edge.verts) / len(edge.verts)
            if (z_top_pillar_lower <= avg_z <= z_top_pillar_upper or
                z_inner_step_lower <= avg_z <= z_inner_step_upper or
                z_mid_tier_lower <= avg_z <= z_mid_tier_upper or
                z_low_tier_lower <= avg_z <= z_low_tier_upper):
                edge.select = True
                selected_edges.append(edge)
    
    bmesh.update_edit_mesh(obj.data) # Apply selection
    
    # Bevel selected edges
    bpy.ops.mesh.bevel(offset=bevel_width * scale, segments=bevel_segments, profile=0.5, clamp_overlap=True)

    bpy.ops.object.mode_set(mode='OBJECT') # Exit Edit Mode

    # --- Step 2: Add Subdivision Surface Modifier and Shade Smooth ---
    subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.levels = subdivision_level
    subdiv.render_levels = subdivision_level
    bpy.ops.object.shade_smooth()

    # --- Step 3: Create Material with Procedural PBR Textures and Object Coordinate Mapping ---
    material_name = f"{object_name}_Material"
    if material_name not in bpy.data.materials:
        mat = bpy.data.materials.new(name=material_name)
    else:
        mat = bpy.data.materials[material_name]

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear existing nodes
    for node in nodes:
        nodes.remove(node)

    # Create Principled BSDF shader
    principled_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled_bsdf.location = (800, 0)
    
    # Material Output
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    material_output.location = (1000, 0)

    # Link Principled BSDF to Material Output
    links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])

    # Texture Coordinate and Mapping nodes
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)

    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-400, 0)
    mapping.vector_type = 'POINT' # Default point transformation

    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # --- Procedural PBR Textures with Object Coordinates ---
    
    # Main Noise for Grunge/Rust pattern
    main_noise = nodes.new(type='ShaderNodeTexNoise')
    main_noise.location = (-200, 300)
    main_noise.inputs['Scale'].default_value = texture_scale * 2
    main_noise.inputs['Detail'].default_value = 10
    main_noise.inputs['Roughness'].default_value = 0.5
    main_noise.inputs['Distortion'].default_value = 0.5 # Add some grunge distortion
    links.new(mapping.outputs['Vector'], main_noise.inputs['Vector'])

    # Albedo (Base Color) - Mix painted and rust using noise
    albedo_color_ramp = nodes.new(type='ShaderNodeValToRGB')
    albedo_color_ramp.location = (200, 300)
    albedo_color_ramp.color_ramp.elements[0].position = 0.2
    albedo_color_ramp.color_ramp.elements[0].color = painted_color[:3]
    albedo_color_ramp.color_ramp.elements[1].position = 0.4
    albedo_color_ramp.color_ramp.elements[1].color = rust_color[:3]
    albedo_color_ramp.color_ramp.elements.new(0.8) 
    albedo_color_ramp.color_ramp.elements[2].color = painted_color[:3] # Worn spots
    links.new(main_noise.outputs['Fac'], albedo_color_ramp.inputs['Fac'])
    links.new(albedo_color_ramp.outputs['Color'], principled_bsdf.inputs['Base Color'])

    # Roughness Map
    roughness_noise = nodes.new(type='ShaderNodeTexNoise')
    roughness_noise.location = (-200, 100)
    roughness_noise.inputs['Scale'].default_value = texture_scale * 3
    roughness_noise.inputs['Detail'].default_value = 5
    roughness_noise.inputs['Roughness'].default_value = 0.7
    links.new(mapping.outputs['Vector'], roughness_noise.inputs['Vector'])
    
    roughness_color_ramp = nodes.new(type='ShaderNodeValToRGB')
    roughness_color_ramp.location = (200, 100)
    roughness_color_ramp.color_ramp.elements[0].position = 0.3
    roughness_color_ramp.color_ramp.elements[0].color = (0.2, 0.2, 0.2, 1) # Smoother areas
    roughness_color_ramp.color_ramp.elements[1].position = 0.8
    roughness_color_ramp.color_ramp.elements[1].color = (0.8, 0.8, 0.8, 1) # Rougher areas
    links.new(roughness_noise.outputs['Fac'], roughness_color_ramp.inputs['Fac'])
    links.new(roughness_color_ramp.outputs['Color'], principled_bsdf.inputs['Roughness'])
    
    # Metallic Map (Procedural to simulate exposed metal)
    metallic_noise = nodes.new(type='ShaderNodeTexNoise')
    metallic_noise.location = (-200, -100)
    metallic_noise.inputs['Scale'].default_value = texture_scale * 1.5
    metallic_noise.inputs['Detail'].default_value = 7
    metallic_noise.inputs['Roughness'].default_value = 0.6
    links.new(mapping.outputs['Vector'], metallic_noise.inputs['Vector'])

    metallic_color_ramp = nodes.new(type='ShaderNodeValToRGB')
    metallic_color_ramp.location = (200, -100)
    metallic_color_ramp.color_ramp.elements[0].position = 0.4
    metallic_color_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1) # Non-metallic
    metallic_color_ramp.color_ramp.elements[1].position = 0.6
    metallic_color_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1) # Metallic
    links.new(metallic_noise.outputs['Fac'], metallic_color_ramp.inputs['Fac'])
    links.new(metallic_color_ramp.outputs['Color'], principled_bsdf.inputs['Metallic'])

    # Normal Map (Procedural Bump)
    normal_noise = nodes.new(type='ShaderNodeTexNoise')
    normal_noise.location = (-200, -300)
    normal_noise.inputs['Scale'].default_value = texture_scale * 5
    normal_noise.inputs['Detail'].default_value = 12
    normal_noise.inputs['Roughness'].default_value = 0.5
    links.new(mapping.outputs['Vector'], normal_noise.inputs['Vector'])

    bump_node = nodes.new(type='ShaderNodeBump')
    bump_node.location = (400, -300)
    bump_node.inputs['Strength'].default_value = 0.5 # Default strength
    links.new(normal_noise.outputs['Fac'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], principled_bsdf.inputs['Normal'])

    # Assign material to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    
    # --- Finalize ---
    # Set the default world's background color to a neutral gray for better visibility
    default_world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    default_world.use_nodes = True
    background_node = default_world.node_tree.nodes.get("Background")
    if background_node:
        background_node.inputs['Color'].default_value = (0.05, 0.05, 0.05, 1)
        background_node.inputs['Strength'].default_value = 1.0
    scene.world = default_world

    return f"Created '{object_name}' at {location} with procedural box-projected material."

