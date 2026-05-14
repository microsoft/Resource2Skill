# Procedural Animated Bouncing Prop (Keyframe & Handle Manipulation)

## Analysis

# High-level Design Pattern Extraction

> **Skill Name**: Procedural Animated Bouncing Prop (Keyframe & Handle Manipulation)

* **Core Visual Mechanism**: The core technique here is the deliberate manipulation of **F-Curves**, **Interpolation Types** (Bezier, Linear, Constant), and **Bezier Handles** (Automatic vs. Free) to create snappy, stylized motion without over-keying. By explicitly isolating a single transform channel (e.g., Z-Axis Location) and breaking the bezier handles at the point of impact, we can create a physically stylized "bounce" using very few keyframes.

* **Why Use This Skill (Rationale)**: Beginners often use "Insert Keyframe > Available/LocRotScale" which litters the timeline with unnecessary keyframes, making adjustments difficult. Furthermore, default "Automatic" bezier handles create soft, floaty transitions. By programmatically injecting single-channel keyframes and explicitly changing the handle type to `FREE` at impact frames, you achieve a sharp, energetic change in momentum (V-shaped graph curve) while keeping the timeline organized. 

* **Overall Applicability**: This technique is essential for animating rigid bodies, stylized character props, bouncing balls, or UI elements that require precise timing, anticipation, and follow-through.

* **Value Addition**: Compared to standard keyframing, this approach yields an optimized Graph Editor layout, making the animation infinitely easier to tweak. It also demonstrates how to add Timeline Markers to track critical animation events (like impacts or footfalls).


# Technical Breakdown

* **Step A: Geometry & Topology**
  - A standard UV Sphere is used as the base primitive to clearly demonstrate the bouncing motion.
  - Geometry is shaded smooth to catch highlights nicely as it moves.

* **Step B: Materials & Shading**
  - A simple `Principled BSDF` material is applied.
  - Base Color defaults to a vibrant red/orange `(0.8, 0.2, 0.1)` to make the fast motion easily trackable by the eye.
  - Roughness is lowered to `0.3` to give it a slightly glossy, toy-like appearance.

* **Step C: Lighting & Rendering Context**
  - EEVEE is highly recommended for real-time playback of the animation at 24 or 30 FPS.
  - Standard viewport lighting is sufficient, though a directional shadow helps anchor the bounce to the "ground."

* **Step D: Animation & Dynamics**
  - **Single Channel Keyframing**: Animation is restricted purely to `location[2]` (Z-axis). X and Y remain completely clean.
  - **Interpolation**: Set to `BEZIER` for smooth arcs at the peak of the bounce.
  - **Handle Types**: At the peak of the bounce, handles are set to `AUTO` for hang-time. At the ground impact, handles are set to `FREE` and manually angled upwards to create a sharp, instantaneous rebound.
  - **Markers**: Timeline markers are created at the exact frames of impact to organize the timeline visually.


# Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base Mesh | `bpy.ops.mesh.primitive_uv_sphere_add` | Provides a clear, visible volume for demonstrating motion. |
| Single-Channel Keyframes | `action.fcurves.new(data_path="location", index=2)` | Prevents cluttering the graph editor with unused X/Y/Rotation data (Tutorial Tip 1 & 2). |
| Interpolation & Handles | `keyframe_points[i].handle_left_type = 'FREE'` | Allows creation of sharp V-curves for the bounce impact, breaking default floaty bezier transitions (Tutorial Tip 6 & 7). |
| Timeline Organization | `scene.timeline_markers.new()` | Visually labels key events in the timeline for easier workflow (Tutorial Tip 10). |

> **Feasibility Assessment**: 100%. Blender's Python API provides extensive, low-level access to the `animation_data`, `fcurves`, and bezier handle coordinate mathematics, allowing us to perfectly replicate the graph editor techniques shown in the video.

#### 3b. Complete Reproduction Code

```python
def create_animated_bounce(
    scene_name: str = "Scene",
    object_name: str = "BouncingProp",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.2, 0.1),
    **kwargs,
) -> str:
    """
    Create an animated bouncing prop demonstrating optimized keyframe injection, 
    handle manipulation, and timeline markers.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position (serves as the ground floor for the bounce).
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created animation data.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_uv_sphere_add(radius=scale, location=(location[0], location[1], location[2] + scale))
    obj = bpy.context.active_object
    obj.name = object_name
    bpy.ops.object.shade_smooth()

    # === Step 2: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.3
    
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    # === Step 3: Animation Setup & Keyframe Injection ===
    # Make sure animation data exists
    if not obj.animation_data:
        obj.animation_data_create()
    
    action = bpy.data.actions.new(name=f"{object_name}_BounceAction")
    obj.animation_data.action = action

    # Tip 1/2: Animate ONLY the Z location (index 2). Prevents graph editor clutter.
    fcurve_z = action.fcurves.new(data_path="location", index=2)

    # Keyframe timings & values
    ground_z = location[2] + scale
    bounce_height = 5.0 * scale
    
    # Format: (Frame, Z-Value, Is_Impact)
    keyframes_data = [
        (1, ground_z + bounce_height, False),
        (15, ground_z, True),
        (30, ground_z + bounce_height * 0.7, False),
        (45, ground_z, True),
        (60, ground_z + bounce_height * 0.4, False),
        (70, ground_z, True)
    ]

    # Add points to the F-Curve
    fcurve_z.keyframe_points.add(len(keyframes_data))
    
    impact_frames = []

    for i, (frame, val, is_impact) in enumerate(keyframes_data):
        kp = fcurve_z.keyframe_points[i]
        kp.co = (frame, val)
        
        # Tip 6: Use Bezier Interpolation
        kp.interpolation = 'BEZIER'
        
        # Tip 7: Modify Handle Types for physics simulation
        if is_impact:
            impact_frames.append(frame)
            # Break the handles so we can make a sharp V-shape curve
            kp.handle_left_type = 'FREE'
            kp.handle_right_type = 'FREE'
            
            # Manually aim handles upwards to create a sharp bounce rebound
            # The left handle looks backwards in time, the right looks forwards
            handle_steepness = bounce_height * 0.6
            kp.handle_left = Vector((frame - 3, val + handle_steepness))
            kp.handle_right = Vector((frame + 3, val + handle_steepness))
        else:
            # Hang-time at the peak of the bounce should be smooth
            kp.handle_left_type = 'AUTO'
            kp.handle_right_type = 'AUTO'

    # Update the fcurve to apply handle positions
    fcurve_z.update()

    # === Step 4: Timeline Organization ===
    # Tip 10: Insert Markers in the timeline at impact points
    for idx, frame in enumerate(impact_frames):
        marker_name = f"{object_name}_Impact_{idx+1}"
        # Prevent duplicate markers if script is run multiple times
        if marker_name in scene.timeline_markers:
            scene.timeline_markers.remove(scene.timeline_markers[marker_name])
        scene.timeline_markers.new(name=marker_name, frame=frame)

    # Ensure timeline range covers the animation
    scene.frame_start = 1
    if scene.frame_end < 80:
        scene.frame_end = 80

    return f"Created animated '{object_name}' demonstrating F-Curve isolation, FREE bezier handles for sharp impacts, and timeline markers."
```