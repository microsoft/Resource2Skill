def create_cinematic_interior_lighting(
    scene_name: str = "Scene",
    rig_name: str = "Cinematic_Interior_Rig",
    location_offset: tuple = (0, 0, 0),
    base_scale: float = 1.0,
    **kwargs,
) -> str:
    """
    Creates a comprehensive cinematic interior lighting rig and compositor setup.
    Includes a direct Sun, warm/cool Area fill lights, World Sky, and post-processing (Glare + Vignette).

    Args:
        scene_name: Name of the target scene.
        rig_name: Base name for the generated lighting collection/objects.
        location_offset: (x, y, z) global offset for the entire light rig.
        base_scale: Scale multiplier for the size and spread of the area lights.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created rig.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === 1. Render Engine & Color Management ===
    scene.render.engine = 'CYCLES'
    scene.cycles.use_preview_denoising = True
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'High Contrast'
    
    # === 2. World Environment (Nishita Sky Fallback) ===
    scene.use_nodes = True
    world = scene.world
    if world is None:
        world = bpy.data.worlds.new("Interior_World")
        scene.world = world
    world.use_nodes = True
    w_tree = world.node_tree
    
    # Add sky if not present
    if not any(n.type == 'TEX_SKY' for n in w_tree.nodes):
        bg_node = w_tree.nodes.get("Background")
        if not bg_node:
            bg_node = w_tree.nodes.new("ShaderNodeBackground")
            out_node = w_tree.nodes.new("ShaderNodeOutputWorld")
            w_tree.links.new(bg_node.outputs[0], out_node.inputs[0])
            
        sky_node = w_tree.nodes.new("ShaderNodeTexSky")
        sky_node.sky_type = 'NISHITA'
        sky_node.sun_elevation = math.radians(15) # Low sun for dramatic shadows
        sky_node.sun_rotation = math.radians(45)
        sky_node.sun_intensity = 0.5 # Kept soft to let the specific Scene Sun dominate
        w_tree.links.new(sky_node.outputs['Color'], bg_node.inputs['Color'])

    # Create Collection for Light Rig
    rig_coll = bpy.data.collections.get(rig_name)
    if not rig_coll:
        rig_coll = bpy.data.collections.new(rig_name)
        scene.collection.children.link(rig_coll)

    created_lights = []

    # Helper function to create lights
    def make_light(l_name, l_type, location, rotation, energy, color, size_x=1.0, size_y=None):
        loc = Vector(location) * base_scale + Vector(location_offset)
        light_data = bpy.data.lights.new(name=l_name, type=l_type)
        light_data.energy = energy
        light_data.color = color
        
        if l_type == 'AREA':
            light_data.shape = 'RECTANGLE' if size_y else 'SQUARE'
            light_data.size = size_x * base_scale
            if size_y:
                light_data.size_y = size_y * base_scale
                
        elif l_type == 'SUN':
            light_data.angle = math.radians(11.4) # Soft shadow edge

        light_obj = bpy.data.objects.new(name=l_name, object_data=light_data)
        light_obj.location = loc
        light_obj.rotation_euler = [math.radians(r) for r in rotation]
        
        rig_coll.objects.link(light_obj)
        created_lights.append(light_obj)
        return light_obj

    # === 3. Add Lighting Array ===
    # Direct Sunlight (Angled through hypothetical window)
    make_light(f"{rig_name}_Sun", 'SUN', (-5, -5, 5), (60, 0, -45), 4.0, (1.0, 0.95, 0.9))
    
    # Ceiling Ambient Fill (Large, weak, pointing down)
    make_light(f"{rig_name}_CeilingFill", 'AREA', (0, 0, 2.8), (0, 0, 0), 10.0, (1.0, 0.95, 0.85), size_x=4.0, size_y=0.5)
    
    # Practical Lamp Boost (Warm, medium power, above seating area)
    make_light(f"{rig_name}_LampAccent", 'AREA', (0, 1.5, 2.0), (-45, 0, 0), 15.0, (1.0, 0.8, 0.5), size_x=1.5)
    
    # Shadow Lifter (Cool blue, pointing at dark corners opposite window)
    make_light(f"{rig_name}_ShadowLift_1", 'AREA', (2, -2, 1.0), (0, 90, 45), 4.0, (0.7, 0.85, 1.0), size_x=2.0)
    
    # Floor Fill (Very low power, aiming horizontally to lift deep floor shadows)
    make_light(f"{rig_name}_FloorFill", 'AREA', (0, 0, 0.5), (90, 0, 0), 2.0, (0.8, 0.9, 1.0), size_x=3.0)

    # === 4. Compositor Setup ===
    scene.use_nodes = True
    comp_tree = scene.node_tree
    
    # Find base nodes
    render_layers = comp_tree.nodes.get("Render Layers")
    composite = comp_tree.nodes.get("Composite")
    
    if not render_layers:
        render_layers = comp_tree.nodes.new('CompositorNodeRLayers')
        render_layers.location = (0, 0)
    if not composite:
        composite = comp_tree.nodes.new('CompositorNodeComposite')
        composite.location = (1200, 0)

    # We will safely inject nodes by finding the link between Render Layers and Composite (if it exists)
    # Brightness/Contrast
    bc_node = comp_tree.nodes.new('CompositorNodeBrightContrast')
    bc_node.location = (300, 0)
    bc_node.inputs['Contrast'].default_value = 0.5 # Subtle contrast boost
    
    # Glare Node (Fog Glow)
    glare_node = comp_tree.nodes.new('CompositorNodeGlare')
    glare_node.location = (500, 0)
    glare_node.glare_type = 'FOG_GLOW'
    glare_node.quality = 'HIGH'
    glare_node.mix = -0.1
    
    # Bottom Vignette Masking (Box Mask -> Blur -> Alpha Over)
    box_mask = comp_tree.nodes.new('CompositorNodeBoxMask')
    box_mask.location = (500, -300)
    box_mask.x = 0.5
    box_mask.y = 0.05
    box_mask.width = 1.0
    box_mask.height = 0.15
    
    blur_node = comp_tree.nodes.new('CompositorNodeBlur')
    blur_node.location = (700, -300)
    blur_node.size_x = 100
    blur_node.size_y = 100
    
    # Black color for vignette
    rgb_node = comp_tree.nodes.new('CompositorNodeRGB')
    rgb_node.location = (700, -500)
    rgb_node.outputs[0].default_value = (0.0, 0.0, 0.0, 1.0)
    
    # Mix (Alpha Over)
    alpha_over = comp_tree.nodes.new('CompositorNodeAlphaOver')
    alpha_over.location = (900, 0)
    
    # Connect Compositor tree
    comp_tree.links.new(render_layers.outputs['Image'], bc_node.inputs['Image'])
    comp_tree.links.new(bc_node.outputs['Image'], glare_node.inputs['Image'])
    
    # Vignette path
    comp_tree.links.new(box_mask.outputs['Mask'], blur_node.inputs['Image'])
    comp_tree.links.new(blur_node.outputs['Image'], alpha_over.inputs['Fac'])
    
    comp_tree.links.new(glare_node.outputs['Image'], alpha_over.inputs[1])
    comp_tree.links.new(rgb_node.outputs['Image'], alpha_over.inputs[2])
    
    comp_tree.links.new(alpha_over.outputs['Image'], composite.inputs['Image'])

    return f"Created '{rig_name}' lighting collection with {len(created_lights)} objects, and injected Glare/Vignette post-processing."
