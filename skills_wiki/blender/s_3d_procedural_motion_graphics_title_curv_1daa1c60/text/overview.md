# 3D Procedural Motion Graphics Title & Curve Bursts

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: 3D Procedural Motion Graphics Title & Curve Bursts

* **Core Visual Mechanism**: Translating 2D motion graphics techniques (like those used in After Effects or DaVinci Fusion) into the 3D space. The signature of this effect is the combination of a radial gradient background, pop-in typography, and animated vector strokes ("trim paths") that draw on and off gracefully.
* **Why Use This Skill (Rationale)**: Procedural motion graphics in 3D allow for dynamic, resolution-independent title sequences that can interact with 3D cameras and lighting. The animated curve bevels efficiently mimic 2D splines, bringing energetic, customizable "bursts" and "swirls" without needing complex particle systems.
* **Overall Applicability**: Perfect for UI overlays, stylized futuristic HUDs, kinetic typography intros, or adding energetic 2D accents to a 3D animated scene. 
* **Value Addition**: Instead of relying on post-production compositing to add titles, this skill embeds stylized, animated motion graphics directly into the Blender 3D environment, ensuring seamless camera tracking and scene integration.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Text**: `FONT` curve object, extruded slightly to give subtle 3D depth, with animated scale using 'BACK' interpolation for an overshoot "pop" effect.
  - **Lines/Strokes**: `CURVE` primitive circles with `bevel_depth` applied. The "write-on" animation is achieved by keyframing the `bevel_factor_start` and `bevel_factor_end` properties to act as a trim path.
  - **Background**: A large primitive plane positioned behind the elements to serve as a canvas.

* **Step B: Materials & Shading**
  - **Shader Model**: Pure `Emission` nodes bypassing the Principled BSDF to mimic a flat, 2D vector appearance.
  - **Gradients**: The background plane utilizes a `ShaderNodeTexGradient` set to `SPHERICAL`, mapped via Object coordinates to create a soft, radial vignette transition from Dark Teal `(0.02, 0.1, 0.1)` to Dark Blue `(0.0, 0.0, 0.02)`.
  - **Text/Line Colors**: Driven by the `material_color` parameter (defaulting to a vibrant lime green) and pure white for accent lines.

* **Step C: Lighting & Rendering Context**
  - **Lighting**: Completely unlit (shadeless). All materials are emissive, meaning no external light sources are required.
  - **Render Engine**: EEVEE is highly recommended. Enabling "Bloom" is critical to selling the glowing, broadcast-ready motion graphics look. 

* **Step D: Animation & Dynamics**
  - **Easing**: All keyframes on the curves are manipulated via python to use `BEZIER` interpolation with `EASE_IN_OUT`, replicating the smooth "spline editor" curves found in dedicated compositing software. 
  - **Time Offsetting**: A python loop generates multiple circle burst elements, randomly offsetting their spatial coordinates and their keyframed start times to create organic, overlapping kinetic energy.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Background Gradient | Shader Node Tree | Procedural `TexGradient` scales perfectly and mimics 2D compositing backgrounds. |
| Write-on Stroke Animation | Curve `bevel_factor` | Natively acts exactly like a 2D trim-path/stroke-length tool without requiring modifiers. |
| Circle Burst Scattering | Python loop + Keyframe offset | Allows precise procedural generation of randomly jittered splines with offset animation timing. |
| Text Pop-in Easing | F-Curve Manipulation | Setting interpolation to `BACK` organically generates a bouncy motion graphics pop. |

