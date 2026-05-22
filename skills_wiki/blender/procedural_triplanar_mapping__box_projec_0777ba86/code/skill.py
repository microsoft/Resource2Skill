def create_object(
    scene_name: str = "Scene",
    object_name: str = "Triplanar_Stepped_Part",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.35, 0.1), # Rusty orange base
    **kwargs,
) -> str:
    """
    Create a complex stepped cylinder using Box-Projected (Triplanar) materials.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color tint in 0-1 range.
        **kwargs: Additional overrides.
        
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector
    
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Create Base Geometry ===
    mesh = bpy.data.meshes.new(f"{object_name}_mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    bm = bmesh.new()
    
    # Create base flat cylinder
    bmesh.ops.create_cone(
        bm, 
        cap_ends=True, 
        cap_tris=False, 
        segments=32, 
        radius1=1.0, 
        radius2=1.0, 
        depth=0.3
    )
    
    # Helper to find the top-most face
    def get_top_face(b_mesh):
        return max(b_mesh.faces, key=lambda f: f.calc_center_median().z)
    
    # Operation 1: Inset and Extrude UP
    top_face = get_top_face(bm)
    inset_1 = bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.25, use_even_offset=True)
    top_face = inset_1['faces'][0]
    
    extrude_1 = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    top_face = extrude_1['faces'][0]
    bmesh.ops.translate(bm, vec=(0, 0, 0.4), verts=top_face.verts)
    
    # Operation 2: Inset and Extrude UP again
    inset_2 = bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.15, use_even_offset=True)
    top_face = inset_2['faces'][0]
    
    extrude_2 = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    top_face = extrude_2['faces'][0]
    bmesh.ops.translate(bm, vec=(0, 0, 0.3), verts=top_face.verts)
    
    # Operation 3: Inset and Extrude DOWN (creating a hole)
    inset_3 = bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.15, use_even_offset=True)
    top_face = inset_3['faces'][0]
    
    extrude_3 = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    top_face = extrude_3['faces'][0]
    bmesh.ops.translate(bm, vec=(0, 0, -0.6), verts=top_face.verts)
    
    bm.to_mesh(mesh)
    bm.free()
    
    # === Step 2: Add Modifiers ===
    # Bevel modifier (limit by angle) replaces manual Ctrl+B from tutorial
    bevel = obj.modifiers.new(name="Edge Bevel", type='BEVEL')
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(35)
    bevel.segments = 2
    bevel.width = 0.04
    
    # Subsurf to smooth out the cylinder walls and bevels
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 3
    subsurf.render_levels = 3
    
    # Smooth shading
    for poly in mesh.polygons:
        poly.use_smooth = True
        
    # === Step 3: Build Triplanar (Box-Projected) Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_TriplanarMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clean default nodes
    for node in nodes:
        nodes.remove(node)
        
    # Create Material Output and BSDF
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1200, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (800, 0)
    bsdf.inputs['Roughness'].default_value = 0.7
    bsdf.inputs['Metallic'].default_value = 0.8  # Make it look like metal
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])
    
    # Texture Coordinates and Mapping
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-200, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (0, 0)
    # The crucial step: use 'Object' coords so it scales uniformly in 3D space
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    
    # Image Texture with Box Mapping
    img_tex = nodes.new('ShaderNodeTexImage')
    img_tex.location = (200, 0)
    # CORE TUTORIAL SKILL: Set to Box projection, and increase blend
    img_tex.projection = 'BOX'
    img_tex.projection_blend = 0.25
    links.new(mapping.outputs['Vector'], img_tex.inputs['Vector'])
    
    # Generate a procedural testing image to prove the projection works
    img_name = "Triplanar_Test_Grid"
    img = bpy.data.images.get(img_name)
    if not img:
        img = bpy.data.images.new(img_name, width=1024, height=1024, alpha=False)
        img.generated_type = 'COLOR_GRID'
    img_tex.image = img
    
    # Tint the grid with the requested material color (Version-agnostic math)
    color_val = nodes.new('ShaderNodeRGB')
    color_val.outputs[0].default_value = (*material_color, 1.0)
    color_val.location = (200, -300)
    
    multiply = nodes.new('ShaderNodeVectorMath')
    multiply.operation = 'MULTIPLY'
    multiply.location = (500, 0)
    links.new(img_tex.outputs['Color'], multiply.inputs[0])
    links.new(color_val.outputs['Color'], multiply.inputs[1])
    
    # Link tinted result to Base Color
    links.new(multiply.outputs['Vector'], bsdf.inputs['Base Color'])
    
    obj.data.materials.append(mat)
    
    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    return f"Created '{obj.name}' at {location} with Box-Projected material."
