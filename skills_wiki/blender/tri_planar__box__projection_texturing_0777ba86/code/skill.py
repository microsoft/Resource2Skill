def create_object(
    scene_name: str = "Scene",
    object_name: str = "TriPlanar_MechanicalProp",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.25, 0.1),
    **kwargs,
) -> str:
    """
    Create a mechanical prop utilizing Box (Tri-Planar) Projection Texturing.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) color used to tint the projected texture.

    Returns:
        Status string confirming object creation.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    # Ensure target scene exists
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Mechanical Geometry ===
    mesh = bpy.data.meshes.new(name=object_name)
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    
    # Base flange
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=32,
        radius1=1.5,
        radius2=1.5,
        depth=0.4
    )

    # Find the top face (+Z normal) to extrude complex tiers
    top_faces = [f for f in bm.faces if f.normal.z > 0.9]
    if top_faces:
        top_face = top_faces[0]

        # Tier 1 (Inset)
        res = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
        top_face = res['faces'][0]
        bmesh.ops.scale(bm, vec=(0.7, 0.7, 1.0), verts=top_face.verts)

        # Tier 1 (Extrude up)
        res = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
        top_face = res['faces'][0]
        bmesh.ops.translate(bm, verts=top_face.verts, vec=(0, 0, 0.5))

        # Tier 2 (Inset)
        res = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
        top_face = res['faces'][0]
        bmesh.ops.scale(bm, vec=(0.6, 0.6, 1.0), verts=top_face.verts)

        # Trench (Extrude down)
        res = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
        top_face = res['faces'][0]
        bmesh.ops.translate(bm, verts=top_face.verts, vec=(0, 0, -0.4))

        # Center Pillar (Inset)
        res = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
        top_face = res['faces'][0]
        bmesh.ops.scale(bm, vec=(0.5, 0.5, 1.0), verts=top_face.verts)

        # Center Pillar (Extrude up)
        res = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
        top_face = res['faces'][0]
        bmesh.ops.translate(bm, verts=top_face.verts, vec=(0, 0, 0.8))

        # Pillar Cap
        res = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
        top_face = res['faces'][0]
        bmesh.ops.scale(bm, vec=(0.8, 0.8, 1.0), verts=top_face.verts)
        bmesh.ops.translate(bm, verts=top_face.verts, vec=(0, 0, 0.1))

    bm.to_mesh(mesh)
    bm.free()

    # Shade smooth
    for poly in mesh.polygons:
        poly.use_smooth = True

    # === Step 2: Apply Modifiers ===
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(35)
    bevel.width = 0.04
    bevel.segments = 3

    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # === Step 3: Build Tri-Planar Material Setup ===
    mat = bpy.data.materials.new(name=f"{object_name}_TriPlanar_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    for node in nodes:
        nodes.remove(node)

    # Coordinates & Mapping
    node_tc = nodes.new('ShaderNodeTexCoord')
    node_tc.location = (-1000, 0)

    node_mapping = nodes.new('ShaderNodeMapping')
    node_mapping.location = (-800, 0)

    # Core Skill: Image Texture with Box Projection
    node_tex = nodes.new('ShaderNodeTexImage')
    node_tex.location = (-500, 0)
    
    # Generate a Color Grid to visually prove the seams are blending correctly
    grid_img = bpy.data.images.get("BoxProj_ColorGrid")
    if not grid_img:
        grid_img = bpy.data.images.new("BoxProj_ColorGrid", 1024, 1024, alpha=False, generated_type='COLOR_GRID')
    node_tex.image = grid_img
    
    # THE CRITICAL PROPERTIES
    node_tex.projection = 'BOX'
    node_tex.projection_blend = 0.25 # Feather/blur the seams

    # Tint the grid with material_color
    node_tint = nodes.new('ShaderNodeVectorMath')
    node_tint.operation = 'MULTIPLY'
    node_tint.inputs[1].default_value = (*material_color,)
    node_tint.location = (-200, 0)

    # Add procedural noise bump to simulate the video's worn/rusted surface
    node_noise = nodes.new('ShaderNodeTexNoise')
    node_noise.location = (-500, -300)
    node_noise.inputs['Scale'].default_value = 15.0

    node_bump = nodes.new('ShaderNodeBump')
    node_bump.location = (-200, -300)
    node_bump.inputs['Distance'].default_value = 0.1
    node_bump.inputs['Strength'].default_value = 0.6

    # Main BSDF
    node_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    node_bsdf.location = (0, 0)
    node_bsdf.inputs['Metallic'].default_value = 0.8
    node_bsdf.inputs['Roughness'].default_value = 0.4

    node_output = nodes.new('ShaderNodeOutputMaterial')
    node_output.location = (300, 0)

    # Connect tree
    links.new(node_tc.outputs['Object'], node_mapping.inputs['Vector'])
    links.new(node_mapping.outputs['Vector'], node_tex.inputs['Vector'])
    links.new(node_tex.outputs['Color'], node_tint.inputs[0])
    links.new(node_tint.outputs['Vector'], node_bsdf.inputs['Base Color'])
    
    links.new(node_noise.outputs['Fac'], node_bump.inputs['Height'])
    links.new(node_bump.outputs['Normal'], node_bsdf.inputs['Normal'])
    
    links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])

    # Assign material
    obj.data.materials.append(mat)

    # === Step 4: Final Placement ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{obj.name}' with Tri-Planar box projection material at {location}"
