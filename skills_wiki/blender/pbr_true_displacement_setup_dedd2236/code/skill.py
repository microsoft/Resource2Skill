def create_displaced_pbr_surface(
    scene_name: str = "Scene",
    object_name: str = "DisplacedRockPlane",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 4.0,
    material_color: tuple = (0.4, 0.35, 0.3),
    **kwargs
) -> str:
    """
    Creates a highly subdivided plane with a procedural PBR material utilizing 
    Cycles' True Displacement to generate a 3D rocky surface.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created plane.
        location: (x, y, z) world-space position.
        scale: Size of the plane.
        material_color: (R, G, B) base color of the rock surface.
        **kwargs: Optional 'subdiv_levels' (default 7) and 'displacement_scale' (default 0.2).

    Returns:
        Status string describing the created setup.
    """
    import bpy
    import math

    # Configuration kwargs
    subdiv_levels = kwargs.get("subdiv_levels", 7)
    disp_scale = kwargs.get("displacement_scale", 0.2)

    # 1. Enforce Cycles (Required for True Displacement)
    bpy.context.scene.render.engine = 'CYCLES'
    if bpy.context.scene.cycles.feature_set == 'SUPPORTED':
        # Optional: Adaptive subdivision works best with experimental, but we'll use a brute-force modifier for safety
        pass

    # 2. Create Base Geometry
    bpy.ops.mesh.primitive_plane_add(size=scale, location=location)
    obj = bpy.context.active_object
    obj.name = object_name

    # 3. Add High-Density Subdivision Surface
    subsurf = obj.modifiers.new(name="Displacement_Subdiv", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = subdiv_levels
    subsurf.render_levels = subdiv_levels

    # 4. Create & Configure PBR Material
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    # CRITICAL: Enable True Displacement in material settings
    mat.cycles.displacement_method = 'DISPLACEMENT'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Clear defaults

    # Core Output Nodes
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (1000, 0)
    
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (600, 0)
    
    displacement = nodes.new('ShaderNodeDisplacement')
    displacement.location = (600, -300)
    displacement.inputs['Scale'].default_value = disp_scale
    displacement.inputs['Midlevel'].default_value = 0.0

    # Procedural Height/Pattern (Voronoi 'Distance to Edge' creates rocky cracks)
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (0, 0)
    voronoi.feature = 'DISTANCE_TO_EDGE'
    voronoi.inputs['Scale'].default_value = 5.0

    # Base Color via ColorRamp
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (300, 200)
    elements = color_ramp.color_ramp.elements
    # Dark cracks
    elements[0].position = 0.05
    elements[0].color = (material_color[0]*0.2, material_color[1]*0.2, material_color[2]*0.2, 1.0)
    # Surface color
    elements[1].position = 0.4
    elements[1].color = (material_color[0], material_color[1], material_color[2], 1.0)

    # Roughness mapping (cracks are rougher, peaks slightly smoother)
    map_range = nodes.new('ShaderNodeMapRange')
    map_range.location = (300, 0)
    map_range.inputs['From Min'].default_value = 0.0
    map_range.inputs['From Max'].default_value = 1.0
    map_range.inputs['To Min'].default_value = 0.9 # Cracks
    map_range.inputs['To Max'].default_value = 0.5 # Surface

    # Micro-detail Bump (for high-frequency texture on the rocks)
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (0, -300)
    noise.inputs['Scale'].default_value = 40.0
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (300, -300)
    bump.inputs['Distance'].default_value = 0.02
    
    # 5. Connect the Node Tree
    # Color
    links.new(voronoi.outputs['Distance'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
    
    # Roughness
    links.new(voronoi.outputs['Distance'], map_range.inputs['Value'])
    links.new(map_range.outputs['Result'], principled.inputs['Roughness'])
    
    # Normal/Bump
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], principled.inputs['Normal'])
    
    # Displacement (The core skill)
    links.new(voronoi.outputs['Distance'], displacement.inputs['Height'])
    
    # Final Outputs
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    links.new(displacement.outputs['Displacement'], output.inputs['Displacement'])

    # 6. Ensure complimentary lighting (Sun light to cast shadows over the displaced geometry)
    sun_found = any(light.type == 'SUN' for light in bpy.data.lights)
    if not sun_found:
        bpy.ops.object.light_add(
            type='SUN', 
            location=(location[0] + 5, location[1] - 5, location[2] + 10)
        )
        sun = bpy.context.active_object
        sun.name = f"{object_name}_Sun"
        sun.data.energy = 5.0 # High energy to emulate outdoor sun
        # Angle at roughly 45 degrees to highlight the displacement shadows
        sun.rotation_euler = (math.radians(45), 0, math.radians(45))
        
        # Restore active object back to the plane
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

    return f"Created '{object_name}' with True Displacement (Cycles enabled, {subdiv_levels} subsurf levels)."
