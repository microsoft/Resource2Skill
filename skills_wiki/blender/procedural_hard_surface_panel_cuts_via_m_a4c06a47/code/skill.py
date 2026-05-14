def create_object(
    scene_name: str = "Scene",
    object_name: str = "SciFi_Panel_Surface",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.05, 0.4, 0.6),
    **kwargs,
) -> str:
    """
    Create a procedurally paneled hard-surface mesh using the Edge Split/Solidify/Bevel technique.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the metallic panel material.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    # Retrieve scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry and Topology ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    # Create a dense grid to allow for high-res panel cuts and smooth curving
    bmesh.ops.create_grid(bm, x_segments=40, y_segments=40, size=1.0) 

    # --- Define Panel Regions ---
    # We define sets of faces to act as distinct physical panels.
    panels = set()
    for f in bm.faces:
        c = f.calc_center_median()
        
        # Panel A: Large panel on the right with a cutout
        if 0.1 < c.x < 0.9 and -0.8 < c.y < 0.8:
            # Create a hollow cutout inside Panel A
            if 0.3 < c.x < 0.7 and 0.2 < c.y < 0.6:
                continue 
            panels.add(f)
            
        # Panel B: L-Shape panel on the left
        elif -0.9 < c.x < -0.1 and -0.8 < c.y < 0.1:
            if c.x > -0.5 and c.y > -0.4:
                continue
            panels.add(f)
            
        # Panel C: Circular hatch/panel approximation
        elif math.hypot(c.x - (-0.5), c.y - 0.6) < 0.25:
            panels.add(f)
            
        # Panel D: Small floating detail inside the Panel A cutout
        elif math.hypot(c.x - 0.5, c.y - 0.4) < 0.1:
            panels.add(f)

    # --- Mark Boundary Edges as Sharp ---
    # An edge is a boundary if it sits exactly between a panel face and a non-panel face.
    for e in bm.edges:
        e.smooth = True # Default all edges to smooth
        
        # Prevent splitting the outer boundary of the entire grid
        if len(e.link_faces) == 1:
            continue 
            
        linked_in_panels = sum(1 for f in e.link_faces if f in panels)
        if linked_in_panels == 1:
            e.smooth = False # Mark as Sharp for the Edge Split modifier

    # --- Curve the Surface ---
    # Wrap the flat grid into a cylindrical arc
    for v in bm.verts:
        radius = 1.5
        # v.co.x ranges from -1 to 1 based on grid size
        angle = v.co.x / radius
        v.co.x = math.sin(angle) * radius
        v.co.z = math.cos(angle) * radius - radius

    # Recalculate normals after curving
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()

    # Enable smooth shading so Edge Split works correctly
    for poly in mesh.polygons:
        poly.use_smooth = True

    # === Step 2: Apply the Magic Modifier Stack ===
    # 1. Split the mesh at the sharp boundary edges we defined
    mod_split = obj.modifiers.new("EdgeSplit", 'EDGE_SPLIT')
    mod_split.use_edge_angle = False
    mod_split.use_edge_sharp = True

    # 2. Add thickness to the separated pieces
    mod_solidify = obj.modifiers.new("Solidify", 'SOLIDIFY')
    mod_solidify.thickness = 0.02
    mod_solidify.offset = -1.0 # Grow inward to keep outer silhouette exact

    # 3. Bevel the newly created 90-degree solid corners to create the V-groove
    mod_bevel = obj.modifiers.new("Bevel", 'BEVEL')
    mod_bevel.width = 0.008
    mod_bevel.segments = 3
    mod_bevel.limit_method = 'ANGLE'
    mod_bevel.angle_limit = math.radians(30)
    mod_bevel.use_clamp_overlap = False


    # === Step 3: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Metal_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Metallic"].default_value = 0.8
        bsdf.inputs["Roughness"].default_value = 0.25
    obj.data.materials.append(mat)


    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))

    return f"Created '{object_name}' with procedural panel cuts at {location}"
