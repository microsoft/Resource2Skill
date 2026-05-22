def create_object(
    scene_name: str = "Scene",
    object_name: str = "ChocolateCookieTray",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.45, 0.25),
    **kwargs,
) -> str:
    """
    Create a composite Chocolate Chip Cookie on a baking tray with procedural chip scattering.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position for the tray assembly.
        scale: Uniform scale factor for the entire assembly.
        material_color: (R, G, B) base color for the cookie dough.
        **kwargs: 
            - num_chips (int): Number of chocolate chips to scatter (default: 18)
            - tray_color (tuple): (R, G, B) color of the tray (default: Blue)

    Returns:
        Status string detailing the created assembly.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math
    import random

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection
    
    # === Step 1: Material Setup ===
    def create_mat(name, color, roughness):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Ensure color is 4D (RGBA)
            if len(color) == 3:
                color = (*color, 1.0)
            bsdf.inputs['Base Color'].default_value = color
            bsdf.inputs['Roughness'].default_value = roughness
        return mat
        
    mat_cookie = create_mat(f"{object_name}_CookieMat", material_color, 0.7)
    mat_chip = create_mat(f"{object_name}_ChipMat", (0.04, 0.015, 0.005, 1.0), 0.3)
    tray_color = kwargs.get('tray_color', (0.1, 0.2, 0.6, 1.0))
    mat_tray = create_mat(f"{object_name}_TrayMat", tray_color, 0.5)
    
    # === Step 2: Tray Geometry (Cube -> Inset -> Extrude) ===
    bm_tray = bmesh.new()
    bmesh.ops.create_cube(bm_tray, size=1.0)
    # Scale cube into a flat tray (bounds become Z: -0.1 to 0.1)
    bmesh.ops.scale(bm_tray, vec=(4.0, 4.0, 0.2), verts=bm_tray.verts)
    bm_tray.faces.ensure_lookup_table()
    
    # Find top face and inset it
    top_face = [f for f in bm_tray.faces if f.normal.z > 0.9][0]
    bmesh.ops.inset_region(bm_tray, faces=[top_face], thickness=0.2)
    # Push inner face down to create tray floor exactly at local Z = 0.0
    bmesh.ops.translate(bm_tray, vec=(0, 0, -0.1), verts=top_face.verts)
    
    tray_mesh = bpy.data.meshes.new(f"{object_name}_TrayMesh")
    bm_tray.to_mesh(tray_mesh)
    bm_tray.free()
    
    tray_obj = bpy.data.objects.new(object_name, tray_mesh)
    collection.objects.link(tray_obj)
    tray_obj.data.materials.append(mat_tray)
    
    # === Step 3: Cookie Base Geometry ===
    bm_cookie = bmesh.new()
    bmesh.ops.create_cone(bm_cookie, cap_ends=True, cap_tris=False, segments=32, radius1=1.2, radius2=1.2, depth=0.3)
    cookie_mesh = bpy.data.meshes.new(f"{object_name}_CookieMesh")
    bm_cookie.to_mesh(cookie_mesh)
    bm_cookie.free()
    
    for poly in cookie_mesh.polygons:
        poly.use_smooth = True
        
    cookie_obj = bpy.data.objects.new(f"{object_name}_Cookie", cookie_mesh)
    collection.objects.link(cookie_obj)
    cookie_obj.parent = tray_obj
    
    # Position: Cookie depth is 0.3 (bounds -0.15 to +0.15). Moving up by 0.15 places bottom exactly on tray floor.
    cookie_obj.location = (0, 0, 0.15) 
    cookie_obj.data.materials.append(mat_cookie)
    
    # === Step 4: Chocolate Chips (Scatter Logic) ===
    bm_chip = bmesh.new()
    bmesh.ops.create_uvsphere(bm_chip, u_segments=16, v_segments=8, radius=0.12)
    bmesh.ops.scale(bm_chip, vec=(1.0, 1.0, 0.8), verts=bm_chip.verts) # Squash slightly
    chip_mesh = bpy.data.meshes.new(f"{object_name}_ChipMesh")
    bm_chip.to_mesh(chip_mesh)
    bm_chip.free()
    
    for poly in chip_mesh.polygons:
        poly.use_smooth = True
    chip_mesh.materials.append(mat_chip)
    
    num_chips = kwargs.get('num_chips', 18)
    random.seed(hash(object_name)) # Consistent scatter per object name
    
    for i in range(num_chips):
        chip = bpy.data.objects.new(f"{object_name}_Chip_{i}", chip_mesh)
        collection.objects.link(chip)
        chip.parent = cookie_obj
        
        # Uniform circular area distribution (kept within 1.05 radius to avoid overhanging edges)
        r = 1.05 * math.sqrt(random.uniform(0, 1))
        theta = random.uniform(0, 2 * math.pi)
        
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        # Surface of cookie is local Z=0.15. Add slight noise so they sink naturally.
        z = 0.15 + random.uniform(-0.02, 0.04) 
        
        chip.location = (x, y, z)
        chip.rotation_euler = (
            random.uniform(-0.4, 0.4), 
            random.uniform(-0.4, 0.4), 
            random.uniform(0, math.pi*2)
        )
        chip.scale = (random.uniform(0.8, 1.2),) * 3

    # === Step 5: Add Dedicated Lighting ===
    light_data = bpy.data.lights.new(name=f"{object_name}_Light", type='AREA')
    light_data.energy = 1000.0
    light_data.color = (1.0, 0.85, 0.7) # Warm tungsten vibe
    light_data.size = 3.0
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_LightObj", object_data=light_data)
    collection.objects.link(light_obj)
    light_obj.parent = tray_obj
    light_obj.location = (2.5, -2.5, 3.0)
    
    # Track the light towards the cookie
    dir_vec = (Vector((0, 0, 0)) - light_obj.location).normalized()
    light_obj.rotation_euler = dir_vec.to_track_quat('-Z', 'Y').to_euler()

    # === Step 6: Final Placement ===
    tray_obj.location = Vector(location)
    tray_obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' (Tray, Cookie, and {num_chips} Chips) at {location}"
