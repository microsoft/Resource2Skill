def create_pbr_displacement_plane(
    scene_name: str = "Scene",
    object_name: str = "DisplacedRockPlane",
    location: tuple = (0, 0, 0),
    scale: float = 2.0,
    material_color: tuple = (0.5, 0.4, 0.3),
    **kwargs
) -> str:
    """
    Create a heavily subdivided plane with a True Displacement PBR material in Cycles.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the plane.
        material_color: (R, G, B) base color for the procedural rock.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Render Engine Setup ===
    # True displacement requires Cycles.
    scene.render.engine = 'CYCLES'

    # === Step 2: Create Base Geometry ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # Create a simple 2x2m plane
    verts = [(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)]
    faces = [(0, 1, 2, 3)]
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # Add heavy subdivision (8 levels = 65,536 faces) to provide density for displacement
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 8
    subsurf.render_levels = 8

    # === Step 3: Build Procedural PBR Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Material")
    mat.use_nodes = True
    # CRITICAL: Tell Cycles to use True Displacement instead of Bump
    mat.cycles.displacement_method = 'DISPLACEMENT' 
    obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Output Nodes
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (400, 0)

    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf_node.location = (0, 0)

    disp_node = nodes.new(type='ShaderNodeDisplacement')
    disp_node.location = (0, -300)
    disp_node.inputs['Midlevel'].default_value = 0.5
    disp_node.inputs['Scale'].default_value = 0.15 # Keep displacement reasonable

    # Procedural Rock Pattern Generation (Replacing external textures)
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-1200, -300)

    # Distort the Voronoi vectors using noise to make cracks look natural
    noise_distort = nodes.new(type='ShaderNodeTexNoise')
    noise_distort.location = (-1000, -300)
    noise_distort.inputs['Scale'].default_value = 2.0

    math_scale = nodes.new(type='ShaderNodeVectorMath')
    math_scale.operation = 'MULTIPLY'
    math_scale.location = (-800, -100)
    math_scale.inputs[1].default_value = (0.2, 0.2, 0.2)

    math_add = nodes.new(type='ShaderNodeVectorMath')
    math_add.operation = 'ADD'
    math_add.location = (-800, -300)

    voronoi = nodes.new(type='ShaderNodeTexVoronoi')
    voronoi.location = (-600, -300)
    voronoi.feature = 'DISTANCE_TO_EDGE'
    voronoi.inputs['Scale'].default_value = 5.0

    # Shape the rock height profile (deep narrow cracks, flat tops)
    ramp_disp = nodes.new(type='ShaderNodeValToRGB')
    ramp_disp.location = (-300, -300)
    ramp_disp.color_ramp.elements[0].position = 0.0
    ramp_disp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    ramp_disp.color_ramp.elements[1].position = 1.0
    ramp_disp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    el = ramp_disp.color_ramp.elements.new(0.1) # Create sharp rise
    el.color = (0.8, 0.8, 0.8, 1.0)

    # Color Map Generation
    noise_color = nodes.new(type='ShaderNodeTexNoise')
    noise_color.location = (-600, 100)
    noise_color.inputs['Scale'].default_value = 20.0

    ramp_color = nodes.new(type='ShaderNodeValToRGB')
    ramp_color.location = (-300, 100)
    ramp_color.color_ramp.elements[0].position = 0.4
    ramp_color.color_ramp.elements[0].color = (material_color[0]*0.5, material_color[1]*0.5, material_color[2]*0.5, 1.0)
    ramp_color.color_ramp.elements[1].position = 0.6
    ramp_color.color_ramp.elements[1].color = (material_color[0], material_color[1], material_color[2], 1.0)

    # Roughness Map Generation
    ramp_rough = nodes.new(type='ShaderNodeValToRGB')
    ramp_rough.location = (-300, -50)
    ramp_rough.color_ramp.elements[0].position = 0.0
    ramp_rough.color_ramp.elements[0].color = (0.6, 0.6, 0.6, 1.0)
    ramp_rough.color_ramp.elements[1].position = 1.0
    ramp_rough.color_ramp.elements[1].color = (0.9, 0.9, 0.9, 1.0)

    # Wiring the Nodes
    links.new(tex_coord.outputs['Object'], math_add.inputs[0])
    links.new(noise_distort.outputs['Color'], math_scale.inputs[0])
    links.new(math_scale.outputs['Vector'], math_add.inputs[1])
    links.new(math_add.outputs['Vector'], voronoi.inputs['Vector'])

    links.new(voronoi.outputs['Distance'], ramp_disp.inputs['Fac'])
    links.new(ramp_disp.outputs['Color'], disp_node.inputs['Height'])

    links.new(noise_color.outputs['Fac'], ramp_color.inputs['Fac'])
    links.new(ramp_color.outputs['Color'], bsdf_node.inputs['Base Color'])

    links.new(noise_color.outputs['Fac'], ramp_rough.inputs['Fac'])
    links.new(ramp_rough.outputs['Color'], bsdf_node.inputs['Roughness'])

    links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])
    links.new(disp_node.outputs['Displacement'], out_node.inputs['Displacement'])

    # === Step 4: Lighting Context ===
    # Add a Sun light to cast strong shadows and reveal the displacement (from tutorial)
    light_data = bpy.data.lights.new(name=f"{object_name}_Sun", type='SUN')
    light_data.energy = 5.0 
    light_data.angle = math.radians(11.4)
    light_obj = bpy.data.objects.new(name=f"{object_name}_SunLight", object_data=light_data)
    scene.collection.objects.link(light_obj)
    
    light_obj.location = (location[0], location[1], location[2] + 10.0)
    # Angle the sun to graze the surface and cast shadows into the displaced crevices
    light_obj.rotation_euler = (math.radians(45), math.radians(30), 0)

    return f"Created PBR Displaced Plane '{object_name}' with True Displacement and directional Sun lighting."
