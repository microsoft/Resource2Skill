def create_stylized_fish(
    scene_name: str = "Scene",
    object_name: str = "StylizedFish",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.05, 0.05),
    **kwargs,
) -> str:
    """
    Create a Stylized Fish base mesh ready for sculpting or stylized rendering.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) primary color of the fish body.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector, Matrix
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Create master collection
    fish_col = bpy.data.collections.new(object_name)
    scene.collection.children.link(fish_col)

    # === Step 1: Material Setup ===
    mat_body = bpy.data.materials.new(name=f"{object_name}_BodyMat")
    mat_body.use_nodes = True
    bsdf_body = mat_body.node_tree.nodes.get("Principled BSDF")
    bsdf_body.inputs["Base Color"].default_value = (*material_color, 1.0)
    bsdf_body.inputs["Roughness"].default_value = 0.3

    # Derive fin color (brighter, slightly shifted hue)
    fin_color = (min(material_color[0] * 1.2, 1.0), min(material_color[1] + 0.25, 1.0), material_color[2])
    mat_fin = bpy.data.materials.new(name=f"{object_name}_FinMat")
    mat_fin.use_nodes = True
    bsdf_fin = mat_fin.node_tree.nodes.get("Principled BSDF")
    bsdf_fin.inputs["Base Color"].default_value = (*fin_color, 1.0)
    bsdf_fin.inputs["Roughness"].default_value = 0.3
    
    mat_eye_w = bpy.data.materials.new(name=f"{object_name}_EyeWhite")
    mat_eye_w.use_nodes = True
    mat_eye_w.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (1, 1, 1, 1)
    mat_eye_w.node_tree.nodes.get("Principled BSDF").inputs["Roughness"].default_value = 0.1

    mat_eye_b = bpy.data.materials.new(name=f"{object_name}_EyeBlack")
    mat_eye_b.use_nodes = True
    mat_eye_b.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (0.02, 0.02, 0.02, 1)
    mat_eye_b.node_tree.nodes.get("Principled BSDF").inputs["Roughness"].default_value = 0.1

    # Helper function for mesh creation
    def make_mesh(name, bmesh_func, mat):
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        fish_col.objects.link(obj)
        bm = bmesh.new()
        bmesh_func(bm)
        bm.to_mesh(mesh)
        bm.free()
        obj.data.materials.append(mat)
        for p in mesh.polygons:
            p.use_smooth = True
        return obj

    # === Step 2: Geometry Generation ===
    
    # Body
    def body_shape(bm):
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1.0)
        for v in bm.verts:
            x, y, z = v.co.x, v.co.y, v.co.z
            x *= 1.2
            y *= 0.5
            z *= 0.7
            # Taper tail (negative X)
            if x < 0:
                t = abs(x) / 1.2
                y *= (1.0 - t * 0.6)
                z *= (1.0 - t * 0.6)
            # Round head (positive X)
            else:
                t = x / 1.2
                y *= (1.0 + t * 0.1)
                z *= (1.0 + t * 0.1)
            v.co = Vector((x, y, z))
            
    body_obj = make_mesh(f"{object_name}_Body", body_shape, mat_body)

    # Tail Fin
    def tail_shape(bm):
        bmesh.ops.create_cone(bm, segments=16, radius1=0.6, radius2=0.0, depth=1.2)
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0,0,0), matrix=Matrix.Rotation(-math.pi/2, 3, 'Y'))
        for v in bm.verts:
            v.co.y *= 0.1 
            v.co.z *= 1.5 
            v.co.x -= 1.1 

    tail_obj = make_mesh(f"{object_name}_Tail", tail_shape, mat_fin)

    # Dorsal Fin (Top)
    def top_fin_shape(bm):
        bmesh.ops.create_cone(bm, segments=16, radius1=0.5, radius2=0.0, depth=0.8)
        for v in bm.verts:
            v.co.y *= 0.1 
            v.co.x *= 1.5 
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0,0,0), matrix=Matrix.Rotation(-math.pi/8, 3, 'Y'))
        for v in bm.verts:
            v.co.z += 0.7 
            v.co.x -= 0.2
            
    top_fin_obj = make_mesh(f"{object_name}_TopFin", top_fin_shape, mat_fin)

    # Pectoral Fin (Side)
    def side_fin_shape(bm):
        bmesh.ops.create_cone(bm, segments=16, radius1=0.4, radius2=0.0, depth=1.0)
        for v in bm.verts:
            v.co.y *= 0.1
        # Sweep backwards and angle outwards
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0,0,0), matrix=Matrix.Rotation(-math.pi/2, 3, 'Y'))
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0,0,0), matrix=Matrix.Rotation(-math.pi/6, 3, 'X'))
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0,0,0), matrix=Matrix.Rotation(-math.pi/6, 3, 'Z'))
        for v in bm.verts:
            v.co.x += 0.2
            v.co.y -= 0.55
            v.co.z -= 0.2

    fin_R = make_mesh(f"{object_name}_Pectoral_R", side_fin_shape, mat_fin)
    
    # Eyes
    def eye_shape(bm):
        bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=16, radius=0.25)
        for v in bm.verts:
            v.co.y *= 0.8
            v.co.x += 0.6 
            v.co.y -= 0.35 
            v.co.z += 0.15 
            
    eye_w_R = make_mesh(f"{object_name}_Eye_R", eye_shape, mat_eye_w)

    def pupil_shape(bm):
        bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=16, radius=0.1)
        for v in bm.verts:
            v.co.y *= 0.5
            v.co.x += 0.7   
            v.co.y -= 0.52  
            v.co.z += 0.15

    eye_b_R = make_mesh(f"{object_name}_Pupil_R", pupil_shape, mat_eye_b)

    # === Step 3: Hierarchy & Symmetry Setup ===
    
    objects_to_parent = [tail_obj, top_fin_obj, fin_R, eye_w_R, eye_b_R]
    objects_to_mirror = [fin_R, eye_w_R, eye_b_R]

    for obj in objects_to_mirror:
        mod = obj.modifiers.new("Mirror", 'MIRROR')
        mod.mirror_object = body_obj
        mod.use_axis[0] = False
        mod.use_axis[1] = True # Mirror across Y-axis
        
    for obj in objects_to_parent:
        obj.parent = body_obj

    # === Step 4: Final Positioning ===
    body_obj.location = Vector(location)
    body_obj.scale = Vector((scale, scale, scale))

    return f"Created Stylized Fish Blockout '{object_name}' at {location} with {len(objects_to_parent) + 1} mesh components."
