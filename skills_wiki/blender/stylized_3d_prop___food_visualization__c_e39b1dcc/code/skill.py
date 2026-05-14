def create_object(
    scene_name: str = "Scene",
    object_name: str = "KevinCookie",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.5, 0.25, 0.08),  # Cookie base color
    **kwargs,
) -> str:
    """
    Creates a Stylized Chocolate Chip Cookie sitting on a blue tray, 
    illuminated by a warm Area light.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created object hierarchy.
        location: (x, y, z) world-space position for the tray.
        scale: Uniform scale factor for the entire set.
        material_color: Base color for the cookie dough (R, G, B).
        **kwargs: Extensible parameters.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector, Euler

    # Get target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Helper function to create materials
    def create_material(name, color, roughness):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Ensure color has alpha channel
            bsdf.inputs["Base Color"].default_value = (*color, 1.0)
            bsdf.inputs["Roughness"].default_value = roughness
        return mat

    # --- 1. Materials ---
    mat_cookie = create_material(f"{object_name}_Mat_Cookie", material_color, 0.8)
    mat_chip = create_material(f"{object_name}_Mat_Chip", (0.02, 0.01, 0.005), 0.35)
    mat_tray = create_material(f"{object_name}_Mat_Tray", (0.05, 0.15, 0.6), 0.5)

    # --- 2. Root Empty ---
    # Everything is built at origin relative to this root, then the root handles location/scale
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    root = bpy.context.active_object
    root.name = object_name
    root.scale = (scale, scale, scale)

    # --- 3. Tray Creation (Using bmesh for procedural inset) ---
    tray_mesh = bpy.data.meshes.new(f"{object_name}_Tray_Mesh")
    tray_obj = bpy.data.objects.new(f"{object_name}_Tray", tray_mesh)
    scene.collection.objects.link(tray_obj)
    tray_obj.parent = root
    tray_obj.data.materials.append(mat_tray)

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    # Scale to tray proportions (wide and thin)
    bmesh.ops.scale(bm, vec=(3.0, 3.0, 0.2), verts=bm.verts)
    
    # Inset top face to create rim
    top_faces = [f for f in bm.faces if f.normal.z > 0.9]
    if top_faces:
        inset_result = bmesh.ops.inset_region(bm, faces=top_faces, thickness=0.1)
        # Move the new inner face down to create the tray depth
        inner_faces = inset_result.get('faces', [])
        inner_verts = list({v for f in inner_faces for v in f.verts})
        bmesh.ops.translate(bm, vec=(0.0, 0.0, -0.05), verts=inner_verts)

    bm.to_mesh(tray_mesh)
    bm.free()

    # --- 4. Cookie Base Creation ---
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=1.0, depth=0.2, location=(0, 0, 0.2))
    cookie = bpy.context.active_object
    cookie.name = f"{object_name}_Cookie"
    cookie.parent = root
    cookie.data.materials.append(mat_cookie)
    
    # Shade Smooth
    for poly in cookie.data.polygons:
        poly.use_smooth = True

    # --- 5. Chocolate Chips Scattering ---
    chip_count = 14
    for i in range(chip_count):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.12)
        chip = bpy.context.active_object
        chip.name = f"{object_name}_Chip_{i:02d}"
        chip.parent = root
        chip.data.materials.append(mat_chip)
        
        for poly in chip.data.polygons:
            poly.use_smooth = True

        # Scatter math: Random distance and angle on the cookie top
        angle = random.uniform(0, 2 * math.pi)
        # Sqrt ensures uniform distribution over area
        dist = math.sqrt(random.uniform(0, 1)) * 0.8  
        
        chip.location.x = dist * math.cos(angle)
        chip.location.y = dist * math.sin(angle)
        chip.location.z = 0.30  # Sits slightly embedded in the top of the cookie base

        # Randomize rotation for variety
        chip.rotation_euler = Euler((
            random.uniform(0, math.pi),
            random.uniform(0, math.pi),
            random.uniform(0, math.pi)
        ), 'XYZ')

    # --- 6. Lighting (Warm Area Light) ---
    light_data = bpy.data.lights.new(name=f"{object_name}_LightData", type='AREA')
    light_data.energy = 800.0
    light_data.color = (1.0, 0.85, 0.7)  # Warm 4000K look
    light_data.size = 2.0
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_AreaLight", object_data=light_data)
    scene.collection.objects.link(light_obj)
    light_obj.parent = root
    
    # Position above and angled slightly
    light_obj.location = (0.5, -1.0, 3.0)
    light_obj.rotation_euler = Euler((math.radians(15), math.radians(10), 0), 'XYZ')

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created '{object_name}' (Cookie, Tray, {chip_count} Chips, and Lighting) at {location}."
