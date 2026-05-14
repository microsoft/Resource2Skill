def create_archviz_room(
    scene_name: str = "Scene",
    object_name: str = "ArchRoom",
    location: tuple = (0, 0, 0),
    size: tuple = (5.0, 4.0, 3.0), 
    window_size: tuple = (2.0, 1.5),
    wall_color: tuple = (0.85, 0.85, 0.82),
    floor_color: tuple = (0.2, 0.1, 0.05),
    **kwargs,
) -> str:
    """
    Create a Parametric Arch-Viz Room Shell with a Boolean window, frame, and procedural floor.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position of the room's bottom center.
        size: (width_x, depth_y, height_z) dimensions of the interior space.
        window_size: (width, height) of the window on the Y-wall.
        wall_color: (R, G, B) color of the interior plaster walls.
        floor_color: (R, G, B) base color of the procedural wood floorboards.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    import mathutils
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    col = scene.collection
    
    wall_thickness = 0.2
    objs_created = 0

    # === 1. Create Materials ===
    mat_wall = bpy.data.materials.new(name=f"{object_name}_Wall")
    mat_wall.use_nodes = True
    mat_wall.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*wall_color, 1.0)
    mat_wall.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9

    mat_floor = bpy.data.materials.new(name=f"{object_name}_Floor")
    mat_floor.use_nodes = True
    mat_floor.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.3
    
    # Procedural Floorboard Shader Network
    nodes = mat_floor.node_tree.nodes
    links = mat_floor.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_brick = nodes.new('ShaderNodeTexBrick')
    tex_brick.inputs['Color1'].default_value = (*floor_color, 1.0)
    tex_brick.inputs['Color2'].default_value = (floor_color[0]*0.7, floor_color[1]*0.7, floor_color[2]*0.7, 1.0)
    tex_brick.inputs['Mortar'].default_value = (0.01, 0.01, 0.01, 1.0)
    tex_brick.inputs['Scale'].default_value = 1.0
    tex_brick.inputs['Mortar Size'].default_value = 0.005
    tex_brick.inputs['Brick Width'].default_value = 2.0
    tex_brick.inputs['Row Height'].default_value = 0.2

    links.new(tex_coord.outputs['Object'], tex_brick.inputs['Vector'])
    links.new(tex_brick.outputs['Color'], bsdf.inputs['Base Color'])

    # === 2. Create Room Mesh ===
    mesh = bpy.data.meshes.new(object_name)
    room_obj = bpy.data.objects.new(object_name, mesh)
    col.objects.link(room_obj)
    
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    bmesh.ops.translate(bm, vec=Vector((0, 0, size[2]/2)), verts=bm.verts)
    bmesh.ops.reverse_faces(bm, faces=bm.faces) # Flip normals to point inwards
    
    room_obj.data.materials.append(mat_wall)
    room_obj.data.materials.append(mat_floor)
    
    # Assign floor material (index 1) to the bottom face (which now points UP due to flipped normals)
    for face in bm.faces:
        face.material_index = 1 if face.normal.z > 0.9 else 0
            
    bm.to_mesh(mesh)
    bm.free()
    
    # Solidify modifier for walls
    mod_solid = room_obj.modifiers.new(name="WallThickness", type='SOLIDIFY')
    mod_solid.thickness = wall_thickness
    mod_solid.offset = 1.0 # Push thickness outwards from the interior volume
    
    room_obj.location = Vector(location)
    objs_created += 1

    # === 3. Add Window Cutout & Geometry ===
    window_name = f"{object_name}_Window"
    
    # Calculate local position: centered on positive Y wall, halfway up
    cutter_local_pos = Vector((0, size[1]/2 + wall_thickness/2, size[2]/2))
    
    # Window Cutter (Boolean Target)
    cutter_mesh = bpy.data.meshes.new(f"{window_name}_Cutter")
    cutter_obj = bpy.data.objects.new(f"{window_name}_Cutter", cutter_mesh)
    col.objects.link(cutter_obj)
    
    bm_cutter = bmesh.new()
    bmesh.ops.create_cube(bm_cutter, size=1.0)
    bmesh.ops.scale(bm_cutter, vec=Vector((window_size[0], 1.0, window_size[1])), verts=bm_cutter.verts)
    bm_cutter.to_mesh(cutter_mesh)
    bm_cutter.free()
    
    cutter_obj.location = cutter_local_pos
    cutter_obj.display_type = 'WIRE'
    cutter_obj.hide_render = True
    cutter_obj.parent = room_obj
    
    # Apply Boolean Difference
    mod_bool = room_obj.modifiers.new(name="WindowCut", type='BOOLEAN')
    mod_bool.object = cutter_obj
    mod_bool.operation = 'DIFFERENCE'
    
    # Window Frame (using Wireframe modifier on a subdivided grid)
    frame_mesh = bpy.data.meshes.new(f"{window_name}_Frame")
    frame_obj = bpy.data.objects.new(f"{window_name}_Frame", frame_mesh)
    col.objects.link(frame_obj)
    
    bm_frame = bmesh.new()
    # 2x2 grid provides a perfect central crossbar
    bmesh.ops.create_grid(bm_frame, x_segments=2, y_segments=2, size=0.5) 
    bmesh.ops.scale(bm_frame, vec=Vector((window_size[0], window_size[1], 1.0)), verts=bm_frame.verts)
    rot_mat = mathutils.Matrix.Rotation(math.pi/2, 4, 'X')
    bmesh.ops.rotate(bm_frame, cent=Vector((0,0,0)), matrix=rot_mat, verts=bm_frame.verts)
    bm_frame.to_mesh(frame_mesh)
    bm_frame.free()
    
    frame_obj.location = cutter_local_pos
    frame_obj.parent = room_obj
    
    mod_wire = frame_obj.modifiers.new(name="FrameThickness", type='WIREFRAME')
    mod_wire.thickness = 0.04
    
    mat_frame = bpy.data.materials.new(name=f"{window_name}_FrameMat")
    mat_frame.use_nodes = True
    mat_frame.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.05, 0.05, 0.05, 1.0)
    mat_frame.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 0.8
    frame_obj.data.materials.append(mat_frame)
    
    # Window Glass Pane
    glass_mesh = bpy.data.meshes.new(f"{window_name}_Glass")
    glass_obj = bpy.data.objects.new(f"{window_name}_Glass", glass_mesh)
    col.objects.link(glass_obj)
    
    bm_glass = bmesh.new()
    bmesh.ops.create_grid(bm_glass, x_segments=1, y_segments=1, size=0.5)
    bmesh.ops.scale(bm_glass, vec=Vector((window_size[0]-0.05, window_size[1]-0.05, 1.0)), verts=bm_glass.verts)
    bmesh.ops.rotate(bm_glass, cent=Vector((0,0,0)), matrix=rot_mat, verts=bm_glass.verts)
    bm_glass.to_mesh(glass_mesh)
    bm_glass.free()
    
    glass_obj.location = cutter_local_pos
    glass_obj.parent = room_obj
    
    mat_glass = bpy.data.materials.new(name=f"{window_name}_GlassMat")
    mat_glass.use_nodes = True
    bsdf_glass = mat_glass.node_tree.nodes["Principled BSDF"]
    bsdf_glass.inputs["Base Color"].default_value = (0.9, 0.95, 1.0, 1.0)
    bsdf_glass.inputs["Roughness"].default_value = 0.02
    
    # Handle API changes for Transmission across Blender versions
    if "Transmission Weight" in bsdf_glass.inputs:
        bsdf_glass.inputs["Transmission Weight"].default_value = 1.0
    elif "Transmission" in bsdf_glass.inputs:
        bsdf_glass.inputs["Transmission"].default_value = 1.0
        
    mat_glass.blend_method = 'BLEND'
    mat_glass.shadow_method = 'NONE'
    mat_glass.use_screen_refraction = True
    glass_obj.data.materials.append(mat_glass)

    # === 4. Add Staging Area Light ===
    light_data = bpy.data.lights.new(name=f"{window_name}_Daylight", type='AREA')
    light_obj = bpy.data.objects.new(name=f"{window_name}_Daylight", object_data=light_data)
    col.objects.link(light_obj)
    
    light_data.energy = 800.0
    light_data.color = (0.95, 0.98, 1.0)
    light_data.shape = 'RECTANGLE'
    light_data.size = window_size[0]
    light_data.size_y = window_size[1]
    
    # Place light slightly outside the window and point it inwards (-Y)
    light_obj.location = cutter_local_pos + Vector((0, 1.0, 0))
    light_obj.rotation_euler = (-math.pi/2, 0, 0)
    light_obj.parent = room_obj
    
    objs_created += 4

    return f"Created Parametric Arch-Viz Room '{object_name}' at {location} with {objs_created} components."
