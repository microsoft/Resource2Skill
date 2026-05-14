def create_procedural_cobblestone_scatter(
    scene_name: str = "Scene",
    object_name: str = "CobblestonePatch",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    patch_size: float = 4.0,
    grid_density: int = 12,
    **kwargs,
) -> str:
    """
    Creates a procedurally scattered cobblestone ground plane with foliage 
    growing specifically in the crevices using Geo Node Raycast masking.

    Args:
        scene_name: Name of the scene.
        object_name: Name of the main environment patch.
        location: (x,y,z) location of the patch.
        scale: Overall scale multiplier.
        patch_size: The X/Y physical dimensions of the ground patch.
        grid_density: How many stones per row/column.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector
    import random

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes.new(scene_name)

    # ==========================================
    # Helper 1: Procedural Materials
    # ==========================================
    def make_material(name, color, roughness):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = color
            bsdf.inputs['Roughness'].default_value = roughness
        return mat

    mat_ground = make_material("Mat_Dirt", (0.03, 0.025, 0.02, 1), 0.9)
    mat_stone = make_material("Mat_Cobble", (0.2, 0.2, 0.2, 1), 0.7)
    mat_plant = make_material("Mat_Weed", (0.05, 0.25, 0.02, 1), 0.4)

    # Procedural Stone bump
    stone_tree = mat_stone.node_tree
    voronoi = stone_tree.nodes.new('ShaderNodeTexVoronoi')
    voronoi.inputs['Scale'].default_value = 10.0
    bump = stone_tree.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.5
    stone_tree.links.new(voronoi.outputs['Distance'], bump.inputs['Height'])
    stone_tree.links.new(bump.outputs['Normal'], stone_tree.nodes['Principled BSDF'].inputs['Normal'])

    # ==========================================
    # Helper 2: Create Base Assets (Hidden)
    # ==========================================
    # 1. Base Stone
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -50))
    obj_stone = bpy.context.active_object
    obj_stone.name = "Base_Cobblestone"
    obj_stone.data.materials.append(mat_stone)
    
    # Subdivide and displace to look like a rock
    subsurf = obj_stone.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf.levels = 3
    
    tex_noise = bpy.data.textures.new("RockNoise", type='CLOUDS')
    tex_noise.noise_scale = 0.5
    displace = obj_stone.modifiers.new(name="Displace", type='DISPLACE')
    displace.texture = tex_noise
    displace.strength = 0.2
    
    # Flatten the top/bottom slightly
    obj_stone.scale = (1.0, 1.0, 0.4)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj_stone.hide_viewport = True
    obj_stone.hide_render = True

    # 2. Base Plant/Weed
    bpy.ops.mesh.primitive_plane_add(size=0.5, location=(0, 0, -50))
    obj_plant = bpy.context.active_object
    obj_plant.name = "Base_Weed"
    obj_plant.data.materials.append(mat_plant)
    
    # Create intersecting planes for leaves
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.duplicate_move()
    bpy.ops.transform.rotate(value=math.pi/2, orient_axis='Z')
    bpy.ops.object.mode_set(mode='OBJECT')
    obj_plant.hide_viewport = True
    obj_plant.hide_render = True

    # ==========================================
    # Main Setup: The Ground Patch & Geo Nodes
    # ==========================================
    bpy.ops.mesh.primitive_plane_add(size=patch_size, location=location)
    obj_main = bpy.context.active_object
    obj_main.name = object_name
    obj_main.data.materials.append(mat_ground)
    obj_main.scale = (scale, scale, scale)

    # Create Geometry Node Tree
    gn_mod = obj_main.modifiers.new(name="Raycast_Scatter", type='NODES')
    tree = bpy.data.node_groups.new(name="GN_CobbleRaycast", type='GeometryNodeTree')
    gn_mod.node_group = tree

    # Add default IO nodes
    node_in = tree.nodes.new('NodeGroupInput')
    tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    tree.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    node_out = tree.nodes.new('NodeGroupOutput')
    
    node_in.location = (-1000, 0)
    node_out.location = (1000, 0)

    # --- Branch 1: Staggered Cobblestones ---
    node_grid = tree.nodes.new('GeometryNodeMeshGrid')
    node_grid.inputs['Size X'].default_value = patch_size
    node_grid.inputs['Size Y'].default_value = patch_size
    node_grid.inputs['Vertices X'].default_value = grid_density
    node_grid.inputs['Vertices Y'].default_value = grid_density
    node_grid.location = (-800, 200)

    # Stagger Logic: Offset alternating rows
    node_idx = tree.nodes.new('GeometryNodeInputIndex')
    node_mod = tree.nodes.new('ShaderNodeMath')
    node_mod.operation = 'MODULO'
    node_mod.inputs[1].default_value = 2.0
    node_mult = tree.nodes.new('ShaderNodeVectorMath')
    node_mult.operation = 'MULTIPLY'
    node_mult.inputs[1].default_value = ((patch_size/grid_density) * 0.5, 0, 0)
    
    node_setpos_grid = tree.nodes.new('GeometryNodeSetPosition')
    
    tree.links.new(node_idx.outputs[0], node_mod.inputs[0])
    tree.links.new(node_mod.outputs[0], node_mult.inputs[0])
    tree.links.new(node_grid.outputs['Mesh'], node_setpos_grid.inputs['Geometry'])
    tree.links.new(node_mult.outputs[0], node_setpos_grid.inputs['Offset'])

    # Instance Stones
    node_inst_stones = tree.nodes.new('GeometryNodeInstanceOnPoints')
    node_stone_info = tree.nodes.new('GeometryNodeObjectInfo')
    node_stone_info.inputs['Object'].default_value = obj_stone
    
    # Random Rotation & Scale for Stones
    node_rot_stone = tree.nodes.new('GeometryNodeRandomValue')
    node_rot_stone.data_type = 'FLOAT_VECTOR'
    node_rot_stone.inputs[0].default_value = (0, 0, 0)
    node_rot_stone.inputs[1].default_value = (0, 0, math.pi * 2)
    
    node_scale_stone = tree.nodes.new('GeometryNodeRandomValue')
    node_scale_stone.data_type = 'FLOAT'
    # Base scale relative to density
    base_s = (patch_size / grid_density) * 0.8
    node_scale_stone.inputs[2].default_value = base_s * 0.7 # Min
    node_scale_stone.inputs[3].default_value = base_s * 1.1 # Max

    tree.links.new(node_setpos_grid.outputs['Geometry'], node_inst_stones.inputs['Points'])
    tree.links.new(node_stone_info.outputs['Geometry'], node_inst_stones.inputs['Instance'])
    tree.links.new(node_rot_stone.outputs[0], node_inst_stones.inputs['Rotation'])
    tree.links.new(node_scale_stone.outputs[0], node_inst_stones.inputs['Scale'])

    # Realize Instances (CRITICAL for Raycast to work)
    node_realize = tree.nodes.new('GeometryNodeRealizeInstances')
    tree.links.new(node_inst_stones.outputs['Instances'], node_realize.inputs['Geometry'])

    # --- Branch 2: Raycast Crevice Plants ---
    # Distribute on Ground
    node_dist_plants = tree.nodes.new('GeometryNodeDistributePointsOnFaces')
    node_dist_plants.inputs['Density'].default_value = 200.0
    tree.links.new(node_in.outputs['Geometry'], node_dist_plants.inputs['Mesh'])

    # Lift points up slightly for the Raycast
    node_lift = tree.nodes.new('GeometryNodeSetPosition')
    node_lift.inputs['Offset'].default_value = (0, 0, 1.0)
    tree.links.new(node_dist_plants.outputs['Points'], node_lift.inputs['Geometry'])

    # Raycast
    node_raycast = tree.nodes.new('GeometryNodeRaycast')
    node_raycast.inputs['Ray Direction'].default_value = (0, 0, -1.0) # Shoot down
    tree.links.new(node_realize.outputs['Geometry'], node_raycast.inputs['Target Geometry'])
    # Mapping points to raycast
    
    # Delete points that hit a stone
    node_delete = tree.nodes.new('GeometryNodeDeleteGeometry')
    tree.links.new(node_lift.outputs['Geometry'], node_delete.inputs['Geometry'])
    tree.links.new(node_raycast.outputs['Is Hit'], node_delete.inputs['Selection'])

    # Drop points back down to ground
    node_drop = tree.nodes.new('GeometryNodeSetPosition')
    node_drop.inputs['Offset'].default_value = (0, 0, -1.0)
    tree.links.new(node_delete.outputs['Geometry'], node_drop.inputs['Geometry'])

    # Instance Plants
    node_inst_plants = tree.nodes.new('GeometryNodeInstanceOnPoints')
    node_plant_info = tree.nodes.new('GeometryNodeObjectInfo')
    node_plant_info.inputs['Object'].default_value = obj_plant

    # Random Rot/Scale for Plants
    node_rot_plant = tree.nodes.new('GeometryNodeRandomValue')
    node_rot_plant.data_type = 'FLOAT_VECTOR'
    node_rot_plant.inputs[1].default_value = (0, 0, math.pi * 2)
    node_scale_plant = tree.nodes.new('GeometryNodeRandomValue')
    node_scale_plant.data_type = 'FLOAT'
    node_scale_plant.inputs[2].default_value = 0.2
    node_scale_plant.inputs[3].default_value = 0.6

    tree.links.new(node_drop.outputs['Geometry'], node_inst_plants.inputs['Points'])
    tree.links.new(node_plant_info.outputs['Geometry'], node_inst_plants.inputs['Instance'])
    tree.links.new(node_rot_plant.outputs[0], node_inst_plants.inputs['Rotation'])
    tree.links.new(node_scale_plant.outputs[0], node_inst_plants.inputs['Scale'])

    # --- Final Join ---
    node_join = tree.nodes.new('GeometryNodeJoinGeometry')
    tree.links.new(node_in.outputs['Geometry'], node_join.inputs['Geometry']) # Ground
    tree.links.new(node_realize.outputs['Geometry'], node_join.inputs['Geometry']) # Stones
    tree.links.new(node_inst_plants.outputs['Instances'], node_join.inputs['Geometry']) # Weeds

    tree.links.new(node_join.outputs['Geometry'], node_out.inputs['Geometry'])

    return f"Created '{object_name}' at {location} with staggered cobblestones and raycast-masked crevice foliage."
