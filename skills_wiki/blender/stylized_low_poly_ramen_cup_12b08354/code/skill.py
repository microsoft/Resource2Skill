def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyRamen",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.9, 0.85, 0.8),
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Ramen Cup in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created master object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the cup exterior.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector, Matrix
    import math
    import random

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Helper Function for Materials ---
    def create_mat(name, color, roughness=0.8):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (*color, 1.0)
            bsdf.inputs['Roughness'].default_value = roughness
        return mat

    # Create Materials
    mat_cup = create_mat(f"{object_name}_Mat_Cup", material_color)
    mat_soup = create_mat(f"{object_name}_Mat_Soup", (0.8, 0.4, 0.05), roughness=0.2)
    mat_lid = create_mat(f"{object_name}_Mat_Lid", (0.85, 0.85, 0.85), roughness=0.4)
    mat_wood = create_mat(f"{object_name}_Mat_Wood", (0.7, 0.5, 0.3))
    mat_green = create_mat(f"{object_name}_Mat_Scallion", (0.2, 0.6, 0.1))
    mat_pink = create_mat(f"{object_name}_Mat_Meat", (0.8, 0.3, 0.3))

    # ==========================================
    # 1. CREATE RAMEN CUP BASE
    # ==========================================
    cup_mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    cup_obj = bpy.data.objects.new(object_name, cup_mesh)
    scene.collection.objects.link(cup_obj)
    
    cup_obj.data.materials.append(mat_cup)
    cup_obj.data.materials.append(mat_soup)

    bm = bmesh.new()
    
    # Octagonal Cone (Tapered Cylinder)
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=8, 
        radius1=0.7, radius2=1.0, depth=2.0
    )

    # Find the top face (normal pointing directly up)
    top_face = next((f for f in bm.faces if f.normal.z > 0.9 and f.calc_center_median().length_squared < 0.01), None)

    if top_face:
        # Inset to create the lip rim
        bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.08, use_even_offset=True)
        
        # Re-identify the inner face after inset
        inner_face = next((f for f in bm.faces if f.normal.z > 0.9 and f.calc_center_median().length_squared < 0.01), None)
        
        # Extrude cavity down
        geom_to_extrude = [inner_face] + inner_face.edges[:] + inner_face.verts[:]
        ext_res = bmesh.ops.extrude_face_region(bm, geom=geom_to_extrude)
        
        # Push extruded vertices down
        extruded_verts = [elem for elem in ext_res['geom'] if isinstance(elem, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, vec=Vector((0, 0, -0.4)), verts=extruded_verts)
        
        # Scale cavity floor inwards to match the cup's outer taper
        extruded_faces = [elem for elem in ext_res['geom'] if isinstance(elem, bmesh.types.BMFace)]
        if extruded_faces:
            soup_face = extruded_faces[0]
            soup_face.material_index = 1 # Assign Soup Material
            center = soup_face.calc_center_median()
            scale_mat = Matrix.Translation(center) @ Matrix.Diagonal(Vector((0.9, 0.9, 1.0)).to_4x4()) @ Matrix.Translation(-center)
            for v in soup_face.verts:
                v.co = scale_mat @ v.co

    # Ensure flat shading for retro low poly look
    for f in bm.faces:
        f.smooth = False

    bm.to_mesh(cup_mesh)
    bm.free()

    # ==========================================
    # 2. CREATE PEELED LID
    # ==========================================
    lid_mesh = bpy.data.meshes.new(f"{object_name}_Lid_Mesh")
    lid_obj = bpy.data.objects.new(f"{object_name}_Lid", lid_mesh)
    scene.collection.objects.link(lid_obj)
    lid_obj.parent = cup_obj
    lid_obj.location = Vector((0, 0, 1.01)) # Sit just above the cup lip
    lid_obj.data.materials.append(mat_lid)

    lid_bm = bmesh.new()
    bmesh.ops.create_circle(lid_bm, cap_ends=True, cap_tris=False, segments=8, radius=1.02)
    
    # Fold vertices on the positive Y half to create the peel effect
    rot_mat = Matrix.Rotation(math.radians(-110), 4, 'X')
    for v in lid_bm.verts:
        if v.co.y > 0.05:
            v.co = rot_mat @ v.co
            
    # Add thickness
    bmesh.ops.solidify(lid_bm, geom=lid_bm.faces[:], thickness=0.02)
    
    for f in lid_bm.faces:
        f.smooth = False

    lid_bm.to_mesh(lid_mesh)
    lid_bm.free()

    # ==========================================
    # 3. CREATE CHOPSTICKS
    # ==========================================
    stick_mesh = bpy.data.meshes.new(f"{object_name}_Stick_Mesh")
    stick_bm = bmesh.new()
    bmesh.ops.create_cube(stick_bm, size=1.0)
    
    # Scale to stick dimensions
    bmesh.ops.scale(stick_bm, vec=Vector((0.06, 0.06, 2.5)), verts=stick_bm.verts)
    
    # Taper the bottom
    for v in stick_bm.verts:
        if v.co.z < 0:
            v.co.x *= 0.5
            v.co.y *= 0.5
            
    for f in stick_bm.faces:
        f.smooth = False
            
    stick_bm.to_mesh(stick_mesh)
    stick_bm.free()

    stick_positions = [
        (Vector((0.2, 0.4, 1.2)), (math.radians(30), math.radians(15), math.radians(20))),
        (Vector((0.05, 0.5, 1.3)), (math.radians(25), math.radians(-10), math.radians(10)))
    ]

    for i, (pos, rot) in enumerate(stick_positions):
        stick_obj = bpy.data.objects.new(f"{object_name}_Chopstick_{i}", stick_mesh)
        scene.collection.objects.link(stick_obj)
        stick_obj.parent = cup_obj
        stick_obj.location = pos
        stick_obj.rotation_euler = rot
        stick_obj.data.materials.append(mat_wood)

    # ==========================================
    # 4. ADD SOUP GARNISH (Flat geometric bits)
    # ==========================================
    for i in range(6):
        g_mesh = bpy.data.meshes.new(f"{object_name}_Garnish_{i}")
        g_obj = bpy.data.objects.new(f"{object_name}_Garnish_{i}", g_mesh)
        scene.collection.objects.link(g_obj)
        g_obj.parent = cup_obj
        
        g_bm = bmesh.new()
        bmesh.ops.create_cube(g_bm, size=0.1)
        bmesh.ops.scale(g_bm, vec=Vector((1.0, 1.0, 0.1)), verts=g_bm.verts) # Flatten
        g_bm.to_mesh(g_mesh)
        g_bm.free()

        # Randomize placement inside the cup cavity
        angle = random.uniform(0, math.pi * 2)
        rad = random.uniform(0, 0.6)
        g_obj.location = Vector((math.cos(angle) * rad, math.sin(angle) * rad, 0.62))
        g_obj.rotation_euler = (random.uniform(0, 3), random.uniform(0, 3), random.uniform(0, 3))
        
        g_mat = mat_green if random.random() > 0.4 else mat_pink
        g_obj.data.materials.append(g_mat)

    # ==========================================
    # 5. POSITION & SCALE MASTER OBJECT
    # ==========================================
    cup_obj.location = Vector(location)
    cup_obj.scale = (scale, scale, scale)

    return f"Created Stylized Ramen Cup '{object_name}' at {location} with lid, chopsticks, and garnish components."
