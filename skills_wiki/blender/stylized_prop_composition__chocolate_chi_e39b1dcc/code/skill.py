def create_object(
    scene_name: str = "Scene",
    object_name: str = "CookieScene",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.6, 0.35, 0.15, 1.0), # Cookie base color
    **kwargs,
) -> str:
    """
    Create Stylized Prop Composition (Chocolate Chip Cookie on Tray) in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created hierarchy.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B, A) base color for the cookie dough.
        **kwargs: 
            tray_color: tuple (R, G, B, A)
            chip_color: tuple (R, G, B, A)
            chip_count: int (number of chocolate chips)

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Extract kwargs
    tray_color = kwargs.get("tray_color", (0.05, 0.15, 0.6, 1.0))
    chip_color = kwargs.get("chip_color", (0.03, 0.015, 0.005, 1.0))
    chip_count = kwargs.get("chip_count", 12)

    # --- Helper: Material Creation ---
    def make_material(name, color):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = color
            bsdf.inputs['Roughness'].default_value = 0.6 # Slightly rough
        return mat

    mat_tray = make_material(f"{object_name}_TrayMat", tray_color)
    mat_cookie = make_material(f"{object_name}_CookieMat", material_color)
    mat_chip = make_material(f"{object_name}_ChipMat", chip_color)

    # --- Step 1: Create the Tray (using BMesh for Inset/Extrude) ---
    bpy.ops.mesh.primitive_cube_add(size=1)
    tray = bpy.context.active_object
    tray.name = f"{object_name}_Tray"
    
    # Scale tray to make it a flat square plate
    tray_scale_x = 2.5 * scale
    tray_scale_z = 0.2 * scale
    tray.scale = (tray_scale_x, tray_scale_x, tray_scale_z)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # BMesh operations: Inset top face and push down
    bm = bmesh.new()
    bm.from_mesh(tray.data)
    bm.faces.ensure_lookup_table()
    
    # Find the top-facing face
    top_face = None
    for face in bm.faces:
        if face.normal.z > 0.9:
            top_face = face
            break
            
    if top_face:
        # Inset the face
        inset_result = bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.15 * scale)
        # The original top_face is shrunk to the center. Push it down.
        bmesh.ops.translate(bm, vec=Vector((0, 0, -0.05 * scale)), verts=top_face.verts)
        
    bm.to_mesh(tray.data)
    bm.free()
    tray.data.materials.append(mat_tray)

    # --- Step 2: Create the Cookie Base ---
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1, depth=1)
    cookie = bpy.context.active_object
    cookie.name = f"{object_name}_Dough"
    
    # Scale into a cookie shape
    cookie_radius = 1.2 * scale
    cookie_height = 0.25 * scale
    cookie.scale = (cookie_radius, cookie_radius, cookie_height)
    
    # Position cookie on the tray
    cookie.location = (0, 0, (tray_scale_z / 2) + (cookie_height / 2) - (0.05 * scale))
    
    # Shade Smooth
    for poly in cookie.data.polygons:
        poly.use_smooth = True
        
    cookie.data.materials.append(mat_cookie)
    cookie.parent = tray # Parent to tray for easy moving

    # --- Step 3: Generate and Scatter Chocolate Chips ---
    chip_radius = 0.15 * scale
    chip_height = 0.08 * scale
    
    for i in range(chip_count):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=1)
        chip = bpy.context.active_object
        chip.name = f"{object_name}_Chip_{i+1}"
        
        # Flatten the sphere to look like a chip
        chip.scale = (chip_radius, chip_radius, chip_height)
        chip.data.materials.append(mat_chip)
        for poly in chip.data.polygons:
            poly.use_smooth = True
            
        # Random distribution within a circle (keeping them away from the absolute edge)
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(0, cookie_radius * 0.75)
        
        cx = dist * math.cos(angle)
        cy = dist * math.sin(angle)
        
        # Place chip slightly embedded into the top of the cookie
        cz = cookie.location.z + (cookie_height / 2)
        
        chip.location = (cx, cy, cz)
        
        # Add slight random rotation for realism
        chip.rotation_euler = (
            random.uniform(-0.2, 0.2), 
            random.uniform(-0.2, 0.2), 
            random.uniform(0, 2 * math.pi)
        )
        
        chip.parent = cookie

    # --- Step 4: Add Warm Lighting Context ---
    bpy.ops.object.light_add(type='AREA', radius=2.0 * scale, location=(0, -1.0 * scale, 3.0 * scale))
    light = bpy.context.active_object
    light.name = f"{object_name}_WarmLight"
    
    # Angle light towards the cookie
    light.rotation_euler = (math.radians(15), 0, 0)
    
    # Set light properties (Warm 4000K, bright)
    light.data.energy = 850.0 * (scale ** 2)
    # Convert 4000K approx to RGB (warm yellow/white)
    light.data.color = (1.0, 0.85, 0.7)
    
    light.parent = tray

    # --- Finalize Global Placement ---
    tray.location = Vector(location)

    return f"Created '{object_name}' scene (Tray, Cookie, {chip_count} Chips, Light) at {location}."
