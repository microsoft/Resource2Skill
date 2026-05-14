# Procedural Surface Scattering (Sugar Coating)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Surface Scattering (Sugar Coating)

* **Core Visual Mechanism**: The defining signature of this technique is a dense, randomized scattering of small instances (sugar crystals) over the surface of a base mesh (a gummy candy), combined with the original base mesh so both are visible. This is achieved procedurally using Geometry Nodes.
* **Why Use This Skill (Rationale)**: Manually placing hundreds of tiny objects on a surface is practically impossible and computationally expensive if not instanced. Geometry Nodes allow for parametric control over density, scale, and rotation, ensuring the crystals look organic and completely cover the surface without uniform, unnatural patterning.
* **Overall Applicability**: This scattering pattern is foundational for 3D environments and product visualization. It is directly applicable to adding sprinkles to donuts, water droplets on soda cans, moss/rocks on terrain, or dust on old props. 
* **Value Addition**: Transforms a basic, flat primitive into a highly tactile, macro-level photorealistic object. The random rotation (utilizing $2\pi$ or `tau` radians) allows lighting to catch the edges of the crystals from all angles, creating a realistic, sparkling "glint" effect.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A Torus (representing the gummy candy ring). Subdivided and shaded smooth.
  - **Instance Mesh**: A small standard Cube (representing the sugar crystal).
  - **Geometry Nodes Modifier**: 
    - `Distribute Points on Faces`: Scatters placeholder points across the base mesh.
    - `Instance on Points`: Replaces those points with the Cube mesh.
    - `Object Info`: Brings the external Cube object into the node tree.
    - `Random Value (Vector)`: Set to a max of $2\pi$ (6.283 radians or `math.tau`) on X, Y, and Z to give every crystal a completely random 3D orientation.
    - `Random Value (Float)`: Randomizes the scale of the crystals so they aren't uniform.
    - `Join Geometry`: Combines the new instances with the original base mesh so the gummy candy doesn't disappear.

* **Step B: Materials & Shading**
  - **Gummy Base**: Principled BSDF with Subsurface Scattering. Base Color: `(0.8, 0.05, 0.05)` (Deep Red). Subsurface weight turned up to give it that translucent, gelatinous look.
  - **Sugar Crystal**: Principled BSDF with high transmission and roughness to simulate translucent, light-scattering sugar. Base Color: `(1.0, 1.0, 1.0)`, Transmission: `1.0`, IOR: `1.5`, Roughness: `0.3`.

* **Step C: Lighting & Rendering Context**
  - Best rendered in **Cycles** to accurately calculate the transmission and subsurface scattering.
  - Requires bright point lights or a strong HDRI to create specular highlights (glints) on the randomly rotated sugar crystal faces.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base & Instance Meshes | `bpy.ops.mesh.primitive_*` | Provides the necessary starting geometry. |
| Surface Scattering | Geometry Nodes | The exact method demonstrated in the tutorial. Procedural, mathematically accurate (using Tau for rotation), and non-destructive. |
| Materials | Shader Node Tree | Needed to achieve the distinct "gummy" subsurface scattering and "sugar" transmission effects. |

