def create_object(
    scene_name: str = "Scene",
    object_name: str = "ClearGlassCup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.95, 0.95, 0.95),
    **kwargs,
) -> str:
    """
    Create a Custom Clear Glass Material applied to a procedural cup mesh.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base tint of the glass in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import bpy
    import bmesh
    from mathutils import Vector, Matrix

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (Procedural Cup) ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    # Create tapered cylinder, shift up so base rests at local Z=0
    matrix = Matrix.Translation((0, 0, 1.0))
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=32,
        radius1=0.7,  # Base radius
        radius2=1.0,  # Top radius
        depth=2.0,
        matrix=matrix
    )
    
    # Delete the top face to hollow it out
    top_faces = [f for f in bm.faces if f.calc_center_median().z > 1.9]
    bmesh.ops.delete(bm, geom=top_faces, context='FACES')

    # Add edge crease to the bottom face to keep it flat during subdivision
    bottom_faces = [f for f in bm.faces if f.calc_center_median().z < 0.1]
    if bottom_faces:
        crease_layer = bm.edges.layers.crease.verify()
        for e in bottom_faces[0].edges:
            e[crease_layer] = 1.0

    bm.to_mesh(mesh)
    bm.free()

    # Apply smooth shading to polygons
    for poly in mesh.polygons:
        poly.use_smooth = True

    # Add Modifiers for physical glass thickness and smooth curves
    solidify = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = 0.08
    solidify.offset = 0.0  # Expand evenly

    subsurf = obj.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 3

    # === Step 2: Build Material (Custom Clear Glass Nodes) ===
    mat = bpy.data.materials.new(name="ClearGlassMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes (Removes Principled BSDF)
    for node in nodes:
        nodes.remove(node)

    # Output Node
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (300, 0)

    # Mix Shader
    mix_node = nodes.new(type='ShaderNodeMixShader')
    mix_node.location = (100, 0)

    # Refraction BSDF (Handles straight-on transparency)
    refraction_node = nodes.new(type='ShaderNodeBsdfRefraction')
    refraction_node.location = (-100, 100)
    refraction_node.inputs['Color'].default_value = (*material_color, 1.0)
    refraction_node.inputs['Roughness'].default_value = 0.0
    refraction_node.inputs['IOR'].default_value = 1.5

    # Glossy BSDF (Handles grazing-angle reflections)
    glossy_node = nodes.new(type='ShaderNodeBsdfGlossy')
    glossy_node.location = (-100, -100)
    glossy_node.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0) # Reflections remain white
    glossy_node.inputs['Roughness'].default_value = 0.0

    # Fresnel Node (Drives the Mix Factor based on view angle)
    fresnel_node = nodes.new(type='ShaderNodeFresnel')
    fresnel_node.location = (-100, 300)
    fresnel_node.inputs['IOR'].default_value = 1.5

    # Connect Nodes
    # NOTE: Refraction goes into Top Socket (1), Glossy into Bottom Socket (2)
    links.new(fresnel_node.outputs['Fac'], mix_node.inputs[0])
    links.new(refraction_node.outputs['BSDF'], mix_node.inputs[1])
    links.new(glossy_node.outputs['BSDF'], mix_node.inputs[2])
    links.new(mix_node.outputs['Shader'], out_node.inputs['Surface'])

    # Enable EEVEE transparency settings (acts as a fallback, though Cycles is intended)
    try:
        mat.use_screen_refraction = True
        mat.blend_method = 'HASHED'
    except AttributeError:
        pass

    obj.data.materials.append(mat)

    # === Step 3: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' (Clear Glass Cup) at {location}"
