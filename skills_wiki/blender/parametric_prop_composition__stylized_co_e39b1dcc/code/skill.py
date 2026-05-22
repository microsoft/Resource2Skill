def create_object(
    scene_name: str = "Scene",
    object_name: str = "ChocolateChipCookie",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    cookie_color: tuple = (0.58, 0.33, 0.19),
    chip_color: tuple = (0.04, 0.015, 0.005),
    plate_color: tuple = (0.05, 0.15, 0.6),
    num_chips: int = 15,
    **kwargs,
) -> str:
    """
    Create a 3D Chocolate Chip Cookie on a tray with a presentation light.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position for the tray.
        scale: Uniform scale factor.
        cookie_color: (R, G, B) color for the cookie dough.
        chip_color: (R, G, B) color for the chocolate chips.
        plate_color: (R, G, B) color for the tray/plate.
        num_chips: Number of chocolate chips to scatter.
        
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector, Euler

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # 1. Create a root empty for hierarchy management
    root = bpy.data.objects.new(f"{object_name}_Root", None)
    root.empty_display_size = 2.0
    root.location = Vector(location)
    root.scale = (scale, scale, scale)
    scene.collection.objects.link(root)

    # 2. Materials Setup
    def create_material(name, color, roughness):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*color, 1.0)
            bsdf.inputs["Roughness"].default_value = roughness
        return mat

    mat_plate = create_material(f"{object_name}_Mat_Plate", plate_color, 0.5)
    mat_cookie = create_material(f"{object_name}_Mat_Cookie", cookie_color, 0.8)
    mat_chip = create_material(f"{object_name}_Mat_Chip", chip_color, 0.25) # Slightly glossy

    # 3. Create the Tray (Using BMesh for Inset/Extrude)
    bm_plate = bmesh.new()
    bmesh.ops.create_cube(bm_plate, size=2.0)
    
    # Scale cube down to a flat tray
    bmesh.ops.scale(bm_plate, vec=(1.5, 1.5, 0.1), verts=bm_plate.verts)
    
    # Find the top face (normal pointing up)
    bm_plate.faces.ensure_lookup_table()
    top_face = next(f for f in bm_plate.faces if f.normal.z > 0.9)
    
    # Inset the top face
    inset_result = bmesh.ops.inset_region(bm_plate, faces=[top_face], thickness=0.1, use_even_offset=True)
    
    # Extrude the inner face down (top_face is updated to be the inner face)
    bmesh.ops.translate(bm_plate, vec=(0, 0, -0.1), verts=top_face.verts)
    
    me_plate = bpy.data.meshes.new(f"{object_name}_Tray")
    bm_plate.to_mesh(me_plate)
    bm_plate.free()
    
    plate_obj = bpy.data.objects.new(f"{object_name}_Tray", me_plate)
    plate_obj.data.materials.append(mat_plate)
    plate_obj.parent = root
    scene.collection.objects.link(plate_obj)

    # 4. Create the Cookie Base
    cookie_radius = 1.0
    cookie_depth = 0.2
    bpy.ops.mesh.primitive_cylinder_add(radius=cookie_radius, depth=cookie_depth, location=(0, 0, 0.1))
    cookie_obj = bpy.context.active_object
    cookie_obj.name = f"{object_name}_Cookie"
    cookie_obj.data.materials.append(mat_cookie)
    cookie_obj.parent = root
    
    # Shade Smooth for cookie
    for poly in cookie_obj.data.polygons:
        poly.use_smooth = True

    # 5. Scatter Chocolate Chips
    chip_radius = 0.08
    for i in range(num_chips):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=chip_radius, segments=16, ring_count=8)
        chip_obj = bpy.context.active_object
        chip_obj.name = f"{object_name}_Chip_{i:03d}"
        chip_obj.data.materials.append(mat_chip)
        chip_obj.parent = root
        
        # Shade Smooth for chip
        for poly in chip_obj.data.polygons:
            poly.use_smooth = True
            
        # Randomize placement on top of the cookie
        angle = random.uniform(0, 2 * math.pi)
        # Sqrt ensures uniform distribution over the circular area
        distance = math.sqrt(random.uniform(0, 1)) * (cookie_radius * 0.8) 
        
        x = math.cos(angle) * distance
        y = math.sin(angle) * distance
        # Sink chips slightly into the cookie
        z = 0.1 + (cookie_depth / 2.0) - (chip_radius * 0.4) 
        
        chip_obj.location = (x, y, z)
        # Random rotation for variety
        chip_obj.rotation_euler = (
            random.uniform(0, math.pi),
            random.uniform(0, math.pi),
            random.uniform(0, math.pi)
        )

    # 6. Add the Presentation Area Light (Warm Tone)
    light_data = bpy.data.lights.new(name=f"{object_name}_Light", type='AREA')
    light_data.energy = 850.0  # Bright light as per tutorial
    light_data.color = (1.0, 0.85, 0.7)  # Warm ~4000K look
    light_data.size = 2.0
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_Light", object_data=light_data)
    scene.collection.objects.link(light_obj)
    light_obj.parent = root
    
    # Position light up and to the side, pointing at the cookie
    light_obj.location = (-1.5, -2.0, 3.0)
    # Point towards origin (where cookie is relative to root)
    direction = Vector((0, 0, 0)) - light_obj.location
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    return f"Created '{object_name}' (Cookie, Tray, {num_chips} Chips, and Light) parented to '{root.name}' at {location}."
