def create_object(
    scene_name: str = "Scene",
    object_name: str = "BoxProjectedPart",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 0.8),
    **kwargs,
) -> str:
    """
    Create a complex stepped cylinder demonstrating Box (Triplanar) projection texturing.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) color used for the worn paint layer.
        **kwargs: Optional 'blend' float to control the Box projection seam softness.

    Returns:
        Status string describing the operation.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Mesh & Object ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # === Step 2: Build Stepped Geometry with BMesh ===
    bm = bmesh.new()
    # Base cylinder
    bmesh.ops.create_cone(bm, cap_ends=True, segments=32, radius1=1.0, radius2=1.0, depth=0.5)
    bmesh.ops.translate(bm, vec=(0, 0, 0.25), verts=bm.verts) # Base on Z=0
    bm.normal_update()

    # Find top face
    top_face = next((f for f in bm.faces if f.normal.z > 0.9), None)
            
    if top_face:
        # Tier 2
        bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3)
        res = bmesh.ops.extrude_face_region(bm, geom=[top_face])
        ext_verts = [v for v in res['geom'] if isinstance(v, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, vec=(0, 0, 0.5), verts=ext_verts)
        bm.normal_update()
        
        # Find new top face
        top_face2 = next((f for f in bm.faces if f.normal.z > 0.9 and f.calc_center_median().z > 0.6), None)
                
        if top_face2:
            # Tier 3
            bmesh.ops.inset_region(bm, faces=[top_face2], thickness=0.2)
            res2 = bmesh.ops.extrude_face_region(bm, geom=[top_face2])
            ext_verts2 = [v for v in res2['geom'] if isinstance(v, bmesh.types.BMVert)]
            bmesh.ops.translate(bm, vec=(0, 0, 0.4), verts=ext_verts2)

    bm.to_mesh(mesh)
    bm.free()

    for poly in mesh.polygons:
        poly.use_smooth = True

    # === Step 3: Add Modifiers ===
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.segments = 3
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = 0.52 # ~30 degrees
    bevel.width = 0.05

    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # === Step 4: Build Triplanar Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (800, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (500, 0)
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    # Coordinates
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-400, 0)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-200, 0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # Create a generated image pattern to visualize the projection
    img_name = "Triplanar_Test_Grid"
    if img_name not in bpy.data.images:
        img = bpy.data.images.new(name=img_name, width=1024, height=1024, alpha=False)
        img.generated_type = 'COLOR_GRID'
    else:
        img = bpy.data.images[img_name]

    # THE CORE SKILL: Box Projection setup
    img_tex = nodes.new('ShaderNodeTexImage')
    img_tex.location = (100, -200)
    img_tex.image = img
    img_tex.projection = 'BOX'  # Triplanar projection
    blend_val = kwargs.get('blend', 0.2)
    img_tex.projection_blend = blend_val # Seamless edge blending
    links.new(mapping.outputs['Vector'], img_tex.inputs['Vector'])

    # Mask for worn paint effect
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-100, 200)
    noise.inputs['Scale'].default_value = 5.0
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (100, 200)
    colorramp.color_ramp.elements[0].position = 0.4
    colorramp.color_ramp.elements[1].position = 0.6
    links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])

    # Mix Paint Color with the Box-Projected Grid
    if bpy.app.version >= (3, 4, 0):
        mix_node = nodes.new('ShaderNodeMix')
        mix_node.data_type = 'RGBA'
        mix_node.blend_type = 'MIX'
        mix_node.inputs[6].default_value = (*material_color, 1.0) # A (Paint)
        links.new(img_tex.outputs['Color'], mix_node.inputs[7])   # B (Underlying texture)
        links.new(colorramp.outputs['Color'], mix_node.inputs[0]) # Factor
        result_output = mix_node.outputs['Result']
    else:
        mix_node = nodes.new('ShaderNodeMixRGB')
        mix_node.blend_type = 'MIX'
        mix_node.inputs[1].default_value = (*material_color, 1.0)
        links.new(img_tex.outputs['Color'], mix_node.inputs[2])
        links.new(colorramp.outputs['Color'], mix_node.inputs[0])
        result_output = mix_node.outputs['Color']

    links.new(result_output, bsdf.inputs['Base Color'])
    obj.data.materials.append(mat)

    # === Step 5: Placement & Finalization ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    # Ensure viewport displays the material correctly
    if scene.view_settings.view_transform != 'Standard':
        scene.view_settings.view_transform = 'Filmic'

    return f"Created '{object_name}' with Box Projection (Blend: {blend_val}) at {location}"
