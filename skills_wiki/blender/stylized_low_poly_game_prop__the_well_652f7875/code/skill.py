def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyWell",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.7, 0.1, 0.1),  # Default roof color
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Well in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the root container object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the roof.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # --- Helper: Material Creation ---
    def create_solid_mat(name, color_rgb, roughness):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # color_rgb + alpha
            bsdf.inputs["Base Color"].default_value = (*color_rgb, 1.0)
            bsdf.inputs["Roughness"].default_value = roughness
        return mat

    # Define Materials
    mat_stone = create_solid_mat(f"{object_name}_Stone", (0.5, 0.5, 0.5), 0.9)
    mat_wood = create_solid_mat(f"{object_name}_Wood", (0.25, 0.12, 0.05), 0.8)
    mat_rope = create_solid_mat(f"{object_name}_Rope", (0.8, 0.7, 0.5), 0.9)
    mat_water = create_solid_mat(f"{object_name}_Water", (0.1, 0.4, 0.8), 0.1)
    mat_roof = create_solid_mat(f"{object_name}_Roof", material_color, 0.9)

    created_parts = []

    # --- 1. Stone Base (Hollow Tube via BMesh) ---
    mesh_base = bpy.data.meshes.new(f"{object_name}_BaseMesh")
    base_obj = bpy.data.objects.new(f"{object_name}_Base", mesh_base)
    scene.collection.objects.link(base_obj)
    
    bm = bmesh.new()
    # cap_ends=False makes it a tube
    bmesh.ops.create_cone(bm, cap_ends=False, cap_tris=False, segments=12, radius1=1.2, radius2=1.2, depth=1.0)
    bm.to_mesh(mesh_base)
    bm.free()
    
    base_obj.location.z = 0.5  # Sits on ground (0 to 1.0)
    base_obj.data.materials.append(mat_stone)
    
    # Add thickness
    solidify = base_obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = 0.25
    solidify.offset = -1.0 # Grow inwards
    created_parts.append(base_obj)

    # --- 2. Water ---
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=1.0, depth=0.1, location=(0, 0, 0.6))
    water_obj = bpy.context.active_object
    water_obj.name = f"{object_name}_Water"
    water_obj.data.materials.append(mat_water)
    created_parts.append(water_obj)

    # --- 3. Wooden Pillars ---
    # Left Pillar
    bpy.ops.mesh.primitive_cube_add(size=1, scale=(0.25, 0.25, 3.0), location=(1.05, 0, 1.5))
    pillar_l = bpy.context.active_object
    pillar_l.name = f"{object_name}_PillarL"
    pillar_l.data.materials.append(mat_wood)
    created_parts.append(pillar_l)

    # Right Pillar
    bpy.ops.mesh.primitive_cube_add(size=1, scale=(0.25, 0.25, 3.0), location=(-1.05, 0, 1.5))
    pillar_r = bpy.context.active_object
    pillar_r.name = f"{object_name}_PillarR"
    pillar_r.data.materials.append(mat_wood)
    created_parts.append(pillar_r)

    # --- 4. Crossbeam & Rope ---
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.12, depth=2.8, location=(0, 0, 2.7))
    beam = bpy.context.active_object
    beam.name = f"{object_name}_Beam"
    beam.rotation_euler[1] = math.pi / 2
    beam.data.materials.append(mat_wood)
    created_parts.append(beam)

    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.04, depth=1.6, location=(0, 0, 1.9))
    rope = bpy.context.active_object
    rope.name = f"{object_name}_Rope"
    rope.data.materials.append(mat_rope)
    created_parts.append(rope)

    # --- 5. Pyramid Roof ---
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=1.9, depth=1.2, location=(0, 0, 3.6))
    roof = bpy.context.active_object
    roof.name = f"{object_name}_Roof"
    roof.rotation_euler[2] = math.pi / 4  # Rotate to align flat sides with pillars
    roof.data.materials.append(mat_roof)
    created_parts.append(roof)

    # --- Grouping & Final Setup ---
    # Create root empty
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = object_name

    # Enforce flat shading and parent to root
    for obj in created_parts:
        obj.parent = root
        if obj.type == 'MESH':
            for poly in obj.data.polygons:
                poly.use_smooth = False

    # Apply global transforms
    root.location = Vector(location)
    root.scale = (scale, scale, scale)

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created '{object_name}' (Stylized Low-Poly Well) at {location} consisting of {len(created_parts)} meshes."
