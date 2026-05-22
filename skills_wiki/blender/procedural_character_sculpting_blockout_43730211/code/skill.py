def create_object(
    scene_name: str = "Scene",
    object_name: str = "SculptBase",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.6, 0.5),
    **kwargs,
) -> str:
    """
    Create Procedural Character Sculpting Blockout in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the character hierarchy.
        location: (x, y, z) world-space position for the character root.
        scale: Uniform scale factor (1.0 = standard 1.8m character).
        material_color: Base clay color.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Ensure we are in Object mode
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # === Step 1: Create Root Control ===
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = object_name

    # === Step 2: Build Sculpt Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Clay")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.85
        bsdf.inputs['Specular IOR Level'].default_value = 0.2

    # === Step 3: Blockout Generation Helper ===
    def create_block(name, loc, size, rot=(0,0,0), mirror=False):
        bpy.ops.mesh.primitive_cube_add(size=2)
        obj = bpy.context.active_object
        obj.name = f"{object_name}_{name}"
        obj.location = loc
        obj.scale = size
        obj.rotation_euler = rot
        
        # Subsurf for organic rounding
        mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
        mod.levels = 2
        mod.render_levels = 2
        
        bpy.ops.object.shade_smooth()
        
        # Mirror setup
        if mirror:
            mmod = obj.modifiers.new(name="Mirror", type='MIRROR')
            mmod.mirror_object = root
            mmod.use_axis[0] = True
            
        obj.data.materials.append(mat)
        obj.parent = root
        return obj

    parts_count = 0

    # === Step 4: Center Line Anatomy (Torso & Head) ===
    create_block("Pelvis", (0, 0, 0.95), (0.16, 0.11, 0.13))
    create_block("Chest", (0, 0, 1.3), (0.15, 0.1, 0.18))
    create_block("Neck", (0, -0.02, 1.52), (0.04, 0.04, 0.06))
    create_block("Head", (0, -0.02, 1.7), (0.1, 0.12, 0.13))
    parts_count += 4

    # === Step 5: Mirrored Anatomy (Left side generated, mirrored to Right) ===
    # Legs (-Y is considered the 'Front' of the character based on head offset)
    create_block("Thigh", (0.09, 0, 0.65), (0.07, 0.07, 0.22), mirror=True) 
    create_block("Calf", (0.09, -0.02, 0.25), (0.06, 0.06, 0.2), mirror=True)
    create_block("Foot", (0.09, -0.08, 0.03), (0.05, 0.12, 0.03), mirror=True)

    # Arms (A-Pose: rotated slightly forward and heavily down)
    create_block("UpperArm", (0.25, 0, 1.25), (0.05, 0.05, 0.15), rot=(0, -0.5, 0), mirror=True)
    create_block("Forearm", (0.39, 0, 1.0), (0.04, 0.04, 0.14), rot=(0, -0.5, 0), mirror=True)
    create_block("Hand", (0.48, 0, 0.82), (0.02, 0.05, 0.06), rot=(0, -0.5, 0), mirror=True)

    # Torso Details (Pecs/Breasts, Glutes, Ears)
    create_block("ChestVolume", (0.08, -0.1, 1.35), (0.07, 0.04, 0.07), rot=(0.2, 0.2, 0), mirror=True)
    create_block("Glute", (0.08, 0.1, 0.95), (0.08, 0.08, 0.1), rot=(-0.2, 0, 0), mirror=True)
    create_block("Ear", (0.1, -0.02, 1.7), (0.02, 0.04, 0.05), rot=(0, 0.2, -0.2), mirror=True)
    parts_count += 9

    # === Step 6: Finalize Placement & Scale ===
    # Apply absolute transformations to the root empty. 
    # This safely scales the mirror offsets and subsurf shapes proportionally.
    root.location = Vector(location)
    root.scale = (scale, scale, scale)

    # Deselect all, then select the root
    bpy.ops.object.select_all(action='DESELECT')
    root.select_set(True)
    bpy.context.view_layer.objects.active = root

    return f"Created '{object_name}' blockout base at {location} consisting of {parts_count} volumetric parts."
