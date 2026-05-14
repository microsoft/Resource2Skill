import bpy
import bmesh
from mathutils import Vector
import math
import random

def create_cookie_scene(
    scene_name: str = "Scene",
    base_location: tuple = (0, 0, 0),
    base_scale: float = 1.0,
    cookie_color: tuple = (0.6, 0.3, 0.1, 1.0), # RGBA
    chip_color: tuple = (0.2, 0.1, 0.05, 1.0), # RGBA
    tray_color: tuple = (0.1, 0.2, 0.8, 1.0), # RGBA
    light_location: tuple = (5, -5, 5),
    light_power: float = 850.0,
    light_temperature: float = 4000.0, # Kelvin
    num_chips: int = 15,
    cookie_radius: float = 1.0,
    cookie_height: float = 0.2,
    tray_inset_thickness: float = 0.1,
    tray_extrusion_depth: float = 0.05,
    **kwargs,
) -> str:
    """
    Create a 3D chocolate chip cookie scene with a tray and lighting.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        base_location: (x, y, z) world-space position for the entire scene.
        base_scale: Uniform scale factor for the entire scene.
        cookie_color: (R, G, B, A) base color for the cookie (0-1 range).
        chip_color: (R, G, B, A) base color for the chocolate chips (0-1 range).
        tray_color: (R, G, B, A) base color for the tray (0-1 range).
        light_location: (x, y, z) world-space position for the area light.
        light_power: Power of the area light in Watts.
        light_temperature: Color temperature of the area light in Kelvin.
        num_chips: Number of chocolate chips on the cookie.
        cookie_radius: Radius of the cookie base.
        cookie_height: Height of the cookie base.
        tray_inset_thickness: Thickness of the tray's inner ridge.
        tray_extrusion_depth: Depth of the tray's inner depression.
        **kwargs: Additional overrides for specific properties (e.g., subdivision_level, roughness).

    Returns:
        Status string, e.g., "Created 'CookieScene' at (0, 0, 0)"
    """

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- Materials ---
    def create_material(name, color):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        principled_bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if not principled_bsdf:
            principled_bsdf = mat.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
            mat.node_tree.links.new(principled_bsdf.outputs['BSDF'], mat.node_tree.nodes['Material Output'].inputs['Surface'])
        
        principled_bsdf.inputs["Base Color"].default_value = color
        return mat

    cookie_mat = create_material("CookieMaterial", cookie_color)
    chip_mat = create_material("ChipMaterial", chip_color)
    tray_mat = create_material("TrayMaterial", tray_color)

    # --- Ensure objects are deselected before adding new ones ---
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None

    # --- 1. Cookie Base ---
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=64,
        radius=cookie_radius * base_scale,
        depth=cookie_height * base_scale,
        location=base_location
    )
    cookie_obj = bpy.context.active_object
    cookie_obj.name = f"{object_name}_Cookie"
    cookie_obj.data.use_auto_smooth = True
    cookie_obj.data.auto_smooth_angle = math.radians(60)
    if cookie_obj.data.materials:
        cookie_obj.data.materials[0] = cookie_mat
    else:
        cookie_obj.data.materials.append(cookie_mat)

    # --- 2. Chocolate Chips ---
    chips_collection = bpy.data.collections.new(f"{object_name}_ChocolateChips")
    scene.collection.children.link(chips_collection)

    chip_size_factor = kwargs.get('chip_size_factor', 0.15)
    current_chip_scale = (cookie_radius * chip_size_factor) * base_scale 
    chip_z_offset = (cookie_height * base_scale / 2) + (current_chip_scale / 2)
    
    # Create the first chip
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=32,
        ring_count=16,
        radius=current_chip_scale / 2,
        location=(base_location[0], base_location[1], base_location[2] + chip_z_offset)
    )
    first_chip_obj = bpy.context.active_object
    first_chip_obj.name = f"{object_name}_Chip_000"
    first_chip_obj.data.use_auto_smooth = True
    first_chip_obj.data.auto_smooth_angle = math.radians(60)
    if first_chip_obj.data.materials:
        first_chip_obj.data.materials[0] = chip_mat
    else:
        first_chip_obj.data.materials.append(chip_mat)
    
    bpy.context.collection.objects.unlink(first_chip_obj)
    chips_collection.objects.link(first_chip_obj)

    # Duplicate and distribute remaining chips
    for i in range(1, num_chips):
        bpy.ops.object.select_all(action='DESELECT')
        first_chip_obj.select_set(True)
        bpy.context.view_layer.objects.active = first_chip_obj
        
        bpy.ops.object.duplicate_move(
            TRANSFORM_OT_translate={
                "value": (random.uniform(-cookie_radius * 0.8, cookie_radius * 0.8) * base_scale,
                          random.uniform(-cookie_radius * 0.8, cookie_radius * 0.8) * base_scale,
                          0.0)
            }
        )
        chip_obj = bpy.context.active_object
        chip_obj.name = f"{object_name}_Chip_{i:03d}"
        
        # Adjust Z position relative to the base_location and cookie_height
        chip_obj.location.z = base_location[2] + chip_z_offset


    # --- 3. Tray ---
    tray_size = (cookie_radius * 2.5) * base_scale
    tray_base_z = base_location[2] - (cookie_height * base_scale / 2) - (0.05 * base_scale / 2)

    bpy.ops.mesh.primitive_cube_add(
        size=tray_size,
        location=(base_location[0], base_location[1], tray_base_z)
    )
    tray_obj = bpy.context.active_object
    tray_obj.name = f"{object_name}_Tray"
    
    # Scale height to make it flatter (0.05 is an arbitrary thin factor)
    tray_thickness_factor = kwargs.get('tray_thickness_factor', 0.05)
    tray_obj.scale.z = tray_thickness_factor * base_scale / tray_size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Enter Edit Mode
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(tray_obj.data)
    bm.faces.ensure_lookup_table()

    top_face = None
    for face in bm.faces:
        if face.normal.z > 0.9:
            top_face = face
            break

    if top_face:
        # Inset top face to create a ridge
        bmesh.ops.inset_region(bm, faces=[top_face], thickness=tray_inset_thickness * base_scale, depth=0)
        
        # Find the newly created inner face (it's usually the last one after inset)
        bm.faces.ensure_lookup_table()
        # The new face is likely the active one or accessible via selected faces if bmesh ops handle selection
        # For simplicity, assuming the last face added by inset is the inner one
        inner_face_verts = [v for v in bm.verts if v.select]
        # Extrude the inner face downwards
        extrude_result = bmesh.ops.extrude_face_region(bm, geom=[bm.faces[-1]]) # Extrude the innermost face
        
        # Move the extruded geometry down
        extrude_verts = [v for v in extrude_result['geom'] if isinstance(v, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, verts=extrude_verts, vec=Vector((0, 0, -tray_extrusion_depth * base_scale)))
        
    bmesh.update_edit_mesh(tray_obj.data)
    bpy.ops.object.mode_set(mode='OBJECT') # Exit Edit Mode
    
    tray_obj.data.use_auto_smooth = True
    tray_obj.data.auto_smooth_angle = math.radians(60)
    if tray_obj.data.materials:
        tray_obj.data.materials[0] = tray_mat
    else:
        tray_obj.data.materials.append(tray_mat)
    
    # --- 4. Lighting ---
    # Delete default light if it exists
    if 'Light' in bpy.data.objects:
        default_light = bpy.data.objects['Light']
        if default_light.type == 'LIGHT':
            bpy.data.objects.remove(default_light, do_unlink=True)

    bpy.ops.object.light_add(type='AREA', location=light_location)
    area_light_obj = bpy.context.active_object
    area_light_obj.name = f"{object_name}_AreaLight"
    
    area_light_obj.data.energy = light_power
    area_light_obj.data.color = (1.0, 0.9, 0.8) # Warm white light
    area_light_obj.data.use_temperature = True
    area_light_obj.data.temperature = light_temperature
    area_light_obj.data.size = 2.0 * base_scale
    
    area_light_obj.rotation_euler = (math.radians(60), math.radians(0), math.radians(-30)) # Example rotation

    # --- 5. Camera ---
    if 'Camera' in bpy.data.objects:
        default_camera = bpy.data.objects['Camera']
        if default_camera.type == 'CAMERA':
             bpy.data.objects.remove(default_camera, do_unlink=True)

    camera_pos_offset = Vector((-(base_scale * 3), -(base_scale * 3), (base_scale * 3)))
    bpy.ops.object.camera_add(location=Vector(base_location) + camera_pos_offset)
    camera_obj = bpy.context.active_object
    camera_obj.name = f"{object_name}_Camera"
    
    # Point camera at the cookie (using constraints for simple targeting)
    look_at_constraint = camera_obj.constraints.new(type='TRACK_TO')
    look_at_constraint.target = cookie_obj
    look_at_constraint.track_axis = 'TRACK_NEGATIVE_Z'
    look_at_constraint.up_axis = 'UP_Y'

    # --- Render Settings (for consistency with tutorial outcome) ---
    scene.render.engine = 'CYCLES'
    # Set GPU Compute if available (requires user preferences setup for Cycles)
    # try:
    #     preferences = bpy.context.preferences.addons['cycles'].preferences
    #     preferences.compute_device_type = 'CUDA' # or 'OPTIX', 'OPENCL'
    #     for device in preferences.devices:
    #         if device.type == 'CUDA' or device.type == 'OPTIX':
    #             device.use = True
    #             print(f"Using Cycles device: {device.name}")
    #             break
    #     else:
    #         print("No compatible Cycles GPU device found, falling back to CPU.")
    #         preferences.compute_device_type = 'NONE' # Fallback if no GPU is found
    #     scene.cycles.device = 'GPU' if preferences.compute_device_type != 'NONE' else 'CPU'
    # except Exception as e:
    #     print(f"Could not configure Cycles GPU compute: {e}")
    #     scene.cycles.device = 'CPU'
    
    return f"Created '{object_name}' scene at {base_location} with cookie, chips, tray, and light."
