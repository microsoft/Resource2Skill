def create_object(
    scene_name: str = "Scene",
    object_name: str = "Parametric_Bracket",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.7, 0.75),
    **kwargs,
) -> str:
    """
    Create a Parametric Mechanical L-Bracket with mounting holes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created bracket object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default 100mm scale).
        material_color: (R, G, B) base metal color.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Real-world dimensions (scaled)
    length = 0.1 * scale          # 100mm base plate
    width = 0.012 * scale         # 12mm width
    thickness = 0.003 * scale     # 3mm thickness
    leg_height = 0.01 * scale     # 10mm leg height
    hole_radius = 0.0028 * scale  # 5.6mm diameter holes
    
    # Helper to create localized bounding boxes via BMesh
    def create_box(name, dim, loc):
        mesh = bpy.data.meshes.new(name + "_Mesh")
        obj = bpy.data.objects.new(name, mesh)
        scene.collection.objects.link(obj)
        
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=dim, verts=bm.verts)
        bmesh.ops.translate(bm, vec=loc, verts=bm.verts)
        bm.to_mesh(mesh)
        bm.free()
        return obj

    # === Step 1: Base Plate and Leg (Additive CSG) ===
    # Base plate centered on X, sitting on the ground plane (Z=0)
    base_obj = create_box(object_name, Vector((length, width, thickness)), Vector((0, 0, thickness/2)))
    
    # L-Leg placed exactly at the positive X edge of the base plate
    leg_x_pos = (length / 2) + (thickness / 2)
    leg_z_pos = thickness + (leg_height / 2)
    leg_obj = create_box("Leg_Temp", Vector((thickness, width, leg_height)), Vector((leg_x_pos, 0, leg_z_pos)))
    
    # Join Leg to Base
    bool_union = base_obj.modifiers.new(name="UnionLeg", type='BOOLEAN')
    bool_union.operation = 'UNION'
    bool_union.object = leg_obj
    
    bpy.context.view_layer.objects.active = base_obj
    base_obj.select_set(True)
    bpy.ops.object.modifier_apply(modifier=bool_union.name)
    bpy.data.objects.remove(leg_obj, do_unlink=True)
    
    # === Step 2: Mounting Holes (Subtractive CSG) ===
    cutter_mesh = bpy.data.meshes.new("Cutters_Mesh")
    cutter_obj = bpy.data.objects.new("Cutters_Temp", cutter_mesh)
    scene.collection.objects.link(cutter_obj)
    
    bm_cutter = bmesh.new()
    hole_positions = [-0.045 * scale, 0, 0.045 * scale] # Spaced exactly as in tutorial
    
    for hx in hole_positions:
        geom = bmesh.ops.create_cone(
            bm_cutter, 
            cap_ends=True, 
            cap_tris=False, 
            segments=32, 
            radius1=hole_radius, 
            radius2=hole_radius, 
            depth=thickness * 4 # Exaggerated depth ensures clean boolean cut
        )
        verts = [v for v in geom['verts']]
        bmesh.ops.translate(bm_cutter, vec=Vector((hx, 0, thickness/2)), verts=verts)
        
    bm_cutter.to_mesh(cutter_mesh)
    bm_cutter.free()
    
    # Difference Boolean for holes
    bool_diff = base_obj.modifiers.new(name="Holes", type='BOOLEAN')
    bool_diff.operation = 'DIFFERENCE'
    bool_diff.object = cutter_obj
    
    bpy.ops.object.modifier_apply(modifier=bool_diff.name)
    bpy.data.objects.remove(cutter_obj, do_unlink=True)
    
    # === Step 3: Polish & Edge Realism ===
    bevel = base_obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.0002 * scale
    bevel.segments = 3
    bevel.limit_method = 'ANGLE'
        
    # === Step 4: Material Definition ===
    mat = bpy.data.materials.new(name=object_name + "_Metal")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Metallic"].default_value = 0.85
        bsdf.inputs["Roughness"].default_value = 0.3
    base_obj.data.materials.append(mat)
    
    # === Step 5: Final Placement ===
    base_obj.location = Vector(location)
    base_obj.select_set(False)
    
    return f"Created Parametric Mechanical L-Bracket '{object_name}' at {location}."
