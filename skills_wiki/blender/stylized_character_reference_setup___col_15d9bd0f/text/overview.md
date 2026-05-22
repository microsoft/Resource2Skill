### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized Character Reference Setup & Color Management

* **Core Visual Mechanism**: This pattern establishes the foundational environment for non-photorealistic (NPR) and stylized 3D modeling. The critical mechanism is overriding Blender's default photorealistic tone mapping (AgX or Filmic) by switching the View Transform to **Standard**, ensuring that unlit, flat colors render exactly as they are picked, without desaturation or hue-shifting. It pairs this with a spatial anchoring system—a calibrated scale dummy and aligned orthographic reference planes.

* **Why Use This Skill (Rationale)**: Photorealistic color management systems (like AgX) are designed to roll off highlights and handle intense light realistically. However, when modeling stylized low-poly characters (like anime or retro game models), artists rely on highly specific, hand-picked hexadecimal color palettes. If AgX is left on, these colors look washed out. Furthermore, placing blueprint planes and a standard human-sized armature before modeling ensures the character's proportions will be accurate and compatible with standard animation rigs later.

* **Overall Applicability**: This is "Step 0" for any stylized asset creation, low-poly character modeling, cell-shaded environments, or whenever strict 1:1 hex color accuracy is required in the viewport.

* **Value Addition**: Instead of starting with an empty void and a photorealistic camera, this skill instantly prepares an albedo-accurate workspace with an un-selectable blueprint cage and a proportionate 1.7m tall skeletal guide, accelerating the transition from 2D concept to 3D mesh.


### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Scale Guide**: A custom, script-generated Armature (Pelvis, Spine, Head, Arms) measuring exactly 1.7m tall. This mimics the tutorial's use of the Rigify Meta-Rig without requiring the add-on to be enabled.
  - **Blueprint Cage**: Two 2x2 meter planes (Front and Side) acting as canvases for reference images.
  - The planes are parented to a root empty and have `hide_select` set to `True` so they don't interfere with box-modeling selections.

* **Step B: Materials & Shading**
  - **Reference Grid Material**: Since external user images cannot be reliably imported in a generic script, the script procedurally generates a blueprint grid.
  - It uses a `Mix Shader` driven by a `Math (Less Than)` node reading a `Brick Texture`. 
  - The mortar lines map to an **Emission** shader (making the grid visible regardless of scene lighting), while the blocks map to a **Transparent BSDF** (allowing the artist to see through the reference plane to the model).
  - Blend Mode is set to `BLEND` and Shadows to `NONE`.

* **Step C: Lighting & Rendering Context**
  - **Engine**: EEVEE (Ideal for fast, stylized viewport feedback).
  - **Color Management**: View Transform forced to `Standard`.
  - **Post-Processing**: Ambient Occlusion, Bloom, Screen Space Reflections, and Motion Blur are disabled to prevent atmospheric interference with raw modeling geometry.

* **Step D: Animation & Dynamics**
  - N/A - This is a static modeling reference environment.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Color Management | `bpy.context.scene.view_settings` | Directly forces the viewport to render flat, accurate colors. |
| Scale Reference | `bpy.data.armatures.new` | A custom 5-bone armature is lightweight, non-rendering, and perfectly mimics the spatial volume of a human figure. |
| Blueprint Planes | `bpy.ops.mesh.primitive_plane_add` | Simple geometry placed at specific mathematical offsets (-Y and +X). |
| Blueprint Grid | Procedural Shader Nodes | Uses `TexBrick` + `Emission` + `Transparent BSDF` to create an unlit, see-through reference grid without needing external image files. |

