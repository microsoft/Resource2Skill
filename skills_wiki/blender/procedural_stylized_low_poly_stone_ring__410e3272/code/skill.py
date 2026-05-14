def create_stylized_stone_ring(
    scene_name: str = "Scene",
    object_name: str = "StylizedWellBase",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    num_layers: int = 3,
    stones_per_layer: int = 12,
    base_radius: float = 1.0,
    color_1: tuple = (0.45, 0.45, 0.50, 1.0), # Grayish
    color_2: tuple = (0.55, 0.50, 0.55, 1.0), # Purplish
    **kwargs
) -> str:
    """
    Creates a stylized, low-poly stone ring (e.g., for a well base) using the procedural 
    'Wobble & Crunch' modifier pattern.
    
    Args:
        scene_name: Target scene.
        object_name: Name of the generated mesh.
        location: World placement.
        scale: Uniform scale.
        num_layers: Number of stacked stone rings.
        stones_per_layer: Number of bricks per ring.
        base_radius: Size of the circular base.
        color_1/color_2: Base color range for the random per-island tinting.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector, Euler

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Step 1: Procedural Geometry Generation ---
    bm = bmesh.new()
    
    # Calculate base stone dimensions
    # Leave a ~15% gap between stones for the organic look
    stone_x = (2 * math.pi * base_radius) / stones_per_layer * 0.85 
    stone_y = base_radius * 0.35  # Depth/Thickness
    stone_z = 0.25                # Height
    
    for layer in range(num_layers):
        # Taper the radius slightly inward as it goes up
        layer_radius = base_radius * (1.0 - layer * 0.03)
        # Overlap the Z layers slightly so they intersect heavily
        layer_z_offset = layer * stone_z * 0.85
        # Interlock the bricks (offset angle for alternating layers)
        layer_angle_offset = (math.pi / stones_per_layer) if layer % 2 == 1 else 0
        
        for i in range(stones_per_layer):
            angle = i * (2 * math.pi / stones_per_layer) + layer_angle_offset
            
            # Record existing geometry to isolate the new cube
            geom_start = set(bm.verts) | set(bm.edges) | set(bm.faces)
            bmesh.ops.create_cube(bm, size=1.0)
            
            new_verts = [v for v in bm.verts if v not in geom_start]
            
            # Add random scale variation per stone
            sx = stone_x * random.uniform(0.85, 1.15)
            sy = stone_y * random.uniform(0.85, 1.15)
            sz = stone_z * random.uniform(0.85, 1.15)
            
            bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=new_verts)
            
            # Rotate so the long side (X) is tangent to the circle
            rot_eul = Euler((0, 0, angle + math.pi/2), 'XYZ')
            bmesh.ops.rotate(bm, verts=new_verts, cent=(0,0,0), matrix=rot_eul.to_matrix())
            
            # Translate to the circle edge
            pos = Vector((layer_radius * math.cos(angle), layer_radius * math.sin(angle), layer_z_offset))
            bmesh.ops.translate(bm, vec=pos, verts=new_verts)

    # Output to mesh
    mesh = bpy.data.meshes.new(object_name)
    bm.to_mesh(mesh)
    bm.free()
    
    # Force flat shading for low-poly look
    for poly in mesh.polygons:
        poly.use_smooth = False

    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # --- Step 2: The 'Wobble & Crunch' Modifier Stack ---
    
    # 2a. Bevel (softens corners before displacement)
    mod_bevel = obj.modifiers.new("Bevel", 'BEVEL')
    mod_bevel.width = 0.04
    mod_bevel.segments = 2
    
    # 2b. Simple Subdivision (adds grid for noise to affect)
    mod_subd = obj.modifiers.new("Subdivide", 'SUBSURF')
    mod_subd.subdivision_type = 'SIMPLE'
    mod_subd.levels = 3
    mod_subd.render_levels = 3

    # 2c. Displace (the Wobble)
    tex_name = f"{object_name}_Noise"
    tex = bpy.data.textures.get(tex_name) or bpy.data.textures.new(tex_name, type='CLOUDS')
    tex.noise_scale = 0.45
    
    mod_disp = obj.modifiers.new("Wobble", 'DISPLACE')
    mod_disp.texture = tex
    mod_disp.strength = 0.12
    mod_disp.texture_coords = 'LOCAL' # Keeps stones consistent if moved
    
    # 2d. Decimate (the Crunch - creates faceted chipped stone look)
    mod_dec = obj.modifiers.new("Decimate", 'DECIMATE')
    mod_dec.ratio = 0.15 # Aggressive reduction

    # --- Step 3: Material Generation ---
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs['Roughness'].default_value = 0.85
    
    # Use Random Per Island to give each brick a unique tint
    try:
        geom_node = nodes.new(type='ShaderNodeNewGeometry')
        color_ramp = nodes.new(type='ShaderNodeValToRGB')
        color_ramp.color_ramp.elements[0].color = color_1
        color_ramp.color_ramp.elements[1].color = color_2
        
        # Add a mid-tone
        mid_elem = color_ramp.color_ramp.elements.new(0.5)
        mid_elem.color = ((color_1[0]+color_2[0])/2, (color_1[1]+color_2[1])/2, (color_1[2]+color_2[2])/2, 1.0)
        
        links.new(geom_node.outputs['Random Per Island'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
    except Exception:
        # Fallback if specific nodes fail
        bsdf.inputs['Base Color'].default_value = color_1
        
    obj.data.materials.append(mat)

    # --- Step 4: Final Positioning ---
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' at {location} with {num_layers * stones_per_layer} interlocking stones."
