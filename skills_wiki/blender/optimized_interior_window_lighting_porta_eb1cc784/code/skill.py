def create_optimized_window_setup(
    scene_name: str = "Scene",
    object_name: str = "OptimizedWindow",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    glass_color: tuple = (1.0, 1.0, 1.0, 1.0),
    curtain_color: tuple = (0.8, 0.8, 0.75, 1.0),
    window_width: float = 2.0,
    window_height: float = 3.0,
    **kwargs,
) -> str:
    """
    Creates an optimized window setup for interior rendering, including shadowless
    glass, translucent wave curtains, and an environment light portal.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created object hierarchy.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        glass_color: RGBA color for the glass tint.
        curtain_color: RGBA color for the fabric.
        window_width: Width of the window/portal in meters.
        window_height: Height of the window/portal in meters.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Calculate scaled dimensions
    w = window_width * scale
    h = window_height * scale
    loc = Vector(location)
    
    # === Step 1: Create Parent Hierarchy ===
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=loc)
    parent_obj = bpy.context.active_object
    parent_obj.name = object_name
    
    # === Step 2: Create Optimized Glass Material ===
    glass_mat = bpy.data.materials.new(name=f"{object_name}_OptimizedGlass")
    glass_mat.use_nodes = True
    nodes = glass_mat.node_tree.nodes
    links = glass_mat.node_tree.links
    nodes.clear()
    
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (300, 0)
    
    mix_node = nodes.new(type='ShaderNodeMixShader')
    mix_node.location = (100, 0)
    
    glass_node = nodes.new(type='ShaderNodeBsdfGlass')
    glass_node.location = (-100, 100)
    glass_node.inputs['Color'].default_value = glass_color
    
    transp_node = nodes.new(type='ShaderNodeBsdfTransparent')
    transp_node.location = (-100, -100)
    transp_node.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0) # Pure white lets all light pass
    
    lp_node = nodes.new(type='ShaderNodeLightPath')
    lp_node.location = (-100, 300)
    
    # Connect nodes: If 'Is Shadow Ray', use Transparent (Input 2), else use Glass (Input 1)
    links.new(glass_node.outputs['BSDF'], mix_node.inputs[1])
    links.new(transp_node.outputs['BSDF'], mix_node.inputs[2])
    links.new(lp_node.outputs['Is Shadow Ray'], mix_node.inputs[0])
    links.new(mix_node.outputs['Shader'], out_node.inputs['Surface'])
    
    # === Step 3: Create Glass Mesh ===
    bpy.ops.mesh.primitive_plane_add(size=1)
    glass_obj = bpy.context.active_object
    glass_obj.name = f"{object_name}_Glass"
    glass_obj.scale = (w, h, 1.0)
    glass_obj.rotation_euler[0] = math.radians(90) # Stand upright, normal faces +Y
    glass_obj.location = loc
    glass_obj.parent = parent_obj
    glass_obj.data.materials.append(glass_mat)
    
    # === Step 4: Create Optimized Curtain Material ===
    curtain_mat = bpy.data.materials.new(name=f"{object_name}_OptimizedCurtain")
    curtain_mat.use_nodes = True
    nodes = curtain_mat.node_tree.nodes
    links = curtain_mat.node_tree.links
    nodes.clear()
    
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (500, 0)
    
    mix_node = nodes.new(type='ShaderNodeMixShader')
    mix_node.location = (300, 0)
    
    add_node = nodes.new(type='ShaderNodeAddShader')
    add_node.location = (100, 100)
    
    diff_node = nodes.new(type='ShaderNodeBsdfDiffuse')
    diff_node.location = (-100, 200)
    diff_node.inputs['Color'].default_value = curtain_color
    
    transl_node = nodes.new(type='ShaderNodeBsdfTranslucent')
    transl_node.location = (-100, 50)
    transl_node.inputs['Color'].default_value = curtain_color
    
    transp_node2 = nodes.new(type='ShaderNodeBsdfTransparent')
    transp_node2.location = (100, -100)
    transp_node2.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
    
    lp_node2 = nodes.new(type='ShaderNodeLightPath')
    lp_node2.location = (100, 300)
    
    # Connect nodes: Mix Diffuse + Translucent, then bypass shadows with Transparent
    links.new(diff_node.outputs['BSDF'], add_node.inputs[0])
    links.new(transl_node.outputs['BSDF'], add_node.inputs[1])
    links.new(add_node.outputs['Shader'], mix_node.inputs[1])
    links.new(transp_node2.outputs['BSDF'], mix_node.inputs[2])
    links.new(lp_node2.outputs['Is Shadow Ray'], mix_node.inputs[0])
    links.new(mix_node.outputs['Shader'], out_node.inputs['Surface'])
    
    # === Step 5: Create Curtain Mesh ===
    bpy.ops.mesh.primitive_plane_add(size=1)
    curtain_obj = bpy.context.active_object
    curtain_obj.name = f"{object_name}_Curtain"
    curtain_obj.scale = (w * 1.2, h * 1.1, 1.0) # Slightly larger than window
    curtain_obj.rotation_euler[0] = math.radians(90)
    
    # Place curtain slightly "inside" the room (assuming room is in +Y direction)
    curtain_obj.location = loc + Vector((0.0, 0.2 * scale, 0.0))
    curtain_obj.parent = parent_obj
    curtain_obj.data.materials.append(curtain_mat)
    
    # Procedural wavy folds
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=25)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()
    
    wave_mod = curtain_obj.modifiers.new(name="FabricFolds", type='WAVE')
    wave_mod.use_x = True
    wave_mod.use_y = False
    wave_mod.height = 0.06 * scale
    wave_mod.width = 0.25 * scale
    
    # === Step 6: Create Area Light (Portal) ===
    bpy.ops.object.light_add(type='AREA', radius=1, location=loc)
    portal_obj = bpy.context.active_object
    portal_obj.name = f"{object_name}_LightPortal"
    portal_obj.data.shape = 'RECTANGLE'
    portal_obj.data.size = w
    portal_obj.data.size_y = h
    
    # Enable portal logic (requires Cycles)
    if hasattr(portal_obj.data, "cycles"):
        portal_obj.data.cycles.is_portal = True 
    else:
        # Fallback for newer blender versions where it might be structured differently
        try:
            portal_obj.data.use_portal = True
        except AttributeError:
            pass
            
    # Rotate pointing inward (+Y). Area lights default to pointing -Z.
    portal_obj.rotation_euler[0] = math.radians(90)
    
    # Place portal slightly "outside" the glass
    portal_obj.location = loc + Vector((0.0, -0.1 * scale, 0.0))
    portal_obj.parent = parent_obj

    # === Step 7: Apply Recommended Render Settings (Additive/Safe) ===
    if scene.render.engine == 'CYCLES':
        scene.cycles.sample_clamping_indirect = 10.0
        if scene.cycles.transparent_max_bounces < 24:
            scene.cycles.transparent_max_bounces = 24
            
    # Deselect all, set parent as active
    bpy.ops.object.select_all(action='DESELECT')
    parent_obj.select_set(True)
    bpy.context.view_layer.objects.active = parent_obj
    
    return f"Created '{object_name}' (Optimized Window setup) at {location} with {len(parent_obj.children)} children."
