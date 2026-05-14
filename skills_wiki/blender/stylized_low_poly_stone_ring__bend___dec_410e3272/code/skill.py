def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyWellBase",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.55, 0.55, 0.6),
    layers: int = 3,
    stones_per_layer: int = 12,
    **kwargs
) -> str:
    """
    Create a Stylized Low-Poly Stone Ring (e.g., for a well) in the active scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the stone.
        layers: Number of vertical stone rings stacked on top of each other.
        stones_per_layer: Number of stones making up a single 360-degree ring.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector, Matrix

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.9
        bsdf.inputs["Specular IOR Level"].default_value = 0.2

    # === Step 2: Parametric Configuration ===
    radius = 1.0
    total_length = 2 * math.pi * radius
    stone_width = total_length / stones_per_layer
    stone_depth = 0.35
    stone_height = 0.30
    
    mesh = bpy.data.meshes.new(object_name)
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    obj.data.materials.append(mat)
    
    bm = bmesh.new()
    
    # === Step 3: Build Flat Staggered Wall ===
    for layer in range(layers):
        # Stagger every other layer by half a brick for interlocking pattern
        x_offset = (layer % 2) * (stone_width / 2.0)
        z_pos = layer * (stone_height * 0.9) # 10% vertical overlap
        
        for i in range(stones_per_layer):
            # Introduce slight scale variations for organic feel
            s_width = stone_width * random.uniform(0.85, 1.15)
            s_depth = stone_depth * random.uniform(0.85, 1.15)
            s_height = stone_height * random.uniform(0.85, 1.15)
            
            x_pos = x_offset + (i * stone_width)
            y_pos = random.uniform(-0.03, 0.03)
            
            # Create individual stone base
            ret = bmesh.ops.create_cube(bm, size=1.0)
            verts = ret['verts']
            
            bmesh.ops.scale(bm, vec=(s_width, s_depth, s_height), verts=verts)
            # Offset x by s_width/2 so bounding left edge starts exactly at x_pos
            bmesh.ops.translate(bm, vec=(x_pos + s_width/2, y_pos, z_pos), verts=verts)
            
            # Subdivide to provide geometry for the noise & decimation process
            edges = [e for e in bm.edges if e.verts[0] in verts and e.verts[1] in verts]
            bmesh.ops.subdivide_edges(bm, edges=edges, cuts=2, use_grid_fill=True)
            
    # === Step 4: Randomize & Taper ===
    max_z = (layers - 1) * stone_height
    for v in bm.verts:
        # Spatial noise (simulates manual 'Randomize' tool)
        v.co.x += random.uniform(-0.02, 0.02)
        v.co.y += random.uniform(-0.02, 0.02)
        v.co.z += random.uniform(-0.02, 0.02)
        
        # Taper upper layers inward slightly (creates a sturdier silhouette)
        taper_amount = 0.12 * (v.co.z / max_z) if max_z > 0 else 0
        v.co.y -= taper_amount * radius
        
    # === Step 5: Wrap Flat Wall into a Perfect Cylinder ===
    # Using polar coordinates bypasses all bounding-box issues found in standard Bend modifiers.
    for v in bm.verts:
        angle = (v.co.x / total_length) * 2 * math.pi
        r = radius + v.co.y
        
        # Convert to Polar
        v.co.x = math.cos(angle) * r
        v.co.y = math.sin(angle) * r

    bm.to_mesh(mesh)
    bm.free()
    
    # === Step 6: Decimate for Chunky Low-Poly Look ===
    decimate = obj.modifiers.new(name="Decimate", type='DECIMATE')
    decimate.ratio = 0.25 # Aggressively collapses quads into jagged triangles
    
    # Evaluate depsgraph to permanently apply the decimation modifier
    dg = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(dg)
    eval_mesh = bpy.data.meshes.new_from_object(eval_obj)
    
    # Ensure mandatory flat shading for the low poly style
    for poly in eval_mesh.polygons:
        poly.use_smooth = False
        
    obj.modifiers.clear()
    obj.data = eval_mesh
    
    # === Step 7: Final Transform & Placement ===
    # Adjust origin to the bottom center of the geometry
    local_bbox_center = sum((Vector(b) for b in obj.bound_box), Vector()) / 8
    min_z = min(v.co.z for v in obj.data.vertices)
    offset = Vector((local_bbox_center.x, local_bbox_center.y, min_z))
    
    obj.data.transform(Matrix.Translation(-offset))
    
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    return f"Created '{object_name}' (Low-Poly Well Base) at {location} with {layers} layers"
