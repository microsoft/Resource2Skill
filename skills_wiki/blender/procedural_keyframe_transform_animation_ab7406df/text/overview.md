# Procedural Keyframe Transform Animation

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Keyframe Transform Animation

* **Core Visual Mechanism**: The core mechanism is transitioning an object's spatial properties (Location, Rotation, Scale) over time using Keyframes and F-Curves. The visual signature is the *interpolation* between these states—specifically the `BEZIER` easing curve that provides a natural "ease-in" and "ease-out" movement, as opposed to rigid, robotic linear motion.

* **Why Use This Skill (Rationale)**: Static scenes often feel lifeless. Adding basic transform animations using proper Bezier easing mimics natural physics (where objects require time to accelerate and decelerate due to momentum). Understanding how to manipulate F-Curve handles in the Graph Editor allows for precise timing and impact, such as a slow wind-up followed by a snappy stop.

* **Overall Applicability**: Essential for almost any dynamic scene. This pattern is the foundation for animating props (doors opening, moving platforms), blocking out camera movements (fly-throughs), and creating motion graphics (scaling text/UI elements).

* **Value Addition**: Transforms a static mesh into a dynamic actor within the timeline, instantly adding narrative or temporal depth to a composition.


### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - A standard primitive (Cube) is used as the base subject. Topology is irrelevant for basic object-level transform animation, as the entire object moves as a single unit without vertex deformation.

* **Step B: Materials & Shading**
  - A basic Principled BSDF shader is applied with a distinct color and moderate roughness.
  - A colored material is necessary to clearly perceive rotation and scale changes during playback, as a default grey cube rotating on certain axes can look stationary due to lack of surface definition.

* **Step C: Lighting & Rendering Context**
  - Works universally in both EEVEE and Cycles. Standard lighting is sufficient.
  - The scene's timeline (`frame_start`, `frame_end`) dictates the context in which this animation plays.

* **Step D: Animation & Dynamics (if applicable)**
  - **Keyframes**: Inserted using `obj.keyframe_insert()` for `location`, `rotation_euler`, and `scale`.
  - **Interpolation**: Handled via `fcurve.keyframe_points[x].interpolation`. The default is `'BEZIER'`. Other types introduced are `'LINEAR'` (constant speed) and `'CONSTANT'` (instant snap).
  - **Graph Editor Handles**: Accessed via `keyframe_point.handle_left_type` and `.handle_left`. By setting the handle type to `'FREE'`, you can break the default symmetry to create sharp stops or exaggerated wind-ups.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base Object | `bpy.ops.mesh.primitive_cube_add` | Simple visual anchor to demonstrate spatial movement. |
| Keyframing | `obj.keyframe_insert()` | The programmatic equivalent of hovering and pressing the 'I' or 'K' key in the UI. |
| Easing & Graph Editor | `fcurve.keyframe_points` manipulation | Allows direct access to the animation curve math (interpolation types and handle vectors) demonstrated in the Graph Editor portion of the tutorial. |

> **Feasibility Assessment**: 100% — The code fully reproduces the concept of adding transform keyframes, applying interpolation, and tweaking graph editor handles to create custom ease-in/ease-out motion.

#### 3b. Complete Reproduction Code

```python
def create_animated_object(
    scene_name: str = "Scene",
    object_name: str = "AnimatedCube",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.1, 0.5, 0.8),
    start_frame: int = 1,
    end_frame: int = 60,
    move_distance: float = 5.0,
    **kwargs,
) -> str:
    """
    Create an animated object demonstrating keyframes, Bezier interpolation, 
    and custom Graph Editor handle adjustments.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) starting world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color in 0-1 range.
        start_frame: Frame where animation begins.
        end_frame: Frame where animation stops.
        move_distance: Distance to travel along the X axis.

    Returns:
        Status string describing the created animation.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry ===
    bpy.ops.mesh.primitive_cube_add(size=2.0)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # === Step 2: Build Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.3
    obj.data.materials.append(mat)

    # === Step 3: Animation & Keyframing ===
    # Ensure animation data and action exist
    if not obj.animation_data:
        obj.animation_data_create()
    action = bpy.data.actions.new(name=f"{object_name}_Action")
    obj.animation_data.action = action

    # Keyframe 1: Start State
    obj.location = Vector(location)
    obj.rotation_euler = (0.0, 0.0, 0.0)
    obj.scale = (scale, scale, scale)
    
    obj.keyframe_insert(data_path="location", frame=start_frame)
    obj.keyframe_insert(data_path="rotation_euler", frame=start_frame)
    obj.keyframe_insert(data_path="scale", frame=start_frame)

    # Keyframe 2: End State (Moved, rotated, and scaled)
    obj.location = Vector(location) + Vector((move_distance, 0.0, 0.0))
    obj.rotation_euler = (math.pi / 2, 0.0, math.pi) # Rotate to make movement obvious
    obj.scale = (scale * 1.5, scale * 1.5, scale * 1.5)
    
    obj.keyframe_insert(data_path="location", frame=end_frame)
    obj.keyframe_insert(data_path="rotation_euler", frame=end_frame)
    obj.keyframe_insert(data_path="scale", frame=end_frame)

    # === Step 4: Graph Editor / Interpolation Adjustments ===
    for fcurve in action.fcurves:
        for kf in fcurve.keyframe_points:
            # Set default interpolation to smooth ease-in/ease-out
            kf.interpolation = 'BEZIER'

        # Replicate a "sharp stop" effect by modifying the X-location curve handles
        if fcurve.data_path == "location" and fcurve.array_index == 0:
            start_kf = fcurve.keyframe_points[0]
            end_kf = fcurve.keyframe_points[-1]
            
            # Make the end keyframe handle 'FREE' so we can manipulate it
            end_kf.handle_left_type = 'FREE'
            
            # Flatten the left handle of the end keyframe to create a sudden, harsh stop
            # rather than a gradual deceleration
            end_kf.handle_left.y = end_kf.co.y
            end_kf.handle_left.x = end_kf.co.x - (end_frame - start_frame) * 0.1

    # Ensure the scene plays long enough to see the animation
    if scene.frame_end < end_frame + 20:
        scene.frame_end = end_frame + 20

    return f"Created animated '{object_name}' at {location}. Animation spans frames {start_frame}-{end_frame} with Bezier easing."
```