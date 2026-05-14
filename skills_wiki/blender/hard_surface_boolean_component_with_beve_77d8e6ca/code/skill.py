def create_object(
    scene_name: str = "Scene",
    object_name: str = "SciFi_MuzzleBrake",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.2, 0.22),
    **kwargs,
) -> str:
    """
    Creates a procedural hard-surface component using Booleans and a Bevel Shader.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) color for the gunmetal material.
        **kwargs: Additional options.
        
    Returns:
        Status string confirming creation.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # The Bevel shader node is exclusive to Cycles raytracing
    scene.render.engine = 'CYCLES'

    # Create a Master Parent Empty
    parent = bpy.data.objects.new(object_name, None)
    scene.collection.objects.link(parent)
    parent.location = Vector(location)
    parent.scale = (scale, scale, scale)

    # === 1. Base Geometry ===
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=1, depth=6)
    base_obj = bpy.context.active_object
    base_obj.name = f"{object_name}_Base"
    base_obj.parent = parent
    # Rotate to lie along the X axis
    base_obj.rotation_euler = (0, math.radians(90), 0)
    
    bpy.ops.object.shade_smooth()

    # Edge Split ensures boolean intersections look sharp in viewport, 
    # setting up a perfect base for the Bevel node to blend.
    edge_split = base_obj.modifiers.new(name="EdgeSplit", type='EDGE_SPLIT')
    edge_split.split_angle = math.radians(40)

    # === 2. Hidden Collection for Cutters ===
    cutter_coll_name = "Hidden_Boolean_Cutters"
    cutter_coll = bpy.data.collections.get(cutter_coll_name)
    if not cutter_coll:
        cutter_coll = bpy.data.collections.new(cutter_coll_name)
        scene.collection.children.link(cutter_coll)
        cutter_coll.hide_viewport = True
        cutter_coll.hide_render = True

    # === 3. Cutter A: Side Exhaust Slots ===
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.35, depth=4)
    cutter_side = bpy.context.active_object
    cutter_side.name = f"{object_name}_Cutter_Side"
    
    # Move to the hidden collection
    bpy.context.collection.objects.unlink(cutter_side)
    cutter_coll.objects.link(cutter_side)
    
    cutter_side.parent = parent
    cutter_side.rotation_euler = (math.radians(90), 0, 0) # Align to Y axis
    cutter_side.location = (-1.8, 0, 0)
    cutter_side.scale = (1.5, 1.0, 1.0) # Stretch into an oval pill shape
    
    # Array modifier to repeat the slot
    arr_side = cutter_side.modifiers.new("Array", 'ARRAY')
    arr_side.count = 4
    arr_side.use_relative_offset = False
    arr_side.use_constant_offset = True
    arr_side.constant_offset_displace = (1.2, 0, 0)

    # Apply Boolean to Base
    bool_side = base_obj.modifiers.new("Bool_Side", 'BOOLEAN')
    bool_side.operation = 'DIFFERENCE'
    bool_side.object = cutter_side

    # === 4. Cutter B: Top Ventilation Holes ===
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.25, depth=4)
    cutter_top = bpy.context.active_object
    cutter_top.name = f"{object_name}_Cutter_Top"
    
    # Move to the hidden collection
    bpy.context.collection.objects.unlink(cutter_top)
    cutter_coll.objects.link(cutter_top)
    
    cutter_top.parent = parent
    cutter_top.location = (-1.5, 0, 0) # Aligned to Z by default
    
    # Array modifier to repeat the holes
    arr_top = cutter_top.modifiers.new("Array", 'ARRAY')
    arr_top.count = 3
    arr_top.use_relative_offset = False
    arr_top.use_constant_offset = True
    arr_top.constant_offset_displace = (1.5, 0, 0)

    # Apply Boolean to Base
    bool_top = base_obj.modifiers.new("Bool_Top", 'BOOLEAN')
    bool_top.operation = 'DIFFERENCE'
    bool_top.object = cutter_top

    # === 5. Material & Bevel Shader Setup ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Metallic"].default_value = 0.9
        bsdf.inputs["Roughness"].default_value = 0.25

        # The Bevel Node - creates the illusion of smooth geometry at render time
        bevel_node = nodes.new(type="ShaderNodeBevel")
        bevel_node.inputs["Radius"].default_value = 0.04
        bevel_node.samples = 6
        
        # Link Bevel normal to BSDF normal
        links.new(bevel_node.outputs["Normal"], bsdf.inputs["Normal"])

    base_obj.data.materials.append(mat)

    return f"Created hard-surface boolean component '{object_name}' with Bevel shader at {location}"
