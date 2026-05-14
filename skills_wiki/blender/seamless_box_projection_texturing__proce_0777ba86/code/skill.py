def create_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjectedPart",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.4, 0.1),
    **kwargs,
) -> str:
    """
    Create a complex stepped cylinder textured using Seamless Box Projection.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor applied directly to mesh data.
        material_color: (R, G, B) color used to tint the projected grid.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector, Matrix

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry via BMesh ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    
    # Base cylinder
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=32, radius1=1.0, radius2=1.0, depth=0.4)
    
    # Find the top face (Z is positive)
    top_faces = [f for f in bm.faces if f.calc_center_median().z > 0.19]
    if top_faces:
        top_face = top_faces[0]
        
        # 1st Inset
        res = bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3, use_even_offset=True)
        # 1st Extrude (Upwards)
        res = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
        top_face = res['faces'][0]
        bmesh.ops.translate(bm, vec=(0, 0, 0.4), verts=top_face.verts)
        
        # 2nd Inset
        res = bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.25, use_even_offset=True)
        # 2nd Extrude (Downwards into the shape to make a hole)
        res = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
        top_face = res['faces'][0]
        bmesh.ops.translate(bm, vec=(0, 0, -0.3), verts=top_face.verts)

    # Apply scale directly to mesh data (crucial for accurate Box Projection)
    # The Object Transform scale remains (1,1,1) so the projection maps uniformly in world space.
    bmesh.ops.scale(bm, vec=(scale, scale, scale), verts=bm.verts)

    bm.to_mesh(mesh)
    bm.free()

    # Apply smooth shading to polygons
    for poly in obj.data.polygons:
        poly.use_smooth = True

    # === Step 2: Apply Modifiers ===
    # Bevel modifier to catch the sharp 90 degree edges
    bevel = obj.modifiers.new(name="EdgeBevel", type='BEVEL')
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = 0.52 # ~30 degrees
    bevel.width = 0.05 * scale
    bevel.segments = 3

    # Subdivision modifier to smooth the overall cylindrical shape
    subsurf = obj.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # === Step 3: Build Seamless Box Projection Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_BoxProjMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Material Output & BSDF
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1000, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (700, 0)
    bsdf.inputs['Metallic'].default_value = 0.7
    bsdf.inputs['Roughness'].default_value = 0.3
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    # Generated Image (To demonstrate Box Projection blending clearly)
    img = bpy.data.images.new(name=f"{object_name}_ColorGrid", width=1024, height=1024, alpha=False)
    img.generated_type = 'COLOR_GRID'

    # The Core Technique: Box Projection Setup
    tex_node = nodes.new('ShaderNodeTexImage')
    tex_node.image = img
    tex_node.projection = 'BOX'           # Switch from Flat to Box
    tex_node.projection_blend = 0.25      # Blend the edges seamlessly
    tex_node.location = (200, 0)

    # Coordinate Mapping
    map_node = nodes.new('ShaderNodeMapping')
    map_node.location = (0, 0)
    # Optional: Scale the texture pattern up a bit
    map_node.inputs['Scale'].default_value = (2.0, 2.0, 2.0)
    
    coord_node = nodes.new('ShaderNodeTexCoord')
    coord_node.location = (-200, 0)

    # Tint the grid with the specified material color (Robust version-agnostic Mix node)
    try:
        mix = nodes.new("ShaderNodeMix")
        mix.data_type = 'RGBA'
        mix.blend_type = 'MULTIPLY'
        mix.inputs.get("Factor", mix.inputs[0]).default_value = 1.0
        c1 = mix.inputs.get("A", mix.inputs[4])
        c2 = mix.inputs.get("B", mix.inputs[5])
        res = mix.outputs.get("Result", mix.outputs[2])
    except:
        mix = nodes.new("ShaderNodeMixRGB")
        mix.blend_type = 'MULTIPLY'
        mix.inputs[0].default_value = 1.0
        c1, c2, res = mix.inputs[1], mix.inputs[2], mix.outputs[0]

    mix.location = (500, 0)
    c1.default_value = (*material_color, 1.0)
    
    # Wire the node tree
    links.new(coord_node.outputs['Object'], map_node.inputs['Vector'])
    links.new(map_node.outputs['Vector'], tex_node.inputs['Vector'])
    links.new(tex_node.outputs['Color'], c2)
    links.new(res, bsdf.inputs['Base Color'])

    obj.data.materials.append(mat)

    # === Step 4: Position ===
    obj.location = Vector(location)

    return f"Created '{object_name}' (Box Projected) at {location}"
