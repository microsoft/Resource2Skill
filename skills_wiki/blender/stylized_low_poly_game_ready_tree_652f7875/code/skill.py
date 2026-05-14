def create_low_poly_tree(
    scene_name: str = "Scene",
    object_name: str = "LowPolyTree",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    trunk_color: tuple = (0.35, 0.20, 0.10),
    foliage_color: tuple = (0.15, 0.60, 0.20),
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Game-Ready Tree in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the tree objects.
        location: (x, y, z) world-space position of the tree base.
        scale: Uniform scale factor.
        trunk_color: (R, G, B) base color for the wood.
        foliage_color: (R, G, B) base color for the leaves.
        **kwargs: Additional overrides (e.g., foliage_radius).

    Returns:
        Status string describing the creation.
    """
    import bpy
    import bmesh
    import random
    from mathutils import Vector

    # Ensure we are in object mode before generating meshes
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # Deselect all to ensure clean additive operation
    bpy.ops.object.select_all(action='DESELECT')

    # === Step 1: Create Trunk Geometry ===
    trunk_height = 2.0
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8, 
        radius=0.4, 
        depth=trunk_height, 
        location=(0, 0, trunk_height / 2) # Base sits at Z=0 locally
    )
    trunk = bpy.context.active_object
    trunk.name = f"{object_name}_Trunk"

    # Taper the top of the trunk using BMesh
    bm = bmesh.new()
    bm.from_mesh(trunk.data)
    for v in bm.verts:
        if v.co.z > 0.1:  # Select top vertices
            v.co.x *= 0.4
            v.co.y *= 0.4
    
    # Ensure flat shading for low-poly look
    for f in bm.faces:
        f.smooth = False
        
    bm.to_mesh(trunk.data)
    bm.free()

    # === Step 2: Create Foliage Geometry ===
    foliage_radius = kwargs.get("foliage_radius", 1.8)
    foliage_height_offset = trunk_height * 0.9
    
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=1, # Keep very low for stylized look
        radius=foliage_radius, 
        location=(0, 0, foliage_height_offset)
    )
    foliage = bpy.context.active_object
    foliage.name = f"{object_name}_Foliage"

    # Randomize foliage vertices for organic chunky look
    bm = bmesh.new()
    bm.from_mesh(foliage.data)
    for v in bm.verts:
        # Move vertices randomly outwards/inwards and slightly side-to-side
        random_vec = Vector((
            random.uniform(-0.3, 0.3), 
            random.uniform(-0.3, 0.3), 
            random.uniform(-0.3, 0.3)
        ))
        v.co += random_vec

    # Ensure flat shading for low-poly look
    for f in bm.faces:
        f.smooth = False

    bm.to_mesh(foliage.data)
    bm.free()

    # === Step 3: Build Materials ===
    def create_simple_material(mat_name, rgb_color):
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Convert RGB tuple to RGBA
            bsdf.inputs["Base Color"].default_value = (*rgb_color, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.9  # Matte look
            if "Specular" in bsdf.inputs:
                bsdf.inputs["Specular"].default_value = 0.1
            elif "Specular IOR Level" in bsdf.inputs: # Blender 4.0+
                bsdf.inputs["Specular IOR Level"].default_value = 0.1
        return mat

    mat_trunk = create_simple_material(f"{object_name}_Trunk_Mat", trunk_color)
    mat_foliage = create_simple_material(f"{object_name}_Foliage_Mat", foliage_color)

    trunk.data.materials.append(mat_trunk)
    foliage.data.materials.append(mat_foliage)

    # === Step 4: Parent, Position & Scale ===
    # Parent foliage to trunk
    foliage.parent = trunk
    # Keep the offset transformation during parenting
    foliage.matrix_parent_inverse = trunk.matrix_world.inverted()

    # Apply global location and scale to the parent (trunk)
    trunk.location = Vector(location)
    trunk.scale = (scale, scale, scale)

    # Link to a specific collection if necessary, though ops.mesh.add does this to the active collection automatically.
    
    return f"Created '{object_name}' (Trunk & Foliage) at {location} with scale {scale}. Ready for game engine export."
