# Realistic Day & Night Interior Lighting Rig

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Realistic Day & Night Interior Lighting Rig

* **Core Visual Mechanism**: Physically accurate illumination achieved by pairing the procedural `Nishita Sky Texture` with matching Sun lamps for daylight, and utilizing `Blackbody` shader nodes on Area and Spot lights to drive realistic color temperatures (Kelvin) for nighttime interior lighting.
* **Why Use This Skill (Rationale)**: Instead of arbitrarily guessing light colors using the RGB picker, relying on Kelvin temperatures (e.g., 3200K for warm cove lighting) and real-world sun elevation angles guarantees photorealistic light interaction, predictable bounce lighting, and cinematic contrast. Increasing the sun's angular diameter softens shadow edges naturally, mirroring atmospheric scattering.
* **Overall Applicability**: Essential for architectural visualization, interior renders, and setting up rapid mood lighting (golden hour vs. deep night) for any enclosed environment or room set.
* **Value Addition**: Transforms a flatly lit scene into a highly dimensional, realistic environment. It provides a parametric toggle between day and night without needing complex HDRI swapping, all while maintaining perfect color theory through physical temperatures.

### 2. Technical Breakdown

* **Step A: Daylight Configuration (World & Sun)**
  - **Environment**: `ShaderNodeTexSky` set to `NISHITA`.
  - **Sun Sync**: A discrete `SUN` light is instantiated and its X/Z rotations are mathematically mapped to match the Nishita Sky's `Elevation` and `Rotation`.
  - **Shadow Softness**: The Sun light's `Angle` (size) is increased to ~3-5 degrees to cast natural, softly diffused shadows through windows.
  - **Intensity Control**: Sun intensity is slightly reduced to prevent floor textures from burning out (overexposing).

* **Step B: Nighttime Configuration (Blackbody Nodes)**
  - **Environment**: Sky elevation is set to a negative value (e.g., -5°) to simulate dusk/night, darkening the procedural sky.
  - **Cove/Hidden Lighting**: Long, thin `RECTANGLE` Area lights placed near walls/ceilings, driven by a `ShaderNodeBlackbody` set to a warm ~3200K.
  - **Downlights**: While the tutorial uses external IES textures, this can be procedurally approximated using `SPOT` lights with a tight cone angle (60°), high blend (0.8), and driven by a 3000K Blackbody node.

* **Step C: Rendering Context**
  - **Engine**: **Cycles** is highly recommended. While EEVEE supports some of these features, Cycles correctly computes the bounced GI from the Nishita sky and the accurate physical falloff of the Blackbody node.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Environment Sky | `ShaderNodeTexSky` (Nishita) | Built-in procedural, physically accurate atmospheric scattering. |
| Daylight | `SUN` light | Syncs with sky; allows precise control over shadow softness via Angle. |
| Night Color | `ShaderNodeBlackbody` | Maps exact Kelvin values to RGB for photorealistic artificial light colors. |
| IES Downlights | `SPOT` light fallback | Because external `.ies` files cannot be dynamically loaded by the agent, Spot lights mimic the physical cone. |

> **Feasibility Assessment**: 95% reproduction. The overall lighting mood, physics, and node setups are perfectly recreated. The only missing element is the specific throw-pattern of an external IES file, which is gracefully substituted with high-blend Spot lights.

#### 3b. Complete Reproduction Code

