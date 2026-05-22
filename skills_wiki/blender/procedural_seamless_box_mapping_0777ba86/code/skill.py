def create_seamless_box_mapped_object(
    scene_name: str = "Scene",
    object_name: str = "BoxMapped_Part",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.4, 0.1),
    **kwargs,
) -> str:
    """
    Creates a complex stepped cylinder and applies a seamless Box-Mapped material,
    bypassing the need for UV unwrapping.
    
    Args:
        scene_name: Target scene.
        object_name: Name of the generated object.
        location: (x, y, z) placement in the world.
        scale: Uniform scale.
        material_color: (R, G, B) tint applied to the procedural texture.
        
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Create Complex Geometry (Stepped Cylinder) via BMesh ===
    mesh = bpy.data.meshes.new(object_name)
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    bm = bmesh.new()
    
    # Base Cylinder
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=32, radius1=1.0, radius2=1.0, depth=0.4)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, 0.2))
    
    # Find top face
    top_face = next(f for f in bm.faces if f.normal.z > 0.9)
    
    # Step Tier 1: Inset and Extrude
    bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3, use_even_offset=True)
    geom_to_extrude1 = [top_face] + list(top_face.edges) + list(top_face.verts)
    ext1 = bmesh.ops.extrude_face_region(bm, geom=geom_to_extrude1)
    ext_verts1 = [ele for ele in ext1['geom'] if isinstance(ele, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=ext_verts1, vec=(0, 0, 0.4))
    
    # Find new top face
    top_face = next(f for f in ext1['geom'] if isinstance(f, bmesh.types.BMFace) and f.normal.z > 0.9)
    
    # Step Tier 2: Inset and Extrude
    bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3, use_even_offset=True)
    geom_to_extrude2 = [top_face] + list(top_face.edges) + list(top_face.verts)
    ext2 = bmesh.ops.extrude_face_region(bm, geom=geom_to_extrude2)
    ext_verts2 = [ele for ele in ext2['geom'] if isinstance(ele, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=ext_verts2, vec=(0, 0, 0.4))
    
    bm.to_mesh(mesh)
    bm.free()
    
    # Apply smooth shading
    for poly in mesh.polygons:
        poly.use_smooth = True
        
    # === Step 2: Add Modifiers ===
    # Bevel smooths the 90 degree corners so the Box projection can blend beautifully
    bevel = obj.modifiers.new("Bevel", 'BEVEL')
    bevel.width = 0.04
    bevel.segments = 3
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = 0.5  # ~28 degrees
    
    subsurf = obj.modifiers.new("Subsurf", 'SUBSURF')
    subsurf.levels = 2
    
    # === Step 3: Transform ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    # === Step 4: The Core Skill - Seamless Box Mapping Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_BoxMapMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (300, 0)
    bsdf.inputs['Metallic'].default_value = 0.8
    bsdf.inputs['Roughness'].default_value = 0.35
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    # Coordinates mapping
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-700, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-500, 0)
    mapping.inputs['Scale'].default_value = (2.0, 2.0, 2.0)
    
    # Image Texture with Box Mapping
    tex_img = nodes.new('ShaderNodeTexImage')
    tex_img.location = (-300, 0)
    
    # *** CORE TECHNIQUE APPLIED HERE ***
    tex_img.projection = 'BOX'
    tex_img.projection_blend = 0.25
    
    # Generate an internal test grid image to project (bypassing external files)
    img_name = f"{object_name}_DemoGrid"
    img = bpy.data.images.get(img_name)
    if not img:
        img = bpy.data.images.new(img_name, width=1024, height=1024)
        img.source = 'GENERATED'
        img.generated_type = 'COLOR_GRID'
    tex_img.image = img
    
    # Vector Math (Multiply) to tint the generated grid with our parameter color
    vec_math = nodes.new('ShaderNodeVectorMath')
    vec_math.location = (-50, 0)
    vec_math.operation = 'MULTIPLY'
    vec_math.inputs[1].default_value = (*material_color, 1.0)
    
    # Connect everything
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], tex_img.inputs['Vector'])
    links.new(tex_img.outputs['Color'], vec_math.inputs[0])
    links.new(vec_math.outputs['Vector'], bsdf.inputs['Base Color'])
    
    obj.data.materials.append(mat)
    
    return f"Created '{obj.name}' utilizing seamless Box Mapping projection at {location}."
