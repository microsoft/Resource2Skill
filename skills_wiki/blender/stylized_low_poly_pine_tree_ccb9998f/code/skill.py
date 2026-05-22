def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyPineTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.12, 0.35, 0.1),
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Pine Tree in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color of the foliage in 0-1 range.
        **kwargs: Extensible parameters (e.g., layers=4 to control foliage tiers).

    Returns:
        Status string describing the creation of the object.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector, Matrix

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Materials ===
    
    # Foliage Material
    mat_foliage = bpy.data.materials.new(name=f"{object_name}_Foliage")
    mat_foliage.use_nodes = True
    bsdf_f = mat_foliage.node_tree.nodes.get("Principled BSDF")
    if bsdf_f:
        bsdf_f.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf_f.inputs["Roughness"].default_value = 0.9

    # Trunk Material
    mat_trunk = bpy.data.materials.new(name=f"{object_name}_Trunk")
    mat_trunk.use_nodes = True
    bsdf_t = mat_trunk.node_tree.nodes.get("Principled BSDF")
    if bsdf_t:
        bsdf_t.inputs["Base Color"].default_value = (0.05, 0.025, 0.01, 1.0)
        bsdf_t.inputs["Roughness"].default_value = 0.9

    # === Step 2: Create Geometry via BMesh ===
    mesh = bpy.data.meshes.new(name=object_name)
    obj = bpy.data.objects.new(name=object_name, object_data=mesh)
    scene.collection.objects.link(obj)

    mesh.materials.append(mat_trunk)   # Index 0
    mesh.materials.append(mat_foliage) # Index 1

    bm = bmesh.new()

    # 2a. Build Trunk (Tapered 8-sided Cylinder)
    trunk_geom = bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=8,
        radius1=0.2 * scale,
        radius2=0.08 * scale,
        depth=1.5 * scale
    )
    # Translate trunk so the base sits exactly on Z=0
    bmesh.ops.translate(
        bm,
        vec=(0, 0, 0.75 * scale),
        verts=trunk_geom['verts']
    )
    # Assign trunk material index (0)
    for f in bm.faces:
        f.material_index = 0

    # 2b. Build Foliage Layers (Stacked 12-sided Frustums)
    layers = kwargs.get("layers", 4)
    base_z = 0.5 * scale  # Start the first layer part-way up the trunk
    
    rad1 = 0.9 * scale
    rad2 = 0.3 * scale
    depth = 0.8 * scale

    for i in range(layers):
        faces_before = set(bm.faces)
        
        # The final top layer ends in a sharp point (radius2 = 0.0)
        is_top = (i == layers - 1)
        r2 = 0.0 if is_top else rad2
        
        cone_geom = bmesh.ops.create_cone(
            bm,
            cap_ends=True,
            cap_tris=False,
            segments=12,
            radius1=rad1,
            radius2=r2,
            depth=depth
        )
        
        # Position height, and rotate to add organic variation between tiers
        z_offset = base_z + (depth / 2)
        rot_mat = Matrix.Rotation(math.radians(15 * i), 4, 'Z')
        trans_mat = Matrix.Translation((0, 0, z_offset))
        transform_mat = trans_mat @ rot_mat
        
        bmesh.ops.transform(
            bm,
            matrix=transform_mat,
            verts=cone_geom['verts']
        )
        
        # Assign foliage material index (1) to newly generated faces
        new_faces = set(bm.faces) - faces_before
        for f in new_faces:
            f.material_index = 1
            
        # Update metrics to shrink and shift up for the next layer tier
        base_z += depth * 0.55  
        rad1 *= 0.75
        rad2 *= 0.75
        depth *= 0.9

    bm.to_mesh(mesh)
    bm.free()

    # === Step 3: Shading & Modifiers ===
    
    # First, enable smooth shading internally on all mesh polygons
    for poly in mesh.polygons:
        poly.use_smooth = True

    # Use Edge Split to replicate "Auto Smooth" shading robustly across different versions of Blender.
    # It sharpens angles greater than 30 degrees (preserves the flat overlapping skirt geometry) 
    # but smooths the curved 12-sided wrapping form.
    edge_split = obj.modifiers.new(name="Auto_Smooth_Proxy", type='EDGE_SPLIT')
    edge_split.split_angle = math.radians(30)

    # === Step 4: Finalize Transformations ===
    obj.location = Vector(location)

    return f"Created '{object_name}' at {location} with {layers} foliage layers."
