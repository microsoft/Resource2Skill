def create_object(
    scene_name: str = "Scene",
    object_name: str = "LazyBuilding",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.5, 0.5, 0.45),
    **kwargs,
) -> str:
    """
    Create a procedural, semi-derelict building block based on the "Lazy Tutorials" workflow.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created building object.
        location: (x, y, z) world-space base position.
        scale: Uniform scale factor multiplier.
        material_color: (R, G, B) base color for the building walls.
        **kwargs: width, depth, and height overrides.

    Returns:
        Status string describing the generated building.
    """
    import bpy
    import bmesh
    import random
    from mathutils import Vector

    # Parse dimensions
    b_width = kwargs.get("width", 2.0) * scale
    b_depth = kwargs.get("depth", 2.0) * scale
    b_height = kwargs.get("height", 6.0) * scale
    
    # Initialize mesh and object
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    scene.collection.objects.link(obj)
    
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    
    # Scale cube bounding box
    for v in bm.verts:
        v.co.x *= b_width
        v.co.y *= b_depth
        v.co.z *= b_height
        
    # Translate so the building base sits exactly at Z=0 relative to its origin
    for v in bm.verts:
        v.co.z += b_height / 2.0
        
    # Subdivide heavily to create the "grid" for architectural details
    bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=7, use_grid_fill=True)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=1, use_grid_fill=True)

    # 1. Macro Extrusions (Balconies, structural variation)
    faces = [f for f in bm.faces if abs(f.normal.z) < 0.1]
    num_extrusions = max(1, len(faces) // 20)
    extrude_candidates = random.sample(faces, min(num_extrusions, len(faces)))
    
    if extrude_candidates:
        ret = bmesh.ops.extrude_discrete_faces(bm, faces=extrude_candidates)
        for f in ret['faces']:
            center = f.calc_center_median()
            # Scale slightly to avoid perfectly coplanar overlapping walls
            for v in f.verts:
                v.co = center + (v.co - center) * random.uniform(0.85, 0.95)
            # Push outward
            bmesh.ops.translate(bm, vec=f.normal * random.uniform(0.3, 1.2) * scale, verts=f.verts)

    # 2. Window Insets
    bm.faces.ensure_lookup_table()
    side_faces = [f for f in bm.faces if abs(f.normal.z) < 0.1 and f.calc_area() > (0.02 * scale * scale)]
    
    # Randomly select a portion of the side grid to become windows
    window_faces = [f for f in side_faces if random.random() > 0.35]
    
    if window_faces:
        ret = bmesh.ops.extrude_discrete_faces(bm, faces=window_faces)
        new_window_faces = set(ret['faces'])
        
        for f in new_window_faces:
            center = f.calc_center_median()
            # Inset the face (scales it down to form the window frame)
            inset_factor = random.uniform(0.7, 0.85)
            for v in f.verts:
                v.co = center + (v.co - center) * inset_factor
            # Push inwards to create the recess depth
            recess_depth = random.uniform(0.05, 0.15) * scale
            bmesh.ops.translate(bm, vec=-f.normal * recess_depth, verts=f.verts)
    else:
        new_window_faces = set()

    # Assign materials mapping based on face type
    for f in bm.faces:
        if f in new_window_faces:
            # 1 = Lit Window (30% chance), 2 = Dark Window (70% chance)
            f.material_index = 1 if random.random() > 0.7 else 2
        else:
            # 0 = Wall
            f.material_index = 0

    # 3. Random perturbation for "lazy/crooked" derelict look
    perturb_amount = 0.015 * scale
    for v in bm.verts:
        v.co.x += random.uniform(-perturb_amount, perturb_amount)
        v.co.y += random.uniform(-perturb_amount, perturb_amount)
        v.co.z += random.uniform(-perturb_amount, perturb_amount)

    bm.to_mesh(mesh)
    bm.free()
    
    # --- Materials Setup ---
    # Wall Material (Grungy Concrete)
    mat_wall = bpy.data.materials.new(f"{object_name}_Wall")
    mat_wall.use_nodes = True
    nodes = mat_wall.node_tree.nodes
    links = mat_wall.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    
    noise = nodes.new("ShaderNodeTexNoise")
    noise.inputs['Scale'].default_value = 25.0
    
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.4
    ramp.color_ramp.elements[0].color = (*material_color, 1.0)
    ramp.color_ramp.elements[1].position = 0.6
    dark_color = (max(0, material_color[0]-0.2), max(0, material_color[1]-0.2), max(0, material_color[2]-0.2), 1.0)
    ramp.color_ramp.elements[1].color = dark_color
    
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    if bsdf:
        links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
        bsdf.inputs['Roughness'].default_value = 0.85
        
    # Lit Window Material (Emissive)
    mat_lit = bpy.data.materials.new(f"{object_name}_LitWindow")
    mat_lit.use_nodes = True
    bsdf_lit = mat_lit.node_tree.nodes.get("Principled BSDF")
    if bsdf_lit:
        bsdf_lit.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1.0)
        bsdf_lit.inputs['Roughness'].default_value = 0.2
        emission_color = (1.0, 0.6, 0.1, 1.0) # Warm orange/yellow light
        # Handle Blender 3.x vs 4.x Emission API changes
        if 'Emission Color' in bsdf_lit.inputs:
            bsdf_lit.inputs['Emission Color'].default_value = emission_color
        elif 'Emission' in bsdf_lit.inputs:
            bsdf_lit.inputs['Emission'].default_value = emission_color
        if 'Emission Strength' in bsdf_lit.inputs:
            bsdf_lit.inputs['Emission Strength'].default_value = 5.0
            
    # Dark Window Material (Glossy/Unlit)
    mat_dark = bpy.data.materials.new(f"{object_name}_DarkWindow")
    mat_dark.use_nodes = True
    bsdf_dark = mat_dark.node_tree.nodes.get("Principled BSDF")
    if bsdf_dark:
        bsdf_dark.inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1.0)
        bsdf_dark.inputs['Roughness'].default_value = 0.15
        
    # Append materials in exact order of indices (0, 1, 2)
    obj.data.materials.append(mat_wall)
    obj.data.materials.append(mat_lit)
    obj.data.materials.append(mat_dark)
    
    # Position object in world
    obj.location = Vector(location)
    
    # Apply EdgeSplit to retain hard architectural edges while smoothing the slight jitter
    for poly in mesh.polygons:
        poly.use_smooth = True
    mod = obj.modifiers.new(name="EdgeSplit", type='EDGE_SPLIT')
    mod.split_angle = 0.523599 # ~30 degrees
    
    return f"Created procedural building '{object_name}' with {len(mesh.polygons)} faces at {location}."
