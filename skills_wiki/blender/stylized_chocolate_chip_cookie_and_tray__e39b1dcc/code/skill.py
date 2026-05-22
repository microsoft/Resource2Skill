def create_blender_cookie_scene(
    scene_name: str = "Scene",
    base_location: tuple = (0, 0, 0),
    scene_scale: float = 1.0,
    cookie_color: tuple = (0.40, 0.22, 0.12),
    chip_color: tuple = (0.19, 0.10, 0.05),
    tray_color: tuple = (0.00, 0.19, 0.81),
    num_chips: int = 15,
    light_power: float = 850.0, # Watts
    light_temp: float = 4000.0, # Kelvin
    **kwargs,
) -> str:
    """
    Create a stylized chocolate chip cookie on a tray scene in Blender.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        base_location: (x, y, z) world-space position for the entire scene.
        scene_scale: Uniform scale factor for all created objects.
        cookie_color: (R, G, B) base color for the cookie in 0-1 range.
        chip_color: (R, G, B) base color for the chocolate chips in 0-1 range.
        tray_color: (R, G, B) base color for the tray in 0-1 range.
        num_chips: Number of chocolate chips to place on the cookie.
        light_power: Power of the area light in Watts.
        light_temp: Temperature of the area light in Kelvin.
        **kwargs: Additional overrides for specific object properties.

    Returns:
        Status string, e.g., "Created 'CookieScene' at (0, 0, 0) with 3 main objects"
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import random
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    bpy.context.window.scene = scene

    # --- 0. Scene Setup (ensure viewport shading is material preview) ---
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL' # Material Preview
                    break
            break

    # --- 1. Materials ---
    def create_pbr_material(mat_name, base_color_rgb, roughness=0.8, metallic=0.0):
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = (*base_color_rgb, 1)
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
        mat.blend_method = 'OPAQUE' # Ensure opaque for solid materials
        return mat

    cookie_mat = create_pbr_material("CookieMaterial", cookie_color, roughness=0.8)
    chip_mat = create_pbr_material("ChipMaterial", chip_color, roughness=0.8)
    tray_mat = create_pbr_material("TrayMaterial", tray_color, roughness=0.8)

    # --- 2. Cookie Base ---
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1.0 * scene_scale,
        depth=0.2 * scene_scale,
        location=Vector(base_location) + Vector((0, 0, 0.1 * scene_scale))
    )
    cookie_obj = bpy.context.active_object
    cookie_obj.name = "Cookie"
    
    # Shade Smooth for cookie base
    bpy.context.view_layer.objects.active = cookie_obj
    bpy.ops.object.shade_smooth()
    cookie_obj.data.materials.append(cookie_mat)

    # --- 3. Chocolate Chips ---
    for i in range(num_chips):
        # Random position on the cookie surface, scaled
        radius = random.uniform(0.1 * scene_scale, 0.8 * scene_scale)
        angle = random.uniform(0, 2 * math.pi)
        
        chip_x = radius * math.cos(angle)
        chip_y = radius * math.sin(angle)
        chip_z = cookie_obj.location.z + (0.1 * scene_scale * 0.5) # Slightly above cookie surface

        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.1 * scene_scale,
            segments=16,
            ring_count=8,
            location=Vector(base_location) + Vector((chip_x, chip_y, chip_z))
        )
        chip_obj = bpy.context.active_object
        chip_obj.name = f"ChocolateChip_{i+1}"
        
        # Shade Smooth for chocolate chip
        bpy.ops.object.shade_smooth()
        chip_obj.data.materials.append(chip_mat)

    # --- 4. Tray ---
    bpy.ops.mesh.primitive_cube_add(
        size=2.5 * scene_scale,
        location=Vector(base_location) + Vector((0, 0, -0.05 * scene_scale))
    )
    tray_obj = bpy.context.active_object
    tray_obj.name = "Tray"
    tray_obj.data.materials.append(tray_mat)
    
    # Switch to Edit Mode for the tray
    bpy.context.view_layer.objects.active = tray_obj
    bpy.ops.object.mode_set(mode='EDIT')
    
    bm = bmesh.from_edit_mesh(tray_obj.data)
    bm.faces.ensure_lookup_table()
    
    # Select top face (assuming the cube is created axis-aligned)
    top_face = None
    for face in bm.faces:
        if face.normal.z > 0.9: # Top face
            top_face = face
            break
            
    if top_face:
        # Inset the top face
        bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.2 * scene_scale, depth=0)
        
        # Get the newly created inner face (it's the top_face after inset)
        bm.faces.ensure_lookup_table()
        inner_face = None
        for face in bm.faces:
             if face.normal.z > 0.9 and face != top_face: # Check for a new top face
                # More robust way to find the new inner face after inset
                # Assuming inset creates one new face at the top which is smaller
                # Simplistic check: find the face that replaced the original top_face
                if all(v.co.z == top_face.calc_center_median().z for v in face.verts):
                    if face.calc_area() < top_face.calc_area():
                        inner_face = face
                        break
        # Fallback if the above doesn't work perfectly (depends on bmesh behavior)
        # Often the inset face will be the newly created smaller face
        if not inner_face:
            # Sort faces by area to find the smallest top face after inset
            top_faces = [f for f in bm.faces if f.normal.z > 0.9]
            if len(top_faces) > 1:
                top_faces.sort(key=lambda f: f.calc_area())
                inner_face = top_faces[0]
            elif len(top_faces) == 1: # if only one top face it's likely the original
                inner_face = top_faces[0]

        if inner_face:
            # Extrude the inner face downwards to create the ridge
            extrude_vector = Vector((0, 0, -0.05 * scene_scale)) # Extrude downwards
            bmesh.ops.extrude_face_region(bm, geom=[inner_face], vec=extrude_vector)
        
    bmesh.update_edit_mesh(tray_obj.data)
    bpy.ops.object.mode_set(mode='OBJECT') # Exit Edit Mode
    tray_obj.select_set(False) # Deselect tray

    # --- 5. Lighting ---
    # Delete default light (if any) - ensure it's not deleted if it's the current selection
    default_light = bpy.data.objects.get('Light')
    if default_light and default_light.name != 'Light': # Avoid deleting the new light if it reuses the name
        bpy.data.objects.remove(default_light, do_unlink=True)

    bpy.ops.object.light_add(
        type='AREA',
        radius=1.0 * scene_scale,
        align='WORLD',
        location=Vector(base_location) + Vector((3 * scene_scale, -3 * scene_scale, 5 * scene_scale)),
        rotation=(math.radians(45), math.radians(0), math.radians(45))
    )
    area_light_obj = bpy.context.active_object
    area_light_obj.name = "AreaLight_Main"
    area_light = area_light_obj.data
    area_light.energy = light_power
    area_light.color = bpy.data.collections["Lights"].objects["AreaLight_Main"].data.color # Get current color
    area_light.node_tree.nodes["Emission"].inputs[1].default_value = light_power # Set power if using nodes
    area_light.node_tree.nodes["Emission"].inputs[0].default_value = (1.0, 0.8, 0.6, 1.0) # Warm white color for temp control
    
    # Set light temperature (Blender uses node setup for color temperature)
    bpy.context.view_layer.objects.active = area_light_obj
    area_light_obj.data.use_nodes = True
    emission_node = area_light_obj.data.node_tree.nodes.get('Emission')
    if emission_node:
        # Add Blackbody node for color temperature
        blackbody_node = area_light_obj.data.node_tree.nodes.new(type='ShaderNodeBlackbody')
        blackbody_node.location = emission_node.location - Vector((200, 0))
        blackbody_node.inputs['Temperature'].default_value = light_temp
        
        # Link Blackbody to Emission color
        area_light_obj.data.node_tree.links.new(blackbody_node.outputs['Color'], emission_node.inputs['Color'])

    # --- 6. Camera Setup ---
    camera_obj = bpy.data.objects.get('Camera')
    if camera_obj:
        camera_obj.location = Vector(base_location) + Vector((6 * scene_scale, -6 * scene_scale, 4 * scene_scale))
        camera_obj.rotation_euler = (math.radians(55), math.radians(0), math.radians(45))
        camera_obj.data.lens = 50 # Focal length in mm
        camera_obj.data.clip_start = 0.1 # Near clipping
        camera_obj.data.clip_end = 1000 # Far clipping
        
        # Lock camera to view (for interactive framing, but uncheck for final render)
        # This is a viewport setting, not object setting
        # for area in bpy.context.window.screen.areas:
        #     if area.type == 'VIEW_3D':
        #         for space in area.spaces:
        #             if space.type == 'VIEW_3D':
        #                 space.region_3d.view_perspective = 'CAMERA'
        #                 space.region_3d.lock_camera_to_views = True
        #                 break
        #         break
    
    # --- 7. Render Settings ---
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU' # Ensure GPU if available and set in preferences
    scene.cycles.samples = 128 # Render samples
    scene.render.image_settings.file_format = 'PNG'
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100

    return f"Created 'CookieScene' at {base_location} with cookie, chips, and tray. Light set with power={light_power}W, temp={light_temp}K."

