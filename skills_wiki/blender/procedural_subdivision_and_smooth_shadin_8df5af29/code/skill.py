def create_procedural_subdiv_smooth_modifier(
    scene_name: str = "Scene",
    object_name: str = "MyObject",  # Target object to apply modifier to, or if using internal_primitive_type, it's the new object's name
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.5, 0.2),
    subdivision_level: int = 3,
    edge_crease: float = 0.0,
    internal_primitive_type: str = "INPUT_GEOMETRY",  # "CUBE", "CYLINDER", "SPHERE", or "INPUT_GEOMETRY"
    transform_translation: tuple = (0, 0, 0),
    transform_rotation: tuple = (0, 0, 0),  # Degrees
    transform_scale: tuple = (1, 1, 1),
    **kwargs,
) -> str:
    """
    Create a reusable Geometry Nodes modifier that applies procedural subdivision,
    smooth shading, and optional transformation to an object.
    It can either modify the existing geometry of a target object or generate
    a new primitive within the node tree.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object or the existing object to modify.
        location: (x, y, z) world-space position for the modified/new object.
        scale: Uniform scale factor for the modified/new object.
        material_color: (R, G, B) base color in 0-1 range for the material.
        subdivision_level: Number of subdivision levels for the surface.
        edge_crease: Value for edge creasing (0.0 for fully smooth, 1.0 for sharp).
        internal_primitive_type: Type of primitive to generate internally ("CUBE", "CYLINDER", "SPHERE", or "INPUT_GEOMETRY" to use existing object geometry).
        transform_translation: (x, y, z) translation for the Transform Geometry node.
        transform_rotation: (x, y, z) rotation in degrees for the Transform Geometry node.
        transform_scale: (x, y, z) scale for the Transform Geometry node.
        **kwargs: Additional overrides for node properties.

    Returns:
        Status string, e.g., "Created 'ProceduralCube' with Subsurf and Smooth modifier."
    """
    import bpy
    from mathutils import Euler
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 1. Get or Create Target Object ---
    target_obj = bpy.data.objects.get(object_name)
    if not target_obj:
        # If target object doesn't exist, create a new cube as a placeholder
        # The geometry nodes will overwrite its mesh if internal_primitive_type is not "INPUT_GEOMETRY"
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0,0,0))
        target_obj = bpy.context.active_object
        target_obj.name = object_name
        
    target_obj.location = location
    target_obj.scale = (scale, scale, scale)

    # --- 2. Create or Get Geometry Node Tree ---
    gn_tree_name = "Subsurf_and_Smooth_Procedural"
    node_tree = bpy.data.node_groups.get(gn_tree_name)
    if not node_tree:
        node_tree = bpy.data.node_groups.new(name=gn_tree_name, type='GeometryNodeTree')

        # Clear default nodes
        for node in node_tree.nodes:
            node_tree.nodes.remove(node)

        # Add Group Input and Group Output
        group_input = node_tree.nodes.new(type='NodeGroupInput')
        group_input.location = (-800, 0)
        group_output = node_tree.nodes.new(type='NodeGroupOutput')
        group_output.location = (800, 0)

        # Add Geometry output to Group Output
        node_tree.outputs.new('NodeSocketGeometry', 'Geometry')
        # Link Group Output directly to receive final geometry, this link will be updated later
        node_tree.links.new(group_input.outputs['Geometry'], group_output.inputs['Geometry']) 

        # Current node position for cleaner layout
        current_node_location_x = -600
        
        # Determine the initial geometry source
        last_output_node = group_input
        last_output_socket = 'Geometry'

        # Optional: Internal Primitive Node
        primitive_node = None
        if internal_primitive_type != "INPUT_GEOMETRY":
            if internal_primitive_type == "CUBE":
                primitive_node = node_tree.nodes.new(type='GeometryNodeMeshCube')
            elif internal_primitive_type == "CYLINDER":
                primitive_node = node_tree.nodes.new(type='GeometryNodeMeshCylinder')
            elif internal_primitive_type == "SPHERE":
                primitive_node = node_tree.nodes.new(type='GeometryNodeMeshUVSphere')
            else:
                return f"Error: Invalid internal_primitive_type '{internal_primitive_type}'."
            
            primitive_node.location = (current_node_location_x, 0)
            
            # Remove the default link from Group Input to Group Output if using internal primitive
            for link in node_tree.links:
                if link.from_node == group_input and link.to_node == group_output and link.from_socket == group_input.outputs['Geometry']:
                    node_tree.links.remove(link)
                    break
            
            last_output_node = primitive_node
            last_output_socket = 'Mesh'
            current_node_location_x += 200 # Move subsequent nodes

        # Transform Geometry Node
        transform_node = node_tree.nodes.new(type='GeometryNodeTransform')
        transform_node.name = "Transform Geometry" # Set name for easier access
        transform_node.location = (current_node_location_x, 0)
        node_tree.links.new(last_output_node.outputs[last_output_socket], transform_node.inputs['Geometry'])
        last_output_node = transform_node
        last_output_socket = 'Geometry'
        current_node_location_x += 200

        # Subdivision Surface Node
        subdiv_node = node_tree.nodes.new(type='GeometryNodeSubdivideSurface')
        subdiv_node.name = "Subdivision Surface" # Set name for easier access
        subdiv_node.location = (current_node_location_x, 0)
        node_tree.links.new(last_output_node.outputs[last_output_socket], subdiv_node.inputs['Mesh'])
        last_output_node = subdiv_node
        last_output_socket = 'Mesh'
        current_node_location_x += 200

        # Set Shade Smooth Node
        shade_smooth_node = node_tree.nodes.new(type='GeometryNodeSetShadeSmooth')
        shade_smooth_node.name = "Set Shade Smooth" # Set name for easier access
        shade_smooth_node.location = (current_node_location_x, 0)
        node_tree.links.new(last_output_node.outputs[last_output_socket], shade_smooth_node.inputs['Geometry'])
        last_output_node = shade_smooth_node
        last_output_socket = 'Geometry'
        current_node_location_x += 200

        # Link final output to Group Output
        node_tree.links.new(last_output_node.outputs[last_output_socket], group_output.inputs['Geometry'])

    # --- 3. Apply GN Modifier to Object ---
    gn_modifier = target_obj.modifiers.get(gn_tree_name)
    if not gn_modifier:
        gn_modifier = target_obj.modifiers.new(name=gn_tree_name, type='NODES')
        gn_modifier.node_group = node_tree

    # --- 4. Configure Node Parameters ---
    transform_node = node_tree.nodes.get("Transform Geometry")
    if transform_node:
        transform_node.inputs['Translation'].default_value = transform_translation
        # Convert degrees to radians for Euler rotation
        transform_node.inputs['Rotation'].default_value = Euler([math.radians(r) for r in transform_rotation]) 
        transform_node.inputs['Scale'].default_value = transform_scale

    subdiv_node = node_tree.nodes.get("Subdivision Surface")
    if subdiv_node:
        subdiv_node.inputs['Level'].default_value = subdivision_level
        subdiv_node.inputs['Edge Crease'].default_value = edge_crease

    # --- 5. Create or Get Material and Apply ---
    mat_name = f"{object_name}_Material"
    material = bpy.data.materials.get(mat_name)
    if not material:
        material = bpy.data.materials.new(name=mat_name)
        material.use_nodes = True
        bsdf = material.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = material_color + (1.0,) # Add alpha for Principled BSDF
        bsdf.inputs['Roughness'].default_value = 0.7
        bsdf.inputs['Metallic'].default_value = 0.0

    # Ensure the material is linked to the object
    if target_obj.data.materials:
        target_obj.data.materials[0] = material
    else:
        target_obj.data.materials.append(material)

    return f"Created Geometry Nodes modifier '{gn_tree_name}' and applied to '{object_name}'."
