def create_object(
    scene_name: str = "Scene",
    object_name: str = "SeamlessFlange",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.4, 0.5),
    blend_amount: float = 0.2,
    **kwargs,
) -> str:
    """
    Create a complex mechanical shape using Box Projection for seamless PBR texturing.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: Base paint color of the object.
        blend_amount: Box projection edge blend amount to hide seams (Core Skill).

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (Stepped Cylinder) ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    
    if scene.collection.objects.get(obj.name) is None:
        scene.collection.objects.link(obj)

    bm = bmesh.new()
    # Bottom tier
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=32, radius1=1.5, radius2=1.5, depth=0.2)
    top_faces = [f for f in bm.faces if f.normal.z > 0.9]
    bmesh.ops.translate(bm, vec=(0, 0, 0.1), verts=[v for f in bm.faces for v in f.verts]) # Rest on Z=0

    # Middle tier
    ret = bmesh.ops.inset_region(bm, faces=top_faces, thickness=0.4, depth=0.0)
    extruded = bmesh.ops.extrude_face_region(bm, geom=ret['faces'])
    extruded_faces = [elem for elem in extruded['geom'] if isinstance(elem, bmesh.types.BMFace)]
    bmesh.ops.translate(bm, vec=(0, 0, 0.4), verts=[v for f in extruded_faces for v in f.verts])

    # Top tier
    ret = bmesh.ops.inset_region(bm, faces=extruded_faces, thickness=0.4, depth=0.0)
    extruded = bmesh.ops.extrude_face_region(bm, geom=ret['faces'])
    extruded_faces2 = [elem for elem in extruded['geom'] if isinstance(elem, bmesh.types.BMFace)]
    bmesh.ops.translate(bm, vec=(0, 0, 0.3), verts=[v for f in extruded_faces2 for v in f.verts])

    bm.to_mesh(mesh)
    bm.free()

    # Shade smooth
    for p in mesh.polygons:
        p.use_smooth = True

    # Add Bevel Modifier for sharp industrial edges
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.segments = 3
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(30)
    bevel.width = 0.04

    # Add Subdivision Surface Modifier
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # === Step 2: Generate Synthetic PBR Textures ===
    # We generate textures via python to remain self-contained.
    def generate_rust_albedo(name, size=128):
        img = bpy.data.images.new(name, width=size, height=size)
        pixels = [1.0] * (size * size * 4)
        rust_color = (0.3, 0.15, 0.05)
        for y in range(size):
            for x in range(size):
                idx = (y * size + x) * 4
                nx, ny = x * 0.1, y * 0.1
                # Organic noise math
                noise_val = (math.sin(nx) + math.sin(ny) + math.sin((nx+ny)*1.5)) / 3.0
                noise_val = (noise_val + 1) / 2
                noise_val = noise_val * 0.8 + random.uniform(0, 0.2)
                
                # Mix between base paint and rust
                r, g, b = material_color if noise_val > 0.5 else rust_color
                
                pixels[idx]   = r * (0.8 + noise_val * 0.2)
                pixels[idx+1] = g * (0.8 + noise_val * 0.2)
                pixels[idx+2] = b * (0.8 + noise_val * 0.2)
                pixels[idx+3] = 1.0
        img.pixels = pixels
        return img

    def generate_roughness_bump(name, size=128):
        img = bpy.data.images.new(name, width=size, height=size)
        pixels = [1.0] * (size * size * 4)
        for y in range(size):
            for x in range(size):
                idx = (y * size + x) * 4
                nx, ny = x * 0.1, y * 0.1
                noise_val = (math.sin(nx) + math.sin(ny) + math.sin((nx+ny)*1.5)) / 3.0
                noise_val = (noise_val + 1) / 2
                noise_val = noise_val * 0.8 + random.uniform(0, 0.2)
                
                pixels[idx]   = noise_val
                pixels[idx+1] = noise_val
                pixels[idx+2] = noise_val
                pixels[idx+3] = 1.0
        img.pixels = pixels
        img.colorspace_settings.name = 'Non-Color'
        return img

    img_albedo = generate_rust_albedo(f"{object_name}_Albedo")
    img_data = generate_roughness_bump(f"{object_name}_Data")

    # === Step 3: Build Material & Apply Box Projection ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Nodes
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (800, 0)
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (1100, 0)

    # Coordinate mapping
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (0, 0)
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (200, 0)
    mapping.inputs['Scale'].default_value = (3.0, 3.0, 3.0)

    # Albedo Image Texture (Box Projection)
    tex_color = nodes.new('ShaderNodeTexImage')
    tex_color.location = (500, 200)
    tex_color.image = img_albedo
    tex_color.projection = 'BOX'                  # Core Tutorial Skill
    tex_color.projection_blend = blend_amount     # Hides the seams

    # Roughness/Normal Image Texture (Box Projection)
    tex_data = nodes.new('ShaderNodeTexImage')
    tex_data.location = (500, -200)
    tex_data.image = img_data
    tex_data.projection = 'BOX'
    tex_data.projection_blend = blend_amount

    # Bump Node
    bump = nodes.new('ShaderNodeBump')
    bump.location = (500, -500)
    bump.inputs['Strength'].default_value = 0.4
    bump.inputs['Distance'].default_value = 0.1

    # Connections
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], tex_color.inputs['Vector'])
    links.new(mapping.outputs['Vector'], tex_data.inputs['Vector'])

    links.new(tex_color.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(tex_data.outputs['Color'], bsdf.inputs['Roughness'])
    links.new(tex_data.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Apply material
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    # === Step 4: Finalize ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' with Box Projected seamless material at {location}. (Blend value: {blend_amount})"
