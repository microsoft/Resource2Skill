def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralPanelCut",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.3, 0.35, 0.4),
    **kwargs,
) -> str:
    """
    Creates a perfectly curved, non-destructive panel cut on a cylinder using boolean intersections.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created object hierarchy.
        location: (x, y, z) position of the assembly.
        scale: Uniform scale of the entire assembly.
        material_color: (R, G, B) color for the metallic hull.
        
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    # Get target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # 1. Create Parent Empty
    parent_empty = bpy.data.objects.new(object_name, None)
    scene.collection.objects.link(parent_empty)
    parent_empty.location = Vector(location)
    parent_empty.scale = (scale, scale, scale)

    # 2. Build Base Cylinder Mesh (64 segments for smooth curvature)
    base_mesh = bpy.data.meshes.new(f"{object_name}_Base_Mesh")
    bm_base = bmesh.new()
    bmesh.ops.create_cone(
        bm_base, cap_ends=True, cap_tris=False, 
        segments=64, radius1=1.0, radius2=1.0, depth=2.0
    )
    bm_base.to_mesh(base_mesh)
    bm_base.free()

    # Apply smooth shading configuration
    for poly in base_mesh.polygons:
        poly.use_smooth = True
    if hasattr(base_mesh, "use_auto_smooth"):
        base_mesh.use_auto_smooth = True
        base_mesh.auto_smooth_angle = 1.047 # 60 degrees

    # 3. Create the Main Hull Object and Panel Object
    base_obj = bpy.data.objects.new(f"{object_name}_Hull", base_mesh)
    scene.collection.objects.link(base_obj)
    base_obj.parent = parent_empty

    # The panel piece uses a direct copy of the base mesh to guarantee identical starting curvature
    panel_mesh = base_mesh.copy()
    panel_mesh.name = f"{object_name}_Panel_Mesh"
    panel_obj = bpy.data.objects.new(f"{object_name}_Panel", panel_mesh)
    scene.collection.objects.link(panel_obj)
    panel_obj.parent = parent_empty

    # 4. Build the Cutter Mesh (A T-shaped composite block)
    cutter_mesh = bpy.data.meshes.new(f"{object_name}_Cutter_Mesh")
    bm_cutter = bmesh.new()
    
    # First intersecting block
    ret1 = bmesh.ops.create_cube(bm_cutter, size=1.0)
    for v in ret1['verts']:
        v.co.x *= 0.8   # Width
        v.co.y *= 0.6   # Depth
        v.co.z *= 0.8   # Height
        v.co.y -= 0.8   # Push forward to intersect outer cylinder wall
        v.co.z += 0.2   # Offset vertically
        
    # Second intersecting block (creates a more complex T-shaped cut)
    ret2 = bmesh.ops.create_cube(bm_cutter, size=1.0)
    for v in ret2['verts']:
        v.co.x *= 0.5   
        v.co.y *= 0.6   
        v.co.z *= 0.4   
        v.co.y -= 0.8   
        v.co.z += 0.8   
        
    bm_cutter.to_mesh(cutter_mesh)
    bm_cutter.free()
    
    cutter_obj = bpy.data.objects.new(f"{object_name}_Cutter", cutter_mesh)
    scene.collection.objects.link(cutter_obj)
    cutter_obj.parent = parent_empty
    
    # Hide the cutter from normal view
    cutter_obj.display_type = 'WIRE'
    cutter_obj.hide_render = True
    cutter_obj.hide_viewport = True

    # 5. Apply Non-Destructive Modifiers
    # Cut a hole in the Main Hull
    mod_diff = base_obj.modifiers.new(name="Cutout", type='BOOLEAN')
    mod_diff.operation = 'DIFFERENCE'
    mod_diff.object = cutter_obj
    mod_diff.solver = 'EXACT'

    # Extract the matching panel piece from the Duplicate Hull
    mod_int = panel_obj.modifiers.new(name="PanelPiece", type='BOOLEAN')
    mod_int.operation = 'INTERSECT'
    mod_int.object = cutter_obj
    mod_int.solver = 'EXACT'

    # Add Bevel to the base to create the outer edge of the panel gap
    bev_base = base_obj.modifiers.new(name="PanelGap", type='BEVEL')
    bev_base.segments = 3
    bev_base.width = 0.015
    bev_base.limit_method = 'ANGLE'
    bev_base.angle_limit = 0.523 # 30 degrees
    bev_base.harden_normals = True

    # Add Bevel to the panel piece to create the inner edge of the panel gap
    bev_panel = panel_obj.modifiers.new(name="PanelGap", type='BEVEL')
    bev_panel.segments = 3
    bev_panel.width = 0.015
    bev_panel.limit_method = 'ANGLE'
    bev_panel.angle_limit = 0.523
    bev_panel.harden_normals = True

    # 6. Create Material
    mat = bpy.data.materials.new(name=f"{object_name}_Metal")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = 0.85
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = 0.35

    base_obj.data.materials.append(mat)
    panel_obj.data.materials.append(mat)

    return f"Created '{object_name}' assembly at {location} utilizing 3 objects (Base, Panel, Cutter)."
