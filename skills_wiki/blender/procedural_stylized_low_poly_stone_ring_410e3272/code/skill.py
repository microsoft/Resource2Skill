def create_low_poly_well_base(
    scene_name: str = "Scene",
    object_name: str = "LowPolyWellBase",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.4, 0.38, 0.38),
    radius: float = 1.2,
    layers: int = 3,
    stones_per_layer: int = 12,
    stone_height: float = 0.3,
    stone_thickness: float = 0.4
) -> str:
    """
    Creates a stylized, low-poly circular stone base (e.g., for a well) 
    using a non-destructive modifier stack to generate wobbly, faceted stones.

    Args:
        scene_name: Target scene.
        object_name: Name of the generated object.
        location: World-space position.
        scale: Uniform scale factor.
        material_color: RGB tuple for the stone color.
        radius: Distance from the center to the center of the stones.
        layers: Number of vertically stacked stone rings.
        stones_per_layer: Number of individual stones per ring.
        stone_height: Vertical height of each stone.
        stone_thickness: Radial depth of each stone.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Matrix, Euler, Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create the Disjoint Base Geometry via BMesh ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()

    # Calculate stone width to fit the circumference with a small gap (90% coverage)
    circumference = 2 * math.pi * radius
    stone_width = (circumference / stones_per_layer) * 0.90

    # Build the rings
    for layer in range(layers):
        z_offset = layer * stone_height
        
        # Offset every other layer by half a stone to create an interlocking brick pattern
        angle_offset = (math.pi / stones_per_layer) if layer % 2 != 0 else 0.0
        
        for i in range(stones_per_layer):
            angle = angle_offset + (i / stones_per_layer) * 2 * math.pi
            
            # Transformation stack:
            # 1. Scale the 1x1x1 unit cube to stone dimensions
            # 2. Translate out by 'radius' along X
            # 3. Rotate around Z by 'angle'
            # 4. Translate up by 'z_offset'
            scale_mat = Matrix.Diagonal((stone_thickness, stone_width, stone_height, 1.0))
            loc_x_mat = Matrix.Translation((radius, 0.0, 0.0))
            rot_z_mat = Euler((0.0, 0.0, angle)).to_matrix().to_4x4()
            loc_z_mat = Matrix.Translation((0.0, 0.0, z_offset))
            
            # Matrix multiplication applies right-to-left in Blender Python
            final_mat = loc_z_mat @ rot_z_mat @ loc_x_mat @ scale_mat
            
            # Create the block at the correct location
            bmesh.ops.create_cube(bm, size=1.0, matrix=final_mat)

    # Write bmesh data to the object
    bm.to_mesh(mesh)
    bm.free()

    # Ensure flat shading initially so the Decimate modifier looks correct
    for poly in mesh.polygons:
        poly.use_smooth = False

    # === Step 2: Build the Procedural Stylization Modifiers ===
    
    # 2a. Bevel - Rounds off the sharp corners of the base blocks
    mod_bevel = obj.modifiers.new(name="StoneBevel", type='BEVEL')
    mod_bevel.width = 0.04
    mod_bevel.segments = 2
    mod_bevel.limit_method = 'ANGLE'

    # 2b. Subdivision - Adds internal geometry so the Displace has vertices to move
    mod_subdiv = obj.modifiers.new(name="StoneSubdiv", type='SUBSURF')
    mod_subdiv.subdivision_type = 'SIMPLE'
    mod_subdiv.levels = 2

    # 2c. Displace - Pushes vertices randomly to create the "wobble"
    tex_name = "StoneWobble_Tex"
    wobble_tex = bpy.data.textures.get(tex_name)
    if not wobble_tex:
        wobble_tex = bpy.data.textures.new(name=tex_name, type='CLOUDS')
        wobble_tex.noise_scale = 0.6
        
    mod_displace = obj.modifiers.new(name="StoneDisplace", type='DISPLACE')
    mod_displace.texture = wobble_tex
    mod_displace.strength = 0.08  # The amount of randomness/wobble
    mod_displace.mid_level = 0.5

    # 2d. Decimate - Collapses the wobbly mesh into a stylized, faceted low-poly look
    mod_decimate = obj.modifiers.new(name="StoneDecimate", type='DECIMATE')
    mod_decimate.ratio = 0.35  # Reduces geometry by 65%, causing jagged planar facets

    # === Step 3: Build Material ===
    mat_name = f"{object_name}_Stone_Mat"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Set base color and high roughness for dry stone
            bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.95
            bsdf.inputs['Specular IOR Level'].default_value = 0.2

    # Assign material
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # Force view layer update so modifiers evaluate correctly
    bpy.context.view_layer.update()

    total_stones = layers * stones_per_layer
    return f"Created '{obj.name}' at {location}. Generated {total_stones} stones across {layers} layers with procedural low-poly faceting."
