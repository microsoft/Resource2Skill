def create_scifi_surface_panel(
    scene_name: str = "Scene",
    object_name: str = "SciFi_Panel",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.3, 0.3, 0.32),
    **kwargs,
) -> str:
    """
    Create a procedural Sci-Fi panel using non-destructive modifiers.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color in 0-1 range.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Create Base Grid ===
    # 11 vertices = 10 face segments. Size=2 means from -1.0 to 1.0 in local space.
    bpy.ops.mesh.primitive_grid_add(
        verticesX=11, 
        verticesY=11, 
        size=2, 
        enter_editmode=False, 
        rotation=(0, 0, 0)
    )
    obj = bpy.context.active_object
    obj.name = object_name
    mesh = obj.data

    # === Step 2: Boundary Edge Creasing ===
    # Crease the outer boundaries so the subsurf modifier doesn't round the whole object
    bm = bmesh.new()
    bm.from_mesh(mesh)
    crease_layer = bm.edges.layers.crease.verify()
    for edge in bm.edges:
        if edge.is_boundary:
            edge[crease_layer] = 1.0
    bm.to_mesh(mesh)
    bm.free()

    # === Step 3: Procedural Edge Marking ===
    # Mark specific internal edges as sharp to define the panel cuts
    for edge in mesh.edges:
        v1 = mesh.vertices[edge.vertices[0]].co
        v2 = mesh.vertices[edge.vertices[1]].co
        
        # Determine if edge is purely horizontal or vertical
        is_horiz = abs(v1.y - v2.y) < 0.01
        is_vert = abs(v1.x - v2.x) < 0.01
        
        # Get midpoints for logical targeting
        mx = round((v1.x + v2.x) / 2.0, 3)
        my = round((v1.y + v2.y) / 2.0, 3)
        
        is_cut = False
        
        if is_horiz:
            # Main horizontal split across the middle
            if round(v1.y, 3) == 0.0:
                is_cut = True
            # Top-mid panel bottom boundary
            if round(v1.y, 3) == 0.4 and abs(mx) < 0.45:
                is_cut = True
            # Top-left circle panel boundaries
            if round(v1.y, 3) in [0.4, 0.8] and mx > -0.85 and mx < -0.35:
                is_cut = True
            # Bottom main panel top boundary
            if round(v1.y, 3) == -0.6 and abs(mx) < 0.65:
                is_cut = True
            # Small inner bottom panel
            if round(v1.y, 3) == -0.8 and abs(mx) < 0.25:
                is_cut = True
                
        if is_vert:
            # Top-mid panel side boundaries
            if round(v1.x, 3) in [-0.4, 0.4] and my > 0.0 and my < 0.45:
                is_cut = True
            # Top-left circle panel side boundaries
            if round(v1.x, 3) in [-0.8, -0.4] and my > 0.35 and my < 0.85:
                is_cut = True
            # Bottom main panel side boundaries
            if round(v1.x, 3) in [-0.6, 0.6] and my < -0.55:
                is_cut = True
            # Small inner bottom panel sides
            if round(v1.x, 3) in [-0.2, 0.2] and my < -0.75:
                is_cut = True
                
        if is_cut:
            edge.use_edge_sharp = True

    # Enable smooth shading on the base geometry
    for poly in mesh.polygons:
        poly.use_smooth = True

    # === Step 4: The Modifier Stack (Core Technique) ===
    
    # 1. Edge Split: Physically separates the geometry where we marked sharp edges
    mod_split = obj.modifiers.new(name="EdgeSplit", type='EDGE_SPLIT')
    mod_split.use_edge_angle = False
    mod_split.use_edge_sharp = True
    
    # 2. Subdivision: Rounds the separated panel corners (turns the 2x2 square into a circle)
    mod_subdiv1 = obj.modifiers.new(name="SubdivRounded", type='SUBSURF')
    mod_subdiv1.levels = 2
    mod_subdiv1.render_levels = 2
    
    # 3. Solidify: Extrudes the flat panels inward to create deep panel gaps
    mod_solid = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    mod_solid.thickness = 0.05
    mod_solid.offset = -1.0
    mod_solid.use_rim_only = False
    
    # 4. Bevel: Adds micro-bevels to the sharp extruded corners for realistic highlights
    mod_bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    mod_bevel.segments = 3
    mod_bevel.width = 0.01
    
    # 5. Final Subdivision: Smooths out the micro-bevels
    mod_subdiv2 = obj.modifiers.new(name="SubdivSmooth", type='SUBSURF')
    mod_subdiv2.levels = 1
    mod_subdiv2.render_levels = 1

    # === Step 5: Materials & Shading ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.7
        bsdf.inputs['Roughness'].default_value = 0.25
    obj.data.materials.append(mat)

    # === Step 6: Final Positioning ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' Sci-Fi Panel at {location}"
