def create_animated_isometric_element(
    scene_name: str = "Scene",
    object_name: str = "IsoProp",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.25, 0.1),
    spawn_start_frame: int = 1,
    spawn_duration: int = 20,
    setup_isometric_camera: bool = True,
    enable_freestyle: bool = True,
    **kwargs,
) -> str:
    """
    Create an Animated Isometric Prop in the active Blender scene.
    It appears with a bouncy scale-up animation and sets up the scene for isometric rendering.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Final uniform scale factor after animation finishes.
        material_color: (R, G, B) base color in 0-1 range.
        spawn_start_frame: The frame at which the object begins to scale up from 0.
        spawn_duration: How many frames the bounce animation takes.
        setup_isometric_camera: If True, creates an orthographic camera at an isometric angle.
        enable_freestyle: If True, enables Freestyle line rendering.

    Returns:
        Status string describing what was generated.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Create the Base Object ===
    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.active_object
    obj.name = object_name
    
    # Add a small bevel so Freestyle lines catch the edges nicely
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.05
    bevel.segments = 3
    
    # Position the object
    obj.location = Vector(location)
    
    # === Step 2: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.8 # Matte illustrative look
    obj.data.materials.append(mat)

    # === Step 3: Animation (Bounce Spawning) ===
    # Frame A: Scale is 0
    obj.scale = (0.0, 0.0, 0.0)
    obj.keyframe_insert(data_path="scale", frame=spawn_start_frame)
    
    # Frame B: Scale is target scale
    obj.scale = (scale, scale, scale)
    obj.keyframe_insert(data_path="scale", frame=spawn_start_frame + spawn_duration)
    
    # Modify F-Curves for Bounce Out interpolation
    if obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            if fcurve.data_path == "scale":
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'BOUNCE'
                    kf.easing = 'EASE_OUT'

    # === Step 4: Scene Context (Camera & Render Settings) ===
    status_msg = f"Created animated '{object_name}' at {location} starting at frame {spawn_start_frame}."

    if setup_isometric_camera:
        cam_name = "IsometricCamera"
        if cam_name not in scene.objects:
            cam_data = bpy.data.cameras.new(cam_name)
            cam_data.type = 'ORTHO'
            cam_data.ortho_scale = 15.0
            
            cam_obj = bpy.data.objects.new(cam_name, cam_data)
            scene.collection.objects.link(cam_obj)
            
            # Position the camera to look at the origin from an equal offset
            d = 15.0
            cam_obj.location = (d, -d, d)
            # Standard isometric rotation angles
            cam_obj.rotation_euler = (math.radians(54.736), 0.0, math.radians(45.0))
            
            scene.camera = cam_obj
            status_msg += " Setup Orthographic Camera."

    if enable_freestyle:
        scene.render.engine = 'EEVEE' 
        scene.render.use_freestyle = True
        scene.render.line_thickness = 1.2
        
        # Ensure we have a view layer for freestyle settings
        view_layer = scene.view_layers[0]
        view_layer.use_freestyle = True
        
        status_msg += " Enabled Freestyle rendering."

    return status_msg
