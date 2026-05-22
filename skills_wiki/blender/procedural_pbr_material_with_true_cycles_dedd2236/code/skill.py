def create_object(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Wall",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.35, 0.25, 0.20),
    **kwargs,
) -> str:
    """
    Create a highly subdivided plane with true material displacement in Cycles.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created plane.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the procedural rock/dirt.
        **kwargs: Additional overrides (e.g., disp_scale).

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # 0. The tutorial effect fundamentally requires Cycles to render true displacement
    scene.render.engine = 'CYCLES'

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2.0)
    obj = bpy.context.active_object
    obj.name = object_name
    
    # Add heavy subdivision to provide geometry for the displacement
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE' # Keeps the edges square
    subsurf.levels = 6
    subsurf.render_levels = 6

    # === Step 2: Build Procedural PBR Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    
    # CRITICAL: Tell Cycles to actually move geometry, not just fake normals
    mat.cycles.displacement_method = 'DISPLACEMENT'
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Clear default nodes
    
    # Output and Shader
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    
    # Displacement Node
    disp = nodes.new('ShaderNodeDisplacement')
    disp.location = (0, -200)
    disp.inputs['Midlevel'].default_value = 0.5
    disp_scale = kwargs.get('disp_scale', 0.2)
    disp.inputs['Scale'].default_value = disp_scale
    
    # Procedural Texture (simulating the downloaded PBR images)
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-400, 0)
    noise.inputs['Scale'].default_value = 10.0
    noise.inputs['Detail'].default_value = 15.0
    noise.inputs['Roughness'].default_value = 0.65 # Crunchy, rock-like detail
    
    # Color mapping
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-200, 100)
    color_ramp.color_ramp.elements[0].color = (material_color[0]*0.3, material_color[1]*0.3, material_color[2]*0.3, 1.0)
    color_ramp.color_ramp.elements[1].color = (material_color[0], material_color[1], material_color[2], 1.0)
    
    # Connect everything
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    
    # Fake Albedo
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
    
    # Fake Roughness map
    links.new(noise.outputs['Fac'], bsdf.inputs['Roughness'])
    
    # True Displacement Height map
    links.new(noise.outputs['Fac'], disp.inputs['Height'])
    
    # Final outputs
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    links.new(disp.outputs['Displacement'], output.inputs['Displacement'])
    
    # Assign material
    obj.data.materials.append(mat)
    bpy.ops.object.shade_smooth()

    # === Step 3: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # === Step 4: Lighting (Crucial for showing off displacement) ===
    light_name = f"{object_name}_Sun"
    light_data = bpy.data.lights.new(name=light_name, type='SUN')
    light_data.energy = 5.0
    light_data.angle = 0.1 # Sharp angle for distinct shadows
    
    light_obj = bpy.data.objects.new(name=light_name, object_data=light_data)
    scene.collection.objects.link(light_obj)
    
    # Position sun above and to the side, pointing at the plane
    light_obj.location = Vector(location) + Vector((-5, -5, 5))
    direction = Vector(location) - light_obj.location
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    return f"Created '{obj.name}' with True Displacement material '{mat.name}' and Sun light. Set viewport to Cycles Rendered view to see geometry changes."
