def create_object(
    scene_name: str = "Scene",
    object_name: str = "SciFiBracket",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.22, 0.25),
    **kwargs,
) -> str:
    """
    Create a Procedural Hard-Surface Mechanical Frame using a non-destructive boolean workflow.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the main frame object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color.
        
    Returns:
        Status string confirming creation.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # --- Ensure Cutters Collection Exists ---
    cutters_coll_name = "Boolean_Cutters"
    cutters_collection = bpy.data.collections.get(cutters_coll_name)
    if not cutters_collection:
        cutters_collection = bpy.data.collections.new(cutters_coll_name)
        scene.collection.children.link(cutters_collection)
        # Exclude collection from rendering
        bpy.context.view_layer.layer_collection.children[cutters_coll_name].exclude = True

    cutters_list = []

    def add_cutter(name, c_loc, c_scale, c_rot=(0,0,0), shape='CUBE', bevel_amt=0.0):
        """Helper to create and configure invisible proxy cutter objects."""
        if shape == 'CUBE':
            bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,0))
        elif shape == 'CYLINDER':
            bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=1.0, location=(0,0,0))
        
        c = bpy.context.active_object
        c.name = f"{object_name}_{name}"
        c.location = c_loc
        c.scale = c_scale
        c.rotation_euler = c_rot
        c.display_type = 'WIRE'
        c.hide_render = True
        
        if bevel_amt > 0:
            bm = c.modifiers.new(name="CutterBevel", type='BEVEL')
            bm.width = bevel_amt
            bm.segments = 4
            bm.limit_method = 'ANGLE'
            
        # Move object to cutters collection
        for coll in c.users_collection:
            coll.objects.unlink(c)
        cutters_collection.objects.link(c)
        
        cutters_list.append(c)
        return c

    def apply_boolean(target, cutter, operation='DIFFERENCE'):
        """Helper to add boolean modifier to target."""
        mod = target.modifiers.new(name=f"Bool_{cutter.name}", type='BOOLEAN')
        mod.object = cutter
        mod.operation = operation
        mod.solver = 'EXACT'

    # === Step 1: Base Geometry ===
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,0))
    base = bpy.context.active_object
    base.name = object_name
    
    # Scale to bracket proportions (4 wide, 0.4 thick, 2 tall)
    base.scale = (4.0, 0.4, 2.0)
    
    # Apply scale so bevels and booleans evaluate correctly
    bpy.context.view_layer.objects.active = base
    base.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    base.select_set(False)

    # === Step 2: Create and Apply Cutters ===
    
    # Outer Chamfers
    c_tl = add_cutter("ChamferTL", (-2.0, 0.0, 1.0), (1.0, 1.0, 1.0), (0.0, math.radians(45), 0.0))
    apply_boolean(base, c_tl, 'DIFFERENCE')
    
    c_br = add_cutter("ChamferBR", (2.0, 0.0, -1.0), (1.0, 1.0, 1.0), (0.0, math.radians(45), 0.0))
    apply_boolean(base, c_br, 'DIFFERENCE')

    # Top Slant profile
    c_top = add_cutter("TopSlant", (0.0, 0.0, 1.2), (4.5, 1.0, 1.0), (0.0, math.radians(-5), 0.0))
    apply_boolean(base, c_top, 'DIFFERENCE')

    # Inner Truss Cutouts (hollow out the frame with rounded corners)
    c_winL = add_cutter("WindowL", (-0.8, 0.0, 0.0), (1.2, 1.0, 1.0), (0.0, math.radians(15), 0.0), bevel_amt=0.1)
    apply_boolean(base, c_winL, 'DIFFERENCE')

    c_winR = add_cutter("WindowR", (1.0, 0.0, -0.2), (1.2, 1.0, 0.8), (0.0, math.radians(-10), 0.0), bevel_amt=0.1)
    apply_boolean(base, c_winR, 'DIFFERENCE')
    
    # Mechanical Hinge Joint (Union)
    # Cylinder default faces Z. Rotated 90 on X makes it face global Y.
    c_joint = add_cutter("JointEnd", (-2.0, 0.0, 0.0), (1.2, 1.2, 0.6), (math.radians(90), 0.0, 0.0), shape='CYLINDER')
    apply_boolean(base, c_joint, 'UNION')
    
    # Hinge Hole
    c_hole = add_cutter("JointHole", (-2.0, 0.0, 0.0), (0.6, 0.6, 1.5), (math.radians(90), 0.0, 0.0), shape='CYLINDER')
    apply_boolean(base, c_hole, 'DIFFERENCE')

    # Edge Slot Details
    c_slot1 = add_cutter("SlotTop", (1.5, 0.2, 0.6), (0.4, 0.2, 0.05))
    apply_boolean(base, c_slot1, 'DIFFERENCE')
    
    c_slot2 = add_cutter("SlotBot", (1.5, -0.2, 0.6), (0.4, 0.2, 0.05))
    apply_boolean(base, c_slot2, 'DIFFERENCE')

    # Arrayed Bolt Holes
    c_bolt = add_cutter("BoltHole", (1.5, 0.0, -0.6), (0.1, 0.1, 1.5), (math.radians(90), 0.0, 0.0), shape='CYLINDER')
    arr = c_bolt.modifiers.new(name="Array", type='ARRAY')
    arr.use_relative_offset = False
    arr.use_constant_offset = True
    arr.constant_offset_displace = (-0.35, 0.0, 0.0)
    arr.count = 3
    apply_boolean(base, c_bolt, 'DIFFERENCE')

    # === Step 3: Polish Modifiers (Bevel & Shading) ===
    # Global Bevel for hard surface highlights
    bev = base.modifiers.new(name="GlobalBevel", type='BEVEL')
    bev.width = 0.015
    bev.segments = 3
    bev.limit_method = 'ANGLE'
    bev.angle_limit = math.radians(30)
    try: bev.use_hard_normals = True
    except AttributeError: pass
    
    # Weighted Normal for n-gon shading correction
    wn = base.modifiers.new(name="WeightedNormal", type='WEIGHTED_NORMAL')
    wn.keep_sharp = True

    for poly in base.data.polygons:
        poly.use_smooth = True
        
    try:
        base.data.use_auto_smooth = True
        base.data.auto_smooth_angle = math.radians(30)
    except AttributeError:
        pass # Blender 4.1+ behavior

    # === Step 4: Procedural Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Metallic"].default_value = 0.85
        bsdf.inputs["Roughness"].default_value = 0.35
        
        bump = nodes.new("ShaderNodeBump")
        bump.inputs["Distance"].default_value = 0.003
        bump.inputs["Strength"].default_value = 0.6
        
        noise = nodes.new("ShaderNodeTexNoise")
        noise.inputs["Scale"].default_value = 200.0
        noise.inputs["Detail"].default_value = 4.0
        
        links.new(noise.outputs["Fac"], bump.inputs["Height"])
        links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
        
    base.data.materials.append(mat)

    # === Step 5: Positioning & Hierarchy ===
    # Parent cutters to the base so moving the base moves the entire boolean rig
    for c in cutters_list:
        c.parent = base
        # Matrix inverse keeps local offsets intact
        c.matrix_parent_inverse = base.matrix_world.inverted()

    # Finally apply requested transformations
    base.location = Vector(location)
    base.scale = (scale, scale, scale)

    return f"Created '{object_name}' kitbash frame at {location} with {len(cutters_list)} live boolean cutters."
