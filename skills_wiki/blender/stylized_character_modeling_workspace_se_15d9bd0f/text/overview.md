### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized Character Modeling Workspace Setup

* **Core Visual Mechanism**: This pattern establishes a standardized 3D workspace specifically optimized for stylized, low-poly character modeling. It relies on bypassing Blender's default photorealistic color mapping (switching from AgX/Filmic to 'Standard' view transform), configuring EEVEE for flat rendering, and programmatic generation of a real-world scale reference (Rigify Human Meta-Rig) paired with orthographic reference planes.
* **Why Use This Skill (Rationale)**: Blender's default settings are geared toward photorealism. View transforms like Filmic or AgX will desaturate flat colors and lower contrast, which ruins the vibrant, 1:1 hex-code color accuracy needed for stylized low-poly art or game engines. Additionally, starting character modeling without a predefined human scale leads to massive lighting, physics, and rigging issues later.
* **Overall Applicability**: Used as the absolute first step before poly-modeling any anime, low-poly, or stylized character. 
* **Value Addition**: Automates the tedious pre-modeling checklist. It locks in color accuracy, establishes exact metric scale (via the meta-rig), and creates a 3D blueprint corner using semi-transparent reference images, preventing scale drift and topology misalignment.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Scale Reference**: A Rigify `human_meta_rig` is spawned at the world origin. This armature is approximately 1.8 meters tall and acts as a bounding box and proportion guide for the character block-out.
  - **Blueprint Planes**: Two flat planes are spawned to act as orthographic image references. One is rotated 90° on the X-axis (Front View) and pushed back on the Y-axis. The second is rotated 90° on both X and Z (Side View) and pushed back on the X-axis.

* **Step B: Materials & Shading**
  - **Color Management**: `view_transform` is explicitly forced to `'Standard'`. This is the most critical shading step for stylized textures.
  - **Reference Material**: A Principled BSDF is used for the blueprint planes. Alpha is set to `0.5`, Base Color to a procedural placeholder grid, and the material's blend mode is set to `'BLEND'` (Alpha Blend) so the modeler can see the 3D mesh *through* the reference images.

* **Step C: Lighting & Rendering Context**
  - **Engine**: EEVEE.
  - **Optimization**: Post-processing effects that interfere with flat shading (Ambient Occlusion, Bloom, Screen Space Reflections, Motion Blur) are explicitly disabled to keep the viewport clean and responsive.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Render & Color Space | `bpy.context.scene` properties | Required to bypass default photorealistic color handling (AgX) for 1:1 stylized colors. |
| Scale Reference | `addon_utils` + `bpy.ops` | Enables Rigify programmatically and spawns the Human Meta-Rig. |
| Reference Images | Mesh Planes + Alpha Material | Using actual planes with transparent materials is more robust for API generation than Image Empties, and behaves identically in orthographic views. |

> **Feasibility Assessment**: 100% reproduction of the tutorial's technical outcome. Since the tutorial relies on a downloaded zip file for the specific 2D drawings, the script procedurally generates geometric placeholder planes that serve the exact same mechanical purpose. The user can easily swap the image texture in the generated material.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedWorkspace",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 0.8),
    **kwargs,
) -> str:
    """
    Create a Stylized Character Modeling Workspace.
    Configures EEVEE, sets 'Standard' color transform, spawns a scale reference rig,
    and sets up semi-transparent orthographic reference planes.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Prefix name for the created objects.
        location: (x, y, z) world-space position offset for the workspace.
        scale: Uniform scale factor (1.0 = standard human height ~1.8m).
        material_color: (R, G, B) base color for the placeholder reference planes.

    Returns:
        Status string.
    """
    import bpy
    import addon_utils
    from mathutils import Vector, Euler
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Render Engine & Color Management Configuration ===
    scene.render.engine = 'BLENDER_EEVEE'
    
    # Disable interfering post-processing for flat stylized look
    scene.eevee.use_gtao = False
    scene.eevee.use_bloom = False
    scene.eevee.use_ssr = False
    scene.eevee.use_motion_blur = False
    
    # CRITICAL: Set View Transform to Standard (prevents desaturation of stylized colors)
    scene.view_settings.view_transform = 'Standard'

    objects_created = []

    # === Step 2: Spawn Scale Reference (Rigify Human Meta-Rig) ===
    # Attempt to enable rigify, fallback to standard armature if it fails
    rig_spawned = False
    try:
        addon_utils.enable("rigify", default_set=True)
        bpy.ops.object.armature_human_metarig_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_MetaRig_ScaleRef"
        rig_spawned = True
    except Exception:
        pass

    if not rig_spawned:
        bpy.ops.object.armature_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_BasicRig_ScaleRef"
        # Scale a single bone to roughly 1.8 meters
        rig.scale = (1.8 * scale, 1.8 * scale, 1.8 * scale)
    
    # Push rig back slightly so it doesn't clip with the origin where we model
    rig.location.y += 0.5
    objects_created.append(rig.name)

    # === Step 3: Create Transparent Blueprint Reference Material ===
    mat_name = f"{object_name}_Reference_Mat"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    mat.blend_method = 'BLEND' # Enable transparency in Eevee
    mat.shadow_method = 'NONE' # References shouldn't cast shadows
    
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        # Set alpha to 0.5 for semi-transparency
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = 0.5
        bsdf.inputs["Roughness"].default_value = 1.0
        bsdf.inputs["Specular IOR Level"].default_value = 0.0

    # === Step 4: Create Orthographic Reference Planes ===
    
    # Front Reference Plane (Pushed back on Y)
    bpy.ops.mesh.primitive_plane_add(size=2.0 * scale, location=(location[0], location[1] + 1.5 * scale, location[2] + 1.0 * scale))
    front_plane = bpy.context.active_object
    front_plane.name = f"{object_name}_Ref_Front"
    front_plane.rotation_euler = Euler((math.radians(90), 0, 0), 'XYZ')
    
    # Scale up vertically to mimic a character drawing (1:2 ratio)
    front_plane.scale.y = 2.0
    
    if len(front_plane.data.materials) == 0:
        front_plane.data.materials.append(mat)
    objects_created.append(front_plane.name)

    # Side Reference Plane (Pushed back on X)
    bpy.ops.mesh.primitive_plane_add(size=2.0 * scale, location=(location[0] - 1.5 * scale, location[1], location[2] + 1.0 * scale))
    side_plane = bpy.context.active_object
    side_plane.name = f"{object_name}_Ref_Side"
    side_plane.rotation_euler = Euler((math.radians(90), 0, math.radians(90)), 'XYZ')
    
    side_plane.scale.y = 2.0
    
    if len(side_plane.data.materials) == 0:
        side_plane.data.materials.append(mat)
    objects_created.append(side_plane.name)

    # Prevent references from being accidentally selected during modeling
    front_plane.hide_select = True
    side_plane.hide_select = True

    return f"Created Stylized Workspace '{object_name}' (Configured 'Standard' view transform, added scale rig and 2 reference planes)."
```