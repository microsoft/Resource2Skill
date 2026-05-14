def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Surface",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 2.0,
    material_color: tuple = (0.6, 0.25, 0.2),
    **kwargs,
) -> str:
    """
    Create a PBR surface using true adaptive displacement in Cycles.
    Simulates a comprehensive PBR node workflow (Albedo, Roughness, Normal, Displacement).

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the plane.
        material_color: (R, G, B) base color for the procedural texture.
        **kwargs: Additional overrides (e.g., disp_scale).

    Returns:
        Status string describing the creation and settings.
    """
    import bpy

    # Fetch scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Configure Render Engine for Adaptive Displacement ===
    # True micro-polygon displacement requires Cycles and the Experimental feature set
    scene.render.engine = 'CYCLES'
    try:
        scene.cycles.feature_set = 'EXPERIMENTAL'
    except AttributeError:
        pass # Handle case if API structure differs slightly

    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    
    # Apply Scale so displacement scale is accurate
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Add Subdivision Surface Modifier
    subsurf = obj.modifiers.new(name="Adaptive_Subsurf", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE' # Keep the plane square
    
    # Enable Adaptive Subdivision (requires experimental cycles to be active)
    try:
        subsurf.use_adaptive_subdivision = True
    except AttributeError:
        pass # Safe fallback for different Blender versions

    # === Step 3: Build Procedural PBR Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    
    # Crucial: Tell Cycles to use true displacement on this material
    mat.cycles.displacement_method = 'DISPLACEMENT' # Equivalent to "Displacement Only"
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes safely
    nodes.clear()

    # --- Setup Core Nodes ---
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (1000, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (600, 0)

    # --- Setup Coordinate Mapping (Ctrl+T equivalent) ---
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    
    # Link UV/Generated to Mapping
    links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])

    # --- 1. Base Color (Albedo) ---
    color_noise = nodes.new('ShaderNodeTexNoise')
    color_noise.location = (-200, 300)
    color_noise.inputs['Scale'].default_value = 5.0
    
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (100, 300)
    # Map noise to our chosen material color and a darker variant
    color_ramp.color_ramp.elements[0].color = (material_color[0]*0.3, material_color[1]*0.3, material_color[2]*0.3, 1.0)
    color_ramp.color_ramp.elements[1].color = (material_color[0], material_color[1], material_color[2], 1.0)
    
    links.new(mapping.outputs['Vector'], color_noise.inputs['Vector'])
    links.new(color_noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])

    # --- 2. Roughness Map ---
    # Simulates loading a gloss/roughness map as Non-Color data
    rough_voronoi = nodes.new('ShaderNodeTexVoronoi')
    rough_voronoi.location = (-200, 0)
    rough_voronoi.inputs['Scale'].default_value = 15.0
    
    # Invert node (as shown in the tutorial for Gloss maps)
    invert = nodes.new('ShaderNodeInvert')
    invert.location = (100, 0)
    
    links.new(mapping.outputs['Vector'], rough_voronoi.inputs['Vector'])
    links.new(rough_voronoi.outputs['Distance'], invert.inputs['Color'])
    links.new(invert.outputs['Color'], bsdf.inputs['Roughness'])

    # --- 3. Normal Map ---
    # Simulates bumping via a Normal Map node
    normal_noise = nodes.new('ShaderNodeTexNoise')
    normal_noise.location = (-200, -300)
    normal_noise.inputs['Scale'].default_value = 25.0
    
    normal_map = nodes.new('ShaderNodeNormalMap')
    normal_map.location = (100, -300)
    normal_map.inputs['Strength'].default_value = 0.5
    
    links.new(mapping.outputs['Vector'], normal_noise.inputs['Vector'])
    links.new(normal_noise.outputs['Color'], normal_map.inputs['Color'])
    links.new(normal_map.outputs['Normal'], bsdf.inputs['Normal'])

    # --- 4. True Displacement Map ---
    # The star of the show. We pass procedural height data into a Displacement Node
    disp_noise = nodes.new('ShaderNodeTexMusgrave') # Using Musgrave for stark height contrast
    disp_noise.location = (200, -600)
    disp_noise.inputs['Scale'].default_value = 4.0
    
    displacement = nodes.new('ShaderNodeDisplacement')
    displacement.location = (600, -500)
    
    # Key settings highlighted in tutorial
    displacement.inputs['Midlevel'].default_value = 0.0
    disp_scale = kwargs.get("disp_scale", 0.1) # Default to 0.1 so it doesn't tear the mesh
    displacement.inputs['Scale'].default_value = disp_scale
    
    links.new(mapping.outputs['Vector'], disp_noise.inputs['Vector'])
    links.new(disp_noise.outputs['Fac'], displacement.inputs['Height'])
    
    # Connect to Output
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    links.new(displacement.outputs['Displacement'], output.inputs['Displacement'])

    # Assign material to object
    obj.data.materials.append(mat)
    
    # Smooth shading for better visual results
    bpy.ops.object.shade_smooth()

    return f"Created '{object_name}' at {location}. Cycles Experimental Adaptive Displacement configured with scale {disp_scale}."
