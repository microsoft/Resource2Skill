def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyTree",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    leaf_color: tuple = (0.1, 0.45, 0.15),
    trunk_color: tuple = (0.25, 0.12, 0.05),
    **kwargs,
) -> str:
    """
    Creates a procedural, stylized low-poly tree using the 'Crumple and Collapse' method.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        leaf_color: (R, G, B) color for the canopy.
        trunk_color: (R, G, B) color for the wood base.
        
    Returns:
        Status string confirming creation.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math
    import random

    # Get target scene and collection
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection

    # === 1. Create Parent Empty ===
    parent_empty = bpy.data.objects.new(object_name, None)
    collection.objects.link(parent_empty)

    # === 2. Create Trunk (8-sided tapered cylinder/cone) ===
    bm_trunk = bmesh.new()
    bmesh.ops.create_cone(
        bm_trunk, 
        cap_ends=True, 
        cap_tris=False, 
        segments=8, 
        radius1=0.3, 
        radius2=0.15, 
        depth=2.0
    )
    # Move base to local Z=0
    bmesh.ops.translate(bm_trunk, verts=bm_trunk.verts, vec=(0, 0, 1.0)) 
    me_trunk = bpy.data.meshes.new(f"{object_name}_Trunk_Mesh")
    bm_trunk.to_mesh(me_trunk)
    bm_trunk.free()

    trunk_obj = bpy.data.objects.new(f"{object_name}_Trunk", me_trunk)
    trunk_obj.parent = parent_empty
    collection.objects.link(trunk_obj)

    # === 3. Create Canopy (Dense base for displacement) ===
    bm_canopy = bmesh.new()
    bmesh.ops.create_icosphere(bm_canopy, subdivisions=4, radius=1.6)
    me_canopy = bpy.data.meshes.new(f"{object_name}_Canopy_Mesh")
    bm_canopy.to_mesh(me_canopy)
    bm_canopy.free()

    canopy_obj = bpy.data.objects.new(f"{object_name}_Canopy", me_canopy)
    canopy_obj.parent = parent_empty
    canopy_obj.location = (0, 0, 2.4) # Overlap with the top of the trunk
    
    # Apply random rotation to make each instance unique when scattered
    canopy_obj.rotation_euler = (
        random.uniform(0, math.pi),
        random.uniform(0, math.pi),
        random.uniform(0, math.pi)
    )
    collection.objects.link(canopy_obj)

    # === 4. Apply Modifiers for the Stylized Low-Poly Look ===
    # Procedural Noise Texture
    tex_name = f"{object_name}_DisplaceTex_{random.randint(1000,9999)}"
    tex = bpy.data.textures.new(tex_name, type='CLOUDS')
    tex.noise_scale = random.uniform(0.8, 1.3) # Randomize chunk size

    # Displace to make the sphere organic and lumpy
    disp_mod = canopy_obj.modifiers.new(name="Displace", type='DISPLACE')
    disp_mod.texture = tex
    disp_mod.strength = 0.75

    # Decimate to create sharp, chunky facets
    dec_mod = canopy_obj.modifiers.new(name="Decimate", type='DECIMATE')
    dec_mod.ratio = 0.08  # Extremely aggressive reduction

    # Force flat shading (crucial for low poly style)
    for poly in me_canopy.polygons:
        poly.use_smooth = False
    for poly in me_trunk.polygons:
        poly.use_smooth = False

    # === 5. Materials ===
    # Trunk Material
    mat_trunk = bpy.data.materials.new(name=f"{object_name}_Mat_Trunk")
    mat_trunk.use_nodes = True
    bsdf_trunk = mat_trunk.node_tree.nodes.get("Principled BSDF")
    if bsdf_trunk:
        bsdf_trunk.inputs["Base Color"].default_value = (*trunk_color, 1.0)
        bsdf_trunk.inputs["Roughness"].default_value = 0.95
        bsdf_trunk.inputs["Specular IOR Level"].default_value = 0.1
    trunk_obj.data.materials.append(mat_trunk)

    # Leaf/Canopy Material
    mat_leaf = bpy.data.materials.new(name=f"{object_name}_Mat_Leaf")
    mat_leaf.use_nodes = True
    bsdf_leaf = mat_leaf.node_tree.nodes.get("Principled BSDF")
    if bsdf_leaf:
        bsdf_leaf.inputs["Base Color"].default_value = (*leaf_color, 1.0)
        bsdf_leaf.inputs["Roughness"].default_value = 0.85
        bsdf_leaf.inputs["Specular IOR Level"].default_value = 0.1
    canopy_obj.data.materials.append(mat_leaf)

    # === 6. Final Placement ===
    parent_empty.location = Vector(location)
    parent_empty.scale = (scale, scale, scale)

    return f"Created Procedural Low-Poly Tree '{object_name}' with unique seed {tex_name} at {location}"
