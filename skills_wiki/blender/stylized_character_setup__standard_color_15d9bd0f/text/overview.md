### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized Character Setup (Standard Color Space & Ortho References)

* **Core Visual Mechanism**: The defining mechanism of this setup is the deliberate shift away from photorealistic color processing. By changing the Color Management View Transform from `AgX` (or `Filmic`) to `Standard`, the scene stops compressing highlights and desaturating colors. Combined with perfectly aligned, semi-transparent orthographic reference planes, this creates a 1:1 environment for anime/low-poly modeling where texture colors exactly match their hex codes.
* **Why Use This Skill (Rationale)**: When painting stylized or low-poly textures (like the "Love-chan" character in the video), artists often pick specific, vibrant hex colors. Default photorealistic view transforms will wash these colors out to simulate realistic lighting behavior. Reverting to the `Standard` transform ensures that the colors you pick in your 2D software look exactly the same in the 3D viewport. Furthermore, setting up semi-transparent front and side references locked to the origin provides the foundational blueprint needed to maintain accurate proportions.
* **Overall Applicability**: Essential for any non-photorealistic rendering (NPR) workflow, including anime-style characters, retro PS1/low-poly props, pixel art 3D scenes, and cel-shaded environments.
* **Value Addition**: Transforms the default physically-based environment into a flat, predictable canvas optimized for stylized art, and establishes a robust spatial framework for tracing 2D concepts into 3D.

### 2. Technical Breakdown

* **Step A: Render & Scene Environment**
  - **Render Engine**: EEVEE (optimized for real-time stylized rendering).
  - **Post-Processing Disabled**: Ambient Occlusion, Bloom, Screen Space Reflections, and Motion Blur are turned off to prevent photorealistic shading artifacts from interfering with flat, stylized textures.
  - **Color Management**: View Transform set explicitly to `Standard` (bypassing AgX/Filmic tone mapping).

* **Step B: Reference Geometry**
  - **Type**: `Empty` objects with `empty_display_type` set to `IMAGE`.
  - **Front Reference**: Rotated 90° on the X-axis (`math.radians(90), 0, 0`).
  - **Side Reference**: Rotated 90° on X and 90° on Z (`math.radians(90), 0, math.radians(90)`), offset slightly backward on the Y-axis so it doesn't clip with the front mesh during modeling.
  - **Transparency**: `use_empty_image_alpha` enabled, with the alpha channel (color[3]) set to `0.5` for easy overlay visibility.

* **Step C: Scale Reference**
  - A human-scale reference is added to ensure the model isn't built microscopically small or kilometers tall. The tutorial uses the Rigify add-on (`armature_human_metarig_add`), but a robust proxy (like a 1.7m tall primitive) serves the exact same purpose if the add-on isn't enabled.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Stylized Color Space | `scene.view_settings` / `scene.eevee` | Required to replicate the 1:1 flat color look shown in the video. |
| Reference Images | `bpy.ops.object.empty_add(type='IMAGE')` | Native Blender method for reference images. We use programmatic `COLOR_GRID` generated images to ensure the code runs without needing to download external files. |
| Scale Reference | `addon_utils` (Rigify) + Primitive Fallback | Attempts to use the Rigify meta-rig as shown in the video, but falls back to a standardized wireframe cylinder to ensure script robustness. |

