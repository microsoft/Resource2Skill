def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedPineTree",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    leaf_color: tuple = (0.1, 0.35, 0.1),
    trunk_color: tuple = (0.25, 0.12, 0.05),
    num_tiers: int = 3,
    **kwargs,
) -> str:
    """
    Creates a Stylized Low-Poly Pine Tree based on the extrude/scale workflow.
    
    Args:
        scene_name: Name of the scene to add the tree to.
        object_name: Name of the final tree object.
        location: World-space location (x, y, z).
        scale: Overall size of the tree.
        leaf_color: RGB tuple for the foliage.
        trunk_color: RGB tuple for the wood.
        num_tiers: Number of overlapping leaf layers.
        
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector, Matrix
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === 1. Material Setup ===
    mat_trunk_name = f"{object_name}_Trunk_Mat"
    mat_leaf_name = f"{object_name}_Leaf_Mat"
    
    # Create or get trunk material
    mat_trunk = bpy.data.materials.get(mat_trunk_name)
    if not mat_trunk:
        mat_trunk = bpy.data.materials.new(name=mat_trunk_name)
        mat_trunk.use_nodes = True
        bsdf_trunk = mat_trunk.node_tree.nodes.get("Principled BSDF")
        bsdf_trunk.inputs["Base Color"].default_value = (*trunk_color, 1.0)
        bsdf_trunk.inputs["Roughness"].default_value = 0.9

    # Create or get leaf material
    mat_leaf = bpy.data.materials.get(mat_leaf_name)
    if not mat_leaf:
        mat_leaf = bpy.data.materials.new(name=mat_leaf_name)
        mat_leaf.use_nodes = True
        bsdf_leaf = mat_leaf.node_tree.nodes.get("Principled BSDF")
        bsdf_leaf.inputs["Base Color"].default_value = (*leaf_color, 1.0)
        bsdf_leaf.inputs["Roughness"].default_value = 0.85

    # === 2. Mesh Construction via BMesh ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    obj.data.materials.append(mat_trunk) # Index 0
    obj.data.materials.append(mat_leaf)  # Index 1

    bm = bmesh.new()

    # --- Construct Trunk ---
    # Cylinder tapered at the top
    trunk_height = 2.0
    geom_trunk = bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=10, 
        radius1=0.25, radius2=0.1, depth=trunk_height
    )
    # Move trunk up so the base rests exactly on the origin (Z=0)
    trunk_verts = [v for v in geom_trunk['verts']]
    bmesh.ops.translate(bm, vec=(0, 0, trunk_height / 2.0), verts=trunk_verts)

    # --- Construct Foliage Tiers ---
    base_radius = 1.2
    base_height = 1.5
    z_cursor = 0.8 # Starting height for the lowest tier

    for i in range(num_tiers):
        # Each subsequent tier is slightly smaller
        tier_radius = base_radius * (0.8 ** i)
        tier_height = base_height * (0.85 ** i)
        
        # Calculate slight rotation for organic variation, and height placement
        rot_z = math.radians(i * 35.0)
        mat_rot = Matrix.Rotation(rot_z, 4, 'Z')
        mat_trans = Matrix.Translation((0, 0, z_cursor + tier_height / 2.0))
        tier_matrix = mat_trans @ mat_rot
        
        # Create cone (top radius 0.001 to simulate a sharp point)
        geom_tier = bmesh.ops.create_cone(
            bm, cap_ends=True, cap_tris=False, segments=12,
            radius1=tier_radius, radius2=0.001, depth=tier_height,
            matrix=tier_matrix
        )
        
        tier_faces = [f for f in geom_tier['faces'] if isinstance(f, bmesh.types.BMFace)]
        
        # Assign leaf material
        for f in tier_faces:
            f.material_index = 1
            
        # --- Bottom Detailing (The core technique from the video) ---
        # Find the flat bottom face of this newly created cone
        bottom_face = min(tier_faces, key=lambda f: f.calc_center_median().z)
        
        # 1. Extrude face, then scale inwards (X & Y) to create a flat ring
        ext1 = bmesh.ops.extrude_discrete_faces(bm, faces=[bottom_face])
        new_face_1 = ext1['faces'][0]
        bmesh.ops.scale(bm, vec=(0.6, 0.6, 1.0), verts=new_face_1.verts)
        
        # 2. Extrude again, push UP into the mesh along Z, and scale inwards again
        ext2 = bmesh.ops.extrude_discrete_faces(bm, faces=[new_face_1])
        new_face_2 = ext2['faces'][0]
        bmesh.ops.translate(bm, vec=(0, 0, tier_height * 0.25), verts=new_face_2.verts)
        bmesh.ops.scale(bm, vec=(0.5, 0.5, 1.0), verts=new_face_2.verts)
        
        # Move cursor up for the next overlapping tier
        z_cursor += tier_height * 0.55

    # === 3. Finalize Geometry ===
    bm.to_mesh(mesh)
    bm.free()

    # Ensure flat shading for the low-poly look
    for poly in mesh.polygons:
        poly.use_smooth = False

    # Apply Object Transforms
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' (Stylized Pine Tree) at {location} with {num_tiers} foliage tiers."
