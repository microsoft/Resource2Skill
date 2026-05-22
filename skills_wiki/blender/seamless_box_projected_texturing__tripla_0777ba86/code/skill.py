def create_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjected_Part",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.3, 0.1),
    **kwargs,
) -> str:
    """
    Create a complex stepped cylinder textured seamlessly using Box Projection blending.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color tint for the generated texture.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Custom 2D Image Texture ===
    # We generate a noisy grid pattern to explicitly show how Box Projection fixes seams.
    res = 128
    img_name = f"{object_name}_GridTex"
    if img_name in bpy.data.images:
        bpy.data.images.remove(bpy.data.images[img_name])
    img = bpy.data.images.new(name=img_name, width=res, height=res)
    
    pixels = [0.0] * (res * res * 4)
    r, g, b = material_color
    for i in range(res * res):
        x = i % res
        y = i // res
        
        # Create obvious grid lines every 32 pixels
        is_grid = (x % 32 == 0) or (y % 32 == 0)
        # Random noise for the rest to simulate rust/wear
        intensity = 0.15 if is_grid else random.uniform(0.5, 1.0)
        
        idx = i * 4
        pixels[idx]     = r * intensity
        pixels[idx + 1] = g * intensity
        pixels[idx + 2] = b * intensity
        pixels[idx + 3] = 1.0
        
    img.pixels = [float(p) for p in pixels]

    # === Step 2: Build Base Geometry (Stepped Cylinder) ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    # Base cylinder
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=32, radius1=1.0, radius2=1.0, depth=0.5)

    def get_top_face(bmesh_obj):
        return max(bmesh_obj.faces, key=lambda f: f.calc_center_median().z)

    top_face = get_top_face(bm)

    # Inset 1 (top_face becomes the inner smaller face)
    bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3)

    # Extrude Up
    ext = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    new_top = ext['faces'][0]
    bmesh.ops.translate(bm, vec=(0, 0, 0.5), verts=new_top.verts)

    # Inset 2
    bmesh.ops.inset_region(bm, faces=[new_top], thickness=0.2)

    # Extrude Down (create cavity)
    ext2 = bmesh.ops.extrude_discrete_faces(bm, faces=[new_top])
    cavity = ext2['faces'][0]
    bmesh.ops.translate(bm, vec=(0, 0, -0.3), verts=cavity.verts)

    # Apply scaling directly to mesh to keep object scale at (1,1,1) for perfect Object texturing
    bmesh.ops.scale(bm, vec=(scale, scale, scale), verts=bm.verts)

    bm.to_mesh(mesh)
    bm.free()

    # Shade Smooth
    for poly in mesh.polygons:
        poly.use_smooth = True

    # Modifiers for hard-surface detailing
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(45)
    bevel.width = 0.02 * scale
    bevel.segments = 3

    subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.levels = 2
    subdiv.render_levels = 2

    # === Step 3: Build Box-Projected Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1000, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (700, 0)
    bsdf.inputs['Roughness'].default_value = 0.6
    bsdf.inputs['Metallic'].default_value = 0.3
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    # The core Box Projection setup
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (0, 0)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (200, 0)

    img_tex = nodes.new('ShaderNodeTexImage')
    img_tex.location = (400, 0)
    img_tex.image = img
    
    # --- CRITICAL SKILL MECHANISM ---
    img_tex.projection = 'BOX'         # Project from X, Y, and Z axes
    img_tex.projection_blend = 0.3     # Cross-fade intersections to hide seams
    # --------------------------------

    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], img_tex.inputs['Vector'])
    links.new(img_tex.outputs['Color'], bsdf.inputs['Base Color'])

    # Optional: Connect to bump to simulate the video's PBR depth
    bump = nodes.new('ShaderNodeBump')
    bump.location = (400, -250)
    bump.inputs['Distance'].default_value = 0.05
    links.new(img_tex.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    obj.data.materials.append(mat)

    # === Step 4: Finalize Position ===
    obj.location = Vector(location)

    return f"Created '{object_name}' with Box Projected Triplanar mapping at {location}"
