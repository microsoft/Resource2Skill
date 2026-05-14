def create_object(
    scene_name: str = "Scene",
    object_name: str = "WarpedSphere",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.6, 0.1),  # Golden metallic tint
    **kwargs,
) -> str:
    """
    Create a highly subdivided sphere with procedural vector-warped true displacement.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created abstract sphere.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the object and its displacement.
        material_color: (R, G, B) base color for the Fresnel rim lighting.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created object and scene modifications.
    """
    import bpy

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Engine Preparation ===
    # True displacement requires Cycles
    scene.render.engine = 'CYCLES'
    
    # Set world background to black for contrast
    if scene.world and scene.world.use_nodes:
        bg_node = scene.world.node_tree.nodes.get("Background")
        if bg_node:
            bg_node.inputs[0].default_value = (0, 0, 0, 1)

    # === Step 2: Create Base Geometry ===
    # Using an icosphere for uniform topology without poles
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5, radius=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)
    bpy.ops.object.shade_smooth()
    
    # Add Subdivision Surface modifier for dense micro-polygon details
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2
    
    # === Step 3: Build Procedural Warped Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_WarpMat")
    mat.use_nodes = True
    # Crucial: Enable physical displacement in the material settings
    mat.cycles.displacement_method = 'DISPLACEMENT' 
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Output Node
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (800, 0)
    
    # Glossy Surface
    glossy = nodes.new('ShaderNodeBsdfGlossy')
    glossy.inputs['Roughness'].default_value = 0.05
    glossy.location = (500, 100)
    
    # Fresnel node for dynamic edge lighting
    fresnel = nodes.new('ShaderNodeFresnel')
    fresnel.inputs['IOR'].default_value = 2.0
    fresnel.location = (100, 200)
    
    # ColorRamp to map Fresnel to colors
    cramp = nodes.new('ShaderNodeValToRGB')
    cramp.color_ramp.elements[0].color = (0.05, 0.05, 0.05, 1.0) # Core/facing color (dark)
    cramp.color_ramp.elements[1].color = (*material_color, 1.0)  # Rim color
    cramp.location = (300, 200)
    
    # Displacement Node
    disp = nodes.new('ShaderNodeDisplacement')
    disp.inputs['Midlevel'].default_value = 0.5
    disp.inputs['Scale'].default_value = 0.2 * scale # Proportional displacement
    disp.location = (500, -200)
    
    # Base Pattern: Voronoi
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.inputs['Scale'].default_value = 2.5
    voronoi.location = (200, -200)
    
    # Warping Driver: Noise Texture
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 5.0
    noise.inputs['Detail'].default_value = 2.0
    noise.location = (-100, -200)
    
    # --- Connect the Nodes ---
    # The Vector Warp: Noise Color -> Voronoi Vector
    links.new(noise.outputs['Color'], voronoi.inputs['Vector']) 
    
    # Displacement
    links.new(voronoi.outputs['Color'], disp.inputs['Height'])
    links.new(disp.outputs['Displacement'], out_node.inputs['Displacement'])
    
    # Shading
    links.new(fresnel.outputs['Fac'], cramp.inputs['Fac'])
    links.new(cramp.outputs['Color'], glossy.inputs['Color'])
    links.new(glossy.outputs['BSDF'], out_node.inputs['Surface'])
    
    obj.data.materials.append(mat)
    
    # === Step 4: Create Studio Lighting (Blackbody Emission Plane) ===
    light_name = f"{object_name}_WarmStudioLight"
    if light_name not in bpy.data.objects:
        # Position overhead
        bpy.ops.mesh.primitive_plane_add(size=5.0, location=(location[0], location[1], location[2] + (3.0 * scale)))
        light_obj = bpy.context.active_object
        light_obj.name = light_name
        light_obj.scale = (2.0, 0.5, 1.0) # Strip light shape
        
        light_mat = bpy.data.materials.new(name=f"{light_name}_EmissionMat")
        light_mat.use_nodes = True
        l_nodes = light_mat.node_tree.nodes
        l_links = light_mat.node_tree.links
        l_nodes.clear()
        
        l_out = l_nodes.new('ShaderNodeOutputMaterial')
        l_out.location = (300, 0)
        
        l_emission = l_nodes.new('ShaderNodeEmission')
        l_emission.inputs['Strength'].default_value = 15.0
        l_emission.location = (100, 0)
        
        l_blackbody = l_nodes.new('ShaderNodeBlackbody')
        l_blackbody.inputs['Temperature'].default_value = 3200.0 # Warm, realistic bulb color
        l_blackbody.location = (-100, 0)
        
        l_links.new(l_blackbody.outputs['Color'], l_emission.inputs['Color'])
        l_links.new(l_emission.outputs['Emission'], l_out.inputs['Surface'])
        
        light_obj.data.materials.append(light_mat)
        
    return f"Created '{object_name}' (Warped Sphere) with true displacement and 3200K Blackbody light at {location}"
