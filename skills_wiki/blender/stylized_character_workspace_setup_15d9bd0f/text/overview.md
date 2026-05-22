### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized Character Workspace Setup

* **Core Visual Mechanism**: Configuring Blender's render environment specifically for stylized, non-photorealistic (NPR) modeling. This involves switching the view transform from AgX/Filmic to Standard, disabling default Eevee post-processing effects, and establishing a rigorous scaling and orthographic reference system using transparent planes and a meta-rig.
* **Why Use This Skill (Rationale)**: By default, Blender's color management (AgX/Filmic) is designed for photorealism—it compresses highlights and shifts hues to simulate real cameras. For stylized, "anime," or flat-shaded models, this washes out hand-painted colors. Switching to "Standard" ensures a 1-to-1 color mapping from 2D concepts to the 3D viewport. Additionally, establishing a human scale rig early prevents modeling characters that are completely out of proportion to real-world physics/lighting units.
* **Overall Applicability**: This is the mandatory first step for any 3D artist starting a low-poly, cel-shaded, or hand-painted character modeling project. 
* **Value Addition**: Compared to jumping straight into modeling from the default cube, this structured setup guarantees color fidelity across different software (e.g., Photoshop to Blender), ensures correct sizing for game engines, and provides physical boundaries (reference planes) to guide the modeling process.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Scale Reference**: A Human Meta-Rig (via the Rigify add-on) is spawned at the origin. This provides an immediate visual cue for human proportions (roughly 2 meters tall).
  - **Reference Boards**: Two 2D planes are spawned to act as stand-ins for Front and Side orthographic image references. They are scaled to match the rig and offset along the Y and X axes to avoid intersecting with the modeling space at the origin.

* **Step B: Materials & Shading**
  - The reference planes use a custom semi-transparent material.
  - **Shader Model**: Principled BSDF with Alpha blending.
  - **Opacity**: Set to exactly `0.5` (50%), mimicking the opacity settings of an Image Empty. This allows the modeler to see their geometry *through* the reference images.
  - Emission is slightly raised to ensure the reference planes are visible regardless of scene lighting (mimicking unlit image planes).

* **Step C: Lighting & Rendering Context**
  - **Render Engine**: EEVEE. Cycles is explicitly avoided as raytracing is unnecessary for this specific low-poly style.
  - **Color Management**: View Transform is forced to `Standard`.
  - **Post-Processing**: Ambient Occlusion, Bloom, Screen Space Reflections, and Motion Blur are disabled to provide a clean, unbiased viewport for precision modeling.

* **Step D: Animation & Dynamics (if applicable)**
  - N/A for the setup phase, though enabling Rigify prepares the scene for future skeletal animation.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Render & Color Accuracy | `scene.view_settings.view_transform` | Overrides photorealistic defaults (AgX) to ensure 2D stylized colors map exactly 1-to-1 in the viewport. |
| Proportion & Scale | `bpy.ops.object.armature_human_metarig_add` | Uses Rigify to drop in an industry-standard human proportion guide instantly. |
| Reference Alignment | `bpy.ops.mesh.primitive_plane_add` + Materials | Creates physical boundaries aligned to orthographic views. Uses alpha-blended materials to replicate the tutorial's 50% image opacity. |

> **Feasibility Assessment**: 100% reproduction of the workspace setup logic. Since local image paths from the user's computer cannot be hardcoded, semi-transparent colored planes are generated as robust placeholders for the Front and Side concept art.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "Stylized_Workspace",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.5),
    **kwargs,
) -> str:
    """
    Create a Stylized Character Workspace Setup in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created workspace rig.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = approx 2m character height).
        material_color: (R, G, B) placeholder color for reference planes.
        **kwargs: Additional overrides.

    Returns:
        Status string detailing the setup.
    """
    import bpy
    import math
    import addon_utils
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Configure Render & Color Management for Stylized Art ===
    scene.render.engine = 'BLENDER_EEVEE'
    
    # Force Standard view transform (crucial for flat/stylized color accuracy)
    if hasattr(scene, 'view_settings'):
        scene.view_settings.view_transform = 'Standard'
        
    # Disable post-processing for a clean viewport
    if hasattr(scene, 'eevee'):
        scene.eevee.use_gtao = False
        scene.eevee.use_bloom = False
        scene.eevee.use_ssr = False
        scene.eevee.use_motion_blur = False

    # Create root object to keep the outliner clean
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    setup_root = bpy.context.active_object
    setup_root.name = object_name
    setup_root.scale = (scale, scale, scale)

    # === Step 2: Add Scale Reference Rig ===
    addon_utils.enable("rigify")
    try:
        # Attempt to add Rigify Meta-rig
        bpy.ops.object.armature_human_metarig_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_ScaleReference"
    except Exception:
        # Fallback to basic armature if Rigify is unavailable
        bpy.ops.object.armature_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_ScaleReference"
        rig.scale = (1, 1, 1)
        
    rig.parent = setup_root

    # === Step 3: Create Semi-Transparent Reference Planes ===
    # Setup material to mimic image opacity behavior (50% transparent, slightly emissive)
    mat = bpy.data.materials.new(name=f"{object_name}_ReferenceMat")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'  # Enable transparency in Eevee
    
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Alpha'].default_value = 0.5  # 50% opacity
        
        # Connect emission for unlit visibility
        if 'Emission' in bsdf.inputs:
            # Handle Blender 4.0+ Principled BSDF
            if hasattr(bsdf.inputs['Emission'], "default_value") and type(bsdf.inputs['Emission'].default_value) == float:
                # Old API
                pass
            else:
                bsdf.inputs['Emission Color'].default_value = (*material_color, 1.0)
                if 'Emission Strength' in bsdf.inputs:
                    bsdf.inputs['Emission Strength'].default_value = 0.2
        elif 'Emission' in bsdf.inputs: # Older blender fallback
             bsdf.inputs['Emission'].default_value = (*material_color, 1.0)

    # Add Front Reference Plane (placed behind character on +Y)
    bpy.ops.mesh.primitive_plane_add(size=2, location=(location[0], location[1] + 1.5, location[2] + 1))
    front_ref = bpy.context.active_object
    front_ref.name = f"{object_name}_FrontView"
    front_ref.rotation_euler = (math.pi / 2, 0, 0)
    front_ref.data.materials.append(mat)
    front_ref.parent = setup_root
    
    # Add Side Reference Plane (placed to the left on -X)
    bpy.ops.mesh.primitive_plane_add(size=2, location=(location[0] - 1.5, location[1], location[2] + 1))
    side_ref = bpy.context.active_object
    side_ref.name = f"{object_name}_SideView"
    side_ref.rotation_euler = (math.pi / 2, 0, math.pi / 2)
    side_ref.data.materials.append(mat)
    side_ref.parent = setup_root

    # Deselect all to finish cleanly
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created Stylized Workspace '{object_name}' at {location} with scale rig, front/side reference boards, and 'Standard' color transform applied."
```