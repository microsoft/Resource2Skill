def create_object(
    scene_name: str = "Scene",
    object_name: str = "CookieProp",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.76, 0.52, 0.25),  # Cookie base color
    **kwargs,
) -> str:
    """
    Create a Stylized Cookie and Tray prop in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position of the tray.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the cookie.
        **kwargs: Optional 'tray_color', 'chip_color', and 'num_chips'.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector, Matrix

    # Get target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    collection = scene.collection

    # Helper function to create materials
    def create_solid_material(name, rgb_color, roughness=0.5):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Ensure alpha channel is 1.0
            color_rgba = (rgb_color[0], rgb_color[1], rgb_color[2], 1.0)
            bsdf.inputs["Base Color"].default_value = color_rgba
            bsdf.inputs["Roughness"].default_value = roughness
        return mat

    # Extract kwargs
    tray_color = kwargs.get("tray_color", (0.05, 0.20, 0.60))
    chip_color = kwargs.get("chip_color", (0.10, 0.04, 0.01))
    num_chips = kwargs.get("num_chips", 12)

    # 1. Create Materials
    mat_cookie = create_solid_material(f"{object_name}_Mat_Cookie", material_color, 0.6)
    mat_tray = create_solid_material(f"{object_name}_Mat_Tray", tray_color, 0.4)
    mat_chip = create_solid_material(f"{object_name}_Mat_Chip", chip_color, 0.3)

    # Root Empty for easy positioning/scaling
    root_empty = bpy.data.objects.new(object_name, None)
    root_empty.location = Vector(location)
    root_empty.scale = Vector((scale, scale, scale))
    collection.objects.link(root_empty)

    # 2. Build the Tray (Cube with inset top)
    bm_tray = bmesh.new()
    bmesh.ops.create_cube(bm_tray, size=1.0)
    # Scale cube to tray proportions
    bmesh.ops.scale(bm_tray, vec=(3.0, 3.0, 0.2), verts=bm_tray.verts)
    
    # Inset and extrude the top face
    top_face = next((f for f in bm_tray.faces if f.normal.z > 0.9), None)
    if top_face:
        bmesh.ops.inset_region(bm_tray, faces=[top_face], thickness=0.15)
        # The original top face is now the inner face; extrude it down
        bmesh.ops.translate(bm_tray, vec=(0, 0, -0.05), verts=top_face.verts)

    mesh_tray = bpy.data.meshes.new(f"{object_name}_Tray")
    bm_tray.to_mesh(mesh_tray)
    bm_tray.free()
    
    obj_tray = bpy.data.objects.new(f"{object_name}_Tray", mesh_tray)
    obj_tray.data.materials.append(mat_tray)
    obj_tray.parent = root_empty
    # Move tray up slightly so its bottom sits on the root origin
    obj_tray.location = Vector((0, 0, 0.1))
    collection.objects.link(obj_tray)

    # 3. Build the Cookie (Squashed Cylinder)
    bm_cookie = bmesh.new()
    bmesh.ops.create_cone(
        bm_cookie, cap_ends=True, cap_tris=False, segments=32, 
        radius1=1.0, radius2=1.0, depth=0.2
    )
    
    mesh_cookie = bpy.data.meshes.new(f"{object_name}_CookieBase")
    bm_cookie.to_mesh(mesh_cookie)
    bm_cookie.free()
    
    # Shade Smooth
    for p in mesh_cookie.polygons:
        p.use_smooth = True
        
    obj_cookie = bpy.data.objects.new(f"{object_name}_CookieBase", mesh_cookie)
    obj_cookie.data.materials.append(mat_cookie)
    obj_cookie.parent = root_empty
    # Rest cookie inside the tray
    obj_cookie.location = Vector((0, 0, 0.25)) 
    collection.objects.link(obj_cookie)

    # 4. Build Chocolate Chips (Scattered UV Spheres merged into one mesh)
    bm_chips = bmesh.new()
    cookie_radius = 0.85 # Keep chips slightly away from absolute edge
    
    for _ in range(num_chips):
        # Random position in a circle
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(0, cookie_radius)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        
        # Random scale and rotation for variety
        chip_scale = random.uniform(0.06, 0.12)
        z = 0.1 + (chip_scale * 0.4) # Embed slightly into cookie
        
        geom = bmesh.ops.create_uvsphere(
            bm_chips, u_segments=12, v_segments=12, radius=chip_scale
        )
        
        # Squash the chip slightly on Z
        bmesh.ops.scale(bm_chips, vec=(1.0, 1.0, 0.8), verts=geom['verts'])
        
        # Translate to random position
        bmesh.ops.translate(bm_chips, vec=(x, y, z), verts=geom['verts'])

    mesh_chips = bpy.data.meshes.new(f"{object_name}_Chips")
    bm_chips.to_mesh(mesh_chips)
    bm_chips.free()
    
    for p in mesh_chips.polygons:
        p.use_smooth = True

    obj_chips = bpy.data.objects.new(f"{object_name}_Chips", mesh_chips)
    obj_chips.data.materials.append(mat_chip)
    obj_chips.parent = obj_cookie # Parent to cookie
    obj_chips.location = Vector((0, 0, 0))
    collection.objects.link(obj_chips)

    # 5. Add Area Light (to mimic the tutorial's lighting environment)
    light_data = bpy.data.lights.new(name=f"{object_name}_Light", type='AREA')
    light_data.energy = 800.0
    light_data.color = (1.0, 0.9, 0.7) # Warm temperature
    light_data.shape = 'SQUARE'
    light_data.size = 2.0
    
    obj_light = bpy.data.objects.new(name=f"{object_name}_Light", object_data=light_data)
    obj_light.parent = root_empty
    obj_light.location = Vector((-2.0, -2.0, 3.0))
    # Point light towards the cookie
    direction = -obj_light.location
    obj_light.rotation_euler = direction.to_track_quat('-Z', 'Y')
    collection.objects.link(obj_light)

    return f"Created '{object_name}' (Tray, Cookie, and {num_chips} Chips) at {location} with scale {scale}"
