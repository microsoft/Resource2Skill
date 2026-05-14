def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedEye",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.05, 0.35, 0.8),  # Default blue iris
    **kwargs,
) -> str:
    """
    Create a Stylized Procedural Eye (Double-Sphere) in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the iris in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    # Ensure we are in object mode
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # ==========================================
    # 1. Create Materials
    # ==========================================
    
    # --- Inner Eye Material (Procedural Iris) ---
    mat_inner = bpy.data.materials.new(name=f"{object_name}_Inner_Mat")
    mat_inner.use_nodes = True
    nodes_in = mat_inner.node_tree.nodes
    links_in = mat_inner.node_tree.links
    bsdf_inner = nodes_in.get("Principled BSDF")
    bsdf_inner.inputs.get("Roughness").default_value = 0.5 # Soft inner eye
    
    # Setup Procedural Projection Nodes
    tex_coord = nodes_in.new('ShaderNodeTexCoord')
    sep_xyz = nodes_in.new('ShaderNodeSeparateXYZ')
    comb_xyz = nodes_in.new('ShaderNodeCombineXYZ')
    vec_len = nodes_in.new('ShaderNodeVectorMath')
    vec_len.operation = 'LENGTH'
    
    ramp = nodes_in.new('ShaderNodeValToRGB')
    ramp.color_ramp.interpolation = 'EASE'
    
    mask_greater = nodes_in.new('ShaderNodeMath')
    mask_greater.operation = 'GREATER_THAN'
    mask_greater.inputs[1].default_value = 0.0 # Mask for Front Side (+Y)
    
    mix_front_back = nodes_in.new('ShaderNodeMixRGB')
    mix_front_back.inputs[1].default_value = (1.0, 1.0, 1.0, 1.0) # Back Color (White Sclera)
    
    # Configure Color Ramp (Pupil -> Iris -> Limbal -> Sclera)
    cr = ramp.color_ramp
    cr.elements[0].position = 0.12
    cr.elements[0].color = (0.01, 0.01, 0.01, 1.0) # Pupil
    
    cr.elements[1].position = 0.42
    cr.elements[1].color = (1.0, 1.0, 1.0, 1.0) # Sclera
    
    e1 = cr.elements.new(0.15)
    e1.color = (material_color[0], material_color[1], material_color[2], 1.0) # Inner Iris
    
    e2 = cr.elements.new(0.35)
    e2.color = (material_color[0] * 0.4, material_color[1] * 0.4, material_color[2] * 0.4, 1.0) # Outer Iris (Darker)
    
    e3 = cr.elements.new(0.38)
    e3.color = (0.02, 0.02, 0.02, 1.0) # Limbal Ring
    
    # Connect Inner Material Nodes
    links_in.new(tex_coord.outputs['Object'], sep_xyz.inputs['Vector'])
    links_in.new(sep_xyz.outputs['X'], comb_xyz.inputs[0]) # Map X to X
    links_in.new(sep_xyz.outputs['Z'], comb_xyz.inputs[1]) # Map Z to Y
    links_in.new(sep_xyz.outputs['Y'], mask_greater.inputs[0]) # Use Y to isolate front facing half
    
    links_in.new(comb_xyz.outputs['Vector'], vec_len.inputs[0])
    links_in.new(vec_len.outputs['Value'], ramp.inputs['Fac'])
    
    links_in.new(mask_greater.outputs['Value'], mix_front_back.inputs['Fac'])
    links_in.new(ramp.outputs['Color'], mix_front_back.inputs[2]) # Front Color
    
    links_in.new(mix_front_back.outputs['Color'], bsdf_inner.inputs.get("Base Color"))

    # --- Outer Eye Material (Glass Cornea) ---
    mat_outer = bpy.data.materials.new(name=f"{object_name}_Outer_Mat")
    mat_outer.use_nodes = True
    bsdf_outer = mat_outer.node_tree.nodes.get("Principled BSDF")
    
    # Handle API differences for Transmission across Blender versions
    if 'Transmission Weight' in bsdf_outer.inputs:
        bsdf_outer.inputs['Transmission Weight'].default_value = 1.0
    elif 'Transmission' in bsdf_outer.inputs:
        bsdf_outer.inputs['Transmission'].default_value = 1.0
        
    bsdf_outer.inputs['Roughness'].default_value = 0.0
    bsdf_outer.inputs['IOR'].default_value = 1.45
    
    # Crucial for EEVEE: Allow light to pass through to the inner sphere
    mat_outer.blend_method = 'HASHED'
    mat_outer.shadow_method = 'NONE'
    mat_outer.use_screen_refraction = True

    # ==========================================
    # 2. Create Geometry & Hierarchy
    # ==========================================
    
    # Create Root Controller (Empty)
    bpy.ops.object.empty_add(type='ARROWS', radius=1.2)
    rig_empty = bpy.context.active_object
    rig_empty.name = object_name
    rig_empty.location = Vector(location)
    rig_empty.scale = (scale, scale, scale)

    # Create Inner Sphere
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.0)
    inner_sphere = bpy.context.active_object
    inner_sphere.name = f"{object_name}_Inner"
    bpy.ops.object.shade_smooth()
    inner_sphere.data.materials.append(mat_inner)
    
    # Create Outer Sphere (Slightly larger)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.02)
    outer_sphere = bpy.context.active_object
    outer_sphere.name = f"{object_name}_Cornea"
    bpy.ops.object.shade_smooth()
    outer_sphere.data.materials.append(mat_outer)

    # Setup Parenting
    inner_sphere.parent = rig_empty
    outer_sphere.parent = rig_empty
    
    # Ensure they sit at the rig's origin
    inner_sphere.location = (0, 0, 0)
    outer_sphere.location = (0, 0, 0)

    # Deselect all and select the rig
    bpy.ops.object.select_all(action='DESELECT')
    rig_empty.select_set(True)
    bpy.context.view_layer.objects.active = rig_empty

    return f"Created Stylized Eye Rig '{object_name}' at {location}. The pupil looks down the +Y axis."
