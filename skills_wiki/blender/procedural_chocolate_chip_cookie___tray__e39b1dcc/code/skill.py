import bpy
import bmesh
from mathutils import Vector, Euler
import random
import math

def create_chocolate_chip_cookie_scene(
    scene_name: str = "Scene",
    base_location: tuple = (0, 0, 0),
    overall_scale: float = 1.0,
    cookie_name: str = "Cookie",
    tray_name: str = "Tray",
    chocolate_chip_name_base: str = "ChocolateChip",
    cookie_color: tuple = (0.44, 0.28, 0.17, 1.0), # RGB from video
    chip_color: tuple = (0.18, 0.09, 0.05, 1.0), # RGB from video
    tray_color: tuple = (0.0, 0.0, 0.8, 1.0),   # RGB from video
    num_chips: int = 15,
    light_power: float = 850.0,
    light_temp_kelvin: float = 4000.0,
    camera_location: tuple = (7.2, -8.7, 4.9),
    camera_rotation: tuple = (math.radians(65.5), math.radians(0), math.radians(37.5)), # X, Y, Z Euler
    render_filepath: str = "//render_output.png",
    render_engine: str = "CYCLES", # or 'BLENDER_EEVEE'
    **kwargs,
) -> str:
    """
    Create a 3D chocolate chip cookie scene with a tray in Blender.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        base_location: (x, y, z) world-space position for the entire scene.
        overall_scale: Uniform scale factor for all objects in the scene.
        cookie_name: Name for the main cookie object.
        tray_name: Name for the tray object.
        chocolate_chip_name_base: Base name for individual chocolate chip objects.
        cookie_color: (R, G, B, A) base color for the cookie.
        chip_color: (R, G, B, A) base color for the chocolate chips.
        tray_color: (R, G, B, A) base color for the tray.
        num_chips: Number of chocolate chips to scatter on the cookie.
        light_power: Power of the area light in Watts.
        light_temp_kelvin: Temperature of the light in Kelvin.
        camera_location: (x, y, z) world-space position for the camera.
        camera_rotation: (X, Y, Z) Euler rotation for the camera in radians.
        render_filepath: Path to save the rendered image (relative path starts with //).
        render_engine: Render engine to use ('CYCLES' or 'BLENDER_EEVEE').
        **kwargs: Additional overrides for specific properties.

    Returns:
        Status string, e.g., "Created 'CookieScene' at (0, 0, 0) with 3 objects"
    """
    import bpy
    import bmesh
    from mathutils import Vector, Euler
    import random
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # --- Materials Setup ---
    cookie_mat = bpy.data.materials.new(name=f"{cookie_name}Material")
    cookie_mat.use_nodes = True
    bsdf = cookie_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = cookie_color

    chip_mat = bpy.data.materials.new(name=f"{chocolate_chip_name_base}Material")
    chip_mat.use_nodes = True
    bsdf_chip = chip_mat.node_tree.nodes["Principled BSDF"]
    bsdf_chip.inputs["Base Color"].default_value = chip_color

    tray_mat = bpy.data.materials.new(name=f"{tray_name}Material")
    tray_mat.use_nodes = True
    bsdf_tray = tray_mat.node_tree.nodes["Principled BSDF"]
    bsdf_tray.inputs["Base Color"].default_value = tray_color

    # --- Create Cookie ---
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1.5 * overall_scale,
        depth=0.2 * overall_scale,
        vertices=64, # More vertices for smoother cylinder
        location=Vector((0, 0, base_location[2])),
    )
    obj_cookie = bpy.context.active_object
    obj_cookie.name = cookie_name
    obj_cookie.data.materials.append(cookie_mat)
    bpy.ops.object.shade_smooth()

    # --- Create Chocolate Chips ---
    chips_collection = bpy.data.collections.new(f"{cookie_name}Chips")
    scene.collection.children.link(chips_collection)

    for i in range(num_chips):
        random_x = random.uniform(-0.8, 0.8) * overall_scale
        random_y = random.uniform(-0.8, 0.8) * overall_scale
        random_z_offset = 0.05 * overall_scale # Small offset to sit on cookie surface

        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.1 * overall_scale,
            location=Vector((random_x, random_y, base_location[2] + 0.1 * overall_scale + random_z_offset)),
        )
        obj_chip = bpy.context.active_object
        obj_chip.name = f"{chocolate_chip_name_base}_{i:03d}"
        obj_chip.data.materials.append(chip_mat)
        bpy.ops.object.shade_smooth()
        chips_collection.objects.link(obj_chip)
        scene.collection.objects.unlink(obj_chip) # Unlink from main scene collection

    # --- Create Tray ---
    tray_size = 4 * overall_scale
    tray_depth = 0.1 * overall_scale
    rim_thickness = 0.1 * overall_scale

    bpy.ops.mesh.primitive_cube_add(
        size=tray_size,
        location=Vector((0, 0, base_location[2] - tray_depth/2 - 0.01)), # Sit slightly below cookie
    )
    obj_tray = bpy.context.active_object
    obj_tray.name = tray_name
    obj_tray.data.materials.append(tray_mat)

    # Scale the cube to be flat
    obj_tray.scale = (1, 1, tray_depth / tray_size) # Adjust Z scale for flatness
    bpy.ops.object.transform_apply(scale=True)

    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj_tray.data)
    
    # Select top face
    top_face = None
    for face in bm.faces:
        if abs(face.normal.z - 1.0) < 0.001: # Check for face pointing upwards
            top_face = face
            break

    if top_face:
        # Inset the top face
        bmesh.ops.inset_region(bm, faces=[top_face], thickness=rim_thickness * overall_scale / tray_size, depth=0)
        
        # Extrude the inner face down
        # The new inner face is the last face created by inset_region
        inner_face = bm.faces[-1] 
        bmesh.ops.extrude_region_context(bm, geom=[inner_face])
        
        # Move the extruded face down to create the inner depth
        # After extrude_region_context, the extruded faces are usually selected
        # Get the new extruded face's centroid and move it
        extruded_verts = [v for v in bm.verts if v.select]
        if extruded_verts:
            move_vec = Vector((0, 0, -rim_thickness * overall_scale)) # Move down
            bmesh.ops.translate(bm, verts=extruded_verts, vec=move_vec)

    bmesh.update_edit_mesh(obj_tray.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()


    # --- Finalize Scene Transformations ---
    # Select all created objects to apply base_location and overall_scale
    all_created_objects = [obj_cookie, obj_tray] + list(chips_collection.objects)
    for obj in all_created_objects:
        obj.location += Vector(base_location)
        obj.scale = (overall_scale, overall_scale, overall_scale) # Ensure consistent scaling if not already applied

    # --- Setup Lighting ---
    # Delete default light (if it still exists in the scene and is not already deleted by user)
    default_light = bpy.data.objects.get("Light")
    if default_light:
        bpy.data.objects.remove(default_light, do_unlink=True)

    bpy.ops.object.light_add(type='AREA', location=(base_location[0] + 5 * overall_scale, base_location[1] - 5 * overall_scale, base_location[2] + 7 * overall_scale))
    light_obj = bpy.context.active_object
    light_obj.name = "AreaLight_Cookie"
    light_obj.data.energy = light_power
    light_obj.data.temperature = light_temp_kelvin
    light_obj.rotation_euler = Euler((math.radians(45), math.radians(-30), math.radians(60)), 'XYZ') # Rotate to hit cookie from side

    # --- Setup Camera ---
    camera_obj = bpy.data.objects['Camera']
    camera_obj.location = Vector(camera_location)
    camera_obj.rotation_euler = Euler(camera_rotation, 'XYZ')

    # --- Render Settings ---
    scene.render.engine = render_engine
    if render_engine == 'CYCLES':
        scene.cycles.device = 'GPU' if 'CUDA' in bpy.context.preferences.addons['cycles'].preferences.get_devices() else 'CPU'
        scene.cycles.samples = 128 # Default samples for good quality
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = render_filepath
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080

    # Render the image (optional, as agent might call this separately)
    # bpy.ops.render.render(write_still=True)

    return f"Created '{cookie_name}' scene at {base_location} with multiple objects."

