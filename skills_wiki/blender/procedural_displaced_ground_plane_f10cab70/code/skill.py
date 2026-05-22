def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralGround",
    location: tuple = (0, 0, 0),
    scale: float = 5.0,
    material_color: tuple = (0.35, 0.25, 0.15),
    **kwargs,
) -> str:
    """
    Create a Procedural Displaced Ground Plane in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the ground plane.
        material_color: (R, G, B) base color representing soil/dirt.
        **kwargs: 
            grid_subdivisions (int): Number of subdivisions for the grid (default 100).
            displace_strength (float): Intensity of the displacement (default 0.15).
            noise_size (float): Scale of the cloud noise (default 0.5).

    Returns:
        Status string describing the created object.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    
    # Get scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Extract kwargs with fallbacks
    grid_subdivisions = kwargs.get('grid_subdivisions', 100)
    displace_strength = kwargs.get('displace_strength', 0.15)
    noise_size = kwargs.get('noise_size', 0.5)

    # === Step 1: Create Base Geometry ===
    # Using a high-resolution grid directly bypasses the need for Edit Mode subdivisions
    bpy.ops.mesh.primitive_grid_add(
        x_subdivisions=grid_subdivisions, 
        y_subdivisions=grid_subdivisions, 
        size=2.0, 
        location=location
    )
    
    obj = bpy.context.active_object
    obj.name = object_name
    
    # Apply scale uniformly
    obj.scale = (scale, scale, scale)
    
    # Enable smooth shading for a natural look
    bpy.ops.object.shade_smooth()

    # === Step 2: Create Procedural Texture ===
    # This texture lives in Blender's internal texture data, specifically for modifiers
    tex_name = f"{object_name}_CloudsTex"
    tex = bpy.data.textures.new(name=tex_name, type='CLOUDS')
    tex.noise_scale = noise_size
    tex.noise_depth = 2

    # === Step 3: Add Displacement Modifier ===
    mod = obj.modifiers.new(name="GroundDisplacement", type='DISPLACE')
    mod.texture = tex
    mod.strength = displace_strength
    mod.mid_level = 0.5

    # === Step 4: Build & Assign Material ===
    mat_name = f"{object_name}_DirtMat"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        
        if mat.node_tree:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                # Set dirt base color
                bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
                # Dirt is highly rough and non-metallic
                bsdf.inputs["Roughness"].default_value = 0.85
                bsdf.inputs["Specular IOR Level"].default_value = 0.2
                
    # Assign material to object
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    # Link to specified scene if not already in it
    if obj.name not in scene.collection.objects:
        scene.collection.objects.link(obj)

    return f"Created '{object_name}' (Grid {grid_subdivisions}x{grid_subdivisions}) at {location} with displacement strength {displace_strength}."
