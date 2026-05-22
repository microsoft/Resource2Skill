def create_object(
    scene_name: str = "Scene",
    object_name: str = "Triplanar_Prop",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 0.8),
    **kwargs,
) -> str:
    """
    Create a complex stepped prop with a seamless Box Projected (Triplanar) material.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base tint for the projection.

    Returns:
        Status string detailing creation.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry via BMesh Profile Spinning ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()

    # Define a profile for a stepped mechanical cylinder
    radii = [1.0, 0.7, 0.35]
    heights = [0.2, 0.25, 0.3]
    segments = 32

    v_profile = []
    v_profile.append(bm.verts.new((0, 0, 0)))
    z = 0
    for r, h in zip(radii, heights):
        v_profile.append(bm.verts.new((r, 0, z)))
        z += h
        v_profile.append(bm.verts.new((r, 0, z)))
    v_profile.append(bm.verts.new((0, 0, z)))

    edges = []
    for i in range(len(v_profile) - 1):
        edges.append(bm.edges.new((v_profile[i], v_profile[i + 1])))

    # Spin profile to create a continuous 3D shape
    geom = v_profile + edges
    bmesh.ops.spin(
        bm,
        geom=geom,
        cent=(0, 0, 0),
        axis=(0, 0, 1),
        dvec=(0, 0, 0),
        angle=2 * math.pi,
        steps=segments,
        use_duplicate=False
    )
    
    # Clean up spin artifacts
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    
    bm.to_mesh(mesh)
    bm.free()

    # Apply smooth shading to the polygons
    for poly in mesh.polygons:
        poly.use_smooth = True

    # Add Modifiers for surface detailing
    mod_bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    mod_bevel.limit_method = 'ANGLE'
    mod_bevel.angle_limit = 0.5  # approx 28 degrees
    mod_bevel.segments = 3
    mod_bevel.width = 0.02

    mod_subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    mod_subdiv.levels = 2
    mod_subdiv.render_levels = 2

    # === Step 2: Build Triplanar (Box) Projection Material ===
    mat = bpy.data.materials.new(name=object_name + "_TriplanarMat")
    mat.use_nodes = True
    obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Output & BSDF Nodes
    node_output = nodes.new('ShaderNodeOutputMaterial')
    node_output.location = (1200, 0)

    node_principled = nodes.new('ShaderNodeBsdfPrincipled')
    node_principled.location = (900, 0)
    node_principled.inputs['Roughness'].default_value = 0.6

    # Create a built-in generated Image to visualize the projection wrapping
    img_name = "Triplanar_TestGrid"
    if img_name in bpy.data.images:
        img = bpy.data.images[img_name]
    else:
        img = bpy.data.images.new(name=img_name, width=1024, height=1024)
        img.generated_type = 'COLOR_GRID'

    # --- CRITICAL SKILL: Box Projection Texture Node ---
    node_tex = nodes.new('ShaderNodeTexImage')
    node_tex.location = (300, 0)
    node_tex.image = img
    node_tex.projection = 'BOX'            # Transforms mapping to Triplanar
    node_tex.projection_blend = 0.25       # Softens the seams between orthogonal faces
    # ---------------------------------------------------

    # Coordinate and Mapping Nodes
    node_mapping = nodes.new('ShaderNodeMapping')
    node_mapping.location = (100, 0)
    node_mapping.inputs['Scale'].default_value = (2.0, 2.0, 2.0)

    node_tex_coord = nodes.new('ShaderNodeTexCoord')
    node_tex_coord.location = (-100, 0)

    # Tint the grid with the parameterized material color
    if bpy.app.version >= (3, 4, 0):
        node_mix = nodes.new('ShaderNodeMix')
        node_mix.data_type = 'RGBA'
        node_mix.blend_type = 'MULTIPLY'
        node_mix.inputs[0].default_value = 0.8  # Factor
        node_mix.inputs[6].default_value = (*material_color, 1.0)  # Input A
        links.new(node_tex.outputs['Color'], node_mix.inputs[7])   # Input B
        mix_out = node_mix.outputs[2]
    else:
        node_mix = nodes.new('ShaderNodeMixRGB')
        node_mix.blend_type = 'MULTIPLY'
        node_mix.inputs['Fac'].default_value = 0.8
        node_mix.inputs['Color1'].default_value = (*material_color, 1.0)
        links.new(node_tex.outputs['Color'], node_mix.inputs['Color2'])
        mix_out = node_mix.outputs['Color']
        
    node_mix.location = (600, 100)

    # Connect the flow
    links.new(node_tex_coord.outputs['Object'], node_mapping.inputs['Vector'])
    links.new(node_mapping.outputs['Vector'], node_tex.inputs['Vector'])
    links.new(mix_out, node_principled.inputs['Base Color'])
    links.new(node_principled.outputs['BSDF'], node_output.inputs['Surface'])

    # === Step 3: Final Placement ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' with seamless Box Projected texturing at {location}"
