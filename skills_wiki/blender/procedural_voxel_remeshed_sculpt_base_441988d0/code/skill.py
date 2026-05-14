def create_object(
    scene_name: str = "Scene",
    object_name: str = "OrganicSculptBase",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.65, 0.55, 0.45),
    **kwargs,
) -> str:
    """
    Creates a perfectly uniform, voxel-remeshed organic base ready for Sculpt Mode.
    
    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color mimicking digital clay.
        **kwargs: 
            voxel_size (float): The resolution of the remesh (lower = higher poly). Default 0.02.
            deform_strength (float): How chaotic the initial blob shape is. Default 0.6.
            
    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    # Extract kwargs
    voxel_size = kwargs.get("voxel_size", 0.02)
    deform_strength = kwargs.get("deform_strength", 0.6)

    # Ensure we don't accidentally operate on existing objects
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    # === Step 1: Create Base Geometry (Ico Sphere) ===
    # The instructor explicitly deletes the default cube and uses an Ico Sphere
    # for better, pole-free topology.
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=5, 
        radius=1.0, 
        location=location
    )
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = (scale, scale, scale)

    # === Step 2: Simulate Initial Sculpting Volumes ===
    # Since we cannot script manual mouse strokes, we use a procedural displacement
    # to simulate the "Grab", "Blob", and "Inflate" brushes to create an organic starting shape.
    tex_name = f"{object_name}_DeformTex"
    tex = bpy.data.textures.get(tex_name)
    if not tex:
        tex = bpy.data.textures.new(name=tex_name, type='CLOUDS')
        tex.noise_scale = 1.5
        tex.noise_depth = 2

    disp_mod = obj.modifiers.new(name="SimulateSculptVolume", type='DISPLACE')
    disp_mod.texture = tex
    disp_mod.strength = deform_strength
    disp_mod.mid_level = 0.5

    # === Step 3: Apply Voxel Remesh ===
    # This replicates the Ctrl+R workflow to unify the topology and remove 
    # the stretching caused by the displacement.
    remesh_mod = obj.modifiers.new(name="TopologyFix", type='REMESH')
    remesh_mod.mode = 'VOXEL'
    remesh_mod.voxel_size = voxel_size
    remesh_mod.use_smooth_shade = True

    # Apply the modifiers to bake the geometry into a raw, sculptable mesh
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier="SimulateSculptVolume")
    bpy.ops.object.modifier_apply(modifier="TopologyFix")

    # Ensure smooth shading
    bpy.ops.object.shade_smooth()

    # === Step 4: Build Digital Clay Material ===
    mat_name = f"{object_name}_ClayMat"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        
        # Configure Principled BSDF for a matte clay look
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
            # High roughness, low specular for easy cavity reading during sculpting
            bsdf.inputs['Roughness'].default_value = 0.85
            if 'Specular IOR Level' in bsdf.inputs: # Blender 4.0+
                bsdf.inputs['Specular IOR Level'].default_value = 0.1
            elif 'Specular' in bsdf.inputs: # Older Blender versions
                bsdf.inputs['Specular'].default_value = 0.1
            
    # Assign material
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    # Deselect the object to leave the scene clean
    obj.select_set(False)

    return f"Created Sculpt Base '{obj.name}' at {location} (Voxel Size: {voxel_size}). Ready for Sculpt Mode."
