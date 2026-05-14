def create_retopology_setup(
    scene_name: str = "Scene",
    object_name: str = "Retopo_Mesh",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.0, 0.8, 0.8),
    **kwargs,
) -> str:
    """
    Creates a dedicated retopology workspace, including a starter mesh with correct 
    modifiers (Mirror, Shrinkwrap), viewport display settings, and global snapping rules.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the low-poly retopology mesh.
        location: World-space position for the setup.
        scale: Scale multiplier.
        material_color: Viewport display color for the retopo mesh (R, G, B).
        **kwargs: 
            target_name (str): Name of the high-poly object to retopologize. 
                               If it doesn't exist, a procedural sculpt is generated.

    Returns:
        Status string describing the created setup.
    """
    import bpy
    import bmesh
    import math
    import mathutils
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Step 1: Identify or Create High-Poly Target ---
    target_name = kwargs.get("target_name", "HighPoly_Target")
    target_obj = bpy.data.objects.get(target_name)

    if not target_obj:
        # Generate a lumpy sphere as a stand-in high-poly sculpt
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5, radius=2 * scale, location=location)
        target_obj = bpy.context.active_object
        target_obj.name = target_name
        
        # Add procedural displacement for organic lumpiness
        disp_mod = target_obj.modifiers.new(name="Displacement", type='DISPLACE')
        tex = bpy.data.textures.new(name="LumpyTex", type='CLOUDS')
        tex.noise_scale = 1.0
        tex.noise_depth = 2
        disp_mod.texture = tex
        disp_mod.strength = 0.5 * scale
        
        # Enable smooth shading
        for poly in target_obj.data.polygons:
            poly.use_smooth = True

    # --- Step 2: Create Retopology Starter Mesh ---
    mesh = bpy.data.meshes.new(object_name + "_Data")
    retopo_obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(retopo_obj)

    # Create a single quad facing forward to start the topology
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5 * scale)
    
    # Rotate 90 degrees on X to stand it up (facing -Y)
    rot_matrix = mathutils.Matrix.Rotation(math.radians(90), 3, 'X')
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0,0,0), matrix=rot_matrix)
    
    # Move it to the front surface of the target volume
    bmesh.ops.translate(bm, vec=(0, -2 * scale, 0), verts=bm.verts)
    
    bm.to_mesh(mesh)
    bm.free()

    retopo_obj.location = Vector(location)

    # --- Step 3: Setup Modifier Stack ---
    # 1. Mirror (for symmetrical edge flow)
    mirror_mod = retopo_obj.modifiers.new(name="Mirror", type='MIRROR')
    mirror_mod.use_clip = True
    mirror_mod.use_axis[0] = True # X-axis symmetry

    # 2. Shrinkwrap (to ensure vertices stick to the target)
    shrink_mod = retopo_obj.modifiers.new(name="Shrinkwrap", type='SHRINKWRAP')
    shrink_mod.target = target_obj
    shrink_mod.wrap_method = 'NEAREST_SURFACEPOINT'
    shrink_mod.wrap_mode = 'ON_SURFACE'
    shrink_mod.offset = 0.02 * scale # Slight offset prevents Z-fighting in viewport

    # --- Step 4: Viewport & Material Settings ---
    retopo_obj.show_in_front = True
    retopo_obj.show_wire = True
    retopo_obj.display_type = 'SOLID'

    # Create a distinct material for visibility
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.diffuse_color = (*material_color, 1.0) # Viewport color
    mat.use_nodes = True
    # Update node color as well
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
    
    retopo_obj.data.materials.append(mat)

    # --- Step 5: Global Scene Snapping Settings ---
    scene.tool_settings.use_snap = True
    scene.tool_settings.snap_elements = {'FACE'}
    scene.tool_settings.snap_target = 'CLOSEST'
    scene.tool_settings.use_snap_project = True # Critical: 'Project Individual Elements'
    scene.tool_settings.use_snap_translate = True
    scene.tool_settings.use_snap_rotate = True
    scene.tool_settings.use_snap_scale = True

    # --- Step 6: Finalize ---
    # Make the retopo mesh active so the user can Tab directly into Edit mode
    bpy.context.view_layer.objects.active = retopo_obj
    retopo_obj.select_set(True)
    if target_obj.name != target_name:
        target_obj.select_set(False)

    return f"Created retopology workspace at {location}. Target: '{target_obj.name}', Retopo Mesh: '{object_name}'"
