def create_object(
    scene_name: str = "Scene",
    object_name: str = "GradientStudioRig",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (1.0, 1.0, 1.0),
    **kwargs,
) -> str:
    """
    Create a Cinematic Gradient Studio Lighting Rig in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the rig and its components.
        location: (x, y, z) world-space position for the center of the rig.
        scale: Uniform scale factor for the rig size and dummy product.
        material_color: (R, G, B) base color of the emission lights.
        **kwargs: Additional overrides (e.g., 'emission_strength').

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Enable Screen Space Reflections if using EEVEE
    if scene.render.engine == 'BLENDER_EEVEE':
        scene.eevee.use_ssr = True
        
    # Create a collection to organize the rig
    rig_coll = bpy.data.collections.new(object_name)
    scene.collection.children.link(rig_coll)
    
    base_loc = Vector(location)
    emission_strength = kwargs.get('emission_strength', 15.0)
    
    # === Step 1: Create Dummy Product (Glossy Cylinder) ===
    # This provides immediate visual context for the reflections
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=64, 
        radius=0.5 * scale, 
        depth=1.5 * scale, 
        location=base_loc + Vector((0, 0, 0.75 * scale))
    )
    product = bpy.context.active_object
    product.name = f"{object_name}_DummyProduct"
    bpy.ops.object.shade_smooth()
    
    # Add a slight bevel for edge highlights
    bevel = product.modifiers.new(name="Bevel", type='BEVEL')
    bevel.segments = 4
    bevel.width = 0.05 * scale
    
    # Move to rig collection
    rig_coll.objects.link(product)
    scene.collection.objects.unlink(product)
    
    # Product Material (Dark, highly glossy)
    mat_prod = bpy.data.materials.new(name=f"{object_name}_GlossyDark")
    mat_prod.use_nodes = True
    bsdf = mat_prod.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.02, 0.02, 0.02, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.08
        if "Specular IOR Level" in bsdf.inputs:  # Blender 4.0+
            bsdf.inputs["Specular IOR Level"].default_value = 1.0
        elif "Specular" in bsdf.inputs:          # Blender < 4.0
            bsdf.inputs["Specular"].default_value = 1.0
    product.data.materials.append(mat_prod)
    
    # === Step 2: Material Helper for Gradient Lights ===
    def create_light_mat(name, is_gradient=False, bright_at_one=True):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        out = nodes.new('ShaderNodeOutputMaterial')
        emi = nodes.new('ShaderNodeEmission')
        emi.inputs['Strength'].default_value = emission_strength
        
        if not is_gradient:
            emi.inputs['Color'].default_value = (*material_color, 1.0)
            links.new(emi.outputs['Emission'], out.inputs['Surface'])
            return mat
            
        ramp = nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.interpolation = 'B_SPLINE'
        
        c_bright = (*material_color, 1.0)
        c_dark = (0.0, 0.0, 0.0, 1.0)
        
        # Configure the gradient direction
        if bright_at_one:
            ramp.color_ramp.elements[0].color = c_dark
            ramp.color_ramp.elements[1].color = c_bright
        else:
            ramp.color_ramp.elements[0].color = c_bright
            ramp.color_ramp.elements[1].color = c_dark
            
        grad = nodes.new('ShaderNodeTexGradient')
        grad.gradient_type = 'LINEAR'
        
        map_node = nodes.new('ShaderNodeMapping')
        tc = nodes.new('ShaderNodeTexCoord')
        
        links.new(tc.outputs['Generated'], map_node.inputs['Vector'])
        links.new(map_node.outputs['Vector'], grad.inputs['Vector'])
        links.new(grad.outputs['Color'], ramp.inputs['Fac'])
        links.new(ramp.outputs['Color'], emi.inputs['Color'])
        links.new(emi.outputs['Emission'], out.inputs['Surface'])
        
        return mat

    # === Step 3: Create Light Planes ===
    def create_plane_light(name, loc_offset, rot, scale_vec, mat):
        bpy.ops.mesh.primitive_plane_add(size=1, location=base_loc + loc_offset, rotation=rot)
        plane = bpy.context.active_object
        plane.name = name
        plane.scale = scale_vec
        plane.data.materials.append(mat)
        
        # Make invisible to the camera (only visible in reflections and lighting)
        plane.visible_camera = False
        if hasattr(plane, 'cycles_visibility'):
            plane.cycles_visibility.camera = False
        if hasattr(plane, 'cycles'):
            plane.cycles.is_camera_ray = False
            
        rig_coll.objects.link(plane)
        scene.collection.objects.unlink(plane)
        return plane

    # A. Back Light (Solid Emission for Rim Light)
    mat_back = create_light_mat(f"{object_name}_Mat_Back", is_gradient=False)
    create_plane_light(
        f"{object_name}_BackLight",
        Vector((0, 1.5 * scale, 0.75 * scale)),
        (math.radians(90), 0, 0), # Facing -Y (front)
        (2.5 * scale, 3.0 * scale, 1.0 * scale),
        mat_back
    )
    
    # B. Left Light (Gradient, facing +X)
    # Brightest at the back (+Y global), which maps to Local X=1
    mat_left = create_light_mat(f"{object_name}_Mat_Left", is_gradient=True, bright_at_one=True)
    create_plane_light(
        f"{object_name}_LeftLight",
        Vector((-1.5 * scale, 0, 0.75 * scale)),
        (math.radians(90), 0, math.radians(-90)),
        (2.0 * scale, 3.0 * scale, 1.0 * scale),
        mat_left
    )
    
    # C. Right Light (Gradient, facing -X)
    # Brightest at the back (+Y global), which maps to Local X=0
    mat_right = create_light_mat(f"{object_name}_Mat_Right", is_gradient=True, bright_at_one=False)
    create_plane_light(
        f"{object_name}_RightLight",
        Vector((1.5 * scale, 0, 0.75 * scale)),
        (math.radians(90), 0, math.radians(90)),
        (2.0 * scale, 3.0 * scale, 1.0 * scale),
        mat_right
    )
    
    return f"Created '{object_name}' rig at {location} with 3 planes and 1 dummy product."
