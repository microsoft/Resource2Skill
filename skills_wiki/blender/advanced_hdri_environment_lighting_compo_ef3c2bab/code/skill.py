def create_object(
    scene_name: str = "Scene",
    object_name: str = "HDRI_Reflection_Probe",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.8, 0.8),
    hdri_filepath: str = "",
    rotation_z: float = 45.0,
    strength: float = 1.0,
    transparent_background: bool = True,
    **kwargs,
) -> str:
    """
    Create an advanced HDRI World Lighting setup and a metallic reflection sphere.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the generated reflection sphere.
        location: (x, y, z) world-space position for the reflection sphere.
        scale: Uniform scale factor for the reflection sphere.
        material_color: (R, G, B) base color for the sphere's material.
        hdri_filepath: Path to an .exr or .hdr file. If empty, falls back to Procedural Sky.
        rotation_z: Rotation of the environment map in degrees.
        strength: Emission strength of the environment lighting.
        transparent_background: If True, makes the world background transparent in renders.

    Returns:
        Status string confirming creation.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create World Shading Environment ===
    # We create a new world to be strictly additive and avoid clearing existing setups
    world = bpy.data.worlds.new(f"World_Lighting_{object_name}")
    scene.world = world
    world.use_nodes = True
    
    tree = world.node_tree
    nodes = tree.nodes
    links = tree.links
    nodes.clear() # Clear default nodes in the *new* world

    # Build node pipeline
    node_tex_coord = nodes.new(type="ShaderNodeTexCoord")
    node_tex_coord.location = (-800, 0)
    
    node_mapping = nodes.new(type="ShaderNodeMapping")
    node_mapping.location = (-600, 0)
    node_mapping.inputs['Rotation'].default_value[2] = math.radians(rotation_z)
    
    node_hsv = nodes.new(type="ShaderNodeHueSaturation")
    node_hsv.location = (-100, 0)
    node_hsv.inputs['Saturation'].default_value = 1.0
    
    node_rgb_curves = nodes.new(type="ShaderNodeRGBCurve")
    node_rgb_curves.location = (100, 0)
    
    node_bg = nodes.new(type="ShaderNodeBackground")
    node_bg.location = (400, 0)
    node_bg.inputs['Strength'].default_value = strength
    
    node_output = nodes.new(type="ShaderNodeOutputWorld")
    node_output.location = (600, 0)

    # Determine lighting source (HDRI file vs Procedural Fallback)
    if hdri_filepath:
        node_env_tex = nodes.new(type="ShaderNodeTexEnvironment")
        node_env_tex.location = (-400, 0)
        try:
            img = bpy.data.images.load(hdri_filepath)
            node_env_tex.image = img
        except Exception as e:
            print(f"Could not load HDRI: {e}. Environment will be untextured.")
            
        links.new(node_tex_coord.outputs['Generated'], node_mapping.inputs['Vector'])
        links.new(node_mapping.outputs['Vector'], node_env_tex.inputs['Vector'])
        links.new(node_env_tex.outputs['Color'], node_hsv.inputs['Color'])
    else:
        # Procedural fallback: Nishita Sky Texture
        node_sky = nodes.new(type="ShaderNodeTexSky")
        node_sky.sky_type = 'NISHITA'
        node_sky.location = (-400, 0)
        links.new(node_sky.outputs['Color'], node_hsv.inputs['Color'])

    # Connect color correction and output links
    links.new(node_hsv.outputs['Color'], node_rgb_curves.inputs['Color'])
    links.new(node_rgb_curves.outputs['Color'], node_bg.inputs['Color'])
    links.new(node_bg.outputs['Background'], node_output.inputs['Surface'])

    # === Step 2: Configure Render Properties ===
    if transparent_background:
        scene.render.film_transparent = True

    # === Step 3: Create Reflection Sphere (To visualize the lighting) ===
    # Fulfills object, location, scale, and material parameters
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.0)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    bpy.ops.object.shade_smooth()
    
    # Create glossy metallic material to catch HDRI reflections
    mat = bpy.data.materials.new(name=f"Mat_Chrome_{object_name}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Metallic"].default_value = 1.0
        bsdf.inputs["Roughness"].default_value = 0.05
        
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    return f"Created World Lighting '{world.name}' and reflection probe '{obj.name}' at {location}."
