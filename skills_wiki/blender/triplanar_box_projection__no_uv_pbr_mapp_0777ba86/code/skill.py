def create_box_projected_asset(
    scene_name: str = "Scene",
    object_name: str = "Worn_Mechanical_Base",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create a stepped mechanical cylinder utilizing Triplanar Box Projection
    to apply textures seamlessly without UV unwrapping.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base tint for the object.

    Returns:
        Status string confirming creation.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    
    # Ensure scene exists
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Base Geometry Construction ===
    # Create the base cylinder
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32, 
        radius=1.0, 
        depth=0.5, 
        location=location
    )
    obj = bpy.context.active_object
    obj.name = object_name
    
    # Use BMesh to create the stepped architectural shape
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    
    # Apply base scale directly to vertices to avoid unapplied Object scale
    # This prevents the Bevel Modifier and Box Projection from skewing later
    bmesh.ops.scale(bm, vec=(scale, scale, scale), verts=bm.verts)

    # First Tier: Inset and Extrude UP
    top_faces = [f for f in bm.faces if f.normal.z > 0.99]
    ret1 = bmesh.ops.inset_region(bm, faces=top_faces, thickness=0.3 * scale)
    new_top_faces1 = [f for f in ret1['faces'] if f.normal.z > 0.99]
    
    ret_ext1 = bmesh.ops.extrude_face_region(bm, geom=new_top_faces1)
    extruded_faces1 = [e for e in ret_ext1['geom'] if isinstance(e, bmesh.types.BMFace)]
    verts_to_move1 = list({v for f in extruded_faces1 for v in f.verts})
    bmesh.ops.translate(bm, vec=(0, 0, 0.4 * scale), verts=verts_to_move1)

    # Second Tier: Inset and Extrude UP again
    top_faces2 = [f for f in bm.faces if f.normal.z > 0.99 and f.calc_center_median().z > (0.2 * scale)]
    ret2 = bmesh.ops.inset_region(bm, faces=top_faces2, thickness=0.2 * scale)
    new_top_faces2 = [f for f in ret2['faces'] if f.normal.z > 0.99]
    
    ret_ext2 = bmesh.ops.extrude_face_region(bm, geom=new_top_faces2)
    extruded_faces2 = [e for e in ret_ext2['geom'] if isinstance(e, bmesh.types.BMFace)]
    verts_to_move2 = list({v for f in extruded_faces2 for v in f.verts})
    bmesh.ops.translate(bm, vec=(0, 0, 0.3 * scale), verts=verts_to_move2)

    bm.to_mesh(obj.data)
    bm.free()

    # Shade smooth
    for poly in obj.data.polygons:
        poly.use_smooth = True

    # === Step 2: Non-Destructive Softening (Modifiers) ===
    # Add Bevel to catch light on the hard mechanical edges
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.segments = 3
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = 0.523599  # ~30 degrees
    bevel.width = 0.05 * scale

    # Add Subsurf to smooth out the cylindrical curvature
    subsurf = obj.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 3

    # === Step 3: Triplanar Box Projection Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_BoxProjected_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core material nodes
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (100, 0)
    bsdf.inputs['Roughness'].default_value = 0.8
    bsdf.inputs['Metallic'].default_value = 0.7
    links.new(bsdf.outputs[0], output.inputs[0])

    # THE SKILL: Object Coordinates -> Mapping
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-800, 0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # THE SKILL: Box Projection & Blend
    tex_image = nodes.new('ShaderNodeTexImage')
    tex_image.location = (-500, 0)
    tex_image.projection = 'BOX'           # Replaces 'FLAT' mapping
    tex_image.projection_blend = 0.25      # Blends the seams where the XYZ axes meet
    links.new(mapping.outputs['Vector'], tex_image.inputs['Vector'])

    # Generate an internal Color Grid to visually demonstrate Box Projection
    # (Using a grid makes the lack of stretching incredibly obvious)
    img_name = "BoxProj_DemoGrid"
    img = bpy.data.images.get(img_name)
    if not img:
        img = bpy.data.images.new(name=img_name, width=1024, height=1024, alpha=False, generated_type='COLOR_GRID')
    tex_image.image = img

    # Tint the grid with the specified material color using Vector Math (Version Safe)
    multiply = nodes.new('ShaderNodeVectorMath')
    multiply.operation = 'MULTIPLY'
    multiply.location = (-200, 0)
    multiply.inputs[1].default_value = (*material_color[:3], 1.0)
    links.new(tex_image.outputs['Color'], multiply.inputs[0])
    links.new(multiply.outputs['Vector'], bsdf.inputs['Base Color'])

    # Add procedural bump to simulate the "worn rust" from the tutorial
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-500, -300)
    noise.inputs['Scale'].default_value = 15.0
    noise.inputs['Detail'].default_value = 15.0
    links.new(mapping.outputs['Vector'], noise.inputs['Vector']) # Use object coords here too

    bump = nodes.new('ShaderNodeBump')
    bump.location = (-200, -300)
    bump.inputs['Strength'].default_value = 0.6
    bump.inputs['Distance'].default_value = 0.1
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    # Assign material
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    return f"Created Box-Projected object '{obj.name}' at {location}. Switch to Material Preview to observe the seamless mapping."
