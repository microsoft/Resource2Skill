# Stylized EEVEE Lighting: Fake Bounce and Terminator Bleed

## Analysis

Here is the extracted skill and reproducible strategy based on the EEVEE lighting tutorial.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized EEVEE Lighting: Fake Bounce and Terminator Bleed

* **Core Visual Mechanism**: This technique uses multiple, strategically configured light objects to fake complex raytracing phenomena in real-time rasterizers (like EEVEE). 
  1. **Terminator Bleed**: By duplicating a main Sun light, offsetting its rotation by just a few degrees, and coloring it a highly saturated warm hue, you create a vibrant band of color at the transition point between light and shadow.
  2. **Fake Global Illumination (GI)**: By placing an upward-pointing Sun or Spot light and completely **disabling its shadows**, the light ignores blocking geometry and illuminates the downward-facing normals (undersides) of objects, perfectly simulating light bouncing off the floor.
* **Why Use This Skill (Rationale)**: EEVEE (prior to raytracing updates) struggles with atmospheric light scattering and lacks real-time global illumination. Relying on default lights leaves shadowed areas pitch black and shadow edges stark. This manual rig instantly injects cinematic warmth, ambient depth, and "golden hour" contrast with zero render-time penalty.
* **Overall Applicability**: Outdoor architectural visualisations, stylized anime/cyberpunk environments, or any real-time scene where you want rich, colorful shadow gradients and believable ground light bounce without baking irradiance volumes.
* **Value Addition**: Transforms flat, game-engine-style lighting into a highly stylized, cinematic composition. The modular rig gives the artist absolute control over the height and intensity of "bounce" light independent of physical rendering constraints.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - An `Empty` object is used as a parent handle to group the lights together, allowing the user to reposition the localized bounce or re-orient the sun rig easily.
* **Step B: Materials & Shading**
  - Not applicable (this is purely a lighting rig). 
* **Step C: Lighting & Rendering Context**
  - **Main Sun**: Standard directional light (e.g., X: 50°, Z: 45°). Casts the primary hard shadows. `use_shadow = True`. Color: `(1.0, 0.9, 0.8)`.
  - **Bleed Sun**: Duplicated Sun light. Rotation is offset from the Main Sun by ~3°. Extremely saturated color: `(1.0, 0.2, 0.0)`. `use_shadow = True`. This creates the fiery sliver of light before the shadow hits.
  - **Global Bounce Sun**: Rotation X: 180° (pointing directly UP). **`use_shadow = False`** (Crucial: prevents it from casting weird upward shadows). Low energy. Color mimics the ground: `(0.8, 0.6, 0.4)`.
  - **Local Bounce Spot**: Pointing UP, `use_shadow = False`. High `spot_blend` (1.0) for soft edges. `use_custom_distance` is enabled to limit the bounce influence exclusively to nearby surfaces (e.g., an awning above a glowing sign).
* **Step D: Animation & Dynamics**
  - Animating the `Z` rotation of the parent Empty allows you to easily change the time-of-day direction while maintaining the exact relative terminator bleed offset.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Terminator color bleed | `bpy.data.lights` (Sun) + Rotational Offset | Offsetting a duplicate sun light forces a secondary shadow map calculation, creating the colored rim where the two shadow edges misalign. |
| Fake GI / Bounce Light | `bpy.data.lights` (Sun/Spot) + `use_shadow=False` | Disabling shadows allows the light to pass through solid geometry and exclusively illuminate faces pointing towards it, perfectly mimicking a ground bounce. |
| Localized limit | `use_custom_distance` | Prevents the fake spot bounce light from infinitely traveling up the Z-axis into the sky. |

> **Feasibility Assessment**: 100% reproduction. The code below programmatically generates the exact multi-light array demonstrated in the tutorial, pre-configured with the correct shadow toggles and angular offsets.

#### 3b. Complete Reproduction Code