> **Feasibility Assessment**: 100% reproduction. Geometry Nodes can perfectly replicate the surface distribution, random orientation, and instancing logic shown in the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "SugarCandy",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.02, 0.05),
    **kwargs,
) -> str:
    """
    Create a procedurally sugar-coated gummy candy using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the base candy object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) color for the gummy base.
        **kwargs: Additional overrides (e.g., density).

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection
    
    # -------------------------------------------------------------------------
    # 1. Create Materials
    # -------------------------------------------------------------------------
    
    # Gummy Base Material (Subsurface Scattering)
    mat_gummy = bpy.data.materials.new(name=f"{object_name}_Gummy_Mat")
    mat_gummy.use_nodes = True
    bsdf_gummy = mat_gummy.node_tree.nodes.get("Principled BSDF")
    if bsdf_gummy:
        bsdf_gummy.inputs["Base Color"].default_value = (*material_color, 1.0)
        # Apply Subsurface Scattering for gelatinous look
        if "Subsurface Weight" in bsdf_gummy.inputs: # Blender 4.0+
            bsdf_gummy.inputs["Subsurface Weight"].default_value = 1.0
            bsdf_gummy.inputs["Subsurface Radius"].default_value = (0.2, 0.2, 0.2)
            bsdf_gummy.inputs["Subsurface Color"].default_value = (*material_color, 1.0)
        elif "Subsurface" in bsdf_gummy.inputs: # Older versions
            bsdf_gummy.inputs["Subsurface"].default_value = 1.0
            bsdf_gummy.inputs["Subsurface Color"].default_value = (*material_color, 1.0)
        bsdf_gummy.inputs["Roughness"].default_value = 0.2

    # Sugar Crystal Material (Transmissive/Glassy)
    mat_sugar = bpy.data.materials.new(name=f"{object_name}_Sugar_Mat")
    mat_sugar.use_nodes = True
    bsdf_sugar = mat_sugar.node_tree.nodes.get("Principled BSDF")
    if bsdf_sugar:
        bsdf_sugar.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0)
        bsdf_sugar.inputs["Roughness"].default_value = 0.25
        bsdf_sugar.inputs["IOR"].default_value = 1.55
        # Set transmission for glassy sugar look
        if "Transmission Weight" in bsdf_sugar.inputs: # Blender 4.0+
            bsdf_sugar.inputs["Transmission Weight"].default_value = 1.0
        elif "Transmission" in bsdf_sugar.inputs: # Older versions
            bsdf_sugar.inputs["Transmission"].default_value = 1.0

    # -------------------------------------------------------------------------
    # 2. Create Instance Geometry (Sugar Crystal)
    # -------------------------------------------------------------------------
    bpy.ops.mesh.primitive_cube_add(size=0.05, location=(0, 0, 0))
    sugar_crystal = bpy.context.active_object
    sugar_crystal.name = f"{object_name}_Crystal_Instance"
    sugar_crystal.data.materials.append(mat_sugar)
    
    # Hide the source crystal from the viewport and render
    sugar_crystal.hide_viewport = True
    sugar_crystal.hide_render = True

    # -------------------------------------------------------------------------
    # 3. Create Base Geometry (Gummy Candy)
    # -------------------------------------------------------------------------
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.45, major_segments=64, minor_segments=32)
    candy_base = bpy.context.active_object
    candy_base.name = object_name
    candy_base.location = Vector(location)
    candy_base.scale = (scale, scale, scale)
    bpy.ops.object.shade_smooth()
    candy_base.data.materials.append(mat_gummy)

    # -------------------------------------------------------------------------
    # 4. Create Geometry Nodes Setup
    # -------------------------------------------------------------------------
    mod = candy_base.modifiers.new(name="SugarCoating", type='NODES')
    tree = bpy.data.node_groups.new(name=f"{object_name}_GeoNodes", type='GeometryNodeTree')
    mod.node_group = tree

    # Handle NodeTree interface setup (Compatible with Blender 3.x and 4.x+)
    if hasattr(tree, "interface"):
        tree.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
        tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        tree.inputs.new('NodeSocketGeometry', "Geometry")
        tree.outputs.new('NodeSocketGeometry', "Geometry")

    nodes = tree.nodes
    links = tree.links

    # Create Nodes
    node_in = nodes.new('NodeGroupInput')
    node_in.location = (-600, 0)
    
    node_out = nodes.new('NodeGroupOutput')
    node_out.location = (600, 0)
    
    node_distribute = nodes.new('GeometryNodeDistributePointsOnFaces')
    node_distribute.location = (-300, 100)
    density = kwargs.get("density", 5000.0) # High density for sugar
    node_distribute.inputs['Density'].default_value = density
    
    node_instance = nodes.new('GeometryNodeInstanceOnPoints')
    node_instance.location = (100, 100)
    
    node_join = nodes.new('GeometryNodeJoinGeometry')
    node_join.location = (400, 0)
    
    node_obj_info = nodes.new('GeometryNodeObjectInfo')
    node_obj_info.location = (-300, -100)
    node_obj_info.inputs['Object'].default_value = sugar_crystal
    
    # Math Note: math.tau is 2*PI, which represents a full 360-degree rotation in radians.
    node_rand_rot = nodes.new('FunctionNodeRandomValue')
    node_rand_rot.data_type = 'FLOAT_VECTOR'
    node_rand_rot.location = (-300, -300)
    node_rand_rot.inputs['Min'].default_value = (0.0, 0.0, 0.0)
    node_rand_rot.inputs['Max'].default_value = (math.tau, math.tau, math.tau) 
    
    node_rand_scale = nodes.new('FunctionNodeRandomValue')
    node_rand_scale.data_type = 'FLOAT'
    node_rand_scale.location = (-300, -500)
    node_rand_scale.inputs['Min'].default_value = 0.02
    node_rand_scale.inputs['Max'].default_value = 0.08

    # Link Nodes
    links.new(node_in.outputs[0], node_distribute.inputs['Mesh'])
    links.new(node_distribute.outputs['Points'], node_instance.inputs['Points'])
    
    # Connect Instance data
    links.new(node_obj_info.outputs['Geometry'], node_instance.inputs['Instance'])
    links.new(node_rand_rot.outputs['Value'], node_instance.inputs['Rotation'])
    links.new(node_rand_scale.outputs['Value'], node_instance.inputs['Scale'])
    
    # Join instances with original base geometry
    links.new(node_in.outputs[0], node_join.inputs['Geometry'])
    links.new(node_instance.outputs['Instances'], node_join.inputs['Geometry'])
    
    # Output
    links.new(node_join.outputs['Geometry'], node_out.inputs[0])

    # De-select all, select the new base object
    bpy.ops.object.select_all(action='DESELECT')
    candy_base.select_set(True)
    bpy.context.view_layer.objects.active = candy_base

    return f"Created procedural sugar-coated '{object_name}' at {location} with {density} density points."
```