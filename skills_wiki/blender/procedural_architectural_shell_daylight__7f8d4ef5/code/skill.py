def create_interior_daylight_scene(
    scene_name: str = "Scene",
    room_name: str = "InteriorRoom",
    location: tuple = (0.0, 0.0, 0.0),
    room_size: tuple = (8.0, 6.0, 3.5),  # width(x), depth(y), height(z)
    window_size: tuple = (3.0, 2.0, 0.5), # width(x), height(z), depth(y - thickness)
    window_offset: tuple = (0.0, 3.0, 1.2), # x, y, z offset from room center. Y=3 places it on the +Y wall
    sun_elevation: float = 20.0,
    sun_rotation: float = -45.0,
    **kwargs
) -> str:
    """
    Create an enclosed architectural room shell with a window cutout and Nishita daylight system.

    Args:
        scene_name: Name of the target scene.
        room_name: Base name for the generated objects.
        location: (x, y, z) world-space position for the center of the room base.
        room_size: (X, Y, Z) dimensions of the interior space.
        window_size: (X, Z, Y) dimensions of the window hole.
        window_offset: (X, Y, Z) position of the window relative to the room center.
        sun_elevation: Angle of the sun above the horizon in degrees.
        sun_rotation: Rotational angle of the sun in degrees.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    loc_vec = Vector(location)

    # === 1. Create Procedural Materials ===
    
    # Plaster Wall Material
    mat_wall = bpy.data.materials.new(name=f"{room_name}_Plaster")
    mat_wall.use_nodes = True
    wn = mat_wall.node_tree.nodes
    wl = mat_wall.node_tree.links
    wn.clear()

    output_wall = wn.new('ShaderNodeOutputMaterial')
    output_wall.location = (300, 0)
    bsdf_wall = wn.new('ShaderNodeBsdfPrincipled')
    bsdf_wall.location = (0, 0)
    bsdf_wall.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)
    bsdf_wall.inputs['Roughness'].default_value = 0.8

    noise = wn.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 50.0
    bump_wall = wn.new('ShaderNodeBump')
    bump_wall.inputs['Distance'].default_value = 0.05
    bump_wall.inputs['Strength'].default_value = 0.3

    wl.new(noise.outputs['Fac'], bump_wall.inputs['Height'])
    wl.new(bump_wall.outputs['Normal'], bsdf_wall.inputs['Normal'])
    wl.new(bsdf_wall.outputs['BSDF'], output_wall.inputs['Surface'])

    # Wood Floor Material
    mat_floor = bpy.data.materials.new(name=f"{room_name}_WoodFloor")
    mat_floor.use_nodes = True
    fn = mat_floor.node_tree.nodes
    fl = mat_floor.node_tree.links
    fn.clear()

    output_floor = fn.new('ShaderNodeOutputMaterial')
    output_floor.location = (300, 0)
    bsdf_floor = fn.new('ShaderNodeBsdfPrincipled')
    bsdf_floor.location = (0, 0)
    bsdf_floor.inputs['Roughness'].default_value = 0.25

    wave = fn.new('ShaderNodeTexWave')
    wave.wave_type = 'BANDS'
    wave.inputs['Scale'].default_value = 2.0
    wave.inputs['Distortion'].default_value = 1.5

    cramp = fn.new('ShaderNodeValToRGB')
    cramp.color_ramp.elements[0].position = 0.0
    cramp.color_ramp.elements[0].color = (0.3, 0.15, 0.05, 1.0)
    cramp.color_ramp.elements[1].position = 1.0
    cramp.color_ramp.elements[1].color = (0.1, 0.05, 0.01, 1.0)

    bump_floor = fn.new('ShaderNodeBump')
    bump_floor.inputs['Distance'].default_value = 0.02

    fl.new(wave.outputs['Fac'], cramp.inputs['Fac'])
    fl.new(cramp.outputs['Color'], bsdf_floor.inputs['Base Color'])
    fl.new(wave.outputs['Fac'], bump_floor.inputs['Height'])
    fl.new(bump_floor.outputs['Normal'], bsdf_floor.inputs['Normal'])
    fl.new(bsdf_floor.outputs['BSDF'], output_floor.inputs['Surface'])

    # === 2. Create Geometry ===

    # Room Shell (Cube)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    room_obj = bpy.context.active_object
    room_obj.name = f"{room_name}_Shell"
    room_obj.scale = room_size
    room_obj.location = loc_vec + Vector((0, 0, room_size[2] / 2.0))
    room_obj.data.materials.append(mat_wall)

    # Solidify Modifier (give walls thickness outward to prevent light leaks)
    solidify = room_obj.modifiers.new(name="WallThickness", type='SOLIDIFY')
    solidify.thickness = 0.2
    solidify.offset = 1.0 

    # Window Cutter (Cube)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    cutter = bpy.context.active_object
    cutter.name = f"{room_name}_WindowCutter"
    cutter.scale = window_size
    cutter.location = loc_vec + Vector(window_offset)
    cutter.display_type = 'WIRE'
    cutter.hide_render = True

    # Boolean Modifier on Room
    bool_mod = room_obj.modifiers.new(name="WindowCut", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = cutter

    # Floor Plane
    bpy.ops.mesh.primitive_plane_add(size=1.0)
    floor_obj = bpy.context.active_object
    floor_obj.name = f"{room_name}_Floor"
    floor_obj.scale = (room_size[0] - 0.05, room_size[1] - 0.05, 1.0)
    floor_obj.location = loc_vec + Vector((0, 0, 0.01)) # Slightly above absolute zero to avoid z-fighting
    floor_obj.data.materials.append(mat_floor)

    # === 3. World Lighting Setup ===
    
    scene.render.engine = 'CYCLES' # Nishita Sky operates optimally in Cycles
    
    world = scene.world
    if not world:
        world = bpy.data.worlds.new("InteriorDaylight")
        scene.world = world
        
    world.use_nodes = True
    wnodes = world.node_tree.nodes
    wlinks = world.node_tree.links
    wnodes.clear()
    
    node_bg = wnodes.new('ShaderNodeBackground')
    node_out = wnodes.new('ShaderNodeOutputWorld')
    node_sky = wnodes.new('ShaderNodeTexSky')
    
    # Configure Nishita Sky
    node_sky.sky_type = 'NISHITA'
    node_sky.sun_elevation = math.radians(sun_elevation)
    node_sky.sun_rotation = math.radians(sun_rotation)
    node_sky.sun_intensity = 3.0
    node_sky.sun_size = math.radians(5.0) # Softens the harsh window shadows
    node_sky.air_density = 0.1 
    node_sky.dust_density = 0.05
    node_sky.ozone_density = 0.1
    
    wlinks.new(node_sky.outputs['Color'], node_bg.inputs['Color'])
    wlinks.new(node_bg.outputs['Background'], node_out.inputs['Surface'])

    # === 4. Camera Setup ===
    
    bpy.ops.object.camera_add()
    cam_obj = bpy.context.active_object
    cam_obj.name = f"{room_name}_Camera"
    
    # Position camera in opposite corner from the target window offset
    cam_obj.location = loc_vec + Vector((room_size[0] * 0.35, -room_size[1] * 0.35, 1.5))
    cam_obj.data.lens = 25 # Wide focal length typical for arch-viz
    cam_obj.data.clip_start = 0.1
    
    # Point camera at the window
    track_mod = cam_obj.constraints.new(type='TRACK_TO')
    track_mod.target = cutter
    track_mod.track_axis = 'TRACK_NEGATIVE_Z'
    track_mod.up_axis = 'UP_Y'
    
    scene.camera = cam_obj

    return f"Created '{room_name}' (Size: {room_size}) with Boolean window, wide-angle Camera, and Nishita daylight system."
