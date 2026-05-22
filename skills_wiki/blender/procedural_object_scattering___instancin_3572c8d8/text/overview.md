# Geometry Nodes Object Scattering (Procedural Sugar Coating)

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Object Scattering & Instancing (Sugar Coating Pattern)

* **Core Visual Mechanism**: This pattern leverages Blender's Geometry Nodes to dynamically distribute a secondary "instance" object (e.g., a sugar crystal) across the surface of a primary "base" mesh (e.g., a gummy candy). The signature of this technique is the dense, organically randomized layer of particles clinging to a surface, where each instance has a fully randomized rotation (0 to 360 degrees on all axes) and randomized scale to break up repeating patterns and create natural imperfection.

* **Why Use This Skill (Rationale)**: Procedural scattering is infinitely superior to manual placement or traditional array modifiers. It is non-destructive, meaning if the base mesh changes shape, the scattered crystals automatically conform to the new surface. Randomizing rotation using `tau` (2π radians or 360°) ensures no two crystals catch the light in the exact same way, creating highly realistic glints, sparkles, and specular highlights when rendered.

* **Overall Applicability**: This scattering paradigm is foundational for a vast array of 3D detailing tasks:
  - **Food Visualization**: Sugar on candy, sprinkles on a donut, salt on a pretzel.
  - **Environmental Details**: Pebbles or debris on the ground, moss patches on rocks, leaves on a tree.
  - **Sci-Fi/Hard Surface**: "Greebles" or micro-mechanical details scattered on spaceship hulls.
  - **Abstract/Motion Graphics**: Swarms of geometric shapes clinging to animated topologies.

* **Value Addition**: Instead of a flat material texture simulating depth, this skill creates real, physical micro-geometry. This generates true ambient occlusion, physically accurate light refraction/transmission through the crystals, and accurate silhouette breakup that a normal map or bump map simply cannot achieve.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A Torus (acting as a lifesaver or donut candy) is used, with a Subdivision Surface modifier to smooth the topology, giving it an organic, soft appearance.
  - **Instance Mesh**: A simple low-poly primitive (a tiny Cube) acts as the sugar crystal. Keeping this instance mesh low-poly is critical because it will be duplicated thousands of times.
  - **Geometry Nodes Modifier**: 
    - `Distribute Points on Faces`: Scatters placeholder points randomly across the base mesh.
    - `Instance on Points`: Replaces the points with the crystal geometry.
    - `Random Value (Vector)`: Generates independent X, Y, Z rotations between 0 and `tau` (6.283 radians) for full spherical randomization.
    - `Random Value (Float)`: Generates a uniform scale multiplier between 0.4 and 1.2 so some crystals are chunky and some are dust-like.
    - `Join Geometry`: Merges the original smooth candy mesh with the new scattered crystal instances so both render together.

* **Step B: Materials & Shading**
  - **Candy Material**: Principled BSDF with strong Subsurface Scattering (Weight: 1.0) and low roughness (0.3). This gives the gummy candy a soft, translucent, light-absorbing quality. Base color: Deep Red `(0.8, 0.02, 0.05)`.
  - **Crystal Material**: Principled BSDF simulating glass/sugar. High Transmission (Weight: 1.0), low Roughness (0.05), and an IOR (Index of Refraction) of 1.53, matching real sugar. Base Color: Pure White `(1.0, 1.0, 1.0)`.

* **Step C: Lighting & Rendering Context**
  - **Lighting**: A strong backlight or rim light is highly recommended. Subsurface scattering and transmissive crystals "activate" and sparkle most beautifully when light shines *through* them towards the camera.
  - **Render Engine**: Cycles is strongly recommended over EEVEE for this, as path-tracing handles the complex light bounces through thousands of refractive glass cubes and subsurface volumes much more accurately.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Base & Instance Geometry** | `bpy.ops.mesh.primitive_*` | Generates clean baseline topology to act as the canvas and the instance. |
