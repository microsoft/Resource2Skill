def create_scifi_boolean_paneling(
    scene_name: str = "Scene",
    object_name: str = "SciFi_Core",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.25, 0.3),
    panel_thickness: float = 0.05,
    bevel_width: float = 0.015,
    **kwargs,
) -> str:
    """
    Create a non-destructive sci-fi core with boolean panel cuts and clean bevels.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created base object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the metal shader.
        panel_thickness: Width of the procedural panel cuts.
        bevel_width: Size of the edge highlights on the boolean cuts.

    Returns:
        Status string detailing the created object.
    """
    import bpy
    import math
    from mathutils import Vector

    # Ensure we are in Object mode
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 1. Create Base Object ---
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=scale, location=location)
    base_obj = bpy.context.active_object
    base_obj.name = object_name
    bpy.ops.object.shade_smooth()

    # Backwards compatibility for Auto Smooth (required for older Blender versions to use Harden Normals)
    if hasattr(base_obj.data, "use_auto_smooth"):
        base_obj.data.use_auto_smooth = True
        base_obj.data.auto_smooth_angle = math.radians(60)

    # --- 2. Create Panel Slice Cutter (Plane + Array + Solidify trick) ---
    bpy.ops.mesh.primitive_plane_add(size=scale * 2.5, location=location)
    plane_cutter = bpy.context.active_object
    plane_cutter.name = f"{object_name}_PanelCutter"
    
    # Keep viewport clean, hide from render
    plane_cutter.display_type = 'WIRE'
    plane_cutter.hide_render = True

    mod_array = plane_cutter.modifiers.new(name="Array", type='ARRAY')
    mod_array.count = 5
    mod_array.use_relative_offset = False
    mod_array.use_constant_offset = True
    offset_dist = scale * 0.4
    mod_array.constant_offset_displace = (0, 0, offset_dist)
    
    # Center the stacked array vertically around the base object
    plane_cutter.location.z -= (mod_array.count - 1) * offset_dist / 2.0

    # Solidify turns the 2D planes into 3D cutting volumes
    mod_solid = plane_cutter.modifiers.new(name="Solidify", type='SOLIDIFY')
    mod_solid.thickness = panel_thickness
    mod_solid.offset = 0.0 # Center the cut expansion

    # --- 3. Create Core Hole Cutter (Cylinder) ---
    bpy.ops.mesh.primitive_cylinder_add(radius=scale * 0.4, depth=scale * 3.0, location=location)
    cyl_cutter = bpy.context.active_object
    cyl_cutter.name = f"{object_name}_CylCutter"
    
    # Rotate cylinder to cut horizontally through the Y axis
    cyl_cutter.rotation_euler = (math.radians(90), 0, 0)
    
    cyl_cutter.display_type = 'WIRE'
    cyl_cutter.hide_render = True

    # --- 4. Assemble Modifier Stack on Base Object ---
    # Cut 1: Panel Slices
    mod_bool1 = base_obj.modifiers.new(name="Boolean_Panels", type='BOOLEAN')
    mod_bool1.operation = 'DIFFERENCE'
    mod_bool1.object = plane_cutter
    mod_bool1.solver = 'EXACT'

    # Cut 2: Central Hole
    mod_bool2 = base_obj.modifiers.new(name="Boolean_Hole", type='BOOLEAN')
    mod_bool2.operation = 'DIFFERENCE'
    mod_bool2.object = cyl_cutter
    mod_bool2.solver = 'EXACT'

    # Bevel: Catch edges created by booleans, hardening normals for perfect shading
    mod_bevel = base_obj.modifiers.new(name="Bevel", type='BEVEL')
    mod_bevel.limit_method = 'ANGLE'
    mod_bevel.angle_limit = math.radians(30)
    mod_bevel.width = bevel_width
    mod_bevel.segments = 3
    mod_bevel.harden_normals = True

    # --- 5. Material Setup ---
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Metallic"].default_value = 0.9
        bsdf.inputs["Roughness"].default_value = 0.35
    base_obj.data.materials.append(mat)

    # --- 6. Hierarchy Management ---
    # Parent cutters to the base object so they move together globally, 
    # while maintaining local non-destructive editability
    bpy.ops.object.select_all(action='DESELECT')
    plane_cutter.select_set(True)
    cyl_cutter.select_set(True)
    base_obj.select_set(True)
    bpy.context.view_layer.objects.active = base_obj
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

    # Ensure only the base object is selected at the end
    bpy.ops.object.select_all(action='DESELECT')
    base_obj.select_set(True)
    bpy.context.view_layer.objects.active = base_obj

    return f"Created Non-Destructive Sci-Fi Core '{object_name}' with {mod_array.count} panel slices and 1 central cut."
