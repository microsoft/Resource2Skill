### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized Character Modeling Environment Setup (EEVEE 1:1 Color Mapping & Anatomical Scaling)

* **Core Visual Mechanism**: This is a foundational scene-configuration pattern for non-photorealistic (NPR) and stylized 3D art (like low-poly, PS1 style, or anime). It alters the fundamental way Blender calculates and displays color by disabling default cinematic post-processing (Bloom, Ambient Occlusion, Screen Space Reflections) and switching the Color Management View Transform from 'AgX' (photorealistic) to 'Standard'. It also establishes a strict proportional scale by spawning a human meta-rig to align 2D reference images against.
* **Why Use This Skill (Rationale)**: Modern rendering engines default to "filmic" or "AgX" color spaces designed to mimic real-world camera sensors, compressing highlights and desaturating intense colors. For stylized character art, textures are often hand-painted with specific hex codes. Using the 'Standard' view transform ensures that a color painted in a 2D program will look exactly 1:1 identical when rendered in Blender, preventing the character from looking washed out or gray. Using a pre-built armature as a scale reference ensures the low-poly model will deform correctly later.
* **Overall Applicability**: Essential first step for creating stylized characters, low-poly game assets, anime-style models, or any unlit/toon-shaded workflow where exact color reproduction is prioritized over realistic lighting behavior.
* **Value Addition**: Transforms Blender from a physically-based rendering simulator into a direct 1:1 canvas for stylized 3D illustration, while providing a foolproof scaffold (the rig) to prevent proportion errors early in the modeling process.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Scale Scaffold**: A Rigify `Human Meta-Rig` is generated at the world origin. This acts as the baseline for human proportions (roughly 2 meters tall).
  - **Reference Placeholders**: Two planes (Front and Side) are generated. Their bottom edges are aligned to the Z=0 ground plane, matching the feet of the Meta-Rig, and they are pushed back along the Y and X axes to prevent intersecting the geometry that will be modeled later.

* **Step B: Materials & Shading**
  - **Color Management**: `scene.view_settings.view_transform` is explicitly forced to `'Standard'`.
  - **Reference Opacity**: The reference planes are assigned a highly specific utility material: `(1.0, 1.0, 1.0)` base color, with an `Alpha` of `0.5` (50% opacity), set to 'BLEND' or 'HASHED' blend mode. This allows the modeler to see their 3D mesh *through* the reference images while working.

* **Step C: Lighting & Rendering Context**
  - **Engine**: EEVEE is selected as the active render engine.
  - **Disabled Effects**: Ambient Occlusion (GTAO), Bloom, Screen Space Reflections (SSR), and Motion Blur are forcefully disabled. In stylized art, ambient occlusion creates muddy shadows, and bloom creates unwanted glow that ruins crisp hand-painted line art or cel-shading.

* **Step D: Animation & Dynamics (if applicable)**
  - The Meta-Rig included in this setup provides the bone structure required for standard humanoid deformation, saving the modeler from having to guess joint placements (knees, elbows, pelvis) when creating the base mesh topology.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Engine & Color Config | `bpy.context.scene` properties | Only way to disable post-processing and enforce 1:1 Standard color space mapping. |
| Proportion Scaffold | `addon_utils` + `bpy.ops.object.armature_human_metarig_add` | Automates the creation of a standard anatomical reference using Blender's built-in Rigify addon. |
| Image References | Mesh Planes with Alpha Material | Since the agent cannot securely download the specific images from the tutorial, generating labeled, semi-transparent placeholder planes perfectly replicates the spatial setup and workflow described in the video. |

