def create_low_poly_dungeon_archway(
    scene_name: str = "Scene",
    object_name: str = "DungeonArchway",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    main_color: tuple = (0.3, 0.35, 0.4), # Darker grey for stone
    highlight_color: tuple = (0.4, 0.45, 0.5), # Lighter grey for arch blocks
    roughness: float = 0.8,
    bevel_segments: int = 1,
    bevel_amount: float = 0.02,
    arch_width: float = 2.0,
    arch_height: float = 2.5,
    wall_thickness: float = 0.5,
    pillar_height: float = 1.5,
    num_arch_segments: int = 5,
    **kwargs,
) -> str:
    """
    Create a stylized low-poly dungeon archway in the active Blender scene.

    The archway is constructed from simple cube primitives, suitable for game development.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created archway object (will be parent).
        location: (x, y, z) world-space position for the parent object.
        scale: Uniform scale factor for the entire archway.
        main_color: (R, G, B) base color for the main wall sections in 0-1 range.
        highlight_color: (R, G, B) color for the individual arch blocks in 0-1 range.
        roughness: Material roughness value (0-1).
        bevel_segments: Number of segments for the bevel modifier (0 for no bevel).
        bevel_amount: Amount for the bevel modifier.
        arch_width: Total width of the arch opening.
        arch_height: Height of the arch opening.
        wall_thickness: Thickness of the wall.
        pillar_height: Height of the vertical pillars supporting the arch.
        num_arch_segments: Number of blocks making up one half of the arch curve.
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'DungeonArchway' at (0, 0, 0) with 1 parent object and N children."
    """
    import bpy
    import mathutils
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Create a collection for the archway
    if object_name not in bpy.data.collections:
        arch_collection = bpy.data.collections.new(object_name)
        scene.collection.children.link(arch_collection)
    else:
        arch_collection = bpy.data.collections[object_name]

    # --- Materials ---
    # Main Stone Material
    main_mat_name = f"{object_name}_MainStone"
    if main_mat_name not in bpy.data.materials:
        main_mat = bpy.data.materials.new(name=main_mat_name)
        main_mat.use_nodes = True
        bsdf = main_mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*main_color, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
    else:
        main_mat = bpy.data.materials[main_mat_name]

    # Arch Highlight Material
    highlight_mat_name = f"{object_name}_ArchStone"
    if highlight_mat_name not in bpy.data.materials:
        highlight_mat = bpy.data.materials.new(name=highlight_mat_name)
        highlight_mat.use_nodes = True
        bsdf = highlight_mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*highlight_color, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
    else:
        highlight_mat = bpy.data.materials[highlight_mat_name]

    # --- Parent Object ---
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    parent_obj = bpy.context.object
    parent_obj.name = object_name
    parent_obj.empty_display_size = 0.5 * scale # Adjust visibility
    parent_obj.scale = (scale, scale, scale)

    created_objects = []

    # --- Create Wall Segments ---
    # Side Wall 1 (left)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        enter_editmode=False,
        align='WORLD',
        location=(-(arch_width / 2 + wall_thickness / 2), 0, pillar_height / 2),
    )
    wall1 = bpy.context.object
    wall1.name = f"{object_name}_WallLeft"
    wall1.scale = (wall_thickness, wall_thickness, pillar_height)
    wall1.data.materials.append(main_mat)
    created_objects.append(wall1)

    # Side Wall 2 (right)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        enter_editmode=False,
        align='WORLD',
        location=(arch_width / 2 + wall_thickness / 2, 0, pillar_height / 2),
    )
    wall2 = bpy.context.object
    wall2.name = f"{object_name}_WallRight"
    wall2.scale = (wall_thickness, wall_thickness, pillar_height)
    wall2.data.materials.append(main_mat)
    created_objects.append(wall2)

    # Top Wall (lintel)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        enter_editmode=False,
        align='WORLD',
        location=(0, 0, pillar_height + arch_height / 2),
    )
    top_wall = bpy.context.object
    top_wall.name = f"{object_name}_WallTop"
    top_wall.scale = (arch_width + 2 * wall_thickness, wall_thickness, arch_height)
    top_wall.data.materials.append(main_mat)
    created_objects.append(top_wall)

    # --- Create Arch Blocks ---
    # Arch base position and radius
    arch_center_z = pillar_height
    arch_radius = arch_width / 2

    # Angle step for segments
    angle_step = (math.pi / 2) / num_arch_segments # Quarter circle for one side

    for i in range(num_arch_segments):
        angle = angle_step * i
        block_size = arch_radius * math.sin(angle_step) * 1.1 # Adjust for spacing

        # Left side arch block
        x_pos_left = -arch_width / 2 + arch_radius * math.cos(angle + angle_step / 2)
        z_pos_left = arch_center_z + arch_radius * math.sin(angle + angle_step / 2)
        
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            enter_editmode=False,
            align='WORLD',
            location=(x_pos_left, 0, z_pos_left),
        )
        arch_block_left = bpy.context.object
        arch_block_left.name = f"{object_name}_ArchBlockL_{i+1}"
        
        # Scale block to be slightly trapezoidal or just rectangular
        # For low poly, simple scaling works. We'll use local Y as thickness for simplicity.
        arch_block_left.scale = (block_size, wall_thickness, block_size)
        
        # Rotate to align with arch curve (tangent to arc)
        # Use +math.pi for rotation towards center from left side
        arch_block_left.rotation_euler[1] = angle + (math.pi / 2) # Rotate on Y for thickness, then around Y for orientation
        arch_block_left.data.materials.append(highlight_mat)
        created_objects.append(arch_block_left)

        # Right side arch block (mirroring left)
        x_pos_right = arch_width / 2 - arch_radius * math.cos(angle + angle_step / 2)
        z_pos_right = arch_center_z + arch_radius * math.sin(angle + angle_step / 2)

        bpy.ops.mesh.primitive_cube_add(
            size=1,
            enter_editmode=False,
            align='WORLD',
            location=(x_pos_right, 0, z_pos_right),
        )
        arch_block_right = bpy.context.object
        arch_block_right.name = f"{object_name}_ArchBlockR_{i+1}"
        arch_block_right.scale = (block_size, wall_thickness, block_size)
        arch_block_right.rotation_euler[1] = -(angle + (math.pi / 2)) # Mirror rotation
        arch_block_right.data.materials.append(highlight_mat)
        created_objects.append(arch_block_right)

    # --- Apply Bevel Modifier (Optional, for slightly smoother low-poly) ---
    if bevel_segments > 0 and bevel_amount > 0:
        for obj in created_objects:
            # Check if bevel modifier already exists to avoid duplicates
            if "Bevel" not in obj.modifiers:
                bevel_mod = obj.modifiers.new(name="Bevel", type='BEVEL')
                bevel_mod.segments = bevel_segments
                bevel_mod.width = bevel_amount
                bevel_mod.limit_method = 'NONE' # Apply to all edges
            
            # Apply bevel to top wall to make it solid rather than just a top piece
            if obj == top_wall:
                top_wall.location[2] += (arch_height / 2) - (wall_thickness / 2)
                top_wall.scale = (arch_width + 2 * wall_thickness, wall_thickness, arch_height / 2)
                
                # Now extrude the middle of the top_wall to connect the arches
                bpy.context.view_layer.objects.active = top_wall
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(type='FACE')
                
                # Select top and bottom faces (Y+ and Y- faces)
                bm = mathutils.bmesh.from_edit_mesh(top_wall.data)
                
                faces_to_extrude = []
                for face in bm.faces:
                    # Check if face normal is along Y-axis (or very close)
                    if abs(face.normal.y) > 0.9: 
                        faces_to_extrude.append(face)
                
                # Extrude selected faces to connect the top of the arch
                if faces_to_extrude:
                    extrude_vector = mathutils.Vector((0, wall_thickness, 0)) # Extrude along Y
                    bpy.ops.mesh.extrude_region_move(
                        MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False},
                        TRANSFORM_OT_translate={"value":(0, wall_thickness, 0)}
                    )
                
                mathutils.bmesh.update_edit_mesh(top_wall.data)
                bpy.ops.object.mode_set(mode='OBJECT')

    # --- Parent all created objects ---
    bpy.context.view_layer.objects.active = parent_obj
    for obj in created_objects:
        obj.parent = parent_obj
        obj.matrix_parent_inverse = parent_obj.matrix_world.inverted() # Maintain world transform

    # Set selection for context
    bpy.ops.object.select_all(action='DESELECT')
    parent_obj.select_set(True)
    bpy.context.view_layer.objects.active = parent_obj

    return f"Created '{object_name}' at {location} with {len(created_objects)} child objects."

