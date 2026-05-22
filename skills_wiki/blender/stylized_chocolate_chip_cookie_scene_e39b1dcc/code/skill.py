def create_object(
    scene_name: str = "Scene",
    object_name: str = "ChocolateChipCookie",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.45, 0.2),  # Cookie dough color
    **kwargs,
) -> str:
    """
    Create a Stylized Chocolate Chip Cookie Scene (Cookie, Chips, Tray, and Light).

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the cookie dough.
        **kwargs: 
            chip_color: (R, G, B) for the chocolate chips
            tray_color: (R, G, B) for the tray
            num_chips: Integer number of chips to scatter

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector, Euler
    import math
    import random

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Extract kwargs
    chip_color = kwargs.get("chip_color", (0.1, 0.05, 0.02))
    tray_color = kwargs.get("tray_color", (0.1, 0.2, 0.8))
    num_chips = kwargs.get("num_chips", 15)
    base_loc = Vector(location)

    # --- Helper: Material Creation ---
    def create_simple_mat(name, color):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Ensure Alpha is 1.0
            bsdf.inputs["Base Color"].default_value = (*color, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.6
        return mat

    cookie_mat = create_simple_mat(f"{object_name}_Cookie_Mat", material_color)
    chip_mat = create_simple_mat(f"{object_name}_Chip_Mat", chip_color)
    tray_mat = create_simple_mat(f"{object_name}_Tray_Mat", tray_color)

    # Create a parent Empty to hold the whole composition together
    empty_data = bpy.data.objects.new(name=f"{object_name}_Root", object_data=None)
    empty_data.location = base_loc
    scene.collection.objects.link(empty_data)

    # --- Step 1: Create the Tray using BMesh ---
    tray_mesh = bpy.data.meshes.new(f"{object_name}_Tray_Mesh")
    tray_obj = bpy.data.objects.new(f"{object_name}_Tray", tray_mesh)
    scene.collection.objects.link(tray_obj)
    tray_obj.parent = empty_data
    tray_obj.data.materials.append(tray_mat)

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    
    # Scale tray base
    tray_scale = Vector((scale * 3.0, scale * 3.0, scale * 0.2))
    bmesh.ops.scale(bm, vec=tray_scale, verts=bm.verts)
    
    # Find top face to inset and extrude
    bm.faces.ensure_lookup_table()
    top_face = next((f for f in bm.faces if f.normal.z > 0.9), None)
    if top_face:
        # Inset region
        inset_res = bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.2 * scale)
        # BMesh inset re-uses the original face as the inner face
        # Translate the inner face downwards to create the tray lip
        bmesh.ops.translate(bm, vec=(0, 0, -0.05 * scale), verts=top_face.verts)
        
    bm.to_mesh(tray_mesh)
    bm.free()
    
    # Position tray so its bottom rests at the local Z=0
    tray_obj.location = Vector((0, 0, (scale * 0.1)))

    # --- Step 2: Create the Cookie Base ---
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1.0 * scale, depth=0.2 * scale)
    cookie_obj = bpy.context.active_object
    cookie_obj.name = f"{object_name}_Base"
    cookie_obj.parent = empty_data
    # Sit exactly on the inset tray face
    cookie_obj.location = Vector((0, 0, (scale * 0.2) + (scale * 0.1))) 
    
    # Shade Smooth
    for poly in cookie_obj.data.polygons:
        poly.use_smooth = True
    cookie_obj.data.materials.append(cookie_mat)

    # --- Step 3: Create the Chocolate Chips ---
    # We will procedurally scatter them on the cookie's top surface
    for i in range(num_chips):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08 * scale, segments=16, ring_count=8)
        chip_obj = bpy.context.active_object
        chip_obj.name = f"{object_name}_Chip_{i:02d}"
        chip_obj.parent = cookie_obj
        
        # Shade Smooth
        for poly in chip_obj.data.polygons:
            poly.use_smooth = True
        chip_obj.data.materials.append(chip_mat)
        
        # Random distribution within cookie radius
        r = random.uniform(0.0, 0.85 * scale)
        theta = random.uniform(0.0, 2.0 * math.pi)
        
        c_x = r * math.cos(theta)
        c_y = r * math.sin(theta)
        # Place slightly embedded into the top of the cookie
        c_z = (0.1 * scale) + (0.01 * scale) 
        
        chip_obj.location = Vector((c_x, c_y, c_z))
        
        # Add a random rotation for natural variation
        chip_obj.rotation_euler = Euler((
            random.uniform(0, math.pi),
            random.uniform(0, math.pi),
            random.uniform(0, math.pi)
        ), 'XYZ')

    # --- Step 4: Setup Lighting ---
    light_data = bpy.data.lights.new(name=f"{object_name}_Light", type='AREA')
    light_data.energy = 800.0 * (scale ** 2) # Scale energy logically with object scale
    light_data.color = (1.0, 0.85, 0.7) # Warm temperature (~4000K)
    light_data.shape = 'SQUARE'
    light_data.size = 2.0 * scale
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_AreaLight", object_data=light_data)
    scene.collection.objects.link(light_obj)
    light_obj.parent = empty_data
    
    # Position light above and diagonally offset
    light_obj.location = Vector((-2.0 * scale, -2.0 * scale, 3.0 * scale))
    # Point light towards the cookie
    light_obj.rotation_euler = Euler((math.radians(45), 0, math.radians(-45)), 'XYZ')

    # Deselect all to leave scene clean
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created '{object_name}' scene (Cookie, {num_chips} Chips, Tray, Light) attached to Root Empty at {location}"
