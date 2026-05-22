def create_object(
    scene_name: str = "Scene",
    object_name: str = "TriplanarMechanicalPart",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.3, 0.05),
    blend_amount: float = 0.25,
    **kwargs,
) -> str:
    """
    Create a complex mechanical shape textured with seamless Box Projection.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) color used to tint the projection grid.
        blend_amount: How softly the X/Y/Z projections blend at the seams (0.0 to 1.0).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Procedurally Generate Complex Geometry ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    
    # Base flange
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=48, radius1=1.5, radius2=1.5, depth=0.2)
    
    # Find the single top n-gon face
    top_face = next(f for f in bm.faces if f.normal.z > 0.9)
    
    # Inset and extrude up (Base Pedestal)
    ret = bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.4, depth=0.0)
    top_face = ret['faces'][0]
    ret = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    top_face = ret['faces'][0]
    bmesh.ops.translate(bm, vec=(0, 0, 0.4), verts=top_face.verts)
    
    # Inset and extrude DOWN (Inner Cup)
    ret = bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3, depth=0.0)
    top_face = ret['faces'][0]
    ret = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    top_face = ret['faces'][0]
    bmesh.ops.translate(bm, vec=(0, 0, -0.3), verts=top_face.verts)
    
    # Inset and extrude UP (Center Pin)
    ret = bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.15, depth=0.0)
    top_face = ret['faces'][0]
    ret = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    top_face = ret['faces'][0]
    bmesh.ops.translate(bm, vec=(0, 0, 0.5), verts=top_face.verts)
    
    bm.to_mesh(mesh)
    bm.free()

    # Smooth shading
    for poly in mesh.polygons:
        poly.use_smooth = True

    # Add Modifiers for hard-surface finish
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(40)
    bevel.segments = 2
    bevel.width = 0.04

    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # === Step 2: Build the Box Projection Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_BoxProj_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Output & Shader
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (1000, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (700, 0)
    bsdf.inputs['Metallic'].default_value = 0.7
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Coordinate mapping: Crucial for Triplanar mapping
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-400, 0)
    mapping.inputs['Scale'].default_value = (3.0, 3.0, 3.0) # Scale texture to make it obvious
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # Generate a visual proxy image (Color Grid) to clearly show the projection working
    img_name = "BoxProj_Demo_Grid"
    img = bpy.data.images.get(img_name)
    if not img:
        img = bpy.data.images.new(name=img_name, width=1024, height=1024, alpha=False, generated_type='COLOR_GRID')

    # The Core Skill: Box Projected Image Texture
    img_tex = nodes.new('ShaderNodeTexImage')
    img_tex.location = (-100, 0)
    img_tex.image = img
    img_tex.projection = 'BOX'                  # Set to Box Projection
    img_tex.projection_blend = blend_amount     # Blend the seams
    links.new(mapping.outputs['Vector'], img_tex.inputs['Vector'])

    # Tint the grid with the requested material color
    mix = nodes.new('ShaderNodeMixRGB')
    mix.location = (300, 100)
    mix.blend_type = 'MULTIPLY'
    mix.inputs['Fac'].default_value = 1.0
    mix.inputs['Color1'].default_value = (*material_color, 1.0)
    links.new(img_tex.outputs['Color'], mix.inputs['Color2'])
    links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])

    # Use the grid data to drive roughness and bump for a realistic PBR feel
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (300, -150)
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (0.2, 0.2, 0.2, 1)
    ramp.color_ramp.elements[1].position = 1.0
    ramp.color_ramp.elements[1].color = (0.6, 0.6, 0.6, 1)
    links.new(img_tex.outputs['Color'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], bsdf.inputs['Roughness'])

    bump = nodes.new('ShaderNodeBump')
    bump.location = (300, -400)
    bump.inputs['Strength'].default_value = 0.3
    links.new(img_tex.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    # Assign material to object
    obj.data.materials.append(mat)

    # === Step 3: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' demonstrating Box Projection with {blend_amount} seam blending."
