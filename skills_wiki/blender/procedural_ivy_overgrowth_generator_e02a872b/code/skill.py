def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralIvy",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    leaf_color: tuple = (0.1, 0.5, 0.1),
    **kwargs,
) -> str:
    """
    Create a Procedural Ivy Generator applied to a base mesh.
    
    Args:
        scene_name: Target scene.
        object_name: Name of the generated setup.
        location: (x, y, z) placement.
        scale: Base size scale.
        leaf_color: Base color for the foliage.
        
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 1. Materials ---
    def make_mat(name, color):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*color, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.8
        return mat

    mat_soil = make_mat(f"{object_name}_Soil", (0.05, 0.03, 0.02))
    mat_vine = make_mat(f"{object_name}_Vine", (0.2, 0.1, 0.05))
    mat_leaf = make_mat(f"{object_name}_Leaf", leaf_color)
    mat_flower = make_mat(f"{object_name}_Flower", (0.9, 0.8, 0.85))

    # --- 2. Base Mesh (Trellis/Soil) ---
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=6, radius=1.0 * scale, depth=1.0 * scale, end_fill_type='NGON', location=location
    )
    base_obj = bpy.context.active_object
    base_obj.name = object_name
    base_obj.data.materials.append(mat_soil)

    # --- 3. Custom Instanced Assets (Leaf & Flower) ---
    # Leaf Mesh
    leaf_mesh = bpy.data.meshes.new(f"{object_name}_LeafMesh")
    leaf_obj = bpy.data.objects.new(f"{object_name}_LeafObj", leaf_mesh)
    scene.collection.objects.link(leaf_obj)
    leaf_obj.hide_viewport = True
    leaf_obj.hide_render = True

    bm = bmesh.new()
    v0 = bm.verts.new((0, 0, 0))          # Stem root (pivot)
    v1 = bm.verts.new((0, 0.1, 0.0))      # Base
    v2 = bm.verts.new((0.15, 0.3, 0.05))  # Right lobe
    v3 = bm.verts.new((-0.15, 0.3, 0.05)) # Left lobe
    v4 = bm.verts.new((0, 0.6, 0.0))      # Tip
    bm.faces.new((v0, v1, v2))
    bm.faces.new((v0, v3, v1))
    bm.faces.new((v1, v3, v4, v2))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(leaf_mesh)
    bm.free()

    # Flower Mesh (5-petal bell shape)
    flower_mesh = bpy.data.meshes.new(f"{object_name}_FlowerMesh")
    flower_obj = bpy.data.objects.new(f"{object_name}_FlowerObj", flower_mesh)
    scene.collection.objects.link(flower_obj)
    flower_obj.hide_viewport = True
    flower_obj.hide_render = True

    bm_f = bmesh.new()
    center = bm_f.verts.new((0, 0, -0.05))
    petals = [bm_f.verts.new((math.cos(i*(2*math.pi/5))*0.15, math.sin(i*(2*math.pi/5))*0.15, 0.1)) for i in range(5)]
    for i in range(5):
        bm_f.faces.new((center, petals[i], petals[(i+1)%5]))
    bmesh.ops.recalc_face_normals(bm_f, faces=bm_f.faces)
    bm_f.to_mesh(flower_mesh)
    bm_f.free()

    # --- 4. Geometry Nodes System ---
    gn_tree = bpy.data.node_groups.new(f"{object_name}_NodeTree", 'GeometryNodeTree')
    
    # Cross-compatible IO generation
    if hasattr(gn_tree, "interface"):
        gn_tree.interface.new_socket("Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        gn_tree.interface.new_socket("Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        gn_tree.inputs.new('NodeSocketGeometry', "Geometry")
        gn_tree.outputs.new('NodeSocketGeometry', "Geometry")

    nodes = gn_tree.nodes
    links = gn_tree.links
    group_in = nodes.new('NodeGroupInput')
    group_out = nodes.new('NodeGroupOutput')

    # A: Base Vines (Edges)
    mesh_curve = nodes.new('GeometryNodeMeshToCurve')
    links.new(group_in.outputs[0], mesh_curve.inputs[0])

    # B: Scattered Growth Vines
    dist_pts = nodes.new('GeometryNodeDistributePointsOnFaces')
    dist_pts.inputs['Density'].default_value = 25.0
    links.new(group_in.outputs[0], dist_pts.inputs[0])

    line = nodes.new('GeometryNodeCurvePrimitiveLine')
    line.inputs['End'].default_value = (0, 0, 1.5)

    inst_lines = nodes.new('GeometryNodeInstanceOnPoints')
    links.new(dist_pts.outputs['Points'], inst_lines.inputs['Points'])
    links.new(dist_pts.outputs['Rotation'], inst_lines.inputs['Rotation']) # Grow along normal
    links.new(line.outputs['Curve'], inst_lines.inputs['Instance'])

    realize = nodes.new('GeometryNodeRealizeInstances')
    links.new(inst_lines.outputs['Instances'], realize.inputs[0])

    # C: Combine & Tangle
    join_curves = nodes.new('GeometryNodeJoinGeometry')
    links.new(mesh_curve.outputs[0], join_curves.inputs[0])
    links.new(realize.outputs[0], join_curves.inputs[0])

    resample = nodes.new('GeometryNodeResampleCurve')
    resample.mode = 'LENGTH'
    resample.inputs['Length'].default_value = 0.1
    links.new(join_curves.outputs[0], resample.inputs['Curve'])

    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 2.5

    sub = nodes.new('ShaderNodeVectorMath')
    sub.operation = 'SUBTRACT'
    sub.inputs[1].default_value = (0.5, 0.5, 0.5)
    links.new(noise.outputs['Color'], sub.inputs[0])

    mult = nodes.new('ShaderNodeVectorMath')
    mult.operation = 'MULTIPLY'
    mult.inputs[1].default_value = (0.5, 0.5, 0.5) # Distortion amplitude
    links.new(sub.outputs['Vector'], mult.inputs[0])

    set_pos = nodes.new('GeometryNodeSetPosition')
    links.new(resample.outputs['Curve'], set_pos.inputs['Geometry'])
    links.new(mult.outputs['Vector'], set_pos.inputs['Offset'])

    # Solidify Vines
    curve_to_mesh = nodes.new('GeometryNodeCurveToMesh')
    circle = nodes.new('GeometryNodeCurvePrimitiveCircle')
    circle.inputs['Radius'].default_value = 0.012 * scale
    links.new(set_pos.outputs['Geometry'], curve_to_mesh.inputs['Curve'])
    links.new(circle.outputs['Curve'], curve_to_mesh.inputs['Profile Curve'])
    
    set_mat_vine = nodes.new('GeometryNodeSetMaterial')
    set_mat_vine.inputs['Material'].default_value = mat_vine
    links.new(curve_to_mesh.outputs['Mesh'], set_mat_vine.inputs['Geometry'])

    # D: Scatter Leaves
    pts_leaf = nodes.new('GeometryNodeCurveToPoints')
    pts_leaf.mode = 'LENGTH'
    pts_leaf.inputs['Length'].default_value = 0.15 * scale
    links.new(set_pos.outputs['Geometry'], pts_leaf.inputs['Curve'])

    leaf_info = nodes.new('GeometryNodeObjectInfo')
    leaf_info.inputs['Object'].default_value = leaf_obj

    inst_leaf = nodes.new('GeometryNodeInstanceOnPoints')
    links.new(pts_leaf.outputs['Points'], inst_leaf.inputs['Points'])
    links.new(leaf_info.outputs['Geometry'], inst_leaf.inputs['Instance'])

    # Leaf rotation (tilt outward + random spin)
    tilt = nodes.new('FunctionNodeRotateEuler')
    tilt.type = 'EULER'
    tilt.space = 'LOCAL'
    tilt.inputs['Rotation'].default_value = (math.pi/3, 0, 0)
    links.new(pts_leaf.outputs['Rotation'], tilt.inputs['Rotation'])

    rand_rot = nodes.new('FunctionNodeRandomValue')
    rand_rot.data_type = 'FLOAT_VECTOR'
    rand_rot.inputs[4].default_value = (0, 0, -math.pi/2) # Min
    rand_rot.inputs[5].default_value = (0, 0, math.pi/2)  # Max

    add_rot = nodes.new('ShaderNodeVectorMath')
    add_rot.operation = 'ADD'
    links.new(tilt.outputs['Rotation'], add_rot.inputs[0])
    links.new(rand_rot.outputs[0], add_rot.inputs[1])
    links.new(add_rot.outputs['Vector'], inst_leaf.inputs['Rotation'])

    # Leaf scale
    rand_scale_leaf = nodes.new('FunctionNodeRandomValue')
    rand_scale_leaf.data_type = 'FLOAT'
    rand_scale_leaf.inputs[0].default_value = 0.6 * scale
    rand_scale_leaf.inputs[1].default_value = 1.3 * scale
    links.new(rand_scale_leaf.outputs[0], inst_leaf.inputs['Scale'])

    set_mat_leaf = nodes.new('GeometryNodeSetMaterial')
    set_mat_leaf.inputs['Material'].default_value = mat_leaf
    links.new(inst_leaf.outputs['Instances'], set_mat_leaf.inputs['Geometry'])

    # E: Scatter Flowers
    pts_flower = nodes.new('GeometryNodeCurveToPoints')
    pts_flower.mode = 'LENGTH'
    pts_flower.inputs['Length'].default_value = 1.2 * scale # Sparse spacing
    links.new(set_pos.outputs['Geometry'], pts_flower.inputs['Curve'])

    flower_info = nodes.new('GeometryNodeObjectInfo')
    flower_info.inputs['Object'].default_value = flower_obj

    inst_flower = nodes.new('GeometryNodeInstanceOnPoints')
    links.new(pts_flower.outputs['Points'], inst_flower.inputs['Points'])
    links.new(flower_info.outputs['Geometry'], inst_flower.inputs['Instance'])

    rand_scale_flower = nodes.new('FunctionNodeRandomValue')
    rand_scale_flower.data_type = 'FLOAT'
    rand_scale_flower.inputs[0].default_value = 0.5 * scale
    rand_scale_flower.inputs[1].default_value = 1.1 * scale
    links.new(rand_scale_flower.outputs[0], inst_flower.inputs['Scale'])

    set_mat_flower = nodes.new('GeometryNodeSetMaterial')
    set_mat_flower.inputs['Material'].default_value = mat_flower
    links.new(inst_flower.outputs['Instances'], set_mat_flower.inputs['Geometry'])

    # F: Final Join
    join_final = nodes.new('GeometryNodeJoinGeometry')
    links.new(group_in.outputs[0], join_final.inputs[0]) # Base ground mesh
    links.new(set_mat_vine.outputs['Geometry'], join_final.inputs[0])
    links.new(set_mat_leaf.outputs['Geometry'], join_final.inputs[0])
    links.new(set_mat_flower.outputs['Geometry'], join_final.inputs[0])

    links.new(join_final.outputs[0], group_out.inputs[0])

    # --- 5. Apply Modifier ---
    mod = base_obj.modifiers.new(name="IvySystem", type='NODES')
    mod.node_group = gn_tree

    return f"Created procedural plant system '{object_name}' at {location} with Geometry Nodes"
