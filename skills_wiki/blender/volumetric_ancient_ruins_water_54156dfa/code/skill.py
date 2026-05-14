def create_object(
    scene_name: str = "Scene",
    object_name: str = "AncientRuinsWater",
    location: tuple = (0, 0, 0),
    scale: float = 10.0,
    material_color: tuple = (0.1, 0.7, 0.6),
    **kwargs,
) -> str:
    """
    Create a volumetric body of water using the Light Path Shadow hack and Volume Absorption.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the pool area.
        material_color: (R, G, B) water absorption color (teal/cyan by default).

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Pool Floor Context ===
    # Volume absorption needs a surface underneath to be visually apparent
    floor_z = location[2] - (scale * 0.2)
    bpy.ops.mesh.primitive_plane_add(size=scale*2.2, location=(location[0], location[1], floor_z))
    floor = bpy.context.active_object
    floor.name = f"{object_name}_Floor"
    
    floor_mat = bpy.data.materials.new(name=f"{object_name}_Floor_Mat")
    floor_mat.use_nodes = True
    if floor_mat.node_tree.nodes.get("Principled BSDF"):
        floor_mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.6, 0.5, 0.4, 1.0)
    floor.data.materials.append(floor_mat)

    # === Step 2: Create Water Volume Geometry ===
    bpy.ops.mesh.primitive_cube_add(size=2, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    
    # Scale to create a wide, flat body of water and APPLY scale (crucial for uniform noise)
    obj.scale = (scale, scale, scale * 0.2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # === Step 3: Build Water Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    # Eevee-specific settings for transparency (fallback, though Cycles is recommended)
    mat.blend_method = 'HASHED'
    mat.shadow_method = 'NONE'
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create Nodes
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)

    # --- Surface Shader Network ---
    mix_surface = nodes.new('ShaderNodeMixShader')
    mix_surface.location = (600, 200)

    light_path = nodes.new('ShaderNodeLightPath')
    light_path.location = (200, 400)

    glass = nodes.new('ShaderNodeBsdfGlass')
    glass.location = (200, 200)
    glass.inputs['IOR'].default_value = 1.33 # Water Index of Refraction
    
    transparent = nodes.new('ShaderNodeBsdfTransparent')
    transparent.location = (200, 0)

    bump = nodes.new('ShaderNodeBump')
    bump.location = (0, 100)
    bump.inputs['Strength'].default_value = 0.05
    bump.inputs['Distance'].default_value = 1.0

    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-200, 100)
    noise.inputs['Scale'].default_value = 120.0

    # --- Volume Shader Network ---
    add_vol = nodes.new('ShaderNodeAddShader')
    add_vol.location = (600, -200)

    vol_absorp = nodes.new('ShaderNodeVolumeAbsorption')
    vol_absorp.location = (400, -200)
    vol_absorp.inputs['Color'].default_value = (*material_color, 1.0)
    vol_absorp.inputs['Density'].default_value = 0.3

    prin_vol = nodes.new('ShaderNodeVolumePrincipled')
    prin_vol.location = (400, -400)
    prin_vol.inputs['Color'].default_value = (*material_color, 1.0)
    
    # Safely handle Blender API changes for Emission in Principled Volume
    if 'Emission Color' in prin_vol.inputs:
        prin_vol.inputs['Emission Color'].default_value = (*material_color, 1.0)
    elif 'Emission' in prin_vol.inputs:
        prin_vol.inputs['Emission'].default_value = (*material_color, 1.0)
        
    if 'Emission Strength' in prin_vol.inputs:
        prin_vol.inputs['Emission Strength'].default_value = 0.1

    # --- Connect the Graph ---
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], glass.inputs['Normal'])
    
    # Shadow Ray Hack: If shadow ray (1), use Transparent. If not (0), use Glass.
    links.new(light_path.outputs['Is Shadow Ray'], mix_surface.inputs['Fac'])
    links.new(glass.outputs['BSDF'], mix_surface.inputs[1])      
    links.new(transparent.outputs['BSDF'], mix_surface.inputs[2]) 
    links.new(mix_surface.outputs['Shader'], output.inputs['Surface'])

    # Volumes combined
    links.new(vol_absorp.outputs['Volume'], add_vol.inputs[0])
    links.new(prin_vol.outputs['Volume'], add_vol.inputs[1])
    links.new(add_vol.outputs['Shader'], output.inputs['Volume'])

    # Assign Material
    obj.data.materials.append(mat)

    # === Step 4: Environment Context ===
    # Add a Sun light to ensure the glass ripples refract properly
    sun = bpy.data.lights.new(name=f"{object_name}_Sun", type='SUN')
    sun.energy = 10.0
    sun.angle = math.radians(2.0)
    sun_obj = bpy.data.objects.new(name=f"{object_name}_SunObj", object_data=sun)
    scene.collection.objects.link(sun_obj)
    sun_obj.location = (location[0], location[1], location[2] + 10)
    sun_obj.rotation_euler = (math.radians(45), math.radians(30), math.radians(45))

    return f"Created '{object_name}' with volumetric water shader, pool floor, and sun light at {location}"
