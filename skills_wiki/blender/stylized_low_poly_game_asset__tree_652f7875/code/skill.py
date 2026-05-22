def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyTree",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 0.15),  # Foliage Color
    trunk_color: tuple = (0.3, 0.18, 0.1),     # Bark Color
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Tree (Game-Ready Asset) in the active scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the foliage.
        trunk_color: (R, G, B) base color for the trunk.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import random
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name)
    if not scene:
        scene = bpy.context.scene
        
    # === Step 1: Create the Trunk (Game-Ready Origin at Base) ===
    mesh_trunk = bpy.data.meshes.new(f"{object_name}_Trunk_Mesh")
    obj_trunk = bpy.data.objects.new(object_name, mesh_trunk) # Parent object takes the primary name
    scene.collection.objects.link(obj_trunk)
    
    bm_trunk = bmesh.new()
    # Create a 6-sided tapered cylinder
    bmesh.ops.create_cone(
        bm_trunk,
        cap_ends=True,
        cap_tris=False,
        segments=6,
        radius1=0.4,   # Base radius
        radius2=0.15,  # Top radius
        depth=2.0
    )
    
    # Translate mesh UP by half the depth so the object origin is exactly at Z=0
    bmesh.ops.translate(bm_trunk, verts=bm_trunk.verts, vec=(0, 0, 1.0))
    bm_trunk.to_mesh(mesh_trunk)
    bm_trunk.free()
    
    # === Step 2: Create the Foliage ===
    mesh_foliage = bpy.data.meshes.new(f"{object_name}_Foliage_Mesh")
    obj_foliage = bpy.data.objects.new(f"{object_name}_Foliage", mesh_foliage)
    scene.collection.objects.link(obj_foliage)
    
    bm_foliage = bmesh.new()
    # Icosphere provides the perfect triangulated look for low-poly art
    bmesh.ops.create_icosphere(
        bm_foliage,
        subdivisions=1,
        radius=1.3
    )
    
    # Add procedural imperfection by jittering the vertices
    # Seeded by object name to ensure consistent look if regenerated
    random.seed(hash(object_name))
    for v in bm_foliage.verts:
        v.co += Vector((
            random.uniform(-0.15, 0.15),
            random.uniform(-0.15, 0.15),
            random.uniform(-0.15, 0.15)
        ))
        
    # Translate foliage to sit on top of the trunk
    bmesh.ops.translate(bm_foliage, verts=bm_foliage.verts, vec=(0, 0, 2.2))
    bm_foliage.to_mesh(mesh_foliage)
    bm_foliage.free()
    
    # Parent the foliage to the trunk for easy scene manipulation
    obj_foliage.parent = obj_trunk
    
    # === Step 3: Material Setup ===
    # Trunk Material
    mat_trunk = bpy.data.materials.new(name=f"{object_name}_Trunk_Mat")
    mat_trunk.use_nodes = True
    bsdf_trunk = mat_trunk.node_tree.nodes.get("Principled BSDF")
    if bsdf_trunk:
        bsdf_trunk.inputs["Base Color"].default_value = (*trunk_color, 1.0)
        bsdf_trunk.inputs["Roughness"].default_value = 0.9
    obj_trunk.data.materials.append(mat_trunk)
    
    # Foliage Material
    mat_foliage = bpy.data.materials.new(name=f"{object_name}_Foliage_Mat")
    mat_foliage.use_nodes = True
    bsdf_foliage = mat_foliage.node_tree.nodes.get("Principled BSDF")
    if bsdf_foliage:
        bsdf_foliage.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf_foliage.inputs["Roughness"].default_value = 0.8
    obj_foliage.data.materials.append(mat_foliage)
    
    # Note: We deliberately do NOT apply smooth shading. 
    # Flat shading is the desired visual aesthetic for this low-poly skill.
    
    # === Step 4: Finalize Placement ===
    obj_trunk.location = Vector(location)
    obj_trunk.scale = Vector((scale, scale, scale))
    
    return f"Created game-ready asset '{object_name}' (Low-Poly Tree) at {location}."
