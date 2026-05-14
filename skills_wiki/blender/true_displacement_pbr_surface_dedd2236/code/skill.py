def create_object(
    scene_name: str = "Scene",
    object_name: str = "DisplacedGround",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.3, 0.2, 0.15),
    **kwargs,
) -> str:
    """
    Create a PBR Displaced Ground plane in the active Blender scene.
    Demonstrates Cycles true displacement using a procedural texture 
    (as a self-contained substitute for downloaded image textures).

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created plane.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base rock color in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Use a Subdivision Surface modifier for non-destructive dense topology
    # (Replaces the destructive Edit Mode subdivide from the tutorial)
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 6
    subsurf.render_levels = 7

    # === Step 2: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    # CRITICAL: Enable true displacement in material settings (Tutorial 1:35)
    mat.cycles.displacement_method = 'DISPLACEMENT'
    obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Shader Nodes
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (800, 0)

    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (500, 200)

    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (500, -200)
    disp_node.inputs['Scale'].default_value = 0.2 * scale
    disp_node.inputs['Midlevel'].default_value = 0.0

    # Procedural Texture (Self-contained substitute for PolyHaven images)
    voronoi_node = nodes.new('ShaderNodeTexVoronoi')
    voronoi_node.location = (0, 0)
    voronoi_node.feature = 'DISTANCE_TO_EDGE'
    voronoi_node.inputs['Scale'].default_value = 5.0 / scale

    # ColorRamp for Height Mapping (Creates flat rocks with deep cracks)
    ramp_height = nodes.new('ShaderNodeValToRGB')
    ramp_height.location = (200, -200)
    ramp_height.color_ramp.elements[0].position = 0.0
    ramp_height.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    ramp_height.color_ramp.elements[1].position = 0.15
    ramp_height.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)

    # ColorRamp for Base Color
    ramp_color = nodes.new('ShaderNodeValToRGB')
    ramp_color.location = (200, 200)
    ramp_color.color_ramp.elements[0].position = 0.0
    ramp_color.color_ramp.elements[0].color = (0.05, 0.05, 0.05, 1.0) # Dark cracks
    ramp_color.color_ramp.elements[1].position = 0.1
    ramp_color.color_ramp.elements[1].color = (*material_color, 1.0) # Rock color

    # Connect Nodes
    links.new(voronoi_node.outputs['Distance'], ramp_height.inputs['Fac'])
    links.new(voronoi_node.outputs['Distance'], ramp_color.inputs['Fac'])
    
    links.new(ramp_height.outputs['Color'], disp_node.inputs['Height'])
    links.new(ramp_color.outputs['Color'], bsdf_node.inputs['Base Color'])
    
    links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])

    # === Step 3: Lighting & Rendering Context ===
    # Switch to Cycles to view displacement (Tutorial 1:15)
    scene.render.engine = 'CYCLES'
    # Optional: Switch to GPU compute if available to speed up viewport
    scene.cycles.device = 'GPU'

    # Add Sun Light (Tutorial 1:18)
    bpy.ops.object.light_add(type='SUN', location=(location[0]+5, location[1]-5, location[2]+10))
    sun = bpy.context.active_object
    sun.name = f"{object_name}_Sun"
    sun.data.energy = 5.0
    
    # Angle the sun to cast harsh shadows over the displaced geometry
    direction = Vector(location) - sun.location
    sun.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    return f"Created '{object_name}' with procedural PBR displacement and a Sun light at {location}."