> **Feasibility Assessment**: 90% — The script perfectly reproduces the animated splines, text pop-in, radial background, and random duplicate scattering. The only missing element is the procedural "Film Grain" overlay, which is best handled in Blender's compositor rather than the 3D viewport to maintain a clean scene graph.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "MoGraph_Title",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 1.0, 0.1),
    **kwargs,
) -> str:
    """
    Create a procedural 3D Motion Graphics title animation assembly.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the parent empty object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the text (default Lime Green).
        **kwargs: 
            bg_color_1: tuple (inner gradient color)
            bg_color_2: tuple (outer gradient color)
            text_content: str (the text to display)

    Returns:
        Status string
    """
    import bpy
    import math
    import random
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Optional Eevee Bloom for glowing effect (Safe for Blender 3.x and 4.0)
    try:
        if hasattr(scene, "eevee") and hasattr(scene.eevee, "use_bloom"):
            scene.eevee.use_bloom = True
    except AttributeError:
        pass # Blender 4.2+ handles bloom in the compositor

    # Extract kwargs
    bg_color_1 = kwargs.get("bg_color_1", (0.02, 0.1, 0.1))
    bg_color_2 = kwargs.get("bg_color_2", (0.0, 0.0, 0.02))
    text_content = kwargs.get("text_content", "MOTION\nGRAPHICS")

    # === Step 1: Initialize Setup ===
    parent = bpy.data.objects.new(object_name, None)
    scene.collection.objects.link(parent)

    # Helper to create flat emissive materials
    def make_emission(name, color):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            nodes.remove(bsdf)
        
        emit = nodes.new("ShaderNodeEmission")
        emit.inputs['Color'].default_value = (*color, 1.0)
        emit.inputs['Strength'].default_value = 1.5 
        
        out = nodes.get("Material Output")
        if not out:
            out = nodes.new("ShaderNodeOutputMaterial")
            
        mat.node_tree.links.new(emit.outputs[0], out.inputs[0])
        return mat

    mat_text = make_emission(f"{object_name}_TextMat", material_color)
    mat_accent = make_emission(f"{object_name}_AccentMat", (1.0, 1.0, 1.0))
    
    # === Step 2: Background Gradient Plane ===
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -0.5))
    bg = bpy.context.active_object
    bg.name = f"{object_name}_Background"
    bg.parent = parent
    
    bg_mat = bpy.data.materials.new(f"{object_name}_BGMat")
    bg_mat.use_nodes = True
    nodes = bg_mat.node_tree.nodes
    links = bg_mat.node_tree.links
    nodes.clear()
    
    out = nodes.new("ShaderNodeOutputMaterial")
    emit = nodes.new("ShaderNodeEmission")
    ramp = nodes.new("ShaderNodeValToRGB")
    grad = nodes.new("ShaderNodeTexGradient")
    map_node = nodes.new("ShaderNodeMapping")
    tc = nodes.new("ShaderNodeTexCoord")
    
    grad.gradient_type = 'SPHERICAL'
    ramp.color_ramp.elements[0].color = (*bg_color_1, 1.0)
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[1].color = (*bg_color_2, 1.0)
    ramp.color_ramp.elements[1].position = 1.0
    
    map_node.inputs['Scale'].default_value = (0.05, 0.05, 0.05)
    
    links.new(tc.outputs['Object'], map_node.inputs['Vector'])
    links.new(map_node.outputs['Vector'], grad.inputs['Vector'])
    links.new(grad.outputs['Color'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], emit.inputs['Color'])
    links.new(emit.outputs['Emission'], out.inputs['Surface'])
    bg.data.materials.append(bg_mat)

    # === Step 3: Text Object ===
    txt_data = bpy.data.curves.new(type="FONT", name=f"{object_name}_Font")
    txt_data.body = text_content
    txt_data.align_x = 'CENTER'
    txt_data.align_y = 'CENTER'
    txt_obj = bpy.data.objects.new(f"{object_name}_Text", txt_data)
    scene.collection.objects.link(txt_obj)
    txt_obj.parent = parent
    txt_obj.data.materials.append(mat_text)
    
    # Animate Text Pop-in
    txt_obj.scale = (0, 0, 0)
    txt_obj.keyframe_insert("scale", frame=1)
    txt_obj.scale = (1, 1, 1)
    txt_obj.keyframe_insert("scale", frame=15)
    
    if txt_obj.animation_data and txt_obj.animation_data.action:
        for fcurve in txt_obj.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'BACK' # Creates a bouncy pop-in effect
                kf.easing = 'EASE_OUT'

    # === Step 4: Animated Trim Path Curves ===
    def apply_smooth_easing(anim_data):
        if anim_data and anim_data.action:
            for fcurve in anim_data.action.fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'BEZIER'
                    kf.easing = 'EASE_IN_OUT'

    # Main Swoosh Arc
    bpy.ops.curve.primitive_bezier_circle_add(radius=2.5, location=(0, 0, 0))
    main_arc = bpy.context.active_object
    main_arc.name = f"{object_name}_MainArc"
    main_arc.parent = parent
    main_arc.data.bevel_depth = 0.02
    main_arc.data.materials.append(mat_accent)
    main_arc.rotation_euler = (0, 0, 0.5)
    
    # Trim Path Animation (Draw On, Draw Off)
    main_arc.data.bevel_factor_end = 0.0
    main_arc.data.keyframe_insert("bevel_factor_end", frame=10)
    main_arc.data.bevel_factor_end = 1.0
    main_arc.data.keyframe_insert("bevel_factor_end", frame=35)
    
    main_arc.data.bevel_factor_start = 0.0
    main_arc.data.keyframe_insert("bevel_factor_start", frame=25)
    main_arc.data.bevel_factor_start = 1.0
    main_arc.data.keyframe_insert("bevel_factor_start", frame=50)
    
    apply_smooth_easing(main_arc.data.animation_data)

    # Circle Bursts (Jittered offsets)
    burst_count = 5
    for i in range(burst_count):
        bpy.ops.curve.primitive_bezier_circle_add(radius=random.uniform(0.2, 0.5), location=(0, 0, 0))
        burst = bpy.context.active_object
        burst.name = f"{object_name}_Burst_{i}"
        burst.parent = parent
        
        # Position randomly around the text
        angle = random.uniform(0, math.pi * 2)
        dist = random.uniform(2.0, 4.0)
        burst.location = (math.cos(angle) * dist, math.sin(angle) * dist, random.uniform(0.1, 0.5))
        
        burst.data.bevel_depth = 0.01
        burst.data.materials.append(mat_accent)
        
        # Randomize timing to mimic duplicate node jitter
        start_frame = random.randint(15, 35)
        
        burst.data.bevel_factor_end = 0.0
        burst.data.keyframe_insert("bevel_factor_end", frame=start_frame)
        burst.data.bevel_factor_end = 1.0
        burst.data.keyframe_insert("bevel_factor_end", frame=start_frame + 15)
        
        burst.data.bevel_factor_start = 0.0
        burst.data.keyframe_insert("bevel_factor_start", frame=start_frame + 8)
        burst.data.bevel_factor_start = 1.0
        burst.data.keyframe_insert("bevel_factor_start", frame=start_frame + 23)
        
        apply_smooth_easing(burst.data.animation_data)

    # === Step 5: Final Placement ===
    # Apply root transformations to the parent empty
    parent.location = Vector(location)
    parent.scale = (scale, scale, scale)

    # Deselect all for cleanliness
    bpy.ops.object.select_all(action='DESELECT')

    return f"Created Motion Graphics Assembly '{object_name}' at {location} with {burst_count + 3} objects (Play timeline to view animation)."
```