def create_proximity_effector_system(
    scene_name: str = "Scene",
    object_name: str = "ProximityGrid",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    base_color: tuple = (0.01, 0.1, 0.4), # Dark Blue
    highlight_color: tuple = (0.2, 0.6, 1.0), # Light Blue
) -> str:
    """
    Creates an interactive grid of tiles that depress and change color when a sphere rolls over them.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated objects.
        location: (x, y, z) world-space position of the grid center.
        scale: Uniform scale factor for the overall grid.
        base_color: (R, G, B) color of tiles when the sphere is far away.
        highlight_color: (R, G, B) color of tiles when the sphere is directly overhead.
        
    Returns:
        Status string detailing the created system.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    scene.render.engine = 'CYCLES' # Required for high-quality glass transmission

    # ==========================================
    # 1. CREATE TILE TEMPLATE
    # ==========================================
    bpy.ops.mesh.primitive_cube_add(size=1)
    tile_obj = bpy.context.active_object
    tile_obj.name = f"{object_name}_Tile"
    tile_obj.scale = (1.0, 1.0, 0.2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Add bevel for satisfying edge highlights
    mod_bevel = tile_obj.modifiers.new(name="Bevel", type='BEVEL')
    mod_bevel.width = 0.04
    mod_bevel.segments = 3
    bpy.ops.object.shade_smooth()
    
    # Hide the source tile (it will only be instanced)
    tile_obj.hide_set(True)
    tile_obj.hide_render = True

    # ==========================================
    # 2. CREATE EFFECTOR (GLASS SPHERE)
    # ==========================================
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.2, segments=64, ring_count=32)
    effector_obj = bpy.context.active_object
    effector_obj.name = f"{object_name}_Effector"
    bpy.ops.object.shade_smooth()
    
    # Position and Animate Effector
    start_loc = Vector((location[0] - 6, location[1], location[2] + 1.2))
    end_loc = Vector((location[0] + 6, location[1], location[2] + 1.2))
    effector_obj.location = start_loc
    
    # Animate 
    effector_obj.keyframe_insert(data_path="location", frame=1)
    effector_obj.location = end_loc
    effector_obj.keyframe_insert(data_path="location", frame=120)
    
    # Make keyframes linear for a smooth looping roll
    if effector_obj.animation_data and effector_obj.animation_data.action:
        for fcurve in effector_obj.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'

    # Effector Material (Glass)
    eff_mat = bpy.data.materials.new(name=f"{object_name}_Glass")
    eff_mat.use_nodes = True
    eff_bsdf = eff_mat.node_tree.nodes.get("Principled BSDF")
    if eff_bsdf:
        eff_bsdf.inputs['Roughness'].default_value = 0.05
        # Handle Blender 4.0+ vs 3.x transmission socket names
        if 'Transmission Weight' in eff_bsdf.inputs:
            eff_bsdf.inputs['Transmission Weight'].default_value = 1.0
        elif 'Transmission' in eff_bsdf.inputs:
            eff_bsdf.inputs['Transmission'].default_value = 1.0
    effector_obj.data.materials.append(eff_mat)

    # ==========================================
    # 3. CREATE TILE REACTIVE MATERIAL
    # ==========================================
    tile_mat = bpy.data.materials.new(name=f"{object_name}_ReactiveMat")
    tile_mat.use_nodes = True
    nodes = tile_mat.node_tree.nodes
    links = tile_mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")

    # Read the custom attribute passed from Geometry Nodes
    attr_node = nodes.new("ShaderNodeAttribute")
    attr_node.attribute_name = "proximity_glow"

    # Mix colors based on proximity
    mix_node = nodes.new("ShaderNodeMixRGB")
    mix_node.inputs['Color1'].default_value = base_color + (1.0,)
    mix_node.inputs['Color2'].default_value = highlight_color + (1.0,)
    links.new(attr_node.outputs['Fac'], mix_node.inputs['Fac'])
    
    if bsdf:
        links.new(mix_node.outputs['Color'], bsdf.inputs['Base Color'])
        bsdf.inputs['Roughness'].default_value = 0.15 # Slightly shiny tiles
    tile_obj.data.materials.append(tile_mat)

    # ==========================================
    # 4. CREATE MAIN GRID & GEOMETRY NODES
    # ==========================================
    bpy.ops.mesh.primitive_plane_add(size=1)
    grid_obj = bpy.context.active_object
    grid_obj.name = object_name
    grid_obj.location = location
    grid_obj.scale = (scale, scale, scale)

    # Setup GeoNodes Modifier
    mod_geo = grid_obj.modifiers.new(name="ProximitySystem", type='NODES')
    tree = bpy.data.node_groups.new(name=f"{object_name}_NodeTree", type='GeometryNodeTree')
    mod_geo.node_group = tree

    # Create Node Group Interface (Compatible with 3.x and 4.x)
    if hasattr(tree, "interface"):
        tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        tree.outputs.new("NodeSocketGeometry", "Geometry")
    out_node = tree.nodes.new("NodeGroupOutput")

    # Node: Mesh Grid
    node_grid = tree.nodes.new("GeometryNodeMeshGrid")
    node_grid.inputs['Size X'].default_value = 10.0
    node_grid.inputs['Size Y'].default_value = 10.0
    node_grid.inputs['Vertices X'].default_value = 10
    node_grid.inputs['Vertices Y'].default_value = 10

    # Node: Mesh to Points (Faces)
    node_m2p = tree.nodes.new("GeometryNodeMeshToPoints")
    node_m2p.mode = 'FACES'
    tree.links.new(node_grid.outputs['Mesh'], node_m2p.inputs['Mesh'])

    # Node: Object Info (Tile Template)
    node_info_tile = tree.nodes.new("GeometryNodeObjectInfo")
    node_info_tile.inputs['Object'].default_value = tile_obj

    # Node: Instance on Points
    node_iop = tree.nodes.new("GeometryNodeInstanceOnPoints")
    node_iop.inputs['Scale'].default_value = (0.95, 0.95, 0.95) # Leave satisfying gaps
    tree.links.new(node_m2p.outputs['Points'], node_iop.inputs['Points'])
    tree.links.new(node_info_tile.outputs['Geometry'], node_iop.inputs['Instance'])

    # Node: Object Info (Effector Sphere)
    node_info_eff = tree.nodes.new("GeometryNodeObjectInfo")
    node_info_eff.inputs['Object'].default_value = effector_obj
    node_info_eff.transform_space = 'RELATIVE'

    # Node: Mesh Line (Acts as a 1-point proxy to measure spherical center distance)
    node_line = tree.nodes.new("GeometryNodeMeshLine")
    node_line.inputs['Count'].default_value = 1
    tree.links.new(node_info_eff.outputs['Location'], node_line.inputs['Start Location'])

    # Node: Geometry Proximity
    node_prox = tree.nodes.new("GeometryNodeProximity")
    node_prox.target_element = 'POINTS'
    tree.links.new(node_line.outputs['Mesh'], node_prox.inputs['Target'])

    # Node: Map Range (Displacement) - Maps close distances to negative Z
    node_map_disp = tree.nodes.new("ShaderNodeMapRange")
    node_map_disp.inputs['From Min'].default_value = 0.5 # Core radius
    node_map_disp.inputs['From Max'].default_value = 2.5 # Falloff outer radius
    node_map_disp.inputs['To Min'].default_value = -1.2  # Max depression depth
    node_map_disp.inputs['To Max'].default_value = 0.0   # Neutral height
    tree.links.new(node_prox.outputs['Distance'], node_map_disp.inputs['Value'])

    # Node: Combine XYZ
    node_xyz = tree.nodes.new("ShaderNodeCombineXYZ")
    tree.links.new(node_map_disp.outputs['Result'], node_xyz.inputs['Z'])

    # Node: Translate Instances
    node_trans = tree.nodes.new("GeometryNodeTranslateInstances")
    tree.links.new(node_iop.outputs['Instances'], node_trans.inputs['Instances'])
    tree.links.new(node_xyz.outputs['Vector'], node_trans.inputs['Translation'])

    # Node: Map Range (Color) - Maps close distances to high glow factor
    node_map_color = tree.nodes.new("ShaderNodeMapRange")
    node_map_color.inputs['From Min'].default_value = 0.0
    node_map_color.inputs['From Max'].default_value = 3.5
    node_map_color.inputs['To Min'].default_value = 1.0  # 1.0 = Highlight Color
    node_map_color.inputs['To Max'].default_value = 0.0  # 0.0 = Base Color
    tree.links.new(node_prox.outputs['Distance'], node_map_color.inputs['Value'])

    # Node: Store Named Attribute (Data Handoff to Shader)
    node_store = tree.nodes.new("GeometryNodeStoreNamedAttribute")
    node_store.data_type = 'FLOAT'
    node_store.domain = 'INSTANCE'
    node_store.inputs['Name'].default_value = "proximity_glow"
    tree.links.new(node_trans.outputs['Instances'], node_store.inputs['Geometry'])
    tree.links.new(node_map_color.outputs['Result'], node_store.inputs['Value'])

    # Node: Set Material
    node_setmat = tree.nodes.new("GeometryNodeSetMaterial")
    node_setmat.inputs['Material'].default_value = tile_mat
    tree.links.new(node_store.outputs['Geometry'], node_setmat.inputs['Geometry'])

    # Final Output Link
    tree.links.new(node_setmat.outputs['Geometry'], out_node.inputs[0])

    # ==========================================
    # 5. LIGHTING SETUP
    # ==========================================
    light_data = bpy.data.lights.new(name=f"{object_name}_SoftLight", type='AREA')
    light_data.energy = 2500
    light_data.shape = 'DISK'
    light_data.size = 12.0
    light_obj = bpy.data.objects.new(name=f"{object_name}_LightRig", object_data=light_data)
    scene.collection.objects.link(light_obj)
    light_obj.location = (location[0], location[1], location[2] + 6)

    return f"Created procedural Proximity Effector System '{object_name}' at {location}. Press Spacebar to play the animation."
