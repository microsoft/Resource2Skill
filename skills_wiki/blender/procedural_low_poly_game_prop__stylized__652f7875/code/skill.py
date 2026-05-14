def create_low_poly_barrel(
    scene_name: str = "Scene",
    object_name: str = "LowPolyBarrel",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    wood_color: tuple = (0.40, 0.18, 0.05),
    metal_color: tuple = (0.20, 0.20, 0.20),
    segments: int = 12
) -> str:
    """
    Create a stylized, low-poly wooden barrel optimized for game engines.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created object.
        location: (x, y, z) world-space position. The origin is at the base.
        scale: Uniform scale factor.
        wood_color: (R, G, B) color for the wooden planks.
        metal_color: (R, G, B) color for the metal bands.
        segments: Number of vertical sides (12 is standard for stylized low-poly).
        
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Define Materials ===
    def get_or_create_mat(name, color, metallic, roughness):
        mat = bpy.data.materials.get(name)
        if not mat:
            mat = bpy.data.materials.new(name)
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                # Blender expects RGBA
                bsdf.inputs['Base Color'].default_value = (*color, 1.0)
                bsdf.inputs['Metallic'].default_value = metallic
                bsdf.inputs['Roughness'].default_value = roughness
        return mat

    dark_wood_color = (wood_color[0] * 0.3, wood_color[1] * 0.3, wood_color[2] * 0.3)
    
    mat_wood = get_or_create_mat("Prop_Wood", wood_color, 0.0, 0.8)
    mat_metal = get_or_create_mat("Prop_Metal", metal_color, 0.8, 0.4)
    mat_dark = get_or_create_mat("Prop_DarkWood", dark_wood_color, 0.0, 0.9)

    # === Step 2: Define the Profile Rings ===
    # Format: (Radius, Z_Height, Material_Index_For_Faces_Below)
    # Materials: 0=Wood, 1=Metal, 2=Dark Inside
    # Origin (Z=0) is placed exactly at the bottom of the barrel.
    rings = [
        (0.00,  1.95, 2), # 0: Top cap center
        (0.65,  1.95, 2), # 1: Top cap inside edge
        (0.65,  2.00, 0), # 2: Top rim inner
        (0.80,  2.00, 0), # 3: Top rim outer
        (0.92,  1.60, 1), # 4: Wood wall down to top metal band
        (0.96,  1.60, 1), # 5: Top metal band upper lip
        (0.99,  1.30, 1), # 6: Top metal band outer face
        (0.96,  1.30, 0), # 7: Top metal band lower lip
        (1.05,  1.00, 0), # 8: Equator (widest bulge)
        (0.96,  0.70, 1), # 9: Wood wall down to bot metal band
        (0.99,  0.70, 1), # 10: Bot metal band upper lip
        (0.96,  0.40, 1), # 11: Bot metal band outer face
        (0.92,  0.40, 0), # 12: Bot metal band lower lip
        (0.80,  0.00, 0), # 13: Wood wall to bottom rim
        (0.65,  0.00, 2), # 14: Bottom rim inner
        (0.65,  0.05, 2), # 15: Bottom cap inside edge
        (0.00,  0.05, 0), # 16: Bottom cap center
    ]

    verts = []
    faces = []
    mat_indices = []

    # Generate Vertices
    vert_count = 0
    ring_start_indices = []

    for i, (r, z, mat) in enumerate(rings):
        ring_start_indices.append(vert_count)
        if r == 0:
            verts.append((0.0, 0.0, z))
            vert_count += 1
        else:
            for s in range(segments):
                angle = (s / segments) * 2 * math.pi
                verts.append((r * math.cos(angle), r * math.sin(angle), z))
            vert_count += segments

    # Generate Faces and Assign Material Indices
    for i in range(len(rings) - 1):
        r1, z1, mat = rings[i]
        r2, z2, _ = rings[i+1]
        
        idx1 = ring_start_indices[i]
        idx2 = ring_start_indices[i+1]
        
        if r1 == 0:
            # Triangle fan from center out
            for s in range(segments):
                n_s = (s + 1) % segments
                faces.append((idx1, idx2 + s, idx2 + n_s))
                mat_indices.append(mat)
        elif r2 == 0:
            # Triangle fan from outer in
            for s in range(segments):
                n_s = (s + 1) % segments
                faces.append((idx1 + s, idx1 + n_s, idx2))
                mat_indices.append(mat)
        else:
            # Quads connecting rings
            for s in range(segments):
                n_s = (s + 1) % segments
                faces.append((idx1 + s, idx2 + s, idx2 + n_s, idx1 + n_s))
                mat_indices.append(mat)

    # === Step 3: Create Mesh and Object ===
    mesh = bpy.data.meshes.new(name=object_name + "_Mesh")
    mesh.from_pydata(verts, [], faces)
    
    # Apply material indices to polygons
    for i, poly in enumerate(mesh.polygons):
        poly.material_index = mat_indices[i]
        # Flat shading is default, which looks best for this low-poly style
        poly.use_smooth = False 

    # Assign materials to the mesh
    mesh.materials.append(mat_wood)   # index 0
    mesh.materials.append(mat_metal)  # index 1
    mesh.materials.append(mat_dark)   # index 2

    # Fix normals
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()

    # Create Object
    obj = bpy.data.objects.new(object_name, mesh)
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    scene.collection.objects.link(obj)

    return f"Created '{obj.name}' at {location} with {len(faces)} optimized faces."
