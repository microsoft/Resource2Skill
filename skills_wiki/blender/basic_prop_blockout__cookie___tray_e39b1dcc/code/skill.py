def create_object(
    scene_name: str = "Scene",
    object_name: str = "CookieAndTray",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.3, 0.8),  # Default to a nice tray blue
    **kwargs,
) -> str:
    """
    Create a procedural 3D Cookie resting on a Tray in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created objects and root empty.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the whole assembly.
        material_color: (R, G, B) base color for the Tray.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Helper: Material Creation ---
    def make_mat(name, color):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (*color, 1.0)
            # High roughness for baked goods/matte tray
            bsdf.inputs['Roughness'].default_value = 0.85
        return mat

    mat_tray = make_mat(f"{object_name}_TrayMat", material_color)
    mat_cookie = make_mat(f"{object_name}_CookieMat", (0.5, 0.25, 0.08))
    mat_chip = make_mat(f"{object_name}_ChipMat", (0.05, 0.02, 0.01))

    # --- Step 1: Create the Tray ---
    # Default primitive cube is 2x2x2. size=1.0 makes it 1x1x1.
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    tray = bpy.context.active_object
    tray.name = f"{object_name}_Tray"
    tray.scale = (2.0, 2.0, 0.1)  # Final bounds: 2.0 x 2.0 x 0.1. Z goes from -0.05 to +0.05
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    tray.data.materials.append(mat_tray)

    # Use BMesh to inset the top face and extrude it down
    bm = bmesh.new()
    bm.from_mesh(tray.data)
    bm.faces.ensure_lookup_table()
    
    # The top face has a normal pointing straight up (+Z)
    top_face = max(bm.faces, key=lambda f: f.normal.z)

    # Inset (leaves top_face as the inner face)
    bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.1)
    
    # Extrude down to create the tray floor
    extrude_res = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
    floor_face = extrude_res['faces'][0]
    
    # Move the floor down by 0.03 units. (Top was 0.05, floor becomes 0.02)
    bmesh.ops.translate(bm, vec=(0, 0, -0.03), verts=floor_face.verts)

    bm.to_mesh(tray.data)
    bm.free()

    # --- Step 2: Create the Cookie Base ---
    # Tray floor is at Z = 0.02. Cookie depth = 0.15. 
    # Center should be at Z = 0.02 + (0.15 / 2) = 0.095.
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.7, depth=0.15, location=(0, 0, 0.095))
    cookie = bpy.context.active_object
    cookie.name = f"{object_name}_CookieBase"
    cookie.data.materials.append(mat_cookie)
    
    # Shade Smooth
    for poly in cookie.data.polygons:
        poly.use_smooth = True

    # --- Step 3: Create Chocolate Chips ---
    # Cookie top surface is at Z = 0.02 + 0.15 = 0.17
    chips = []
    num_chips = 9
    
    for i in range(num_chips):
        # Distribute randomly within a circle slightly smaller than the cookie radius
        r = random.uniform(0.0, 0.55)
        theta = random.uniform(0, 2 * math.pi)
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        z = 0.17 

        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.06, location=(x, y, z))
        chip = bpy.context.active_object
        chip.name = f"{object_name}_Chip_{i}"
        chip.data.materials.append(mat_chip)
        
        # Flatten slightly and apply random rotation so they sit organically
        chip.scale = (1.0, 1.0, 0.6)
        chip.rotation_euler = (
            random.uniform(-0.3, 0.3),
            random.uniform(-0.3, 0.3),
            random.uniform(0, 2 * math.pi)
        )
        
        # Shade Smooth
        for poly in chip.data.polygons:
            poly.use_smooth = True
            
        chips.append(chip)

    # --- Step 4: Organization and Hierarchy ---
    # Create an empty to act as the root controller
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    root = bpy.context.active_object
    root.name = object_name
    root.scale = (scale, scale, scale)

    # Parent everything to the root
    tray.parent = root
    cookie.parent = root
    for chip in chips:
        chip.parent = root

    # Deselect all to finish cleanly
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created '{object_name}' (Tray, Cookie, and {num_chips} Chips) at {location}."
