### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized NPR Scene & Scale Reference Setup

* **Core Visual Mechanism**: The core of this technique isn't a 3D mesh, but the **architectural configuration of the rendering environment** specifically tuned for Non-Photorealistic Rendering (NPR) and stylized low-poly art. The signature mechanism is switching Blender's Color Management View Transform from tone-mapped (AgX/Filmic) to linear (`Standard`), combined with disabling physically-based rendering screen-space effects (AO, Bloom, SSR).
* **Why Use This Skill (Rationale)**: Default Blender is configured to mimic real-world cameras (Filmic/AgX compress dynamic range to prevent clipping). However, when painting anime or low-poly textures, you want the exact hex colors you pick to render 1:1 on the screen without being desaturated or shifted by tone-mapping. Furthermore, placing a Human Meta-Rig before modeling ensures the character's proportions are structurally sound and appropriately scaled (approx. 1.8m) for export to game engines.
* **Overall Applicability**: This is the mandatory "Step Zero" for any project aimed at anime-style cel-shading, retro PS1/N64 low-poly aesthetics, or stylized mobile game assets. 
* **Value Addition**: Automating this boilerplate setup prevents lighting artifacts, color wash-out, and severe scaling issues that often plague beginners who model stylized characters in photorealistic scene constraints.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Primitive**: Instead of a mesh, a `Human Meta-Rig` (via the Rigify addon) is spawned to establish a strict 3D bounding box for human proportions. 
  - **Reference Planes**: Empty objects configured as `IMAGE` types are spawned and rigidly rotated 90 degrees on the X and Z axes to act as front and side orthographic modeling guides.
* **Step B: Materials & Shading**
  - **Color Management**: `scene.view_settings.view_transform` is strictly set to `'Standard'`.
  - **Reference Opacity**: The reference image empties have their viewport color alpha set to `0.5` to allow "x-ray" style modeling over the references.
* **Step C: Lighting & Rendering Context**
  - **Render Engine**: EEVEE is forced.
  - **Post-Processing**: Ambient Occlusion, Bloom, Screen Space Reflections, and Motion Blur are explicitly disabled on the EEVEE engine properties to maintain a flat, unpolluted viewport.
* **Step D: Animation & Dynamics**
  - Not applicable for scene setup, though the Rigify skeleton lays the exact foundation needed for the eventual character rig.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Scene Configuration | `bpy.types.Scene` attributes | Direct modification of EEVEE and Color Management parameters is the only way to enforce the NPR look. |
| Scale Reference | `bpy.ops.preferences.addon_enable` + Meta-Rig | Automates the enabling of Blender's built-in Rigify addon to spawn an industry-standard human proportion guide. |
| Image References | `bpy.data.objects.new(..., None)` | Bypasses operators to cleanly spawn and orient Empty Placeholders for orthographic drafting. |

> **Feasibility Assessment**: 100% of the structural setup shown in the video is reproduced. Note that the script generates placeholder Image Empties; it cannot download the creator's specific reference `.png` files from the web, but the geometric alignment and transparency settings for those references are fully automated.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "Stylized_NPR_Workspace",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create Stylized NPR Scene & Scale Reference Setup in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the parent workspace empty.
        location: (x, y, z) world-space position for the setup.
        scale: Uniform scale factor for the references.
        material_color: (R, G, B) used to color the fallback rig.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Enforce NPR / Stylized Scene Settings ===
    if hasattr(scene, "render"):
        scene.render.engine = 'BLENDER_EEVEE'
        
    if hasattr(scene, "eevee"):
        # Disable photorealistic screen-space effects for clean flat shading
        eevee_flags = ['use_gtao', 'use_bloom', 'use_ssr', 'use_motion_blur']
        for flag in eevee_flags:
            if hasattr(scene.eevee, flag):
                setattr(scene.eevee, flag, False)
                
    if hasattr(scene, "view_settings"):
        # CRUCIAL: 'Standard' prevents tonemapping from washing out stylized hex colors
        try:
            scene.view_settings.view_transform = 'Standard'
        except TypeError:
            pass

    # === Step 2: Create Workspace Parent Structure ===
    parent_empty = bpy.data.objects.new(object_name, None)
    parent_empty.empty_display_size = scale
    parent_empty.empty_display_type = 'PLAIN_AXES'
    parent_empty.location = Vector(location)
    scene.collection.objects.link(parent_empty)

    # === Step 3: Create Human Scale Reference (Rigify or Fallback) ===
    rig = None
    try:
        # Attempt to enable Rigify and spawn the standard Human Meta-Rig
        bpy.ops.preferences.addon_enable(module='rigify')
        
        # Keep track of objects before the operator
        existing_objs = set(scene.objects)
        bpy.ops.object.armature_human_metarig_add(location=location)
        
        # Find the newly created rig
        new_objs = set(scene.objects) - existing_objs
        if new_objs:
            rig = list(new_objs)[0]
            rig.name = f"{object_name}_HumanMetaRig"
    except Exception:
        pass

    if not rig:
        # Fallback to a simple armature if Rigify fails/is unavailable
        arm_data = bpy.data.armatures.new(f"{object_name}_ArmatureData")
        rig = bpy.data.objects.new(f"{object_name}_ScaleRig", arm_data)
        scene.collection.objects.link(rig)
        rig.location = Vector(location)
        
        # Scale to roughly average human height (1.8m)
        rig.scale = (1.8 * scale, 1.8 * scale, 1.8 * scale)
        rig.color = (*material_color, 1.0)

    rig.parent = parent_empty

    # === Step 4: Create Orthographic Reference Image Placeholders ===
    
    # Front Reference Placeholder (Moved slightly back on Y)
    empty_front = bpy.data.objects.new(f"{object_name}_Ref_Front", None)
    empty_front.empty_display_type = 'IMAGE'
    empty_front.empty_display_size = 2.0 * scale
    empty_front.location = Vector(location) + Vector((0, 1.5 * scale, 1.0 * scale))
    empty_front.rotation_euler = (math.radians(90), 0, 0)
    empty_front.color = (1.0, 1.0, 1.0, 0.5) # Prepare 50% opacity
    empty_front.parent = parent_empty
    scene.collection.objects.link(empty_front)

    # Side Reference Placeholder (Moved slightly right on X)
    empty_side = bpy.data.objects.new(f"{object_name}_Ref_Side", None)
    empty_side.empty_display_type = 'IMAGE'
    empty_side.empty_display_size = 2.0 * scale
    empty_side.location = Vector(location) + Vector((1.5 * scale, 0, 1.0 * scale))
    empty_side.rotation_euler = (math.radians(90), 0, math.radians(90))
    empty_side.color = (1.0, 1.0, 1.0, 0.5) # Prepare 50% opacity
    empty_side.parent = parent_empty
    scene.collection.objects.link(empty_side)

    # Select the parent to signify the end of the operation
    bpy.context.view_layer.objects.active = parent_empty
    parent_empty.select_set(True)

    return f"Created NPR Workspace '{object_name}' (View Transform: Standard, Ref Empties, Scale Rig generated)."
```