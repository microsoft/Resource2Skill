def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralLandscape",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.3, 0.1),  # Natural grassy/mossy green
    **kwargs,
) -> str:
    """
    Create a Procedural Sculpted Landscape in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created landscape object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (affects overall size, base size is 10x10 units).
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: 
            subdivisions (int): Density of the mesh (default: 6).
            noise_scale (float): Size of the hills/valleys (default: 1.5).
            displacement_strength (float): Height of the terrain (default: 0.8).

    Returns:
        Status string confirming creation.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # Create a 2x2 plane centered at origin
    verts = [(-1, -1, 0), (1, -1, 0), (-1, 1, 0), (1, 1, 0)]
    faces = [(0, 1, 3, 2)]
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    # === Step 2: Apply "Sculpting" Modifiers ===
    # 1. Provide geometry (equivalent to Subdivide in Edit Mode)
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    sub_levels = kwargs.get('subdivisions', 6)
    subsurf.levels = sub_levels
    subsurf.render_levels = sub_levels

    # 2. Procedural Texture for terrain generation
    tex_name = f"{object_name}_TerrainNoise"
    tex = bpy.data.textures.get(tex_name)
    if not tex:
        tex = bpy.data.textures.new(name=tex_name, type='CLOUDS')
        tex.noise_scale = kwargs.get('noise_scale', 1.5)
        tex.noise_depth = 2

    # 3. Displace Modifier (equivalent to manual sculpting strokes)
    disp = obj.modifiers.new(name="Displacement", type='DISPLACE')
    disp.texture = tex
    disp.direction = 'Z'
    disp.strength = kwargs.get('displacement_strength', 0.8)
    disp.mid_level = 0.5

    # Apply smooth shading to the base polygons
    for poly in mesh.polygons:
        poly.use_smooth = True

    # === Step 3: Build Material ===
    mat_name = f"{object_name}_Mat"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.85
            bsdf.inputs["Specular IOR Level"].default_value = 0.1

    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    
    # Landscapes are typically large wide planes.
    # We multiply X and Y by a base size of 5 (making it a 10x10 grid before user scale), 
    # but keep Z relatively contained so displacement strength remains predictable.
    base_spread = 5.0
    obj.scale = (base_spread * scale, base_spread * scale, scale)

    return f"Created '{object_name}' (Landscape) at {location} with {sub_levels} subdivision levels."
