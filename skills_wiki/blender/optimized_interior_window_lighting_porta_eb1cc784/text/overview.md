# Optimized Interior Window Lighting (Portals & Shadowless Materials)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Optimized Interior Window Lighting (Portals & Shadowless Materials)

* **Core Visual Mechanism**: This technique floods interior scenes with natural environment light while dramatically reducing render noise. It utilizes **Area Lights set as Portals** to guide the path tracer's sample rays. Crucially, it uses the **Light Path node (`Is Shadow Ray`)** to dynamically swap complex Glass and Translucent materials for purely Transparent materials whenever the render engine calculates shadows.

* **Why Use This Skill (Rationale)**: Interior scenes in path tracers (like Cycles) are notoriously noisy because most environmental light rays bounce off exterior walls and fail to find the small window openings. Calculating refractive caustics through glass and subsurface scattering through curtains creates severe "fireflies" (hot pixels) and increases render times exponentially. By explicitly telling the engine where the light comes from (Portals) and allowing light to pass through windows/curtains without casting complex shadows, you achieve clean, realistic lighting in a fraction of the time.

* **Overall Applicability**: Essential for Architectural Visualization (ArchViz), interior design rendering, or any scene where a camera is inside a room looking at (or illuminated by) a window.

* **Value Addition**: Replaces naive, noisy window setups with a production-ready, highly optimized lighting rig. It provides physically plausible light transmission without the computational overhead of true glass caustics.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Glass**: A simple flat plane, as thickness can cause unnecessary refractive distortion for basic windows.
  - **Curtain**: A highly subdivided plane using a `Wave` modifier (along the local X-axis) to procedurally generate vertical folds and draped fabric geometry.

* **Step B: Materials & Shading**
  - **Optimized Glass**: A `Mix Shader` blending a `Glass BSDF` (for camera reflections/refractions) and a `Transparent BSDF` (pure white, completely invisible). The mix factor is driven by a `Light Path` node's `Is Shadow Ray` output.
  - **Optimized Curtain**: A `Diffuse BSDF` and `Translucent BSDF` combined via an `Add Shader`. This combination is then mixed with a `Transparent BSDF` using the same `Is Shadow Ray` trick.
  - *Note*: The Transparent BSDF color must be pure white `(1.0, 1.0, 1.0, 1.0)` to let 100% of the light through.

* **Step C: Lighting & Rendering Context**
  - **Light Portal**: An Area Light scaled to exactly match the window dimensions, placed slightly outside, pointing inward. `use_portal` is enabled, which disables its own light emission and instead turns it into a "magnet" for HDRI/Environment light samples.
  - **Engine Context**: Exclusively designed for path tracers (Cycles). 
  - **Render Settings**: Benefits from clamping indirect light (e.g., 10.0) and raising `Transparent Max Bounces` (e.g., to 24) to ensure light penetrates multiple layers of glass and fabric.

* **Step D: Animation & Dynamics**
  - The Wave modifier on the curtain can have its `Time` offset animated to simulate a gentle breeze.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Window & Curtain Geometry | `bpy.ops.mesh.primitive_plane_add` + `Wave` modifier | Provides clean UVs and procedural, non-destructive fabric folds. |
| Shadowless Materials | Shader Node Tree (`Mix Shader` + `Light Path`) | Programmatically bypasses the engine's shadow calculations for specific materials, which is the core optimization technique shown. |
| Guided Lighting | `bpy.ops.object.light_add(type='AREA')` + `use_portal = True` | The native Blender method for optimizing environment sampling through architectural openings. |

> **Feasibility Assessment**: 100% reproduction of the core lighting and material optimization technique. Note that the tutorial also discusses Cryptomatte compositing, which is heavily dependent on individual user scene setups; therefore, this script focuses purely on the robust, universally applicable 3D scene elements (materials and portals).

#### 3b. Complete Reproduction Code

