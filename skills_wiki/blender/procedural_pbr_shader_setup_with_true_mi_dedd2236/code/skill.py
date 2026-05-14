def create_pbr_displaced_surface(
    scene_name: str = "Scene",
    object_name: str = "Displaced_PBR_Surface",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    base_color_dark: tuple = (0.15, 0.12, 0.1),  # Dark earthy brown
    base_color_light: tuple = (0.5, 0.45, 0.4),  # Light dusty stone
    displacement_scale: float = 0.25,
    subdivision_levels: int = 6,
    **kwargs,
) -> str:
    """
    Creates a highly subdivided plane with a fully routed procedural PBR material,
    configured for true mesh displacement in the Cycles render engine.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        base_color_dark: RGB base color for the "valleys" (0-1).
        base_color_light: RGB base color for the "peaks" (0-1).
        displacement_scale: Strength/height of the physical displacement.
        subdivision_levels: Number of subdivision levels (higher = more detail, slower).
        **kwargs: Additional options.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Force Cycles Engine for True Displacement ===
    # Displacement mapping physically moving vertices requires Cycles.
    scene.render.engine = 'CYCLES'

    # === Step 2: Create Base Geometry ===
    mesh = bpy.data.meshes.new(f"{object_name}_mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # Use bmesh to create a basic grid
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=4, y_segments=4, size=2.0)
    bm.to_mesh(mesh)
    bm.free()

    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))

    # Add Subdivision Surface modifier to provide geometry for displacement
    subdiv = obj.modifiers.new(name="Subdivision_for_Displacement", type='SUBSURF')
    subdiv.levels = subdivision_levels
    subdiv.render_levels = subdivision_levels
    subdiv.subdivision_type = 'SIMPLE' # Keep square edges

    # === Step 3: Build PBR Material Setup ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)

    # CRITICAL: Tell Cycles to use actual vertex displacement, not just bump
    mat.cycles.displacement_method = 'BOTH' # Displacement and Bump

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Nodes
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (1200, 0)

    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.location = (800, 0)

    disp_node = nodes.new(type='ShaderNodeDisplacement')
    disp_node.location = (800, -300)
    disp_node.inputs['Midlevel'].default_value = 0.5
    disp_node.inputs['Scale'].default_value = displacement_scale

    # Procedural Texture Generator (Acting as our downloaded PBR map)
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)

    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-400, 0)

    # Base noise for rocky height
    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.location = (-200, 0)
    noise.inputs['Scale'].default_value = 4.0
    noise.inputs['Detail'].default_value = 15.0
    noise.inputs['Roughness'].default_value = 0.65

    # Albedo / Base Color Map Simulation
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (300, 200)
    color_ramp.color_ramp.elements[0].color = (*base_color_dark, 1.0)
    color_ramp.color_ramp.elements[1].color = (*base_color_light, 1.0)
    color_ramp.color_ramp.elements[0].position = 0.35
    color_ramp.color_ramp.elements[1].position = 0.65

    # Roughness Map Simulation (peaks are drier/rougher, valleys are slightly smoother)
    rough_ramp = nodes.new(type='ShaderNodeValToRGB')
    rough_ramp.location = (300, -50)
    rough_ramp.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1.0)
    rough_ramp.color_ramp.elements[1].color = (0.95, 0.95, 0.95, 1.0)

    # Normal / Bump Map Simulation for micro details
    bump = nodes.new(type='ShaderNodeBump')
    bump.location = (300, -300)
    bump.inputs['Distance'].default_value = 0.05
    bump.inputs['Strength'].default_value = 0.8

    # === Step 4: Route the PBR Channels ===
    # Coordinates -> Noise
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])

    # Noise -> Color
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])

    # Noise -> Roughness
    links.new(noise.outputs['Fac'], rough_ramp.inputs['Fac'])
    links.new(rough_ramp.outputs['Color'], principled.inputs['Roughness'])

    # Noise -> Normal (Micro details)
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], principled.inputs['Normal'])

    # Noise -> True Displacement (Macro silhouette)
    links.new(noise.outputs['Fac'], disp_node.inputs['Height'])
    
    # Final connections to Output
    links.new(principled.outputs['BSDF'], out_node.inputs['Surface'])
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])

    return f"Created '{object_name}' with procedural PBR mapping and Cycles true displacement at {location}."
