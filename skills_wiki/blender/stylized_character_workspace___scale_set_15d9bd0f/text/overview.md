### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized Character Workspace & Scale Setup

* **Core Visual Mechanism**: Transitioning the color space from photorealistic (`AgX` or `Filmic`) to `Standard` view transform, and establishing a baseline world scale using a standard `Human Meta-Rig` armature to align 2D orthographic reference images.
* **Why Use This Skill (Rationale)**: 
  1. **Color Accuracy**: Default photorealistic view transforms (like AgX) are designed to mimic camera sensors, meaning they compress highlights, desaturate high-intensity colors, and shift hues. For low-poly, anime, or stylized workflows using hand-painted textures, this ruins the intended 1-to-1 color mapping. Setting the transform to `Standard` ensures what you paint is exactly what renders.
  2. **Pipeline Scaling**: Modeling a character arbitrarily without a scale reference often leads to massive resizing issues later when exporting to game engines or attaching standard animation rigs. Using a standard Meta-Rig as a 3D blueprint ensures the character is "human-sized" and topologically proportioned from vertex one.
* **Overall Applicability**: Essential foundational setup for any stylized (non-PBR) 3D asset creation, low-poly modeling, and character pipeline integration.
* **Value Addition**: Prevents critical color-space errors that cause textures to look "washed out," and eliminates rigging/scaling headaches downstream by enforcing standard proportions early in the block-out phase.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - Uses the built-in `Rigify` add-on to generate a `Human Meta-Rig` (`bpy.ops.object.armature_human_metarig_add`).
  - Uses basic geometric planes mapped to the front (XZ) and side (YZ) orthogonal axes to act as spatial reference boards.
* **Step B: Materials & Shading**
  - Employs a semi-transparent shader for the reference boards to allow the user to see the 3D model "through" the 2D reference blueprint.
  - Material uses `BLEND` mode (in EEVEE) with Alpha set to `0.5`.
* **Step C: Lighting & Rendering Context**
  - **Engine**: EEVEE (preferred for stylized, flat-lit real-time preview).
  - **Color Management**: View Transform forced to `Standard`.
  - **Post-Processing disabled**: Ambient Occlusion, Bloom, Screen Space Reflections, and Motion Blur are turned off to prevent photorealistic shading artifacts from interfering with stylized textures.
* **Step D: Animation & Dynamics (if applicable)**
  - N/A for this stage, though the generated Meta-Rig is the first step toward the character's final skeletal structure.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Viewport Color Matching | `scene.view_settings` | Directly disables photorealistic tonemapping required for 1:1 color workflows. |
| Engine Setup | `scene.eevee` attributes | Disables post-processing overlays that break stylized shading. |
| Scale Reference | `addon_utils` + `armature_human_metarig_add` | Guarantees standard real-world proportions and game-engine ready scaling. |
| Reference Blueprints | Mesh planes + transparent material | Creates a reproducible placeholder for image references that the agent can interact with in 3D space. |

> **Feasibility Assessment**: 100%. While the tutorial relies on importing external image files, this code generates functional placeholder reference boards with a procedural grid, alongside the exact render settings and Meta-Rig setup demonstrated.

#### 3b. Complete Reproduction Code

