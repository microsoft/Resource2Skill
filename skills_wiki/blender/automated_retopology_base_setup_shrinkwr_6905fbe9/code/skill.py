def create_retopology_sleeve(
    scene_name: str = "Scene",
    object_name: str = "Retopo_Sleeve",
    target_object_name: str = "HighPolyTarget",
    location: tuple = (0, 0, 0),
    rotation: tuple = (0, 1.5708, 0),  # Rotated 90 degrees on Y by default (horizontal)
    scale: float = 1.0,
    length: float = 2.0,
    radius: float = 0.5,
    segments: int = 16,
    loops: int = 10,
    offset: float = 0.015,
    material_color: tuple = (0.15, 0.6, 0.8),
    **kwargs,
) -> str:
    """
    Creates a procedural retopology sleeve (hollow cylinder with loop cuts) 
    automatically shrinkwrapped to a target high-poly object.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created retopology mesh.
        target_object_name: The high-poly object to wrap around. (If not found, a dummy is created).
        location: (x, y, z) world-space position.
        rotation: (x, y, z) euler rotation in radians.
        scale: Uniform scale factor.
        length: Total length of the generated sleeve.
        radius: Radius of the sleeve.
        segments: Number of vertices in each circular ring.
        loops: Number of subdivisions along the length.
        offset: Distance to float above the target surface.
        material_color: (R, G, B) color of the retopology mesh.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Ensure Target Exists ===
    target_obj = bpy.data.objects.get(target_object_name)
    if not target_obj:
        # Create a dummy high-poly "arm" to demonstrate the wrapping effect
        mesh_dummy = bpy.data.meshes.new(f"{target_object_name}_Mesh")
        target_obj = bpy.data.objects.new(target_object_name, mesh_dummy)
        bpy.context.collection.objects.link(target_obj)
        
        bm_dummy = bmesh.new()
        bmesh.ops.create_uvsphere(
            bm_dummy, u_segments=64, v_segments=32, radius=radius * 0.8
        )
        bm_dummy.to_mesh(mesh_dummy)
        bm_dummy.free()
        
        target_obj.location = location
        target_obj.rotation_euler = rotation
        # Stretch into an arm-like pill shape
        target_obj.scale = (scale, scale, scale * (length / (radius * 1.6)))
        
        for poly in mesh_dummy.polygons:
            poly.use_smooth = True
            
        # Add a displace modifier for organic lumps
        mod = target_obj.modifiers.new(name="Displace", type='DISPLACE')
        tex = bpy.data.textures.new("DummyNoise", type='CLOUDS')
        tex.noise_scale = 0.5
        mod.texture = tex
        mod.strength = radius * 0.2

    # === Step 2: Create Procedural Retopo Sleeve Geometry ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    bpy.context.collection.objects.link(obj)
    
    bm = bmesh.new()
    
    # Generate the un-capped cylinder loop by loop
    for i in range(loops + 2):
        z = (i / (loops + 1) - 0.5) * length
        circle_verts = []
        
        for s in range(segments):
            angle = (s / segments) * math.pi * 2
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            v = bm.verts.new((x, y, z))
            circle_verts.append(v)
            
        # Connect to the previous ring to form quad faces
        if i > 0:
            prev_ring_verts = bm.verts[-(segments * 2):-segments]
            for s in range(segments):
                v1 = prev_ring_verts[s]
                v2 = prev_ring_verts[(s + 1) % segments]
                v3 = circle_verts[(s + 1) % segments]
                v4 = circle_verts[s]
                bm.faces.new((v1, v2, v3, v4))

    bm.to_mesh(mesh)
    bm.free()

    # === Step 3: Positioning and Display Settings ===
    obj.location = location
    obj.rotation_euler = rotation
    obj.scale = (scale, scale, scale)
    
    # Crucial viewport settings for retopology workflow
    obj.display_type = 'SOLID'
    obj.show_wire = True
    obj.show_in_front = True

    # === Step 4: Shrinkwrap Modifier ===
    # This matches the new 'Face Nearest' snapping behavior
    sw_mod = obj.modifiers.new(name="Retopo_Shrinkwrap", type='SHRINKWRAP')
    sw_mod.target = target_obj
    sw_mod.wrap_method = 'NEAREST_SURFACEPOINT'
    sw_mod.wrap_mode = 'ABOVE_SURFACE'
    sw_mod.offset = offset

    # === Step 5: Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.8
    obj.data.materials.append(mat)

    return f"Created retopology sleeve '{object_name}' (Shrinkwrapped to '{target_obj.name}' with offset {offset})"
