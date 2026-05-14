def create_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjected_Part",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.4, 0.1),
    **kwargs,
) -> str:
    """
    Creates a complex hard-surface shape and applies a seamlessly Box-Projected 
    procedural/image material without relying on UV maps.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: Base tint (R, G, B) to influence the PBR procedural mix.
        **kwargs: Additional overrides.

    Returns:
        Status string confirming creation.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    # Get the scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (Stepped Cylinder) ===
    # Start with a base cylinder
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1.0, depth=0.6, location=(0,0,0))
    obj = bpy.context.active_object
    obj.name = object_name
    
    # Enter BMesh to create the complex extruded shape
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()

    # Find the top face (sort by highest Z coordinate and normal pointing up)
    top_faces = sorted([f for f in bm.faces if f.normal.z > 0.9], key=lambda f: f.calc_center_bounds().z, reverse=True)
    top_face = top_faces[0]

    # Inset 1
    res1 = bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3)
    
    # Extrude Up
    res2 = bmesh.ops.extrude_face_region(bm, geom=[top_face])
    new_faces1 = [f for f in res2['geom'] if isinstance(f, bmesh.types.BMFace)]
    new_top = next(f for f in new_faces1 if f.normal.z > 0.9)
    bmesh.ops.translate(bm, vec=(0, 0, 0.5), verts=new_top.verts)

    # Inset 2
    res3 = bmesh.ops.inset_region(bm, faces=[new_top], thickness=0.2)

    # Extrude Down (creating a central hole/indent)
    res4 = bmesh.ops.extrude_face_region(bm, geom=[new_top])
    new_faces2 = [f for f in res4['geom'] if isinstance(f, bmesh.types.BMFace)]
    new_bottom = next(f for f in new_faces2 if f.normal.z > 0.9)
    bmesh.ops.translate(bm, vec=(0, 0, -0.3), verts=new_bottom.verts)

    # Write back to mesh
    bm.to_mesh(obj.data)
    bm.free()

    # Apply Modifiers for smooth mechanical look
    mod_bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    mod_bevel.limit_method = 'ANGLE'
    mod_bevel.angle_limit = math.radians(30)
    mod_bevel.segments = 3
    mod_bevel.width = 0.03

    mod_subd = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    mod_subd.levels = 2
    mod_subd.render_levels = 2

    # Smooth shading
    for poly in obj.data.polygons:
        poly.use_smooth = True

    # === Step 2: Build the Box Projection Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Create Material Output and Principled BSDF
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (1200, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (800, 0)
    bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.8
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    # Coordinate mapping (The Core Technique: Object Space)
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-400, 0)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-200, 0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # Create an internal Generated Image (Color Grid) to visually prove the Box Projection works seamlessly
    img_name = "Projection_Test_Grid"
    if img_name in bpy.data.images:
        img = bpy.data.images[img_name]
    else:
        img = bpy.data.images.new(name=img_name, width=1024, height=1024, alpha=False, generated_type='COLOR_GRID')

    # Image Texture node with Box Projection
    tex_img = nodes.new('ShaderNodeTexImage')
    tex_img.location = (100, 200)
    tex_img.image = img
    tex_img.projection = 'BOX'           # Tri-planar projection
    tex_img.projection_blend = 0.25      # Blends the seams
    links.new(mapping.outputs['Vector'], tex_img.inputs['Vector'])
    links.new(tex_img.outputs['Color'], bsdf.inputs['Base Color'])

    # Add procedural Noise to simulate the uneven rust/dirt roughness from the video
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (100, -200)
    noise.inputs['Scale'].default_value = 4.0
    noise.inputs['Detail'].default_value = 15.0
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])

    # Map noise to Roughness
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (400, -100)
    color_ramp.color_ramp.elements[0].position = 0.3
    color_ramp.color_ramp.elements[1].position = 0.8
    color_ramp.color_ramp.elements[0].color = (0.2, 0.2, 0.2, 1.0)
    color_ramp.color_ramp.elements[1].color = (0.9, 0.9, 0.9, 1.0)
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Roughness'])

    # Add Bump mapping for structural realism
    bump = nodes.new('ShaderNodeBump')
    bump.location = (400, -400)
    bump.inputs['Distance'].default_value = 0.05
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    # Assign material
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    # === Step 3: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # Make sure object is in scene collection
    if obj.name not in scene.collection.objects:
        scene.collection.objects.link(obj)

    return f"Created '{obj.name}' utilizing Box Projection Texturing at {location}"
