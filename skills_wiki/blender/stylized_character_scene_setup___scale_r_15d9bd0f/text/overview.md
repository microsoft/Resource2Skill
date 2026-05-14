### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized Character Scene Setup & Scale Reference

* **Core Visual Mechanism**: The defining mechanism of this setup is the deliberate shift away from photorealistic tone mapping. By setting the Blender View Transform to 'Standard' instead of 'AgX' or 'Filmic', colors are mapped 1:1 to the screen. This is combined with spawning a "Human Meta-Rig" to serve as an immediate real-world scale reference, ensuring the imported 2D blueprint references are sized correctly.
* **Why Use This Skill (Rationale)**: When modeling stylized, low-poly, or anime-style characters, artists often hand-paint textures or rely on flat base colors. High Dynamic Range transforms (like AgX) will mathematically desaturate and compress these colors to mimic physical cameras, making flat colors look washed out. The 'Standard' transform prevents this. Furthermore, starting a model without a scale reference often leads to characters that are either microscopic or 100 meters tall in Blender units, which breaks physics simulations and lighting calculations later on. 
* **Overall Applicability**: This is the mandatory foundational setup for any non-photorealistic (NPR) workflow, low-poly game asset creation, or stylized character modeling project. 
* **Value Addition**: Instead of starting with an empty scene and a default cube, this skill instantly configures the rendering environment for accurate color reproduction, provides a skeletal human scale reference, and provisions correctly oriented, semi-transparent placeholder planes for front and side orthographic blueprints.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Root**: An Empty object is used as a container to hold the setup.
  - **Scale Reference**: A Rigify `Human Meta-Rig` (Armature) is spawned at the center. It has standard human proportions and bone structure.
  - **References**: Two basic primitive planes are spawned. One is rotated `90°` on the X-axis (Front View) and the other is rotated `90°` on both X and Z (Side View). 
* **Step B: Materials & Shading**
  - The scene's Color Management `View Transform` is forced to `Standard`.
  - The blueprint planes use a Principled BSDF with `Alpha` set to `0.4` and the material's Blend Method set to `BLEND` (allowing EEVEE transparency). Roughness is set to `1.0` and Specular to `0.0` to prevent glare from obscuring the reference drawings.
* **Step C: Lighting & Rendering Context**
  - **Render Engine**: EEVEE is selected, as real-time rasterized rendering is preferred for stylized asset creation where physical light bouncing (Cycles) is not the focus.
* **Step D: Animation & Dynamics**
  - The Rigify Meta-rig is static but is natively prepared to be generated into a full IK/FK animation rig once the character modeling is complete.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Color Accuracy | `bpy.context.scene.view_settings` | Programmatically forces the View Transform to 'Standard', which is the core thesis of the video's shading logic. |
| Scale Reference | `addon_utils` + `armature_human_metarig_add` | Automates the enabling of Blender's built-in Rigify addon to spawn a structurally accurate human proportion guide. |
| Blueprint Setup | `bpy.ops.mesh.primitive_plane_add` + Nodes | Creates transparent, non-reflective billboard planes perfectly aligned to orthographic axes for drawing projection. |

> **Feasibility Assessment**: 100% of the foundational setup shown in the video is reproduced. While the code creates placeholder planes instead of importing the creator's specific 2D drawings (which require external image files), the functional 3D infrastructure is identical.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedCharacterSetup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 0.8), # Blueprint placeholder tint
    **kwargs,
) -> str:
    """
    Create a Stylized Character Modeling Setup in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the root container object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the rig and references.
        material_color: (R, G, B) tint for the placeholder reference planes.

    Returns:
        Status string describing the created setup.
    """
    import bpy
    import math
    import addon_utils
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Stylized Render & Color Management Setup ===
    # For stylized/anime models, 'Standard' view transform is absolutely required 
    # to prevent colors from washing out (unlike AgX/Filmic which are for photorealism).
    scene.render.engine = 'BLENDER_EEVEE'
    scene.display_settings.display_device = 'sRGB'
    scene.view_settings.view_transform = 'Standard'

    # Ensure we are in object mode before adding items
    if bpy.context.active_object and bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # === Step 2: Create Root Container ===
    root = bpy.data.objects.new(object_name, None)
    scene.collection.objects.link(root)
    root.location = Vector(location)
    root.scale = (scale, scale, scale)

    # === Step 3: Add Scale Reference Rig (Rigify) ===
    rig_added = False
    try:
        # Safely enable rigify addon if not already enabled
        if not addon_utils.check("rigify")[0]:
            addon_utils.enable("rigify", default_set=True)
            
        bpy.ops.object.armature_human_metarig_add(location=(0, 0, 0))
        rig = bpy.context.active_object
        rig_added = True
    except Exception:
        # Fallback if rigify fails/is missing
        bpy.ops.object.armature_add(location=(0, 0, 0))
        rig = bpy.context.active_object

    rig.name = f"{object_name}_ScaleRefRig"
    rig.display_type = 'WIRE'
    rig.show_in_front = True
    
    # Parent rig to root
    rig.parent = root
    rig.location = (0, 0, 0) # Zero out location relative to parent

    # === Step 4: Create Transparent Reference Planes ===
    # Material for blueprint references
    mat = bpy.data.materials.new(name=f"{object_name}_Ref_Mat")
    mat.use_nodes = True
    mat.blend_method = 'BLEND' # Enable transparency in EEVEE
    mat.shadow_method = 'NONE'
    
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Alpha'].default_value = 0.4 # Semi-transparent
        bsdf.inputs['Roughness'].default_value = 1.0 # Matte
        
        # Safely handle Specular inputs across different Blender versions (pre-4.0 and 4.0+)
        if 'Specular' in bsdf.inputs:
            bsdf.inputs['Specular'].default_value = 0.0
        elif 'Specular IOR Level' in bsdf.inputs:
            bsdf.inputs['Specular IOR Level'].default_value = 0.0

    # Add Front Reference Plane
    bpy.ops.mesh.primitive_plane_add(size=2)
    front_ref = bpy.context.active_object
    front_ref.name = f"{object_name}_Blueprint_Front"
    front_ref.rotation_euler = (math.radians(90), 0, 0)
    # Move back on Y so it doesn't block front modeling, scale to roughly human rig height
    front_ref.location = (0, 1.5, 1.0) 
    front_ref.scale = (1.5, 1.2, 1.5) 
    front_ref.data.materials.append(mat)
    front_ref.parent = root

    # Add Side Reference Plane
    bpy.ops.mesh.primitive_plane_add(size=2)
    side_ref = bpy.context.active_object
    side_ref.name = f"{object_name}_Blueprint_Side"
    side_ref.rotation_euler = (math.radians(90), 0, math.radians(90))
    # Move left on X so it doesn't block side modeling
    side_ref.location = (-1.5, 0, 1.0) 
    side_ref.scale = (1.5, 1.2, 1.5)
    side_ref.data.materials.append(mat)
    side_ref.parent = root

    # Clean up selection state
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created '{object_name}' setup at {location}. View Transform explicitly set to 'Standard'. Human Meta-Rig included: {rig_added}"
```