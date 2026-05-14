def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Terrain",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.15, 0.10, 0.07),  # Dark rocky brown
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with a procedural PBR material and true Cycles displacement.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Enable Cycles (True Displacement only works in Cycles)
    scene.render.engine = 'CYCLES'

    # === Step 1: Base Geometry ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    # Create a dense base grid using bmesh
    bm = bmesh.new()
    # 64x64 segments gives the displacement enough vertices to work with
    bmesh.ops.create_grid(bm, x_segments=64, y_segments=64, size=2.0)
    bm.to_mesh(mesh)
    bm.free()
    
    # Add Subdivision Surface modifier for even more detail
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 3
    subsurf.render_levels = 4
    
    # === Step 2: Build Procedural PBR Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    
    # Critical step: Enable true displacement in material settings
    mat.cycles.displacement_method = 'DISPLACEMENT' 
    obj.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Material Output
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1000, 0)
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (600, 0)
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])
    
    # Displacement Node
    disp_node = nodes.new('ShaderNodeDisplacement')
    disp_node.location = (600, -300)
    disp_node.inputs['Scale'].default_value = scale * 0.25
    disp_node.inputs['Midlevel'].default_value = 0.5
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])
    
    # Texture Coordinates & Mapping
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-400, 0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    
    # Height Map Generation (Procedural substitute for downloaded texture)
    noise_height = nodes.new('ShaderNodeTexNoise')
    noise_height.location = (-100, -300)
    noise_height.inputs['Scale'].default_value = 3.0
    noise_height.inputs['Detail'].default_value = 15.0
    noise_height.inputs['Roughness'].default_value = 0.65
    links.new(mapping.outputs['Vector'], noise_height.inputs['Vector'])
    links.new(noise_height.outputs['Fac'], disp_node.inputs['Height'])
    
    # Normal/Bump Map
    bump = nodes.new('ShaderNodeBump')
    bump.location = (300, -150)
    bump.inputs['Strength'].default_value = 0.6
    bump.inputs['Distance'].default_value = 0.1
    
    noise_bump = nodes.new('ShaderNodeTexNoise')
    noise_bump.location = (-100, -100)
    noise_bump.inputs['Scale'].default_value = 40.0 # High frequency micro-detail
    links.new(mapping.outputs['Vector'], noise_bump.inputs['Vector'])
    links.new(noise_bump.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    
    # Albedo (Color) Map
    ramp_color = nodes.new('ShaderNodeValToRGB')
    ramp_color.location = (200, 200)
    ramp_color.color_ramp.elements[0].position = 0.2
    ramp_color.color_ramp.elements[0].color = (material_color[0] * 0.3, material_color[1] * 0.3, material_color[2] * 0.3, 1.0)
    ramp_color.color_ramp.elements[1].position = 0.8
    ramp_color.color_ramp.elements[1].color = (material_color[0], material_color[1], material_color[2], 1.0)
    links.new(noise_height.outputs['Fac'], ramp_color.inputs['Fac'])
    links.new(ramp_color.outputs['Color'], bsdf.inputs['Base Color'])
    
    # Roughness Map
    ramp_rough = nodes.new('ShaderNodeValToRGB')
    ramp_rough.location = (200, 0)
    ramp_rough.color_ramp.elements[0].position = 0.3
    ramp_rough.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1.0)
    ramp_rough.color_ramp.elements[1].position = 0.7
    ramp_rough.color_ramp.elements[1].color = (0.95, 0.95, 0.95, 1.0)
    links.new(noise_height.outputs['Fac'], ramp_rough.inputs['Fac'])
    links.new(ramp_rough.outputs['Color'], bsdf.inputs['Roughness'])
    
    # === Step 3: Lighting Setup ===
    # A strong directional light is required to visualize the displacement shadows
    sun_data = bpy.data.lights.new(name=f"{object_name}_Sun", type='SUN')
    sun_data.energy = 5.0
    sun_data.angle = math.radians(10.0)
    sun_obj = bpy.data.objects.new(name=f"{object_name}_SunLight", object_data=sun_data)
    scene.collection.objects.link(sun_obj)
    
    sun_obj.location = (location[0] + 5 * scale, location[1] - 5 * scale, location[2] + 10 * scale)
    
    # Point sun downwards at an angle towards the plane
    direction = Vector(location) - sun_obj.location
    sun_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    
    # === Step 4: Finalize Location & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    # Smooth shading for better displacement interpretation
    for poly in mesh.polygons:
        poly.use_smooth = True
        
    return f"Created '{object_name}' with PBR Displacement and a Sun Light at {location}. (Note: Render in Cycles to see displacement)"
