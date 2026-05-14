def create_object(
    scene_name: str = "Scene",
    object_name: str = "CupBot",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.9, 0.3, 0.05, 1.0),
    **kwargs,
) -> str:
    """
    Create a 'Cup Bot' demonstrating non-destructive SubD hard surface modeling 
    and modular Shrinkwrap attachment techniques.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector, Matrix

    # Get or create scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Create Parent Empty for easy transformation
    parent = bpy.data.objects.new(object_name, None)
    parent.location = location
    parent.scale = (scale, scale, scale)
    bpy.context.collection.objects.link(parent)

    # ==========================================
    # 1. MATERIALS
    # ==========================================
    mat_body = bpy.data.materials.new(name=f"{object_name}_Body")
    mat_body.use_nodes = True
    mat_body.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = material_color
    mat_body.node_tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 0.3

    mat_white = bpy.data.materials.new(name=f"{object_name}_White")
    mat_white.use_nodes = True
    mat_white.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)
    mat_white.node_tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 0.3

    mat_lens = bpy.data.materials.new(name=f"{object_name}_Lens")
    mat_lens.use_nodes = True
    bsdf_lens = mat_lens.node_tree.nodes["Principled BSDF"]
    bsdf_lens.inputs['Base Color'].default_value = (0.01, 0.05, 0.15, 1.0)
    bsdf_lens.inputs['Roughness'].default_value = 0.1
    bsdf_lens.inputs['Metallic'].default_value = 0.8

    mat_glow = bpy.data.materials.new(name=f"{object_name}_Glow")
    mat_glow.use_nodes = True
    bsdf_glow = mat_glow.node_tree.nodes["Principled BSDF"]
    bsdf_glow.inputs['Emission Color'].default_value = (0.0, 0.8, 1.0, 1.0)
    bsdf_glow.inputs['Emission Strength'].default_value = 5.0

    mat_metal = bpy.data.materials.new(name=f"{object_name}_Metal")
    mat_metal.use_nodes = True
    bsdf_metal = mat_metal.node_tree.nodes["Principled BSDF"]
    bsdf_metal.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1.0)
    bsdf_metal.inputs['Roughness'].default_value = 0.35
    bsdf_metal.inputs['Metallic'].default_value = 1.0

    # ==========================================
    # 2. CUP MAIN BODY
    # ==========================================
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=3, use_grid_fill=True)
    
    # Cast to sphere logic
    for v in bm.verts:
        v.co.normalize()
        v.co *= 0.8  # Radius of 0.8

    # Delete top half to form a bowl
    tops = [v for v in bm.verts if v.co.z > 0.05]
    bmesh.ops.delete(bm, geom=tops, context='VERTS')

    # Extrude top rim upwards to make the cup
    boundary_edges = [e for e in bm.edges if e.is_boundary]
    ret = bmesh.ops.extrude_edge_only(bm, edges=boundary_edges)
    ext_verts = [e for e in ret['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=Vector((0, 0, 1.2)), verts=ext_verts)

    cup_mesh = bpy.data.meshes.new(f"{object_name}_CupMesh")
    bm.to_mesh(cup_mesh)
    bm.free()
    
    cup = bpy.data.objects.new(f"{object_name}_Cup", cup_mesh)
    bpy.context.collection.objects.link(cup)
    cup.parent = parent
    if hasattr(cup.data, "use_auto_smooth"):
        cup.data.use_auto_smooth = True

    # Material Assignment (Two-tone)
    cup.data.materials.append(mat_body)
    cup.data.materials.append(mat_white)
    bm = bmesh.new()
    bm.from_mesh(cup.data)
    for f in bm.faces:
        if f.calc_center_median().z > 0.2:
            f.material_index = 1
    bm.to_mesh(cup.data)
    bm.free()

    # Non-Destructive Modifiers
    mod_sol = cup.modifiers.new("Solidify", 'SOLIDIFY')
    mod_sol.thickness = 0.08
    mod_sol.offset = -1.0

    mod_subd = cup.modifiers.new("Subdivision", 'SUBSURF')
    mod_subd.levels = 2

    mod_bev = cup.modifiers.new("Bevel", 'BEVEL')
    mod_bev.segments = 3
    mod_bev.limit_method = 'ANGLE'
    mod_bev.angle_limit = math.radians(45)
    mod_bev.use_harden_normals = True

    # ==========================================
    # 3. SHRINKWRAPPED HANDLE
    # ==========================================
    # Create U-Shape Curve
    curve_data = bpy.data.curves.new(f"{object_name}_HandleCurve", type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.resolution_u = 4
    curve_data.bevel_depth = 0.08
    curve_data.bevel_resolution = 3

    spline = curve_data.splines.new('POLY')
    spline.points.add(3)
    # Start/End points at X=0.9 (outside the cup radius of 0.8)
    spline.points[0].co = (0.9, 0.0, 0.7, 1)
    spline.points[1].co = (1.4, 0.0, 0.7, 1)
    spline.points[2].co = (1.4, 0.0, 0.1, 1)
    spline.points[3].co = (0.9, 0.0, 0.1, 1)

    handle_temp = bpy.data.objects.new("TempHandle", curve_data)
    bpy.context.collection.objects.link(handle_temp)

    # Convert curve to mesh to enable vertex groups and modifiers
    depsgraph = bpy.context.evaluated_depsgraph_get()
    handle_mesh = bpy.data.meshes.new_from_object(handle_temp.evaluated_get(depsgraph))
    handle = bpy.data.objects.new(f"{object_name}_Handle", handle_mesh)
    bpy.context.collection.objects.link(handle)
    bpy.data.objects.remove(handle_temp) # Clean up curve
    
    handle.parent = parent
    handle.data.materials.append(mat_white)
    if hasattr(handle.data, "use_auto_smooth"):
        handle.data.use_auto_smooth = True
    for p in handle.data.polygons:
        p.use_smooth = True

    # Vertex Group for the ends pointing towards the cup
    vg_handle = handle.vertex_groups.new(name="ShrinkTarget")
    bm = bmesh.new()
    bm.from_mesh(handle.data)
    end_verts = [v.index for v in bm.verts if v.co.x < 1.0]
    vg_handle.add(end_verts, 1.0, 'ADD')
    bm.free()

    # Shrinkwrap logic: Raycast backwards (-X) onto the Cup surface
    sw_handle = handle.modifiers.new("Shrinkwrap", 'SHRINKWRAP')
    sw_handle.target = cup
    sw_handle.vertex_group = "ShrinkTarget"
    sw_handle.wrap_method = 'PROJECT'
    sw_handle.use_project_x = True
    sw_handle.use_project_y = False
    sw_handle.use_project_z = False
    sw_handle.use_negative_direction = True
    sw_handle.use_positive_direction = False

    # ==========================================
    # 4. SHRINKWRAPPED EYE
    # ==========================================
    bm = bmesh.new()
    bmesh.ops.create_cylinder(bm, cap_ends=True, cap_tris=False, segments=24, radius=0.22, depth=0.15)
    bmesh.ops.rotate(bm, cent=Vector(), matrix=Matrix.Rotation(math.radians(90), 3, 'X'), verts=bm.verts)
    
    # Place at -Y, outside the radius of 0.8
    bmesh.ops.translate(bm, vec=Vector((0, -0.95, 0.4)), verts=bm.verts)
    
    eye_mesh = bpy.data.meshes.new(f"{object_name}_EyeMesh")
    bm.to_mesh(eye_mesh)
    bm.free()
    
    eye = bpy.data.objects.new(f"{object_name}_Eye", eye_mesh)
    bpy.context.collection.objects.link(eye)
    eye.parent = parent
    if hasattr(eye.data, "use_auto_smooth"):
        eye.data.use_auto_smooth = True
    for p in eye.data.polygons:
        p.use_smooth = True

    eye.data.materials.append(mat_white)
    eye.data.materials.append(mat_lens)
    eye.data.materials.append(mat_glow)

    # Group back vertices for Shrinkwrap, assign front faces to Lens/Glow materials
    vg_eye = eye.vertex_groups.new(name="ShrinkTarget")
    bm = bmesh.new()
    bm.from_mesh(eye.data)
    back_verts = [v.index for v in bm.verts if v.co.y > -0.9] # Near the back side
    vg_eye.add(back_verts, 1.0, 'ADD')
    
    for f in bm.faces:
        if f.normal.y < -0.9: # Front face pointing -Y
            f.material_index = 1 # Lens
            # Create inner emission ring via rudimentary face area check (hacky but functional for script)
            if f.calc_area() < 0.1: 
                f.material_index = 2 # Glow
    bm.to_mesh(eye.data)
    bm.free()

    # Shrinkwrap logic: Raycast backwards (+Y) onto the Cup surface
    sw_eye = eye.modifiers.new("Shrinkwrap", 'SHRINKWRAP')
    sw_eye.target = cup
    sw_eye.vertex_group = "ShrinkTarget"
    sw_eye.wrap_method = 'PROJECT'
    sw_eye.use_project_x = False
    sw_eye.use_project_y = True
    sw_eye.use_project_z = False
    sw_eye.use_negative_direction = False
    sw_eye.use_positive_direction = True

    mod_bev_eye = eye.modifiers.new("Bevel", 'BEVEL')
    mod_bev_eye.segments = 2
    mod_bev_eye.limit_method = 'ANGLE'
    mod_bev_eye.angle_limit = math.radians(40)
    mod_bev_eye.use_harden_normals = True

    # ==========================================
    # 5. MECHANICAL LEGS
    # ==========================================
    bm = bmesh.new()
    def make_leg(bmesh_obj, x_offset):
        # Joint
        geom = bmesh.ops.create_cylinder(bmesh_obj, cap_ends=True, segments=16, radius=0.08, depth=0.1)
        bmesh.ops.rotate(bmesh_obj, cent=Vector(), matrix=Matrix.Rotation(math.radians(90), 3, 'Y'), verts=geom['verts'])
        bmesh.ops.translate(bmesh_obj, vec=Vector((x_offset, 0, -0.85)), verts=geom['verts'])
        # Strut
        geom = bmesh.ops.create_cube(bmesh_obj, size=1.0)
        bmesh.ops.scale(bmesh_obj, vec=Vector((0.06, 0.08, 0.3)), verts=geom['verts'])
        bmesh.ops.translate(bmesh_obj, vec=Vector((x_offset, 0, -1.1)), verts=geom['verts'])
        # Foot
        geom = bmesh.ops.create_cube(bmesh_obj, size=1.0)
        bmesh.ops.scale(bmesh_obj, vec=Vector((0.15, 0.3, 0.05)), verts=geom['verts'])
        bmesh.ops.translate(bmesh_obj, vec=Vector((x_offset, 0.05, -1.25)), verts=geom['verts'])

    make_leg(bm, -0.3)
    make_leg(bm, 0.3)

    legs_mesh = bpy.data.meshes.new(f"{object_name}_LegsMesh")
    bm.to_mesh(legs_mesh)
    bm.free()
    
    legs = bpy.data.objects.new(f"{object_name}_Legs", legs_mesh)
    bpy.context.collection.objects.link(legs)
    legs.parent = parent
    legs.data.materials.append(mat_metal)
    if hasattr(legs.data, "use_auto_smooth"):
        legs.data.use_auto_smooth = True
        
    for p in legs.data.polygons:
        p.use_smooth = True

    mod_bev_legs = legs.modifiers.new("Bevel", 'BEVEL')
    mod_bev_legs.width = 0.015
    mod_bev_legs.segments = 2
    mod_bev_legs.limit_method = 'ANGLE'
    mod_bev_legs.use_harden_normals = True

    return f"Created modular hard-surface '{object_name}' with integrated Shrinkwrap attachments at {location}."
