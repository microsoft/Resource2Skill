def create_object(
    scene_name: str = "Scene",
    object_name: str = "FuzzyPuff",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.15, 0.3),  # Deep pinkish red
    hair_length: float = 0.3,
    hair_count: int = 1500,
    **kwargs,
) -> str:
    """
    Create a Procedural Stylized Fur/Hair Sphere in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the fur roots.
        hair_length: Length of the hair particles.
        hair_count: Number of parent hairs.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (UV Sphere) ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1.0)
    bm.to_mesh(mesh)
    bm.free()
    
    for poly in mesh.polygons:
        poly.use_smooth = True

    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))

    # === Step 2: Modifiers (Subsurf & Displace) ===
    subsurf = obj.modifiers.new(name="Smooth", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    disp_tex = bpy.data.textures.new(f"{object_name}_DispTex", type='CLOUDS')
    disp_tex.noise_scale = 1.2
    
    disp_mod = obj.modifiers.new(name="OrganicShape", type='DISPLACE')
    disp_mod.texture = disp_tex
    disp_mod.strength = 0.15

    # === Step 3: Material with Root-to-Tip Gradient ===
    mat = bpy.data.materials.new(name=f"{object_name}_FurMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (300, 0)
    
    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (0, 0)
    if 'Roughness' in bsdf_node.inputs:
        bsdf_node.inputs['Roughness'].default_value = 0.75
        
    color_input = bsdf_node.inputs.get('Base Color') or bsdf_node.inputs.get('Base') or bsdf_node.inputs[0]
    color_input.default_value = (*material_color, 1.0)
    
    # Try to add Hair Info gradient (makes tips lighter)
    try:
        hair_info = nodes.new('ShaderNodeHairInfo')
        hair_info.location = (-400, 0)
        
        color_ramp = nodes.new('ShaderNodeValToRGB')
        color_ramp.location = (-200, 0)
        
        # Root color
        color_ramp.color_ramp.elements[0].color = (*material_color, 1.0)
        color_ramp.color_ramp.elements[0].position = 0.1
        
        # Tip color (Lighter and slightly desaturated)
        tip_color = (min(material_color[0] + 0.35, 1.0), 
                     min(material_color[1] + 0.35, 1.0), 
                     min(material_color[2] + 0.35, 1.0), 1.0)
        color_ramp.color_ramp.elements[1].color = tip_color
        color_ramp.color_ramp.elements[1].position = 0.9
        
        links.new(hair_info.outputs['Intercept'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], color_input)
    except Exception:
        pass # Fallback to solid color if nodes are unavailable in current version
        
    links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])
    obj.data.materials.append(mat)

    # === Step 4: Particle System (Hair) ===
    # Workaround to safely add a particle system via ops to avoid context/data issues
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.particle_system_add()
    
    ps = obj.particle_systems[0]
    ps.name = f"{object_name}_HairSystem"
    pset = ps.settings
    pset.name = f"{object_name}_HairSettings"
    
    pset.type = 'HAIR'
    pset.count = hair_count
    pset.hair_length = hair_length
    if hasattr(pset, "use_advanced_hair"):
        pset.use_advanced_hair = True
        
    # Children settings (Performance vs Render)
    pset.child_type = 'INTERPOLATED'
    pset.child_nbr = 10              # Viewport count
    pset.rendered_child_count = 60   # Render count
    
    # Styling (Tufts and Waves)
    pset.clump_factor = -0.6         # Clumps hair together slightly
    pset.roughness_random = 0.05
    pset.roughness_endpoint = 0.03
    
    pset.kink = 'CURL'
    pset.kink_amplitude = 0.06
    pset.kink_frequency = 2.5
    
    pset.material = 1 # Force use of the first material slot for hair rendering

    # === Step 5: Dramatic Fur Lighting (Additive) ===
    # Key Light
    key_light_data = bpy.data.lights.new(name=f"{object_name}_KeyLight", type='AREA')
    key_light_data.energy = 800.0
    key_light_data.color = (1.0, 0.95, 0.9)
    key_light_data.size = 2.0
    key_light_obj = bpy.data.objects.new(name=f"{object_name}_KeyLight", object_data=key_light_data)
    scene.collection.objects.link(key_light_obj)
    key_light_obj.location = Vector(location) + Vector((3, -3, 3)) * scale
    
    # Rim Light (Crucial for fur aesthetics)
    rim_light_data = bpy.data.lights.new(name=f"{object_name}_RimLight", type='AREA')
    rim_light_data.energy = 2500.0
    rim_light_data.color = (0.7, 0.85, 1.0)
    rim_light_data.size = 4.0
    rim_light_obj = bpy.data.objects.new(name=f"{object_name}_RimLight", object_data=rim_light_data)
    scene.collection.objects.link(rim_light_obj)
    rim_light_obj.location = Vector(location) + Vector((-4, 4, 1)) * scale
    
    # Helper to point lights at the fuzzy object
    def point_at(light_obj, target_loc):
        direction = target_loc - light_obj.location
        light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
        
    point_at(key_light_obj, obj.location)
    point_at(rim_light_obj, obj.location)

    return f"Created '{object_name}' (Fuzzy Sphere) at {location} with {hair_count} base hairs, interpolated children, and dual-lighting setup."
