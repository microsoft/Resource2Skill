def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyCrate",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.4, 0.2, 0.05),
    **kwargs,
) -> str:
    """
    Create a Low-Poly Stylized Crate game asset in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the outer frame.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created object.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Material Setup ===
    # Frame Material (Outer Structure)
    mat_frame = bpy.data.materials.new(name=f"{object_name}_FrameMat")
    mat_frame.use_nodes = True
    bsdf_frame = mat_frame.node_tree.nodes.get("Principled BSDF")
    if bsdf_frame:
        bsdf_frame.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf_frame.inputs["Roughness"].default_value = 0.9

    # Panel Material (Inner Recessed Faces - Darker)
    inner_color = (
        max(0.0, material_color[0] * 0.5), 
        max(0.0, material_color[1] * 0.5), 
        max(0.0, material_color[2] * 0.5), 
        1.0
    )
    mat_inner = bpy.data.materials.new(name=f"{object_name}_PanelMat")
    mat_inner.use_nodes = True
    bsdf_inner = mat_inner.node_tree.nodes.get("Principled BSDF")
    if bsdf_inner:
        bsdf_inner.inputs["Base Color"].default_value = inner_color
        bsdf_inner.inputs["Roughness"].default_value = 0.95

    # === Step 2: Base Geometry ===
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    obj.data.materials.append(mat_frame) # Index 0
    obj.data.materials.append(mat_inner) # Index 1

    bm = bmesh.new()
    # Create base cube
    bmesh.ops.create_cube(bm, size=2.0)

    # Assign frame material to all base faces
    for f in bm.faces:
        f.material_index = 0

    # Inset all faces individually to generate the wooden frame boundary
    inset_res = bmesh.ops.inset_individual(bm, faces=list(bm.faces), thickness=0.2)
    inner_faces = inset_res.get('faces', [])

    # Extrude the newly created inner faces to prepare them for recessing
    ext_res = bmesh.ops.extrude_discrete_faces(bm, faces=inner_faces)
    extruded_faces = ext_res.get('faces', [])

    # Push the extruded cap faces inward along their normals and assign the darker material
    for f in extruded_faces:
        bmesh.ops.translate(bm, verts=f.verts, vec=f.normal * -0.15)
        f.material_index = 1

    bm.to_mesh(mesh)
    bm.free()

    # Apply smooth shading to the polygons (modifiers will handle sharp edges)
    for poly in mesh.polygons:
        poly.use_smooth = True

    # === Step 3: Modifiers for Game Assets ===
    # Bevel modifier to catch edge highlights (a standard game art workflow)
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.04
    bevel.segments = 2
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = 0.5  # ~28 degrees to only bevel the sharp 90 degree frame corners

    # Triangulate modifier (forces predictable geometry for game engines)
    tri = obj.modifiers.new(name="Triangulate", type='TRIANGULATE')
    tri.keep_custom_normals = True

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' (Low-Poly Game Prop) at {location} with {len(mesh.polygons)} faces."
