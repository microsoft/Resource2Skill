# Hard-Surface Boolean Component with Bevel Shader

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Hard-Surface Boolean Component with Bevel Shader

* **Core Visual Mechanism**: This technique uses non-destructive Boolean modifiers to carve complex mechanical details (like slots and holes) out of a primitive shape, bypassing traditional topological cleanup. The defining "magic" is the use of the Cycles `Bevel` shader node plugged directly into the `Normal` input of the Principled BSDF. This fakes perfectly rounded, smooth highlights on all the harsh boolean intersections at render time.

* **Why Use This Skill (Rationale)**: Hard-surface modeling often suffers from shading artifacts when boolean cuts ruin the mesh topology, usually requiring hours of painstaking control loop placement or subdivision surface tuning. This workflow allows artists to focus entirely on silhouette and design. The geometry stays messy and lightweight, but the render looks like a highly refined, subdivided, and beveled mechanical part.

* **Overall Applicability**: Essential for rapid concept art, sci-fi props, mechs, weapon attachments (like muzzle brakes, barrels, and scopes), and kitbashing assets where physical accuracy of the mesh is less important than the final rendered image.

* **Value Addition**: Transforms basic intersecting primitives into a complex, manufactured-looking object. It achieves AAA-quality edge highlights without the massive polygon count normally required for curved, beveled cutouts.


### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A simple Cylinder rotated 90 degrees to lie flat.
  - **Cutters**: Additional cylinders stretched into oval "pill" shapes for side exhaust slots, and standard cylinders for top ventilation holes.
  - **Modifiers**: 
    - `Array` modifiers on the cutters to repeat the shapes cleanly.
    - `Boolean` modifiers (Difference) on the base mesh.
    - `Edge Split` modifier on the base mesh to ensure the flat faces shade perfectly flat in the viewport, providing a clean canvas for the shader to work on.

* **Step B: Materials & Shading**
  - **Shader Model**: Principled BSDF designed to look like machined gunmetal.
  - **Colors**: Base color `(0.3, 0.3, 0.35)` (dark steel).
  - **Properties**: High `Metallic` (0.9) and low `Roughness` (0.25) to catch light on the beveled edges.
  - **The Secret Sauce**: A `ShaderNodeBevel` (Radius ~0.04, Samples 6) connected to the `Normal` input of the BSDF. This samples adjacent faces during raytracing to blend the normals across the sharp, disconnected boolean intersections.

* **Step C: Lighting & Rendering Context**
  - **Render Engine**: Must be **Cycles**. The Bevel shader node evaluates geometric intersections during raytracing and *does not work* in EEVEE.
  - **Lighting**: Best paired with a high-contrast HDRI or multi-point lighting to catch the artificial edge highlights created by the Bevel node.

* **Step D: Animation & Dynamics**
  - Entirely procedural and non-destructive. Cutters can be animated to "eat" into the mesh over time, or array counts can be driven by custom properties to create procedural weapon variants.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base & Cutters | `bpy.ops.mesh.primitive_*` | Provides the necessary solid volumes for Boolean operations. |
| Repetitive Features | Array Modifier | Keeps the cutter logic parametric and non-destructive. |
| Cutout Detailing | Boolean Modifier | Allows complex surface detailing without manual topological modeling. |
| Edge Rounding | Shader Node Tree (`Bevel` node) | Fakes rounded bevels at render time, ignoring the messy boolean topology entirely. |

