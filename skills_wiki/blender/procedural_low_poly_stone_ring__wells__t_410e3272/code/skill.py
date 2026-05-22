def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyWellBase",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.4, 0.38, 0.45), # Cool purplish-gray stone
    **kwargs,
) -> str:
    """
    Create a Procedural Low-Poly Stone Ring (Well Base) in the active Blender scene.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position for the assembly.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Overrides for 'radius', 'num_stones', 'height', 'depth', 'layers'.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector
    
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # 1. Create Parent Empty to hold the assembly
    parent_obj = bpy.data.objects.new(object_name, None)
    parent_obj.empty_display_type = 'ARROWS'
    parent_obj.empty_display_size = 1.0
    parent_obj.location = location
    parent_obj.scale = (scale, scale, scale)
    scene.collection.objects.link(parent_obj)
    
    # 2. Build the Material
    mat = bpy.data.materials.new(name=f"{object_name}_StoneMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.8
        bsdf.inputs['Specular IOR Level'].default_value = 0.1
        
    # 3. Build Procedural Global Noise Texture (for variation)
    tex_name = f"{object_name}_Clouds"
    tex = bpy.data.textures.get(tex_name)
    if not tex:
        tex = bpy.data.textures.new(tex_name, 'CLOUDS')
        tex.noise_scale = 1.5
        
    # Parameters
    radius = kwargs.get('radius', 1.2)
    num_stones = kwargs.get('num_stones', 14)
    height = kwargs.get('height', 0.25)
    depth = kwargs.get('depth', 0.4)
    gap_ratio = kwargs.get('gap_ratio', 0.05)
    layers = kwargs.get('layers', 3)
    
    created_objects = []
    
    # 4. Generate Layers procedurally
    for layer in range(layers):
        current_radius = radius * (1.0 - layer * 0.05) # Slight taper upwards
        L = 2 * math.pi * current_radius # Total circumference
        stone_step = L / num_stones
        stone_width = stone_step * (1.0 - gap_ratio)
        
        # BMesh: Create stones in a mathematically perfect straight line centered on X=0
        bm = bmesh.new()
        for i in range(num_stones):
            # Calculate position so the entire array is centered from -L/2 to +L/2
            x_pos = -L/2 + (i + 0.5) * stone_step
            
            cube_data = bmesh.ops.create_cube(bm, size=1.0)
            
            # Scale and translate vertices natively to preserve (1,1,1) object scale
            for v in cube_data['verts']:
                v.co.x = (v.co.x * stone_width) + x_pos
                v.co.y = (v.co.y * depth)
                v.co.z = (v.co.z * height)
                
        mesh = bpy.data.meshes.new(f"{object_name}_Ring_{layer}")
        bm.to_mesh(mesh)
        bm.free()
        
        # Instantiate object
        obj = bpy.data.objects.new(f"{object_name}_Ring_{layer}", mesh)
        scene.collection.objects.link(obj)
        obj.parent = parent_obj
        obj.data.materials.append(mat)
        
        # Stack vertically
        obj.location.z = layer * height
        # Rotate on Z to create interlocked masonry patterns
        obj.rotation_euler.z = layer * (math.pi / num_stones)
        
        # --- Procedural Modifier Stack ---
        
        # A. Soften hard mathematical edges
        bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
        bevel.width = 0.03
        bevel.segments = 2
        
        # B. Add geometry required for organic bending and displacement
        subdiv = obj.modifiers.new(name="Subdiv", type='SUBSURF')
        subdiv.subdivision_type = 'SIMPLE'
        subdiv.levels = 3
        
        # C. Wobble vertices globally (Replaces manual "Randomize")
        displace = obj.modifiers.new(name="Displace", type='DISPLACE')
        displace.texture = tex
        displace.strength = 0.05
        displace.texture_coords = 'GLOBAL'
        
        # D. Wrap the straight array into a perfect circle
        bend = obj.modifiers.new(name="Bend", type='SIMPLE_DEFORM')
        bend.deform_method = 'BEND'
        bend.angle = 2 * math.pi # 360 degrees
        bend.deform_axis = 'Z'
        
        # E. Collapse smooth geometry into stylized chunky polygons
        decimate = obj.modifiers.new(name="Decimate", type='DECIMATE')
        decimate.decimate_type = 'COLLAPSE'
        decimate.ratio = 0.25
        
        # Ensure flat shading for the faceted low-poly look
        for poly in obj.data.polygons:
            poly.use_smooth = False
            
        created_objects.append(obj.name)
        
    return f"Created '{object_name}' with {layers} layers (Objects: {', '.join(created_objects)})"
