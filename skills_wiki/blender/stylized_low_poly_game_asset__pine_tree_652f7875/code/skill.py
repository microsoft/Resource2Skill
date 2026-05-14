def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyTree",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    trunk_color: tuple = (0.15, 0.06, 0.02),
    leaf_color: tuple = (0.08, 0.25, 0.1),
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Pine Tree game asset.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the tree object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        trunk_color: (R, G, B) color for the wood.
        leaf_color: (R, G, B) color for the foliage.
        **kwargs: Additional options like 'num_layers' for foliage height.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import random
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection

    # Helper function to create a simple flat material
    def create_simple_material(name, color):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Ensure color has alpha channel
            if len(color) == 3:
                color = (color[0], color[1], color[2], 1.0)
            bsdf.inputs["Base Color"].default_value = color
            bsdf.inputs["Roughness"].default_value = 0.95
            if "Specular IOR Level" in bsdf.inputs: # Blender 4.0+
                bsdf.inputs["Specular IOR Level"].default_value = 0.1
            elif "Specular" in bsdf.inputs: # Older versions
                bsdf.inputs["Specular"].default_value = 0.1
        return mat

    # Create Materials
    mat_trunk = create_simple_material(f"{object_name}_Mat_Trunk", trunk_color)
    mat_foliage = create_simple_material(f"{object_name}_Mat_Foliage", leaf_color)

    # === 1. Create Trunk ===
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=7, # Low poly count
        radius=0.25, 
        depth=1.5, 
        location=(0, 0, 0.75)
    )
    trunk = bpy.context.active_object
    trunk.name = object_name
    trunk.data.materials.append(mat_trunk)

    # Taper the trunk slightly using bmesh
    bm = bmesh.new()
    bm.from_mesh(trunk.data)
    for v in bm.verts:
        if v.co.z > 0:
            v.co.x *= 0.6
            v.co.y *= 0.6
    # Ensure flat shading
    for f in bm.faces:
        f.smooth = False
    bm.to_mesh(trunk.data)
    bm.free()

    # === 2. Create Foliage Layers ===
    num_layers = kwargs.get('num_layers', 3)
    created_objects = [trunk]
    
    # Use a fixed seed for reproducible chunkiness, or random if preferred
    random.seed(hash(object_name) + hash(location))

    for i in range(num_layers):
        z_offset = 1.0 + (i * 0.9)
        scale_fac = 1.0 - (i * 0.25)
        
        # Icosphere is perfect for chunky low poly
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=1, 
            radius=1.2, 
            location=(0, 0, z_offset)
        )
        foliage = bpy.context.active_object
        foliage.name = f"{object_name}_Foliage_L{i}"
        
        # Scale to make it look more like a pine branch layer
        foliage.scale = (scale_fac, scale_fac, scale_fac * 0.8)
        
        # Randomize vertices for organic low-poly feel
        bm = bmesh.new()
        bm.from_mesh(foliage.data)
        for v in bm.verts:
            # Shift vertices outward/inward slightly
            v.co.x += random.uniform(-0.15, 0.15)
            v.co.y += random.uniform(-0.15, 0.15)
            v.co.z += random.uniform(-0.2, 0.2)
        
        # Enforce flat shading (crucial for low poly style)
        for f in bm.faces:
            f.smooth = False
            
        bm.to_mesh(foliage.data)
        bm.free()
        
        foliage.data.materials.append(mat_foliage)
        
        # Parent to trunk
        foliage.parent = trunk
        # Apply scale so it doesn't get messed up when root is scaled
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        created_objects.append(foliage)

    # === 3. Position & Scale Root Object ===
    # Set the trunk (parent) to the desired location and scale
    trunk.location = Vector(location)
    trunk.scale = (scale, scale, scale)

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created game-ready '{object_name}' (Low-Poly Tree) at {location} with {num_layers} foliage layers."
