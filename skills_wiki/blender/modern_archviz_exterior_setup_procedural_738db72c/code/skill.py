def create_archviz_exterior_setup(
    scene_name: str = "Scene",
    object_name: str = "ArchViz_Setup",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    sun_elevation: float = 0.436, # ~25 degrees in radians
    sun_rotation: float = 2.11,   # ~121 degrees in radians
    **kwargs,
) -> str:
    """
    Create a modern ArchViz exterior staging environment, including Nishita lighting, 
    AgX color management, a procedural street/curb, and a proxy house with normal fixes.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated setup (root empty).
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        sun_elevation: Elevation of the Nishita sun.
        sun_rotation: Rotation of the Nishita sun.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Ensure Cycles is the engine for physical sky to look correct
    scene.render.engine = 'CYCLES'
    
    # === Step 1: Lighting & Color Management ===
    # Set AgX and Exposure (As per tutorial: -2.0 exposure, AgX look)
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.exposure = -2.0
    
    # Setup Nishita Sky
    world = scene.world
    if not world:
        world = bpy.data.worlds.new("ArchViz_World")
        scene.world = world
    world.use_nodes = True
    wnodes = world.node_tree.nodes
    wlinks = world.node_tree.links
    
    wnodes.clear()
    node_sky = wnodes.new(type='ShaderNodeTexSky')
    node_sky.sky_type = 'NISHITA'
    node_sky.sun_elevation = sun_elevation
    node_sky.sun_rotation = sun_rotation
    
    node_bg = wnodes.new(type='ShaderNodeBackground')
    node_out = wnodes.new(type='ShaderNodeOutputWorld')
    
    wlinks.new(node_sky.outputs['Color'], node_bg.inputs['Color'])
    wlinks.new(node_bg.outputs['Background'], node_out.inputs['Surface'])

    # === Step 2: Materials ===
    def create_material(name, color, roughness, is_asphalt=False):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs['Base Color'].default_value = (*color, 1.0)
        bsdf.inputs['Roughness'].default_value = roughness
        
        if is_asphalt:
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            noise = nodes.new('ShaderNodeTexNoise')
            noise.inputs['Scale'].default_value = 50.0
            noise.inputs['Detail'].default_value = 15.0
            bump = nodes.new('ShaderNodeBump')
            bump.inputs['Distance'].default_value = 0.05
            links.new(noise.outputs['Fac'], bump.inputs['Height'])
            links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
            
        return mat

    mat_plaster = create_material("Arch_Plaster", (0.8, 0.8, 0.8), 0.9)
    mat_wood = create_material("Arch_Wood", (0.35, 0.15, 0.05), 0.5)
    mat_asphalt = create_material("Arch_Asphalt", (0.05, 0.05, 0.05), 0.8, is_asphalt=True)
    mat_concrete = create_material("Arch_Concrete", (0.3, 0.3, 0.3), 0.75)
    mat_glass = create_material("Arch_Glass", (0.02, 0.02, 0.02), 0.1)

    # === Step 3: Geometry Generation ===
    # Create a root empty to hold everything
    root_empty = bpy.data.objects.new(object_name, None)
    root_empty.location = Vector(location)
    root_empty.scale = (scale, scale, scale)
    scene.collection.objects.link(root_empty)
    
    objects_created = 0

    # Helper function to create meshes
    def create_box(name, dimensions, loc, mat):
        bpy.ops.mesh.primitive_cube_add(size=1)
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = dimensions
        obj.location = loc
        obj.data.materials.append(mat)
        obj.parent = root_empty
        return obj

    # 1. Procedural Street Context
    road = create_box(f"{object_name}_Road", (20.0, 10.0, 0.1), (0, -8.0, -0.05), mat_asphalt)
    
    # 2. Curbs (with Bevel as specified in video)
    curb = create_box(f"{object_name}_Curb", (20.0, 0.4, 0.25), (0, -2.8, 0.125), mat_concrete)
    bevel = curb.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.02
    bevel.segments = 3
    bpy.ops.object.shade_smooth({"object": curb})

    # 3. House Proxy (Modern overlapping volumes)
    house_base = create_box(f"{object_name}_House_Base", (12.0, 6.0, 3.0), (0, 0.5, 1.5), mat_plaster)
    house_upper = create_box(f"{object_name}_House_Upper", (8.0, 7.0, 2.5), (2.0, 1.0, 4.25), mat_plaster)
    house_wood_accent = create_box(f"{object_name}_House_Accent", (4.0, 0.2, 3.0), (-2.0, -2.4, 1.5), mat_wood)
    house_window = create_box(f"{object_name}_House_Glass", (3.0, 0.3, 2.0), (3.0, -2.4, 4.25), mat_glass)
    
    # Apply Weighted Normal Fix (crucial archviz step mentioned in tutorial)
    for house_part in [house_base, house_upper, house_wood_accent]:
        wn = house_part.modifiers.new(name="WeightedNormal", type='WEIGHTED_NORMAL')
        wn.keep_sharp = True
        
        # Enable auto-smooth to make weighted normal work properly
        house_part.data.use_auto_smooth = True
        bpy.ops.object.shade_smooth({"object": house_part})
        
        objects_created += 1
        
    objects_created += 2 # Road and Curb

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created ArchViz Context '{object_name}' at {location} with {objects_created} stylized objects, Nishita Sky, and AgX profile."
