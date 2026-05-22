def create_sunlit_architectural_box(
    scene_name: str = "Scene",
    object_name: str = "SunlitRoom",
    location: tuple = (0, 0, 0),
    room_dimensions: tuple = (6.0, 5.0, 3.0), # Width(X), Depth(Y), Height(Z)
    window_dimensions: tuple = (3.0, 2.5), # Width(X), Height(Z)
    wall_color: tuple = (0.65, 0.30, 0.15),
    floor_color: tuple = (0.30, 0.10, 0.05),
    sun_elevation_deg: float = 15.0,
    sun_rotation_deg: float = 210.0,
    **kwargs,
) -> str:
    """
    Create an interior architectural box with a large window and Nishita sky lighting.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the room object.
        location: (x, y, z) world-space position.
        room_dimensions: (x, y, z) dimensions of the interior room.
        window_dimensions: (x, z) size of the window cut on the positive Y wall.
        wall_color: (R, G, B) color for the walls/ceiling.
        floor_color: (R, G, B) color for the floor.
        sun_elevation_deg: Angle of the sun (lower = longer shadows).
        sun_rotation_deg: Direction of the sun (adjust to cast light through window).
        
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Switch to Cycles for proper global illumination and Nishita compatibility
    scene.render.engine = 'CYCLES'
    # Drop exposure by 3 stops to handle realistic sky intensity (as per tutorial)
    scene.view_settings.exposure = -3.0

    # === Step 1: Materials ===
    # Wall Material
    mat_wall = bpy.data.materials.new(name=f"{object_name}_WallMat")
    mat_wall.use_nodes = True
    bsdf_wall = mat_wall.node_tree.nodes.get("Principled BSDF")
    if bsdf_wall:
        bsdf_wall.inputs["Base Color"].default_value = (*wall_color, 1.0)
        bsdf_wall.inputs["Roughness"].default_value = 0.85 # Matte plaster

    # Floor Material
    mat_floor = bpy.data.materials.new(name=f"{object_name}_FloorMat")
    mat_floor.use_nodes = True
    bsdf_floor = mat_floor.node_tree.nodes.get("Principled BSDF")
    if bsdf_floor:
        bsdf_floor.inputs["Base Color"].default_value = (*floor_color, 1.0)
        bsdf_floor.inputs["Roughness"].default_value = 0.4 # Semi-reflective tile

    # === Step 2: Base Geometry (Room Shell) ===
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    room = bpy.context.active_object
    room.name = object_name
    room.scale = room_dimensions
    
    # Position so the floor sits exactly at the provided Z location
    room.location = Vector(location) + Vector((0, 0, room_dimensions[2] / 2))
    
    # Apply scale so modifiers and bmesh operations calculate correctly
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Assign material slots
    room.data.materials.append(mat_wall)  # Slot 0
    room.data.materials.append(mat_floor) # Slot 1

    # === Step 3: Bmesh Operations (Normals & Floor Assignment) ===
    # We want to be *inside* the box, so we flip the normals inward.
    # Then we find the face pointing UP (inside floor) to assign the floor material.
    bm = bmesh.new()
    bm.from_mesh(room.data)
    
    bmesh.ops.reverse_faces(bm, faces=bm.faces)
    
    for face in bm.faces:
        # If the normal is pointing straight UP (Z == 1.0), it's the floor
        if face.normal.z > 0.9:
            face.material_index = 1
        else:
            face.material_index = 0
            
    bm.to_mesh(room.data)
    bm.free()

    # === Step 4: Add Thickness (Solidify) ===
    # Add thickness pushing OUTWARDS so we don't shrink interior space
    solidify = room.modifiers.new(name="WallThickness", type='SOLIDIFY')
    solidify.thickness = 0.3
    solidify.offset = 1.0 

    # === Step 5: Cut Window (Boolean) ===
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    cutter = bpy.context.active_object
    cutter.name = f"{object_name}_WindowCutter"
    
    # Make cutter deep enough on Y to slice entirely through the solidified wall
    cutter.scale = (window_dimensions[0], 2.0, window_dimensions[1])
    
    # Position cutter on the positive Y wall, resting on the floor
    cutter.location = (
        location[0], 
        location[1] + (room_dimensions[1] / 2), 
        location[2] + (window_dimensions[1] / 2)
    )
    
    cutter.display_type = 'WIRE'
    cutter.hide_render = True
    cutter.hide_viewport = True

    # Link cutter to room via Boolean Difference
    bool_mod = room.modifiers.new(name="WindowCut", type='BOOLEAN')
    bool_mod.object = cutter
    bool_mod.operation = 'DIFFERENCE'

    # === Step 6: World Lighting (Nishita Sky) ===
    world = scene.world
    if not world:
        world = bpy.data.worlds.new("World")
        scene.world = world
        
    world.use_nodes = True
    tree = world.node_tree
    
    # Clear existing world nodes
    for node in tree.nodes:
        tree.nodes.remove(node)
        
    # Create Sky and Background nodes
    node_sky = tree.nodes.new(type="ShaderNodeTexSky")
    node_sky.sky_type = 'NISHITA'
    node_sky.sun_elevation = math.radians(sun_elevation_deg)
    node_sky.sun_rotation = math.radians(sun_rotation_deg)
    
    node_bg = tree.nodes.new(type="ShaderNodeBackground")
    node_out = tree.nodes.new(type="ShaderNodeOutputWorld")
    
    node_sky.location = (-300, 0)
    node_bg.location = (0, 0)
    node_out.location = (300, 0)
    
    # Link them together
    tree.links.new(node_sky.outputs['Color'], node_bg.inputs['Color'])
    tree.links.new(node_bg.outputs['Background'], node_out.inputs['Surface'])

    # Deselect all, select main object
    bpy.ops.object.select_all(action='DESELECT')
    room.select_set(True)
    bpy.context.view_layer.objects.active = room

    return f"Created architectural box '{object_name}' with Nishita Sky (Sun Elevation: {sun_elevation_deg}°). Camera exposure set to -3.0."
