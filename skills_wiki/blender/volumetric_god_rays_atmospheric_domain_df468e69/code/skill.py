def create_object(
    scene_name: str = "Scene",
    object_name: str = "VolumetricGodRays",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 10.0,
    material_color: tuple = (1.0, 1.0, 1.0),
    **kwargs,
) -> str:
    """
    Create a localized volumetric fog domain and a driving spotlight for god rays.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position for the center of the fog domain.
        scale: Uniform scale factor for the cubic fog domain.
        material_color: (R, G, B) base color of the fog particles.
        **kwargs: 
            density (float): Density of the volume (default 0.025).
            anisotropy (float): Forward scattering intensity (default 0.6).
            create_spotlight (bool): Whether to create a driving spotlight (default True).
            light_location (tuple): World position of the spotlight (default (0, 0, 8)).
            light_power (float): Energy/power of the spotlight in Watts (default 2000.0).

    Returns:
        Status string describing the generated atmospheric setup.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    # Extract scene and kwargs
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    density = kwargs.get("density", 0.025)
    anisotropy = kwargs.get("anisotropy", 0.6)
    create_spotlight = kwargs.get("create_spotlight", True)
    light_location = kwargs.get("light_location", (0.0, 0.0, 8.0))
    light_power = kwargs.get("light_power", 2000.0)
    light_color = kwargs.get("light_color", (1.0, 0.95, 0.9))  # Slightly warm light

    objects_created = []

    # === Step 1: Create Volumetric Domain Geometry ===
    mesh = bpy.data.meshes.new(name=f"{object_name}_DomainMesh")
    domain_obj = bpy.data.objects.new(name=object_name, object_data=mesh)
    scene.collection.objects.link(domain_obj)
    objects_created.append(domain_obj.name)
    
    # Generate cube geometry (2x2x2 base size)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    bm.to_mesh(mesh)
    bm.free()
    
    # Transform and optimize viewport
    domain_obj.location = Vector(location)
    domain_obj.scale = (scale, scale, scale)
    domain_obj.display_type = 'BOUNDS'  # Keep viewport clear

    # === Step 2: Build Volumetric Shader ===
    mat = bpy.data.materials.new(name=f"{object_name}_VolMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default Surface nodes
    for node in nodes:
        nodes.remove(node)

    # Add Output Node
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (300, 0)

    # Add Principled Volume Node
    vol_node = nodes.new(type='ShaderNodeVolumePrincipled')
    vol_node.location = (0, 0)
    
    # Set Volumetric Properties
    vol_node.inputs['Color'].default_value = (*material_color, 1.0)
    vol_node.inputs['Density'].default_value = density
    vol_node.inputs['Anisotropy'].default_value = anisotropy

    # Link Volume Output to Material Volume Socket
    links.new(vol_node.outputs['Volume'], out_node.inputs['Volume'])
    domain_obj.data.materials.append(mat)

    # === Step 3: Create Driving Spotlight ===
    if create_spotlight:
        light_data = bpy.data.lights.new(name=f"{object_name}_SpotData", type='SPOT')
        light_obj = bpy.data.objects.new(name=f"{object_name}_SpotLight", object_data=light_data)
        scene.collection.objects.link(light_obj)
        objects_created.append(light_obj.name)
        
        # Position light
        light_obj.location = Vector(light_location)
        
        # Track light rotation to point at the center of the volumetric domain
        direction = domain_obj.location - light_obj.location
        if direction.length > 0:
            # -Z is the default forward direction for Spot lights in Blender
            light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
        
        # Configure Light Properties
        light_data.energy = light_power
        light_data.spot_size = math.radians(35)  # Narrow beam
        light_data.spot_blend = 1.0              # Soft edges
        light_data.color = light_color

    # Ensure EEVEE renders volumetrics if it is the active engine
    if scene.render.engine == 'BLENDER_EEVEE':
        try:
            scene.eevee.use_volumetric = True
        except Exception:
            pass

    return f"Created {len(objects_created)} atmospheric objects: {', '.join(objects_created)} at location {location}"
