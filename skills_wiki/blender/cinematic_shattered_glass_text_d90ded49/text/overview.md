# Cinematic Shattered Glass Text

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Cinematic Shattered Glass Text

* **Core Visual Mechanism**: This technique uses a combination of pre-fractured geometry (via the Cell Fracture add-on) and Geometry Nodes to procedurally animate a slow-motion explosion. The signature look comes from the material: instead of expensive path-traced caustics, it uses a Layer Weight (Facing) node driving an Emission shader on a highly transmissive Principled BSDF. This creates glowing, crystalline edges that fake internal refraction and reflections.
* **Why Use This Skill (Rationale)**: Physically accurate glass shattering with internal caustics is computationally brutal to render. This method bakes the shattered pieces into static geometry, uses node-based instances to control the explosion trajectory cheaply, and utilizes an emissive edge-glow shader to simulate cinematic lighting. It's highly performant and visually striking.
* **Overall Applicability**: Perfect for motion graphics, title sequences, logo reveals, and abstract sci-fi/magical environmental debris.
* **Value Addition**: Transforms basic text primitives into complex, dynamic particle assemblies that react to animation and emit their own atmospheric light.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Primitive**: Text object, extruded and converted to a mesh.
  - **Topology Correction**: A Remesh modifier (Sharp mode) is applied to create an even, voxel-like topology. This is mandatory, as default text topology (n-gons and chaotic triangles) causes boolean fracture operations to fail.
  - **Fracture**: The Cell Fracture add-on slices the remeshed text into ~150 individual solid chunks.
  - **Geometry Nodes**: A `Collection Info` node brings the chunks into a procedural tree. `Set Position` and `Rotate Instances` nodes, driven by animated `Random Value` nodes, push the shards outward over time.
* **Step B: Materials & Shading**
  - **Glass Shards**: A Principled BSDF with 1.0 Transmission and low Roughness (0.05). A `Layer Weight` node (Facing, 0.85 Blend) is clamped through a `ColorRamp` and plugged into the Emission Color/Strength. This makes only the sharp, grazing angles of the glass glow.
  - **Atmospheric Particles**: A separate Geometry Node setup distributes Ico Spheres in a volume surrounding the text, shaded with a pure Emission material to look like glowing dust or stars.
* **Step C: Lighting & Rendering Context**
  - **Render Engine**: Cycles (required for realistic glass transmission, though the emission trick looks decent in EEVEE).
  - **Environment**: Pure black world background. The scene is entirely lit by the emissive edges of the glass and the background particles.
  - **Camera**: A low F-Stop (e.g., f/2.8) Depth of Field is crucial to separate the foreground shards from the glowing background dust.
* **Step D: Animation & Dynamics**
  - No rigid body physics are used. The explosion is purely procedural, animated by keyframing the `Min` and `Max` values of the `Random Value` nodes in Geometry Nodes to expand outwards over 150 frames.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base Geometry | `bpy.ops.object.text_add` + Remesh Modifier | Quickly generates thick, uniform text ready for boolean operations. |
| Shattering | `object_fracture_cell` Add-on | Blender's native, fastest way to create solid Voronoi chunks from a mesh. |
| Explosion Animation | Geometry Nodes | Allows procedural, non-destructive translation and rotation of the fractured collection without managing hundreds of individual keyframes. |
| Edge Glow / Reflections | Shader Node Tree (Layer Weight + Emission) | Achieves a cinematic, "magical glass" look that renders infinitely faster than actual caustics. |

> **Feasibility Assessment**: 100% reproducible. The code will programmatically generate the text, enable the required fracture add-on, slice the mesh, construct the complete Geometry Node trees for both the text and the atmospheric particles, build the glowing glass materials, and bake the animation keyframes.

#### 3b. Complete Reproduction Code

