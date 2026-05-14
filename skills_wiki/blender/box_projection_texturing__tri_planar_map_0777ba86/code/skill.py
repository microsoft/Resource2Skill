def create_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjected_Cylinder",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.4, 0.1),
    blend_amount: float = 0.2,
    **kwargs,
) -> str:
    """
    Create a complex mechanical cylinder and apply a Box-Projected (Tri-Planar) material.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base metallic color.
        blend_amount: The amount to blend the seams of the box projection (0.0 to 1.0).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    # Get target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Create Base Geometry using BMesh ===
    mesh = bpy.data.meshes.new(name=f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    # Create base cylinder
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=32, radius1=1.0, radius2=1.0, depth=0.5
    )

    # Function to get the current highest face
    def get_top_face(b_mesh):
        b_mesh.faces.ensure_lookup_table()
        return max(b_mesh.faces, key=lambda f: f.calc_center_median().z)

    # Inset 1 (via extrude and scale)
    top_face = get_top_face(bm)
    ret = bmesh.ops.extrude_face_region(bm, geom=[top_face])
    verts = [v for v in ret['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.scale(bm, vec=(0.6, 0.6, 1.0), verts=verts)

    # Extrude Up
    top_face = get_top_face(bm)
    ret = bmesh.ops.extrude_face_region(bm, geom=[top_face])
    verts = [v for v in ret['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, 0.4), verts=verts)

    # Inset 2
    top_face = get_top_face(bm)
    ret = bmesh.ops.extrude_face_region(bm, geom=[top_face])
    verts = [v for v in ret['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.scale(bm, vec=(0.5, 0.5, 1.0), verts=verts)

    # Extrude Down (creating an inner cavity)
    top_face = get_top_face(bm)
    ret = bmesh.ops.extrude_face_region(bm, geom=[top_face])
    verts = [v for v in ret['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, -0.3), verts=verts)

    # Write back and clean up
    bm.to_mesh(mesh)
    bm.free()

    # Shade smooth
    for poly in mesh.polygons:
        poly.use_smooth = True

    # === Step 2: Add Modifiers ===
    # Bevel to catch sharp mechanical edges
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(35)
    bevel.width = 0.04
    bevel.segments = 3

    # Subdiv to smooth the overall topology
    subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.levels = 2
    subdiv.render_levels = 2

    # === Step 3: Build Box-Projected Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output and BSDF
    output = nodes.new(type="ShaderNodeOutputMaterial")
    output.location = (400, 0)
    
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.location = (100, 0)
    bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.9
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Coordinates and Mapping
    tex_coord = nodes.new(type="ShaderNodeTexCoord")
    tex_coord.location = (-800, 0)
    
    mapping = nodes.new(type="ShaderNodeMapping")
    mapping.location = (-600, 0)
    mapping.inputs['Scale'].default_value = (4.0, 4.0, 4.0) # Tile the texture
    
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # Internal Image generation to demonstrate texture projection
    img_name = "Generated_Grid_Tex"
    if img_name in bpy.data.images:
        img = bpy.data.images[img_name]
    else:
        img = bpy.data.images.new(img_name, width=1024, height=1024, alpha=False)
        img.generated_type = 'COLOR_GRID'

    # The Core Technique: Box Projection Setup
    tex_img = nodes.new(type="ShaderNodeTexImage")
    tex_img.location = (-350, 0)
    tex_img.image = img
    tex_img.projection = 'BOX'                  # Swap from Flat to Box
    tex_img.projection_blend = blend_amount     # Blend the harsh projection seams
    
    links.new(mapping.outputs['Vector'], tex_img.inputs['Vector'])

    # Apply the projected texture to physical properties (Bump & Roughness)
    bump = nodes.new(type="ShaderNodeBump")
    bump.location = (-150, -200)
    bump.inputs['Distance'].default_value = 0.05
    
    links.new(tex_img.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(tex_img.outputs['Color'], bsdf.inputs['Roughness'])

    # Assign material
    obj.data.materials.append(mat)

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' with Box Projection Material (Blend: {blend_amount}) at {location}."