```python
def create_stylized_character_setup(
    scene_name: str = "Scene",
    object_name: str = "CharacterSetup",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.5),
    **kwargs,
) -> str:
    """
    Create a stylized character modeling workspace including color management fixes,
    a scale-reference Meta-Rig, and orthogonal reference boards.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created setup objects.
        location: (x, y, z) world-space base position.
        scale: Uniform scale factor for the rig and boards.
        material_color: (R, G, B) color for the placeholder reference grid.

    Returns:
        Status string.
    """
    import bpy
    import addon_utils
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    base_loc = Vector(location)

    # === Step 1: Stylized Rendering & Color Management Setup ===
    # Force View Transform to Standard to prevent AgX/Filmic from desaturating stylized colors
    scene.view_settings.view_transform = 'Standard'
    
    # Set to EEVEE and disable realistic post-processing overlays
    scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(scene, "eevee_next") else 'BLENDER_EEVEE'
    
    # Safely disable legacy EEVEE settings (Graceful fallback for Blender 4.2+)
    if hasattr(scene, "eevee"):
        if hasattr(scene.eevee, "use_gtao"): scene.eevee.use_gtao = False
        if hasattr(scene.eevee, "use_bloom"): scene.eevee.use_bloom = False
        if hasattr(scene.eevee, "use_ssr"): scene.eevee.use_ssr = False
        if hasattr(scene.eevee, "use_motion_blur"): scene.eevee.use_motion_blur = False

    created_objects = []

    # === Step 2: Enable Rigify & Add Scale Reference Meta-Rig ===
    addon_utils.enable("rigify", default_set=True)
    
    try:
        bpy.ops.object.select_all(action='DESELECT')
        # Add Human Meta-Rig as a proportion/scale blueprint
        bpy.ops.object.armature_human_metarig_add(location=base_loc)
        rig = bpy.context.active_object
        rig.name = f"{object_name}_Scale_MetaRig"
        rig.scale = (scale, scale, scale)
        created_objects.append(rig.name)
    except Exception as e:
        print(f"Rigify rig creation failed (add-on may be missing): {e}")

    # === Step 3: Create Semi-Transparent Placeholder Reference Boards ===
    # Setup transparency material
    mat_ref = bpy.data.materials.new(name=f"{object_name}_Reference_Grid")
    mat_ref.use_nodes = True
    mat_ref.blend_method = 'BLEND' # Essential for EEVEE transparency
    
    nodes = mat_ref.node_tree.nodes
    links = mat_ref.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    
    if bsdf:
        bsdf.inputs["Alpha"].default_value = 0.4
        bsdf.inputs["Roughness"].default_value = 1.0
        
        # Add a procedural checker grid to act as a measurement reference
        checker = nodes.new(type="ShaderNodeTexChecker")
        checker.inputs["Color1"].default_value = (*material_color, 1.0) 
        checker.inputs["Color2"].default_value = (0.05, 0.05, 0.05, 1.0)
        checker.inputs["Scale"].default_value = 8.0
        links.new(checker.outputs["Color"], bsdf.inputs["Base Color"])

    # Build Front View Reference Board
    front_loc = base_loc + Vector((0.0, 1.5 * scale, 1.0 * scale))
    bpy.ops.mesh.primitive_plane_add(
        size=2.0 * scale, 
        location=front_loc, 
        rotation=(math.radians(90), 0, 0)
    )
    front_ref = bpy.context.active_object
    front_ref.name = f"{object_name}_RefBoard_Front"
    front_ref.scale = (1.0, 2.0, 1.0) # Scale to human proportion aspect ratio
    front_ref.data.materials.append(mat_ref)
    created_objects.append(front_ref.name)

    # Build Side View Reference Board
    side_loc = base_loc + Vector((1.5 * scale, 0.0, 1.0 * scale))
    bpy.ops.mesh.primitive_plane_add(
        size=2.0 * scale, 
        location=side_loc, 
        rotation=(math.radians(90), 0, math.radians(90))
    )
    side_ref = bpy.context.active_object
    side_ref.name = f"{object_name}_RefBoard_Side"
    side_ref.scale = (1.0, 2.0, 1.0)
    side_ref.data.materials.append(mat_ref)
    created_objects.append(side_ref.name)

    # Disable selection on reference boards so they don't interfere with modeling
    front_ref.hide_select = True
    side_ref.hide_select = True

    return f"Created Setup '{object_name}' (Color space set to Standard). Spawned: {', '.join(created_objects)}"
```

#### 3c. Verification Checklist
- [x] Does the code import all required modules INSIDE the function body?
- [x] Is it purely ADDITIVE (no scene clearing, no deleting existing objects)?
- [x] Does it set `obj.name = object_name` so the object is identifiable?
- [x] Are all color values explicit numeric tuples (not referencing undefined variables)?
- [x] Does it respect the `location` and `scale` parameters?
- [x] Does the function return a descriptive status string?
- [x] Would someone looking at the viewport say "yes, that is the technique from the tutorial"?
- [x] Does it avoid hardcoded file paths or external image dependencies?
- [x] Does it handle the case where an object with the same name already exists (Blender auto-suffixes, but verify no crashes)?