def create_stylized_cookie(
    scene_name: str = "Scene",
    object_name: str = "Kevin_Cookie",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    cookie_color: tuple = (0.65, 0.40, 0.15, 1.0),
    tray_color: tuple = (0.10, 0.20, 0.60, 1.0),
    **kwargs,
) -> str:
    """
    Create a stylized chocolate chip cookie on a tray with lighting.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created objects/group.
        location: (x, y, z) world-space position for the root object.
        scale: Uniform scale factor for the entire assembly.
        cookie_color: (R, G, B, A) base color for the cookie dough.
        tray_color: (R, G, B, A) base color for the tray.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector, Euler

    # Ensure we are operating in the right scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection

    # Ensure we are in Object mode to avoid bmesh conflicts
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # ==========================================
    # Step 1: Create Materials
    # ==========================================
    def create_simple_material(name, color, roughness):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = color
            bsdf.inputs["Roughness"].default_value = roughness
        return mat

    mat_cookie = create_simple_material(f"{object_name}_Mat_Dough", cookie_color, 0.85)
    mat_chip = create_simple_material(f"{object_name}_Mat_Chip", (0.08, 0.03, 0.01, 1.0), 0.4)
    mat_tray = create_simple_material(f"{object_name}_Mat_Tray", tray_color, 0.3)

    # ==========================================
    # Step 2: Create Parent Empty
    # ==========================================
    parent_empty = bpy.data.objects.new(f"{object_name}_Root", None)
    parent_empty.empty_display_size = 2.0
    parent_empty.empty_display_type = 'ARROWS'
    collection.objects.link(parent_empty)
    
    parent_empty.location = Vector(location)
    parent_empty.scale = (scale, scale, scale)

    # ==========================================
    # Step 3: Create the Tray (bmesh Inset/Extrude)
    # ==========================================
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    
    # Scale cube into a flat square board
    bmesh.ops.scale(bm, vec=(1.5, 1.5, 0.1), verts=bm.verts)
    
    # Identify the top face
    top_face = None
    for face in bm.faces:
        if face.normal.z > 0.9:
            top_face = face
            break
            
    # Inset the top face
    inset_result = bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.1)
    
    # "Extrude" downwards by lowering the vertices of the newly inset face
    for v in top_face.verts:
        v.co.z -= 0.05
        
    mesh_tray = bpy.data.meshes.new(f"{object_name}_Tray")
    bm.to_mesh(mesh_tray)
    bm.free()
    
    obj_tray = bpy.data.objects.new(f"{object_name}_Tray", mesh_tray)
    collection.objects.link(obj_tray)
    obj_tray.parent = parent_empty
    obj_tray.data.materials.append(mat_tray)

    # ==========================================
    # Step 4: Create the Cookie Base
    # ==========================================
    # Using ops for primitive to utilize built-in generation, then assigning
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32, radius=1.0, depth=0.3, 
        location=(0, 0, 0.25) # Resting on the tray
    )
    obj_cookie = bpy.context.active_object
    obj_cookie.name = f"{object_name}_Base"
    obj_cookie.parent = parent_empty
    obj_cookie.data.materials.append(mat_cookie)
    
    # Apply smooth shading via polygon data
    for p in obj_cookie.data.polygons:
        p.use_smooth = True

    # ==========================================
    # Step 5: Procedurally Scatter Chocolate Chips
    # ==========================================
    num_chips = random.randint(10, 14)
    for i in range(num_chips):
        # Random circular distribution
        angle = random.uniform(0, math.pi * 2)
        radius_offset = random.uniform(0.1, 0.8) # Keep away from exact edge
        x = math.cos(angle) * radius_offset
        y = math.sin(angle) * radius_offset
        z = 0.4 # Embedded slightly into the top of the cookie base
        
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=16, ring_count=8, radius=0.1, 
            location=(x, y, z)
        )
        chip = bpy.context.active_object
        chip.name = f"{object_name}_Chip_{i}"
        chip.parent = parent_empty
        chip.data.materials.append(mat_chip)
        
        for p in chip.data.polygons:
            p.use_smooth = True
            
        # Add slight random variations to the chips
        chip.scale = (random.uniform(0.8, 1.2), random.uniform(0.8, 1.2), random.uniform(0.5, 0.9))
        chip.rotation_euler = Euler((random.uniform(0, 3.14), random.uniform(0, 3.14), random.uniform(0, 3.14)))

    # ==========================================
    # Step 6: Setup Area Lighting
    # ==========================================
    light_data = bpy.data.lights.new(name=f"{object_name}_AreaLight", type='AREA')
    light_data.energy = 850.0
    light_data.color = (1.0, 0.9, 0.7) # Warm 4000k tint
    light_data.size = 2.0
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_Light", object_data=light_data)
    collection.objects.link(light_obj)
    light_obj.parent = parent_empty
    
    # Position diagonally above and point at the cookie
    light_obj.location = (-1.5, -1.5, 2.0)
    light_obj.rotation_euler = Euler((math.radians(45), 0, math.radians(-45)))

    # Ensure Cycles engine is active for proper preview (as per tutorial)
    scene.render.engine = 'CYCLES'

    # Deselect all to clean up context
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created '{object_name}' scene (Cookie, {num_chips} Chips, Tray, Light) at {location} scaled by {scale}."
