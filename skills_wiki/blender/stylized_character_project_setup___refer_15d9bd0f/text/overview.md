Here is the extracted 3D modeling skill based on the provided tutorial.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized Character Project Setup & Reference Alignment

* **Core Visual Mechanism**: This is a foundational project setup pattern rather than a specific modeled object. The defining mechanism is configuring Blender's Color Management to output raw, unmapped colors (Standard View Transform) and establishing a calibrated 3D spatial environment by aligning orthographic reference images to a real-world scale baseline (the Rigify human meta-rig).

* **Why Use This Skill (Rationale)**: By default, modern Blender versions use the 'AgX' or 'Filmic' view transforms. While excellent for photorealism, these tone-mappers compress highlights and desaturate colors, making stylized, anime, or low-poly textures look washed out. Switching to 'Standard' ensures that the exact hex colors you pick or paint are exactly what renders. Additionally, spawning a human meta-rig before modeling ensures your character has correct real-world proportions, preventing lighting, physics, and animation scaling issues later down the line.

* **Overall Applicability**: The absolute first step for any anime, low-poly, stylized, or non-photorealistic (NPR) character modeling workflow in Blender.

* **Value Addition**: Transforms Blender from a photorealistic simulator into a predictable canvas for stylized art, providing a precise scaffolding for modeling.


### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Scale Reference**: A Human Meta-Rig (via the built-in Rigify add-on) is spawned at the world origin to represent an average human height (~1.8m).
  - **Reference Planes**: 2D Image references (Front and Side orthographic views) are spawned and aligned to the rig.
  - The Front view is pushed back along the Y-axis. The Side view is pushed left along the X-axis.

* **Step B: Materials & Shading**
  - **Scene Color Management**: `View Transform` is changed from 'AgX' to 'Standard'. This maps render values linearly to the display (1.0 = 1.0), preserving vibrant, stylized colors.
  - **Reference Material**: The reference images are set to 50% opacity (Alpha = 0.5) to allow the modeler to see the 3D mesh passing through the reference drawing.

* **Step C: Lighting & Rendering Context**
  - **Render Engine**: EEVEE is selected for fast, real-time previewing.
  - **Post-Processing Disabled**: Ambient Occlusion, Bloom, Screen Space Reflections, and Motion Blur are disabled. These physically-based effects often conflict with flat, stylized shading goals.

* **Step D: Setup & Organization**
  - Reference objects are made unselectable in the viewport so they aren't accidentally moved during the modeling process.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Scene Settings | `bpy.context.scene` properties | Modifies global render engine and color management parameters natively. |
| Scale Reference | `addon_utils` + `bpy.ops` | Enables the built-in Rigify add-on programmatically to spawn the exact meta-rig used in the video. |
| Reference Images | `bpy.ops.mesh.primitive_plane_add` | Since external image files cannot be safely loaded via an automated script, semi-transparent placeholder planes are constructed to perfectly replicate the spatial layout and opacity settings of the reference images shown. |

> **Feasibility Assessment**: 100% of the project setup steps (Render Engine, Color Management, Rig spawning, and Reference alignment) are reproduced. Placeholder planes substitute the specific downloaded character artwork.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "Stylized_Project_Setup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.5), # Color for the placeholder reference planes
    **kwargs,
) -> str:
    """
    Configures the Blender scene for stylized character modeling and sets up a scale reference environment.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the setup objects.
        location: (x, y, z) world-space position for the setup origin.
        scale: Overall scale factor for the reference setup.
        material_color: (R, G, B) tint for the reference planes.
        **kwargs: Additional overrides.
        
    Returns:
        Status string describing the setup.
    """
    import bpy
    import bmesh
    from mathutils import Vector, Euler
    import math
    import addon_utils

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Configure Render Engine and Color Management ===
    # Crucial for stylized/anime characters: use Eevee and Standard color transform
    scene.render.engine = 'BLENDER_EEVEE'
    scene.eevee.use_gtao = False
    scene.eevee.use_bloom = False
    scene.eevee.use_ssr = False
    scene.eevee.use_motion_blur = False
    
    # Prevents "washed out" colors, mapping hex codes 1:1 to the screen
    scene.view_settings.view_transform = 'Standard'

    # Create a root empty to keep the outliner organized
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    setup_root = bpy.context.active_object
    setup_root.name = object_name
    setup_root.scale = (scale, scale, scale)

    # === Step 2: Add Scale Reference (Human Meta-Rig) ===
    rig_added = False
    try:
        # Attempt to enable Rigify and spawn the human meta-rig
        addon_utils.enable("rigify")
        bpy.ops.object.armature_human_metarig_add(location=location)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_ScaleRef_Rig"
        rig.parent = setup_root
        
        # The Rigify meta-rig is generated with its origin slightly off the floor
        rig.location.z += 0.95 
        rig_added = True
    except Exception as e:
        print(f"Could not add Rigify rig (context issue): {e}. Using fallback.")
        # Fallback to a basic bounding box representing a 1.8m tall human
        bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=1.8, location=(location[0], location[1], location[2] + 0.9))
        rig = bpy.context.active_object
        rig.name = f"{object_name}_ScaleRef_Fallback"
        rig.parent = setup_root

    # Lock the scale reference so it isn't accidentally edited
    rig.hide_select = True

    # === Step 3: Add Reference Planes ===
    # We construct semi-transparent planes to mimic the behavior of Reference Image Empties
    
    mat_ref = bpy.data.materials.new(name=f"{object_name}_RefPlane_Mat")
    mat_ref.use_nodes = True
    mat_ref.blend_method = 'BLEND' # Enable Eevee transparency
    mat_ref.shadow_method = 'NONE' # References shouldn't cast shadows
    
    bsdf = mat_ref.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
        # Set to 50% opacity as instructed in the tutorial
        bsdf.inputs["Alpha"].default_value = 0.5 
        bsdf.inputs["Roughness"].default_value = 1.0

    plane_size = 2.2 # Covers a standard human height

    # Front Reference Plane
    # Moved backwards along Y, rotated to face Front orthographic (Numpad 1)
    bpy.ops.mesh.primitive_plane_add(size=plane_size)
    front_ref = bpy.context.active_object
    front_ref.name = f"{object_name}_Ref_Front"
    front_ref.location = Vector((location[0], location[1] + 1.2, location[2] + plane_size/2))
    front_ref.rotation_euler = Euler((math.radians(90), 0, 0), 'XYZ')
    front_ref.data.materials.append(mat_ref)
    front_ref.parent = setup_root
    front_ref.hide_select = True # Prevent accidental selection during modeling

    # Side Reference Plane
    # Moved left along X, rotated to face Right orthographic (Numpad 3)
    bpy.ops.mesh.primitive_plane_add(size=plane_size)
    side_ref = bpy.context.active_object
    side_ref.name = f"{object_name}_Ref_Side"
    side_ref.location = Vector((location[0] - 1.2, location[1], location[2] + plane_size/2))
    side_ref.rotation_euler = Euler((math.radians(90), 0, math.radians(-90)), 'XYZ')
    side_ref.data.materials.append(mat_ref)
    side_ref.parent = setup_root
    side_ref.hide_select = True # Prevent accidental selection during modeling

    return f"Created Stylized Project Setup '{object_name}' (Standard View Transform set, Rigify reference: {rig_added})"
```