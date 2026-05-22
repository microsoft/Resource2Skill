def create_sugar_coated_candy(
    scene_name: str = "Scene",
    object_name: str = "SugarCandy",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.05, 0.1),
    density: float = 3000.0,
    **kwargs,
) -> str:
    """
    Create a procedural sugar-coated candy using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created candy object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the candy.
        density: How tightly packed the sugar crystals are.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Build Materials ===
    # Candy Material (Subsurface Gummy)
    candy_mat = bpy.data.materials.new(name=f"{object_name}_BaseMat")
    candy_mat.use_nodes = True
    bsdf = candy_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.2
        # Backwards/forwards compatibility for SSS (Blender 3.x vs 4.x)
        if 'Subsurface Weight' in bsdf.inputs:
            bsdf.inputs['Subsurface Weight'].default_value = 0.8
            bsdf.inputs['Subsurface Radius'].default_value = (0.2, 0.2, 0.2)
            if 'Subsurface Color' in bsdf.inputs:
                bsdf.inputs['Subsurface Color'].default_value = (*material_color, 1.0)
        elif 'Subsurface' in bsdf.inputs:
            bsdf.inputs['Subsurface'].default_value = 0.8
            bsdf.inputs['Subsurface Radius'].default_value = (0.2, 0.2, 0.2)
            bsdf.inputs['Subsurface Color'].default_value = (*material_color, 1.0)

    # Sugar Material (Refractive Glass)
    sugar_mat = bpy.data.materials.new(name=f"{object_name}_SugarMat")
    sugar_mat.use_nodes = True
    s_bsdf = sugar_mat.node_tree.nodes.get("Principled BSDF")
    if s_bsdf:
        s_bsdf.inputs['Base Color'].default_value = (0.95, 0.95, 0.95, 1.0)
        s_bsdf.inputs['Roughness'].default_value = 0.15
        if 'Transmission Weight' in s_bsdf.inputs:
            s_bsdf.inputs['Transmission Weight'].default_value = 0.9
        elif 'Transmission' in s_bsdf.inputs:
            s_bsdf.inputs['Transmission'].default_value = 0.9
        s_bsdf.inputs['IOR'].default_value = 1.5

    # === Step 2: Create Base Meshes ===
    # Candy Base (Torus)
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.0, 
        minor_radius=0.4, 
        major_segments=64, 
        minor_segments=32, 
        location=location
    )
    candy_obj = bpy.context.active_object
    candy_obj.name = object_name
    candy_obj.data.materials.append(candy_mat)
    bpy.ops.object.shade_smooth()
    candy_obj.scale = (scale, scale, scale)

    # Instance Mesh (Sugar Crystal)
    bpy.ops.mesh.primitive_cube_add(size=0.03, location=location)
    crystal_obj = bpy.context.active_object
    crystal_obj.name = f"{object_name}_Crystal_Template"
    crystal_obj.data.materials.append(sugar_mat)
    
    # Bevel modifier to catch specular highlights better
    bevel = crystal_obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.003
    bevel.segments = 2
    bpy.ops.object.shade_smooth()
    
    # Hide the template crystal from viewport and render
    crystal_obj.hide_viewport = True
    crystal_obj.hide_render = True

    # Deselect crystal and re-select candy as active
    bpy.ops.object.select_all(action='DESELECT')
    candy_obj.select_set(True)
    bpy.context.view_layer.objects.active = candy_obj

    # === Step 3: Geometry Nodes Implementation ===
    gn_mod = candy_obj.modifiers.new(name="Sugar Scatter", type='NODES')
    ng = bpy.data.node_groups.new(name=f"{object_name}_SugarScatter", type='GeometryNodeTree')
    gn_mod.node_group = ng

    # Version-agnostic Socket Interface Setup
    if hasattr(ng, "interface"):
        ng.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        ng.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        ng.inputs.new('NodeSocketGeometry', "Geometry")
        ng.outputs.new('NodeSocketGeometry', "Geometry")

    # Spawn nodes
    node_in = ng.nodes.new('NodeGroupInput')
    node_out = ng.nodes.new('NodeGroupOutput')
    distribute = ng.nodes.new('GeometryNodeDistributePointsOnFaces')
    instance = ng.nodes.new('GeometryNodeInstanceOnPoints')
    join = ng.nodes.new('GeometryNodeJoinGeometry')
    obj_info = ng.nodes.new('GeometryNodeObjectInfo')
    
    rand_scale = ng.nodes.new('FunctionNodeRandomValue')
    rand_scale.data_type = 'FLOAT'
    
    rand_rot = ng.nodes.new('FunctionNodeRandomValue')
    rand_rot.data_type = 'FLOAT_VECTOR'

    # Configure logic and values
    distribute.inputs['Density'].default_value = density
    obj_info.inputs['Object'].default_value = crystal_obj
    
    # Scale randomization
    rand_scale.inputs['Min'].default_value = 0.4
    rand_scale.inputs['Max'].default_value = 1.2
    
    # Full 360 XYZ Rotation (math.tau = 2 * PI = 360 degrees in radians)
    rand_rot.inputs['Min'].default_value = (0.0, 0.0, 0.0)
    rand_rot.inputs['Max'].default_value = (math.tau, math.tau, math.tau)

    # Safe socket getters
    def get_socket(node, socket_type):
        return next((out for out in node.outputs if out.type == socket_type), node.outputs[0])

    # Connect tree logic
    # Base flow
    ng.links.new(node_in.outputs[0], distribute.inputs['Mesh'])
    ng.links.new(distribute.outputs['Points'], instance.inputs['Points'])
    
    # Inject instance geometry
    ng.links.new(obj_info.outputs.get('Geometry') or obj_info.outputs.get('Instance'), instance.inputs['Instance'])
    
    # Inject randomization
    ng.links.new(get_socket(rand_scale, 'VALUE'), instance.inputs['Scale'])
    ng.links.new(get_socket(rand_rot, 'VECTOR'), instance.inputs['Rotation'])

    # Merge instance points with the original un-modified mesh
    ng.links.new(node_in.outputs[0], join.inputs[0])
    ng.links.new(instance.outputs.get('Instances') or instance.outputs[0], join.inputs[0])
    ng.links.new(join.outputs[0], node_out.inputs[0])

    return f"Created '{object_name}' candy at {location} scattered with {density} sugar instances."