```python
def create_stylized_eevee_lighting(
    scene_name: str = "Scene",
    object_name: str = "EEVEE_LightRig",
    location: tuple = (0, 0, 2),
    scale: float = 1.0,
    main_color: tuple = (1.0, 0.9, 0.8),
    main_energy: float = 3.0,
    bleed_color: tuple = (1.0, 0.2, 0.0), 
    bleed_energy: float = 5.0,
    bleed_offset_degrees: float = 3.0,
    bounce_color: tuple = (0.8, 0.6, 0.4), 
    bounce_energy: float = 0.5,
    **kwargs,
) -> str:
    """
    Create a Stylized EEVEE Lighting Rig (Terminator Bleed + Fake Bounce) in the active scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the rig and lights.
        location: (x, y, z) world-space position for the rig parent.
        scale: Influences the custom distance falloff of the local spot bounce.
        main_color: (R, G, B) primary sunlight color.
        main_energy: Intensity of primary sunlight.
        bleed_color: (R, G, B) highly saturated color for the shadow edge.
        bleed_energy: Intensity of the terminator bleed effect.
        bleed_offset_degrees: Angular offset to shift the shadow edge.
        bounce_color: (R, G, B) color of the ground/ambient bounce.
        bounce_energy: Intensity of the global ambient bounce.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    collection = scene.collection

    # === Step 1: Create Rig Parent (Empty) ===
    rig_empty = bpy.data.objects.new(name=object_name, object_data=None)
    rig_empty.empty_display_size = scale * 2.0
    rig_empty.empty_display_type = 'ARROWS'
    rig_empty.location = Vector(location)
    collection.objects.link(rig_empty)

    # Base sunlight angle (e.g., coming from upper-left front)
    base_rot_x = math.radians(50)
    base_rot_y = math.radians(0)
    base_rot_z = math.radians(45)

    # === Step 2: Main Sun Light ===
    main_data = bpy.data.lights.new(name=f"{object_name}_MainSun", type='SUN')
    main_data.color = main_color
    main_data.energy = main_energy
    main_data.use_shadow = True

    main_obj = bpy.data.objects.new(name=f"{object_name}_MainSun", object_data=main_data)
    main_obj.parent = rig_empty
    main_obj.location = (0, 0, 0)
    main_obj.rotation_euler = (base_rot_x, base_rot_y, base_rot_z)
    collection.objects.link(main_obj)

    # === Step 3: Bleed Sun Light (Terminator Effect) ===
    # Offset the rotation slightly to shift the shadow edge and reveal the saturated color
    bleed_data = bpy.data.lights.new(name=f"{object_name}_BleedSun", type='SUN')
    bleed_data.color = bleed_color
    bleed_data.energy = bleed_energy
    bleed_data.use_shadow = True

    bleed_obj = bpy.data.objects.new(name=f"{object_name}_BleedSun", object_data=bleed_data)
    bleed_obj.parent = rig_empty
    bleed_obj.location = (0, 0, 0)
    offset_rad = math.radians(bleed_offset_degrees)
    bleed_obj.rotation_euler = (base_rot_x, base_rot_y + offset_rad, base_rot_z + offset_rad)
    collection.objects.link(bleed_obj)

    # === Step 4: Global Bounce Sun Light (Fake GI) ===
    # Points UP, NO shadows. Uniformly illuminates all downward-facing polygons.
    gbounce_data = bpy.data.lights.new(name=f"{object_name}_GlobalBounce", type='SUN')
    gbounce_data.color = bounce_color
    gbounce_data.energy = bounce_energy
    gbounce_data.use_shadow = False  # CRITICAL: allows light to pass through geometry

    gbounce_obj = bpy.data.objects.new(name=f"{object_name}_GlobalBounce", object_data=gbounce_data)
    gbounce_obj.parent = rig_empty
    gbounce_obj.location = (0, 0, 0)
    gbounce_obj.rotation_euler = (math.radians(180), 0, 0) # 180x = Point straight up
    collection.objects.link(gbounce_obj)

    # === Step 5: Local Bounce Spot Light (Fake localized GI) ===
    # Soft, upward pointing spot with a strict cutoff distance to fake local ground scattering.
    lbounce_data = bpy.data.lights.new(name=f"{object_name}_LocalBounce", type='SPOT')
    lbounce_data.color = bounce_color
    lbounce_data.energy = bounce_energy * 200.0  # Spots need significantly higher wattage than suns
    lbounce_data.use_shadow = False              # CRITICAL for fake bounce
    lbounce_data.spot_blend = 1.0                # Maximum edge softness
    lbounce_data.spot_size = math.radians(120)
    lbounce_data.use_custom_distance = True
    lbounce_data.cutoff_distance = scale * 15.0  # Limit bounce height

    lbounce_obj = bpy.data.objects.new(name=f"{object_name}_LocalBounce", object_data=lbounce_data)
    lbounce_obj.parent = rig_empty
    lbounce_obj.location = (0, 0, -scale * 2.0) # Placed slightly below rig center
    lbounce_obj.rotation_euler = (math.radians(180), 0, 0)
    collection.objects.link(lbounce_obj)

    return f"Created stylized lighting rig '{object_name}' (Main, Bleed, Global Bounce, Local Bounce) at {location}."
```