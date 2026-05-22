def create_object(
    scene_name: str = "Scene",
    object_name: str = "SeamlessBoxProjected_Part",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.4, 0.8),
    **kwargs,
) -> str:
    """
    Create a mechanical part mapped with a seamless Box Projection PBR setup.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the material.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    bm = bmesh.new()
    # Create the base cylindrical flange
    bmesh.ops.create_cone(
        bm, 
        cap_ends=True, 
        cap_tris=False, 
        segments=32, 
        radius1=1.0, 
        radius2=1.0, 
        depth=0.5
    )

    # Reconstruct the inner geometry shown in the tutorial
    top_face = next((f for f in bm.faces if f.normal.z > 0.9), None)

    if top_face:
        # First inset
        res1 = bmesh.ops.inset_region(bm, faces=[top_face], thickness=0.3)
        inner_face1 = next((f for f in res1['faces'] if f.normal.z > 0.9), None)
        
        if inner_face1:
            # First extrude (upwards center column)
            res2 = bmesh.ops.extrude_discrete_faces(bm, faces=[inner_face1])
            ext_face1 = res2['faces'][0]
            for v in ext_face1.verts:
                v.co.z += 0.4
                
            # Second inset
            res3 = bmesh.ops.inset_region(bm, faces=[ext_face1], thickness=0.15)
            inner_face2 = next((f for f in res3['faces'] if f.normal.z > 0.9), None)
            
            if inner_face2:
                # Second extrude (downwards center hole)
                res4 = bmesh.ops.extrude_discrete_faces(bm, faces=[inner_face2])
                ext_face2 = res4['faces'][0]
                for v in ext_face2.verts:
                    v.co.z -= 0.3

    # Apply scale directly to mesh data (crucial for Bevel modifier uniformity)
    for v in bm.verts:
        v.co *= scale

    # Convert bmesh to standard mesh object
    mesh = bpy.data.meshes.new(f"{object_name}_mesh")
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(object_name, mesh)
    obj.location = Vector(location)
    scene.collection.objects.link(obj)

    # Enable smooth shading for all faces
    for poly in mesh.polygons:
        poly.use_smooth = True

    # === Step 2: Modifiers ===
    # Bevel sharp edges
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(30)
    bevel.width = 0.02 * scale
    bevel.segments = 3

    # Add Subdivision Surface
    subdiv = obj.modifiers.new(name="Subdiv", type='SUBSURF')
    subdiv.levels = 2
    subdiv.render_levels = 2

    # === Step 3: Box Projection Material Setup ===
    mat = bpy.data.materials.new(name=f"{object_name}_BoxProj_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core BSDF Node
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.7

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Coordinate and Mapping setup
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    mapping.inputs['Scale'].default_value = (2.0, 2.0, 2.0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # Generate an internal pattern to act as our "PBR Image Texture"
    img = bpy.data.images.new(name="Internal_BoxProj_Grid", width=1024, height=1024)
    img.generated_type = 'COLOR_GRID'

    # The Core Technique: Image Texture set to BOX projection
    img_tex = nodes.new('ShaderNodeTexImage')
    img_tex.location = (-350, 0)
    img_tex.image = img
    img_tex.projection = 'BOX'
    img_tex.projection_blend = 0.25  # Blends the seams together
    links.new(mapping.outputs['Vector'], img_tex.inputs['Vector'])

    # Connect the projection to Roughness and Bump to clearly visualize the wrap
    links.new(img_tex.outputs['Color'], bsdf.inputs['Roughness'])

    bump = nodes.new('ShaderNodeBump')
    bump.location = (-250, -250)
    bump.inputs['Strength'].default_value = 0.4
    links.new(img_tex.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    # Assign material
    obj.data.materials.append(mat)

    return f"Created '{obj.name}' mapped seamlessly via Box Projection at {location}."
