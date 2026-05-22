def create_object(
    scene_name: str = "Scene",
    object_name: str = "CookieScene",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.824, 0.620, 0.396), # Cookie Base Color
    **kwargs,
) -> str:
    """
    Create a Chocolate Chip Cookie on a tray with an area light in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created master object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the cookie.
        **kwargs: 
            num_chips (int): Number of chocolate chips to scatter (default: 12).
            tray_color (tuple): RGB color for the tray.
            chip_color (tuple): RGB color for the chips.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector, Euler

    # Retrieve kwargs
    num_chips = kwargs.get("num_chips", 12)
    tray_color = kwargs.get("tray_color", (0.15, 0.25, 0.65))
    chip_color = kwargs.get("chip_color", (0.12, 0.04, 0.01))

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection

    # === Step 1: Master Empty for Composition ===
    master = bpy.data.objects.new(object_name, None)
    master.empty_display_type = 'PLAIN_AXES'
    master.location = Vector(location)
    master.scale = (scale, scale, scale)
    collection.objects.link(master)

    # === Step 2: Create Tray ===
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    tray = bpy.context.active_object
    tray.name = f"{object_name}_Tray"
    tray.scale = (2.5, 2.5, 0.1)
    
    # Apply scale so bmesh inset thickness is uniform
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # BMesh operations for tray lip (Inset + Translate down)
    bm = bmesh.new()
    bm.from_mesh(tray.data)
    bm.faces.ensure_lookup_table()
    
    # Find the top face (normal pointing up +Z)
    top_face = next((f for f in bm.faces if f.normal.z > 0.9), None)
    if top_face:
        # Inset the top face
        bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.1)
        # Translate the resulting inner face downwards to create a lip
        bmesh.ops.translate(bm, vec=(0.0, 0.0, -0.05), verts=top_face.verts)
        
    bm.to_mesh(tray.data)
    bm.free()
    tray.parent = master

    # === Step 3: Create Cookie Base ===
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1.0, depth=0.2)
    cookie = bpy.context.active_object
    cookie.name = f"{object_name}_Base"
    # Position cookie so its bottom sits flat on the tray's inner face (Z=0.0 relative)
    cookie.location.z = 0.1 
    
    # Shade smooth
    for poly in cookie.data.polygons:
        poly.use_smooth = True
    cookie.parent = master

    # === Step 4: Create and Scatter Chips ===
    # Shared material for all chips
    chip_mat = bpy.data.materials.new(name=f"{object_name}_ChipMat")
    chip_mat.use_nodes = True
    chip_bsdf = chip_mat.node_tree.nodes.get("Principled BSDF")
    if chip_bsdf:
        chip_bsdf.inputs["Base Color"].default_value = (*chip_color, 1.0)
        chip_bsdf.inputs["Roughness"].default_value = 0.6

    cookie_radius = 1.0
    for i in range(num_chips):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.08)
        chip = bpy.context.active_object
        chip.name = f"{object_name}_Chip_{i}"
        
        for poly in chip.data.polygons:
            poly.use_smooth = True
            
        chip.data.materials.append(chip_mat)
        
        # Random circular distribution logic
        angle = random.uniform(0, 2 * math.pi)
        # Keep chips slightly away from the absolute edge of the cookie
        dist = random.uniform(0, cookie_radius * 0.75) 
        
        x = math.cos(angle) * dist
        y = math.sin(angle) * dist
        # Z-height: top of cookie is at 0.2 local, add slight random variance
        z = 0.2 + random.uniform(-0.01, 0.03) 
        
        chip.location = (x, y, z)
        chip.parent = master # Parent to master so they scale together correctly

    # === Step 5: Materials for Tray and Cookie ===
    tray_mat = bpy.data.materials.new(name=f"{object_name}_TrayMat")
    tray_mat.use_nodes = True
    tray_bsdf = tray_mat.node_tree.nodes.get("Principled BSDF")
    if tray_bsdf:
        tray_bsdf.inputs["Base Color"].default_value = (*tray_color, 1.0)
    tray.data.materials.append(tray_mat)

    cookie_mat = bpy.data.materials.new(name=f"{object_name}_CookieMat")
    cookie_mat.use_nodes = True
    cookie_bsdf = cookie_mat.node_tree.nodes.get("Principled BSDF")
    if cookie_bsdf:
        cookie_bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        cookie_bsdf.inputs["Roughness"].default_value = 0.8
    cookie.data.materials.append(cookie_mat)

    # === Step 6: Add Lighting ===
    light_data = bpy.data.lights.new(name=f"{object_name}_AreaLight", type='AREA')
    light_data.energy = 800.0
    light_data.color = (1.0, 0.85, 0.7) # Warm temperature (~4000K)
    light_data.size = 2.0

    light_obj = bpy.data.objects.new(name=f"{object_name}_AreaLight", object_data=light_data)
    collection.objects.link(light_obj)
    
    light_obj.parent = master
    light_obj.location = Vector((0.0, -2.0, 3.0))
    light_obj.rotation_euler = Euler((math.radians(45), 0, 0), 'XYZ')

    # De-select all to leave scene clean
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created '{object_name}' (Cookie, {num_chips} chips, Tray, and Area Light) at {location} with scale {scale}."
