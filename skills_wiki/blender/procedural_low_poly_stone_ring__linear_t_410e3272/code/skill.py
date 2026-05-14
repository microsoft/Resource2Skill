def create_low_poly_well_base(
    scene_name: str = "Scene",
    object_name: str = "LowPolyWellBase",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    base_color: tuple = (0.5, 0.5, 0.5),
    num_layers: int = 4,
    stones_per_layer: int = 14,
    radius: float = 1.5,
    **kwargs
) -> str:
    """
    Create a stylized low-poly circular stone base using a linear-to-radial procedural stack.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        base_color: (R, G, B) average color for the stones.
        num_layers: How many rings of stone to stack vertically.
        stones_per_layer: Number of individual stone blocks per ring.
        radius: Inner radius of the well base.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Procedural Stone Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_StoneMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs['Roughness'].default_value = 0.9
    bsdf.inputs['Specular IOR Level'].default_value = 0.1
    
    geo_node = nodes.new("ShaderNodeNewGeometry")
    geo_node.location = (-600, 0)
    
    ramp_node = nodes.new("ShaderNodeValToRGB")
    ramp_node.location = (-300, 0)
    
    # Configure ColorRamp for varied stone colors
    ramp_node.color_ramp.elements[0].position = 0.0
    ramp_node.color_ramp.elements[0].color = (base_color[0]*0.9, base_color[1]*0.9, base_color[2]*0.9, 1.0)
    
    ramp_node.color_ramp.elements[1].position = 1.0
    ramp_node.color_ramp.elements[1].color = (base_color[0]*1.1, base_color[1]*1.1, base_color[2]*1.2, 1.0) # slight blue/cool tint
    
    elem_mid = ramp_node.color_ramp.elements.new(0.5)
    elem_mid.color = (base_color[0]*1.15, base_color[1]*1.0, base_color[2]*0.9, 1.0) # slight warm tint
    
    links.new(geo_node.outputs['Random Per Island'], ramp_node.inputs['Fac'])
    links.new(ramp_node.outputs['Color'], bsdf.inputs['Base Color'])

    # === Step 2: Create Displacement Texture ===
    tex_name = f"{object_name}_WobbleTex"
    tex = bpy.data.textures.get(tex_name)
    if not tex:
        tex = bpy.data.textures.new(tex_name, type='CLOUDS')
        tex.noise_scale = 0.6
        tex.noise_depth = 2

    # === Step 3: Create Master Parent Empty ===
    empty = bpy.data.objects.new(object_name, None)
    empty.location = Vector(location)
    empty.scale = (scale, scale, scale)
    scene.collection.objects.link(empty)

    # === Step 4: Generate Layers ===
    stone_height = 0.35
    
    for layer in range(num_layers):
        circumference = 2 * math.pi * radius
        stone_length = circumference / stones_per_layer
        
        bm = bmesh.new()
        
        # Build stones in a flat line centered on the origin
        for i in range(stones_per_layer):
            # Randomize dimensions
            sx = stone_length * random.uniform(0.85, 0.92) # 0.85-0.92 leaves organic gaps
            sy = random.uniform(0.35, 0.45) # Wall thickness
            sz = stone_height * random.uniform(0.8, 1.1)
            
            # Position along X axis
            cx = -circumference/2 + (i * stone_length) + (stone_length / 2.0)
            
            ret = bmesh.ops.create_cube(bm, size=1.0)
            verts = ret['verts']
            
            bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=verts)
            bmesh.ops.translate(bm, vec=(cx, 0, 0), verts=verts)
            
        mesh = bpy.data.meshes.new(f"{object_name}_Layer_{layer}")
        bm.to_mesh(mesh)
        bm.free()
        
        # Shade Flat for the low-poly look
        for p in mesh.polygons:
            p.use_smooth = False
            
        obj = bpy.data.objects.new(f"{object_name}_Layer_{layer}", mesh)
        obj.data.materials.append(mat)
        scene.collection.objects.link(obj)
        obj.parent = empty
        
        # --- Apply the "Stylized Low Poly" Modifier Stack ---
        
        # 1. Bevel: Separate the blocks slightly
        mod_bevel = obj.modifiers.new("Bevel", 'BEVEL')
        mod_bevel.width = 0.02
        mod_bevel.segments = 2
        
        # 2. Subdiv: Add geometry without smoothing silhouette
        mod_subdiv = obj.modifiers.new("Subdiv", 'SUBSURF')
        mod_subdiv.subdivision_type = 'SIMPLE'
        mod_subdiv.levels = 2
        mod_subdiv.render_levels = 2
        
        # 3. Displace: Add organic wobbly irregularity
        mod_displace = obj.modifiers.new("Displace", 'DISPLACE')
        mod_displace.texture = tex
        mod_displace.strength = 0.12
        
        # 4. Bend: Wrap the line into a circle
        mod_bend = obj.modifiers.new("Bend", 'SIMPLE_DEFORM')
        mod_bend.deform_method = 'BEND'
        mod_bend.deform_axis = 'Z'
        mod_bend.angle = 2 * math.pi
        
        # 5. Decimate: Destroy the grid topology for stylized triangles
        mod_decimate = obj.modifiers.new("Decimate", 'DECIMATE')
        mod_decimate.ratio = 0.35
        
        # Position and transform layer
        obj.location.z = layer * (stone_height * 0.9) # overlap layers slightly
        obj.rotation_euler.z = random.uniform(0, 2 * math.pi) # stagger stone joints
        
        # Taper the well slightly as it goes up
        layer_scale = 1.0 - (layer * 0.03)
        obj.scale = (layer_scale, layer_scale, 1.0)

    return f"Created '{object_name}' with {num_layers} layers and {num_layers * stones_per_layer} total stones at {location}."
