def create_box_projected_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjected_Prop",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.7, 0.7),
    **kwargs,
) -> str:
    """
    Create a complex tiered geometry and apply a Box Projected material to demonstrate 
    seamless procedural texturing without UV unwrapping.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) color used to tint the projected texture.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Mesh ===
    mesh = bpy.data.meshes.new(object_name)
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    # Create base cylinder
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=32, 
        radius1=1.0, radius2=1.0, depth=0.5
    )

    # Find the top face
    top_faces = sorted([f for f in bm.faces if f.normal.z > 0.9], key=lambda f: f.calc_center_median().z)
    if top_faces:
        top_face = top_faces[-1]

        # Tier 1
        bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3)
        ret = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
        top_face = ret['faces'][0]
        bmesh.ops.translate(bm, verts=top_face.verts, vec=(0, 0, 0.4))

        # Tier 2
        bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3)
        ret = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
        top_face = ret['faces'][0]
        bmesh.ops.translate(bm, verts=top_face.verts, vec=(0, 0, 0.4))

        # Add a side extrusion (pipe) to demonstrate non-stretched texturing on new edits
        bm.faces.ensure_lookup_table()
        side_faces = [f for f in bm.faces if abs(f.normal.z) < 0.1 and 0.1 < f.calc_center_median().z < 0.4]
        if side_faces:
            side_face = side_faces[0] # Pick one side face
            
            # Extrude outwards
            ret = bmesh.ops.extrude_discrete_faces(bm, faces=[side_face])
            pipe_face = ret['faces'][0]
            bmesh.ops.translate(bm, verts=pipe_face.verts, vec=pipe_face.normal * 0.6)
            
            # Inset to taper
            bmesh.ops.inset_region(bm, faces=[pipe_face], thickness=0.15)
            
            # Extrude again
            ret = bmesh.ops.extrude_discrete_faces(bm, faces=[pipe_face])
            pipe_face = ret['faces'][0]
            bmesh.ops.translate(bm, verts=pipe_face.verts, vec=pipe_face.normal * 0.3)

    bm.to_mesh(mesh)
    bm.free()

    # === Step 2: Modifiers for Smooth Hard-Surface Form ===
    bevel = obj.modifiers.new("Bevel", 'BEVEL')
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(35)
    bevel.segments = 3
    bevel.width = 0.03

    subsurf = obj.modifiers.new("Subdivision", 'SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # Shade smooth
    for poly in mesh.polygons:
        poly.use_smooth = True

    # === Step 3: Build Box Projection Material ===
    mat = bpy.data.materials.new(f"{object_name}_BoxMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create Material Nodes
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (300, 0)

    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (0, 0)
    links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])

    # Coordinates
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # Image Texture (The core Box Projection configuration)
    tex_img = nodes.new('ShaderNodeTexImage')
    tex_img.location = (-400, 0)
    tex_img.projection = 'BOX'            # <-- The core technique
    tex_img.projection_blend = 0.2        # <-- Blends the seams

    # Generate an internal test grid image
    img_name = "BoxProjectedGrid"
    if img_name not in bpy.data.images:
        img = bpy.data.images.new(img_name, width=1024, height=1024, alpha=False)
        img.generated_type = 'COLOR_GRID'
    else:
        img = bpy.data.images[img_name]
    
    tex_img.image = img
    links.new(mapping.outputs['Vector'], tex_img.inputs['Vector'])

    # Mix Node to tint the grid with the provided material parameter
    try:
        # Fallback for cross-version compatibility
        mix_node = nodes.new('ShaderNodeMixRGB')
        mix_node.location = (-200, 0)
        mix_node.blend_type = 'MULTIPLY'
        mix_node.inputs[0].default_value = 0.8  # Factor
        mix_node.inputs[1].default_value = (*material_color, 1.0) # Color 1
        links.new(tex_img.outputs['Color'], mix_node.inputs[2])   # Color 2
        links.new(mix_node.outputs[0], bsdf_node.inputs['Base Color'])
    except Exception:
        # Failsafe if node alias is strictly restricted in newer API
        links.new(tex_img.outputs['Color'], bsdf_node.inputs['Base Color'])

    # Assign material
    obj.data.materials.append(mat)

    # === Step 4: Positioning ===
    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))

    return f"Created '{object_name}' with Object-based Box Projection mapping. Modify the mesh to see dynamic projection."
