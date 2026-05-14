def create_object(
    scene_name: str = "Scene",
    object_name: str = "CookieTray",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    tray_color: tuple = (0.1, 0.2, 0.8, 1.0),
    cookie_color: tuple = (0.6, 0.35, 0.15, 1.0),
    chip_color: tuple = (0.15, 0.05, 0.02, 1.0),
    **kwargs,
) -> str:
    """
    Create a composite Stylized Cookie on a Tray prop.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the root tray object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        tray_color: (R, G, B, A) color for the tray.
        cookie_color: (R, G, B, A) color for the cookie base.
        chip_color: (R, G, B, A) color for the chocolate chips.
        **kwargs: Optional overrides (e.g., 'num_chips').

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import random
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    num_chips = kwargs.get("num_chips", 14)

    # --- Helper: Material Generation ---
    def make_material(name, rgba_color):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = rgba_color
            bsdf.inputs['Roughness'].default_value = 0.6
        return mat

    mat_tray = make_material(f"{object_name}_TrayMat", tray_color)
    mat_cookie = make_material(f"{object_name}_CookieMat", cookie_color)
    mat_chip = make_material(f"{object_name}_ChipMat", chip_color)

    # --- Step 1: Create the Tray ---
    bpy.ops.mesh.primitive_cube_add(size=2.0)
    tray = bpy.context.active_object
    tray.name = object_name
    
    # Flatten and widen the cube into a tray shape
    tray.scale = (1.5, 1.5, 0.15) 
    bpy.ops.object.transform_apply(scale=True)
    tray.data.materials.append(mat_tray)

    # Use BMesh to hollow out the tray (Inset top face, translate down)
    bm = bmesh.new()
    bm.from_mesh(tray.data)
    bm.faces.ensure_lookup_table()
    
    # Identify the top-facing polygon
    top_face = max(bm.faces, key=lambda f: f.calc_center_bounds().z)
    
    # Inset to create a rim (thickness = 0.15m relative to scale)
    bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.15)
    
    # Translate the inset face downwards to create the bowl/floor
    bmesh.ops.translate(bm, vec=(0, 0, -0.15), verts=top_face.verts)
    
    bm.to_mesh(tray.data)
    bm.free()

    # --- Step 2: Create the Cookie Base ---
    bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=0.2)
    cookie = bpy.context.active_object
    cookie.name = f"{object_name}_CookieBase"
    
    # Smooth shading for a baked look
    for poly in cookie.data.polygons:
        poly.use_smooth = True
        
    cookie.data.materials.append(mat_cookie)
    
    # Parent the cookie to the tray
    cookie.parent = tray
    
    # Align Cookie resting on the Tray's inside floor
    # Tray local Z floor is at 0.0 (top is 0.15, translated down by 0.15)
    # Cookie depth is 0.2, so an origin at Z=0.1 rests its bottom at Z=0.0
    cookie.location = Vector((0, 0, 0.1))

    # --- Step 3: Create & Scatter Chocolate Chips ---
    chip_radius = 0.08
    for i in range(num_chips):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=chip_radius)
        chip = bpy.context.active_object
        chip.name = f"{object_name}_Chip_{i:02d}"
        
        for poly in chip.data.polygons:
            poly.use_smooth = True
            
        chip.data.materials.append(mat_chip)
        chip.parent = cookie
        
        # Calculate random position within the cookie's circular radius
        r = random.uniform(0.0, 0.85)  # Leave a slight margin from edge
        theta = random.uniform(0, 2 * math.pi)
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        
        # Embed chips at slightly randomized depths into the top of the cookie
        # Cookie top surface is local Z=0.1 relative to its origin
        z = 0.1 + random.uniform(-0.02, 0.03) 
        
        chip.location = Vector((x, y, z))
        
        # Assign random rotations so the spheres sit irregularly
        chip.rotation_euler = (
            random.uniform(0, math.pi * 2),
            random.uniform(0, math.pi * 2),
            random.uniform(0, math.pi * 2)
        )

    # --- Step 4: Global Placement ---
    tray.location = Vector(location)
    tray.scale = Vector((scale, scale, scale))

    # Clean up context
    bpy.ops.object.select_all(action='DESELECT')
    tray.select_set(True)
    bpy.context.view_layer.objects.active = tray

    return f"Created stylzed prop '{object_name}' (1 Tray, 1 Cookie, {num_chips} Chips) at {location} with scale {scale}"
