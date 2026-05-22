def create_remeshed_hardsurface_part(
    scene_name: str = "Scene",
    object_name: str = "SciFi_Block",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.25, 0.3),
    voxel_size: float = 0.02,
    smooth_iterations: int = 40,
    **kwargs
) -> str:
    """
    Create a complex non-destructive hard surface part using the Voxel Remesh + Smooth workflow.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created main object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color.
        voxel_size: Resolution of the remesh (lower = higher poly, more precise).
        smooth_iterations: How heavily to smooth the voxelized edges into bevels.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_cube_add(size=2.0)
    base_obj = bpy.context.active_object
    base_obj.name = object_name
    base_obj.location = Vector(location)
    base_obj.scale = (scale * 1.0, scale * 0.5, scale * 0.5)
    
    # Create a dedicated collection for boolean cutters to keep the outliner clean
    cutter_coll_name = f"{object_name}_Cutters"
    if cutter_coll_name not in bpy.data.collections:
        cutter_coll = bpy.data.collections.new(cutter_coll_name)
        scene.collection.children.link(cutter_coll)
    else:
        cutter_coll = bpy.data.collections[cutter_coll_name]
        
    # Prevent cutters from showing up in final renders
    cutter_coll.hide_render = True
    
    # === Step 2: Create Non-Destructive Cutters ===
    cutters = []
    
    # Cutter 1: Main cylindrical cutout through the side
    bpy.ops.mesh.primitive_cylinder_add(radius=0.3*scale, depth=2.5*scale, location=location)
    c1 = bpy.context.active_object
    c1.name = f"{object_name}_Cutter_Cyl"
    c1.rotation_euler = (math.pi / 2, 0, 0)  # Align to Y axis
    cutters.append(c1)
    
    # Cutter 2: Rectangular notch on the top surface
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    c2 = bpy.context.active_object
    c2.name = f"{object_name}_Cutter_Notch"
    c2.scale = (scale * 0.4, scale * 0.6, scale * 0.4)
    c2.location = (location[0], location[1], location[2] + (scale * 0.4))
    cutters.append(c2)
    
    # Cutter 3: Angled chamfer cut on the corner
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    c3 = bpy.context.active_object
    c3.name = f"{object_name}_Cutter_Chamfer"
    c3.scale = (scale * 0.5, scale * 0.5, scale * 0.5)
    c3.location = (location[0] + (scale * 0.8), location[1], location[2] + (scale * 0.3))
    c3.rotation_euler = (0, math.pi / 4, 0)  # Rotate 45 degrees
    cutters.append(c3)
    
    # Link cutters to correct collection and apply boolean modifiers to the base
    for c in cutters:
        c.display_type = 'BOUNDS'
        c.hide_render = True
        
        # Unlink from default collections and link to cutter collection
        for coll in list(c.users_collection):
            coll.objects.unlink(c)
        cutter_coll.objects.link(c)
        
        # Add boolean modifier
        bool_mod = base_obj.modifiers.new(name=f"Bool_{c.name}", type='BOOLEAN')
        bool_mod.operation = 'DIFFERENCE'
        bool_mod.object = c
        bool_mod.solver = 'EXACT'

    # === Step 3: Apply the Remesh + Corrective Smooth Workflow ===
    
    # 3A. Voxel Remesh (converts n-gons to dense, uniform voxel topology)
    remesh_mod = base_obj.modifiers.new(name="Voxel_Remesh", type='REMESH')
    remesh_mod.mode = 'VOXEL'
    # Scale the voxel size dynamically so scaling the object doesn't cause infinite calculation
    remesh_mod.voxel_size = voxel_size * scale
    remesh_mod.use_smooth_shade = True
    
    # 3B. Corrective Smooth (melts the jagged voxel steps into perfect bevels)
    smooth_mod = base_obj.modifiers.new(name="Smooth_Corrective", type='CORRECTIVE_SMOOTH')
    smooth_mod.use_only_smooth = True
    smooth_mod.iterations = smooth_iterations
    smooth_mod.factor = 0.5
    
    # Ensure the base object is smooth shaded to match the modifiers
    for poly in base_obj.data.polygons:
        poly.use_smooth = True
        
    # === Step 4: Material & Shading ===
    mat_name = f"{object_name}_Metal_Mat"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (material_color[0], material_color[1], material_color[2], 1.0)
            bsdf.inputs["Metallic"].default_value = 0.8
            bsdf.inputs["Roughness"].default_value = 0.35
            
    if len(base_obj.data.materials) == 0:
        base_obj.data.materials.append(mat)
    else:
        base_obj.data.materials[0] = mat
        
    return f"Created '{object_name}' with {len(cutters)} procedural Boolean cutters and Remesh bevels at {location}"
