def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyCar",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.4, 0.8),
    **kwargs,
) -> str:
    """
    Create a stylized low-poly car in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created car hierarchy.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base paint color in 0-1 range.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Target Collection setup
    target_collection = bpy.data.collections.get(object_name)
    if not target_collection:
        target_collection = bpy.data.collections.new(object_name)
        scene.collection.children.link(target_collection)

    # --- MATERIALS ---
    # 1. Car Paint
    mat_body = bpy.data.materials.new(name=f"{object_name}_Paint")
    mat_body.use_nodes = True
    bsdf_body = mat_body.node_tree.nodes.get("Principled BSDF")
    bsdf_body.inputs['Base Color'].default_value = (*material_color, 1.0)
    bsdf_body.inputs['Metallic'].default_value = 0.6
    bsdf_body.inputs['Roughness'].default_value = 0.3

    # 2. Window Glass
    mat_glass = bpy.data.materials.new(name=f"{object_name}_Glass")
    mat_glass.use_nodes = True
    bsdf_glass = mat_glass.node_tree.nodes.get("Principled BSDF")
    bsdf_glass.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1.0)
    bsdf_glass.inputs['Roughness'].default_value = 0.1

    # 3. Tire Rubber
    mat_tire = bpy.data.materials.new(name=f"{object_name}_Tire")
    mat_tire.use_nodes = True
    bsdf_tire = mat_tire.node_tree.nodes.get("Principled BSDF")
    bsdf_tire.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)
    bsdf_tire.inputs['Roughness'].default_value = 0.9

    # 4. Metal Trim
    mat_metal = bpy.data.materials.new(name=f"{object_name}_Metal")
    mat_metal.use_nodes = True
    bsdf_metal = mat_metal.node_tree.nodes.get("Principled BSDF")
    bsdf_metal.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)
    bsdf_metal.inputs['Metallic'].default_value = 1.0
    bsdf_metal.inputs['Roughness'].default_value = 0.2


    # --- BASE CAR BODY ---
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    car = bpy.context.active_object
    car.name = object_name
    
    # Scale to car proportions and apply
    car.scale = (1.6, 3.6, 0.6)
    car.location.z = 0.5  # Lift up slightly
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    car.data.materials.append(mat_body)   # Index 0
    car.data.materials.append(mat_glass)  # Index 1

    # Sculpt the cabin and windows using bmesh
    bm = bmesh.new()
    bm.from_mesh(car.data)

    # Bisect geometry to create the base of the cabin
    bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(0, 0.8, 0), plane_no=(0, 1, 0))
    bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(0, -1.0, 0), plane_no=(0, 1, 0))

    # Find the top face that represents the roof
    bm.faces.ensure_lookup_table()
    top_faces = [f for f in bm.faces if f.normal.z > 0.9]
    cabin_base_face = next((f for f in top_faces if -1.0 < f.calc_center_bounds().y < 0.8), None)

    if cabin_base_face:
        # Extrude cabin upwards
        ret = bmesh.ops.extrude_discrete_faces(bm, faces=[cabin_base_face])
        extruded_face = ret['faces'][0]
        bmesh.ops.translate(bm, vec=(0, 0, 0.7), verts=extruded_face.verts)
        
        # Slant the windshields by scaling the roof down on the Y axis
        roof_center_y = -0.1
        for v in extruded_face.verts:
            v.co.y = roof_center_y + (v.co.y - roof_center_y) * 0.5

    # Filter for window faces (newly created vertical cabin walls)
    window_faces = []
    for f in bm.faces:
        if f.calc_center_bounds().z > 0.9 and abs(f.normal.z) < 0.1:
            window_faces.append(f)
            f.material_index = 1  # Assign glass material
            
    # Inset and extrude windows inwards
    for f in window_faces:
        bmesh.ops.inset_region(bm, faces=[f], thickness=0.08)
        bmesh.ops.translate(bm, vec=-f.normal * 0.05, verts=f.verts)

    bm.to_mesh(car.data)
    bm.free()


    # --- WHEEL WELL BOOLEANS ---
    # Create two cylinder cutters for front and back wells
    bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=2.0, location=(0, 1.0, 0.2))
    cutter1 = bpy.context.active_object
    cutter1.rotation_euler = (0, math.pi / 2, 0)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=2.0, location=(0, -1.0, 0.2))
    cutter2 = bpy.context.active_object
    cutter2.rotation_euler = (0, math.pi / 2, 0)

    # Join cutters
    bpy.ops.object.select_all(action='DESELECT')
    cutter1.select_set(True)
    cutter2.select_set(True)
    bpy.context.view_layer.objects.active = cutter1
    bpy.ops.object.join()

    # Apply Boolean Difference
    bool_mod = car.modifiers.new(name="WheelWells", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = cutter1
    bpy.context.view_layer.objects.active = car
    bpy.ops.object.modifier_apply(modifier="WheelWells")
    
    # Cleanup cutter
    bpy.data.objects.remove(cutter1)


    # --- WHEELS ---
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.4, depth=0.3, location=(0.8, 1.0, 0.2))
    wheel = bpy.context.active_object
    wheel.name = f"{object_name}_Wheel"
    wheel.rotation_euler = (0, math.pi / 2, 0)
    wheel.data.materials.append(mat_tire)

    # Inset rim details
    bm_wheel = bmesh.new()
    bm_wheel.from_mesh(wheel.data)
    bm_wheel.faces.ensure_lookup_table()
    outer_face = next(f for f in bm_wheel.faces if f.normal.x > 0.9)
    
    bmesh.ops.inset_region(bm_wheel, faces=[outer_face], thickness=0.1)
    bmesh.ops.translate(bm_wheel, vec=(-0.05, 0, 0), verts=outer_face.verts)
    bmesh.ops.inset_region(bm_wheel, faces=[outer_face], thickness=0.05)
    bmesh.ops.translate(bm_wheel, vec=(0.02, 0, 0), verts=outer_face.verts)
    
    bm_wheel.to_mesh(wheel.data)
    bm_wheel.free()

    # Duplicate wheel via Modifiers (Array for rear, Mirror for opposite side)
    array_mod = wheel.modifiers.new(name="WheelArray", type='ARRAY')
    array_mod.use_relative_offset = False
    array_mod.use_constant_offset = True
    array_mod.constant_offset_displace = (0, -2.0, 0) # Exact distance to back axle
    array_mod.count = 2

    mirror_mod = wheel.modifiers.new(name="WheelMirror", type='MIRROR')
    mirror_mod.use_axis[0] = True 
    mirror_mod.mirror_object = car


    # --- DETAILS (Bumpers & Mirrors) ---
    def add_trim(name, loc, scale_vec):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
        trim = bpy.context.active_object
        trim.name = f"{object_name}_{name}"
        trim.scale = scale_vec
        trim.data.materials.append(mat_metal)
        trim.parent = car
        return trim

    add_trim("FrontBumper", (0, 1.85, 0.3), (1.4, 0.1, 0.2))
    add_trim("BackBumper", (0, -1.85, 0.3), (1.4, 0.1, 0.2))
    
    mirror = add_trim("SideMirror", (0.85, 0.6, 0.8), (0.1, 0.2, 0.15))
    mirror_mod = mirror.modifiers.new(name="Mirror", type='MIRROR')
    mirror_mod.use_axis[0] = True
    mirror_mod.mirror_object = car


    # --- HIERARCHY, POSITION, & COLLECTION MANAGEMENT ---
    wheel.parent = car

    # Link everything to target collection
    created_objects = [car, wheel] + [child for child in car.children]
    for obj in created_objects:
        if obj.name in scene.collection.objects:
            scene.collection.objects.unlink(obj)
        if obj.name not in target_collection.objects:
            target_collection.objects.link(obj)

    # Apply spatial parameters to root object
    car.location = Vector(location)
    car.scale = (scale, scale, scale)

    return f"Created '{object_name}' (stylized low-poly car) at {location} with fully procedural wheels and trim."
