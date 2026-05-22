def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyTree",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.15, 0.5, 0.2),  # Stylized Green
    **kwargs,
) -> str:
    """
    Create a Game-Ready Stylized Low-Poly Pine Tree.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created hierarchy.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the foliage in 0-1 range.
        **kwargs: Can include 'num_layers' (int) and 'trunk_color' (R,G,B).

    Returns:
        Status string detailing the created geometry.
    """
    import bpy
    import bmesh
    import mathutils
    import random
    from mathutils import Vector

    # Fetch the target scene and collection
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection

    # -----------------------------------------
    # 1. Material Setup
    # -----------------------------------------
    trunk_color = kwargs.get('trunk_color', (0.25, 0.12, 0.05))
    if len(trunk_color) == 3: trunk_color = (*trunk_color, 1.0)
    if len(material_color) == 3: material_color = (*material_color, 1.0)

    # Trunk Material
    mat_trunk = bpy.data.materials.new(name=f"{object_name}_Trunk_Mat")
    mat_trunk.use_nodes = True
    bsdf_trunk = mat_trunk.node_tree.nodes.get("Principled BSDF")
    if bsdf_trunk:
        bsdf_trunk.inputs['Base Color'].default_value = trunk_color
        bsdf_trunk.inputs['Roughness'].default_value = 0.9
        bsdf_trunk.inputs['Specular'].default_value = 0.1

    # Foliage Material
    mat_foliage = bpy.data.materials.new(name=f"{object_name}_Foliage_Mat")
    mat_foliage.use_nodes = True
    bsdf_foliage = mat_foliage.node_tree.nodes.get("Principled BSDF")
    if bsdf_foliage:
        bsdf_foliage.inputs['Base Color'].default_value = material_color
        bsdf_foliage.inputs['Roughness'].default_value = 0.95
        bsdf_foliage.inputs['Specular'].default_value = 0.1

    # -----------------------------------------
    # 2. Hierarchy Setup
    # -----------------------------------------
    root = bpy.data.objects.new(object_name, None)
    root.location = Vector(location)
    root.scale = (scale, scale, scale)
    collection.objects.link(root)

    def add_mesh_to_scene(name, mesh, parent, mat):
        obj = bpy.data.objects.new(name, mesh)
        obj.parent = parent
        obj.data.materials.append(mat)
        collection.objects.link(obj)
        # Force flat shading for the low-poly aesthetic
        for poly in mesh.polygons:
            poly.use_smooth = False
        return obj

    # -----------------------------------------
    # 3. Geometry Generation
    # -----------------------------------------
    
    # --- Generate Trunk ---
    bm = bmesh.new()
    trunk_height = 0.8
    # 6 segments creates a nice blocky cylinder
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=6,
        radius1=0.2, radius2=0.15, depth=trunk_height,
        matrix=mathutils.Matrix.Translation((0, 0, trunk_height / 2))
    )
    trunk_mesh = bpy.data.meshes.new(f"{object_name}_Trunk")
    bm.to_mesh(trunk_mesh)
    bm.free()
    
    add_mesh_to_scene(f"{object_name}_Trunk", trunk_mesh, root, mat_trunk)

    # --- Generate Foliage Layers ---
    num_layers = kwargs.get('num_layers', 3)
    base_radius = 0.9
    base_height = 1.0
    z_offset = trunk_height * 0.8 # Overlap the bottom leaf layer with the trunk

    for i in range(num_layers):
        bm = bmesh.new()
        
        # Taper the size of the cones as they go up
        radius = base_radius * (1.0 - (i * 0.25))
        depth = base_height * (1.0 - (i * 0.15))
        
        # 7 segments avoids perfect symmetry, looking more stylized
        bmesh.ops.create_cone(
            bm, cap_ends=True, cap_tris=True, segments=7,
            radius1=radius, radius2=0.0, depth=depth,
            matrix=mathutils.Matrix.Translation((0, 0, z_offset + depth / 2))
        )
        
        # Apply slight randomization to vertices to make it organic
        for v in bm.verts:
            v.co.x += random.uniform(-0.06, 0.06)
            v.co.y += random.uniform(-0.06, 0.06)
            # Only randomize the bottom rim on the Z axis
            if v.co.z < (z_offset + depth / 2):
                v.co.z += random.uniform(-0.08, 0.08)

        foliage_mesh = bpy.data.meshes.new(f"{object_name}_Foliage_L{i+1}")
        bm.to_mesh(foliage_mesh)
        bm.free()
        
        add_mesh_to_scene(f"{object_name}_Foliage_L{i+1}", foliage_mesh, root, mat_foliage)
        
        # Step up for the next layer (overlapping them slightly)
        z_offset += depth * 0.55

    return f"Created game-ready low-poly hierarchy '{object_name}' at {location} with {num_layers} foliage layers."
