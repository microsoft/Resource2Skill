def create_lowpoly_stone_base(
    scene_name: str = "Scene",
    object_name: str = "WellBase",
    location: tuple = (0, 0, 0),
    radius: float = 1.2,
    scale: float = 1.0,
    base_color: tuple = (0.5, 0.45, 0.48),
    **kwargs,
) -> str:
    """
    Create a procedural low-poly stone well base using the Build Flat -> Bend -> Decimate workflow.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        radius: Base radius of the well.
        scale: Uniform scale factor.
        base_color: (R, G, B) primary color of the stones.
        **kwargs: Additional optional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import random
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Procedural Parameters
    layers = kwargs.get("layers", 3)
    stones_per_layer = kwargs.get("stones_per_layer", 14)
    
    circumference = 2 * math.pi * radius
    stone_len = circumference / stones_per_layer
    stone_depth = stone_len * 0.6
    stone_height = stone_len * 0.4

    # === Step 1: Generate Linear Stone Array via BMesh ===
    bm = bmesh.new()
    
    for layer in range(layers):
        # Offset every other layer by half a brick for interlocking pattern
        offset_x = (layer % 2) * (stone_len / 2.0)
        
        # Shift higher layers slightly inward (-Y) to create a subtle conical well shape
        y_offset = -layer * (stone_depth * 0.15)
        
        for i in range(stones_per_layer):
            ret = bmesh.ops.create_cube(bm, size=1.0)
            verts = ret['verts']
            
            # Randomize individual stone dimensions slightly
            sl = stone_len * random.uniform(0.9, 1.1)
            sd = stone_depth * random.uniform(0.8, 1.2)
            sh = stone_height * random.uniform(0.8, 1.2)
            
            bmesh.ops.scale(bm, vec=Vector((sl, sd, sh)), verts=verts)
            
            # Calculate linear position
            x_pos = -circumference / 2.0 + (i * stone_len) + offset_x
            # Wrap around bounds to ensure consistent bounding box for bending
            if x_pos >= circumference / 2.0:
                x_pos -= circumference
                
            z_pos = layer * stone_height
            
            bmesh.ops.translate(bm, vec=Vector((x_pos, y_offset, z_pos)), verts=verts)

    mesh = bpy.data.meshes.new(object_name)
    bm.to_mesh(mesh)
    bm.free()
    
    # Ensure smooth shading is off for low-poly look (Decimate will also enforce this)
    mesh.polygons.foreach_set('use_smooth', [False] * len(mesh.polygons))

    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # === Step 2: Apply Procedural Modifier Stack ===
    
    # 1. Bevel: round the blocky cube edges
    bevel = obj.modifiers.new("Bevel", 'BEVEL')
    bevel.segments = 2
    bevel.width = 0.04
    
    # 2. Subsurf: add geometry so displacement and bending are smooth
    subsurf = obj.modifiers.new("Subsurf", 'SUBSURF')
    subsurf.levels = 1
    subsurf.render_levels = 1
    
    # 3. Displace: add hand-sculpted wobble
    tex_name = "WobbleTex_" + object_name
    tex = bpy.data.textures.get(tex_name)
    if not tex:
        tex = bpy.data.textures.new(tex_name, type='CLOUDS')
        tex.noise_scale = 0.5
    
    disp = obj.modifiers.new("Wobble", 'DISPLACE')
    disp.texture = tex
    disp.strength = 0.08
    
    # 4. Bend: Wrap the linear wall into a 360 ring
    bend = obj.modifiers.new("Bend", 'SIMPLE_DEFORM')
    bend.deform_method = 'BEND'
    bend.angle = 2 * math.pi
    bend.deform_axis = 'Z'
    
    # 5. Decimate: Create the faceted, low-poly chiseled aesthetic
    dec = obj.modifiers.new("Faceted", 'DECIMATE')
    dec.ratio = 0.35

    # === Step 3: Material & Shading ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs['Roughness'].default_value = 0.95
    
    # Assign varied colors to each disconnected stone island
    geo_node = nodes.new("ShaderNodeNewGeometry")
    geo_node.location = (-600, 0)
    
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (-300, 0)
    ramp.color_ramp.elements[0].color = (*base_color, 1.0)
    
    # Calculate a slightly darker, contrasting stone color
    var_color = (
        max(0.0, base_color[0] - 0.15), 
        max(0.0, base_color[1] - 0.12), 
        max(0.0, base_color[2] - 0.08), 
        1.0
    )
    ramp.color_ramp.elements[1].color = var_color
    
    links.new(geo_node.outputs['Random Per Island'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    
    obj.data.materials.append(mat)

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created low-poly ring '{object_name}' at {location} with {layers} layers ({layers * stones_per_layer} stones)."
