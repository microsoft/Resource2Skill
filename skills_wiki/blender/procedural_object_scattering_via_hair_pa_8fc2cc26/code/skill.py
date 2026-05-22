def create_object(
    scene_name: str = "Scene",
    object_name: str = "ScatteredForest",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.25, 0.1),
    density: int = 400,
    **kwargs,
) -> str:
    """
    Create a procedural scattered forest using a Hair Particle System.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the ground emitter object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the ground plane.
        material_color: (R, G, B) base color for the ground.
        density: Number of scattered objects to emit.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector
    
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === 1. Create Collection for instances (Hidden from View Layer) ===
    # By creating the collection but NOT linking it to scene.collection, 
    # the base objects remain hidden, but the particle system can still instance them.
    scatter_col = bpy.data.collections.new(f"{object_name}_Assets")
    
    # === 2. Create Low-Poly Pine Tree Prototype ===
    mesh_tree = bpy.data.meshes.new("TreeMesh")
    tree = bpy.data.objects.new("ScatterTree", mesh_tree)
    scatter_col.objects.link(tree)
    
    bm = bmesh.new()
    
    # Trunk
    trunk_geom = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=8, radius1=0.2, radius2=0.15, depth=1.0)
    bmesh.ops.translate(bm, verts=trunk_geom['verts'], vec=(0, 0, 0.5))
    
    # Leaves Tier 1
    l1_geom = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=8, radius1=1.0, radius2=0.0, depth=1.5)
    bmesh.ops.translate(bm, verts=l1_geom['verts'], vec=(0, 0, 1.5))
    
    # Leaves Tier 2
    l2_geom = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=8, radius1=0.75, radius2=0.0, depth=1.2)
    bmesh.ops.translate(bm, verts=l2_geom['verts'], vec=(0, 0, 2.2))
    
    # Assign Material Indices
    trunk_verts = set(trunk_geom['verts'])
    for f in bm.faces:
        if f.verts[0] in trunk_verts:
            f.material_index = 0
        else:
            f.material_index = 1
            
    bm.to_mesh(mesh_tree)
    bm.free()
    
    # Tree Materials
    mat_trunk = bpy.data.materials.new("Mat_Trunk")
    mat_trunk.use_nodes = True
    mat_trunk.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.05, 0.02, 0.005, 1.0)
    tree.data.materials.append(mat_trunk)
    
    mat_leaves = bpy.data.materials.new("Mat_Leaves")
    mat_leaves.use_nodes = True
    mat_leaves.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.02, 0.15, 0.05, 1.0)
    tree.data.materials.append(mat_leaves)
    
    # === 3. Create Low-Poly Rock Prototype ===
    mesh_rock = bpy.data.meshes.new("RockMesh")
    rock = bpy.data.objects.new("ScatterRock", mesh_rock)
    scatter_col.objects.link(rock)
    
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.5)
    
    # Randomize vertices and flatten bottom
    random.seed(42)
    for v in bm.verts:
        v.co.x += random.uniform(-0.1, 0.1)
        v.co.y += random.uniform(-0.1, 0.1)
        v.co.z += random.uniform(-0.1, 0.1)
        if v.co.z < 0:
            v.co.z = 0
            
    bmesh.ops.scale(bm, vec=(1.5, 1.2, 0.8), verts=bm.verts)
    bm.to_mesh(mesh_rock)
    bm.free()
    
    mat_rock = bpy.data.materials.new("Mat_Rock")
    mat_rock.use_nodes = True
    mat_rock.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.2, 0.2, 0.2, 1.0)
    rock.data.materials.append(mat_rock)
    
    # === 4. Create Ground Terrain Emitter ===
    mesh_ground = bpy.data.meshes.new(f"{object_name}_Mesh")
    ground = bpy.data.objects.new(object_name, mesh_ground)
    scene.collection.objects.link(ground)
    
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=20, y_segments=20, size=15.0)
    
    # Slight procedural displacement for organic terrain
    for v in bm.verts:
        v.co.z += math.sin(v.co.x * 0.5) * math.cos(v.co.y * 0.5) * 0.8
        
    bm.to_mesh(mesh_ground)
    bm.free()
    
    ground.location = Vector(location)
    ground.scale = (scale, scale, scale)
    
    mat_ground = bpy.data.materials.new("Mat_Ground")
    mat_ground.use_nodes = True
    mat_ground.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*material_color, 1.0)
    mat_ground.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9
    ground.data.materials.append(mat_ground)
    
    # === 5. Set up Hair Particle Scatter System ===
    psys_mod = ground.modifiers.new("ScatterSys", type='PARTICLE_SYSTEM')
    psys = ground.particle_systems[0]
    pset = psys.settings
    
    # Core settings
    pset.type = 'HAIR'
    pset.count = density
    pset.hair_length = 1.0
    
    # Rendering instances
    pset.render_type = 'COLLECTION'
    pset.instance_collection = scatter_col
    pset.use_collection_pick_random = True
    
    # Advanced Orientation Settings (Trees point straight up)
    pset.use_advanced_hair = True
    pset.use_rotations = True
    pset.rotation_mode = 'GLOB_Z'
    pset.phase_factor_random = 2.0  # Randomize Z rotation phase so trees face different ways
    
    # Scale Randomization
    pset.particle_size = 1.0
    pset.size_random = 0.6
    
    return f"Created '{object_name}' at {location} scattering {density} stylized trees and rocks."
