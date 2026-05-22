def create_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjected_Part",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.3, 0.1),
    **kwargs,
) -> str:
    """
    Create a mechanical part demonstrating seamless Box Projection texturing.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color mixed with the texture.
        **kwargs: Additional overrides.

    Returns:
        Status string confirming creation.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (Mechanical Part) ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    
    # Base cylinder
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=32, radius1=1.0, radius2=1.0, depth=0.5)
    
    # Find top face to begin extrusions
    bm.faces.ensure_lookup_table()
    top_face = next((f for f in bm.faces if f.normal.z > 0.5), None)
    
    if top_face:
        # Inset 1
        bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3)
        
        # Extrude Up
        res = bmesh.ops.extrude_face_region(bm, geom=[top_face])
        new_verts = [e for e in res['geom'] if isinstance(e, bmesh.types.BMVert)]
        new_faces = [e for e in res['geom'] if isinstance(e, bmesh.types.BMFace)]
        bmesh.ops.translate(bm, verts=new_verts, vec=(0, 0, 0.5))
        
        # Find the new top face
        top_face_2 = next((f for f in new_faces if f.normal.z > 0.5), None)
        if top_face_2:
            # Inset 2
            bmesh.ops.inset_region(bm, faces=[top_face_2], thickness=0.2)
            
            # Extrude Down (create interior hole)
            res2 = bmesh.ops.extrude_face_region(bm, geom=[top_face_2])
            new_verts2 = [e for e in res2['geom'] if isinstance(e, bmesh.types.BMVert)]
            bmesh.ops.translate(bm, verts=new_verts2, vec=(0, 0, -0.3))

    bm.to_mesh(mesh)
    bm.free()

    # Shade smooth
    for poly in mesh.polygons:
        poly.use_smooth = True

    # Modifiers: Bevel (to catch sharp corners) + Subsurf (to smooth cylinder)
    bevel = obj.modifiers.new("Bevel", 'BEVEL')
    bevel.segments = 3
    bevel.width = 0.05
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = 0.523599  # ~30 degrees

    subsurf = obj.modifiers.new("Subsurf", 'SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # === Step 2: Build Material (Box Projection Skill) ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = (400, 0)

    node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_principled.location = (100, 0)
    node_principled.inputs['Roughness'].default_value = 0.6
    node_principled.inputs['Metallic'].default_value = 0.7

    # Create a built-in generated Image to demonstrate the mapping without external files
    img_name = "BoxProject_Test_Grid"
    if img_name in bpy.data.images:
        img = bpy.data.images[img_name]
    else:
        img = bpy.data.images.new(img_name, width=1024, height=1024)
        img.source = 'GENERATED'
        img.generated_type = 'COLOR_GRID'

    node_tex = nodes.new(type='ShaderNodeTexImage')
    node_tex.location = (-200, 0)
    node_tex.image = img
    
    # *** CORE SKILL: Set projection to BOX and apply blend ***
    node_tex.projection = 'BOX'
    node_tex.projection_blend = 0.2

    node_mapping = nodes.new(type='ShaderNodeMapping')
    node_mapping.location = (-400, 0)
    node_mapping.inputs['Scale'].default_value = (3.0, 3.0, 3.0)

    # Use Object coordinates for scale-independent, seamless mapping
    node_coord = nodes.new(type='ShaderNodeTexCoord')
    node_coord.location = (-600, 0)

    # Connecting Mapping
    links.new(node_coord.outputs['Object'], node_mapping.inputs['Vector'])
    links.new(node_mapping.outputs['Vector'], node_tex.inputs['Vector'])

    # Mix the grid texture with the provided material color 
    # Use a try-except block to gracefully handle the Mix node API change between Blender 3.x and 4.x
    try:
        node_mix = nodes.new(type='ShaderNodeMix')
        node_mix.data_type = 'RGBA'
        node_mix.blend_type = 'MULTIPLY'
        node_mix.inputs['Factor'].default_value = 0.8
        node_mix.inputs['A'].default_value = (*material_color, 1.0)
        links.new(node_tex.outputs['Color'], node_mix.inputs['B'])
        links.new(node_mix.outputs['Result'], node_principled.inputs['Base Color'])
    except Exception:
        # Fallback for Blender versions < 3.4
        node_mix = nodes.new(type='ShaderNodeMixRGB')
        node_mix.blend_type = 'MULTIPLY'
        node_mix.inputs['Fac'].default_value = 0.8
        node_mix.inputs['Color1'].default_value = (*material_color, 1.0)
        links.new(node_tex.outputs['Color'], node_mix.inputs['Color2'])
        links.new(node_mix.outputs['Color'], node_principled.inputs['Base Color'])

    links.new(node_principled.outputs['BSDF'], node_output.inputs['Surface'])

    # Assign material
    obj.data.materials.append(mat)

    # === Step 3: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' demonstrating Box Projection Material at {location}"
