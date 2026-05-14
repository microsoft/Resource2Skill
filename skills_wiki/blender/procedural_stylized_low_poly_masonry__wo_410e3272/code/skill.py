def create_low_poly_well_base(
    scene_name: str = "Scene",
    object_name: str = "StylizedWellBase",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    radius: float = 1.5,
    rings: int = 4,
    stones_per_ring: int = 14,
    stone_height: float = 0.3,
    stone_depth: float = 0.4,
    wobble_strength: float = 0.08,
    decimate_ratio: float = 0.3,
    color_base: tuple = (0.55, 0.55, 0.55),
    color_variation: tuple = (0.45, 0.45, 0.50),
    **kwargs
) -> str:
    """
    Creates a procedural, low-poly stylized masonry ring (like a well base).
    
    Args:
        scene_name: Target scene.
        object_name: Master name for the parent object and children.
        location: (x,y,z) coordinates for the center base of the well.
        scale: Master scale multiplier.
        radius: Inner radius of the well base.
        rings: Number of vertical layers of stones.
        stones_per_ring: Number of stones placed in a 360-degree circle.
        stone_height/stone_depth: Thickness dimensions of individual stones.
        wobble_strength: How severely the stones are distorted.
        decimate_ratio: The severity of the low-poly look (lower = more faceted).
        color_base / color_variation: RGB tuples for the randomized stone coloring.
        
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === 1. Create Parent Hierarchy ===
    parent_empty = bpy.data.objects.new(object_name, None)
    parent_empty.location = Vector(location)
    parent_empty.scale = (scale, scale, scale)
    scene.collection.objects.link(parent_empty)

    # Empty to drive the noise displacement (ensures each stone gets unique noise)
    noise_empty = bpy.data.objects.new(f"{object_name}_NoiseOrigin", None)
    noise_empty.parent = parent_empty
    noise_empty.location = (0.1, 0.2, 0.3)  # Offset to break symmetry
    scene.collection.objects.link(noise_empty)

    # === 2. Procedural Assets (Texture & Material) ===
    texture = bpy.data.textures.new(f"{object_name}_Noise", type='CLOUDS')
    texture.noise_scale = 0.35

    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    node_out = nodes.new("ShaderNodeOutputMaterial")
    node_out.location = (300, 0)
    
    node_bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    node_bsdf.location = (0, 0)
    node_bsdf.inputs['Roughness'].default_value = 0.95
    node_bsdf.inputs['Specular IOR Level'].default_value = 0.1
    
    node_ramp = nodes.new("ShaderNodeValToRGB")
    node_ramp.location = (-300, 0)
    node_ramp.color_ramp.elements[0].color = (*color_base, 1.0)
    node_ramp.color_ramp.elements[1].color = (*color_variation, 1.0)
    
    node_obj_info = nodes.new("ShaderNodeObjectInfo")
    node_obj_info.location = (-600, 0)

    # Route Object Random -> ColorRamp -> Base Color
    links.new(node_obj_info.outputs['Random'], node_ramp.inputs['Fac'])
    links.new(node_ramp.outputs['Color'], node_bsdf.inputs['Base Color'])
    links.new(node_bsdf.outputs['BSDF'], node_out.inputs['Surface'])

    # === 3. Pre-calculate Geometry ===
    # s_len calculates the tangential length to fit 'stones_per_ring' perfectly.
    # We multiply by 0.98 to leave a tiny stylized 2% gap between stones.
    s_len = (2 * math.pi * radius) / stones_per_ring * 0.98
    s_depth = stone_depth
    s_height = stone_height
    
    # === 4. Generate Stone Rings ===
    stone_count = 0
    for ring in range(rings):
        z_offset = ring * s_height
        # Offset alternating rings for standard masonry overlapping
        angle_offset = (math.pi / stones_per_ring) if ring % 2 == 1 else 0.0

        for i in range(stones_per_ring):
            angle = i * (2 * math.pi / stones_per_ring) + angle_offset
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)

            # Generate base mesh (Vertices scaled directly so object scale stays 1,1,1)
            mesh = bpy.data.meshes.new(f"{object_name}_Mesh_R{ring}_S{i}")
            bm = bmesh.new()
            bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=(s_len, s_depth, s_height), verts=bm.verts)
            bm.to_mesh(mesh)
            bm.free()

            # Create and place object
            stone = bpy.data.objects.new(f"{object_name}_R{ring}_S{i}", mesh)
            stone.parent = parent_empty
            
            # Local transforms relative to the parent empty
            stone.location = (x, y, z_offset)
            # Rotate tangential to the circle
            stone.rotation_euler.z = angle + (math.pi / 2)
            
            scene.collection.objects.link(stone)

            # === 5. The "Stylized Stone" Modifier Stack ===
            # Bevel edges slightly
            mod_bevel = stone.modifiers.new("Bevel", 'BEVEL')
            mod_bevel.limit_method = 'NONE'
            mod_bevel.width = min(s_len, s_depth, s_height) * 0.15
            mod_bevel.segments = 2

            # Add topology for noise displacement
            mod_subdiv = stone.modifiers.new("Subdiv", 'SUBSURF')
            mod_subdiv.subdivision_type = 'SIMPLE'
            mod_subdiv.levels = 3

            # Distort with procedural noise
            mod_displace = stone.modifiers.new("Displace", 'DISPLACE')
            mod_displace.texture = texture
            mod_displace.strength = wobble_strength
            mod_displace.texture_coords = 'OBJECT'
            mod_displace.texture_coords_object = noise_empty

            # Decimate back down to chunky flat-shaded triangles
            mod_decimate = stone.modifiers.new("Decimate", 'DECIMATE')
            mod_decimate.decimate_type = 'COLLAPSE'
            mod_decimate.ratio = decimate_ratio

            # Apply material and explicitly ensure flat shading
            stone.data.materials.append(mat)
            for poly in stone.data.polygons:
                poly.use_smooth = False
                
            stone_count += 1

    return f"Created low-poly well base '{object_name}' at {location} containing {stone_count} highly randomized procedural stones."
