# Parametric Three-Point Studio Lighting

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Parametric Three-Point Studio Lighting

* **Core Visual Mechanism**: This pattern establishes a classic three-point lighting setup (Key, Fill, Rim) using Area Lights. It utilizes physically accurate inverse-square energy scaling, `Track To` constraints for perfect subject targeting, and cinematic color temperature contrast (warm key light, cool fill/rim lights) to wrap light around an object and separate it from the background.
* **Why Use This Skill (Rationale)**: Default primitive lighting in 3D scenes is often flat and lifeless. As explained in the tutorial, a proper lighting setup conveys depth, highlights the object's silhouette, and establishes mood. Using warm colors in the front and cool colors in the back creates the classic "Hollywood blockbuster" look, adding immediate professional polish to any raw 3D model.
* **Overall Applicability**: Absolutely essential for product rendering, character showcases, and portfolio turntables. This skill acts as a drop-in "studio environment" for any focal object in a scene.
* **Value Addition**: Transforms a flatly-lit graybox scene into a cinematic render by introducing dynamic range, controlled shadows, and chromatic contrast without needing complex HDRI environments.

### 2. Technical Breakdown

* **Step A: Geometry & Tracking**
  - Creates an `Empty` object (displayed as a CROSS) to act as the central focal point.
  - All lights are spawned at calculated offset vectors and use a `TRACK_TO` constraint pointing at the Empty. This allows the lights to automatically stay focused even if the scale or location changes.

* **Step B: Materials & Shading (Light Properties)**
  - **Key Light**: Warm color, high energy, medium size for soft but defined shadows.
  - **Fill Light**: Cool color (e.g., light blue), 40-50% energy of the Key, larger size to cast very soft, diffuse light that lifts the black levels in the shadows.
  - **Rim/Back Light**: Cool color, extremely high energy, smaller size for a harder, sharp highlight along the silhouette.

* **Step C: Lighting & Rendering Context**
  - Uses `AREA` lights which are highly recommended in the tutorial for their realistic falloff and soft edge properties.
  - Light energy automatically scales with the square of the `scale` parameter (Inverse Square Law) to maintain consistent exposure regardless of how far away the lights are placed.
  - Works exceptionally well in both EEVEE and Cycles.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Light Targeting | `TRACK_TO` Constraints | Keeps lights perfectly aimed at the subject regardless of placement or scale. |
| Illumination Type | `AREA` Lights | Provides physically realistic, soft shadows critical for professional studio setups. |
| Intensity Scaling | Math (`scale ** 2`) | Ensures the lights don't blow out or under-expose the subject when the rig is scaled up or down. |

> **Feasibility Assessment**: 100% reproduction of the core lighting principles taught in the tutorial. The script fully automates the manual placement, constraint setup, and balancing of Key, Fill, and Rim lights.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "StudioLightSetup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (1.0, 0.9, 0.8), # Used as the Warm Key Light Color
    **kwargs,
) -> str:
    """
    Create Parametric Three-Point Studio Lighting in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created lighting objects.
        location: (x, y, z) world-space position of the focal target.
        scale: Distance multiplier for the lights (Energy scales automatically).
        material_color: (R, G, B) color of the main Key Light.
        **kwargs: Additional overrides for fill/rim ratios and colors.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # Lighting Parameters
    base_distance = 5.0 * scale
    
    # Energy scales with the square of the distance (Inverse Square Law)
    key_energy = kwargs.get('key_energy', 1000.0 * (scale ** 2)) 
    fill_ratio = kwargs.get('fill_ratio', 0.4) # Fill is 40% as bright as Key
    fill_color = kwargs.get('fill_color', (0.8, 0.9, 1.0)) # Cool Cyan/Blue
    rim_energy = kwargs.get('rim_energy', 2000.0 * (scale ** 2)) # Rim is hottest
    rim_color = kwargs.get('rim_color', (0.7, 0.8, 1.0)) # Cool Blue
    
    # 1. Create target empty for lights to track
    target_obj = bpy.data.objects.new(f"{object_name}_Target", None)
    target_obj.location = Vector(location)
    target_obj.empty_display_type = 'CROSS'
    target_obj.empty_display_size = scale
    scene.collection.objects.link(target_obj)

    # Helper function to create, position, and aim lights
    def add_light(name, location_offset, energy, color, size):
        # Create light data
        light_data = bpy.data.lights.new(name=f"{name}_Data", type='AREA')
        light_data.energy = energy
        light_data.color = color
        light_data.size = size
        light_data.shape = 'SQUARE'

        # Create light object
        light_obj = bpy.data.objects.new(name, light_data)
        scene.collection.objects.link(light_obj)
        
        # Position in world space relative to the target
        light_obj.location = target_obj.location + Vector(location_offset)
        
        # Add Track To constraint pointing at the target Empty
        track = light_obj.constraints.new(type='TRACK_TO')
        track.target = target_obj
        track.track_axis = 'TRACK_NEGATIVE_Z'
        track.up_axis = 'UP_Y'
        
        return light_obj

    # === Step 2: Spawn Lights ===
    
    # Key Light (Front-Right, High, Warm, Medium softness)
    key_offset = (base_distance * 0.7, -base_distance * 0.8, base_distance * 0.7)
    add_light(
        name=f"{object_name}_Key", 
        location_offset=key_offset, 
        energy=key_energy, 
        color=material_color, 
        size=base_distance * 0.5
    )

    # Fill Light (Front-Left, Lower, Cool, Maximum softness)
    fill_offset = (-base_distance * 0.8, -base_distance * 0.5, base_distance * 0.3)
    add_light(
        name=f"{object_name}_Fill", 
        location_offset=fill_offset, 
        energy=key_energy * fill_ratio, 
        color=fill_color, 
        size=base_distance * 0.8
    )

    # Rim Light (Back-Left, High, Cool, Harder shadows for sharp silhouette)
    rim_offset = (-base_distance * 0.4, base_distance * 0.9, base_distance * 0.6)
    add_light(
        name=f"{object_name}_Rim", 
        location_offset=rim_offset, 
        energy=rim_energy, 
        color=rim_color, 
        size=base_distance * 0.2
    )

    return f"Created Three-Point Lighting setup '{object_name}' focused at {location} (Scale: {scale})."
```