def create_object(
    scene_name: str = "Scene",
    object_name: str = "Triplanar_Machined_Part",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.3, 0.1),
    **kwargs,
) -> str:
    """
    Creates a stepped mechanical cylinder with smooth beveled edges, 
    textured seamlessly using UV-less Box Projection (Triplanar mapping).

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color tint for the texture.

    Returns:
        Status string describing the created object.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry using BMesh ===
    mesh = bpy.data.meshes.new(f"{object_name}_mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    
    # Create base cylinder (Centered at origin, height = 0.4 -> Z from -0.2 to 0.2)
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=32, 
        radius1=1.0, radius2=1.0, depth=0.4
    )

    def get_top_face(bmesh_data):
        """Helper to reliably find the current highest horizontal face"""
        top_faces = [f for f in bmesh_data.faces if f.normal.z > 0.9]
        if not top_faces: return None
        return max(top_faces, key=lambda f: f.calc_center_median().z)

    top_face = get_top_face(bm)

    # Inset 1
    bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.25)
    top_face = get_top_face(bm)

    # Extrude 1
    ext = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    top_face = ext['faces'][0]
    bmesh.ops.translate(bm, vec=Vector((0, 0, 0.3)), verts=top_face.verts)

    # Inset 2
    bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.25)
    top_face = get_top_face(bm)

    # Extrude 2
    ext = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    top_face = ext['faces'][0]
    bmesh.ops.translate(bm, vec=Vector((0, 0, 0.3)), verts=top_face.verts)

    # Finalize BMesh
    bm.to_mesh(mesh)
    bm.free()

    # Enable smooth shading for all polygons
    for poly in mesh.polygons:
        poly.use_smooth = True

    # === Step 2: Add Non-Destructive Smoothing Modifiers ===
    # Bevel catches the sharp 90-degree extrusions
    bevel = obj.modifiers.new("Bevel", 'BEVEL')
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = 0.52  # Approx 30 degrees
    bevel.segments = 3
    bevel.width = 0.05

    # Subdiv perfectly rounds out the beveled cylinder
    subdiv = obj.modifiers.new("Subdivision", 'SUBSURF')
    subdiv.levels = 2
    subdiv.render_levels = 2

    # === Step 3: UV-less Triplanar Material Setup ===
    mat = bpy.data.materials.new(name=f"{object_name}_BoxProjected_Mat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Output & Shader
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (1000, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (700, 0)
    bsdf.inputs['Roughness'].default_value = 0.6

    # Mapping Coordinates
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-300, 0)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-100, 0)
    mapping.inputs['Scale'].default_value = (2.0, 2.0, 2.0)

    # Create a visible generated image to prove the projection works
    img_name = "Triplanar_Test_Grid"
    img = bpy.data.images.get(img_name)
    if not img:
        img = bpy.data.images.new(img_name, width=1024, height=1024)
        img.generated_type = 'COLOR_GRID'

    # The Core Technique: Box Projection Image Texture
    tex_image = nodes.new('ShaderNodeTexImage')
    tex_image.location = (150, 0)
    tex_image.image = img
    tex_image.projection = 'BOX'           # Triplanar mapping
    tex_image.projection_blend = 0.25      # Blends the seams

    # Tinting the texture with the function parameter (Version safe Mix node)
    if bpy.app.version >= (3, 4, 0):
        mix = nodes.new('ShaderNodeMix')
        mix.data_type = 'RGBA'
        mix.blend_type = 'MULTIPLY'
        mix.inputs[0].default_value = 0.8
        mix.inputs[6].default_value = (*material_color, 1.0)
        mix_input_b = mix.inputs[7]
        mix_output = mix.outputs[2]
    else:
        mix = nodes.new('ShaderNodeMixRGB')
        mix.blend_type = 'MULTIPLY'
        mix.inputs['Fac'].default_value = 0.8
        mix.inputs['Color1'].default_value = (*material_color, 1.0)
        mix_input_b = mix.inputs['Color2']
        mix_output = mix.outputs['Color']
    mix.location = (450, 0)

    # Bump mapping to add surface detail
    bump = nodes.new('ShaderNodeBump')
    bump.location = (450, -300)
    bump.inputs['Distance'].default_value = 0.05

    # Wire it all together
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], tex_image.inputs['Vector'])
    
    links.new(tex_image.outputs['Color'], mix_input_b)
    links.new(mix_output, bsdf.inputs['Base Color'])
    
    links.new(tex_image.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' with Box Projected material (UV-less texturing) at {location}."
