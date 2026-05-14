import bpy
import bmesh
from mathutils import Vector
import math
import random

def create_cookie_scene(
    scene_name: str = "Scene",
    base_location: tuple = (0, 0, 0),
    base_scale: float = 1.0,
    cookie_name: str = "Cookie",
    tray_name: str = "Tray",
    chocolate_chip_count: int = 15,
    cookie_color: tuple = (0.487, 0.320, 0.198), # Brown
    chocolate_chip_color: tuple = (0.188, 0.119, 0.048), # Dark Brown
    tray_color: tuple = (0.021, 0.149, 0.821), # Blue
    light_name: str = "Area_Light",
    light_location: tuple = (5, -5, 5),
    light_power: float = 850.0,
    light_temperature: float = 4000.0, # Kelvin
    camera_name: str = "Camera_Main",
    camera_location: tuple = (3, -3, 3),
    camera_rotation_euler: tuple = (math.radians(60), 0, math.radians(45)),
    **kwargs,
) -> str:
    """
    Create a 3D chocolate chip cookie scene with a tray in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        base_location: (x, y, z) world-space position for the entire scene.
        base_scale: Uniform scale factor for the entire scene.
        cookie_name: Name for the main cookie object.
        tray_name: Name for the tray object.
        chocolate_chip_count: Number of chocolate chips to generate.
        cookie_color: (R, G, B) base color for the cookie in 0-1 range.
        chocolate_chip_color: (R, G, B) base color for the chocolate chips in 0-1 range.
        tray_color: (R, G, B) base color for the tray in 0-1 range.
        light_name: Name for the area light.
        light_location: (x, y, z) world-space position for the light.
        light_power: Power of the area light in Watts.
        light_temperature: Color temperature of the area light in Kelvin.
        camera_name: Name for the camera object.
        camera_location: (x, y, z) Euler world-space position for the camera.
        camera_rotation_euler: (x, y, z) Euler rotation for the camera in radians.
        **kwargs: Additional overrides for specific settings.

    Returns:
        Status string, e.g., "Created 'ChocolateChipCookieScene' at (0, 0, 0) with 3 objects"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math
    import random

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    created_objects = []

    # --- Materials ---
    # Cookie Material
    cookie_mat = bpy.data.materials.new(name=f"{cookie_name}_Material")
    cookie_mat.use_nodes = True
    bsdf_cookie = cookie_mat.node_tree.nodes["Principled BSDF"]
    bsdf_cookie.inputs["Base Color"].default_value = (*cookie_color, 1)
    bsdf_cookie.inputs["Roughness"].default_value = 0.5
    bsdf_cookie.inputs["Specular"].default_value = 0.5

    # Chocolate Chip Material
    chip_mat = bpy.data.materials.new(name=f"{cookie_name}_Chips_Material")
    chip_mat.use_nodes = True
    bsdf_chip = chip_mat.node_tree.nodes["Principled BSDF"]
    bsdf_chip.inputs["Base Color"].default_value = (*chocolate_chip_color, 1)
    bsdf_chip.inputs["Roughness"].default_value = 0.5
    bsdf_chip.inputs["Specular"].default_value = 0.5

    # Tray Material
    tray_mat = bpy.data.materials.new(name=f"{tray_name}_Material")
    tray_mat.use_nodes = True
    bsdf_tray = tray_mat.node_tree.nodes["Principled BSDF"]
    bsdf_tray.inputs["Base Color"].default_value = (*tray_color, 1)
    bsdf_tray.inputs["Roughness"].default_value = 0.5
    bsdf_tray.inputs["Specular"].default_value = 0.5

    # --- 1. Create Cookie Base ---
    cookie_radius = 1.0 * base_scale
    cookie_depth = 0.2 * base_scale
    bpy.ops.mesh.primitive_cylinder_add(
        radius=cookie_radius,
        depth=cookie_depth,
        location=Vector(base_location),
        align='WORLD'
    )
    cookie_obj = bpy.context.active_object
    cookie_obj.name = cookie_name
    cookie_obj.data.materials.append(cookie_mat)
    bpy.ops.object.shade_smooth()
    created_objects.append(cookie_obj)

    # --- 2. Create Chocolate Chips ---
    cookie_top_z = base_location[2] + cookie_depth / 2
    chip_base_scale = 0.1 * base_scale
    cookie_surface_radius = cookie_radius - chip_base_scale * 0.5 # To keep chips on surface

    for i in range(chocolate_chip_count):
        # Generate random position within the cookie's top surface
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(0, cookie_surface_radius)
        chip_x = base_location[0] + dist * math.cos(angle)
        chip_y = base_location[1] + dist * math.sin(angle)
        chip_z = cookie_top_z + chip_base_scale * 0.51 # Place slightly on top of cookie

        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=chip_base_scale,
            location=Vector((chip_x, chip_y, chip_z)),
            align='WORLD'
        )
        chip_obj = bpy.context.active_object
        chip_obj.name = f"{cookie_name}_Chip_{i+1}"
        chip_obj.data.materials.append(chip_mat)
        bpy.ops.object.shade_smooth()
        created_objects.append(chip_obj)

    # --- 3. Create Tray ---
    tray_size_xy = 2.5 * base_scale
    tray_thickness = 0.1 * base_scale
    ridge_height = 0.15 * base_scale
    ridge_inset_amount = 0.1 * base_scale

    bpy.ops.mesh.primitive_cube_add(
        size=tray_size_xy,
        location=(base_location[0], base_location[1], base_location[2] - tray_thickness / 2 - 0.05 * base_scale), # Below cookie
        align='WORLD'
    )
    tray_obj = bpy.context.active_object
    tray_obj.name = tray_name
    tray_obj.data.materials.append(tray_mat)
    created_objects.append(tray_obj)

    bpy.context.view_layer.objects.active = tray_obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')

    # Select the top face (assuming it's the 5th face by default for a cube added at origin)
    # The BMesh approach is robust for selection after operations.
    bm = bmesh.from_edit_mesh(tray_obj.data)
    bm.faces.ensure_lookup_table()
    top_face_bmesh = None
    for face in bm.faces:
        # Check normal and Z coordinate to ensure it's the top face of the tray
        if face.normal.z > 0.9 and face.calc_center_median().z > (base_location[2] - tray_thickness / 2 - 0.05 * base_scale - 0.01): # Small offset for float comparison
            top_face_bmesh = face
            break
    
    if top_face_bmesh:
        bm.select_all(action='DESELECT') # Deselect all
        top_face_bmesh.select = True # Select only the top face
        bmesh.update_edit_mesh(tray_obj.data) # Update mesh for operators
        
        bpy.ops.mesh.inset(thickness=ridge_inset_amount)
        
        # After inset, the newly created inner face is selected by default for extrusion
        bpy.ops.mesh.extrude_region_move(
            MESH_OT_extrude_region={"type":"NORMAL"}, 
            TRANSFORM_OT_translate={"value":(0,0,-ridge_height)} # Extrude directly down
        )
    else:
        print(f"Warning: Could not find top face for tray '{tray_name}'. Skipping ridge creation.")

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth() # Shade smooth the tray

    # --- 4. Setup Lighting ---
    for obj in scene.objects:
        if obj.type == 'LIGHT' and obj.name == 'Light':
            bpy.data.objects.remove(obj, do_unlink=True)
            break # Remove only the default light if it exists

    bpy.ops.object.light_add(type='AREA', location=Vector(light_location))
    area_light = bpy.context.active_object
    area_light.name = light_name
    area_light.data.energy = light_power
    area_light.data.use_nodes = True
    
    # Set color temperature (Blender 4.0+)
    # Adjust temperature directly on the light data
    area_light.data.temperature = light_temperature
    
    created_objects.append(area_light)

    # --- 5. Setup Camera ---
    # Remove existing camera if specified (or just reuse if it's the default 'Camera')
    for obj in scene.objects:
        if obj.type == 'CAMERA' and obj.name == 'Camera':
            bpy.data.objects.remove(obj, do_unlink=True)
            break

    bpy.ops.object.camera_add(location=Vector(camera_location), rotation=camera_rotation_euler)
    cam_obj = bpy.context.active_object
    cam_obj.name = camera_name
    created_objects.append(cam_obj)
    scene.camera = cam_obj

    # --- 6. Rendering Settings ---
    scene.render.engine = 'CYCLES'
    scene.cycles.device = kwargs.get('cycles_device', 'GPU') 
    scene.cycles.samples = kwargs.get('render_samples', 128)
    
    # Set background to black (as in the video's final render)
    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0, 0, 0, 1) # Black background
    bg.inputs[1].default_value = 1.0 # Strength

    return f"Created '{cookie_name}' scene at {base_location} with {len(created_objects)} objects."
