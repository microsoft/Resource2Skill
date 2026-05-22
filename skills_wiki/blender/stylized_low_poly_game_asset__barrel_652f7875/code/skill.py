def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyBarrel",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.4, 0.2, 0.05),
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Barrel in the active Blender scene.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base wood color.
        **kwargs: 
            segments (int): Polygon count for the cylinder (default 12 for low-poly).
            
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Initialize Object and Mesh
    mesh = bpy.data.meshes.new(object_name)
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()

    segments = kwargs.get("segments", 12)
    radius_base = 0.35
    
    # === Step 1: Create the Base Ring ===
    # We create the barrel from bottom (Z=0.0) to top (Z=1.0) so the origin is at the base
    ret = bmesh.ops.create_circle(bm, cap_ends=False, segments=segments, radius=radius_base)
    for v in ret['verts']:
        v.co.z = 0.0
        
    current_edges = [e for e in bm.edges]

    # Material Indices
    WOOD_IDX = 0
    METAL_IDX = 1
    DARK_WOOD_IDX = 2

    # === Step 2: Procedural Profile Extrusion ===
    # Each step defines the (Z-height, Radius, Material applied to the side faces generated)
    profile = [
        (0.2, 0.41, WOOD_IDX),      # Curve up to lower band
        (0.2, 0.43, METAL_IDX),     # Metal band bottom shelf (horizontal)
        (0.3, 0.45, METAL_IDX),     # Metal band outer surface
        (0.3, 0.43, METAL_IDX),     # Metal band top shelf (horizontal)
        (0.5, 0.45, WOOD_IDX),      # Curve up to equator (max radius)
        (0.7, 0.43, WOOD_IDX),      # Curve up to upper band
        (0.7, 0.45, METAL_IDX),     # Metal band bottom shelf
        (0.8, 0.43, METAL_IDX),     # Metal band outer surface
        (0.8, 0.41, METAL_IDX),     # Metal band top shelf
        (1.0, 0.35, WOOD_IDX)       # Curve up to top rim
    ]

    for z, r, mat_idx in profile:
        # Extrude the current top loop
        ret = bmesh.ops.extrude_edge_only(bm, edges=current_edges)
        extruded_geom = ret['geom']
        
        # Identify the new components
        new_verts = [v for v in extruded_geom if isinstance(v, bmesh.types.BMVert)]
        new_edges = [e for e in extruded_geom if isinstance(e, bmesh.types.BMEdge) and all(v in new_verts for v in e.verts)]
        new_faces = [f for f in extruded_geom if isinstance(f, bmesh.types.BMFace)]
        
        # Apply Material
        for f in new_faces:
            f.material_index = mat_idx
            
        # Scale and position the new loop radially
        for v in new_verts:
            angle = math.atan2(v.co.y, v.co.x)
            v.co.x = math.cos(angle) * r
            v.co.y = math.sin(angle) * r
            v.co.z = z
            
        current_edges = new_edges

    # === Step 3: Cap the Ends ===
    # Find bottom and top boundary loops based on explicit Z coordinates
    bottom_edges = [e for e in bm.edges if e.verts[0].co.z < 0.01 and e.verts[1].co.z < 0.01]
    ret = bmesh.ops.holes_fill(bm, edges=bottom_edges)
    bottom_cap = ret['faces']

    top_edges = [e for e in bm.edges if e.verts[0].co.z > 0.99 and e.verts[1].co.z > 0.99]
    ret = bmesh.ops.holes_fill(bm, edges=top_edges)
    top_cap = ret['faces']

    # === Step 4: Inset Caps to create the Rim ===
    # Inset the top cap, and sink the inner face downwards
    bmesh.ops.inset_region(bm, faces=top_cap, thickness=0.04)
    for f in top_cap: # The original face remains the inner face
        f.material_index = DARK_WOOD_IDX
        for v in f.verts:
            v.co.z -= 0.03

    # Inset the bottom cap, and push the inner face upwards
    bmesh.ops.inset_region(bm, faces=bottom_cap, thickness=0.04)
    for f in bottom_cap:
        f.material_index = DARK_WOOD_IDX
        for v in f.verts:
            v.co.z += 0.03

    # === Step 5: Finalize Mesh ===
    # Enforce flat shading for the distinct low-poly aesthetic
    for f in bm.faces:
        f.smooth = False

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    
    bm.to_mesh(mesh)
    bm.free()

    # === Step 6: Materials ===
    def create_material(name, color, metallic=0.0, roughness=0.8):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*color, 1.0)
            bsdf.inputs["Metallic"].default_value = metallic
            bsdf.inputs["Roughness"].default_value = roughness
        return mat

    mat_wood = create_material(f"{object_name}_Wood", material_color, 0.0, 0.8)
    mat_metal = create_material(f"{object_name}_Metal", (0.2, 0.2, 0.2), 1.0, 0.4)
    # Darker wood for the interior to fake occlusion depth without textures
    dark_color = (material_color[0]*0.5, material_color[1]*0.5, material_color[2]*0.5)
    mat_dark = create_material(f"{object_name}_DarkWood", dark_color, 0.0, 0.9)

    obj.data.materials.append(mat_wood)   # Slot 0
    obj.data.materials.append(mat_metal)  # Slot 1
    obj.data.materials.append(mat_dark)   # Slot 2

    # === Step 7: Transform ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created game-ready asset '{object_name}' (Low-Poly Barrel) at {location}"
