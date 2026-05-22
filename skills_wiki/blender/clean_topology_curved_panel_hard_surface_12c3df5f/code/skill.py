def create_clean_curved_boolean(
    scene_name: str = "Scene",
    object_name: str = "CleanCurvedPanel",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.2, 0.05),
    **kwargs,
) -> str:
    """
    Create a clean-topology curved hard-surface panel with a cutout in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (Flat Grid) ===
    bm = bmesh.new()
    segments_x = 32
    segments_y = 32
    size_x = 4.0
    size_y = 4.0
    
    # Generate vertices
    verts = []
    for i in range(segments_x + 1):
        row = []
        for j in range(segments_y + 1):
            x = (i / segments_x) * size_x - (size_x / 2)
            y = (j / segments_y) * size_y - (size_y / 2)
            v = bm.verts.new((x, y, 0.0))
            row.append(v)
        verts.append(row)
        
    # Generate faces with a central rectangular hole
    for i in range(segments_x):
        for j in range(segments_y):
            # Calculate face center
            cx = (i / segments_x) * size_x - (size_x / 2) + (size_x / segments_x / 2)
            cy = (j / segments_y) * size_y - (size_y / 2) + (size_y / segments_y / 2)
            
            # Define rectangular hole (1.2 wide, 2.0 tall)
            if abs(cx) < 0.6 and abs(cy) < 1.0:
                continue
                
            v1 = verts[i][j]
            v2 = verts[i+1][j]
            v3 = verts[i+1][j+1]
            v4 = verts[i][j+1]
            bm.faces.new((v1, v2, v3, v4))

    # === Step 2: Crease Outer Boundaries ===
    # Prevents the Subsurf modifier from shrinking the outer edges of the panel
    crease_layer = bm.edges.layers.crease.verify()
    for e in bm.edges:
        if e.is_boundary:
            is_outer = True
            for v in e.verts:
                # If a vertex is strictly inside the perimeter, it belongs to the inner hole
                if abs(v.co.x) < (size_x / 2 - 0.01) and abs(v.co.y) < (size_y / 2 - 0.01):
                    is_outer = False
            if is_outer:
                e[crease_layer] = 1.0

    # === Step 3: Bend into a Curve (Cylindrical Mapping) ===
    radius = 1.5
    for v in bm.verts:
        x, y, z = v.co
        # Map X distance to angle around the Z axis
        theta = x / radius
        new_x = radius * math.sin(theta)
        new_y = y
        new_z = radius * math.cos(theta) - radius
        v.co = Vector((new_x, new_y, new_z))

    # Finalize BMesh to Object
    mesh = bpy.data.meshes.new(object_name)
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # === Step 4: Modifiers for Clean Hard-Surface Detailing ===
    # 1. Subsurf: Rounds the square hole into a smooth capsule slot perfectly
    subdiv = obj.modifiers.new("Subdivision", 'SUBSURF')
    subdiv.levels = 2
    subdiv.render_levels = 2

    # 2. Solidify: Extrudes to give the curved panel physical thickness
    solid = obj.modifiers.new("Solidify", 'SOLIDIFY')
    solid.thickness = 0.1
    solid.offset = 1.0

    # 3. Bevel: Catches the 90-degree cut edges to create machined highlights
    bevel = obj.modifiers.new("Bevel", 'BEVEL')
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(35)
    bevel.width = 0.015
    bevel.segments = 3
    bevel.profile = 0.5
    
    # Smooth Shading application
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.shade_smooth()
    
    # Handle older Auto Smooth API safely
    if bpy.app.version < (4, 1, 0):
        obj.data.use_auto_smooth = True
        obj.data.auto_smooth_angle = math.radians(30)

    # === Step 5: Material Setup ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Metallic"].default_value = 0.8
        bsdf.inputs["Roughness"].default_value = 0.25
        if "Clearcoat" in bsdf.inputs:
            bsdf.inputs["Clearcoat"].default_value = 0.5

    if not obj.data.materials:
        obj.data.materials.append(mat)

    # === Step 6: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' with pure curved topology at {location}"
