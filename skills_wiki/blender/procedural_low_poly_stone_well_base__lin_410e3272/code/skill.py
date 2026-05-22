def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyWellBase",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.55, 0.52, 0.50),
    **kwargs,
) -> str:
    """
    Create a procedural low-poly stone well base using linear-to-circular deformation.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the parent empty object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the stones.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Base Parameters ===
    radius = 1.2
    circumference = 2 * math.pi * radius
    w = 0.35 # Default stone width
    h = 0.25 # Default stone height

    # === Step 2: Create Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_StoneMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.85
        bsdf.inputs['Specular'].default_value = 0.1

    # === Step 3: Generate the Linear Row of Stones ===
    stones = []
    x = -circumference / 2  # Start at the left edge
    
    while x < circumference / 2:
        # Determine random stone length
        l = random.uniform(0.3, 0.7)
        if x + l > circumference / 2:
            l = circumference / 2 - x  # Cap the last stone to exactly fit the circumference
        if l < 0.1:
            break

        # Generate procedural stone via bmesh
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        
        # Scale to random brick dimensions
        stone_l = l * 0.95 # Leave a 5% gap between stones
        stone_w = w * random.uniform(0.85, 1.0)
        stone_h = h * random.uniform(0.85, 1.0)
        bmesh.ops.scale(bm, vec=(stone_l, stone_w, stone_h), verts=bm.verts)

        # Bevel heavily to generate geometric density for the decimate modifier
        bmesh.ops.bevel(bm, geom=bm.edges, offset=min(stone_l, stone_w, stone_h)*0.2, segments=3, profile=0.5)

        # Wobble vertices (Randomize)
        wobble = 0.015
        for v in bm.verts:
            v.co += Vector((
                random.uniform(-wobble, wobble),
                random.uniform(-wobble, wobble),
                random.uniform(-wobble, wobble)
            ))

        # Convert to mesh object
        mesh = bpy.data.meshes.new(f"{object_name}_StoneMesh")
        bm.to_mesh(mesh)
        bm.free()

        obj = bpy.data.objects.new(f"{object_name}_StonePart", mesh)
        obj.data.materials.append(mat)
        scene.collection.objects.link(obj)
        
        # Position the stone along the X axis, resting on the Z plane
        obj.location = (x + l/2, 0, h/2)
        stones.append(obj)

        x += l

    # === Step 4: Join the Row and Prep for Deformation ===
    bpy.ops.object.select_all(action='DESELECT')
    for obj in stones:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = stones[0]
    bpy.ops.object.join()
    base_row = bpy.context.active_object
    base_row.name = f"{object_name}_Tier1"

    # Fix Origin: The Bend modifier requires the origin to be the geometric center (0,0,0)
    saved_cursor = bpy.context.scene.cursor.location.copy()
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.context.scene.cursor.location = saved_cursor

    # === Step 5: Apply Modifiers (Linear to Circular + Stylization) ===
    bend = base_row.modifiers.new(name="Bend", type='SIMPLE_DEFORM')
    bend.deform_method = 'BEND'
    bend.angle = 2 * math.pi  # Wrap 360 degrees
    bend.deform_axis = 'Z'    # Bend the X-axis around the Z-axis

    decimate = base_row.modifiers.new(name="Decimate", type='DECIMATE')
    decimate.ratio = 0.37     # Crunch geometry to create flat, chiseled low-poly facets

    # === Step 6: Create Hierarchy & Tiers ===
    # Create empty parent for global positioning
    parent_empty = bpy.data.objects.new(object_name, None)
    scene.collection.objects.link(parent_empty)
    parent_empty.location = location
    parent_empty.scale = (scale, scale, scale)

    base_row.parent = parent_empty
    tiers = [base_row]

    # Generate Tier 2 and Tier 3
    for i in range(1, 3):
        bpy.ops.object.select_all(action='DESELECT')
        prev_tier = tiers[-1]
        prev_tier.select_set(True)
        bpy.context.view_layer.objects.active = prev_tier

        # Duplicating retains the Bend and Decimate modifiers
        bpy.ops.object.duplicate()
        new_tier = bpy.context.active_object
        new_tier.name = f"{object_name}_Tier{i+1}"
        new_tier.parent = parent_empty

        # Taper the well inwards slightly per level
        taper_factor = 1.0 - (i * 0.08)
        new_tier.scale = (taper_factor, taper_factor, 1.0)
        
        # Move up vertically (slight overlap) and rotate to stagger the bricks
        new_tier.location.z = i * h * 0.95 
        new_tier.rotation_euler.z = i * 0.4 

        tiers.append(new_tier)

    # Cleanup selection
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created procedural low-poly well base '{object_name}' with 3 tiers at {location}."
