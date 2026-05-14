# Procedural Cinematic Tracking Camera Rig

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Cinematic Tracking Camera Rig

* **Core Visual Mechanism**: A decoupled camera system where the camera's position is strictly constrained to a smooth Bezier path (simulating a dolly track or crane), while its rotation and Depth of Field (DoF) dynamically lock onto a designated "Focus Target" (an Empty object). This creates silky-smooth, sweeping cinematic motions without manual rotation keyframing.

* **Why Use This Skill (Rationale)**: Manually keyframing a camera's location and rotation simultaneously usually results in robotic, jittery motion. By decoupling movement (Follow Path) from aiming (Track To constraint), you mimic real-world cinematography equipment. It ensures the subject is never lost from the frame and remains perfectly in focus throughout complex fly-throughs or orbits.

* **Overall Applicability**: Essential for character showcases (turntables), architectural fly-throughs, product visualizations, and establishing shots. It replaces static angles with high-production-value motion.

* **Value Addition**: Compared to a standard static camera, this skill instantly injects motion and dynamic depth of field into a scene. It provides an automated, reusable rig that an agent or user can drop into any scene and immediately get a professional sweeping shot just by moving the track and the target.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Master Root**: An Empty object to control the overall placement of the entire rig.
  - **Focus Target**: A spherical Empty placed on the subject of interest.
  - **Camera Track**: A Bezier Circle (or NURBS path) dictating the movement trajectory.
  - **Camera Object**: The actual rendering camera, driven entirely by constraints, requiring no manual transform keyframes.

* **Step B: Materials & Shading**
  - Not applicable for the camera rig itself, but relies heavily on camera lens properties: Depth of Field enabled, an F-Stop of around 2.8 for cinematic background blur, and a standard focal length (e.g., 50mm or 35mm).

* **Step C: Lighting & Rendering Context**
  - Works natively in both EEVEE and Cycles. The physical separation between the camera and the focus target allows real-time depth of field to calculate accurately.

* **Step D: Animation & Dynamics**
  - **Follow Path Constraint**: Applied to the camera, targeting the Bezier curve. The `offset_factor` is animated linearly from 0.0 to 1.0 to drive the camera along the track.
  - **Track To Constraint**: Applied to the camera, targeting the Focus Empty. The `track_axis` is set to `-Z` (the camera's lens axis) and `up_axis` to `Y`.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Camera Rig Logic | `bpy` object constraints (`FOLLOW_PATH`, `TRACK_TO`) | Native, non-destructive, mathematically precise linking of objects. |
| Path Trajectory | `bpy.ops.curve.primitive_bezier_circle_add` | Provides an instantly smooth, continuous loop for turntable/orbit shots. |
| Focus & DoF | Camera `dof.focus_object` mapping | Keeps the subject sharp automatically as the camera distance changes. |

> **Feasibility Assessment**: 100% of the core functionality of the "AutoCam" rig is reproduced here using native Blender Python. While it doesn't include the UI for "recording" viewport motion, it programmatically generates the exact underlying node/constraint structure the add-on produces, which is much more robust for an automated AI agent.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "CinematicRig",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.0, 0.0, 0.0), # Unused for rig
    **kwargs,
) -> str:
    """
    Create a Procedural Cinematic Tracking Camera Rig.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the rig components.
        location: (x, y, z) world-space position of the focal target.
        scale: Radius of the camera sweep/orbit.
        material_color: Unused for cameras/empties.
        **kwargs: Additional overrides (e.g., frames=250 for loop duration).
        
    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Configuration
    anim_frames = kwargs.get('frames', 250)
    radius = scale * 5.0

    # === Step 1: Create Master Controller ===
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    master_empty = bpy.context.active_object
    master_empty.name = f"{object_name}_Master"
    master_empty.empty_display_size = scale * 0.2

    # === Step 2: Create Focus Target ===
    bpy.ops.object.empty_add(type='SPHERE', location=location)
    target_empty = bpy.context.active_object
    target_empty.name = f"{object_name}_FocusTarget"
    target_empty.empty_display_size = scale * 0.5
    target_empty.parent = master_empty

    # === Step 3: Create Camera Track (Bezier Circle) ===
    bpy.ops.curve.primitive_bezier_circle_add(radius=radius, location=location)
    cam_track = bpy.context.active_object
    cam_track.name = f"{object_name}_Track"
    cam_track.parent = master_empty
    
    # Optional: Tilt the track slightly for a more dynamic orbit
    cam_track.rotation_euler = (0.2, 0.0, 0.0)

    # === Step 4: Create Camera ===
    bpy.ops.object.camera_add(location=location)
    camera = bpy.context.active_object
    camera.name = f"{object_name}_Cam"
    
    # Setup Lens & Depth of Field
    camera.data.lens = 50.0  # 50mm standard focal length
    camera.data.dof.use_dof = True
    camera.data.dof.focus_object = target_empty
    camera.data.dof.aperture_fstop = 2.8
    
    # Set this camera as the active scene camera
    scene.camera = camera

    # === Step 5: Setup Constraints ===
    # 1. Follow Path
    follow_path = camera.constraints.new(type='FOLLOW_PATH')
    follow_path.target = cam_track
    follow_path.use_fixed_position = True # Allows 0.0 - 1.0 offset animation
    follow_path.forward_axis = 'TRACK_NEGATIVE_Z'
    follow_path.up_axis = 'UP_Y'
    
    # 2. Track To
    track_to = camera.constraints.new(type='TRACK_TO')
    track_to.target = target_empty
    track_to.track_axis = 'TRACK_NEGATIVE_Z'
    track_to.up_axis = 'UP_Y'

    # === Step 6: Animate the Camera Sweep ===
    # Keyframe start
    follow_path.offset_factor = 0.0
    follow_path.keyframe_insert(data_path="offset_factor", frame=1)
    
    # Keyframe end
    follow_path.offset_factor = 1.0
    follow_path.keyframe_insert(data_path="offset_factor", frame=anim_frames + 1) # +1 ensures frame 1 and 250 are sequential for perfect loops

    # Ensure linear interpolation for smooth, constant-speed orbit
    if camera.animation_data and camera.animation_data.action:
        for fcurve in camera.animation_data.action.fcurves:
            if fcurve.data_path == "constraints[\"Follow Path\"].offset_factor":
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'LINEAR'
                    
    # Ensure scene length accommodates the animation
    scene.frame_end = max(scene.frame_end, anim_frames)

    return f"Created '{object_name}' rig at {location}. Camera constrained to track, focusing on Target."
```