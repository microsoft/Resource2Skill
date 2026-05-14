def create_glass_pane(
    scene_name: str = "Scene",
    object_name: str = "GlassPane",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    glass_type: str = "clear",  # Options: "clear", "frosted", "colored"
    glass_color: tuple = (0.5, 0.9, 0.6),  # RGB used if glass_type is "colored"
    thickness: float = 0.05,
    ior: float = 1.49,
    **kwargs,
) -> str:
    """
    Creates a realistic beveled glass pane with configurable material properties.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created object.
        location: (x, y, z) world-space position.
        scale: Overall scale factor for the width/height of the pane.
        glass_type: Defines the material ('clear', 'frosted', or 'colored').
        glass_color: (R, G, B) color in 0-1 range (applied if colored).
        thickness: Depth of the glass pane.
        ior: Index of Refraction (1.49 is typical for glass).
        **kwargs: Overrides (e.g., 'roughness' for frosted glass).

    Returns:
        Status string describing the created object.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    # Get target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry using BMesh ===
    # Using bmesh allows us to define the dimensions accurately without 
    # leaving unapplied object scale, which would distort the Bevel modifier.
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    
    # Scale vertices to make it a thin pane: X/Z are 'scale', Y is 'thickness'
    bmesh.ops.scale(
        bm, 
        vec=(scale, thickness * scale, scale), 
        verts=bm.verts
    )
    
    me = bpy.data.meshes.new(f"{object_name}_Mesh")
    bm.to_mesh(me)
    bm.free()

    # Enable smooth shading on all polygons
    for p in me.polygons:
        p.use_smooth = True

    obj = bpy.data.objects.new(object_name, me)
    scene.collection.objects.link(obj)
    obj.location = Vector(location)

    # === Step 2: Add Bevel Modifier ===
    # Crucial for realistic glass edge highlights and refractions
    bevel = obj.modifiers.new(name="EdgeBevel", type='BEVEL')
    bevel.width = 0.01 * scale
    bevel.segments = 3
    # Use angle limit so flat faces don't get unnecessary geometry
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = 0.523599 # ~30 degrees

    # === Step 3: Build Glass Material ===
    mat_name = f"{object_name}_{glass_type.capitalize()}_Mat"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    
    # EEVEE Compatibility for Refraction
    if hasattr(mat, "use_screen_refraction"):
        mat.use_screen_refraction = True
    if hasattr(scene, "eevee"):
        scene.eevee.use_ssr = True
        if hasattr(scene.eevee, "use_ssr_refraction"):
            scene.eevee.use_ssr_refraction = True

    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")

    # Handle API changes for Transmission (Blender < 4.0 vs 4.0+)
    trans_key = "Transmission Weight" if "Transmission Weight" in bsdf.inputs else "Transmission"
    bsdf.inputs[trans_key].default_value = 1.0
    
    # Set IOR
    bsdf.inputs["IOR"].default_value = ior

    # Apply properties based on glass type
    if glass_type.lower() == "frosted":
        # Scatters light
        roughness_val = kwargs.get("roughness", 0.15)
        bsdf.inputs["Roughness"].default_value = roughness_val
        bsdf.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0)
    elif glass_type.lower() == "colored":
        # Smooth surface, tinted volume
        bsdf.inputs["Roughness"].default_value = 0.0
        # Ensure alpha channel is 1.0
        c_rgba = (glass_color[0], glass_color[1], glass_color[2], 1.0) if len(glass_color) == 3 else glass_color
        bsdf.inputs["Base Color"].default_value = c_rgba
    else:
        # Default Clear Glass
        bsdf.inputs["Roughness"].default_value = 0.0
        bsdf.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0)

    # Assign material to object
    obj.data.materials.append(mat)

    return f"Created '{object_name}' (Type: {glass_type.capitalize()}) at {location} with thickness {thickness}"
