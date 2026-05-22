def create_low_poly_well_base(
    scene_name: str = "Scene",
    object_name: str = "LowPolyWellBase",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.45, 0.42, 0.48),
    **kwargs,
) -> str:
    """
    Create a procedural stylized low-poly stone ring (well base) in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the stone.
        **kwargs: Additional options (e.g., stone_count, decimate_ratio).

    Returns:
        Status string describing the creation.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Parameters
    stone_count = kwargs.get("stone_count", 16)
    decimate_ratio = kwargs.get("decimate_ratio", 0.35)
    
    # === Step 1: Create Base Geometry (Single Brick) ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    
    # Scale to brick shape (length, width, height)
    bmesh.ops.scale(bm, vec=(0.8, 0.4, 0.35), verts=bm.verts)
    
    # Shift along X axis so the bounding box starts roughly at X=0.
    # This is critical for the Bend modifier to form a proper circle.
    bmesh.ops.translate(bm, vec=(0.4, 0.0, 0.0), verts=bm.verts)
    
    bm.to_mesh(mesh)
    bm.free()

    # === Step 2: Build the Procedural Modifier Stack ===
    
    # 2a. Bevel (soften initial edges)
    mod_bev = obj.modifiers.new("Bevel", 'BEVEL')
    mod_bev.width = 0.05
    mod_bev.segments = 2

    # 2b. Subdivide (provides geometry for the noise to warp)
    mod_sub = obj.modifiers.new("Subdiv", 'SUBSURF')
    mod_sub.subdivision_type = 'SIMPLE'
    mod_sub.levels = 2

    # 2c. Array (create the long line of stones)
    mod_arr = obj.modifiers.new("Array", 'ARRAY')
    mod_arr.count = stone_count
    mod_arr.use_relative_offset = True
    mod_arr.relative_offset_displace[0] = 1.05 # slight gap between stones

    # 2d. Displace (adds organic wobble to replace manual vertex pushing)
    tex_noise = bpy.data.textures.new(name=f"{object_name}_Noise", type='CLOUDS')
    tex_noise.noise_scale = 0.5
    
    mod_disp = obj.modifiers.new("Displace", 'DISPLACE')
    mod_disp.texture = tex_noise
    mod_disp.strength = 0.08
    mod_disp.direction = 'NORMAL'

    # 2e. Simple Deform (Bend the array into a 360-degree circle)
    mod_bend = obj.modifiers.new("Bend", 'SIMPLE_DEFORM')
    mod_bend.deform_method = 'BEND'
    mod_bend.angle = math.radians(360)
    mod_bend.deform_axis = 'Z'
    
    # 2f. Weld (merges the seam where the first and last stone touch)
    mod_weld = obj.modifiers.new("Weld", 'WELD')
    mod_weld.merge_threshold = 0.05

    # 2g. Decimate (The secret sauce: turns dense wobbly mesh into faceted low-poly)
    mod_dec = obj.modifiers.new("Decimate", 'DECIMATE')
    mod_dec.ratio = decimate_ratio

    # === Step 3: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Set base color, high roughness for stone, low specular
            bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.95
            
            # For Blender 4.0+ Specular is usually mapped differently, but setting IOR/Specular helps
            if 'Specular IOR Level' in bsdf.inputs:
                bsdf.inputs['Specular IOR Level'].default_value = 0.1
            elif 'Specular' in bsdf.inputs:
                bsdf.inputs['Specular'].default_value = 0.1

    obj.data.materials.append(mat)

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    # Smooth shading is technically wrong for standard low poly, 
    # but the Decimate modifier retains flat shading on generated faces natively.

    return f"Created '{object_name}' (Procedural Stone Ring) at {location} using {stone_count} stones."