| **Organic Smoothing** | Subdivision Surface Modifier | Provides the soft, rounded aesthetic necessary for gummy candy. |
| **Procedural Scattering** | Geometry Nodes (`bpy.data.node_groups`) | Non-destructive, parametric, highly performant instancing, and direct vector math manipulation for random rotation (`math.tau`). |
| **Translucency & Refraction** | Shader Node Tree (Principled BSDF) | Accesses physically accurate Transmission and Subsurface Scattering properties. |

> **Feasibility Assessment**: 100% reproduction. The code completely recreates the node graph, random logic, instancing hierarchy, and PBR materials described in the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "SugarCandy",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.02, 0.05),
    crystal_density: float = 2500.0,
    **kwargs,
) -> str:
    """
    Create a procedural scattered object (Sugar Coated Candy) using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created candy object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the candy base.
        material_color: (R, G, B) base color for the candy.
        crystal_density: Number of points to scatter (higher = more sugar).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    # Safely get scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Helper function to reliably fetch sockets by name across Blender versions
    def get_socket(node, name, is_output=False):
        sockets = node.outputs if is_output else node.inputs
        for s in sockets:
            if s.name == name:
                return s
        return sockets[0]  # Safe fallback

    # ==========================================
    # 1. CREATE INSTANCE OBJECT (SUGAR CRYSTAL)
    # ==========================================
    # Placed slightly below the scene, hidden from render/viewport
    bpy.ops.mesh.primitive_cube_add(size=0.03, location=(location[0], location[1], location[2] - 5.0))
    crystal_obj = bpy.context.active_object
    crystal_obj.name = f"{object_name}_Crystal"
    
    # Crystal Material (Transmissive Glass)
    mat_cryst = bpy.data.materials.new(name=f"{object_name}_CrystalMat")
    mat_cryst.use_nodes = True
    bsdf_c = mat_cryst.node_tree.nodes.get("Principled BSDF")
    if bsdf_c:
        bsdf_c.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0)
        bsdf_c.inputs["Roughness"].default_value = 0.05
        bsdf_c.inputs["IOR"].default_value = 1.53  # IOR of sugar/glass
        
        if "Transmission Weight" in bsdf_c.inputs:  # Blender 4.0+
            bsdf_c.inputs["Transmission Weight"].default_value = 1.0
        elif "Transmission" in bsdf_c.inputs:       # Blender 3.x
            bsdf_c.inputs["Transmission"].default_value = 1.0

    crystal_obj.data.materials.append(mat_cryst)
    
    # Hide the source crystal
    crystal_obj.hide_viewport = True
    crystal_obj.hide_render = True

    # ==========================================
    # 2. CREATE BASE MESH (GUMMY CANDY)
    # ==========================================
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.0 * scale, 
        minor_radius=0.4 * scale, 
        location=location
    )
    candy_obj = bpy.context.active_object
    candy_obj.name = object_name
    bpy.ops.object.shade_smooth()

    # Candy Material (Subsurface Scattering)
    mat_candy = bpy.data.materials.new(name=f"{object_name}_CandyMat")
    mat_candy.use_nodes = True
    bsdf_candy = mat_candy.node_tree.nodes.get("Principled BSDF")
    if bsdf_candy:
        bsdf_candy.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf_candy.inputs["Roughness"].default_value = 0.3
        
        if "Subsurface Weight" in bsdf_candy.inputs:  # Blender 4.0+
            bsdf_candy.inputs["Subsurface Weight"].default_value = 1.0
            bsdf_candy.inputs["Subsurface Radius"].default_value = (0.2, 0.2, 0.2)
            if "Subsurface Color" in bsdf_candy.inputs:
                bsdf_candy.inputs["Subsurface Color"].default_value = (*material_color, 1.0)
        elif "Subsurface" in bsdf_candy.inputs:       # Blender 3.x
            bsdf_candy.inputs["Subsurface"].default_value = 1.0
            if "Subsurface Radius" in bsdf_candy.inputs:
                bsdf_candy.inputs["Subsurface Radius"].default_value = (0.2, 0.2, 0.2)
            if "Subsurface Color" in bsdf_candy.inputs:
                bsdf_candy.inputs["Subsurface Color"].default_value = (*material_color, 1.0)
                
    candy_obj.data.materials.append(mat_candy)

    # Subsurf Modifier for smooth base
    subsurf = candy_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2

    # ==========================================
    # 3. BUILD GEOMETRY NODES TREE
    # ==========================================
    tree = bpy.data.node_groups.new(name=f"{object_name}_Scattering", type='GeometryNodeTree')
    
    # Init tree interface sockets safely (compatible with 3.x and 4.0+)
    if hasattr(tree, "interface"):
        tree.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        tree.inputs.new('NodeSocketGeometry', "Geometry")
        tree.outputs.new('NodeSocketGeometry', "Geometry")

    # Add Nodes
    nodes = tree.nodes
    in_node = nodes.new('NodeGroupInput')
    out_node = nodes.new('NodeGroupOutput')
    
    distribute = nodes.new('GeometryNodeDistributePointsOnFaces')
    get_socket(distribute, 'Density').default_value = crystal_density
    
    instance = nodes.new('GeometryNodeInstanceOnPoints')
    join = nodes.new('GeometryNodeJoinGeometry')
    
    obj_info = nodes.new('GeometryNodeObjectInfo')
    get_socket(obj_info, 'Object').default_value = crystal_obj
    obj_info.transform_space = 'RELATIVE'
    
    rand_rot = nodes.new('FunctionNodeRandomValue')
    rand_rot.data_type = 'FLOAT_VECTOR'
    get_socket(rand_rot, 'Min').default_value = (0.0, 0.0, 0.0)
    # Use math.tau for full 360 degree (2 pi radians) rotation on all axes
    get_socket(rand_rot, 'Max').default_value = (math.tau, math.tau, math.tau)
    
    rand_scale = nodes.new('FunctionNodeRandomValue')
    rand_scale.data_type = 'FLOAT'
    get_socket(rand_scale, 'Min').default_value = 0.4
    get_socket(rand_scale, 'Max').default_value = 1.2

    # Link Nodes
    links = tree.links
    
    # Route input mesh to point distributor
    links.new(get_socket(in_node, 'Geometry', True), get_socket(distribute, 'Mesh'))
    
    # Route points to instancer
    links.new(get_socket(distribute, 'Points', True), get_socket(instance, 'Points'))
    
    # Route crystal object data into instancer
    links.new(get_socket(obj_info, 'Geometry', True), get_socket(instance, 'Instance'))
    
    # Route random math into instancer attributes
    links.new(get_socket(rand_rot, 'Value', True), get_socket(instance, 'Rotation'))
    links.new(get_socket(rand_scale, 'Value', True), get_socket(instance, 'Scale'))
    
    # Join original smooth base mesh + generated crystal instances
    links.new(get_socket(in_node, 'Geometry', True), get_socket(join, 'Geometry'))
    links.new(get_socket(instance, 'Instances', True), get_socket(join, 'Geometry'))
    
    # Route to output
    links.new(get_socket(join, 'Geometry', True), get_socket(out_node, 'Geometry'))

    # ==========================================
    # 4. APPLY MODIFIER AND FINALIZE
    # ==========================================
    gn_mod = candy_obj.modifiers.new(name="SugarCoating", type='NODES')
    gn_mod.node_group = tree

    # Clean up selection state
    bpy.ops.object.select_all(action='DESELECT')
    candy_obj.select_set(True)
    bpy.context.view_layer.objects.active = candy_obj

    return f"Created '{object_name}' with procedural sugar scattering at {location}."
```