```python
def create_cinematic_shatter_text(
    scene_name: str = "Scene",
    object_name: str = "ShatterTitle",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 1.0),
    text_string: str = "TITLE",
    **kwargs,
) -> str:
    """
    Create a cinematic slow-motion shattering glass text effect.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for created objects/collections.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) color for the glass glow and atmospheric dust.
        text_string: The word to be shattered.
        
    Returns:
        Status string.
    """
    import bpy
    import math
    import addon_utils
    from mathutils import Vector
    
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Enable Required Add-on ===
    addon_utils.enable("object_fracture_cell")
    
    # === Step 2: Create Base Text & Remesh ===
    bpy.ops.object.text_add(location=(0, 0, 0))
    text_obj = bpy.context.active_object
    text_obj.name = f"{object_name}_BaseText"
    text_obj.data.body = text_string
    text_obj.data.extrude = 0.2
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'CENTER'
    text_obj.rotation_euler = (math.radians(90), 0, 0)
    text_obj.scale = (scale, scale, scale)
    
    bpy.context.view_layer.update()
    bpy.ops.object.convert(target='MESH')
    
    remesh = text_obj.modifiers.new("Remesh", 'REMESH')
    remesh.mode = 'SHARP'
    remesh.octree_depth = 6
    bpy.ops.object.modifier_apply(modifier=remesh.name)
    
    # === Step 3: Cell Fracture ===
    bpy.context.view_layer.objects.active = text_obj
    bpy.ops.object.select_all(action='DESELECT')
    text_obj.select_set(True)
    
    try:
        # Generate the fractured chunks
        bpy.ops.object.add_fracture_cell_objects(
            source_limit=150,
            source_noise=0.2,
            recursion=0
        )
    except Exception as e:
        return f"Failed to run Cell Fracture: {str(e)}. Ensure the 'Cell Fracture' addon is enabled."
        
    # Isolate chunks into a dedicated collection
    cells = [obj for obj in scene.objects if obj.name.startswith(text_obj.name + "_cell")]
    cell_coll = bpy.data.collections.new(f"{object_name}_Cells")
    scene.collection.children.link(cell_coll)
    
    for c in cells:
        cell_coll.objects.link(c)
        for coll in c.users_collection:
            if coll != cell_coll:
                coll.objects.unlink(c)
        c.hide_viewport = True
        c.hide_render = True
        c.location += Vector(location) # Move actual chunks to the target location
        
    text_obj.hide_viewport = True
    text_obj.hide_render = True

    # === Step 4: Glass Material Setup ===
    glass_mat = bpy.data.materials.new(f"{object_name}_Glass")
    glass_mat.use_nodes = True
    nodes = glass_mat.node_tree.nodes
    links = glass_mat.node_tree.links
    nodes.clear()

    out = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    links.new(bsdf.outputs[0], out.inputs[0])

    bsdf.inputs['Base Color'].default_value = (1, 1, 1, 1)
    bsdf.inputs['Roughness'].default_value = 0.05

    # Handle API changes for Blender 4.0+ vs older
    if 'Transmission Weight' in bsdf.inputs:
        bsdf.inputs['Transmission Weight'].default_value = 1.0
    elif 'Transmission' in bsdf.inputs:
        bsdf.inputs['Transmission'].default_value = 1.0

    layer_weight = nodes.new('ShaderNodeLayerWeight')
    layer_weight.inputs['Blend'].default_value = 0.85

    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    color_ramp.color_ramp.elements[1].position = 0.15
    color_ramp.color_ramp.elements[1].color = (0, 0, 0, 1)
    el = color_ramp.color_ramp.elements.new(0.5)
    el.color = (material_color[0], material_color[1], material_color[2], 1.0)

    links.new(layer_weight.outputs['Facing'], color_ramp.inputs['Fac'])

    if 'Emission Color' in bsdf.inputs:
        links.new(color_ramp.outputs['Color'], bsdf.inputs['Emission Color'])
        bsdf.inputs['Emission Strength'].default_value = 5.0
    elif 'Emission' in bsdf.inputs:
        links.new(color_ramp.outputs['Color'], bsdf.inputs['Emission'])
        bsdf.inputs['Emission Strength'].default_value = 5.0

    # === Step 5: Geometry Nodes for Shatter Animation ===
    geo_obj = bpy.data.objects.new(object_name, bpy.data.meshes.new(f"{object_name}_Mesh"))
    scene.collection.objects.link(geo_obj)
    
    mod = geo_obj.modifiers.new("GeometryNodes", 'NODES')
    tree = bpy.data.node_groups.new(f"{object_name}_Tree", 'GeometryNodeTree')
    mod.node_group = tree

    group_out = tree.nodes.new('NodeGroupOutput')
    
    coll_info = tree.nodes.new('GeometryNodeCollectionInfo')
    coll_info.inputs['Collection'].default_value = cell_coll
    coll_info.inputs['Separate Children'].default_value = True
    coll_info.inputs['Reset Children'].default_value = False # Keep world position
    
    set_pos = tree.nodes.new('GeometryNodeSetPosition')
    rot_inst = tree.nodes.new('GeometryNodeRotateInstances')
    set_mat = tree.nodes.new('GeometryNodeSetMaterial')
    set_mat.inputs['Material'].default_value = glass_mat

    rand_y = tree.nodes.new('GeometryNodeRandomValue')
    rand_y.data_type = 'FLOAT'
    combine_xyz = tree.nodes.new('ShaderNodeCombineXYZ')
    
    rand_rot = tree.nodes.new('GeometryNodeRandomValue')
    rand_rot.data_type = 'FLOAT_VECTOR'

    # Build Links
    tree.links.new(coll_info.outputs[0], set_pos.inputs[0])
    tree.links.new(rand_y.outputs[0], combine_xyz.inputs['Y'])
    tree.links.new(combine_xyz.outputs[0], set_pos.inputs['Offset'])
    tree.links.new(set_pos.outputs[0], rot_inst.inputs[0])
    tree.links.new(rand_rot.outputs[0], rot_inst.inputs['Rotation'])
    tree.links.new(rot_inst.outputs[0], set_mat.inputs[0])
    tree.links.new(set_mat.outputs[0], group_out.inputs[0])

    # === Step 6: Keyframe the Explosion ===
    # Frame 1: Intact
    rand_y.inputs['Min'].default_value = 0.0
    rand_y.inputs['Max'].default_value = 0.0
    rand_y.inputs['Min'].keyframe_insert(data_path="default_value", frame=1)
    rand_y.inputs['Max'].keyframe_insert(data_path="default_value", frame=1)

    rand_rot.inputs['Min'].default_value = (0, 0, 0)
    rand_rot.inputs['Max'].default_value = (0, 0, 0)
    rand_rot.inputs['Min'].keyframe_insert(data_path="default_value", frame=1)
    rand_rot.inputs['Max'].keyframe_insert(data_path="default_value", frame=1)

    # Frame 150: Exploded & Rotated
    rand_y.inputs['Min'].default_value = -5.0 * scale
    rand_y.inputs['Max'].default_value = 2.0 * scale
    rand_y.inputs['Min'].keyframe_insert(data_path="default_value", frame=150)
    rand_y.inputs['Max'].keyframe_insert(data_path="default_value", frame=150)

    rand_rot.inputs['Min'].default_value = (-math.pi, -math.pi, -math.pi)
    rand_rot.inputs['Max'].default_value = (math.pi, math.pi, math.pi)
    rand_rot.inputs['Min'].keyframe_insert(data_path="default_value", frame=150)
    rand_rot.inputs['Max'].keyframe_insert(data_path="default_value", frame=150)

    # === Step 7: Atmospheric Particles ===
    part_obj = bpy.data.objects.new(f"{object_name}_Dust", bpy.data.meshes.new(f"{object_name}_DustMesh"))
    scene.collection.objects.link(part_obj)
    
    pmod = part_obj.modifiers.new("GeoNodes", 'NODES')
    ptree = bpy.data.node_groups.new(f"{object_name}_DustTree", 'GeometryNodeTree')
    pmod.node_group = ptree

    p_out = ptree.nodes.new('NodeGroupOutput')
    cube = ptree.nodes.new('GeometryNodeMeshCube')
    cube.inputs['Size'].default_value = (30 * scale, 30 * scale, 30 * scale)
    
    transform = ptree.nodes.new('GeometryNodeTransform')
    transform.inputs['Translation'].default_value = location
    
    m2v = ptree.nodes.new('GeometryNodeMeshToVolume')
    dist = ptree.nodes.new('GeometryNodeDistributePointsInVolume')
    dist.inputs['Density'].default_value = 1.0
    
    ico = ptree.nodes.new('GeometryNodeMeshIcoSphere')
    ico.inputs['Radius'].default_value = 0.03 * scale
    ico.inputs['Subdivisions'].default_value = 1
    
    inst = ptree.nodes.new('GeometryNodeInstanceOnPoints')
    pset_mat = ptree.nodes.new('GeometryNodeSetMaterial')
    
    ptree.links.new(cube.outputs[0], transform.inputs[0])
    ptree.links.new(transform.outputs[0], m2v.inputs[0])
    ptree.links.new(m2v.outputs[0], dist.inputs[0])
    ptree.links.new(dist.outputs[0], inst.inputs['Points'])
    ptree.links.new(ico.outputs[0], inst.inputs['Instance'])
    ptree.links.new(inst.outputs[0], pset_mat.inputs[0])
    ptree.links.new(pset_mat.outputs[0], p_out.inputs[0])

    part_mat = bpy.data.materials.new(f"{object_name}_DustMat")
    part_mat.use_nodes = True
    pnodes = part_mat.node_tree.nodes
    pnodes.clear()
    pout_mat = pnodes.new('ShaderNodeOutputMaterial')
    pemis = pnodes.new('ShaderNodeEmission')
    pemis.inputs['Color'].default_value = (material_color[0], material_color[1], material_color[2], 1.0)
    pemis.inputs['Strength'].default_value = 8.0
    part_mat.node_tree.links.new(pemis.outputs[0], pout_mat.inputs[0])
    
    pset_mat.inputs['Material'].default_value = part_mat

    return f"Created Cinematic Shattered Text '{object_name}' at {location} with {len(cells)} animated glass shards."
```