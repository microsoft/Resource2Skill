def create_export_ready_antenna(
    scene_name: str = "Scene",
    object_name: str = "GameReady_Antenna",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.2, 0.2),
    **kwargs,
) -> str:
    """
    Creates a game-ready Sci-Fi Antenna prop structured for easy FBX export.
    The object origin is perfectly aligned to the base, and materials are 
    kept simple for direct game engine compatibility.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space placement.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the metal structure.
        **kwargs: Optional 'emissive_color' tuple (default orange/red).

    Returns:
        Status string describing the generated object.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector, Matrix

    # Setup Scene & Object
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # === Step 1: Engine-Safe Materials ===
    # 1. Base Metal
    mat_metal = bpy.data.materials.new(name=f"{object_name}_Metal")
    mat_metal.use_nodes = True
    bsdf_metal = mat_metal.node_tree.nodes.get("Principled BSDF")
    if bsdf_metal:
        bsdf_metal.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf_metal.inputs["Metallic"].default_value = 0.8
        bsdf_metal.inputs["Roughness"].default_value = 0.3

    # 2. Emissive Core
    emissive_color = kwargs.get("emissive_color", (1.0, 0.3, 0.0))
    mat_glow = bpy.data.materials.new(name=f"{object_name}_Glow")
    mat_glow.use_nodes = True
    bsdf_glow = mat_glow.node_tree.nodes.get("Principled BSDF")
    if bsdf_glow:
        # Cross-version compatibility for Emission
        if "Emission Color" in bsdf_glow.inputs:  # Blender 4.0+
            bsdf_glow.inputs["Emission Color"].default_value = (*emissive_color, 1.0)
            bsdf_glow.inputs["Emission Strength"].default_value = 5.0
        elif "Emission" in bsdf_glow.inputs:      # Blender 3.x
            bsdf_glow.inputs["Emission"].default_value = (*emissive_color, 1.0)
            bsdf_glow.inputs["Emission Strength"].default_value = 5.0

    obj.data.materials.append(mat_metal)  # Index 0
    obj.data.materials.append(mat_glow)   # Index 1

    # === Step 2: Bmesh Construction with strict pivot alignment ===
    bm = bmesh.new()

    def add_shape(shape_type, mat_idx, matrix, **shape_args):
        faces_before = set(bm.faces)
        if shape_type == 'cone':
            bmesh.ops.create_cone(bm, matrix=matrix, **shape_args)
        elif shape_type == 'cube':
            bmesh.ops.create_cube(bm, matrix=matrix, **shape_args)
        
        # Assign material index to newly created faces
        for f in set(bm.faces) - faces_before:
            f.material_index = mat_idx

    # Center is Z=0. All vertical offsets build UPWARD from the base.
    
    # 1. Base Plate
    add_shape('cone', 0, Matrix.Translation((0, 0, 0.2)), segments=16, radius1=0.8, radius2=0.7, depth=0.4, cap_ends=True, cap_tris=False)
    add_shape('cone', 0, Matrix.Translation((0, 0, 0.45)), segments=16, radius1=0.7, radius2=0.4, depth=0.1, cap_ends=True, cap_tris=False)
    
    # 2. Main Shaft
    add_shape('cone', 0, Matrix.Translation((0, 0, 2.0)), segments=12, radius1=0.15, radius2=0.15, depth=3.0, cap_ends=True, cap_tris=False)
    
    # 3. Lower Support Dish
    add_shape('cone', 0, Matrix.Translation((0, 0, 3.6)), segments=16, radius1=0.15, radius2=0.6, depth=0.2, cap_ends=True, cap_tris=False)
    
    # 4. Emissive Power Core
    add_shape('cone', 1, Matrix.Translation((0, 0, 4.3)), segments=12, radius1=0.2, radius2=0.2, depth=1.2, cap_ends=True, cap_tris=False)
    
    # 5. Top Cap
    add_shape('cone', 0, Matrix.Translation((0, 0, 4.95)), segments=16, radius1=0.25, radius2=0.05, depth=0.1, cap_ends=True, cap_tris=False)
    add_shape('cone', 0, Matrix.Translation((0, 0, 5.25)), segments=8, radius1=0.05, radius2=0.01, depth=0.5, cap_ends=True, cap_tris=False)

    # 6. Array of Vertical Blades around the emissive core
    for i in range(4):
        angle = i * (math.pi / 2)
        dist = 0.3
        
        loc_mat = Matrix.Translation((math.cos(angle) * dist, math.sin(angle) * dist, 4.3))
        rot_mat = Matrix.Rotation(angle, 4, 'Z')
        scale_mat = Matrix.Diagonal((0.4, 0.05, 1.4, 1.0)) # Width, thickness, height
        
        # Scale, then rotate, then translate
        matrix = loc_mat @ rot_mat @ scale_mat
        add_shape('cube', 0, matrix, size=1.0)

    # === Step 3: Finalize ===
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()

    # Flat shading gives a clean stylized look suitable for low-poly game assets
    for poly in mesh.polygons:
        poly.use_smooth = False

    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created Engine-Ready Prop '{object_name}' with optimized pivot at {location}"
