def create_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjected_Part",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.3, 0.4, 0.5),
    **kwargs,
) -> str:
    """
    Create a complex hard-surface part with a seamless Triplanar (Box Projected) material.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base tint for the metal.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    # 1. Ensure Scene
    scene = bpy.data.scenes.get(scene_name)
    if not scene:
        scene = bpy.context.scene

    # 2. Generate Base Geometry (Stepped Cylinder via Spin)
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    
    # Profile coordinates for the stepped shape
    verts = [
        (0, 0, 0),         # Center bottom
        (1.0, 0, 0),       # Base outer
        (1.0, 0, 0.5),     # Base top
        (0.6, 0, 0.5),     # Mid outer
        (0.6, 0, 1.0),     # Mid top
        (0.3, 0, 1.0),     # Top outer
        (0.3, 0, 1.5),     # Top highest
        (0, 0, 1.5)        # Center top
    ]
    bverts = [bm.verts.new(v) for v in verts]
    for i in range(len(bverts) - 1):
        bm.edges.new((bverts[i], bverts[i+1]))

    geom = bm.verts[:] + bm.edges[:]
    
    # Spin profile 360 degrees
    bmesh.ops.spin(
        bm, 
        geom=geom, 
        angle=2 * math.pi, 
        steps=32, 
        axis=(0, 0, 1), 
        cent=(0, 0, 0)
    )
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)

    bm.to_mesh(mesh)
    bm.free()

    # Smooth shading
    for poly in mesh.polygons:
        poly.use_smooth = True

    # 3. Add Hard-Surface Modifiers
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(30)
    bevel.width = 0.04
    bevel.segments = 3

    subsurf = obj.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # 4. Build the Box Projected Material
    mat = bpy.data.materials.new(name=f"{object_name}_TriplanarMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Material Output & BSDF
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1200, 0)

    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (900, 0)
    links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])

    # Coordinates
    tc_node = nodes.new('ShaderNodeTexCoord')
    tc_node.location = (0, 0)

    map_node = nodes.new('ShaderNodeMapping')
    map_node.location = (200, 0)
    map_node.inputs['Scale'].default_value = (3.0, 3.0, 3.0)  # Scale down texture
    links.new(tc_node.outputs['Object'], map_node.inputs['Vector'])

    # -- THE CORE SKILL: Box Projected Image Texture --
    img_node = nodes.new('ShaderNodeTexImage')
    img_node.location = (450, 200)
    
    img_node.projection = 'BOX'            # Crucial: Triplanar projection
    img_node.projection_blend = 0.25       # Crucial: Blends the corners to hide seams

    # Create an internal generated image (Color Grid) to prove the projection works without UVs
    img_name = "Generated_ColorGrid"
    if img_name not in bpy.data.images:
        img = bpy.data.images.new(img_name, width=1024, height=1024, alpha=False)
        img.generated_type = 'COLOR_GRID'
    else:
        img = bpy.data.images[img_name]
    img_node.image = img

    links.new(map_node.outputs['Vector'], img_node.inputs['Vector'])

    # Mix grid with user color
    mix_color = nodes.new('ShaderNodeMix')
    mix_color.data_type = 'RGBA'
    mix_color.blend_type = 'MULTIPLY'
    mix_color.location = (700, 200)
    mix_color.inputs[0].default_value = 0.85
    mix_color.inputs[6].default_value = (*material_color, 1.0)
    
    links.new(img_node.outputs['Color'], mix_color.inputs[7])
    links.new(mix_color.outputs['Result'], bsdf_node.inputs['Base Color'])

    # Add procedural PBR details (Rust/Grunge emulation)
    noise_node = nodes.new('ShaderNodeTexNoise')
    noise_node.location = (450, -150)
    noise_node.inputs['Scale'].default_value = 15.0
    noise_node.inputs['Detail'].default_value = 10.0
    links.new(map_node.outputs['Vector'], noise_node.inputs['Vector'])

    roughness_ramp = nodes.new('ShaderNodeValToRGB')
    roughness_ramp.location = (650, -150)
    roughness_ramp.color_ramp.elements[0].position = 0.4
    roughness_ramp.color_ramp.elements[1].position = 0.7
    roughness_ramp.color_ramp.elements[0].color = (0.2, 0.2, 0.2, 1.0)
    roughness_ramp.color_ramp.elements[1].color = (0.8, 0.8, 0.8, 1.0)
    links.new(noise_node.outputs['Fac'], roughness_ramp.inputs['Fac'])
    links.new(roughness_ramp.outputs['Color'], bsdf_node.inputs['Roughness'])

    bump_node = nodes.new('ShaderNodeBump')
    bump_node.location = (650, -450)
    bump_node.inputs['Distance'].default_value = 0.05
    links.new(noise_node.outputs['Fac'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], bsdf_node.inputs['Normal'])

    bsdf_node.inputs['Metallic'].default_value = 0.6

    obj.data.materials.append(mat)

    # 5. Position & Scale
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' with Box Projected UV-less Material at {location}"
