def create_object(
    scene_name: str = "Scene",
    object_name: str = "Triplanar_Machined_Part",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.3, 0.1),
    **kwargs,
) -> str:
    """
    Create a complex multi-tiered cylinder demonstrating UV-less Box Projection Texturing.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color mapping for the procedural grid.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    # Get target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (Multi-tiered Cylinder) ===
    mesh = bpy.data.meshes.new(object_name)
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    
    # Create base disc
    bmesh.ops.create_cone(
        bm, 
        cap_ends=True, 
        cap_tris=False, 
        segments=32, 
        radius1=1.0, 
        radius2=1.0, 
        depth=0.3
    )

    bm.faces.ensure_lookup_table()
    # Find the top face (positive Z normal)
    top_faces = [f for f in bm.faces if f.normal.z > 0.9]
    top_face = max(top_faces, key=lambda f: f.calc_center_bounds().z)

    # Inset and extrude up (inner ring)
    ret = bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3)
    new_faces = [f for f in ret['faces'] if f.is_valid]
    inner_face = new_faces[0]

    ret = bmesh.ops.extrude_discrete_faces(bm, faces=[inner_face])
    extruded_face = ret['faces'][0]
    bmesh.ops.translate(bm, verts=extruded_face.verts, vec=(0, 0, 0.4))

    # Inset and extrude down (center well)
    ret = bmesh.ops.inset_region(bm, faces=[extruded_face], thickness=0.25)
    center_face = ret['faces'][0]

    ret = bmesh.ops.extrude_discrete_faces(bm, faces=[center_face])
    extruded_center = ret['faces'][0]
    bmesh.ops.translate(bm, verts=extruded_center.verts, vec=(0, 0, -0.3))

    bm.to_mesh(mesh)
    bm.free()

    # Shade smooth
    for poly in mesh.polygons:
        poly.use_smooth = True

    # === Step 2: Modifiers (Sharpen & Smooth) ===
    # Bevel to catch sharp edges
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.segments = 3
    bevel.width = 0.03
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = 0.52 # ~30 degrees

    # Subdivision Surface for smooth curves
    subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.levels = 2
    subdiv.render_levels = 2

    # === Step 3: Material & Box Projection Node Tree ===
    mat = bpy.data.materials.new(name=f"{object_name}_BoxProj_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # PBR Shader setup
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (300, 0)
    
    out = nodes.new(type='ShaderNodeOutputMaterial')
    out.location = (600, 0)
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])

    # Coordinates
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)

    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-400, 0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # Generate internal test image to visualize the projection
    img_name = "BoxProj_TestGrid"
    img = bpy.data.images.get(img_name)
    if not img:
        img = bpy.data.images.new(img_name, width=1024, height=1024, alpha=False, float_buffer=False, generated_type='UV_GRID')

    # The Core Skill: Image Texture with BOX projection and BLEND
    img_tex = nodes.new(type='ShaderNodeTexImage')
    img_tex.location = (-150, 0)
    img_tex.image = img
    img_tex.projection = 'BOX'
    img_tex.projection_blend = 0.25 # Blends the XYZ projection seams
    links.new(mapping.outputs['Vector'], img_tex.inputs['Vector'])

    # ColorRamp to tint the grid with the function's material_color
    ramp_color = nodes.new(type='ShaderNodeValToRGB')
    ramp_color.location = (50, 50)
    ramp_color.color_ramp.elements[0].color = (0.05, 0.05, 0.05, 1.0)
    ramp_color.color_ramp.elements[1].color = (*material_color, 1.0)
    links.new(img_tex.outputs['Color'], ramp_color.inputs['Fac'])
    links.new(ramp_color.outputs['Color'], bsdf.inputs['Base Color'])
    
    # ColorRamp for Roughness variation based on the texture
    ramp_rough = nodes.new(type='ShaderNodeValToRGB')
    ramp_rough.location = (50, -200)
    ramp_rough.color_ramp.elements[0].position = 0.2
    ramp_rough.color_ramp.elements[0].color = (0.3, 0.3, 0.3, 1)
    ramp_rough.color_ramp.elements[1].position = 0.8
    ramp_rough.color_ramp.elements[1].color = (0.7, 0.7, 0.7, 1)
    links.new(img_tex.outputs['Color'], ramp_rough.inputs['Fac'])
    links.new(ramp_rough.outputs['Color'], bsdf.inputs['Roughness'])

    obj.data.materials.append(mat)

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    return f"Created '{object_name}' with Box Projection Triplanar Material at {location}."
