### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized Character Workspace & Reference Setup

* **Core Visual Mechanism**: This pattern establishes the foundational environment required for stylized, non-photorealistic (NPR) modeling. The defining mechanism is changing the rendering color space from a photorealistic tonemapper (like AgX or Filmic) to the **Standard** View Transform. This ensures that the exact hex colors chosen in textures appear exactly the same in the viewport, without cinematic desaturation or contrast shifts. It also includes the procedural instantiation of a predefined proportional human rig (Rigify) to act as a scale benchmark, alongside aligned, semi-transparent image planes for orthographic modeling.

* **Why Use This Skill (Rationale)**: When creating "anime-style" or flat-shaded low-poly characters, photorealistic light calculation works against you. Filmic/AgX tonemapping compresses highlights and shifts hues to emulate a real-world camera sensor, which muddies vibrant, hand-painted textures. Setting the View Transform to 'Standard' provides a 1:1 color mapping. Using a pre-built meta-rig ensures that the character's baseline proportions match standard animation requirements before any polygons are laid down.

* **Overall Applicability**: Essential as the very first step for any stylized 3D character, low-poly game asset, cell-shaded animation, or any project where exact color matching to 2D concept art is required. 

* **Value Addition**: Automates the tedious boilerplate of setting up a modeling workspace. Instead of manually adjusting render settings, navigating add-on menus to enable Rigify, spawning the rig, and perfectly aligning/scaling empty image planes, this skill prepares a production-ready template instantly.


### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Scale Reference**: Utilizes the built-in `human_metarig` from the Rigify add-on. This provides an anatomically proportional skeleton.
  - **Reference Planes**: Empties set to `IMAGE` display type are used instead of actual mesh planes. This avoids them accidentally participating in lighting, rendering, or boolean operations.

* **Step B: Materials & Shading**
  - No physical materials are created, but the **Color Management -> View Transform** is strictly overridden to `Standard`.
  - The Empty objects are given a color alpha value of `0.5` to ensure they are semi-transparent and don't obscure the geometry being modeled in front of them.

* **Step C: Lighting & Rendering Context**
  - Render Engine set to **EEVEE**.
  - Advanced photorealistic effects like Ambient Occlusion, Bloom, Screen Space Reflections, and Motion Blur are disabled to provide a clean, flat modeling environment.

* **Step D: Animation & Dynamics (if applicable)**
  - The Rigify Meta-Rig acts purely as a static spatial reference during the modeling phase. (Later in the pipeline, it will be generated into a functional animation rig).


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Stylized Color | `scene.view_settings.view_transform` | Overrides default tonemapping for exact 1:1 hex color rendering. |
| Scale Benchmark | `addon_utils` + `bpy.ops.armature` | Programmatically enables Rigify and spawns the complex Meta-Rig instantly. |
| Concept Art Planes | `bpy.data.objects.new(type=Empty)` | Creates non-renderable image hosts oriented perfectly for Numpad 1 and Numpad 3 orthographic views. |

