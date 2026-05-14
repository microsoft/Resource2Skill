### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized Character Workspace & Proportion Anchor Setup

* **Core Visual Mechanism**: This is a scene-preparation and layout technique. The defining characteristics are:
  1. **Color Accuracy**: Switching the render engine to EEVEE and the View Transform to 'Standard' (disabling filmic/AgX tone mapping).
  2. **Proportion Anchoring**: Injecting a standard human armature (`Rigify Human Meta-Rig`) to serve as a universal scale reference.
  3. **Orthographic Boundaries**: Aligning reference image planes exactly to the center of the world and scaling them to match the physical height of the armature.

* **Why Use This Skill (Rationale)**: When modeling stylized characters (like anime or low-poly game assets), default color management (AgX/Filmic) washes out colors, making texture painting and material setup inaccurate. Furthermore, importing references without a scale anchor often results in characters that are vastly disproportionate (e.g., 10 meters tall), which breaks physics, lighting, and camera depth of field later on. The Meta-Rig provides an instant, perfect 3D bounding box for human proportions.

* **Overall Applicability**: Essential first step for any character modeling project, hard-surface robot modeling, or asset creation where matching a concept art turnaround is required and real-world scale matters.

* **Value Addition**: Transforms a blank, uncalibrated viewport into a perfectly scaled, color-accurate orthographic modeling environment, preventing structural scale issues down the line.


### 2. Technical Breakdown

* **Step A: Render & Color Management**
  - **Engine**: EEVEE (disabling Ambient Occlusion, Bloom, Screen Space Reflections, and Motion Blur to prevent stylized assets from looking "muddy").
  - **Color Space**: `Render Properties > Color Management > View Transform` changed to `Standard`. This ensures 1:1 color reproduction from reference images to 3D materials.

* **Step B: Scale Anchoring (Topology)**
  - Enable the built-in `Rigify` add-on.
  - Spawn an `Armature > Human (Meta-Rig)`. This rig is roughly 2 meters tall and provides immediate visual cues for joint placement (knees, elbows, waist).

* **Step C: Reference Alignment**
  - **Front View**: Placed on the Y-axis behind the origin (e.g., `Y = 2.0`), rotated `90°` on the X-axis.
  - **Side View**: Placed on the X-axis to the side of the origin (e.g., `X = -2.0`), rotated `90°` on X and `90°` on Z.
  - **Opacity**: Set to 50% so the model and rig can be seen through the reference planes.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Color/Render Settings | `bpy.context.scene` properties | Directly configures the environment for stylized work. |
| Proportion Anchor | `addon_utils.enable("rigify")` + `armature_human_metarig_add` | Guarantees a standard, anatomically scaled guide. |
| Reference Planes | Mesh planes with alpha-blended materials | Because we cannot download external image files in this script, we generate procedural colored grids to act as stand-in reference planes. This perfectly demonstrates the spatial alignment logic. |

> **Feasibility Assessment**: 100% of the scene setup and spatial logic is reproduced. The user will simply replace the procedural materials on the generated planes with their actual character concept art textures.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "Stylized_Workspace",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.0, 0.0, 0.0), # Unused for workspace setup
    **kwargs,
) -> str:
    """
    Create a Stylized Character Workspace with a proportion anchor and reference planes.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the organizational collection.
        location: Base offset for the workspace setup.
        scale: Uniform scale factor for the references and rig.
        material_color: Unused.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import addon_utils
    import math
    from mathutils import Vector
    
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Render & Color Management Setup ===
    scene.render.engine = 'BLENDER_EEVEE'
    scene.view_settings.view_transform = 'Standard'
    
    # Safely disable post-processing effects for a clean stylized look
    if hasattr(scene, "eevee"):
        if hasattr(scene.eevee, "use_gtao"): scene.eevee.use_gtao = False
        if hasattr(scene.eevee, "use_bloom"): scene.eevee.use_bloom = False
        if hasattr(scene.eevee, "use_ssr"): scene.eevee.use_ssr = False
        if hasattr(scene.eevee, "use_motion_blur"): scene.eevee.use_motion_blur = False

    # Create a collection to organize the workspace
    workspace_coll = bpy.data.collections.new(object_name)
    scene.collection.children.link(workspace_coll)

    # === Step 2: Add Proportion Anchor (Meta-Rig) ===
    # Enable rigify to access the meta-rig
    addon_utils.enable("rigify")
    
    bpy.ops.object.armature_human_metarig_add(location=location)
    rig = bpy.context.active_object
    rig.name = f"{object_name}_Proportion_Anchor"
    rig.scale = (scale, scale, scale)
    
    # Move to our collection
    for coll in rig.users_collection:
        coll.objects.unlink(rig)
    workspace_coll.objects.link(rig)

    # === Step 3: Create Procedural Reference Materials ===
    def create_ref_material(name, color):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        mat.blend_method = 'BLEND' # Enable alpha blending
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        bsdf = nodes.get("Principled BSDF")
        
        # Grid Texture for measurement visual
        tex_grid = nodes.new("ShaderNodeTexChecker")
        tex_grid.inputs['Scale'].default_value = 10.0
        tex_grid.inputs['Color1'].default_value = (*color, 1.0)
        tex_grid.inputs['Color2'].default_value = (0.05, 0.05, 0.05, 1.0)
        
        # Transparent Mix
        mix_shader = nodes.new("ShaderNodeMixShader")
        mix_shader.inputs['Fac'].default_value = 0.4 # 40% opacity
        
        transparent = nodes.new("ShaderNodeBsdfTransparent")
        
        # Connect
        links.new(tex_grid.outputs['Color'], bsdf.inputs['Base Color'])
        links.new(bsdf.outputs['BSDF'], mix_shader.inputs[2])
        links.new(transparent.outputs['BSDF'], mix_shader.inputs[1])
        
        # Output
        output = nodes.get("Material Output")
        links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])
        
        return mat

    mat_front = create_ref_material("RefMat_Front", (0.2, 0.6, 0.8)) # Blue-ish for front
    mat_side = create_ref_material("RefMat_Side", (0.8, 0.3, 0.2))   # Red-ish for side

    # === Step 4: Create and Align Reference Planes ===
    base_loc = Vector(location)
    
    # Front Reference Plane (Behind character, facing forward)
    bpy.ops.mesh.primitive_plane_add(
        size=2.5 * scale, 
        location=base_loc + Vector((0, 1.5 * scale, 1.0 * scale)), 
        rotation=(math.radians(90), 0, 0)
    )
    front_plane = bpy.context.active_object
    front_plane.name = f"{object_name}_Ref_Front"
    front_plane.data.materials.append(mat_front)
    
    for coll in front_plane.users_collection:
        coll.objects.unlink(front_plane)
    workspace_coll.objects.link(front_plane)

    # Side Reference Plane (To the side, facing inward)
    bpy.ops.mesh.primitive_plane_add(
        size=2.5 * scale, 
        location=base_loc + Vector((-1.5 * scale, 0, 1.0 * scale)), 
        rotation=(math.radians(90), 0, math.radians(-90))
    )
    side_plane = bpy.context.active_object
    side_plane.name = f"{object_name}_Ref_Side"
    side_plane.data.materials.append(mat_side)
    
    # Scale side plane aspect ratio roughly to a human profile
    side_plane.scale.x = 0.6 
    
    for coll in side_plane.users_collection:
        coll.objects.unlink(side_plane)
    workspace_coll.objects.link(side_plane)

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created workspace '{object_name}' at {location} (EEVEE set to Standard view, Meta-Rig added, Front/Side reference guides positioned)."
```