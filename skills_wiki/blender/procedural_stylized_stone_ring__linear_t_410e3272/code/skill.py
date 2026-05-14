def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedWellBase",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.45, 0.42, 0.48),
    tiers: int = 3,
    **kwargs,
) -> str:
    """
    Create a procedural stylized stone ring (like a well base) using linear-to-radial bending.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated hierarchy.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) flat color for the stones.
        tiers: Number of vertical stone rings to stack.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector

    # 1. Ensure scene exists
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection

    # 2. Create Master Container
    container = bpy.data.objects.new(object_name, None)
    collection.objects.link(container)
    container.location = Vector(location)
    container.scale = (scale, scale, scale)

    # 3. Create Shared Material
    mat_name = f"{object_name}_Mat"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.9
            bsdf.inputs['Specular IOR Level'].default_value = 0.2

    # 4. Create Procedural Displacement Texture (Shared)
    tex_name = f"{object_name}_DisplaceTex"
    tex = bpy.data.textures.get(tex_name)
    if not tex:
        tex = bpy.data.textures.new(tex_name, 'CLOUDS')
        tex.noise_scale = 0.8

    # 5. Build the Tiers
    stone_y = 0.4  # Base thickness of the wall
    stone_z = 0.3  # Base height of each stone row

    for tier in range(tiers):
        tier_radius = 1.2 - (tier * 0.12)  # Taper inwards as tiers go up
        circumference = 2.0 * math.pi * tier_radius
        
        # Vary the number of stones per tier to prevent unnatural alignment
        num_stones = 12 - tier
        stone_len = circumference / num_stones
        
        # BMesh generation for the linear row
        bm = bmesh.new()
        start_x = -circumference / 2.0

        for i in range(num_stones):
            ret = bmesh.ops.create_cube(bm, size=1.0)
            
            # Scale each block. Length is > 1.0 to overlap and prevent gaps
            sx = stone_len * random.uniform(1.05, 1.15)
            sy = stone_y * random.uniform(0.85, 1.15)
            sz = stone_z * random.uniform(0.85, 1.15)
            bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=ret['verts'])

            # Translate to linear position along X axis
            pos_x = start_x + (i * stone_len) + (stone_len / 2.0)
            
            # Minor vertical and depth offsets for organic irregularity
            pos_y = random.uniform(-0.02, 0.02)
            pos_z = random.uniform(-0.02, 0.02)
            
            bmesh.ops.translate(bm, vec=(pos_x, pos_y, pos_z), verts=ret['verts'])

        # Create Mesh & Object
        mesh = bpy.data.meshes.new(f"{object_name}_Tier_{tier}_Mesh")
        bm.to_mesh(mesh)
        bm.free()
        
        obj = bpy.data.objects.new(f"{object_name}_Tier_{tier}", mesh)
        collection.objects.link(obj)
        obj.data.materials.append(mat)
        
        # 6. Modifier Stack for Chiseled Low-Poly Detailing
        
        # A. Subsurf to create geometry for displacement
        subsurf = obj.modifiers.new(name="Subsurf", type='SUBSURF')
        subsurf.levels = 3
        subsurf.render_levels = 3

        # B. Displace to warp the stones
        displace = obj.modifiers.new(name="Displace", type='DISPLACE')
        displace.texture = tex
        displace.strength = 0.12
        displace.mid_level = random.uniform(0.3, 0.7) # Varies the overall bulge per tier

        # C. Decimate to create the chunky, faceted low-poly look
        decimate = obj.modifiers.new(name="Decimate", type='DECIMATE')
        decimate.ratio = 0.15

        # D. Simple Deform to wrap the linear stones into a circle
        bend = obj.modifiers.new(name="Bend", type='SIMPLE_DEFORM')
        bend.deform_method = 'BEND'
        bend.angle = 2.0 * math.pi  # 360 degrees
        bend.deform_axis = 'Z'

        # 7. Parenting and Spatial Orientation
        # We create a pivot empty for this specific tier so we can easily 
        # rotate it (scrambling the seam alignment) without complex origin math.
        pivot = bpy.data.objects.new(f"{object_name}_Pivot_{tier}", None)
        collection.objects.link(pivot)
        pivot.parent = container
        
        # Stack vertically
        pivot.location = (0.0, 0.0, tier * stone_z * 0.95)
        # Randomize rotational seam
        pivot.rotation_euler.z = random.uniform(0.0, 2.0 * math.pi)

        obj.parent = pivot
        
        # CRITICAL OFFSET: After 360 degree bending around local Z, the linear X-axis 
        # wraps into a circle centered at local Y = +Radius. 
        # We shift the object backwards by -Radius so the circle centers exactly on its pivot.
        obj.location.y = -tier_radius

    return f"Created '{object_name}' with {tiers} procedural stone rings at {location}"
