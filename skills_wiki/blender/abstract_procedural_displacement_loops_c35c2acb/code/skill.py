def create_abstract_waves(
    scene_name: str = "Scene",
    object_name: str = "AbstractWaves",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.1, 0.5),
    **kwargs,
) -> str:
    """
    Create Procedural Abstract Displacement Loops in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the generated object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color and subsurface color in 0-1 range.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Construct Geometry Nodes Tree ===
    tree = bpy.data.node_groups.new(name=f"{object_name}_GeoNodes", type="GeometryNodeTree")
    
    # Handle Blender 4.0+ vs older versions for socket creation
    if hasattr(tree, "interface"):
        tree.interface.new_socket(name="Geometry", in_out='OUT', socket_type='NodeSocketGeometry')
    else:
        tree.outputs.new('NodeSocketGeometry', "Geometry")

    nodes = tree.nodes
    links = tree.links

    # Base Line (Spawn points)
    mesh_line = nodes.new("GeometryNodeMeshLine")
    mesh_line.inputs['Count'].default_value = 30
    mesh_line.inputs['Offset'].default_value = (0.0, 0.4, 0.0)

    # Center the grid of lines
    trans = nodes.new("GeometryNodeTransform")
    trans.inputs['Translation'].default_value = (0.0, -6.0, 0.0)

    # Instanced Curve
    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.inputs['Start'].default_value = (-10.0, 0.0, 0.0)
    curve_line.inputs['End'].default_value = (10.0, 0.0, 0.0)

    resample = nodes.new("GeometryNodeResampleCurve")
    resample.inputs['Count'].default_value = 200

    # Instancing & Meshing
    inst = nodes.new("GeometryNodeInstanceOnPoints")
    realize = nodes.new("GeometryNodeRealizeInstances")
    c2m = nodes.new("GeometryNodeCurveToMesh")

    # Profile Curve (Ribbon width)
    # Y-axis orientation so the ribbon lays flat on the XY plane
    prof = nodes.new("GeometryNodeCurvePrimitiveLine")
    prof.inputs['Start'].default_value = (0.0, -0.15, 0.0)
    prof.inputs['End'].default_value = (0.0, 0.15, 0.0)

    # Displacement logic
    set_pos = nodes.new("GeometryNodeSetPosition")
    pos = nodes.new("GeometryNodeInputPosition")
    
    div = nodes.new("ShaderNodeVectorMath")
    div.operation = 'DIVIDE'
    div.inputs[1].default_value = (4.0, 4.0, 1.0) # Stretches noise coordinates

    noise = nodes.new("ShaderNodeTexNoise")
    noise.noise_dimensions = '4D'
    noise.inputs['Scale'].default_value = 0.8
    # Drive 4D noise W parameter with frame for looping animation
    noise.inputs['W'].driver_add("default_value").driver.expression = "frame / 50"

    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = 'EASE'
    
    mult = nodes.new("ShaderNodeMath")
    mult.operation = 'MULTIPLY'
    mult.inputs[1].default_value = 3.0 # Displacement height

    comb = nodes.new("ShaderNodeCombineXYZ")

    set_mat = nodes.new("GeometryNodeSetMaterial")
    smooth = nodes.new("GeometryNodeSetShadeSmooth")
    group_out = nodes.new("NodeGroupOutput")

    # Wire it all together
    links.new(mesh_line.outputs[0], trans.inputs['Geometry'])
    links.new(trans.outputs[0], inst.inputs['Points'])
    
    links.new(curve_line.outputs[0], resample.inputs[0])
    links.new(resample.outputs[0], inst.inputs['Instance'])

    links.new(inst.outputs[0], realize.inputs[0])
    links.new(realize.outputs[0], c2m.inputs['Curve'])
    links.new(prof.outputs[0], c2m.inputs['Profile Curve'])
    links.new(c2m.outputs[0], set_pos.inputs['Geometry'])

    links.new(pos.outputs[0], div.inputs[0])
    links.new(div.outputs[0], noise.inputs['Vector'])
    links.new(noise.outputs.get('Fac') or noise.outputs[1], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], mult.inputs[0])
    links.new(mult.outputs[0], comb.inputs['Z'])
    links.new(comb.outputs[0], set_pos.inputs['Offset'])

    links.new(set_pos.outputs[0], set_mat.inputs['Geometry'])
    links.new(set_mat.outputs[0], smooth.inputs['Geometry'])
    links.new(smooth.outputs[0], group_out.inputs[0])

    # === Step 2: Build Base Object & Apply Modifiers ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    mod_geo = obj.modifiers.new("GeometryNodes", 'NODES')
    mod_geo.node_group = tree

    mod_sol = obj.modifiers.new("Solidify", 'SOLIDIFY')
    mod_sol.thickness = 0.08
    mod_sol.offset = 0.0

    mod_bev = obj.modifiers.new("Bevel", 'BEVEL')
    mod_bev.width = 0.01
    mod_bev.segments = 3

    mod_sub = obj.modifiers.new("Subdivision", 'SUBSURF')
    mod_sub.levels = 1
    mod_sub.render_levels = 2

    # === Step 3: Subsurface Scattering Material ===
    mat = bpy.data.materials.new(f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")

    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.25
        
        # Cross-version compatibility for Subsurface Scattering
        if "Subsurface Weight" in bsdf.inputs: # Blender 4.0+
            bsdf.inputs["Subsurface Weight"].default_value = 1.0
            bsdf.inputs["Subsurface Scale"].default_value = 0.5
            bsdf.inputs["Subsurface Radius"].default_value = (1.0, 0.2, 0.1)
        elif "Subsurface" in bsdf.inputs: # Pre-4.0
            bsdf.inputs["Subsurface"].default_value = 1.0
            bsdf.inputs["Subsurface Color"].default_value = (*material_color, 1.0)
            
    set_mat.inputs['Material'].default_value = mat

    # === Step 4: Scene Context & Lighting ===
    # Area Light
    light_data = bpy.data.lights.new(name=f"{object_name}_Light", type='AREA')
    light_data.energy = 8000 * (scale ** 2)
    light_data.size = 15.0 * scale
    light_obj = bpy.data.objects.new(f"{object_name}_Light", light_data)
    scene.collection.objects.link(light_obj)
    light_obj.location = Vector(location) + Vector((0, 0, 8 * scale))
    
    # Bounce Plane
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=20.0)
    bounce_mesh = bpy.data.meshes.new(f"{object_name}_BouncePlane")
    bm.to_mesh(bounce_mesh)
    bm.free()
    
    bounce_obj = bpy.data.objects.new(f"{object_name}_BouncePlane", bounce_mesh)
    scene.collection.objects.link(bounce_obj)
    bounce_obj.location = Vector(location) + Vector((0, 0, -1.0 * scale))
    
    bounce_mat = bpy.data.materials.new(f"{object_name}_BounceMat")
    bounce_mat.use_nodes = True
    b_bsdf = bounce_mat.node_tree.nodes.get("Principled BSDF")
    if b_bsdf:
        b_bsdf.inputs['Base Color'].default_value = (0.05, 0.03, 0.02, 1.0)
        b_bsdf.inputs['Roughness'].default_value = 0.8
    bounce_obj.data.materials.append(bounce_mat)

    # Position & Scale Master Object
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    bounce_obj.scale = (scale, scale, scale)

    return f"Created procedural AbstractWaves '{object_name}' at {location} with lighting context. Press spacebar to play animation."