```python
def create_realistic_lighting_rig(
    scene_name: str = "Scene",
    rig_name: str = "InteriorLightingRig",
    location: tuple = (0, 0, 0),
    time_of_day: str = "DAY",  # Accepts "DAY" or "NIGHT"
    sun_elevation: float = 25.0,  # Degrees (used if DAY)
    sun_rotation: float = 45.0,  # Degrees (used if DAY)
    cove_light_temp: float = 3200.0,  # Kelvin
    spot_light_temp: float = 3000.0,  # Kelvin
    **kwargs
) -> str:
    """
    Create a Realistic Day/Night Interior Lighting Rig.

    Args:
        scene_name: Name of the target scene.
        rig_name: Base name for the rig components.
        location: (x, y, z) base location for the rig empty.
        time_of_day: "DAY" for sunlight, "NIGHT" for dark sky and artificial lights.
        sun_elevation: Angle of the sun above the horizon.
        sun_rotation: Azimuth angle of the sun.
        cove_light_temp: Blackbody temperature for hidden area lights.
        spot_light_temp: Blackbody temperature for ceiling downlights.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Recommend Cycles for physically accurate lighting
    if scene.render.engine != 'CYCLES':
        scene.render.engine = 'CYCLES'

    # === Step 1: World Environment Setup ===
    world = scene.world
    if not world:
        world = bpy.data.worlds.new(f"{rig_name}_World")
        scene.world = world

    world.use_nodes = True
    tree = world.node_tree
    tree.nodes.clear()

    bg_node = tree.nodes.new(type='ShaderNodeBackground')
    bg_node.location = (0, 0)
    out_node = tree.nodes.new(type='ShaderNodeOutputWorld')
    out_node.location = (200, 0)
    
    # Procedural Nishita Sky
    sky_node = tree.nodes.new(type='ShaderNodeTexSky')
    sky_node.location = (-200, 0)
    sky_node.sky_type = 'NISHITA'

    tree.links.new(sky_node.outputs['Color'], bg_node.inputs['Color'])
    tree.links.new(bg_node.outputs['Background'], out_node.inputs['Surface'])

    # === Step 2: Rig Root ===
    root_obj = bpy.data.objects.new(rig_name, None)
    root_obj.location = Vector(location)
    scene.collection.objects.link(root_obj)

    # === Step 3: Populate Lights based on Time of Day ===
    if time_of_day.upper() == "DAY":
        # Setup Sky
        sky_node.sun_elevation = math.radians(sun_elevation)
        sky_node.sun_rotation = math.radians(sun_rotation)
        sky_node.sun_intensity = 0.5  # Prevents floor blowout

        # Add Sun
        sun_data = bpy.data.lights.new(name=f"{rig_name}_Sun", type='SUN')
        sun_data.energy = 2.0
        sun_data.angle = math.radians(5.0)  # ~5 degrees for soft shadows
        
        sun_obj = bpy.data.objects.new(name=f"{rig_name}_Sun", object_data=sun_data)
        sun_obj.parent = root_obj
        
        # Orient Sun object to match Nishita angles
        rot_x = math.radians(90 - sun_elevation)
        rot_z = math.radians(sun_rotation)
        sun_obj.rotation_euler = (rot_x, 0, rot_z)
        
        scene.collection.objects.link(sun_obj)
        return f"Created Day Lighting Rig '{rig_name}' at {location}."

    else:
        # Night mode: Darken the sky
        sky_node.sun_elevation = math.radians(-5.0) # Sun below horizon
        sky_node.sun_intensity = 0.05

        # 1. Cove Light (Hidden Area Light)
        cove_data = bpy.data.lights.new(name=f"{rig_name}_Cove", type='AREA')
        cove_data.shape = 'RECTANGLE'
        cove_data.size = 4.0
        cove_data.size_y = 0.2
        cove_data.energy = 150.0
        cove_data.use_nodes = True
        
        # Map Blackbody to Emission color
        cove_tree = cove_data.node_tree
        for node in cove_tree.nodes:
            if node.type == 'EMISSION':
                bb_cove = cove_tree.nodes.new(type='ShaderNodeBlackbody')
                bb_cove.inputs['Temperature'].default_value = cove_light_temp
                cove_tree.links.new(bb_cove.outputs['Color'], node.inputs['Color'])
                break
            
        cove_obj = bpy.data.objects.new(name=f"{rig_name}_Cove", object_data=cove_data)
        cove_obj.parent = root_obj
        cove_obj.location = (0, 2, 2.8)
        cove_obj.rotation_euler = (math.radians(-90), 0, 0) # Cast sideways/down
        scene.collection.objects.link(cove_obj)

        # 2. Downlights (Simulated IES using Spots)
        spot_spacing = 1.5
        for i in range(-1, 2):
            spot_name = f"{rig_name}_Spot_{i+2}"
            spot_data = bpy.data.lights.new(name=spot_name, type='SPOT')
            spot_data.energy = 200.0
            spot_data.spot_size = math.radians(60.0)
            spot_data.spot_blend = 0.8
            spot_data.use_nodes = True
            
            spot_tree = spot_data.node_tree
            for node in spot_tree.nodes:
                if node.type == 'EMISSION':
                    bb_spot = spot_tree.nodes.new(type='ShaderNodeBlackbody')
                    bb_spot.inputs['Temperature'].default_value = spot_light_temp
                    spot_tree.links.new(bb_spot.outputs['Color'], node.inputs['Color'])
                    break
                
            spot_obj = bpy.data.objects.new(name=spot_name, object_data=spot_data)
            spot_obj.parent = root_obj
            spot_obj.location = (i * spot_spacing, 0, 3.0) # Positioned on hypothetical ceiling
            spot_obj.rotation_euler = (0, 0, 0) # Point straight down
            scene.collection.objects.link(spot_obj)
            
        # 3. Soft Ambient Fill Light
        fill_data = bpy.data.lights.new(name=f"{rig_name}_Fill", type='AREA')
        fill_data.shape = 'RECTANGLE'
        fill_data.size = 5.0
        fill_data.size_y = 5.0
        fill_data.energy = 10.0
        fill_data.use_nodes = True
        
        fill_tree = fill_data.node_tree
        for node in fill_tree.nodes:
            if node.type == 'EMISSION':
                bb_fill = fill_tree.nodes.new(type='ShaderNodeBlackbody')
                bb_fill.inputs['Temperature'].default_value = 4000.0 # Slightly cooler fill
                fill_tree.links.new(bb_fill.outputs['Color'], node.inputs['Color'])
                break
                
        fill_obj = bpy.data.objects.new(name=f"{rig_name}_Fill", object_data=fill_data)
        fill_obj.parent = root_obj
        fill_obj.location = (0, -2, 1.5)
        fill_obj.rotation_euler = (math.radians(90), 0, 0)
        scene.collection.objects.link(fill_obj)

        return f"Created Night Lighting Rig '{rig_name}' at {location} with Cove, Spot, and Fill lights."
```