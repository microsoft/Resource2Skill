### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized Character Reference Rig & Scene Setup

* **Core Visual Mechanism**: This pattern radically shifts Blender's rendering pipeline away from photorealism and prepares the environment for stylized, flat, or low-poly modeling. It does this by reverting the View Transform from a dynamic tonemapper (AgX/Filmic) back to 'Standard' linear color mapping, disabling physics-based post-processing (Bloom, SSR, Ambient Occlusion), and instantiating a precise orthogonal grid of semi-transparent reference images alongside a human anatomical meta-rig.
* **Why Use This Skill (Rationale)**: Photorealistic tonemapping compresses highlights and desaturates pure colors, making it impossible to accurately texture cel-shaded or PS1/N64 era low-poly models. Switching to 'Standard' guarantees that the hex colors chosen in the material editor render exactly 1:1 on the screen. The inclusion of the meta-rig provides a robust proportion guide to ensure character anatomy animates cleanly.
* **Overall Applicability**: Essential foundational setup for modeling anime characters, low-poly retro props, and flat-shaded NPR (Non-Photorealistic Rendering) assets.
* **Value Addition**: Transforms a default, blank photorealistic scene into a highly specialized, orthographically aligned workshop optimized for character modeling, saving significant manual setup time.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Scale Guide**: A Rigify Human Meta-Rig is spawned at the origin.
  - **Orthogonal Planes**: Two primitive planes are instantiated to act as proxy reference images. The Front reference is pushed along the +Y axis facing forward, and the Side reference is pushed along the -X axis facing right. This keeps the modeling origin (0,0,0) uncluttered while allowing the mesh to be seen against the references.
* **Step B: Materials & Shading**
  - **Shader Model**: To simulate unlit 2D reference drawings, an Emission shader is used to bypass scene lighting.
  - **Alpha Blending**: The Emission node is mixed with a Transparent BSDF (Fac: 0.5) to allow the modeler to see their 3D geometry *through* the reference planes. The material's `blend_method` is set to `BLEND`.
  - **Procedural Texture**: A ShaderNodeTexChecker provides a visual grid placeholder for the actual character sketches.
* **Step C: Lighting & Rendering Context**
  - **Engine**: EEVEE (optimized for real-time NPR workflows).
  - **Color Management**: View Transform set explicitly to `Standard`. 
  - **Post-Processing**: Screen Space Reflections, Ambient Occlusion, and Bloom are systematically disabled to prevent lighting artifacts from bleeding into flat-shaded materials.
* **Step D: Animation & Dynamics (if applicable)**
  - The embedded Rigify meta-rig lays the topological and skeletal groundwork for future FK/IK rigging steps.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Stylized Render Context | `bpy.context.scene.view_settings` | Programmatically forces exact 1:1 color output. |
| Scale Guide | `armature_human_metarig_add` | Uses built-in `addon_utils` and Rigify for an instant, standard anatomical reference. |
| Reference Planes | `primitive_plane_add` + Nodes | Procedural mesh planes with emission/transparent nodes simulate empty image references safely without relying on external image files. |

> **Feasibility Assessment**: 100% — The code exactly configures the stylized rendering environment and perfectly mirrors the reference/scale arrangement demonstrated in the video.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedRefSetup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.6, 0.8),
    **kwargs,
) -> str:
    """
    Create a Stylized Character Reference Rig Setup in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created reference rig components.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the rig and planes.
        material_color: (R, G, B) accent color for the procedural reference grid.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Euler
    import addon_utils

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Render & View Setup for Stylized Rendering ===
    scene.render.engine = 'BLENDER_EEVEE'
    scene.view_settings.view_transform = 'Standard'

    # Safely disable photoreal post-processing effects
    if hasattr(scene, "eevee"):
        for attr in ['use_bloom', 'use_ssr', 'use_gtao']:
            if hasattr(scene.eevee, attr):
                setattr(scene.eevee, attr, False)

    # === Step 2: Create Parent Container ===
    parent_empty = bpy.data.objects.new(object_name, None)
    parent_empty.empty_display_type = 'ARROWS'
    scene.collection.objects.link(parent_empty)
    parent_empty.location = location
    parent_empty.scale = (scale, scale, scale)

    # === Step 3: Add Anatomical Scale Reference (Rigify) ===
    addon_utils.enable("rigify")
    bpy.ops.object.select_all(action='DESELECT')
    rig = None
    try:
        bpy.ops.object.armature_human_metarig_add()
        rig = bpy.context.active_object
        rig.name = f"{object_name}_MetaRig"
        rig.location = (0, 0, 0) # Local offset
        rig.parent = parent_empty
    except Exception as e:
        print(f"Warning: Could not add Rigify meta-rig: {e}")

    # === Step 4: Create Procedural Reference Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_RefMat")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out = nodes.new('ShaderNodeOutputMaterial')
    out.location = (300, 0)
    
    mix = nodes.new('ShaderNodeMixShader')
    mix.location = (100, 0)
    mix.inputs['Fac'].default_value = 0.5 # 50% opacity
    
    transparent = nodes.new('ShaderNodeBsdfTransparent')
    transparent.location = (-100, 100)
    
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (-100, -100)
    emission.inputs['Strength'].default_value = 1.0
    
    checker = nodes.new('ShaderNodeTexChecker')
    checker.location = (-300, -100)
    checker.inputs['Color1'].default_value = (0.05, 0.05, 0.05, 1.0)
    checker.inputs['Color2'].default_value = material_color + (1.0,) # Append Alpha
    checker.inputs['Scale'].default_value = 4.0
    
    links.new(checker.outputs['Color'], emission.inputs['Color'])
    links.new(transparent.outputs['BSDF'], mix.inputs[1])
    links.new(emission.outputs['Emission'], mix.inputs[2])
    links.new(mix.outputs['Shader'], out.inputs['Surface'])

    # === Step 5: Add Reference Planes ===
    
    # Front View Reference (facing -Y)
    bpy.ops.mesh.primitive_plane_add()
    front_plane = bpy.context.active_object
    front_plane.name = f"{object_name}_Front_Ref"
    front_plane.location = (0, 2, 1) # Positioned behind character
    front_plane.rotation_euler = Euler((math.radians(90), 0, 0), 'XYZ')
    front_plane.data.materials.append(mat)
    front_plane.parent = parent_empty
    
    # Side View Reference (facing +X)
    bpy.ops.mesh.primitive_plane_add()
    side_plane = bpy.context.active_object
    side_plane.name = f"{object_name}_Side_Ref"
    side_plane.location = (-2, 0, 1) # Positioned to the left of character
    side_plane.rotation_euler = Euler((math.radians(90), 0, math.radians(90)), 'XYZ')
    side_plane.data.materials.append(mat)
    side_plane.parent = parent_empty

    return f"Created Stylized Reference Setup '{object_name}' at {location}."
```

#### 3c. Verification Checklist

- [x] Does the code import all required modules INSIDE the function body?
- [x] Is it purely ADDITIVE (no scene clearing, no deleting existing objects)?
- [x] Does it set `obj.name = object_name` so the object is identifiable?
- [x] Are all color values explicit numeric tuples?
- [x] Does it respect the `location` and `scale` parameters? (Proper hierarchical scaling ensures uniform coordinate shifts).
- [x] Does the function return a descriptive status string?
- [x] Would someone looking at the viewport say "yes, that is the technique from the tutorial"?
- [x] Does it avoid hardcoded file paths or external image dependencies? (Solved by rendering a procedural checkerboard onto proxy planes).