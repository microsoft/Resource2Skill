# Basic Procedural Geometry Node Setup

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Basic Procedural Geometry Node Setup

* **Core Visual Mechanism**: The core mechanism is completely replacing a static base mesh with a procedurally generated primitive (a Cube) inside a node graph, then sequentially modifying it using a series of mathematical and structural operations (`Transform`, `Subdivision Surface`, `Set Shade Smooth`). This forms a linear, non-destructive pipeline where data flows from left to right.

* **Why Use This Skill (Rationale)**: This is the fundamental building block of procedural modeling in Blender. By moving geometry generation and modification into a node tree, the 3D object becomes fully parametric. You can alter the subdivision level, size, or position at any time without permanently destroying base vertex data, enabling rapid iteration and variation.

* **Overall Applicability**: This pattern is the starting point for almost all Geometry Node setups—whether generating stylized foliage, procedural buildings, or motion graphics. It establishes the workspace, the modifier connection, and the basic input/output data flow required for proceduralism.

* **Value Addition**: Compared to just adding a mesh cube and a Subdivision modifier, this skill introduces the *context* of Geometry Nodes. It allows for internal transformations (scaling/moving geometry before it hits the origin point) and procedural material assignment, keeping the object's external transforms clean while its internal shape is fully dynamic.


### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A completely empty or arbitrary base mesh acts simply as a "container" for the Geometry Nodes modifier.
  - **Procedural Generation**: A `Cube` primitive node generates the actual geometry.
  - **Modifiers (Node-based)**:
    - `Transform Geometry`: Translates, rotates, or scales the generated cube in local space.
    - `Subdivision Surface`: Increases topology density and rounds the procedural cube into a spherical shape.
    - `Set Shade Smooth`: Alters the normal data to render the high-density topology smoothly without faceting.

* **Step B: Materials & Shading**
  - **Shader Model**: A standard Principled BSDF applied procedurally.
  - **Node Integration**: Because the geometry is generated internally, a `Set Material` node must be added at the end of the node tree to bind the external material data-block to the procedural mesh.
  - **Color**: Configurable via parameters, e.g., a neutral placeholder `(0.2, 0.6, 0.8)`.

* **Step C: Lighting & Rendering Context**
  - Operates independently of specific lighting, though the smooth shading effect is best highlighted with standard three-point lighting or an HDRI to show off the curved specular highlights.
  - Works identically in EEVEE and Cycles.

* **Step D: Animation & Dynamics**
  - The `Transform Geometry` node within this setup is a prime target for procedural animation (e.g., driving the Rotation socket with a `#frame` driver) to create spinning motion graphics.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Procedural Container | `bpy.data.objects.new` + Empty Mesh | Creates a clean, non-destructive host for the modifier without excess base geometry. |
| Node Tree Construction | `bpy.data.node_groups.new(type='GeometryNodeTree')` | The exact API method required to build the procedural logic demonstrated in the tutorial. |
| Topology & Shading | Node linking (`Subdivision`, `Smooth`, `Set Material`) | Replicates the linear modifier stack entirely within the procedural graph. |

> **Feasibility Assessment**: 100% reproduction. The code perfectly mimics the introductory Geometry Node setup shown in the tutorial, including the specific nodes, linking structure, and subdivision settings.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "ProceduralGeoNodeObject",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 0.8),
    **kwargs,
) -> str:
    """
    Create a Basic Procedural Geometry Node Setup in the active Blender scene.
    Demonstrates generating a primitive, transforming, subdividing, and smoothing it procedurally.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object and node group.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    # Get target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Container Object ===
    # Create an empty mesh to act as a host for the geometry nodes
    mesh = bpy.data.meshes.new(name=f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    # Position and scale the container object
    obj.location = Vector(location)
    obj.scale = Vector((scale, scale, scale))

    # === Step 2: Create Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.4

    # === Step 3: Build Geometry Nodes Setup ===
    # Add modifier
    mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
    
    # Create node group
    node_group = bpy.data.node_groups.new(name=f"{object_name}_NodeTree", type='GeometryNodeTree')
    mod.node_group = node_group

    # Handle API differences for creating interface sockets (Blender 4.0+ vs older)
    if hasattr(node_group, "interface"):
        node_group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        node_group.outputs.new('NodeSocketGeometry', "Geometry")

    nodes = node_group.nodes
    links = node_group.links

    # Instantiate Nodes
    node_out = nodes.new('NodeGroupOutput')
    node_out.location = (800, 0)

    node_cube = nodes.new('GeometryNodeMeshCube')
    node_cube.location = (-200, 0)
    
    # Allows internal offset independent of object origin
    node_transform = nodes.new('GeometryNodeTransform')
    node_transform.location = (0, 0)
    node_transform.inputs['Translation'].default_value = (0.0, 0.0, 0.5)

    node_subdiv = nodes.new('GeometryNodeSubdivisionSurface')
    node_subdiv.location = (200, 0)
    node_subdiv.inputs['Level'].default_value = 3

    node_smooth = nodes.new('GeometryNodeSetShadeSmooth')
    node_smooth.location = (400, 0)

    node_material = nodes.new('GeometryNodeSetMaterial')
    node_material.location = (600, 0)
    node_material.inputs['Material'].default_value = mat

    # Link the procedural pipeline
    # Cube -> Transform -> Subdivision -> Smooth -> Material -> Output
    links.new(node_cube.outputs['Mesh'], node_transform.inputs['Geometry'])
    links.new(node_transform.outputs['Geometry'], node_subdiv.inputs['Mesh'])
    links.new(node_subdiv.outputs['Mesh'], node_smooth.inputs['Geometry'])
    links.new(node_smooth.outputs['Geometry'], node_material.inputs['Geometry'])
    links.new(node_material.outputs['Geometry'], node_out.inputs['Geometry'])

    return f"Created procedural '{object_name}' at {location} utilizing a complete Geometry Nodes pipeline."
```