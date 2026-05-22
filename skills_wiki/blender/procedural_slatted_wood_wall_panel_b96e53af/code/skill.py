def create_slatted_wall_panel(
    scene_name: str = "Scene",
    object_name: str = "SlattedWallPanel",
    location: tuple = (0.0, 0.0, 0.0),
    rotation: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    width: float = 2.0,
    height: float = 2.6,
    slat_width: float = 0.04,
    slat_depth: float = 0.02,
    gap_width: float = 0.02,
    wood_color: tuple = (0.5, 0.25, 0.1),
    backing_color: tuple = (0.03, 0.03, 0.03),
    **kwargs
) -> str:
    """
    Creates a procedural, architectural slatted wood wall panel.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: World-space base location (bottom center of the panel).
        rotation: Euler rotation in radians.
        scale: Uniform scale multiplier.
        width: Total width of the wall panel.
        height: Total height of the slats.
        slat_width: Width of each individual wooden slat.
        slat_depth: How far the slat extrudes from the backing.
        gap_width: Space between each slat.
        wood_color: Base RGB color for the procedural wood grain.
        backing_color: Dark RGB color for the recessed backboard.
        
    Returns:
        Status string describing the generated object.
    """
    import bpy
    from mathutils import Euler

    # Create root Empty for clean hierarchy management
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    root = bpy.context.active_object
    root.name = object_name
    root.rotation_euler = Euler(rotation)
    root.scale = (scale, scale, scale)

    # === Step 1: Create Backboard ===
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    backboard = bpy.context.active_object
    backboard.name = f"{object_name}_Backing"
    # Dimensions: X=width, Y=0.02 (thickness), Z=height
    backboard.scale = (width, 0.02, height)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    backboard.parent = root
    # Move so origin is at the bottom edge
    backboard.location = (0, 0, height / 2.0)

    # === Step 2: Create Base Slat ===
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    slat = bpy.context.active_object
    slat.name = f"{object_name}_Slat"
    slat.scale = (slat_width, slat_depth, height)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    slat.parent = backboard
    
    # Calculate Array Math to perfectly center the slats on the board
    count = int((width - slat_width) / (slat_width + gap_width)) + 1
    total_array_width = (count * slat_width) + ((count - 1) * gap_width)
    start_x = -total_array_width / 2.0 + slat_width / 2.0
    
    # Position first slat (offset Y slightly so it sits in front of the backing)
    slat.location = (start_x, 0.01 + slat_depth / 2.0, 0)
    
    # Setup Array Modifier
    mod_array = slat.modifiers.new(name="Array", type='ARRAY')
    mod_array.use_relative_offset = False
    mod_array.use_constant_offset = True
    mod_array.constant_offset_displace = (slat_width + gap_width, 0, 0)
    mod_array.count = count

    # Setup Bevel Modifier (Chamfer) for specular edge catching
    mod_bevel = slat.modifiers.new(name="Bevel", type='BEVEL')
    mod_bevel.width = min(slat_width, slat_depth) * 0.15
    mod_bevel.segments = 1 # Flat chamfer looks great for wood strips

    # === Step 3: Material Creation ===
    
    # Backing Material
    mat_backing = bpy.data.materials.new(name=f"{object_name}_BackingMat")
    mat_backing.use_nodes = True
    bsdf_backing = mat_backing.node_tree.nodes.get("Principled BSDF")
    if bsdf_backing:
        bsdf_backing.inputs['Base Color'].default_value = (*backing_color, 1.0)
        bsdf_backing.inputs['Roughness'].default_value = 0.95
    backboard.data.materials.append(mat_backing)

    # Procedural Wood Material
    mat_wood = bpy.data.materials.new(name=f"{object_name}_WoodMat")
    mat_wood.use_nodes = True
    nodes = mat_wood.node_tree.nodes
    links = mat_wood.node_tree.links
    
    bsdf_wood = nodes.get("Principled BSDF")
    if bsdf_wood:
        bsdf_wood.inputs['Roughness'].default_value = 0.35
        
        # Procedural Grain Shader Graph
        tex_coord = nodes.new('ShaderNodeTexCoord')
        tex_coord.location = (-1000, 0)
        
        mapping = nodes.new('ShaderNodeMapping')
        mapping.location = (-800, 0)
        # Stretch texture vertically by squashing the Z coordinate
        mapping.inputs['Scale'].default_value = (1.0, 1.0, 0.05)
        # Add slight rotation to break perfect alignment
        mapping.inputs['Rotation'].default_value = (0.0, 0.0, 0.03)
        
        noise = nodes.new('ShaderNodeTexNoise')
        noise.location = (-600, 0)
        noise.inputs['Scale'].default_value = 4.0
        noise.inputs['Detail'].default_value = 8.0
        noise.inputs['Distortion'].default_value = 0.3
        
        color_ramp = nodes.new('ShaderNodeValToRGB')
        color_ramp.location = (-300, 0)
        color_ramp.color_ramp.elements[0].position = 0.3
        color_ramp.color_ramp.elements[0].color = (*wood_color, 1.0)
        
        # Calculate darker wood shade for grain contrast
        dark_wood = (wood_color[0] * 0.4, wood_color[1] * 0.4, wood_color[2] * 0.4, 1.0)
        color_ramp.color_ramp.elements[1].position = 0.8
        color_ramp.color_ramp.elements[1].color = dark_wood
        
        links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
        links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
        links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], bsdf_wood.inputs['Base Color'])
        
    slat.data.materials.append(mat_wood)

    return f"Created Slatted Wall Panel '{object_name}' with {count} procedural slats at {location}."
