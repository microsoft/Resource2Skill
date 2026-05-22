def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyWell",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.2, 0.1),  # Default roof color (Reddish)
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Well game asset in the active Blender scene.
    Demonstrates block-out modeling and modular primitive construction.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object hierarchy.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the roof tiles.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    # 1. Scene & Context Setup
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # 2. Material Helper
    def get_or_create_mat(name, color, roughness):
        mat = bpy.data.materials.get(name)
        if not mat:
            mat = bpy.data.materials.new(name)
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                # Ensure alpha is 1.0
                bsdf.inputs["Base Color"].default_value = (*color[:3], 1.0)
                bsdf.inputs["Roughness"].default_value = roughness
        return mat

    mat_stone = get_or_create_mat("LowPoly_Stone", (0.45, 0.45, 0.45), 0.9)
    mat_wood = get_or_create_mat("LowPoly_Wood", (0.20, 0.12, 0.06), 0.95)
    mat_roof = get_or_create_mat("LowPoly_Roof", material_color, 0.8)
    mat_water = get_or_create_mat("LowPoly_Water", (0.05, 0.25, 0.60), 0.1)
    mat_metal = get_or_create_mat("LowPoly_Metal", (0.2, 0.2, 0.2), 0.4)

    # 3. Create Root Hierarchy Empty
    root = bpy.data.objects.new(object_name, None)
    scene.collection.objects.link(root)
    
    # 4. Mesh Part Builder
    parts_created = 0
    def add_part(primitive_op, name, mat, loc, scale_vec, rot=(0,0,0), **kwargs):
        nonlocal parts_created
        primitive_op(**kwargs)
        obj = bpy.context.active_object
        obj.name = f"{object_name}_{name}"
        
        # Transform relative to local zero
        obj.location = loc
        obj.rotation_euler = rot
        obj.scale = scale_vec
        
        # Shade flat for low poly aesthetic
        bpy.ops.object.shade_flat()
        
        # Parent and apply material
        obj.parent = root
        if mat:
            obj.data.materials.append(mat)
            
        parts_created += 1
        return obj

    # --- Constructing the Asset ---
    
    # A. Stone Base (Hollowed using Solidify)
    base = add_part(
        bpy.ops.mesh.primitive_cylinder_add, 
        "Base", mat_stone, (0, 0, 0.5), (1.0, 1.0, 1.0),
        vertices=12, radius=1.2, depth=1.0, end_fill_type='NOTHING'
    )
    mod = base.modifiers.new(name="Solidify", type='SOLIDIFY')
    mod.thickness = 0.3
    mod.offset = -1.0 # Thicken inward
    
    # B. Water Surface
    add_part(
        bpy.ops.mesh.primitive_cylinder_add,
        "Water", mat_water, (0, 0, 0.6), (1.0, 1.0, 1.0),
        vertices=12, radius=0.9, depth=0.1
    )

    # C. Wooden Pillars
    add_part(
        bpy.ops.mesh.primitive_cube_add,
        "Pillar_L", mat_wood, (0, -1.0, 1.5), (0.15, 0.15, 1.5), size=1.0
    )
    add_part(
        bpy.ops.mesh.primitive_cube_add,
        "Pillar_R", mat_wood, (0, 1.0, 1.5), (0.15, 0.15, 1.5), size=1.0
    )

    # D. Top Crossbeam
    add_part(
        bpy.ops.mesh.primitive_cylinder_add,
        "Beam", mat_wood, (0, 0, 2.9), (1.0, 1.0, 1.0), rot=(math.radians(90), 0, 0),
        vertices=8, radius=0.12, depth=2.8
    )

    # E. Angled Roof Tiles
    add_part(
        bpy.ops.mesh.primitive_cube_add,
        "Roof_L", mat_roof, (0, -0.65, 3.4), (1.4, 0.9, 0.1), rot=(math.radians(35), 0, 0), size=1.0
    )
    add_part(
        bpy.ops.mesh.primitive_cube_add,
        "Roof_R", mat_roof, (0, 0.65, 3.4), (1.4, 0.9, 0.1), rot=(math.radians(-35), 0, 0), size=1.0
    )

    # F. Crank Handle & Rope
    add_part(
        bpy.ops.mesh.primitive_cylinder_add,
        "Crank", mat_metal, (0, -1.3, 2.9), (1.0, 1.0, 1.0), rot=(math.radians(90), 0, 0),
        vertices=6, radius=0.04, depth=0.4
    )
    add_part(
        bpy.ops.mesh.primitive_cylinder_add,
        "Rope", mat_stone, (0, 0.3, 2.0), (1.0, 1.0, 1.0),
        vertices=6, radius=0.03, depth=1.8
    )

    # G. Bucket
    bucket = add_part(
        bpy.ops.mesh.primitive_cylinder_add,
        "Bucket", mat_wood, (0, 0.3, 1.0), (1.0, 1.0, 1.0),
        vertices=10, radius=0.2, depth=0.4, end_fill_type='NOTHING'
    )
    mod_b = bucket.modifiers.new(name="Solidify", type='SOLIDIFY')
    mod_b.thickness = 0.03
    mod_b.offset = -1.0
    add_part(
        bpy.ops.mesh.primitive_cylinder_add,
        "Bucket_Water", mat_water, (0, 0.3, 1.1), (1.0, 1.0, 1.0),
        vertices=10, radius=0.18, depth=0.05
    )

    # 5. Apply Global Transforms to Root
    root.location = Vector(location)
    root.scale = (scale, scale, scale)

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')
    root.select_set(True)
    bpy.context.view_layer.objects.active = root

    return f"Created '{object_name}' (Stylized Game Asset) at {location} consisting of {parts_created} modular pieces."
