def create_pbr_displacement_setup(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Plane",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 2.0,
    material_color_1: tuple = (0.6, 0.2, 0.1, 1.0),
    material_color_2: tuple = (0.3, 0.1, 0.05, 1.0),
    **kwargs,
) -> str:
    """
    Create a PBR Material Setup with True Adaptive Displacement.
    Uses a procedural brick texture to simulate a full PBR image map pipeline.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color_1: (R, G, B, A) primary brick color.
        material_color_2: (R, G, B, A) secondary brick color.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Engine Context Setup ===
    # True displacement requires Cycles and the Experimental feature set
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'EXPERIMENTAL'
    
    # === Step 2: Create Base Geometry ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=1)
    bm.to_mesh(mesh)
    bm.free()
    
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    # === Step 3: Modifier Setup ===
    subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.subdivision_type = 'SIMPLE'
    # Enable Adaptive Subdivision (only works if Cycles is Experimental)
    if hasattr(subdiv, 'use_adaptive_subdivision'):
        subdiv.use_adaptive_subdivision = True
    
    # === Step 4: Material & PBR Node Pipeline ===
    mat_name = f"{object_name}_PBR_Mat"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    
    # CRITICAL: Tell Blender to physically displace geometry, not just fake bump
    mat.cycles.displacement_method = 'DISPLACEMENT_AND_BUMP'
    obj.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Base Shader and Output
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (1000, 0)
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (600, 100)
    
    # Coordinates & Mapping
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    
    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-400, 0)
    
    # Texture Source (Proxy for downloaded PBR maps)
    brick_tex = nodes.new(type='ShaderNodeTexBrick')
    brick_tex.location = (-150, 0)
    brick_tex.inputs['Color1'].default_value = material_color_1
    brick_tex.inputs['Color2'].default_value = material_color_2
    brick_tex.inputs['Mortar'].default_value = (0.8, 0.8, 0.8, 1.0)
    brick_tex.inputs['Scale'].default_value = 4.0
    
    # Roughness Conversion (Acts like the Invert node for Gloss maps in the tutorial)
    map_range = nodes.new(type='ShaderNodeMapRange')
    map_range.location = (200, -100)
    map_range.inputs['To Min'].default_value = 0.4 # Bricks are moderately rough
    map_range.inputs['To Max'].default_value = 0.9 # Mortar is very rough
    
    # Normal/Bump Translation
    bump = nodes.new(type='ShaderNodeBump')
    bump.location = (200, -300)
    bump.inputs['Distance'].default_value = 0.05
    
    # True Displacement Node
    displacement = nodes.new(type='ShaderNodeDisplacement')
    displacement.location = (600, -300)
    displacement.inputs['Scale'].default_value = 0.1  # Tutorial explicitly lowers this from 1.0 to 0.1
    displacement.inputs['Midlevel'].default_value = 0.0 # Tutorial explicitly sets this to 0.0 to prevent mesh offset
    
    # === Step 5: Wire the PBR Pipeline ===
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], brick_tex.inputs['Vector'])
    
    # Albedo (Color)
    links.new(brick_tex.outputs['Color'], bsdf.inputs['Base Color'])
    
    # Roughness (Non-Color)
    links.new(brick_tex.outputs['Fac'], map_range.inputs['Value'])
    links.new(map_range.outputs['Result'], bsdf.inputs['Roughness'])
    
    # Normal/Bump (Non-Color)
    links.new(brick_tex.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    
    # Displacement (Non-Color -> Material Output)
    links.new(brick_tex.outputs['Fac'], displacement.inputs['Height'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    links.new(displacement.outputs['Displacement'], output.inputs['Displacement'])
    
    return f"Created '{object_name}' with True PBR Displacement. Render engine set to Cycles Experimental."
