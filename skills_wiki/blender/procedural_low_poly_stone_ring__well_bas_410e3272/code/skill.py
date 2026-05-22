def create_stone_ring(
    scene_name: str = "Scene",
    object_name: str = "StoneRing",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    radius: float = 1.0,
    stone_height: float = 0.3,
    stone_thickness: float = 0.3,
    material_color: tuple = (0.5, 0.45, 0.45),
    **kwargs,
) -> str:
    """
    Create a procedural, low-poly circular stone wall (e.g., a well base).
    Call this multiple times with varying radii and Z-locations to stack tiers.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        radius: The radius of the circular stone ring.
        stone_height: Average height of the stones.
        stone_thickness: Average depth/thickness of the stones.
        material_color: (R, G, B) base color of the stones.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Calculate Proportions ===
    circumference = 2 * math.pi * radius
    avg_stone_length = 0.4
    num_stones = max(4, int(circumference / avg_stone_length))
    gap = 0.02

    # Generate random proportions to give stones varying lengths
    proportions = [random.uniform(0.5, 1.5) for _ in range(num_stones)]
    total_prop = sum(proportions)

    # === Step 2: Build Base Mesh (Linear layout) ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    current_x = -circumference / 2.0

    for prop in proportions:
        # Calculate actual length for this specific stone
        stone_len = (prop / total_prop) * circumference
        l = stone_len - gap
        
        # Slight random variations in height and depth
        h = stone_height * random.uniform(0.85, 1.15)
        d = stone_thickness * random.uniform(0.85, 1.15)
        
        # Position centered along X, with slight Y offset for wobble
        cx = current_x + (stone_len / 2.0)
        cy = random.uniform(-0.04, 0.04)
        cz = h / 2.0
        
        # Create cube island
        ret = bmesh.ops.create_cube(bm, size=1.0)
        verts = ret['verts']
        bmesh.ops.scale(bm, vec=Vector((l, d, h)), verts=verts)
        bmesh.ops.translate(bm, vec=Vector((cx, cy, cz)), verts=verts)
        
        current_x += stone_len

    # Add base level of irregularity to vertices
    for v in bm.verts:
        v.co.x += random.uniform(-0.015, 0.015)
        v.co.y += random.uniform(-0.015, 0.015)
        v.co.z += random.uniform(-0.015, 0.015)

    bm.to_mesh(mesh)
    bm.free()

    # Shade flat for the low poly look
    for poly in mesh.polygons:
        poly.use_smooth = False

    # === Step 3: Modifier Stack for Low Poly Detailing & Bending ===
    
    # 1. Bevel: Soften harsh edges
    mod_bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    mod_bevel.width = 0.04
    mod_bevel.segments = 2

    # 2. Subsurf: Add geometric resolution for the displacement step
    mod_subdiv = obj.modifiers.new(name="Subdiv", type='SUBSURF')
    mod_subdiv.subdivision_type = 'SIMPLE'
    mod_subdiv.levels = 2

    # 3. Displace: Adds the random, organic dents and chips
    tex_name = "Procedural_Stone_Noise"
    if tex_name not in bpy.data.textures:
        tex = bpy.data.textures.new(name=tex_name, type='CLOUDS')
        tex.noise_scale = 0.35
    else:
        tex = bpy.data.textures[tex_name]

    mod_disp = obj.modifiers.new(name="Displace", type='DISPLACE')
    mod_disp.texture = tex
    mod_disp.strength = 0.06
    # Use random object location as coords so different rings have different noise
    mod_disp.texture_coords = 'LOCAL'

    # 4. Bend: Wrap the linear wall into a perfect circle
    mod_bend = obj.modifiers.new(name="Bend", type='SIMPLE_DEFORM')
    mod_bend.deform_method = 'BEND'
    mod_bend.angle = 2 * math.pi # 360 degrees
    mod_bend.deform_axis = 'Z'

    # 5. Decimate: Crunch the geometry down to jagged, faceted triangles
    mod_decimate = obj.modifiers.new(name="Decimate", type='DECIMATE')
    mod_decimate.ratio = 0.35 

    # === Step 4: Material with Random Per-Island Tinting ===
    mat = bpy.data.materials.new(name=object_name + "_Mat")
    mat.use_nodes = True
    node_tree = mat.node_tree
    bsdf = node_tree.nodes.get("Principled BSDF")
    
    if bsdf:
        bsdf.inputs['Roughness'].default_value = 0.95
        bsdf.inputs['Specular'].default_value = 0.1
        
        # Create nodes for random color variation
        geom_node = node_tree.nodes.new(type='ShaderNodeNewGeometry')
        ramp_node = node_tree.nodes.new(type='ShaderNodeValToRGB')
        
        c_r, c_g, c_b = material_color
        # Darker variant
        ramp_node.color_ramp.elements[0].position = 0.0
        ramp_node.color_ramp.elements[0].color = (max(0, c_r-0.08), max(0, c_g-0.08), max(0, c_b-0.08), 1.0)
        # Lighter variant
        ramp_node.color_ramp.elements[1].position = 1.0
        ramp_node.color_ramp.elements[1].color = (min(1, c_r+0.08), min(1, c_g+0.08), min(1, c_b+0.08), 1.0)
        
        node_tree.links.new(geom_node.outputs['Random Per Island'], ramp_node.inputs['Fac'])
        node_tree.links.new(ramp_node.outputs['Color'], bsdf.inputs['Base Color'])

    obj.data.materials.append(mat)

    # === Step 5: Final Placement ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' (Radius {radius}m) at {location} with {num_stones} procedurally chipped stones."
