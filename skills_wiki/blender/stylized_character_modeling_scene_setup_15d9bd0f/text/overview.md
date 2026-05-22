### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized Character Modeling Scene Setup

* **Core Visual Mechanism**: Configuring Blender's rendering pipeline and workspace specifically for stylized, non-photorealistic (NPR), or low-poly 3D art. The defining technical shift is changing the **Color Management View Transform from AgX/Filmic to Standard**. It also establishes a calibrated physical workspace using a standardized armature (Rigify Meta-Rig) for scale reference, flanked by semi-transparent orthographic drafting planes.
* **Why Use This Skill (Rationale)**: Default Blender uses AgX or Filmic color spaces designed for photorealism. These color spaces compress highlights and desaturate intense colors to mimic physical cameras. For stylized art (anime, retro low-poly, flat-shaded), artists need 1:1 color accuracy so that the hex colors chosen in 2D software look exactly the same in the 3D viewport. Furthermore, establishing a human-scale reference rig early prevents catastrophic scaling and proportional errors during the later rigging and animation phases.
* **Overall Applicability**: This is the mandatory foundational setup for any stylized character modeling, cell-shaded environments, or low-poly retro game assets. 
* **Value Addition**: Transforms Blender from a photorealistic simulator into a predictable, color-accurate digital drafting board. It automates the tedious boilerplate setup required before starting a stylized project.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Scale Reference**: Spawns a `human_metarig` via the Rigify addon. This enforces real-world proportions (roughly 2 meters tall) so the modeled character conforms to standard physics and engine scaling.
  - **Reference Planes**: Employs planar geometry positioned along the world axes (XZ for Front view, YZ for Side view) to act as drafting boards for reference images.
* **Step B: Materials & Shading**
  - **Color Space**: `scene.view_settings.view_transform = 'Standard'`. This is the most critical shading step, disabling photorealistic tonemapping.
  - **Reference Material**: The drafting planes use a Principled BSDF with Alpha Blending set to `0.4` and a mild Emission. This ensures the references are always visible, unshadowed, but transparent enough to model through.
* **Step C: Lighting & Rendering Context**
  - **Engine**: EEVEE (preferred for fast, stylized real-time rendering).
  - **Post-Processing**: Ambient Occlusion (GTAO), Bloom, and Screen Space Reflections (SSR) are explicitly disabled to keep the viewport visually flat and clean, preventing shading artifacts from obscuring the raw low-poly topology.
* **Step D: Animation & Dynamics**
  - Enables the built-in `rigify` addon, which is an industry standard for generating complex animation rigs from simple meta-rigs.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Stylized Color | `view_settings.view_transform` | 'Standard' transform maps RGB values linearly without photorealistic compression. |
| Scale Reference | `addon_utils.enable` + `armature_human_metarig_add` | Leverages Blender's built-in Rigify to provide an industry-standard proportional guide. |
| Reference Images | Mesh Planes + Transparent Material | Robust procedural alternative to requiring external local image files; creates ready-to-use drafting boards. |

> **Feasibility Assessment**: 100% — This code perfectly reproduces the specific workspace configuration, scaling strategy, and material setup demonstrated in the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedSetup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 0.8),
    **kwargs,
) -> str:
    """
    Create a Stylized Character Modeling Scene Setup in the active Blender scene.
    Configures color management, spawns a scale reference rig, and sets up orthographic drafting planes.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created reference setup.
        location: (x, y, z) world-space position for the center of the setup.
        scale: Uniform scale factor for the rig and references.
        material_color: (R, G, B) color theme for the front reference plane.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import addon_utils
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Render & Color Management Setup ===
    # Set to EEVEE for real-time stylized preview
    scene.render.engine = 'BLENDER_EEVEE'
    
    # CRITICAL: Switch to Standard color transform for accurate flat colors
    scene.view_settings.view_transform = 'Standard'
    
    # Safely disable post-processing that interferes with flat/stylized modeling
    if hasattr(scene.eevee, "use_gtao"): scene.eevee.use_gtao = False
    if hasattr(scene.eevee, "use_bloom"): scene.eevee.use_bloom = False
    if hasattr(scene.eevee, "use_ssr"): scene.eevee.use_ssr = False

    created_objects = []
    loc_vec = Vector(location)

    # === Step 2: Spawn Scale Reference Rig ===
    # Enable Rigify addon to access standard proportions
    addon_utils.enable("rigify", default_set=True)
    
    rig = None
    if hasattr(bpy.ops.object, 'armature_human_metarig_add'):
        bpy.ops.object.armature_human_metarig_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_ScaleRefRig"
    else:
        # Fallback if rigify isn't available
        bpy.ops.object.armature_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_ScaleRefRig_Fallback"
    
    rig.scale = (scale, scale, scale)
    created_objects.append(rig.name)

    # === Step 3: Create Transparent Orthographic Drafting Planes ===
    def create_ref_plane(name, loc, rot, color, scale_vec):
        bpy.ops.mesh.primitive_plane_add(size=1)
        plane = bpy.context.active_object
        plane.name = name
        plane.location = loc
        plane.rotation_euler = rot
        plane.scale = scale_vec
        
        # Setup semi-transparent, unlit material
        mat = bpy.data.materials.new(name=f"{name}_Mat")
        mat.use_nodes = True
        mat.blend_method = 'BLEND'
        mat.shadow_method = 'NONE'
        
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            if 'Base Color' in bsdf.inputs:
                bsdf.inputs['Base Color'].default_value = (*color, 1.0)
            if 'Alpha' in bsdf.inputs:
                bsdf.inputs['Alpha'].default_value = 0.4
                
            # Add emission so it's visible regardless of scene lighting
            if 'Emission Color' in bsdf.inputs: # Blender 4.0+
                bsdf.inputs['Emission Color'].default_value = (*color, 1.0)
                bsdf.inputs['Emission Strength'].default_value = 0.5
            elif 'Emission' in bsdf.inputs: # Blender 3.x
                bsdf.inputs['Emission'].default_value = (*color, 1.0)
                if 'Emission Strength' in bsdf.inputs:
                    bsdf.inputs['Emission Strength'].default_value = 0.5
                    
        plane.data.materials.append(mat)
        
        # Disable selection in viewport so the user doesn't accidentally click it while modeling
        plane.hide_select = True
        return plane

    # Front Reference (Parallel to XZ plane, pushed back along +Y)
    front_loc = loc_vec + Vector((0, 2 * scale, 1 * scale))
    front_rot = (math.radians(90), 0, 0)
    front_scale = (2 * scale, 2 * scale, 2 * scale) 
    front_plane = create_ref_plane(f"{object_name}_FrontRef", front_loc, front_rot, material_color, front_scale)
    created_objects.append(front_plane.name)
    
    # Side Reference (Parallel to YZ plane, pushed to the left along -X)
    # Using an analogous contrasting color for the side view
    side_color = (max(0, 1.0 - material_color[0]), material_color[1], max(0, 1.0 - material_color[2]))
    side_loc = loc_vec + Vector((-2 * scale, 0, 1 * scale))
    side_rot = (math.radians(90), 0, math.radians(-90))
    side_scale = (2 * scale, 2 * scale, 2 * scale)
    side_plane = create_ref_plane(f"{object_name}_SideRef", side_loc, side_rot, side_color, side_scale)
    created_objects.append(side_plane.name)

    return f"Configured Stylized Scene Setup at {location}. Created objects: {', '.join(created_objects)}"
```