> **Feasibility Assessment**: 100% reproduction of the technique. The code replicates the exact modeling workflow and material node setup required to generate smooth boolean cuts in Cycles.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "SciFi_MuzzleBrake",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.2, 0.22),
    **kwargs,
) -> str:
    """
    Creates a procedural hard-surface component using Booleans and a Bevel Shader.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) color for the gunmetal material.
        **kwargs: Additional options.
        
    Returns:
        Status string confirming creation.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # The Bevel shader node is exclusive to Cycles raytracing
    scene.render.engine = 'CYCLES'

    # Create a Master Parent Empty
    parent = bpy.data.objects.new(object_name, None)
    scene.collection.objects.link(parent)
    parent.location = Vector(location)
    parent.scale = (scale, scale, scale)

    # === 1. Base Geometry ===
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=1, depth=6)
    base_obj = bpy.context.active_object
    base_obj.name = f"{object_name}_Base"
    base_obj.parent = parent
    # Rotate to lie along the X axis
    base_obj.rotation_euler = (0, math.radians(90), 0)
    
    bpy.ops.object.shade_smooth()

    # Edge Split ensures boolean intersections look sharp in viewport, 
    # setting up a perfect base for the Bevel node to blend.
    edge_split = base_obj.modifiers.new(name="EdgeSplit", type='EDGE_SPLIT')
    edge_split.split_angle = math.radians(40)

    # === 2. Hidden Collection for Cutters ===
    cutter_coll_name = "Hidden_Boolean_Cutters"
    cutter_coll = bpy.data.collections.get(cutter_coll_name)
    if not cutter_coll:
        cutter_coll = bpy.data.collections.new(cutter_coll_name)
        scene.collection.children.link(cutter_coll)
        cutter_coll.hide_viewport = True
        cutter_coll.hide_render = True

    # === 3. Cutter A: Side Exhaust Slots ===
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.35, depth=4)
    cutter_side = bpy.context.active_object
    cutter_side.name = f"{object_name}_Cutter_Side"
    
    # Move to the hidden collection
    bpy.context.collection.objects.unlink(cutter_side)
    cutter_coll.objects.link(cutter_side)
    
    cutter_side.parent = parent
    cutter_side.rotation_euler = (math.radians(90), 0, 0) # Align to Y axis
    cutter_side.location = (-1.8, 0, 0)
    cutter_side.scale = (1.5, 1.0, 1.0) # Stretch into an oval pill shape
    
    # Array modifier to repeat the slot
    arr_side = cutter_side.modifiers.new("Array", 'ARRAY')
    arr_side.count = 4
    arr_side.use_relative_offset = False
    arr_side.use_constant_offset = True
    arr_side.constant_offset_displace = (1.2, 0, 0)

    # Apply Boolean to Base
    bool_side = base_obj.modifiers.new("Bool_Side", 'BOOLEAN')
    bool_side.operation = 'DIFFERENCE'
    bool_side.object = cutter_side

    # === 4. Cutter B: Top Ventilation Holes ===
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.25, depth=4)
    cutter_top = bpy.context.active_object
    cutter_top.name = f"{object_name}_Cutter_Top"
    
    # Move to the hidden collection
    bpy.context.collection.objects.unlink(cutter_top)
    cutter_coll.objects.link(cutter_top)
    
    cutter_top.parent = parent
    cutter_top.location = (-1.5, 0, 0) # Aligned to Z by default
    
    # Array modifier to repeat the holes
    arr_top = cutter_top.modifiers.new("Array", 'ARRAY')
    arr_top.count = 3
    arr_top.use_relative_offset = False
    arr_top.use_constant_offset = True
    arr_top.constant_offset_displace = (1.5, 0, 0)

    # Apply Boolean to Base
    bool_top = base_obj.modifiers.new("Bool_Top", 'BOOLEAN')
    bool_top.operation = 'DIFFERENCE'
    bool_top.object = cutter_top

    # === 5. Material & Bevel Shader Setup ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Metallic"].default_value = 0.9
        bsdf.inputs["Roughness"].default_value = 0.25

        # The Bevel Node - creates the illusion of smooth geometry at render time
        bevel_node = nodes.new(type="ShaderNodeBevel")
        bevel_node.inputs["Radius"].default_value = 0.04
        bevel_node.samples = 6
        
        # Link Bevel normal to BSDF normal
        links.new(bevel_node.outputs["Normal"], bsdf.inputs["Normal"])

    base_obj.data.materials.append(mat)

    return f"Created hard-surface boolean component '{object_name}' with Bevel shader at {location}"
```