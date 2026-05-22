def create_object(
    scene_name: str = "Scene",
    object_name: str = "MachinedPart",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.15, 0.15, 0.15),
    **kwargs,
) -> str:
    """
    Create a procedural hard-surface machined part using Boolean CSG operations.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created main object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the metal material.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Helper function to create cutters and apply boolean modifier
    def add_cutter(target, name, type='CUBE', size=2.0, radius=1.0, depth=2.0, loc=(0,0,0), rot=(0,0,0), scale=(1,1,1)):
        # Create cutter object
        if type == 'CUBE':
            bpy.ops.mesh.primitive_cube_add(size=size, location=loc, rotation=rot)
        elif type == 'CYLINDER':
            bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, vertices=64, location=loc, rotation=rot)
        
        cutter = bpy.context.active_object
        cutter.name = f"{object_name}_Cutter_{name}"
        cutter.scale = scale
        
        # Hide cutter visually
        cutter.display_type = 'WIRE'
        cutter.hide_render = True
        cutter.hide_viewport = True
        
        # Parent to target so they move together
        cutter.parent = target
        
        # Add boolean modifier to target
        mod = target.modifiers.new(name=f"Bool_{name}", type='BOOLEAN')
        mod.operation = 'DIFFERENCE'
        mod.object = cutter
        mod.solver = 'EXACT'
        
        return cutter

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # === Step 1: Create Base Geometry ===
    # High res sphere for smooth curved surfaces after boolean cuts
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.0, location=(0, 0, 0))
    base_obj = bpy.context.active_object
    base_obj.name = object_name
    
    # Smooth shading
    bpy.ops.object.shade_smooth()
    # Enable Auto Smooth for older Blender versions (required for harden_normals)
    try:
        base_obj.data.use_auto_smooth = True
        base_obj.data.auto_smooth_angle = math.radians(60)
    except AttributeError:
        pass # Blender 4.1+ handles this natively via modifiers if needed, but smooth shade is enough here

    # === Step 2: Add Boolean Cutters ===
    cutters = []
    
    # Top and Bottom Flat Cuts
    cutters.append(add_cutter(base_obj, "TopFlat", type='CUBE', size=2.0, loc=(0, 0, 1.7)))
    cutters.append(add_cutter(base_obj, "BotFlat", type='CUBE', size=2.0, loc=(0, 0, -1.7)))
    
    # Left and Right Flat Profile Cuts
    cutters.append(add_cutter(base_obj, "LeftFlat", type='CUBE', size=2.0, loc=(-1.6, 0, 0)))
    cutters.append(add_cutter(base_obj, "RightFlat", type='CUBE', size=2.0, loc=(1.6, 0, 0)))

    # Main Center Hole (Y-axis)
    cutters.append(add_cutter(base_obj, "CenterHole", type='CYLINDER', radius=0.45, depth=4.0, rot=(math.pi/2, 0, 0)))
    
    # Top and Bottom Cylindrical Grooves (Parallel to Y-axis)
    cutters.append(add_cutter(base_obj, "TopGroove", type='CYLINDER', radius=0.5, depth=4.0, loc=(0, 0, 0.85), rot=(math.pi/2, 0, 0)))
    cutters.append(add_cutter(base_obj, "BotGroove", type='CYLINDER', radius=0.5, depth=4.0, loc=(0, 0, -0.85), rot=(math.pi/2, 0, 0)))
    
    # Small Detail Notches on Front/Back Faces
    cutters.append(add_cutter(base_obj, "NotchFrontTop", type='CUBE', size=1.0, loc=(0, -0.9, 0.6), scale=(0.4, 0.5, 0.3)))
    cutters.append(add_cutter(base_obj, "NotchFrontBot", type='CUBE', size=1.0, loc=(0, -0.9, -0.6), scale=(0.4, 0.5, 0.3)))
    cutters.append(add_cutter(base_obj, "NotchBackTop", type='CUBE', size=1.0, loc=(0, 0.9, 0.6), scale=(0.4, 0.5, 0.3)))
    cutters.append(add_cutter(base_obj, "NotchBackBot", type='CUBE', size=1.0, loc=(0, 0.9, -0.6), scale=(0.4, 0.5, 0.3)))

    # Thin Panel Line / Slot Cut
    cutters.append(add_cutter(base_obj, "PanelLine", type='CUBE', size=2.0, scale=(1.2, 1.2, 0.02)))

    # === Step 3: Add Shading & Edge Catching Modifiers ===
    # Bevel modifier to catch light on sharp boolean edges
    bevel_mod = base_obj.modifiers.new(name="MachiningBevel", type='BEVEL')
    bevel_mod.limit_method = 'ANGLE'
    bevel_mod.angle_limit = math.radians(30)
    bevel_mod.width = 0.015
    bevel_mod.segments = 3
    bevel_mod.harden_normals = True
    bevel_mod.profile = 0.5

    # Weighted Normal to fix n-gon shading distortions on curved surfaces
    wn_mod = base_obj.modifiers.new(name="FixShading", type='WEIGHTED_NORMAL')
    wn_mod.keep_sharp = True

    # === Step 4: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.85
        bsdf.inputs['Roughness'].default_value = 0.3
    
    if len(base_obj.data.materials) == 0:
        base_obj.data.materials.append(mat)
    else:
        base_obj.data.materials[0] = mat

    # === Step 5: Position & Scale ===
    base_obj.location = Vector(location)
    base_obj.scale = (scale, scale, scale)
    
    # Link cutters to the same collection as the base object
    current_collection = base_obj.users_collection[0]
    for c in cutters:
        if c.name not in current_collection.objects:
            current_collection.objects.link(c)
            # Unlink from scene collection if accidentally linked there
            if c.name in scene.collection.objects:
                scene.collection.objects.unlink(c)

    return f"Created procedural hard-surface object '{object_name}' at {location} utilizing {len(cutters)} CSG boolean cutters."
