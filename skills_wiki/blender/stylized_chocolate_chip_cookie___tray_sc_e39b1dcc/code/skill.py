def create_object(
    scene_name: str = "Scene",
    object_name: str = "CookieScene",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.53, 0.28, 0.1),
    **kwargs,
) -> str:
    """
    Create a Stylized Chocolate Chip Cookie on a Baking Tray in the active scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the cookie dough.
        **kwargs: Additional overrides.

    Returns:
        Status string
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Root Hierarchy Setup ===
    parent_empty = bpy.data.objects.new(object_name, None)
    scene.collection.objects.link(parent_empty)
    parent_empty.location = location
    parent_empty.scale = (scale, scale, scale)

    # === Step 2: Material Generation ===
    def make_material(name, color, roughness):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Handle alpha safely
            bsdf.inputs["Base Color"].default_value = (*color[:3], 1.0)
            bsdf.inputs["Roughness"].default_value = roughness
        return mat

    mat_cookie = make_material(f"{object_name}_CookieMat", material_color, 0.85)
    mat_chip = make_material(f"{object_name}_ChipMat", (0.02, 0.01, 0.005), 0.3)
    mat_tray = make_material(f"{object_name}_TrayMat", (0.07, 0.27, 0.6), 0.2)

    # === Step 3: Tray Geometry via BMesh ===
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    # Flatten and widen the cube
    bmesh.ops.scale(bm, vec=(3.0, 3.0, 0.2), verts=bm.verts)
    # Move so base is at Z=0, top face is at Z=0.2
    bmesh.ops.translate(bm, vec=(0, 0, 0.1), verts=bm.verts)

    top_face = None
    for f in bm.faces:
        if f.normal.z > 0.9:
            top_face = f
            break

    if top_face:
        # Inset top face to create the rim
        bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.15)
        # Push the inner face down to create the tray depth and sloped edges
        bmesh.ops.translate(bm, vec=(0, 0, -0.15), verts=top_face.verts)

    me_tray = bpy.data.meshes.new(f"{object_name}_Tray")
    bm.to_mesh(me_tray)
    bm.free()

    tray_obj = bpy.data.objects.new(f"{object_name}_Tray", me_tray)
    scene.collection.objects.link(tray_obj)
    tray_obj.parent = parent_empty
    tray_obj.data.materials.append(mat_tray)

    # Smooth shading & bevel for the tray
    for poly in tray_obj.data.polygons:
        poly.use_smooth = True
    bevel_tray = tray_obj.modifiers.new("Bevel", 'BEVEL')
    bevel_tray.width = 0.02
    bevel_tray.segments = 3

    # === Step 4: Cookie Base Geometry ===
    # Placed sitting in the tray (Z = 0.05 + half depth)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.9, depth=0.15, location=(0, 0, 0.125))
    cookie_obj = bpy.context.active_object
    cookie_obj.name = f"{object_name}_Base"
    cookie_obj.parent = parent_empty
    cookie_obj.data.materials.append(mat_cookie)

    for poly in cookie_obj.data.polygons:
        poly.use_smooth = True
    bevel_cookie = cookie_obj.modifiers.new("Bevel", 'BEVEL')
    bevel_cookie.width = 0.04
    bevel_cookie.segments = 4

    # === Step 5: Chocolate Chip Scattering ===
    random.seed(42)  # Seed for stable visual reproduction
    num_chips = 15
    for i in range(num_chips):
        r = random.uniform(0.0, 0.75)
        theta = random.uniform(0.0, 2.0 * math.pi)
        
        # Convert polar to Cartesian for placement
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        z = 0.2 + random.uniform(-0.01, 0.02)  # Top surface of the cookie
        
        radius = random.uniform(0.04, 0.07)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(x, y, z))
        chip = bpy.context.active_object
        chip.name = f"{object_name}_Chip_{i}"
        chip.parent = parent_empty
        chip.data.materials.append(mat_chip)
        
        for poly in chip.data.polygons:
            poly.use_smooth = True
            
        # Give organic irregularity
        chip.rotation_euler = (
            random.uniform(0, math.pi),
            random.uniform(0, math.pi),
            random.uniform(0, math.pi)
        )
        chip.scale = (1.0, random.uniform(0.8, 1.2), random.uniform(0.5, 0.8))

    # === Step 6: Targeted Lighting ===
    light_data = bpy.data.lights.new(name=f"{object_name}_Light", type='AREA')
    light_data.energy = 800.0
    light_data.color = (1.0, 0.85, 0.7)  # Warm tungsten
    light_data.size = 2.0
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_LightObj", object_data=light_data)
    scene.collection.objects.link(light_obj)
    light_obj.parent = parent_empty
    
    # Position light off-center and point it at the cookie
    light_obj.location = (2.0, -2.0, 3.0)
    target_pos = Vector((0, 0, 0.1))
    direction = target_pos - Vector(light_obj.location)
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    # Deselect all to finish cleanly
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created '{object_name}' (Tray, Cookie Base, {num_chips} Chips, Area Light) at {location}"
