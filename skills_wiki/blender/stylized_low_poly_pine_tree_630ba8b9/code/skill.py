def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedPineTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.4, 0.1),
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Pine Tree in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the foliage.
        **kwargs: 
            tiers (int): Number of foliage tiers (default: 5).
            trunk_color (tuple): (R, G, B) base color for the trunk.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector, Matrix

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    tiers = kwargs.get("tiers", 5)
    trunk_color = kwargs.get("trunk_color", (0.15, 0.08, 0.03))
    
    # === Step 1: Initialize Mesh and BMesh ===
    mesh = bpy.data.meshes.new(name=object_name)
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    bm = bmesh.new()
    
    # === Step 2: Create Trunk ===
    trunk_depth = 1.5
    trunk_geom = bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=8,
        radius1=0.25,
        radius2=0.15,
        depth=trunk_depth
    )
    # Move trunk so base rests at Z=0
    bmesh.ops.translate(bm, verts=trunk_geom['verts'], vec=(0, 0, trunk_depth / 2.0))
    
    # Assign material index 0 to trunk and set flat shading
    for f in bm.faces:
        f.material_index = 0
        f.smooth = False
        
    # === Step 3: Create Foliage Tiers ===
    base_z = 0.8  # Starting height for the first tier
    for i in range(tiers):
        factor = 0.8 ** i
        r1 = 1.2 * factor
        r2 = 0.05 * factor  # Tiny top radius to prevent harsh singular points
        h = 1.2 * factor
        
        tier_geom = bmesh.ops.create_cone(
            bm,
            cap_ends=True,
            cap_tris=False,
            segments=10,
            radius1=r1,
            radius2=r2,
            depth=h
        )
        
        tier_verts = tier_geom['verts']
        
        # Rotate around local Z to break symmetry
        rot_angle = math.radians(i * 35.0)
        rot_mat = Matrix.Rotation(rot_angle, 4, 'Z')
        bmesh.ops.transform(bm, matrix=rot_mat, verts=tier_verts)
        
        # Add a slight organic tilt on X axis
        tilt_angle = math.radians(6.0 * (1 if i % 2 == 0 else -1))
        tilt_mat = Matrix.Rotation(tilt_angle, 4, 'X')
        bmesh.ops.transform(bm, matrix=tilt_mat, verts=tier_verts)
        
        # Translate tier to the correct height
        z_center = base_z + h / 2.0
        bmesh.ops.translate(bm, verts=tier_verts, vec=(0, 0, z_center))
        
        # Identify new faces to assign the foliage material index
        tier_faces = set(f for v in tier_verts for f in v.link_faces)
        for f in tier_faces:
            f.material_index = 1
            f.smooth = False
            
        base_z += h * 0.55  # Calculate overlap for the next tier up
        
    # Finalize Bmesh
    bm.to_mesh(mesh)
    bm.free()
    
    # === Step 4: Build Materials ===
    # Trunk Material
    mat_trunk = bpy.data.materials.new(f"{object_name}_Trunk")
    mat_trunk.use_nodes = True
    bsdf_trunk = mat_trunk.node_tree.nodes.get("Principled BSDF")
    if bsdf_trunk:
        bsdf_trunk.inputs["Base Color"].default_value = (*trunk_color, 1.0)
        bsdf_trunk.inputs["Roughness"].default_value = 0.9
        
    # Foliage Material
    mat_leaf = bpy.data.materials.new(f"{object_name}_Leaves")
    mat_leaf.use_nodes = True
    bsdf_leaf = mat_leaf.node_tree.nodes.get("Principled BSDF")
    if bsdf_leaf:
        bsdf_leaf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf_leaf.inputs["Roughness"].default_value = 0.9
        
    obj.data.materials.append(mat_trunk)
    obj.data.materials.append(mat_leaf)
    
    # === Step 5: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))
    
    return f"Created '{obj.name}' at {location} with {tiers} foliage tiers."
