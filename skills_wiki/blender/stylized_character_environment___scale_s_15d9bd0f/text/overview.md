### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized Character Environment & Scale Setup

* **Core Visual Mechanism**: This pattern sets up a standardized environment for stylized (non-photorealistic) character modeling. It overrides Blender's default photorealistic color mapping (AgX/Filmic) to "Standard" to ensure 1:1 color accuracy, disables realistic Eevee post-processing effects, and establishes a real-world scale reference using a Rigify armature and spatially aligned reference image planes.
* **Why Use This Skill (Rationale)**: 
  1. **Color Accuracy**: Default view transforms (like AgX) desaturate colors and compress contrast to mimic real-world cameras. For stylized low-poly art (where colors are painted flat), this makes textures look washed out. "Standard" view transform maps RGB values directly to the screen.
  2. **Scale**: Modeling without a scale reference often results in characters that are 20 meters or 2 centimeters tall, which breaks lighting, camera clipping, and physics down the line. A default human meta-rig provides a reliable ~1.8m height guide.
* **Overall Applicability**: The absolute required first step for any stylized game asset, anime character, or low-poly prop workflow before adding a single polygon.
* **Value Addition**: Transforms a default, photorealistic-leaning empty scene into a tailored orthographic workspace optimized for exact color picking and proportional modeling.

### 2. Technical Breakdown

* **Step A: Environment & Color Management**
  - **Render Engine**: EEVEE (preferred for real-time stylized looks).
  - **Color Management**: View Transform changed from `AgX` (or `Filmic`) to `Standard`.
  - **Post-processing**: Ambient Occlusion, Bloom, Screen Space Reflections, and Motion Blur are explicitly disabled to prevent unwanted shadows/glows from interfering with flat shading perception.
* **Step B: Scale Reference (Geometry)**
  - Enables the built-in `rigging_rigify` add-on.
  - Spawns an `armature_human_metarig` to act as an un-renderable wireframe scale guide.
* **Step C: Reference Planes**
  - Uses `Empty` objects with the display type set to `IMAGE`.
  - Front reference is pushed back on the Y-axis.
  - Side reference is rotated 90 degrees on the Z-axis and pushed back on the X-axis.
  - Alpha transparency is set to 50% (`0.5`) so the 3D model can be seen through the reference images.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Scene Settings | `bpy.context.scene` properties | Directly configures global render and color logic. |
| Scale Reference | `rigging_rigify` + Armature ops | Provides an instant, anatomically proportioned measuring stick. |
| Reference Images | `Empty` objects (Image type) | Standard Blender workflow for orthographic modeling references; doesn't clutter the render or require UV mapping. |

> **Feasibility Assessment**: 100% reproduction of the video's foundational setup. Because the script cannot reliably download external images from the internet, it procedurally generates tinted blank image data blocks for the Empties. The user can simply swap these data blocks with their own character art.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "CharacterSetup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.8),
    **kwargs,
) -> str:
    """
    Create a Stylized Character Environment & Scale Setup in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created reference setup.
        location: (x, y, z) world-space position for the center of the setup.
        scale: Uniform scale factor (1.0 = ~2 meter tall character reference).
        material_color: (R, G, B) tint color for the generated placeholder reference images.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created setup.
    """
    import bpy
    import addon_utils
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Configure Environment for Stylized Rendering ===
    scene.render.engine = 'BLENDER_EEVEE'
    scene.view_settings.view_transform = 'Standard'

    # Disable realistic post-processing in EEVEE (checks attributes for cross-version compatibility)
    if hasattr(scene, "eevee"):
        if hasattr(scene.eevee, "use_gtao"):
            scene.eevee.use_gtao = False
        if hasattr(scene.eevee, "use_bloom"):
            scene.eevee.use_bloom = False
        if hasattr(scene.eevee, "use_ssr"):
            scene.eevee.use_ssr = False
        if hasattr(scene.eevee, "use_motion_blur"):
            scene.eevee.use_motion_blur = False

    created_items = []

    # === Step 2: Enable Rigify & Add Human Meta-Rig ===
    try:
        addon_utils.enable("rigging_rigify", default_set=True)
        
        # Add the meta-rig using the operator
        bpy.ops.object.armature_human_metarig_add(location=location)
        metarig = bpy.context.active_object
        metarig.name = f"{object_name}_Scale_Metarig"
        metarig.scale = (scale, scale, scale)
        metarig.display_type = 'WIRE'
        
        created_items.append(metarig.name)
    except Exception as e:
        print(f"Note: Could not add Rigify metarig. Error: {e}")

    # === Step 3: Create Synthetic Reference Images ===
    # We generate semi-transparent blank images as placeholders.
    # Users can later replace the file paths of these images with real character art.
    img_width, img_height = 512, 1024
    front_img = bpy.data.images.new(name=f"{object_name}_Front_Art", width=img_width, height=img_height, alpha=True)
    side_img = bpy.data.images.new(name=f"{object_name}_Side_Art", width=img_width, height=img_height, alpha=True)
    
    # Fill image pixels with a flat color
    rgba = list(material_color) + [0.3] # Base color + low alpha
    pixels = rgba * (img_width * img_height)
    front_img.pixels = pixels
    side_img.pixels = pixels

    # === Step 4: Setup Front Reference Empty ===
    front_empty = bpy.data.objects.new(f"{object_name}_Ref_Front", None)
    front_empty.empty_display_type = 'IMAGE'
    front_empty.data = front_img
    # Push back on Y axis, lift on Z axis
    front_empty.location = Vector(location) + Vector((0, 1.5 * scale, 1.0 * scale))
    front_empty.rotation_euler = (math.radians(90), 0, 0)
    front_empty.empty_display_size = 2.0 * scale
    front_empty.use_empty_image_alpha = True
    front_empty.empty_image_alpha = 0.5
    
    scene.collection.objects.link(front_empty)
    created_items.append(front_empty.name)

    # === Step 5: Setup Side Reference Empty ===
    side_empty = bpy.data.objects.new(f"{object_name}_Ref_Side", None)
    side_empty.empty_display_type = 'IMAGE'
    side_empty.data = side_img
    # Push back on X axis, lift on Z axis, rotate to face X
    side_empty.location = Vector(location) + Vector((-1.5 * scale, 0, 1.0 * scale))
    side_empty.rotation_euler = (math.radians(90), 0, math.radians(-90))
    side_empty.empty_display_size = 2.0 * scale
    side_empty.use_empty_image_alpha = True
    side_empty.empty_image_alpha = 0.5
    
    scene.collection.objects.link(side_empty)
    created_items.append(side_empty.name)

    return f"Created Stylized Scene Environment '{object_name}' with elements: {', '.join(created_items)}"
```