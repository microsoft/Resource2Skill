def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedCharacterBase",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 0.3),  # Base green
    **kwargs,
) -> str:
    """
    Create a procedural block-out for a stylized character/creature.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created mesh object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) primary skin color in 0-1 range.
        **kwargs: Extensible parameters.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    # === Step 1: Generate Character Topology via BMesh ===
    mesh = bpy.data.meshes.new(object_name)
    obj = bpy.data.objects.new(object_name, mesh)
    
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    scene.collection.objects.link(obj)
    
    bm = bmesh.new()
    
    # Create base block and offset it for mirroring
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.translate(bm, vec=(0.5, 0, 1.0), verts=bm.verts)
    
    # Delete the symmetry face (X=0)
    sym_face = None
    for f in bm.faces:
        if abs(f.calc_center_median().x - 0.0) < 0.01:
            sym_face = f
            break
    if sym_face:
        bm.faces.remove(sym_face)
        
    # Helper to find faces by normal and center position
    def get_face(normal, z_val=None, x_val=None):
        for f in bm.faces:
            if f.normal.dot(Vector(normal)) > 0.9:
                if z_val is not None and abs(f.calc_center_median().z - z_val) < 0.1: return f
                if x_val is not None and abs(f.calc_center_median().x - x_val) < 0.1: return f
        return None

    # Helper to scale a face relative to its own center
    def scale_face(face, scale_vec):
        center = face.calc_center_median()
        v_vec = Vector(scale_vec)
        for v in face.verts:
            diff = v.co - center
            v.co = center + Vector((diff.x * v_vec.x, diff.y * v_vec.y, diff.z * v_vec.z))
            
    # -- Extrude Head --
    top_face = get_face((0, 0, 1), z_val=1.5)
    ret = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    head = ret['faces'][0]
    bmesh.ops.translate(bm, vec=(0, 0, 0.5), verts=head.verts)
    scale_face(head, (0.8, 1.5, 0.8)) # Wide, frog-like head

    # -- Extrude Arm (2 Segments) --
    right_face = get_face((1, 0, 0), x_val=1.0)
    ret = bmesh.ops.extrude_discrete_faces(bm, faces=[right_face])
    arm1 = ret['faces'][0]
    scale_face(arm1, (0.4, 0.4, 0.4)) # Taper shoulder
    bmesh.ops.translate(bm, vec=(0.6, 0, -0.2), verts=arm1.verts)

    ret = bmesh.ops.extrude_discrete_faces(bm, faces=[arm1])
    arm2 = ret['faces'][0]
    bmesh.ops.translate(bm, vec=(0.5, 0.1, -0.2), verts=arm2.verts)
    scale_face(arm2, (0.8, 0.8, 0.8)) # Hand/Paw

    # -- Extrude Leg (2 Segments) --
    bottom_face = get_face((0, 0, -1), z_val=0.5)
    ret = bmesh.ops.extrude_discrete_faces(bm, faces=[bottom_face])
    leg1 = ret['faces'][0]
    scale_face(leg1, (0.5, 0.5, 0.5))
    bmesh.ops.translate(bm, vec=(0.2, 0, -0.6), verts=leg1.verts)

    ret = bmesh.ops.extrude_discrete_faces(bm, faces=[leg1])
    leg2 = ret['faces'][0]
    bmesh.ops.translate(bm, vec=(0, 0.3, -0.6), verts=leg2.verts)
    scale_face(leg2, (1.2, 1.5, 0.5)) # Flat foot
    
    # Write back to mesh data and cleanup
    bm.to_mesh(mesh)
    bm.free()
    
    # Smooth shading
    for poly in mesh.polygons:
        poly.use_smooth = True

    # === Step 2: Apply Organic Modifiers ===
    mod_mirror = obj.modifiers.new("Mirror", 'MIRROR')
    mod_mirror.use_clip = True
    mod_mirror.use_axis[0] = True # X axis
    
    mod_subd = obj.modifiers.new("Subdivision", 'SUBSURF')
    mod_subd.levels = 2
    mod_subd.render_levels = 2

    # === Step 3: Procedural Stylized Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Roughness'].default_value = 0.8
    bsdf.inputs['Specular IOR Level'].default_value = 0.1
    bsdf.location = (400, 0)
    
    out = nodes.new('ShaderNodeOutputMaterial')
    out.location = (700, 0)
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])

    # Derive colors
    c_base = material_color + (1.0,)
    c_spot = (material_color[0]*0.4, material_color[1]*0.4, material_color[2]*0.4, 1.0)
    c_belly = (0.9, 0.9, 0.8, 1.0) # Pale off-white
    
    # Voronoi Spots
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.feature = 'F1'
    voronoi.inputs['Scale'].default_value = 8.0
    voronoi.location = (-600, 200)
    
    spot_ramp = nodes.new('ShaderNodeValToRGB')
    spot_ramp.color_ramp.elements[0].position = 0.3
    spot_ramp.color_ramp.elements[0].color = (1, 1, 1, 1)
    spot_ramp.color_ramp.elements[1].position = 0.5
    spot_ramp.color_ramp.elements[1].color = (0, 0, 0, 1)
    spot_ramp.location = (-400, 200)
    links.new(voronoi.outputs['Distance'], spot_ramp.inputs['Fac'])
    
    mix_spots = nodes.new('ShaderNodeMix')
    mix_spots.data_type = 'RGBA'
    mix_spots.blend_type = 'MIX'
    mix_spots.inputs[6].default_value = c_base
    mix_spots.inputs[7].default_value = c_spot
    mix_spots.location = (-100, 200)
    links.new(spot_ramp.outputs['Color'], mix_spots.inputs['Factor'])

    # Belly Mask (Front of character based on bounding box)
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, -200)
    
    sep_xyz = nodes.new('ShaderNodeSeparateXYZ')
    sep_xyz.location = (-400, -200)
    links.new(tex_coord.outputs['Generated'], sep_xyz.inputs['Vector'])
    
    belly_ramp = nodes.new('ShaderNodeValToRGB')
    belly_ramp.color_ramp.elements[0].position = 0.1
    belly_ramp.color_ramp.elements[0].color = (1, 1, 1, 1)
    belly_ramp.color_ramp.elements[1].position = 0.4
    belly_ramp.color_ramp.elements[1].color = (0, 0, 0, 1)
    belly_ramp.location = (-200, -200)
    links.new(sep_xyz.outputs['Y'], belly_ramp.inputs['Fac'])
    
    mix_belly = nodes.new('ShaderNodeMix')
    mix_belly.data_type = 'RGBA'
    mix_belly.blend_type = 'MIX'
    mix_belly.inputs[7].default_value = c_belly
    mix_belly.location = (150, 0)
    
    links.new(mix_spots.outputs['Result'], mix_belly.inputs[6])
    links.new(belly_ramp.outputs['Color'], mix_belly.inputs['Factor'])
    links.new(mix_belly.outputs['Result'], bsdf.inputs['Base Color'])
    
    obj.data.materials.append(mat)

    # === Step 4: Position and Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created procedural base mesh '{obj.name}' at {location} with Subdivision Level 2"
