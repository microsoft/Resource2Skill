def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPolyWell",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    stone_color: tuple = (0.5, 0.5, 0.53),
    wood_color: tuple = (0.25, 0.12, 0.05),
    roof_color: tuple = (0.7, 0.15, 0.15),
    **kwargs,
) -> str:
    """
    Create a Stylized Low-Poly Well in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the master object/empty.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        stone_color: (R, G, B) color for the well base.
        wood_color: (R, G, B) color for the wooden supports.
        roof_color: (R, G, B) color for the tiled roof.

    Returns:
        Status string describing the created geometry.
    """
    import bpy
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Helper function to generate clean, matte PBR materials
    def make_material(name, color):
        mat = bpy.data.materials.get(name)
        if not mat:
            mat = bpy.data.materials.new(name)
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs['Base Color'].default_value = (*color, 1.0)
                bsdf.inputs['Roughness'].default_value = 0.9  # High roughness for stylized look
                bsdf.inputs['Metallic'].default_value = 0.0
                bsdf.inputs['Specular IOR Level'].default_value = 0.2
        return mat

    mat_stone = make_material(f"{object_name}_StoneMat", stone_color)
    mat_wood = make_material(f"{object_name}_WoodMat", wood_color)
    mat_roof = make_material(f"{object_name}_RoofMat", roof_color)

    # 1. Create a Master Empty to control the entire asset
    empty = bpy.data.objects.new(object_name, None)
    empty.location = location
    empty.scale = (scale, scale, scale)
    scene.collection.objects.link(empty)

    created_objects = []

    # 2. Well Base (Stone)
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=1.2, depth=1.0, location=(0, 0, 0.5))
    base_obj = bpy.context.active_object
    base_obj.name = f"{object_name}_Base"
    base_obj.data.materials.append(mat_stone)
    base_obj.parent = empty
    created_objects.append(base_obj)

    # Hollow out the well using a boolean difference
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.9, depth=1.2, location=(0, 0, 0.6))
    hole_obj = bpy.context.active_object

    bool_mod = base_obj.modifiers.new(name="Hole", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = hole_obj

    # Apply the boolean modifier for a clean, game-ready mesh
    bpy.context.view_layer.objects.active = base_obj
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(hole_obj, do_unlink=True)

    # 3. Wooden Struts (Left & Right)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-1.0, 0, 1.5))
    strut_l = bpy.context.active_object
    strut_l.name = f"{object_name}_Strut_L"
    strut_l.scale = (0.2, 0.2, 3.0)
    strut_l.data.materials.append(mat_wood)
    strut_l.parent = empty
    created_objects.append(strut_l)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(1.0, 0, 1.5))
    strut_r = bpy.context.active_object
    strut_r.name = f"{object_name}_Strut_R"
    strut_r.scale = (0.2, 0.2, 3.0)
    strut_r.data.materials.append(mat_wood)
    strut_r.parent = empty
    created_objects.append(strut_r)

    # 4. Wooden Crossbeam
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.1, depth=2.4, location=(0, 0, 2.5))
    beam = bpy.context.active_object
    beam.name = f"{object_name}_Crossbeam"
    beam.rotation_euler = (0, math.radians(90), 0)
    beam.data.materials.append(mat_wood)
    beam.parent = empty
    created_objects.append(beam)

    # 5. Roof (Red) - using a 3-sided cylinder to create a triangular prism
    bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1.4, depth=2.8, location=(0, 0, 3.2))
    roof = bpy.context.active_object
    roof.name = f"{object_name}_Roof"
    roof.rotation_euler = (math.radians(90), 0, 0)
    roof.scale = (1.0, 1.0, 0.6)  # Squish vertically to make an attractive roof slope
    roof.data.materials.append(mat_roof)
    roof.parent = empty
    created_objects.append(roof)

    # 6. Enforce flat shading across all components for the low-poly aesthetic
    for obj in created_objects:
        if obj.type == 'MESH':
            for poly in obj.data.polygons:
                poly.use_smooth = False

    return f"Created '{object_name}' (Stylized Low-Poly Well) at {location} consisting of {len(created_objects)} meshes grouped under an Empty."
