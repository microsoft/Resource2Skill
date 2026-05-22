# Compositor Reference Split Pipeline

## Analysis

Here is an extraction of the primary technical workflow pattern demonstrated in the video. While the video is mostly high-level advice, tip #5 ("Stick to Reference") contains a highly specific, reproducible node-based setup used to ensure 3D modeling and lighting accuracy.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Compositor Reference Split Pipeline

* **Core Visual Mechanism**: Using the Blender Compositor's `Split` node to overlay a 2D reference image precisely onto the active 3D render output. This creates a side-by-side or sliding curtain effect, allowing for direct 1:1 visual comparison of silhouette, texturing, and lighting.

* **Why Use This Skill (Rationale)**: The video highlights that one of the biggest time-wasters for beginners is modeling "from imagination." When a piece is finished, there is no "ground truth" to compare it against to see what went wrong. By building this specific compositor pipeline, artists are forced to match focal length, light direction, exposure, and material glossiness exactly to a real photograph, drastically accelerating learning and quality.

* **Overall Applicability**: Essential for Look Development (LookDev), photorealistic prop modeling, lighting studies, and texture matching. It acts as an automated "mentor" that immediately reveals inaccuracies in your 3D scene.

* **Value Addition**: Automates the wiring of a comparison pipeline. Instead of constantly tabbing between an image viewer and Blender, the reference becomes integrated directly into the render result, allowing for pixel-perfect adjustments.

### 2. Technical Breakdown

* **Step A: Scene Integration**
  - The scene must have `use_nodes` enabled to activate the compositor.
  - A standard 3D object and Camera are required so the `Render Layers` node has data to output.

* **Step B: Compositor Node Tree**
  - **Render Layers Node**: Grabs the active 3D viewport render.
  - **Image Node**: Loads the ground-truth reference photograph.
  - **Transform Node**: Added between the Image and Split node. This is crucial because reference images rarely match the exact aspect ratio or pixel scale of the Blender camera. It allows scaling and translating the 2D image to align with the 3D model.
  - **Split Node**: The core mechanism. It takes the Render output in Input 1, and the transformed Reference Image in Input 2, splitting them along the X or Y axis.
  - **Composite & Viewer Nodes**: Final output destinations to view the split result.

* **Step C: Usage Context**
  - Once generated, the user simply loads an image into the "LOAD REFERENCE HERE" node, renders the scene (F12), and slides the `Factor` value on the Split node to check their work.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Pipeline construction | `bpy.context.scene.node_tree` manipulation | The only way to build a post-processing setup programmatically without manual wiring. |
| Object preview | `bpy.ops.mesh.primitive` | Adds a placeholder mesh so the compositor has actual 3D data to split against the reference. |

> **Feasibility Assessment**: 100%. The exact compositor node tree shown at the 7:00 mark of the video is faithfully recreated, complete with the Transform node required for alignment.

#### 3b. Complete Reproduction Code

```python
def create_compositor_reference_split(
    scene_name: str = "Scene",
    object_name: str = "Dummy_Target",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Creates the Reference Split Compositor pipeline taught in the video,
    along with a basic dummy object and camera to demonstrate the effect.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the placeholder 3D object.
        location: (x, y, z) world-space position for the placeholder.
        scale: Uniform scale factor for the placeholder.
        material_color: (R, G, B) base color for the placeholder.
        **kwargs: Optional 'split_factor' (int 0-100) and 'axis' ('X' or 'Y').

    Returns:
        Status string detailing the nodes created.
    """
    import bpy
    import math
    from mathutils import Vector

    # Parse kwargs
    split_factor = int(kwargs.get('split_factor', 50))
    axis = kwargs.get('axis', 'X')

    # 1. Get Scene and Enable Compositor
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    scene.use_nodes = True
    tree = scene.node_tree
    nodes = tree.nodes
    links = tree.links

    # 2. Add Dummy Object and Camera to ensure Render Layers has data
    if object_name not in bpy.data.objects:
        bpy.ops.mesh.primitive_monkey_add(location=location)
        obj = bpy.context.active_object
        obj.name = object_name
        obj.scale = (scale, scale, scale)
        
        # Add basic material
        mat = bpy.data.materials.new(name=f"{object_name}_Mat")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        obj.data.materials.append(mat)

    # Add Camera if missing
    if not scene.camera:
        cam_data = bpy.data.cameras.new("Ref_Camera")
        cam_obj = bpy.data.objects.new("Ref_Camera", cam_data)
        bpy.context.collection.objects.link(cam_obj)
        cam_obj.location = Vector(location) + Vector((0, -5, 1))
        cam_obj.rotation_euler = (math.radians(80), 0, 0)
        scene.camera = cam_obj

    # 3. Setup Compositor Nodes
    # Find existing base nodes
    render_layers = next((n for n in nodes if n.type == 'R_LAYERS'), None)
    composite = next((n for n in nodes if n.type == 'COMPOSITE'), None)

    if not render_layers:
        render_layers = nodes.new('CompositorNodeRLayers')
        render_layers.location = (-400, 0)
    if not composite:
        composite = nodes.new('CompositorNodeComposite')
        composite.location = (400, 0)

    # 4. Create Reference Split nodes
    # Check if we already created it to avoid duplicates
    if "Reference_Image" not in nodes:
        img_node = nodes.new('CompositorNodeImage')
        img_node.name = "Reference_Image"
        img_node.label = "1. LOAD REFERENCE HERE"
        img_node.location = (-400, -300)

        transform_node = nodes.new('CompositorNodeTransform')
        transform_node.name = "Reference_Transform"
        transform_node.label = "2. ALIGN REFERENCE"
        transform_node.location = (-150, -300)

        split_node = nodes.new('CompositorNodeSplit')
        split_node.name = "Reference_Split"
        split_node.label = "3. SLIDE TO COMPARE"
        split_node.axis = axis
        split_node.factor = split_factor
        split_node.location = (150, -100)

        viewer_node = nodes.new('CompositorNodeViewer')
        viewer_node.location = (400, -300)

        # 5. Wire the network
        links.new(img_node.outputs['Image'], transform_node.inputs['Image'])
        links.new(render_layers.outputs['Image'], split_node.inputs[0]) # Input 1: Render
        links.new(transform_node.outputs['Image'], split_node.inputs[1]) # Input 2: Reference Image
        
        # Connect split to final outputs
        links.new(split_node.outputs['Image'], composite.inputs['Image'])
        links.new(split_node.outputs['Image'], viewer_node.inputs['Image'])

    return f"Created Compositor Reference pipeline. Load an image into the '{object_name}' scene compositor."
```