```python
def create_optimized_window_setup(
    scene_name: str = "Scene",
    object_name: str = "OptimizedWindow",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    glass_color: tuple = (1.0, 1.0, 1.0, 1.0),
    curtain_color: tuple = (0.8, 0.8, 0.75, 1.0),
    window_width: float = 2.0,
    window_height: float = 3.0,
    **kwargs,
) -> str:
    """
    Creates an optimized window setup for interior rendering, including shadowless
    glass, translucent wave curtains, and an environment light portal.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created object hierarchy.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        glass_color: RGBA color for the glass tint.
        curtain_color: RGBA color for the fabric.
        window_width: Width of the window/portal in meters.
        window_height: Height of the window/portal in meters.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Calculate scaled dimensions
    w = window_width * scale
    h = window_height * scale
    loc = Vector(location)
    
    # === Step 1: Create Parent Hierarchy ===
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=loc)
    parent_obj = bpy.context.active_object
    parent_obj.name = object_name
    
    # === Step 2: Create Optimized Glass Material ===
    glass_mat = bpy.data.materials.new(name=f"{object_name}_OptimizedGlass")
    glass_mat.use_nodes = True
    nodes = glass_mat.node_tree.nodes
    links = glass_mat.node_tree.links
    nodes.clear()
    
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (300, 0)
    
    mix_node = nodes.new(type='ShaderNodeMixShader')
    mix_node.location = (100, 0)
    
    glass_node = nodes.new(type='ShaderNodeBsdfGlass')
    glass_node.location = (-100, 100)
    glass_node.inputs['Color'].default_value = glass_color
    
    transp_node = nodes.new(type='ShaderNodeBsdfTransparent')
    transp_node.location = (-100, -100)
    transp_node.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0) # Pure white lets all light pass
    
    lp_node = nodes.new(type='ShaderNodeLightPath')
    lp_node.location = (-100, 300)
    
    # Connect nodes: If 'Is Shadow Ray', use Transparent (Input 2), else use Glass (Input 1)
    links.new(glass_node.outputs['BSDF'], mix_node.inputs[1])
    links.new(transp_node.outputs['BSDF'], mix_node.inputs[2])
    links.new(lp_node.outputs['Is Shadow Ray'], mix_node.inputs[0])
    links.new(mix_node.outputs['Shader'], out_node.inputs['Surface'])
    
    # === Step 3: Create Glass Mesh ===
    bpy.ops.mesh.primitive_plane_add(size=1)
    glass_obj = bpy.context.active_object
    glass_obj.name = f"{object_name}_Glass"
    glass_obj.scale = (w, h, 1.0)
    glass_obj.rotation_euler[0] = math.radians(90) # Stand upright, normal faces +Y
    glass_obj.location = loc
    glass_obj.parent = parent_obj
    glass_obj.data.materials.append(glass_mat)
    
    # === Step 4: Create Optimized Curtain Material ===
    curtain_mat = bpy.data.materials.new(name=f"{object_name}_OptimizedCurtain")
    curtain_mat.use_nodes = True
    nodes = curtain_mat.node_tree.nodes
    links = curtain_mat.node_tree.links
    nodes.clear()
    
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (500, 0)
    
    mix_node = nodes.new(type='ShaderNodeMixShader')
    mix_node.location = (300, 0)
    
    add_node = nodes.new(type='ShaderNodeAddShader')
    add_node.location = (100, 100)
    
    diff_node = nodes.new(type='ShaderNodeBsdfDiffuse')
    diff_node.location = (-100, 200)
    diff_node.inputs['Color'].default_value = curtain_color
    
    transl_node = nodes.new(type='ShaderNodeBsdfTranslucent')
    transl_node.location = (-100, 50)
    transl_node.inputs['Color'].default_value = curtain_color
    
    transp_node2 = nodes.new(type='ShaderNodeBsdfTransparent')
    transp_node2.location = (100, -100)
    transp_node2.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
    
    lp_node2 = nodes.new(type='ShaderNodeLightPath')
    lp_node2.location = (100, 300)
    
    # Connect nodes: Mix Diffuse + Translucent, then bypass shadows with Transparent
    links.new(diff_node.outputs['BSDF'], add_node.inputs[0])
    links.new(transl_node.outputs['BSDF'], add_node.inputs[1])
    links.new(add_node.outputs['Shader'], mix_node.inputs[1])
    links.new(transp_node2.outputs['BSDF'], mix_node.inputs[2])
    links.new(lp_node2.outputs['Is Shadow Ray'], mix_node.inputs[0])
    links.new(mix_node.outputs['Shader'], out_node.inputs['Surface'])
    
    # === Step 5: Create Curtain Mesh ===
    bpy.ops.mesh.primitive_plane_add(size=1)
    curtain_obj = bpy.context.active_object
    curtain_obj.name = f"{object_name}_Curtain"
    curtain_obj.scale = (w * 1.2, h * 1.1, 1.0) # Slightly larger than window
    curtain_obj.rotation_euler[0] = math.radians(90)
    
    # Place curtain slightly "inside" the room (assuming room is in +Y direction)
    curtain_obj.location = loc + Vector((0.0, 0.2 * scale, 0.0))
    curtain_obj.parent = parent_obj
    curtain_obj.data.materials.append(curtain_mat)
    
    # Procedural wavy folds
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=25)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()
    
    wave_mod = curtain_obj.modifiers.new(name="FabricFolds", type='WAVE')
    wave_mod.use_x = True
    wave_mod.use_y = False
    wave_mod.height = 0.06 * scale
    wave_mod.width = 0.25 * scale
    
    # === Step 6: Create Area Light (Portal) ===
    bpy.ops.object.light_add(type='AREA', radius=1, location=loc)
    portal_obj = bpy.context.active_object
    portal_obj.name = f"{object_name}_LightPortal"
    portal_obj.data.shape = 'RECTANGLE'
    portal_obj.data.size = w
    portal_obj.data.size_y = h
    
    # Enable portal logic (requires Cycles)
    if hasattr(portal_obj.data, "cycles"):
        portal_obj.data.cycles.is_portal = True 
    else:
        # Fallback for newer blender versions where it might be structured differently
        try:
            portal_obj.data.use_portal = True
        except AttributeError:
            pass
            
    # Rotate pointing inward (+Y). Area lights default to pointing -Z.
    portal_obj.rotation_euler[0] = math.radians(90)
    
    # Place portal slightly "outside" the glass
    portal_obj.location = loc + Vector((0.0, -0.1 * scale, 0.0))
    portal_obj.parent = parent_obj

    # === Step 7: Apply Recommended Render Settings (Additive/Safe) ===
    if scene.render.engine == 'CYCLES':
        scene.cycles.sample_clamping_indirect = 10.0
        if scene.cycles.transparent_max_bounces < 24:
            scene.cycles.transparent_max_bounces = 24
            
    # Deselect all, set parent as active
    bpy.ops.object.select_all(action='DESELECT')
    parent_obj.select_set(True)
    bpy.context.view_layer.objects.active = parent_obj
    
    return f"Created '{object_name}' (Optimized Window setup) at {location} with {len(parent_obj.children)} children."
```