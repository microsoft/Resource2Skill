def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralTerrain",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.3, 0.05, 1.0),
    **kwargs,
) -> str:
    """
    Create a procedural terrain using mathematical proportional falloff in the active scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created terrain object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B, A) base color for the terrain.
        **kwargs: 
            size (float): The overall width/length of the plane (default 10.0).
            subdivisions (int): Number of grid segments (default 60).
            hills (list of dicts): [{'center': (x,y), 'radius': r, 'height': h}, ...]

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Configuration ---
    plane_size = kwargs.get('size', 10.0)
    subdivisions = kwargs.get('subdivisions', 60)
    
    # Default topography if none is provided: 2 hills and 1 valley
    hills = kwargs.get('hills', [
        {'center': (2.0, 2.0), 'radius': 3.0, 'height': 1.5},
        {'center': (-2.5, -1.0), 'radius': 4.0, 'height': 2.2},
        {'center': (1.0, -3.0), 'radius': 2.5, 'height': -1.2}  # Negative height = valley
    ])

    # === Step 1: Create Base Geometry (Grid) ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    
    # In bmesh.ops.create_grid, size is the half-width.
    half_size = plane_size / 2.0
    bmesh.ops.create_grid(
        bm, 
        x_segments=subdivisions, 
        y_segments=subdivisions, 
        size=half_size
    )

    # === Step 2: Apply Mathematical Proportional Editing ===
    # For every vertex, calculate distance to each hill's center. 
    # If within radius, apply smooth displacement (Cosine falloff).
    for v in bm.verts:
        for hill in hills:
            hx, hy = hill['center']
            # Calculate distance in XY plane
            dx = v.co.x - hx
            dy = v.co.y - hy
            dist = math.sqrt(dx*dx + dy*dy)
            
            radius = hill['radius']
            height = hill['height']
            
            if dist < radius:
                # Smooth falloff mimicking Blender's "Smooth" proportional editing
                # (cos(pi * (dist/radius)) + 1) / 2 creates a smooth bell-like curve from 1 to 0
                falloff = (math.cos(math.pi * (dist / radius)) + 1.0) * 0.5
                v.co.z += height * falloff

    # Write bmesh data back to standard mesh
    bm.to_mesh(mesh)
    bm.free()

    # Shade Smooth
    for poly in mesh.polygons:
        poly.use_smooth = True

    # === Step 3: Material & Shading ===
    mat = bpy.data.materials.new(name=object_name + "_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    if bsdf:
        bsdf.inputs["Base Color"].default_value = material_color
        bsdf.inputs["Roughness"].default_value = 0.9  # Matte look for terrain
        # In newer Blender versions, Specular might be structured differently, 
        # but adjusting roughness usually suffices for a matte finish.

    obj.data.materials.append(mat)

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # Ensure the object is active and selected
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    return f"Created '{object_name}' terrain at {location} with {len(hills)} topographical features."
