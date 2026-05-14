def create_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjected_Part",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.25, 0.1),
    **kwargs,
) -> str:
    """
    Create a mechanical tiered part featuring Seamless Box Projection Texturing.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color tint applied to the texture.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry using BMesh ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    
    # Create initial wide base cylinder
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, 
        segments=32, radius1=1.5, radius2=1.5, depth=0.4
    )
    
    def get_top_face(bmesh_obj):
        # Helper to consistently find the topmost flat face
        faces = [f for f in bmesh_obj.faces if f.normal.z > 0.9]
        faces.sort(key=lambda f: f.calc_center_median().z, reverse=True)
        return faces[0]

    # 1st Tier: Inset and Extrude Up
    top_face = get_top_face(bm)
    inset_result = bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.4)
    top_face = get_top_face(bm)
    extrude_result = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    top_face = extrude_result['faces'][0]
    bmesh.ops.translate(bm, verts=top_face.verts, vec=(0, 0, 0.6))

    # 2nd Tier: Inset and Extrude Down (creating a cavity)
    top_face = get_top_face(bm)
    bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3)
    top_face = get_top_face(bm)
    extrude_result = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    top_face = extrude_result['faces'][0]
    bmesh.ops.translate(bm, verts=top_face.verts, vec=(0, 0, -0.4))
    
    # 3rd Tier (Center pole): Inset and Extrude Up
    top_face = get_top_face(bm)
    bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.2)
    top_face = get_top_face(bm)
    extrude_result = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    top_face = extrude_result['faces'][0]
    bmesh.ops.translate(bm, verts=top_face.verts, vec=(0, 0, 0.5))

    bm.to_mesh(mesh)
    bm.free()

    # Shade Smooth
    for poly in mesh.polygons:
        poly.use_smooth = True

    # === Step 2: Apply Modifiers ===
    # Bevel modifier to catch the hard edges
    mod_bevel = obj.modifiers.new(name="EdgeBevel", type='BEVEL')
    mod_bevel.limit_method = 'ANGLE'
    mod_bevel.angle_limit = math.radians(35)
    mod_bevel.width = 0.03
    mod_bevel.segments = 3

    # Subdivision modifier to smooth the rounded flow
    mod_subsurf = obj.modifiers.new(name="SmoothSubdiv", type='SUBSURF')
    mod_subsurf.levels = 2
    mod_subsurf.render_levels = 3

    # === Step 3: Build the Box Projection Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_BoxProjected")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create Material Nodes
    node_out = nodes.new('ShaderNodeOutputMaterial')
    node_out.location = (1000, 0)
    
    node_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    node_bsdf.location = (700, 0)
    node_bsdf.inputs['Roughness'].default_value = 0.7
    node_bsdf.inputs['Metallic'].default_value = 0.8
    
    # Texture Coordinate (Using Object for stable projection)
    node_coord = nodes.new('ShaderNodeTexCoord')
    node_coord.location = (-400, 0)
    
    node_mapping = nodes.new('ShaderNodeMapping')
    node_mapping.location = (-200, 0)
    # Scale up texture coordinates a bit
    node_mapping.inputs['Scale'].default_value = (2.0, 2.0, 2.0)
    
    # THE CORE TECHNIQUE: Box Projection Texture
    node_tex = nodes.new('ShaderNodeTexImage')
    node_tex.location = (0, 0)
    node_tex.projection = 'BOX'
    node_tex.projection_blend = 0.25 # Blends the seams between projections
    
    # Create an internal grid texture to visually prove the technique works
    grid_img = bpy.data.images.get("BoxProject_Grid")
    if not grid_img:
        grid_img = bpy.data.images.new("BoxProject_Grid", 1024, 1024, alpha=False)
        grid_img.generated_type = 'COLOR_GRID'
    node_tex.image = grid_img
    
    # Mix node to tint the grid with the requested material color
    node_mix = nodes.new('ShaderNodeMix')
    node_mix.data_type = 'RGBA'
    node_mix.blend_type = 'MULTIPLY'
    node_mix.location = (300, 0)
    node_mix.inputs['Factor'].default_value = 0.9
    node_mix.inputs[7].default_value = (*material_color, 1.0) # Input 7 is B (second color in newer Blender versions)
    
    # Procedural Bump for rusted metal look
    node_noise = nodes.new('ShaderNodeTexNoise')
    node_noise.location = (0, -300)
    node_noise.inputs['Scale'].default_value = 15.0
    
    node_bump = nodes.new('ShaderNodeBump')
    node_bump.location = (300, -300)
    node_bump.inputs['Distance'].default_value = 0.1
    node_bump.inputs['Strength'].default_value = 0.4

    # Connect Material Links
    links.new(node_coord.outputs['Object'], node_mapping.inputs['Vector'])
    links.new(node_mapping.outputs['Vector'], node_tex.inputs['Vector'])
    
    links.new(node_tex.outputs['Color'], node_mix.inputs[6]) # Input 6 is A (first color)
    links.new(node_mix.outputs[2], node_bsdf.inputs['Base Color']) # Output 2 is Result
    
    links.new(node_mapping.outputs['Vector'], node_noise.inputs['Vector'])
    links.new(node_noise.outputs['Fac'], node_bump.inputs['Height'])
    links.new(node_bump.outputs['Normal'], node_bsdf.inputs['Normal'])
    
    links.new(node_bsdf.outputs['BSDF'], node_out.inputs['Surface'])

    # Assign Material
    obj.data.materials.append(mat)

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{obj.name}' with seamless Box-Projected material at {location}."
