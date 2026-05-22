def create_object(
    scene_name: str = "Scene",
    object_name: str = "FluidGradientCapsules",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = None,  # Not used directly; we use a curated 4-color palette
    **kwargs,
) -> str:
    """
    Create a staggered array of rounded capsules with a procedural fluid gradient.
    """
    import bpy
    import bmesh
    import random
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Configuration
    columns = kwargs.get('columns', 8)
    spacing = kwargs.get('spacing', 1.05)
    bend_strength = kwargs.get('bend_strength', 1.5)
    
    # Colors (Yellow, Purple, Bright Blue, Deep Blue)
    c1 = (1.0, 0.8, 0.0, 1.0)
    c2 = (0.5, 0.0, 0.8, 1.0)
    c3 = (0.0, 0.5, 1.0, 1.0)
    c4 = (0.0, 0.0, 0.1, 1.0)

    # === Step 1: Create the Base Capsule Mesh ===
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(1.0, 1.0, 4.0), verts=bm.verts) # Base height 4
    
    capsule_mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    bm.to_mesh(capsule_mesh)
    bm.free()

    # === Step 2: Build the Procedural Fluid Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_GradientMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create Shader Nodes
    node_geom = nodes.new(type='ShaderNodeNewGeometry')
    node_sep_pos = nodes.new(type='ShaderNodeSeparateXYZ')
    node_sep_norm = nodes.new(type='ShaderNodeSeparateXYZ')
    
    node_abs = nodes.new(type='ShaderNodeMath')
    node_abs.operation = 'ABSOLUTE'
    
    node_mult = nodes.new(type='ShaderNodeMath')
    node_mult.operation = 'MULTIPLY'
    node_mult.inputs[1].default_value = bend_strength
    
    node_sub = nodes.new(type='ShaderNodeMath')
    node_sub.operation = 'SUBTRACT'
    
    node_map = nodes.new(type='ShaderNodeMapRange')
    node_map.inputs[1].default_value = -4.0 # From Min
    node_map.inputs[2].default_value = 4.0  # From Max
    
    node_ramp = nodes.new(type='ShaderNodeValToRGB')
    node_ramp.color_ramp.interpolation = 'B_SPLINE'
    node_ramp.color_ramp.elements[0].position = 0.0
    node_ramp.color_ramp.elements[0].color = c1
    node_ramp.color_ramp.elements[1].position = 0.33
    node_ramp.color_ramp.elements[1].color = c2
    node_ramp.color_ramp.elements.new(0.66)
    node_ramp.color_ramp.elements[2].color = c3
    node_ramp.color_ramp.elements.new(1.0)
    node_ramp.color_ramp.elements[3].color = c4
    
    node_emission = nodes.new(type='ShaderNodeEmission')
    node_emission.inputs['Strength'].default_value = 2.0
    
    node_output = nodes.new(type='ShaderNodeOutputMaterial')

    # Link the Node Tree
    links.new(node_geom.outputs['Position'], node_sep_pos.inputs['Vector'])
    links.new(node_geom.outputs['Normal'], node_sep_norm.inputs['Vector'])
    
    links.new(node_sep_norm.outputs['X'], node_abs.inputs[0])
    links.new(node_abs.outputs['Value'], node_mult.inputs[0])
    
    links.new(node_sep_pos.outputs['Z'], node_sub.inputs[0])
    links.new(node_mult.outputs['Value'], node_sub.inputs[1])
    
    links.new(node_sub.outputs['Value'], node_map.inputs['Value'])
    links.new(node_map.outputs['Result'], node_ramp.inputs['Fac'])
    links.new(node_ramp.outputs['Color'], node_emission.inputs['Color'])
    links.new(node_emission.outputs['Emission'], node_output.inputs['Surface'])

    # === Step 3: Build the Glass Material ===
    glass_mat = bpy.data.materials.new(name=f"{object_name}_GlassMat")
    glass_mat.use_nodes = True
    glass_mat.use_screen_refraction = True # For EEVEE compatibility
    glass_nodes = glass_mat.node_tree.nodes
    glass_bsdf = glass_nodes.get("Principled BSDF")
    if glass_bsdf:
        glass_bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
        glass_bsdf.inputs['Roughness'].default_value = 0.05
        # Handle Blender 4.0+ vs older versions for Transmission
        if 'Transmission Weight' in glass_bsdf.inputs:
            glass_bsdf.inputs['Transmission Weight'].default_value = 1.0
        elif 'Transmission' in glass_bsdf.inputs:
            glass_bsdf.inputs['Transmission'].default_value = 1.0

    # === Step 4: Construct the Scene Assembly ===
    master_empty = bpy.data.objects.new(object_name, None)
    master_empty.location = Vector(location)
    master_empty.scale = (scale, scale, scale)
    scene.collection.objects.link(master_empty)
    
    capsules_created = 0
    random.seed(42) # Consistent generation
    
    total_width = (columns - 1) * spacing
    start_x = -total_width / 2.0

    for col in range(columns):
        x_pos = start_x + (col * spacing)
        # Random staggered height for the intersecting cut
        intersection_z = random.uniform(-1.5, 1.5)
        
        # Create Top and Bottom capsules for this column
        for is_top in [True, False]:
            z_offset = 2.0 if is_top else -2.0
            z_pos = intersection_z + z_offset
            
            cap = bpy.data.objects.new(f"{object_name}_Capsule_{col}_{'Top' if is_top else 'Bot'}", capsule_mesh)
            cap.location = (x_pos, 0, z_pos)
            cap.parent = master_empty
            cap.data.materials.append(mat)
            
            # Add Bevel Modifier for perfect rounding
            mod = cap.modifiers.new(name="Rounding", type='BEVEL')
            mod.width = 0.499 # Just under 0.5 to prevent degenerate geometry
            mod.segments = 16
            mod.use_clamp_overlap = True
            
            # Smooth shading
            for poly in cap.data.polygons:
                poly.use_smooth = True
                
            scene.collection.objects.link(cap)
            capsules_created += 1

    # === Step 5: Add Floating Glass Overlays ===
    for i in range(3):
        glass_cap = bpy.data.objects.new(f"{object_name}_Glass_{i}", capsule_mesh)
        
        # Random placement in front of the main capsules
        gx = start_x + random.randint(0, columns-1) * spacing
        gy = -0.6 - random.uniform(0.1, 0.4) # Push forward towards camera
        gz = random.uniform(-2, 2)
        
        glass_cap.location = (gx, gy, gz)
        glass_cap.scale = (0.9, 0.1, random.uniform(1.0, 1.5)) # Flatter, varying height
        glass_cap.parent = master_empty
        glass_cap.data.materials.append(glass_mat)
        
        g_mod = glass_cap.modifiers.new(name="Rounding", type='BEVEL')
        g_mod.width = 0.499
        g_mod.segments = 16
        g_mod.use_clamp_overlap = True
        
        for poly in glass_cap.data.polygons:
            poly.use_smooth = True
            
        scene.collection.objects.link(glass_cap)
        capsules_created += 1

    return f"Created '{object_name}' with {capsules_created} procedural capsules and glass overlays at {location}."
