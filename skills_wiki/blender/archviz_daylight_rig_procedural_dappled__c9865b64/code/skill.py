def create_object(
    scene_name: str = "Scene",
    object_name: str = "ArchViz_Daylight_Rig",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.3, 0.3, 0.3),
    **kwargs,
) -> str:
    """
    Create an ArchViz Daylight Rig with a wide-angle camera, dual-sky lighting, 
    procedural dappled shadows (Gobo), and thick glass material.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the rig collection and objects.
        location: (x, y, z) world-space center of the staging area.
        scale: Uniform scale factor.
        material_color: (R, G, B) color used for the staging ground plane.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    scene.render.engine = 'CYCLES' # Required for volume absorption and proper sky
    
    # === 1. Create Rig Collection ===
    rig_col = bpy.data.collections.new(object_name)
    scene.collection.children.link(rig_col)
    
    # Helper function to assign objects to our specific collection
    def link_to_rig(obj):
        for coll in obj.users_collection:
            coll.objects.unlink(obj)
        rig_col.objects.link(obj)
    
    # === 2. World Shader Setup (Dual Nishita Sky) ===
    world = scene.world
    if not world:
        world = bpy.data.worlds.new(f"{object_name}_World")
        scene.world = world
    
    world.use_nodes = True
    tree = world.node_tree
    tree.nodes.clear()
    
    node_bg_light = tree.nodes.new(type='ShaderNodeBackground')
    node_bg_cam = tree.nodes.new(type='ShaderNodeBackground')
    
    node_sky = tree.nodes.new(type='ShaderNodeTexSky')
    node_sky.sky_type = 'NISHITA'
    node_sky.sun_elevation = math.radians(25)
    node_sky.sun_rotation = math.radians(135)
    node_sky.sun_intensity = 1.0
    node_sky.ozone = 5.0 # Adds richer atmospheric blue
    
    node_hsv = tree.nodes.new(type='ShaderNodeHueSaturation')
    node_hsv.inputs['Saturation'].default_value = 1.2
    node_hsv.inputs['Value'].default_value = 0.8
    
    node_mix = tree.nodes.new(type='ShaderNodeMixShader')
    node_light_path = tree.nodes.new(type='ShaderNodeLightPath')
    node_output = tree.nodes.new(type='ShaderNodeOutputWorld')
    
    # Layout Nodes
    node_sky.location = (-400, 0)
    node_hsv.location = (-200, -100)
    node_bg_light.location = (0, 100)
    node_bg_cam.location = (0, -100)
    node_light_path.location = (0, 300)
    node_mix.location = (200, 0)
    node_output.location = (400, 0)
    
    # Wiring
    tree.links.new(node_sky.outputs['Color'], node_bg_light.inputs['Color'])
    tree.links.new(node_sky.outputs['Color'], node_hsv.inputs['Color'])
    tree.links.new(node_hsv.outputs['Color'], node_bg_cam.inputs['Color'])
    
    # Mix: Fac=0 -> Light (Input 1), Fac=1 -> Camera (Input 2)
    tree.links.new(node_bg_light.outputs['Background'], node_mix.inputs[1])
    tree.links.new(node_bg_cam.outputs['Background'], node_mix.inputs[2])
    tree.links.new(node_light_path.outputs['Is Camera Ray'], node_mix.inputs[0])
    tree.links.new(node_mix.outputs['Shader'], node_output.inputs['Surface'])
    
    # === 3. ArchViz Camera Setup ===
    cam_data = bpy.data.cameras.new(f"{object_name}_CamData")
    cam_data.lens = 22 # Wide angle for architecture
    cam_obj = bpy.data.objects.new(f"{object_name}_Cam", cam_data)
    rig_col.objects.link(cam_obj)
    
    # Position camera back, and at 1.6m eye level
    cam_obj.location = Vector(location) + Vector((0, -15 * scale, 1.6 * scale))
    cam_obj.rotation_euler = (math.radians(90), 0, 0)
    scene.camera = cam_obj # Set as active camera
    
    # === 4. Procedural Gobo (Dappled Shadow Caster) ===
    bpy.ops.mesh.primitive_plane_add(size=40 * scale, location=Vector(location) + Vector((5 * scale, -5 * scale, 15 * scale)))
    gobo = bpy.context.active_object
    gobo.name = f"{object_name}_Gobo"
    link_to_rig(gobo)
    
    # Hide from camera so we only see its shadows
    gobo.visible_camera = False 
    
    mat_gobo = bpy.data.materials.new(f"{object_name}_GoboMat")
    mat_gobo.use_nodes = True
    mat_gobo.blend_method = 'CLIP'
    mtree = mat_gobo.node_tree
    
    noise = mtree.nodes.new(type='ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 2.0 / scale
    noise.inputs['Detail'].default_value = 4.0
    
    colorramp = mtree.nodes.new(type='ShaderNodeValToRGB')
    colorramp.color_ramp.elements[0].position = 0.4
    colorramp.color_ramp.elements[1].position = 0.55
    colorramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    colorramp.color_ramp.elements[1].color = (1, 1, 1, 1)
    
    mtree.links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    
    pbsdf_gobo = mtree.nodes.get("Principled BSDF")
    if pbsdf_gobo and "Alpha" in pbsdf_gobo.inputs:
        mtree.links.new(colorramp.outputs['Color'], pbsdf_gobo.inputs['Alpha'])
    
    gobo.data.materials.append(mat_gobo)
    
    # === 5. Thick Architectural Glass Material (Reusable) ===
    mat_glass = bpy.data.materials.new(f"{object_name}_ThickGlass")
    mat_glass.use_nodes = True
    gtree = mat_glass.node_tree
    pbsdf_glass = gtree.nodes.get("Principled BSDF")
    
    # Handle Blender 4.x vs <4.0 API
    if "Transmission Weight" in pbsdf_glass.inputs:
        pbsdf_glass.inputs["Transmission Weight"].default_value = 1.0
    elif "Transmission" in pbsdf_glass.inputs:
        pbsdf_glass.inputs["Transmission"].default_value = 1.0
        
    pbsdf_glass.inputs["Roughness"].default_value = 0.0
    pbsdf_glass.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0)
    
    vol_abs = gtree.nodes.new(type='ShaderNodeVolumeAbsorption')
    vol_abs.inputs['Color'].default_value = (0.5, 0.8, 0.9, 1.0) # Cyan physical tint
    vol_abs.inputs['Density'].default_value = 2.0 / scale
    
    gtree.links.new(vol_abs.outputs['Volume'], gtree.nodes["Material Output"].inputs['Volume'])
    
    # === 6. Dummy Staging Ground ===
    bpy.ops.mesh.primitive_plane_add(size=50 * scale, location=location)
    ground = bpy.context.active_object
    ground.name = f"{object_name}_Ground"
    link_to_rig(ground)
    
    mat_ground = bpy.data.materials.new(f"{object_name}_GroundMat")
    mat_ground.use_nodes = True
    mat_ground.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*material_color, 1.0)
    mat_ground.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.8
    ground.data.materials.append(mat_ground)
    
    return f"Created ArchViz Rig '{object_name}' with Gobo, Dual-Sky, and Camera at {location}"
