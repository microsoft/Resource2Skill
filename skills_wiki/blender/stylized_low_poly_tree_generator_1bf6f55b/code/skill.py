def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyTree",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.4, 0.1),  # Leaf Color
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Tree in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created tree hierarchy.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the leaves.
        **kwargs: Optional 'trunk_color' as an (R,G,B) tuple.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import random

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    trunk_color = kwargs.get("trunk_color", (0.15, 0.05, 0.02))

    # --- Step 1: Create the Trunk ---
    # Create a 10-sided cylinder for the low-poly trunk look
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=10, 
        radius=0.4, 
        depth=4.0, 
        location=(0, 0, 2.0)
    )
    trunk = bpy.context.active_object
    trunk.name = f"{object_name}_Trunk"

    # Taper the trunk using bmesh
    bm = bmesh.new()
    bm.from_mesh(trunk.data)
    for v in bm.verts:
        if v.co.z > 0:  # Select top vertices
            v.co.x *= 0.25
            v.co.y *= 0.25
        else:           # Flare out the base slightly
            v.co.x *= 1.2
            v.co.y *= 1.2
    bm.to_mesh(trunk.data)
    bm.free()

    # Ensure flat shading for the trunk
    for poly in trunk.data.polygons:
        poly.use_smooth = False

    # --- Step 2: Create the Canopy ---
    # Define offsets for a cluster of icospheres
    canopy_offsets = [
        (0.0, 0.0, 4.0),
        (0.8, 0.4, 3.5),
        (-0.7, 0.5, 3.2),
        (0.3, -0.9, 3.4),
        (-0.4, -0.6, 3.7)
    ]
    
    canopy_parts = []
    for offset in canopy_offsets:
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=2, 
            radius=1.2 + random.uniform(-0.2, 0.2), 
            location=offset
        )
        canopy_parts.append(bpy.context.active_object)

    # Join the canopy parts into a single object
    bpy.ops.object.select_all(action='DESELECT')
    for part in canopy_parts:
        part.select_set(True)
    bpy.context.view_layer.objects.active = canopy_parts[0]
    bpy.ops.object.join()
    canopy = bpy.context.active_object
    canopy.name = f"{object_name}_Canopy"

    # Apply Modifiers to fuse and stylize the canopy
    # 1. Remesh: Fuses the intersecting spheres into one continuous volume
    remesh = canopy.modifiers.new(name="Fuse_Spheres", type='REMESH')
    remesh.mode = 'VOXEL'
    remesh.voxel_size = 0.2
    
    # 2. Decimate: Reduces polygons to create the sharp, low-poly faceted look
    decimate = canopy.modifiers.new(name="LowPoly_Facets", type='DECIMATE')
    decimate.ratio = 0.15

    # Ensure flat shading for the canopy
    for poly in canopy.data.polygons:
        poly.use_smooth = False

    # --- Step 3: Materials ---
    # Trunk Material
    mat_trunk = bpy.data.materials.new(name=f"{object_name}_Mat_Trunk")
    mat_trunk.use_nodes = True
    bsdf_trunk = mat_trunk.node_tree.nodes.get("Principled BSDF")
    if bsdf_trunk:
        bsdf_trunk.inputs["Base Color"].default_value = (*trunk_color, 1.0)
        bsdf_trunk.inputs["Roughness"].default_value = 0.95
        bsdf_trunk.inputs["Specular IOR Level"].default_value = 0.1
    trunk.data.materials.append(mat_trunk)

    # Canopy Material
    mat_leaves = bpy.data.materials.new(name=f"{object_name}_Mat_Leaves")
    mat_leaves.use_nodes = True
    bsdf_leaves = mat_leaves.node_tree.nodes.get("Principled BSDF")
    if bsdf_leaves:
        bsdf_leaves.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf_leaves.inputs["Roughness"].default_value = 0.95
        bsdf_leaves.inputs["Specular IOR Level"].default_value = 0.1
    canopy.data.materials.append(mat_leaves)

    # --- Step 4: Hierarchy and Transforms ---
    # Parent canopy to trunk
    canopy.parent = trunk
    canopy.matrix_parent_inverse = trunk.matrix_world.inverted()

    # Apply final positioning and scale to the parent (trunk)
    trunk.location = Vector(location)
    trunk.scale = (scale, scale, scale)

    # Ensure trunk is the active selected object at the end
    bpy.ops.object.select_all(action='DESELECT')
    trunk.select_set(True)
    canopy.select_set(True)
    bpy.context.view_layer.objects.active = trunk

    return f"Created '{object_name}' (Stylized Low-Poly Tree) at {location} with scale {scale}"
