def create_pbr_material_setup(
    scene_name: str = "Scene",
    object_name: str = "PBR_Displaced_Surface",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a PBR material setup demonstrating true displacement, inverted gloss maps, 
    and texture tweaking nodes, applied to a subdivided plane.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created plane.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color in 0-1 range.

    Returns:
        Status string.
    """
    import bpy

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # Subdivide base mesh to give the displacement modifier geometry to work with
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=20)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Enable Cycles and Experimental Features for Adaptive Subdivision
    scene.render.engine = 'CYCLES'
    try:
        scene.cycles.feature_set = 'EXPERIMENTAL'
    except AttributeError:
        pass # Fallback safety for differing API versions

    # Add Subdivision Surface Modifier
    mod = obj.modifiers.new(name="Adaptive_Subsurf", type='SUBSURF')
    mod.subdivision_type = 'SIMPLE' # Prevent rounding the sharp corners of the plane
    if hasattr(mod, 'use_adaptive_subdivision'):
        mod.use_adaptive_subdivision = True

    # === Step 2: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_PBR_Mat")
    mat.use_nodes = True
    
    # Enable true displacement in material settings
    if hasattr(mat, 'cycles'):
        mat.cycles.displacement_method = 'DISPLACEMENT'
    
    obj.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Core output and shader
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1200, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (800, 0)
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])
    
    # Texture Coordinate & Mapping
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    mapping.inputs['Scale'].default_value = (2.0, 2.0, 2.0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    
    # Procedural texture simulating a PBR image source
    # Note: If using Image Textures, Normal/Roughness/Displacement nodes require Color Space = 'Non-Color'
    base_tex = nodes.new('ShaderNodeTexNoise')
    base_tex.location = (-400, 0)
    base_tex.inputs['Scale'].default_value = 10.0
    base_tex.inputs['Detail'].default_value = 15.0
    links.new(mapping.outputs['Vector'], base_tex.inputs['Vector'])
    
    # Base Color Path (with tweaking nodes: RGB Curves & Hue/Saturation)
    color_ramp_color = nodes.new('ShaderNodeValToRGB')
    color_ramp_color.location = (-150, 300)
    color_ramp_color.color_ramp.elements[0].color = (material_color[0]*0.2, material_color[1]*0.2, material_color[2]*0.2, 1.0)
    color_ramp_color.color_ramp.elements[1].color = (material_color[0], material_color[1], material_color[2], 1.0)
    
    rgb_curves = nodes.new('ShaderNodeRGBCurve')
    rgb_curves.location = (150, 300)
    
    hue_sat = nodes.new('ShaderNodeHueSaturation')
    hue_sat.location = (450, 300)
    hue_sat.inputs['Saturation'].default_value = 1.1
    
    links.new(base_tex.outputs['Fac'], color_ramp_color.inputs['Fac'])
    links.new(color_ramp_color.outputs['Color'], rgb_curves.inputs['Color'])
    links.new(rgb_curves.outputs['Color'], hue_sat.inputs['Color'])
    links.new(hue_sat.outputs['Color'], bsdf.inputs['Base Color'])
    
    # Roughness Path (simulating an inverted Gloss map)
    invert = nodes.new('ShaderNodeInvert')
    invert.location = (-150, 0)
    
    rough_ramp = nodes.new('ShaderNodeValToRGB')
    rough_ramp.location = (150, 0)
    rough_ramp.color_ramp.elements[0].position = 0.2
    rough_ramp.color_ramp.elements[1].position = 0.8
    
    links.new(base_tex.outputs['Fac'], invert.inputs['Color'])
    links.new(invert.outputs['Color'], rough_ramp.inputs['Fac'])
    links.new(rough_ramp.outputs['Color'], bsdf.inputs['Roughness'])
    
    # Normal Path (using Bump to simulate height-to-normal, conceptually mapping to Normal Map behavior)
    bump = nodes.new('ShaderNodeBump')
    bump.location = (450, -300)
    bump.inputs['Strength'].default_value = 0.8
    links.new(base_tex.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    
    # True Displacement Path
    displacement = nodes.new('ShaderNodeDisplacement')
    displacement.location = (800, -300)
    displacement.inputs['Midlevel'].default_value = 0.0
    displacement.inputs['Scale'].default_value = 0.1
    links.new(base_tex.outputs['Fac'], displacement.inputs['Height'])
    links.new(displacement.outputs['Displacement'], out_node.inputs['Displacement'])
    
    # === Step 3: Finalize ===
    # Set smooth shading
    for poly in obj.data.polygons:
        poly.use_smooth = True

    return f"Created '{object_name}' at {location} with complete PBR node routing and true adaptive displacement."
