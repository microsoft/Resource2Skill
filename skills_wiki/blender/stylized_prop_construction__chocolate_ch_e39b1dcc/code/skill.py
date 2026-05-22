def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedCookieTray",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.76, 0.60, 0.35),
    **kwargs,
) -> str:
    """
    Create a stylized chocolate chip cookie resting on a blue tray.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created object hierarchy.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the cookie dough.
        **kwargs: 
            - num_chips (int): Number of chocolate chips to scatter (default: 15)

    Returns:
        Status string with creation details.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector, Euler

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    num_chips = kwargs.get("num_chips", 15)

    # === Helper: Material Generation ===
    def create_mat(name, color, roughness):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (*color, 1.0)
            bsdf.inputs['Roughness'].default_value = roughness
        return mat

    cookie_mat = create_mat(f"{object_name}_CookieMat", material_color, 0.8)
    chip_mat = create_mat(f"{object_name}_ChipMat", (0.05, 0.025, 0.005), 0.5)
    tray_mat = create_mat(f"{object_name}_TrayMat", (0.05, 0.15, 0.6), 0.3)

    # === Step 1: Root Parent Empty ===
    bpy.ops.object.empty_add(type='PLAIN_AXES')
    root_obj = bpy.context.active_object
    root_obj.name = object_name
    root_obj.location = Vector(location)
    root_obj.scale = (scale, scale, scale)

    # === Step 2: Build the Tray using Bmesh ===
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    tray = bpy.context.active_object
    tray.name = f"{object_name}_Tray"
    
    # Scale to form a wide, flat board
    tray.scale = (4.0, 4.0, 0.2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    bm = bmesh.new()
    bm.from_mesh(tray.data)
    bm.faces.ensure_lookup_table()

    # Find the top face based on normal
    top_face = None
    for f in bm.faces:
        if f.normal.z > 0.9:
            top_face = f
            break

    # Inset and extrude down to create a lip
    if top_face:
        bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.2)
        bmesh.ops.translate(bm, verts=top_face.verts, vec=(0, 0, -0.1))

    bm.to_mesh(tray.data)
    bm.free()

    tray.data.materials.append(tray_mat)
    tray.parent = root_obj
    
    # Position tray so its bottom sits exactly at Z=0 relative to the root
    tray.location = (0, 0, 0.1)

    # === Step 3: Build the Cookie Base ===
    bpy.ops.mesh.primitive_cylinder_add(radius=1.2, depth=0.25, vertices=64)
    cookie = bpy.context.active_object
    cookie.name = f"{object_name}_Cookie"
    
    # Apply smooth shading via data to avoid context overrides
    for poly in cookie.data.polygons:
        poly.use_smooth = True
        
    cookie.data.materials.append(cookie_mat)
    cookie.parent = root_obj
    
    # Position cookie to rest inside the tray's interior floor
    # Tray floor is at local Z=0.1. Half cookie depth is 0.125.
    cookie.location = (0, 0, 0.1 + 0.125)

    # === Step 4: Build & Scatter Chocolate Chips ===
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, segments=16, ring_count=8)
    base_chip = bpy.context.active_object
    base_chip.name = f"{object_name}_Chip_0"
    base_chip.scale = (1.0, 1.0, 0.6) # Squash the chip
    bpy.ops.object.transform_apply(scale=True)
    
    for poly in base_chip.data.polygons:
        poly.use_smooth = True
        
    base_chip.data.materials.append(chip_mat)
    base_chip.parent = cookie

    # Distribute chips
    for i in range(num_chips):
        if i == 0:
            chip = base_chip
        else:
            # Create a linked duplicate for efficiency
            chip = base_chip.copy()
            chip.data = base_chip.data
            chip.name = f"{object_name}_Chip_{i}"
            bpy.context.collection.objects.link(chip)
            chip.parent = cookie
            
        # Random distribution using polar coordinates 
        # (sqrt ensures even distribution, avoiding center clustering)
        r_val = math.sqrt(random.uniform(0.0, 1.0)) * 1.0 
        theta = random.uniform(0, 2 * math.pi)
        
        # Position on top of the cookie surface (Z = 0.125)
        chip.location = (r_val * math.cos(theta), r_val * math.sin(theta), 0.125)
        
        # Slight random rotation for organic imperfection
        chip.rotation_euler = Euler((
            random.uniform(-0.3, 0.3), 
            random.uniform(-0.3, 0.3), 
            random.uniform(0.0, 6.28)
        ))

    return f"Created '{object_name}' (Tray, Cookie, and {num_chips} Chips) successfully at {location}."
