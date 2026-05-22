def create_object(
    scene_name: str = "Scene",
    object_name: str = "ChocolateChipCookie_Set",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.4, 0.15),
    **kwargs,
) -> str:
    """
    Create a stylized Chocolate Chip Cookie sitting on a tray with custom lighting.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position of the composition.
        scale: Uniform scale factor for the entire composition.
        material_color: (R, G, B) base color for the cookie dough in 0-1 range.
        **kwargs: Additional optional overrides.

    Returns:
        Status string detailing the created composition.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector

    # Ensure scene exists and is active
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    bpy.context.window.scene = scene

    # --- 1. Create Root Empty ---
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = object_name
    
    # --- 2. Create Materials ---
    # Tray Material
    mat_tray = bpy.data.materials.new(name=f"{object_name}_TrayMat")
    mat_tray.use_nodes = True
    bsdf_tray = mat_tray.node_tree.nodes.get("Principled BSDF")
    bsdf_tray.inputs["Base Color"].default_value = (0.05, 0.2, 0.6, 1.0) # Blue
    bsdf_tray.inputs["Roughness"].default_value = 0.4

    # Cookie Material
    mat_cookie = bpy.data.materials.new(name=f"{object_name}_CookieMat")
    mat_cookie.use_nodes = True
    bsdf_cookie = mat_cookie.node_tree.nodes.get("Principled BSDF")
    bsdf_cookie.inputs["Base Color"].default_value = (*material_color, 1.0)
    bsdf_cookie.inputs["Roughness"].default_value = 0.85

    # Chip Material
    mat_chip = bpy.data.materials.new(name=f"{object_name}_ChipMat")
    mat_chip.use_nodes = True
    bsdf_chip = mat_chip.node_tree.nodes.get("Principled BSDF")
    bsdf_chip.inputs["Base Color"].default_value = (0.04, 0.015, 0.005, 1.0) # Dark Chocolate
    bsdf_chip.inputs["Roughness"].default_value = 0.3

    # --- 3. Generate the Tray ---
    tray_mesh = bpy.data.meshes.new(f"{object_name}_TrayMesh")
    tray_obj = bpy.data.objects.new(f"{object_name}_Tray", tray_mesh)
    scene.collection.objects.link(tray_obj)
    
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    # Scale cube into a flat tray plate
    bmesh.ops.scale(bm, vec=(3.0, 3.0, 0.2), verts=bm.verts)
    
    # Inset the top face to create the rim
    bm.faces.ensure_lookup_table()
    top_face = next((f for f in bm.faces if f.normal.z > 0.9), None)
    if top_face:
        bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.15)
        # The top_face reference now points to the inner face after inset. 
        # Translate it down to form the interior base.
        bmesh.ops.translate(bm, vec=(0, 0, -0.05), verts=top_face.verts)

    bm.to_mesh(tray_mesh)
    bm.free()
    tray_obj.data.materials.append(mat_tray)
    tray_obj.parent = root

    # --- 4. Generate the Cookie Base ---
    bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=0.2, vertices=32, location=(0, 0, 0.15))
    cookie_obj = bpy.context.active_object
    cookie_obj.name = f"{object_name}_Dough"
    
    for poly in cookie_obj.data.polygons:
        poly.use_smooth = True
    cookie_obj.data.materials.append(mat_cookie)
    cookie_obj.parent = root

    # --- 5. Generate and Scatter Chocolate Chips ---
    num_chips = kwargs.get("num_chips", 14)
    chip_objects = 0
    for i in range(num_chips):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, segments=16, ring_count=8)
        chip_obj = bpy.context.active_object
        chip_obj.name = f"{object_name}_Chip_{i}"
        
        # Flatten the chip slightly on Z
        chip_obj.scale = (1.0, 1.0, 0.6)
        
        # Random polar coordinate placement within cookie radius (0.85 to prevent clipping edges)
        r = random.uniform(0.0, 0.85)
        theta = random.uniform(0, 2 * math.pi)
        cx = r * math.cos(theta)
        cy = r * math.sin(theta)
        
        # Sits exactly half-embedded at the top face of the cookie (Z = 0.25)
        chip_obj.location = (cx, cy, 0.25)
        
        # Randomize tilt rotation
        chip_obj.rotation_euler = (
            random.uniform(-0.4, 0.4), 
            random.uniform(-0.4, 0.4), 
            random.uniform(0, 2 * math.pi)
        )

        for poly in chip_obj.data.polygons:
            poly.use_smooth = True
        chip_obj.data.materials.append(mat_chip)
        chip_obj.parent = root
        chip_objects += 1

    # --- 6. Set up Custom Lighting ---
    bpy.ops.object.light_add(type='AREA', location=(2.0, -2.0, 3.0))
    light_obj = bpy.context.active_object
    light_obj.name = f"{object_name}_Light"
    light_obj.data.energy = 850.0
    light_obj.data.color = (1.0, 0.85, 0.7) # Warm temperature ~4000K
    light_obj.data.size = 2.5
    
    # Track light to look at the cookie (origin)
    direction = Vector((0, 0, 0)) - light_obj.location
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    light_obj.parent = root

    # --- 7. Final Transforms ---
    # Apply requested location and scale to the parent empty
    root.location = Vector(location)
    root.scale = (scale, scale, scale)

    return f"Created '{object_name}' at {location} with 1 tray, 1 cookie, {chip_objects} chips, and 1 area light."
