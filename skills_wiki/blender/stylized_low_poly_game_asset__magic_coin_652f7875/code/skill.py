def create_object(
    scene_name: str = "Scene",
    object_name: str = "LowPoly_MagicCoin",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (1.0, 0.75, 0.05), # Gold Rim
    glow_color: tuple = (0.0, 0.8, 1.0),       # Cyan Inner Glow
    **kwargs,
) -> str:
    """
    Create a game-ready Low-Poly Emissive Coin in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the metallic rim.
        glow_color: (R, G, B) emissive color for the magical core.

    Returns:
        Status string confirming creation.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    # Target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    # Using 16 vertices for a distinct stylized, low-poly look
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16, 
        radius=1.0, 
        depth=0.2, 
        location=location
    )
    obj = bpy.context.active_object
    obj.name = object_name
    
    # Enforce flat shading for the faceted low-poly aesthetic
    bpy.ops.object.shade_flat()

    # === Step 2: Build Materials ===
    # 1. Metallic Gold Rim
    gold_mat = bpy.data.materials.new(name=f"{object_name}_Gold")
    gold_mat.use_nodes = True
    bsdf = gold_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Metallic'].default_value = 1.0
        bsdf.inputs['Roughness'].default_value = 0.3

    # 2. Emissive Glowing Core
    glow_mat = bpy.data.materials.new(name=f"{object_name}_Glow")
    glow_mat.use_nodes = True
    glow_nodes = glow_mat.node_tree.nodes
    glow_nodes.clear()
    
    emission = glow_nodes.new(type='ShaderNodeEmission')
    emission.inputs['Color'].default_value = (*glow_color, 1.0)
    emission.inputs['Strength'].default_value = 5.0
    
    output = glow_nodes.new(type='ShaderNodeOutputMaterial')
    glow_mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])

    # Append materials (Index 0 = Gold, Index 1 = Glow)
    obj.data.materials.append(gold_mat) 
    obj.data.materials.append(glow_mat) 

    # === Step 3: BMesh Topology Manipulation ===
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj.data)

    # Identify the top and bottom circular faces (normals pointing up/down)
    top_bottom_faces = [f for f in bm.faces if abs(f.normal.z) > 0.9]

    # Inset the faces to create the boundary for the rim
    bmesh.ops.inset_individual(bm, faces=top_bottom_faces, thickness=0.25)
    
    # The inset operation leaves the inner faces selected/available in the original reference
    for f in top_bottom_faces:
        f.material_index = 1  # Assign the emissive material to the inner core
        
        # Move the inner faces inwards to create a depression 
        # (f.normal points outwards, so -f.normal pushes them into the coin)
        translation_vec = -f.normal * 0.05
        bmesh.ops.translate(bm, verts=f.verts, vec=translation_vec)

    # Finalize BMesh and return to object mode
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    # === Step 4: Final Transforms ===
    obj.scale = (scale, scale, scale)
    
    # Rotate the coin 90 degrees on the X-axis so it stands upright like a collectible pickup
    obj.rotation_euler = (math.radians(90), 0, 0)

    # Ensure Eevee bloom is enabled in the scene for the glow effect to pop (optional UX enhancement)
    if scene.render.engine == 'BLENDER_EEVEE':
        scene.eevee.use_bloom = True

    return f"Created '{object_name}' (Low-Poly Game Asset) at {location} with {len(obj.data.polygons)} optimized faces."
