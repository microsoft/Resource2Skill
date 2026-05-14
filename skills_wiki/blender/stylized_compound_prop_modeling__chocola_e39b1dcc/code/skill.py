def create_stylized_cookie_scene(
    scene_name: str = "Scene",
    base_name: str = "StylizedCookie",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    cookie_color: tuple = (0.7, 0.4, 0.15),
    chip_color: tuple = (0.04, 0.02, 0.01),
    plate_color: tuple = (0.05, 0.1, 0.6),
    **kwargs
) -> str:
    """
    Create a stylized chocolate chip cookie resting on an extruded plate with warm studio lighting.

    Args:
        scene_name: Target scene to link objects to.
        base_name: Prefix name for the generated objects.
        location: (x, y, z) world-space origin of the plate.
        scale: Uniform scale modifier for the entire prop cluster.
        cookie_color: RGB tuple for the cookie dough.
        chip_color: RGB tuple for the chocolate chips.
        plate_color: RGB tuple for the tray/plate.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Material Setup ===
    def make_color_material(mat_name, rgb_color):
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Ensure alpha is 1.0
            bsdf.inputs["Base Color"].default_value = (*rgb_color, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.8
            bsdf.inputs["Specular IOR Level"].default_value = 0.2
        return mat
        
    mat_plate = make_color_material(f"{base_name}_PlateMat", plate_color)
    mat_cookie = make_color_material(f"{base_name}_CookieMat", cookie_color)
    mat_chip = make_color_material(f"{base_name}_ChipMat", chip_color)

    # === Step 2: Generate the Plate via BMesh ===
    bpy.ops.mesh.primitive_cube_add(
        size=2, 
        location=(location[0], location[1], location[2] - (0.1 * scale))
    )
    plate = bpy.context.active_object
    plate.name = f"{base_name}_Plate"
    plate.scale = (scale * 1.5, scale * 1.5, scale * 0.1)
    
    # Apply scale so bmesh operations calculate thickness proportionally
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    bm = bmesh.new()
    bm.from_mesh(plate.data)
    bm.faces.ensure_lookup_table()
    
    # Identify the top-facing polygon
    top_face = None
    for f in bm.faces:
        if f.normal.z > 0.9:
            top_face = f
            break
            
    if top_face:
        # Inset the top face to create the border lip
        bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.2 * scale)
        # Extrude the newly inset center face
        ext = bmesh.ops.extrude_face_region(bm, geom=[top_face])
        ext_verts = [elem for elem in ext['geom'] if isinstance(elem, bmesh.types.BMVert)]
        # Push the extruded face downwards to hollow out the plate
        bmesh.ops.translate(bm, vec=Vector((0, 0, -0.1 * scale)), verts=ext_verts)
        
    bm.to_mesh(plate.data)
    bm.free()
    plate.data.materials.append(mat_plate)

    # === Step 3: Generate the Cookie Base ===
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32, 
        radius=1.0 * scale, 
        depth=0.2 * scale, 
        location=(location[0], location[1], location[2] + (0.1 * scale))
    )
    cookie = bpy.context.active_object
    cookie.name = f"{base_name}_Dough"
    for poly in cookie.data.polygons:
        poly.use_smooth = True
    cookie.data.materials.append(mat_cookie)

    # === Step 4: Scatter the Chocolate Chips ===
    chip_parent = bpy.data.objects.new(f"{base_name}_Chips_Grp", None)
    chip_parent.location = location
    scene.collection.objects.link(chip_parent)
    
    num_chips = max(6, int(14 * scale))
    for i in range(num_chips):
        # Radial math to place chips on top of the cylinder
        radius = random.uniform(0.1 * scale, 0.85 * scale)
        angle = random.uniform(0, 2 * math.pi)
        x = location[0] + radius * math.cos(angle)
        y = location[1] + radius * math.sin(angle)
        z = location[2] + (0.2 * scale)
        
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=16, 
            ring_count=8, 
            radius=0.1 * scale, 
            location=(x, y, z)
        )
        chip = bpy.context.active_object
        chip.name = f"{base_name}_Chip_{i}"
        
        # Flatten the sphere to look like a settled chocolate chunk
        chip.scale = (1, 1, 0.6) 
        
        # Add slight natural rotation variance
        chip.rotation_euler = (
            random.uniform(-0.2, 0.2), 
            random.uniform(-0.2, 0.2), 
            random.uniform(0, 2 * math.pi)
        )
        
        for poly in chip.data.polygons:
            poly.use_smooth = True
            
        chip.data.materials.append(mat_chip)
        
        # Organization: Unlink from default collection, link to parent Empty
        chip.parent = chip_parent

    # === Step 5: Setup Contextual Lighting & Engine ===
    light_data = bpy.data.lights.new(name=f"{base_name}_KeyLight", type='AREA')
    light_data.energy = 850.0 * (scale ** 2) # Scale wattage relative to prop size
    light_data.color = (1.0, 0.9, 0.8) # Warm baking bulb color
    light_data.size = 2.0 * scale
    
    light_obj = bpy.data.objects.new(name=f"{base_name}_KeyLight", object_data=light_data)
    scene.collection.objects.link(light_obj)
    
    # Position light diagonally above the cookie
    light_obj.location = (
        location[0] - (2 * scale), 
        location[1] - (2 * scale), 
        location[2] + (3 * scale)
    )
    
    # Track the light to look perfectly at the cookie's origin
    direction = Vector(location) - light_obj.location
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    
    # Force Cycles rendering to benefit from Area Light soft shadows and tray ambient occlusion
    scene.render.engine = 'CYCLES'

    return f"Created '{base_name}' prop scene (Cookie, Plate, Chips, Lighting) at {location}."
