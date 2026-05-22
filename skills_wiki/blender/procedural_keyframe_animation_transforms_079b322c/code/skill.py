def create_animated_keyframe_scene(
    scene_name: str = "Scene",
    object_name: str = "AnimatedCube",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    color_start: tuple = (0.8, 0.05, 0.05),
    color_end: tuple = (0.05, 0.1, 0.8),
    start_frame: int = 1,
    end_frame: int = 60,
    **kwargs,
) -> str:
    """
    Create an animated object, material, and light using keyframes.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created object.
        location: (x, y, z) starting world-space position.
        scale: Uniform scale factor for the object.
        color_start: (R, G, B) starting material color.
        color_end: (R, G, B) ending material color.
        start_frame: Timeline frame where the animation begins.
        end_frame: Timeline frame where the animation ends.
        
    Returns:
        Status string summarizing the created animated elements.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    # Get target scene and collection
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection
    
    # Ensure timeline accommodates the animation length
    if scene.frame_end < end_frame:
        scene.frame_end = end_frame + 20

    # === Step 1: Create Base Geometry ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    collection.objects.link(obj)

    # Use bmesh to construct a simple cube
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    bm.to_mesh(mesh)
    bm.free()

    # Set initial transform
    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))
    obj.rotation_euler = (0, 0, 0)

    # === Step 2: Keyframe Transform (Location, Rotation, Scale) ===
    # Insert start keyframes
    obj.keyframe_insert(data_path="location", frame=start_frame)
    obj.keyframe_insert(data_path="rotation_euler", frame=start_frame)
    obj.keyframe_insert(data_path="scale", frame=start_frame)

    # Modify transforms for the end state
    obj.location += Vector((5.0 * scale, 3.0 * scale, 1.5 * scale))
    obj.rotation_euler.x += math.radians(90)
    obj.rotation_euler.z += math.radians(180)
    obj.scale = Vector((scale * 1.5, scale * 1.5, scale * 1.5))

    # Insert end keyframes
    obj.keyframe_insert(data_path="location", frame=end_frame)
    obj.keyframe_insert(data_path="rotation_euler", frame=end_frame)
    obj.keyframe_insert(data_path="scale", frame=end_frame)

    # === Step 3: Build & Keyframe Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_MorphMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    obj.data.materials.append(mat)

    if bsdf:
        # Keyframe Starting Color
        bsdf.inputs['Base Color'].default_value = (*color_start, 1.0) # RGBA
        bsdf.inputs['Base Color'].keyframe_insert(data_path="default_value", frame=start_frame)

        # Keyframe Ending Color
        bsdf.inputs['Base Color'].default_value = (*color_end, 1.0)
        bsdf.inputs['Base Color'].keyframe_insert(data_path="default_value", frame=end_frame)

    # === Step 4: Create & Keyframe Environmental Light ===
    light_data = bpy.data.lights.new(name=f"{object_name}_LightData", type='POINT')
    light_obj = bpy.data.objects.new(name=f"{object_name}_Light", object_data=light_data)
    collection.objects.link(light_obj)
    
    # Position light slightly above the ending location of the cube
    light_obj.location = obj.location + Vector((0, 0, 3.0))
    
    # Keyframe light strength (energy)
    light_data.energy = 500.0  # Start dim
    light_data.keyframe_insert(data_path="energy", frame=start_frame)
    
    light_data.energy = 6000.0 # End intensely bright (mimicking tutorial)
    light_data.keyframe_insert(data_path="energy", frame=end_frame)

    return f"Created animated object '{object_name}' moving to {obj.location}, with morphing material and pulsing light across frames {start_frame}-{end_frame}."