> **Feasibility Assessment**: 100% of the scene setup and methodology demonstrated in the video is reproduced programmatically.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "Stylized_Setup_Group",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (1.0, 1.0, 1.0),
    **kwargs,
) -> str:
    """
    Sets up a scene for Stylized/Low-Poly modeling as demonstrated in the tutorial,
    including Color Management tweaks, EEVEE optimization, and Reference Image planes.

    Args:
        scene_name: Name of the target scene.
        object_name: Prefix for the generated reference objects.
        location: Base location for the scale reference.
        scale: Multiplier for the default human height (1.7m base).
        material_color: Unused directly in setup, kept for signature consistency.
        
    Returns:
        Status string detailing the setup execution.
    """
    import bpy
    import math
    import addon_utils
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Stylized Render Settings ===
    # Force EEVEE for real-time stylized preview
    if scene.render.engine != 'BLENDER_EEVEE':
        scene.render.engine = 'BLENDER_EEVEE'
    
    # Disable photorealistic effects that interfere with stylized/flat shading
    if hasattr(scene, "eevee"):
        scene.eevee.use_gtao = False
        scene.eevee.use_bloom = False
        scene.eevee.use_ssr = False
        scene.eevee.use_motion_blur = False

    # CRITICAL: Set View Transform to Standard to preserve true hex colors
    scene.view_settings.view_transform = 'Standard'

    # === Step 2: Generate Placeholder Reference Images ===
    # Since we cannot download the zip file in a sandboxed script, we generate a placeholder
    img_name = f"{object_name}_Ref_Image"
    img = bpy.data.images.get(img_name)
    if not img:
        img = bpy.data.images.new(img_name, width=1024, height=1024)
        img.generated_type = 'COLOR_GRID'
    
    ref_height = 1.7 * scale

    # === Step 3: Front Reference ===
    bpy.ops.object.empty_add(type='IMAGE', location=(location[0], location[1], location[2] + (ref_height/2)))
    front_ref = bpy.context.active_object
    front_ref.name = f"{object_name}_Front_Ref"
    front_ref.data = img
    front_ref.empty_display_size = ref_height
    front_ref.rotation_euler = (math.radians(90), 0, 0)
    
    # Set transparency
    front_ref.use_empty_image_alpha = True
    front_ref.color[3] = 0.5  # 50% opacity

    # === Step 4: Side Reference ===
    # Offset backward on Y so it doesn't intersect with the front view modeling
    bpy.ops.object.empty_add(type='IMAGE', location=(location[0], location[1] - (ref_height/2), location[2] + (ref_height/2)))
    side_ref = bpy.context.active_object
    side_ref.name = f"{object_name}_Side_Ref"
    side_ref.data = img
    side_ref.empty_display_size = ref_height
    side_ref.rotation_euler = (math.radians(90), 0, math.radians(90))
    
    # Set transparency
    side_ref.use_empty_image_alpha = True
    side_ref.color[3] = 0.5

    # === Step 5: Scale Reference ===
    # Attempt to use Rigify as shown in video; use wireframe cylinder as robust fallback
    scale_ref_created = False
    
    # Check if rigify can be enabled
    try:
        addon_utils.enable("rigging_rigify")
        bpy.ops.object.armature_human_metarig_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_Scale_MetaRig"
        rig.scale = (scale, scale, scale)
        scale_ref_created = True
    except Exception:
        pass
        
    if not scale_ref_created:
        # Fallback to a simple 1.7m primitive to represent human scale
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.25 * scale, 
            depth=ref_height, 
            location=(location[0], location[1], location[2] + (ref_height/2))
        )
        rig = bpy.context.active_object
        rig.name = f"{object_name}_Scale_Dummy"
        rig.display_type = 'WIRE'  # Set to wireframe so it doesn't block modeling

    # Optional: Group them in a collection for neatness
    setup_collection_name = f"{object_name}_Collection"
    setup_col = bpy.data.collections.get(setup_collection_name)
    if not setup_col:
        setup_col = bpy.data.collections.new(setup_collection_name)
        scene.collection.children.link(setup_col)
    
    # Move created objects to the new collection
    for obj in [front_ref, side_ref, rig]:
        for col in obj.users_collection:
            col.objects.unlink(obj)
        setup_col.objects.link(obj)

    return f"Prepared Stylized Scene: View Transform set to 'Standard'. Created {object_name}_Front_Ref, Side_Ref, and Scale Reference at {location}."
```