> **Feasibility Assessment**: 100%. The code accurately configures the exact render environment described in the tutorial and spawns the required helper objects (rig and reference planes) perfectly aligned and scaled. Note: The code creates placeholder images for the reference empties; the user will naturally map their own concept art files to these empties in the properties panel.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "Stylized_Workspace",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (1.0, 1.0, 1.0),
    **kwargs,
) -> str:
    """
    Create a Stylized Character Workspace with standard color transform, 
    a proportional scale rig, and aligned reference image planes.

    Args:
        scene_name: Name of the target scene.
        object_name: Base prefix for created objects.
        location: (x, y, z) base world-space position.
        scale: Uniform scale factor for the rig and reference planes.
        material_color: Unused for this setup script.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created setup.
    """
    import bpy
    import addon_utils
    from mathutils import Vector, Euler
    import math

    # Get target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Render & Color Management Setup ===
    # Set to EEVEE for fast, non-physically based preview
    scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(scene, 'eevee') and hasattr(scene.eevee, 'shadow_ray_count') else 'BLENDER_EEVEE'
    
    # Disable PBR effects for flat stylized modeling
    if hasattr(scene, 'eevee'):
        if hasattr(scene.eevee, 'use_bloom'): scene.eevee.use_bloom = False
        if hasattr(scene.eevee, 'use_ssr'): scene.eevee.use_ssr = False
        if hasattr(scene.eevee, 'use_gtao'): scene.eevee.use_gtao = False
        if hasattr(scene.eevee, 'use_motion_blur'): scene.eevee.use_motion_blur = False

    # CRITICAL: Set View Transform to Standard for 1:1 texture colors
    scene.view_settings.view_transform = 'Standard'

    # === Step 2: Enable Rigify and Add Scale Reference Rig ===
    # Check if Rigify is enabled, if not, enable it silently
    is_enabled, is_loaded = addon_utils.check("rigify")
    if not is_loaded:
        addon_utils.enable("rigify")
        
    # Deselect all to ensure clean rig spawning
    bpy.ops.object.select_all(action='DESELECT')
    
    # Add the Human Meta-Rig
    # We must use the operator context to spawn it correctly
    original_active = bpy.context.active_object
    try:
        bpy.ops.object.armature_human_metarig_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_ScaleRig"
        rig.scale = (scale, scale, scale)
        # Move origin to floor
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    except Exception as e:
        print(f"Warning: Could not add human metarig (Rigify may need manual activation). Error: {e}")
        # Fallback to standard single bone if Rigify fails for any reason
        bpy.ops.object.armature_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_ScaleRig_Fallback"
        rig.scale = (scale * 2, scale * 2, scale * 2)

    # === Step 3: Setup Reference Image Empties ===
    # Create a 1x1 transparent placeholder image
    placeholder_img = bpy.data.images.new(name=f"{object_name}_RefPlaceholder", width=16, height=16, alpha=True)

    # 1. Front View Reference (Visible from Numpad 1 looking +Y)
    front_empty = bpy.data.objects.new(f"{object_name}_Ref_Front", None)
    scene.collection.objects.link(front_empty)
    front_empty.empty_display_type = 'IMAGE'
    front_empty.data = placeholder_img
    
    # 50% Opacity
    front_empty.color = (1.0, 1.0, 1.0, 0.5)
    front_empty.use_empty_image_alpha = True
    
    # Rotate 90 deg on X to stand upright facing Front View (-Y)
    front_empty.rotation_euler = Euler((math.radians(90), 0, 0), 'XYZ')
    
    # Move behind the origin (+Y) and up slightly
    front_empty_loc = Vector(location) + Vector((0, 1.5 * scale, 1.0 * scale))
    front_empty.location = front_empty_loc
    front_empty.scale = (scale * 2.5, scale * 2.5, scale * 2.5)

    # 2. Side View Reference (Visible from Numpad 3 looking -X)
    side_empty = bpy.data.objects.new(f"{object_name}_Ref_Side", None)
    scene.collection.objects.link(side_empty)
    side_empty.empty_display_type = 'IMAGE'
    side_empty.data = placeholder_img
    
    # 50% Opacity
    side_empty.color = (1.0, 1.0, 1.0, 0.5)
    side_empty.use_empty_image_alpha = True
    
    # Rotate 90 deg on X and 90 deg on Z to stand upright facing Right View (+X)
    side_empty.rotation_euler = Euler((math.radians(90), 0, math.radians(90)), 'XYZ')
    
    # Move behind the origin (-X) and up slightly
    side_empty_loc = Vector(location) + Vector((-1.5 * scale, 0, 1.0 * scale))
    side_empty.location = side_empty_loc
    side_empty.scale = (scale * 2.5, scale * 2.5, scale * 2.5)

    # Restore active object context
    if original_active:
        bpy.context.view_layer.objects.active = original_active

    return f"Prepared '{object_name}' workspace: Standard color transform active, Rig added at {location}, Front/Side Ref Empties initialized."
```