> **Feasibility Assessment**: 100%. The script perfectly captures the scene setup, color management overrides, and spatial reference logic described in the video, replacing the specific downloaded character artwork with a generic, reusable procedural blueprint grid.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "Stylized_Reference_Setup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.05, 0.4, 0.8), # Blueprint cyan/blue
    **kwargs,
) -> str:
    """
    Create a Stylized Character Reference Setup in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the root empty and child setup objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the entire reference setup.
        material_color: (R, G, B) color for the procedural blueprint grid.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Stylized Scene Configuration ===
    if scene.render.engine != 'BLENDER_EEVEE':
        scene.render.engine = 'BLENDER_EEVEE'
    
    # CRITICAL: Disable AgX/Filmic for flat, accurate stylized colors
    scene.view_settings.view_transform = 'Standard'

    # Disable interfering Eevee effects (using try/except for forward compatibility with Eevee Next)
    try: scene.eevee.use_gtao = False
    except: pass
    try: scene.eevee.use_bloom = False
    except: pass
    try: scene.eevee.use_ssr = False
    except: pass
    try: scene.eevee.use_motion_blur = False
    except: pass

    # Create Root Empty to hold the setup
    root_empty = bpy.data.objects.new(object_name, None)
    root_empty.empty_display_type = 'ARROWS'
    root_empty.empty_display_size = 0.5
    scene.collection.objects.link(root_empty)
    root_empty.location = Vector(location)
    root_empty.scale = (scale, scale, scale)

    # === Step 2: Proportional Scale Armature ===
    armature_data = bpy.data.armatures.new(name=f"{object_name}_ArmatureData")
    arm_obj = bpy.data.objects.new(name=f"{object_name}_Scale_Guide", object_data=armature_data)
    scene.collection.objects.link(arm_obj)
    arm_obj.parent = root_empty
    
    # Enter Edit Mode to build the 1.7m proportional dummy
    bpy.context.view_layer.objects.active = arm_obj
    arm_obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    
    ebones = armature_data.edit_bones
    
    b_root = ebones.new("Legs")
    b_root.head = (0, 0, 0)
    b_root.tail = (0, 0, 0.9)
    
    b_spine = ebones.new("Spine")
    b_spine.head = (0, 0, 0.9)
    b_spine.tail = (0, 0, 1.4)
    b_spine.parent = b_root
    
    b_head = ebones.new("Head")
    b_head.head = (0, 0, 1.4)
    b_head.tail = (0, 0, 1.7)
    b_head.parent = b_spine
    
    b_arm_l = ebones.new("Arm.L")
    b_arm_l.head = (0.15, 0, 1.35)
    b_arm_l.tail = (0.75, 0, 1.35)
    b_arm_l.parent = b_spine
    
    b_arm_r = ebones.new("Arm.R")
    b_arm_r.head = (-0.15, 0, 1.35)
    b_arm_r.tail = (-0.75, 0, 1.35)
    b_arm_r.parent = b_spine

    bpy.ops.object.mode_set(mode='OBJECT')
    
    # === Step 3: Procedural Blueprint Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Grid_Mat")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'
    mat.shadow_method = 'NONE'
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    for n in nodes: nodes.remove(n)
    
    output = nodes.new('ShaderNodeOutputMaterial')
    transparent = nodes.new('ShaderNodeBsdfTransparent')
    
    emission = nodes.new('ShaderNodeEmission')
    emission.inputs['Color'].default_value = (*material_color, 1.0)
    
    mix_shader = nodes.new('ShaderNodeMixShader')
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    mapping = nodes.new('ShaderNodeMapping')
    mapping.inputs['Scale'].default_value = (10, 10, 10) # 10x10 grid on a 2x2 plane
    
    brick = nodes.new('ShaderNodeTexBrick')
    brick.inputs['Color1'].default_value = (1, 1, 1, 1)
    brick.inputs['Color2'].default_value = (1, 1, 1, 1)
    brick.inputs['Mortar'].default_value = (0, 0, 0, 1) # Black lines to isolate
    brick.inputs['Mortar Size'].default_value = 0.02
    
    # Extract black mortar lines to use as Alpha mask
    math_node = nodes.new('ShaderNodeMath')
    math_node.operation = 'LESS_THAN'
    math_node.inputs[1].default_value = 0.5
    
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], brick.inputs['Vector'])
    links.new(brick.outputs['Color'], math_node.inputs[0])
    
    # Mix Transparent (0) with Emissive Grid (1)
    links.new(transparent.outputs['BSDF'], mix_shader.inputs[1])
    links.new(emission.outputs['Emission'], mix_shader.inputs[2])
    links.new(math_node.outputs['Value'], mix_shader.inputs['Fac'])
    
    links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])

    # === Step 4: Reference Planes ===
    
    # Front View Plane (Placed behind the model on Y axis)
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=(0, 1.5, 1.0))
    front_plane = bpy.context.active_object
    front_plane.name = f"{object_name}_Front_View"
    front_plane.rotation_euler = (math.radians(90), 0, 0)
    front_plane.data.materials.append(mat)
    
    # Side View Plane (Placed beside the model on X axis)
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=(-1.5, 0, 1.0))
    side_plane = bpy.context.active_object
    side_plane.name = f"{object_name}_Side_View"
    side_plane.rotation_euler = (math.radians(90), 0, math.radians(90))
    side_plane.data.materials.append(mat)
    
    # Parent and lock planes
    front_plane.parent = root_empty
    side_plane.parent = root_empty
    
    # Prevent accidental selection of planes while modeling
    front_plane.hide_select = True 
    side_plane.hide_select = True

    return f"Created '{object_name}' setup at {location} (Standard Color Management set, Scale Armature generated, Reference Planes added)"
```