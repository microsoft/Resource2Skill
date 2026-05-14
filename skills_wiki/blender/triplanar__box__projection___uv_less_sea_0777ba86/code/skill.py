def create_object(
    scene_name: str = "Scene",
    object_name: str = "DynamicRustedPart",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.15, 0.45, 0.5),
    **kwargs,
) -> str:
    """
    Create a mechanical part textured via UV-less Object coordinates, demonstrating Box Projection.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the painted areas.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (Stepped Cylinder) ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    bm = bmesh.new()
    # Base thin cylinder
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=32, radius1=1.0, radius2=1.0, depth=0.4)
    
    # Find the top face to begin extrusions
    top_face = next((f for f in bm.faces if f.normal.z > 0.9), None)
    
    if top_face:
        # Inset and Extrude UP
        bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3)
        ret = bmesh.ops.extrude_discrete_faces(bm, faces=[top_face])
        extruded_face = ret['faces'][0]
        bmesh.ops.translate(bm, verts=extruded_face.verts, vec=(0, 0, 0.5))
        
        # Inset and Extrude DOWN (Cavity)
        bmesh.ops.inset_region(bm, faces=[extruded_face], thickness=0.2)
        ret2 = bmesh.ops.extrude_discrete_faces(bm, faces=[extruded_face])
        cavity_face = ret2['faces'][0]
        bmesh.ops.translate(bm, verts=cavity_face.verts, vec=(0, 0, -0.4))

    bm.to_mesh(mesh)
    bm.free()
    
    # Apply smooth shading to all faces
    for poly in mesh.polygons:
        poly.use_smooth = True
        
    # === Step 2: Apply Modifiers ===
    # Bevel to catch light on the hard 90-degree edges
    bevel_mod = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel_mod.limit_method = 'ANGLE'
    bevel_mod.angle_limit = math.radians(45)
    bevel_mod.width = 0.04
    bevel_mod.segments = 3
    
    # Subsurf to smooth the rounded perimeter
    subsurf_mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf_mod.levels = 2
    subsurf_mod.render_levels = 2

    # === Step 3: Build UV-less Triplanar Material ===
    mat = bpy.data.materials.new(name=object_name + "_TriplanarMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Material Nodes
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (1000, 0)
    
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (700, 0)
    
    # Mix between Rust (A) and Paint (B)
    mix_color = nodes.new('ShaderNodeMixRGB')
    mix_color.location = (500, 200)
    mix_color.inputs[1].default_value = (0.2, 0.07, 0.02, 1.0) # Rust
    mix_color.inputs[2].default_value = (*material_color, 1.0) # Paint
    
    # Color Ramp to create a sharp mask from the noise
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (200, 200)
    color_ramp.color_ramp.elements[0].position = 0.4
    color_ramp.color_ramp.elements[1].position = 0.55
    
    # 3D Procedural Noise (Inherently triplanar)
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (0, 200)
    noise.inputs['Scale'].default_value = 4.0
    noise.inputs['Detail'].default_value = 15.0
    noise.inputs['Roughness'].default_value = 0.7
    
    # The Core Technique: Mapping via Object Coordinates
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-200, 200)
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-400, 200)
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (500, -100)
    bump.inputs['Strength'].default_value = 0.6
    bump.inputs['Distance'].default_value = 0.1
    
    # Logic Connections
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector']) # CRITICAL: Object Coords
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], mix_color.inputs['Fac'])
    
    # PBR Connections
    links.new(mix_color.outputs['Color'], principled.inputs['Base Color'])
    links.new(color_ramp.outputs['Color'], principled.inputs['Roughness']) # Paint is shiny (0), Rust is rough (1)
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], principled.inputs['Normal'])
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # --- TUTORIAL DEMONSTRATION NODE ---
    # This node is left disconnected but demonstrates the exact Box mapping settings taught in the video
    box_demo_tex = nodes.new('ShaderNodeTexImage')
    box_demo_tex.location = (0, -150)
    box_demo_tex.label = "Tutorial Box Projection Demo"
    box_demo_tex.projection = 'BOX'           # Skill: Change Flat to Box
    box_demo_tex.projection_blend = 0.25      # Skill: Increase blend to hide seams
    links.new(mapping.outputs['Vector'], box_demo_tex.inputs['Vector'])
    # -----------------------------------
    
    obj.data.materials.append(mat)
    
    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    return f"Created '{object_name}' with UV-less Object mapping at {location}"
