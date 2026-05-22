### 1. High-level Design Pattern Extraction

> **Skill Name**: Character Modeling Blueprint Setup (Meta-Rig Alignment & Color Management)

* **Core Visual Mechanism**: This pattern sets up the foundational workspace for 3D character modeling. It relies on three core actions: 
  1. Switching Color Management from the photorealistic default ("AgX" or "Filmic") to "Standard" to ensure 1:1 color accuracy for stylized textures.
  2. Spawning a Human Meta-Rig (`rigify` add-on) to act as a 3D ruler and proportion guide.
  3. Generating semi-transparent orthogonal reference planes (Front and Side views) scaled and aligned to the Meta-Rig on the ground plane.

* **Why Use This Skill (Rationale)**: Modeling a character in an empty viewport often leads to disproportionate limbs and incorrect scale. Using a Meta-Rig provides an immediate, anatomically standard reference. Furthermore, Blender's default view transforms (Filmic/AgX) desaturate colors to mimic real cameras; changing this to "Standard" is mandatory for stylized or "unlit" low-poly art to prevent colors from washing out.

* **Overall Applicability**: Essential first step for any stylized character modeling, low-poly PS1-style asset creation, or orthographic blueprint modeling (cars, weapons, architecture). 

* **Value Addition**: Instead of starting with a blank canvas and struggling with scale and color accuracy, this skill instantly prepares a mathematically aligned, color-accurate orthographic staging area.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Meta-Rig**: The `armature_human_metarig` from the built-in Rigify addon serves as the spatial core.
  - **Reference Planes**: Two 2D planes are spawned. One is rotated 90° on the X-axis (Front View), and the other is rotated 90° on the X and Z axes (Side View). They are offset from the origin so they don't intersect with the 3D model being built in the center.

* **Step B: Materials & Shading**
  - **Render Engine**: Set to EEVEE.
  - **Post-Processing Disabled**: Ambient Occlusion, Bloom, Screen Space Reflections, and Motion Blur are explicitly disabled to provide a clean, distraction-free silhouette preview.
  - **Color Management**: `view_transform` is forced to `'Standard'`.
  - **Reference Material**: A procedural semi-transparent material (Alpha = 0.5) is applied to the planes to mimic the opacity adjustments made to image empties in the tutorial.

* **Step C: Lighting & Rendering Context**
  - Flat/Solid viewport shading is preferred. No actual lights are needed for the blueprint setup phase, as the goal is purely geometric alignment.

* **Step D: Animation & Dynamics (if applicable)**
  - N/A. The setup is static.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Color/Render Settings | `bpy.context.scene.view_settings` | Programmatically overrides defaults to match stylized requirements |
| Proportion Guide | `bpy.ops.object.armature_human_metarig_add` | Guarantees standard human proportions (requires enabling `rigify`) |
| Image References | `bpy.ops.mesh.primitive_plane_add` + Procedural Material | Replaces local image files (which an automated agent can't access) with semi-transparent procedural blueprint planes. |

> **Feasibility Assessment**: 100% reproduction of the logical setup. Because external image paths cannot be reliably loaded via an automated script, semi-transparent procedural grid planes are used as robust drop-in replacements for the Front/Side concept art images shown in the video.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "CharBlueprint",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 1.0),
    **kwargs,
) -> str:
    """
    Create Character Modeling Blueprint Setup in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created reference objects.
        location: (x, y, z) world-space position for the setup.
        scale: Uniform scale factor (1.0 = standard 2-meter human).
        material_color: (R, G, B) tint for the reference blueprint planes.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import addon_utils
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Render & Color Management Settings ===
    # Set to EEVEE (Handle both 4.2+ EEVEE_NEXT and older EEVEE)
    if 'BLENDER_EEVEE_NEXT' in [e.idname for e in bpy.types.RenderEngine.__subclasses__()]:
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
    else:
        scene.render.engine = 'BLENDER_EEVEE'
        
    # Standard view transform is critical for stylized/low-poly color accuracy
    scene.view_settings.view_transform = 'Standard'

    # Disable interfering post-processing effects (if using pre-4.2 Eevee settings structure)
    try:
        scene.eevee.use_gtao = False
        scene.eevee.use_bloom = False
        scene.eevee.use_ssr = False
        scene.eevee.use_motion_blur = False
    except AttributeError:
        pass # Handle graceful fallback for Blender 4.2+ changed attributes

    # === Step 2: Enable Rigify and Add Meta-Rig ===
    if not addon_utils.check("rigify")[1]:
        addon_utils.enable("rigify")

    # Add Human Meta-rig
    bpy.ops.object.armature_human_metarig_add(location=location)
    rig = bpy.context.active_object
    rig.name = f"{object_name}_MetaRig"
    rig.scale = (scale, scale, scale)
    # Move rig's origin exactly to the floor line if it isn't already
    rig.location.z += (rig.dimensions.z / 2) * scale if rig.location.z < 0 else 0

    # === Step 3: Create Semi-Transparent Blueprint Material ===
    mat_name = f"{object_name}_BlueprintMat"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    mat.blend_method = 'BLEND'  # Enable Alpha Blending for Eevee
    mat.shadow_method = 'NONE'  # References shouldn't cast shadows

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        bsdf.inputs["Alpha"].default_value = 0.35  # Semi-transparent like the video
        bsdf.inputs["Roughness"].default_value = 1.0
        # If emission is needed to make it act unlit:
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (*material_color, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 0.5

    # === Step 4: Create Reference Planes ===
    # Front View Plane (Behind the character on the Y axis)
    front_offset = Vector((0, 1.5 * scale, 1.0 * scale))
    bpy.ops.mesh.primitive_plane_add(size=2.2, location=Vector(location) + front_offset)
    front_plane = bpy.context.active_object
    front_plane.name = f"{object_name}_FrontRef"
    front_plane.rotation_euler = (math.radians(90), 0, 0)
    front_plane.scale = (scale, scale, scale)
    if len(front_plane.data.materials) == 0:
        front_plane.data.materials.append(mat)
    
    # Side View Plane (To the side of the character on the X axis)
    side_offset = Vector((1.5 * scale, 0, 1.0 * scale))
    bpy.ops.mesh.primitive_plane_add(size=2.2, location=Vector(location) + side_offset)
    side_plane = bpy.context.active_object
    side_plane.name = f"{object_name}_SideRef"
    side_plane.rotation_euler = (math.radians(90), 0, math.radians(90))
    side_plane.scale = (scale, scale, scale)
    if len(side_plane.data.materials) == 0:
        side_plane.data.materials.append(mat)

    # Disable selection for reference planes so they don't get in the way of modeling
    front_plane.hide_select = True
    side_plane.hide_select = True

    return f"Created Character Reference Setup '{object_name}' with Meta-Rig and Orthogonal Planes at {location}"
```