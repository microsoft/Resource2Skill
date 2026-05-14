def create_object(
    scene_name: str = "Scene",
    object_name: str = "SciFi_Panel",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.8, 0.8),
    **kwargs,
) -> str:
    """
    Create a Non-Destructive Sci-Fi Panel using Booleans and Weighted Normals.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the generated sci-fi panel.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: Base color for the exterior hull.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Materials ===
    # Primary Hull Material
    mat_primary = bpy.data.materials.new(name=f"{object_name}_Hull")
    mat_primary.use_nodes = True
    bsdf_p = mat_primary.node_tree.nodes.get("Principled BSDF")
    if bsdf_p:
        bsdf_p.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf_p.inputs["Metallic"].default_value = 0.8
        bsdf_p.inputs["Roughness"].default_value = 0.3
        
    # Secondary Internal Material (Darker)
    mat_secondary = bpy.data.materials.new(name=f"{object_name}_Internals")
    mat_secondary.use_nodes = True
    bsdf_s = mat_secondary.node_tree.nodes.get("Principled BSDF")
    if bsdf_s:
        bsdf_s.inputs["Base Color"].default_value = (0.1, 0.1, 0.12, 1.0)
        bsdf_s.inputs["Metallic"].default_value = 0.9
        bsdf_s.inputs["Roughness"].default_value = 0.4

    # === Step 2: Create Base Geometry ===
    mesh = bpy.data.meshes.new(object_name + "_mesh")
    base_obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(base_obj)
    
    # Use bmesh to create a cube and scale its vertices (keeps object scale at 1.0)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    base_dim = Vector((0.2, 3.0, 2.0)) * scale
    bmesh.ops.scale(bm, vec=base_dim, verts=bm.verts)
    bm.to_mesh(mesh)
    bm.free()
    
    base_obj.location = Vector(location)
    
    # Assign materials to slots so boolean transfer works perfectly
    base_obj.data.materials.append(mat_primary)   # Slot 0
    base_obj.data.materials.append(mat_secondary) # Slot 1
    
    # Smooth shading setup
    for poly in base_obj.data.polygons:
        poly.use_smooth = True
    if hasattr(base_obj.data, "use_auto_smooth"):
        base_obj.data.use_auto_smooth = True
        base_obj.data.auto_smooth_angle = math.radians(60)

    # === Step 3: Create Cutters ===
    cutters = []
    
    def add_cutter(name_suffix, size, loc_offset, rot=(0,0,0)):
        c_mesh = bpy.data.meshes.new(object_name + name_suffix)
        c_obj = bpy.data.objects.new(object_name + name_suffix, c_mesh)
        scene.collection.objects.link(c_obj)
        
        c_bm = bmesh.new()
        bmesh.ops.create_cube(c_bm, size=1.0)
        c_dim = Vector(size) * scale
        bmesh.ops.scale(c_bm, vec=c_dim, verts=c_bm.verts)
        c_bm.to_mesh(c_mesh)
        c_bm.free()
        
        c_obj.location = Vector(location) + (Vector(loc_offset) * scale)
        c_obj.rotation_euler = rot
        
        c_obj.display_type = 'WIRE'
        c_obj.hide_render = True
        c_obj.parent = base_obj
        
        # Assign secondary material to cutter so it transfers via Boolean
        c_obj.data.materials.append(mat_secondary)
        cutters.append(c_obj)
        return c_obj

    # Cutter 1: Main inner hole (with rounded corners via Bevel modifier)
    c1 = add_cutter("_cut_inner", (0.5, 1.6, 1.0), (0.0, 0.2, -0.2))
    c1_bev = c1.modifiers.new(name="Bevel", type='BEVEL')
    c1_bev.limit_method = 'ANGLE'
    c1_bev.width = 0.2 * scale
    c1_bev.segments = 6
    
    # Cutter 2: Front bottom chamfer (45 degrees)
    c2 = add_cutter("_cut_front", (0.5, 1.5, 1.5), (0.0, -1.6, -1.0), (math.radians(45), 0, 0))
    
    # Cutter 3: Back top chamfer (echoing the 45 degree angle)
    c3 = add_cutter("_cut_back", (0.5, 1.0, 1.0), (0.0, 1.6, 1.0), (math.radians(45), 0, 0))
    
    # Cutter 4: Panel line slice horizontally
    c4 = add_cutter("_cut_slice", (0.6, 3.5, 0.03), (0.0, 0.0, 0.4))
    
    # Cutter 5: Small technical notch
    c5 = add_cutter("_cut_notch", (0.5, 0.3, 0.3), (0.0, -1.5, 0.2))

    # === Step 4: Apply Modifiers to Base ===
    # 1. Booleans
    for i, cutter in enumerate(cutters):
        bool_mod = base_obj.modifiers.new(name=f"Bool_{i}", type='BOOLEAN')
        bool_mod.operation = 'DIFFERENCE'
        bool_mod.object = cutter
        bool_mod.solver = 'EXACT'

    # 2. Bevel for edge highlights
    bev_mod = base_obj.modifiers.new(name="Bevel_Highlights", type='BEVEL')
    bev_mod.limit_method = 'ANGLE'
    bev_mod.angle_limit = math.radians(30)
    bev_mod.width = 0.02 * scale
    bev_mod.segments = 3
    bev_mod.profile = 0.5
    bev_mod.harden_normals = True
    
    # 3. Triangulate to handle Ngons
    tri_mod = base_obj.modifiers.new(name="Triangulate", type='TRIANGULATE')
    tri_mod.keep_custom_normals = True
    
    # 4. Weighted Normal to perfectly flatten shading
    wn_mod = base_obj.modifiers.new(name="WeightedNormal", type='WEIGHTED_NORMAL')
    wn_mod.keep_sharp = True

    return f"Created '{object_name}' at {location} with {len(cutters)} live boolean cutters applying material transfer."
