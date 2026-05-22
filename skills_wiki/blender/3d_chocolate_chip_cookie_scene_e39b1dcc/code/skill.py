import bpy
import bmesh
from mathutils import Vector
import math
import random

def create_chocolate_chip_cookie_scene(
    scene_name: str = "Scene",
    object_name_prefix: str = "CookieScene",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    cookie_color: tuple = (0.7, 0.4, 0.2), # Brown for cookie dough
    chip_color: tuple = (0.3, 0.15, 0.05), # Dark brown for chocolate chips
    tray_color: tuple = (0.1, 0.2, 0.8), # Blue for tray
    num_chips: int = 15,
    light_power: float = 850.0,
    light_temp: float = 4000.0,
    camera_distance: float = 5.0,
    **kwargs,
) -> str:
    """
    Create a 3D chocolate chip cookie scene with a tray and lighting in Blender.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name_prefix: Prefix for naming created objects.
        location: (x, y, z) world-space position for the center of the scene.
        scale: Uniform scale factor for the entire scene.
        cookie_color: (R, G, B) base color for the cookie dough.
        chip_color: (R, G, B) base color for the chocolate chips.
        tray_color: (R, G, B) base color for the tray.
        num_chips: Number of chocolate chips to generate.
        light_power: Power of the area light in Watts.
        light_temp: Temperature of the area light in Kelvin.
        camera_distance: Distance of the camera from the scene center.
        **kwargs: Additional overrides (not used in this version).

    Returns:
        Status string, e.g., "Created 'CookieScene' at (0, 0, 0) with multiple objects"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math
    import random

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Create a new collection for the scene's objects
    collection = bpy.data.collections.new(object_name_prefix)
    scene.collection.children.link(collection)

    created_objects = []

    # Ensure all objects are deselected
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None

    # === 1. Create Cookie Base ===
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1.0 * scale,
        depth=0.2 * scale,
        location=Vector(location),
        rotation=(0, 0, 0),
        vertices=64 # Higher resolution for smoother curve
    )
    cookie_obj = bpy.context.active_object
    cookie_obj.name = f"{object_name_prefix}_Cookie"
    cookie_obj.data.use_auto_smooth = True # Equivalent to Shade Smooth
    collection.objects.link(cookie_obj)
    scene.collection.objects.unlink(cookie_obj) # Unlink from default scene collection
    created_objects.append(cookie_obj)

    # Cookie Material
    cookie_mat = bpy.data.materials.new(name=f"{object_name_prefix}_CookieMaterial")
    cookie_mat.use_nodes = True
    if "Principled BSDF" in cookie_mat.node_tree.nodes:
        bsdf = cookie_mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*cookie_color, 1.0)
    else: # Fallback if node name changes or is missing
        cookie_mat.diffuse_color = (*cookie_color, 1.0)
    cookie_obj.data.materials.append(cookie_mat)

    # === 2. Create Chocolate Chips ===
    chip_mat = bpy.data.materials.new(name=f"{object_name_prefix}_ChipMaterial")
    chip_mat.use_nodes = True
    if "Principled BSDF" in chip_mat.node_tree.nodes:
        bsdf = chip_mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*chip_color, 1.0)
    else:
        chip_mat.diffuse_color = (*chip_color, 1.0)
    
    for i in range(num_chips):
        offset_x = random.uniform(-0.8 * scale, 0.8 * scale)
        offset_y = random.uniform(-0.8 * scale, 0.8 * scale)
        # Random Z to make some chips more embedded than others
        offset_z = random.uniform(location[2] + 0.05 * scale, location[2] + 0.15 * scale) 

        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.1 * scale,
            segments=16, 
            rings=8,
            location=Vector((location[0] + offset_x, location[1] + offset_y, offset_z)),
            rotation=(0, 0, 0)
        )
        chip_obj = bpy.context.active_object
        chip_obj.name = f"{object_name_prefix}_Chip_{i:02d}"
        chip_obj.data.use_auto_smooth = True
        chip_obj.data.materials.append(chip_mat)
        collection.objects.link(chip_obj)
        scene.collection.objects.unlink(chip_obj)
        created_objects.append(chip_obj)

    # === 3. Create Tray ===
    tray_base_size = 2.5 * scale # Larger than cookie
    tray_height = 0.1 * scale
    ridge_thickness = 0.1 * scale

    # Create base cube for the tray
    bpy.ops.mesh.primitive_cube_add(
        size=tray_base_size,
        location=Vector((location[0], location[1], location[2] - tray_height - ridge_thickness/2 - 0.05 * scale)), # Place below cookie
        rotation=(0, 0, 0)
    )
    tray_obj = bpy.context.active_object
    tray_obj.name = f"{object_name_prefix}_Tray"
    collection.objects.link(tray_obj)
    scene.collection.objects.unlink(tray_obj)
    created_objects.append(tray_obj)
    
    tray_obj.data.use_auto_smooth = True

    # Use bmesh for precise geometry modification
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(tray_obj.data)
    
    # Select the top face (assuming Z-up orientation and cube centered)
    top_face = None
    for face in bm.faces:
        if face.normal.z > 0.99: # Top face normal points mostly up
            top_face = face
            break
            
    if top_face:
        # Deselect all faces first, then select only the top face
        for face in bm.faces:
            face.select = False
        top_face.select = True

        # Inset the top face to create the ridge outline
        # Inset operation returns selected geometry, which is the new inner face
        inset_result = bmesh.ops.inset_regions(bm, faces=[top_face], thickness=ridge_thickness, depth=0)
        
        # The newly created face(s) are now selected. Extrude them downwards.
        # Ensure we operate on the *new* inner face, not the outer ring or original top_face
        inner_faces_after_inset = [f for f in bm.faces if f.select and f != top_face]
        
        if inner_faces_after_inset:
            # Extrude the selected inner faces downwards to form the tray cavity
            geom = bmesh.ops.extrude_discrete_faces(bm, faces=inner_faces_after_inset)
            extruded_verts = geom['verts'] # Verts of the newly extruded faces
            
            # Translate the extruded verts down to create depth
            bmesh.ops.translate(bm, verts=extruded_verts, vec=Vector((0, 0, -tray_height)))
            
    bmesh.update_edit_mesh(tray_obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Tray Material
    tray_mat = bpy.data.materials.new(name=f"{object_name_prefix}_TrayMaterial")
    tray_mat.use_nodes = True
    if "Principled BSDF" in tray_mat.node_tree.nodes:
        bsdf = tray_mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*tray_color, 1.0)
    else:
        tray_mat.diffuse_color = (*tray_color, 1.0)
    tray_obj.data.materials.append(tray_mat)

    # === 4. Add Area Light ===
    bpy.ops.object.light_add(
        type='AREA',
        align='WORLD',
        location=Vector((location[0] + 2 * scale, location[1] - 2 * scale, location[2] + 3 * scale))
    )
    light_obj = bpy.context.active_object
    light_obj.name = f"{object_name_prefix}_AreaLight"
    light_obj.data.energy = light_power
    light_obj.data.color = (1.0, 0.8, 0.6) # Warm light color
    light_obj.data.temperature = light_temp
    light_obj.data.size = 1.0 * scale # Adjust light size
    collection.objects.link(light_obj)
    scene.collection.objects.unlink(light_obj)
    created_objects.append(light_obj)

    # === 5. Add Camera ===
    bpy.ops.object.camera_add(
        align='WORLD',
        location=Vector((location[0] + camera_distance, location[1] - camera_distance, location[2] + camera_distance * 0.7))
    )
    camera_obj = bpy.context.active_object
    camera_obj.name = f"{object_name_prefix}_Camera"
    
    # Point camera towards the scene center
    look_at_vector = Vector(location)
    direction = look_at_vector - camera_obj.location
    # Set camera rotation using track-to constraint for easier aiming
    # Temporarily add a temporary empty to track, then delete it
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=look_at_vector)
    target_empty = bpy.context.active_object
    target_empty.name = f"{object_name_prefix}_CameraTarget"
    
    constraint = camera_obj.constraints.new(type='TRACK_TO')
    constraint.target = target_empty
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'
    
    bpy.context.view_layer.update() # Apply constraint
    
    # Bake the visual transform to permanent rotation and remove constraint/empty
    bpy.ops.object.select_all(action='DESELECT')
    camera_obj.select_set(True)
    bpy.context.view_layer.objects.active = camera_obj
    bpy.ops.object.visual_transform_apply()
    
    camera_obj.constraints.remove(constraint)
    
    bpy.ops.object.select_all(action='DESELECT')
    target_empty.select_set(True)
    bpy.ops.object.delete()
    
    scene.camera = camera_obj
    collection.objects.link(camera_obj)
    scene.collection.objects.unlink(camera_obj)
    created_objects.append(camera_obj)

    # === 6. Rendering Settings (as per video's final render engine) ===
    scene.render.engine = 'CYCLES' 
    # Set GPU compute if available and enabled in user preferences
    prefs = bpy.context.preferences
    cycles_prefs = prefs.addons['cycles'].preferences
    if cycles_prefs.compute_device_type in {'CUDA', 'OPTIX'}:
        scene.cycles.device = 'GPU'
        # Set all available GPUs for rendering
        for device in cycles_prefs.devices:
            if device.type == 'GPU':
                device.use = True
    else:
        scene.cycles.device = 'CPU'
    
    # Set samples lower for quicker feedback
    scene.cycles.samples = 64 
    scene.cycles.max_bounces = 4
    scene.cycles.diffuse_bounces = 2
    scene.cycles.glossy_bounces = 2
    scene.cycles.transmission_bounces = 0
    scene.cycles.transparent_max_bounces = 8

    # World background (dark as seen in rendered image)
    world = scene.world
    if world:
        world.use_nodes = True
        if "Background" in world.node_tree.nodes:
            bg_node = world.node_tree.nodes["Background"]
            bg_node.inputs["Color"].default_value = (0.05, 0.05, 0.05, 1) # Dark grey background
            bg_node.inputs["Strength"].default_value = 0.5 

    return f"Created '{object_name_prefix}' scene with {len(created_objects)} objects at {location}."