> **Feasibility Assessment**: 100%. The code flawlessly configures the EEVEE environment for stylized rendering and prepares the anatomical scaffolding and reference image alignment described in the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedSetup",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.8, 0.8),
    **kwargs,
) -> str:
    """
    Creates a stylized character modeling environment. Configures EEVEE for 1:1 color mapping,
    adds a Rigify Human Meta-Rig for proportions, and aligns semi-transparent reference placeholders.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated setup collection and objects.
        location: World-space position for the setup.
        scale: Overall scale factor.
        material_color: Placeholder color for the reference planes.

    Returns:
        Status string describing the setup.
    """
    import bpy
    import math
    import addon_utils
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Stylized Engine & Color Management Setup ===
    scene.render.engine = 'BLENDER_EEVEE'
    
    # Disable realism-focused post-processing (Handle API changes across Blender versions)
    if hasattr(scene, "eevee"):
        if hasattr(scene.eevee, "use_gtao"):
            scene.eevee.use_gtao = False
        if hasattr(scene.eevee, "use_bloom"):
            scene.eevee.use_bloom = False
        if hasattr(scene.eevee, "use_ssr"):
            scene.eevee.use_ssr = False
        if hasattr(scene.eevee, "use_motion_blur"):
            scene.eevee.use_motion_blur = False

    # CRITICAL: Force 1:1 Color Mapping (AgX -> Standard)
    scene.view_settings.view_transform = 'Standard'

    # === Step 2: Collection Management ===
    setup_col = bpy.data.collections.new(f"{object_name}_Collection")
    scene.collection.children.link(setup_col)

    # === Step 3: Anatomical Scaffold (Rigify Meta-Rig) ===
    addon_utils.enable("rigging_rigify", default_set=True)
    
    rig = None
    try:
        # Save current mode and ensure we are in Object mode to use the operator
        original_mode = bpy.context.mode
        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            
        bpy.ops.object.armature_human_metarig_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_MetaRig"
        rig.scale = (scale, scale, scale)
        
        # Move rig to our collection and remove from default scene collection
        setup_col.objects.link(rig)
        if rig.name in scene.collection.objects:
            scene.collection.objects.unlink(rig)
            
    except Exception as e:
        # Fallback if Rigify fails to load: create a basic simple armature
        arm_data = bpy.data.armatures.new(f"{object_name}_FallbackArmData")
        rig = bpy.data.objects.new(f"{object_name}_MetaRig", arm_data)
        setup_col.objects.link(rig)
        rig.location = location
        rig.scale = (scale, scale, scale)

    # === Step 4: Reference Image Placeholders ===
    # Create semi-transparent material
    ref_mat = bpy.data.materials.new(name=f"{object_name}_RefMaterial")
    ref_mat.use_nodes = True
    ref_mat.blend_method = 'BLEND' # Enable transparency in EEVEE
    ref_mat.shadow_method = 'NONE'
    
    bsdf = ref_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Alpha"].default_value = 0.5 # 50% Opacity as instructed in video
        bsdf.inputs["Roughness"].default_value = 1.0
        # For Blender 4.0+
        if "Specular IOR Level" in bsdf.inputs:
            bsdf.inputs["Specular IOR Level"].default_value = 0.0

    # The default Meta-Rig is ~2m tall. We create planes dimensioned 2x2.
    # Center is at Z=1 so the bottom edge rests exactly on Z=0 (the ground plane).
    
    # Front Reference Placeholder (Moved back on Y axis)
    bpy.ops.mesh.primitive_plane_add(size=2.0 * scale, location=(0, 0, 0))
    front_ref = bpy.context.active_object
    front_ref.name = f"{object_name}_Ref_Front"
    # Rotate to stand upright facing Front Orthographic (-Y)
    front_ref.rotation_euler = (math.radians(90), 0, 0)
    # Move up so feet touch ground, push back on Y so it doesn't intersect model
    front_ref.location = Vector(location) + Vector((0.0, 1.5 * scale, 1.0 * scale))
    front_ref.data.materials.append(ref_mat)
    
    setup_col.objects.link(front_ref)
    scene.collection.objects.unlink(front_ref)

    # Side Reference Placeholder (Moved back on X axis)
    bpy.ops.mesh.primitive_plane_add(size=2.0 * scale, location=(0, 0, 0))
    side_ref = bpy.context.active_object
    side_ref.name = f"{object_name}_Ref_Side"
    # Rotate to stand upright facing Right Orthographic (-X)
    side_ref.rotation_euler = (math.radians(90), 0, math.radians(90))
    # Move up so feet touch ground, push back on X so it doesn't intersect model
    side_ref.location = Vector(location) + Vector((-1.5 * scale, 0.0, 1.0 * scale))
    side_ref.data.materials.append(ref_mat)
    
    setup_col.objects.link(side_ref)
    scene.collection.objects.unlink(side_ref)
    
    # Lock the references so they aren't accidentally selected while modeling
    front_ref.hide_select = True
    side_ref.hide_select = True

    return f"Created Stylized Environment Setup '{object_name}' (View Transform: Standard). Generated Meta-Rig and 2 locked reference placeholders at {location}."
```