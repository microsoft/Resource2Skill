def create_object(
    scene_name: str = "Scene",
    object_name: str = "CookieScene",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    cookie_color: tuple = (0.65, 0.40, 0.15, 1.0),
    chip_color: tuple = (0.05, 0.02, 0.01, 1.0),
    tray_color: tuple = (0.10, 0.25, 0.60, 1.0),
    num_chips: int = 15,
    **kwargs,
) -> str:
    """
    Create a stylized Cookie on a Tray in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created hierarchy.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        cookie_color: (R, G, B, A) color for the cookie dough.
        chip_color: (R, G, B, A) color for the chocolate chips.
        tray_color: (R, G, B, A) color for the presentation tray.
        num_chips: Amount of procedurally scattered chips.

    Returns:
        Status string documenting the creation.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector

    # Safely ensure we are in Object Mode before generating primitives
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection

    # === Step 1: Material Generation ===
    mat_cookie = bpy.data.materials.new(f"{object_name}_Mat_Cookie")
    mat_cookie.use_nodes = True
    mat_cookie.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = cookie_color
    mat_cookie.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.8

    mat_chip = bpy.data.materials.new(f"{object_name}_Mat_Chip")
    mat_chip.use_nodes = True
    mat_chip.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = chip_color
    mat_chip.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.3

    mat_tray = bpy.data.materials.new(f"{object_name}_Mat_Tray")
    mat_tray.use_nodes = True
    mat_tray.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = tray_color
    mat_tray.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.2

    # === Step 2: Tray Construction (BMesh Inset/Extrude) ===
    mesh_tray = bpy.data.meshes.new(f"{object_name}_TrayMesh")
    tray = bpy.data.objects.new(f"{object_name}_Tray", mesh_tray)
    collection.objects.link(tray)

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    # Flatten and widen the cube
    bmesh.ops.scale(bm, vec=(3.2, 3.2, 0.2), verts=bm.verts)
    
    # Locate the top face and inset it to form the rim
    top_face = next(f for f in bm.faces if f.normal.z > 0.9)
    bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.1)
    
    # Push the inner face downward to carve out the tray's cavity
    bmesh.ops.translate(bm, vec=(0, 0, -0.1), verts=top_face.verts)
    
    bm.to_mesh(mesh_tray)
    bm.free()
    tray.data.materials.append(mat_tray)

    # Force a scene update so parent_inverse matrices calculate correctly
    bpy.context.view_layer.update()

    # === Step 3: Cookie Geometry ===
    # Tray cavity surface is exactly at Z = 0.0 local. Cookie depth = 0.2 -> center it at Z = 0.1
    bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=0.2, vertices=32, location=(0, 0, 0.1))
    cookie = bpy.context.active_object
    cookie.name = f"{object_name}_Cookie"
    cookie.data.materials.append(mat_cookie)
    
    for poly in cookie.data.polygons:
        poly.use_smooth = True

    # Lock cookie to tray
    cookie.parent = tray
    cookie.matrix_parent_inverse = tray.matrix_world.inverted()

    # === Step 4: Procedural Chocolate Chips ===
    for i in range(num_chips):
        # Calculate random, uniform scattering strictly within the cookie's radius
        r_scatter = math.sqrt(random.random()) * 0.85 
        theta = random.random() * 2 * math.pi
        pos_x = r_scatter * math.cos(theta)
        pos_y = r_scatter * math.sin(theta)
        pos_z = 0.22  # Surface of the cookie is Z=0.2; place slightly above to embed halfway
        
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, segments=16, ring_count=8, location=(pos_x, pos_y, pos_z))
        chip = bpy.context.active_object
        chip.name = f"{object_name}_Chip_{i}"
        
        # Squash the chip vertically and apply a random orientation
        chip.scale[2] = 0.6
        chip.rotation_euler = (
            random.random() * math.pi, 
            random.random() * math.pi, 
            random.random() * math.pi
        )
        
        chip.data.materials.append(mat_chip)
        for poly in chip.data.polygons:
            poly.use_smooth = True
            
        # Lock chip to cookie
        chip.parent = cookie
        chip.matrix_parent_inverse = cookie.matrix_world.inverted()

    # === Step 5: Warm Accent Lighting ===
    light_data = bpy.data.lights.new(name=f"{object_name}_WarmLight", type='AREA')
    light_data.energy = 300.0
    light_data.color = (1.0, 0.85, 0.7)  # Very warm, appetizing hue
    light_data.size = 2.0
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_LightObj", object_data=light_data)
    collection.objects.link(light_obj)

    # Position off-center, up high, and automatically aim it at the origin (the cookie)
    light_pos = Vector((2.0, -2.0, 2.5))
    light_obj.location = light_pos
    light_obj.rotation_euler = (-light_pos).to_track_quat('-Z', 'Y').to_euler()
    
    light_obj.parent = tray
    light_obj.matrix_parent_inverse = tray.matrix_world.inverted()

    # === Step 6: World Transform Wrap-Up ===
    tray.location = Vector(location)
    tray.scale = (scale, scale, scale)

    return f"Created '{object_name}' (Cookie on Tray) at {location} with {num_chips} procedurally scattered chocolate chips."
