### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized Character Workspace & Scale Reference

* **Core Visual Mechanism**: Transitioning the global Color Management from a photorealistic tone-mapper (AgX/Filmic) to a linear `Standard` view transform. This ensures 1:1 color output. It is paired with spawning a predefined Human Meta-Rig from the built-in Rigify addon to establish standardized human proportions before modeling begins.
* **Why Use This Skill (Rationale)**: By default, Blender uses AgX or Filmic color spaces designed to roll off highlights and emulate camera sensors. For stylized, low-poly, or anime-style 3D art, this photorealistic tone mapping causes hand-painted textures or flat colors to look washed out or desaturated. Setting the View Transform to `Standard` guarantees that the colors you pick are the exact colors rendered on screen. Spawning a Meta-Rig provides an immediate, standard scale baseline, ensuring your character isn't modeled too large or too small relative to Blender's world units.
* **Overall Applicability**: This is the mandatory first step for any stylized character modeling workflow, low-poly game asset creation, or cell-shaded animation project where strict color fidelity and human proportions are required.
* **Value Addition**: Compared to starting with an empty scene or default cube, this skill preemptively fixes color desaturation issues, optimizes the EEVEE render engine for flat shading (disabling heavy photorealistic calculations), and places a proportional scaffolding (the rig) directly into the viewport.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Scale Reference**: Uses the built-in `rigging_rigify` addon to spawn a `Human Meta-Rig` (`bpy.ops.object.armature_human_metarig_add`).
  - **Display Settings**: The armature is set to `show_in_front = True` so it remains visible as a template even when geometry is built around it.
  - **Pedestal (Demo)**: A low-poly cylinder (16 vertices) is spawned underneath the rig to demonstrate the color management changes.
* **Step B: Materials & Shading**
  - **Shader Model**: To emulate game-engine unlit materials and prove the color space is set correctly, the pedestal uses a pure `ShaderNodeEmission` connected directly to the output.
  - **Color Fidelity**: Because the scene is set to `Standard` view transform, the RGB values fed into the Emission node will perfectly match the rendered output on your monitor, with no highlight compression.
* **Step C: Lighting & Rendering Context**
  - **Render Engine**: EEVEE is selected as it is the standard for real-time stylized rendering.
  - **Color Management**: `scene.view_settings.view_transform = 'Standard'`.
  - **Post-Processing**: Ambient Occlusion, Bloom, Screen Space Reflections, and Motion Blur are disabled to prevent photorealistic light bleeding from affecting the flat, stylized look.
* **Step D: Animation & Dynamics (if applicable)**
  - The spawned Meta-Rig contains predefined bone placements for a bipedal character, acting as a template. While not animated out of the box, it is the standard starting point for generating a complex animation control rig later in the pipeline.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Color Space | `bpy.context.scene.view_settings` | Bypasses default tone mapping for exact 1:1 color rendering. |
| Scale Reference | `addon_utils` + `bpy.ops` | The Rigify human meta-rig is the industry-standard scale reference in Blender. |
| Flat Material | Shader Node Tree (Emission) | Pure emission nodes are the best way to achieve unlit, flat-shaded materials for low-poly art. |

> **Feasibility Assessment**: 100% — This code perfectly replicates the tutorial's foundational scene setup and scales reference alignment, preparing the workspace for stylized character modeling.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "ScaleReferenceRig",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.94, 0.40, 0.55), # Stylized pink
    **kwargs,
) -> str:
    """
    Configures the scene for stylized flat-shading and creates a scale reference rig.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created armature rig.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the rig.
        material_color: (R, G, B) flat color applied to the display pedestal.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import addon_utils
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Render & Color Management Setup ===
    # Switch to EEVEE for stylized rendering
    scene.render.engine = 'BLENDER_EEVEE'

    # Set View Transform to Standard. This is critical for stylized rendering
    # as it prevents AgX/Filmic from desaturating pure color values.
    scene.view_settings.view_transform = 'Standard'

    # Disable photorealistic effects (using getattr/setattr to safely handle different Blender versions)
    if hasattr(scene, 'eevee'):
        for attr in ['use_gtao', 'use_bloom', 'use_ssr', 'use_motion_blur']:
            if hasattr(scene.eevee, attr):
                setattr(scene.eevee, attr, False)

    # === Step 2: Enable Rigify Addon ===
    addon_name = "rigging_rigify"
    is_loaded, is_enabled = addon_utils.check(addon_name)
    if not is_enabled:
        addon_utils.enable(addon_name, default_set=True)

    # === Step 3: Spawn Scale Reference (Human Meta-Rig) ===
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.armature_human_metarig_add(location=location)
    rig = bpy.context.active_object
    rig.name = object_name
    rig.scale = (scale, scale, scale)

    # Apply scale so modeling on top of it has 1.0 scale dimensions
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Make the rig display in front of geometry
    rig.show_in_front = True

    # === Step 4: Create a stylized base pedestal to demonstrate flat color ===
    pedestal_loc = (location[0], location[1], location[2] - (0.05 * scale))
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=1.5 * scale,
        depth=0.1 * scale,
        location=pedestal_loc
    )
    pedestal = bpy.context.active_object
    pedestal.name = f"{object_name}_Pedestal"

    # Create flat/unlit material
    mat = bpy.data.materials.new(name=f"{object_name}_UnlitMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    emission_node = nodes.new(type='ShaderNodeEmission')
    emission_node.inputs['Color'].default_value = (*material_color, 1.0)
    links.new(emission_node.outputs['Emission'], out_node.inputs['Surface'])

    pedestal.data.materials.append(mat)

    # Parent pedestal to rig for scene organization
    pedestal.parent = rig

    return f"Configured scene to Standard color space and spawned '{object_name}' with pedestal at {location}"
```