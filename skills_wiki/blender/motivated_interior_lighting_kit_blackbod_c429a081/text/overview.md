# Motivated Interior Lighting Kit (Blackbody & Mixed Types)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Motivated Interior Lighting Kit (Blackbody & Mixed Types)

* **Core Visual Mechanism**: This technique relies on layering different physical light types (Spot, Area, Point) and driving their color output procedurally using a **Blackbody** shader node. This accurately simulates real-world color temperatures (Kelvin) instead of relying on arbitrary RGB values. The lighting is "motivated," meaning the light source types and shapes correspond to implied physical fixtures (e.g., a wide rectangle area light for a computer screen, a spotlight for a ceiling can, a point light for an alarm).
* **Why Use This Skill (Rationale)**: Guessing warm or cool colors using the color wheel often leads to muddy, unnatural lighting. The Blackbody node mathematically outputs the correct spectrum for incandescent (warm, ~3000K), fluorescent (neutral, ~4500K), or daylight (cool, ~6500K) sources. Furthermore, mixing light types leverages their specific falloff and shaping capabilities (like the `Blend` parameter on Spotlights to soften edges) to create depth and contrast.
* **Overall Applicability**: Essential for interior architectural visualization, sci-fi corridors, cockpits, and any scene where light needs to feel physically grounded and localized.
* **Value Addition**: Transforms a flatly lit environment into a moody, cinematic scene. It separates the visual look of a light (handled by low-cost Emission materials on geometry) from the actual illumination calculations (handled by optimized Area/Point lights), yielding better render performance and higher quality shadows.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - Lights do not require geometry, but they require *motivated* placement.
  - A small piece of "practical" geometry (e.g., a cylinder acting as a bulb) is often placed exactly at the Point light location to give the eye a physical source to look at.
* **Step B: Materials & Shading**
  - **Light Nodes**: By enabling `Use Nodes` on the Light Data, you can pass a `Blackbody` node into the `Emission` node.
  - **Temperatures used**: 4500K for neutral overhead spots; 6000K for cool screen glows.
  - **Practical Mesh Material**: A pure `Emission` shader node matching the color of the local point light (e.g., Red for an alarm) at a high strength (e.g., 5.0) to appear blown out/glowing to the camera.
* **Step C: Lighting & Rendering Context**
  - **Spotlight**: Features a high `Blend` value (1.0) to completely soften the edges of the cone, preventing harsh theatrical circles on the floor.
  - **Area Light**: Changed from Square to `Rectangle` (e.g., 3m x 0.5m) to simulate long fluorescent tubes or wide control panels.
  - **Point Light**: Features a very small `Radius` / `Shadow Soft Size` (e.g., 0.05m) to create harder, crisper shadows typical of small exposed bulbs.
  - **Color Management**: Switching the Render View Transform Look from "None" to "High Contrast" immediately deepens shadows and pops highlights, which is critical for cinematic interiors.
* **Step D: Animation & Dynamics**
  - (Optional but noted in tutorial): Point lights can be paired with IES textures (using the `IES Texture` node plugged into the light's emission strength) to cast realistic, real-world manufacturer light patterns on adjacent walls.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Light Data Creation | `bpy.data.lights.new()` | Bypasses context/selection issues of `bpy.ops`, allowing precise programmatic placement. |
| Accurate Light Colors | `ShaderNodeBlackbody` via Light Nodes | Provides physically accurate Kelvin temperatures instead of manual RGB tweaking. |
| Motivated Geometry | `bpy.ops.mesh.primitive_cylinder_add` + `ShaderNodeEmission` | Provides a visible physical source for the camera to look at, separating the "look" from the "lighting". |
| Cinematic Punch | `scene.view_settings.look = 'High Contrast'` | Instantly maps the linear render output to a cinematic curve. |

> **Feasibility Assessment**: 100% of the core lighting setup, hierarchy, and node structures described in the tutorial are reproducible procedurally. (Note: External IES textures and image Gobos are omitted to keep the code self-contained and purely procedural).

#### 3b. Complete Reproduction Code

```python
def create_motivated_interior_lighting(
    scene_name: str = "Scene",
    kit_name: str = "Motivated_Light_Kit",
    location: tuple = (0, 0, 0),
    scale: float = 1.0, # Scales relative positions
    key_temperature: float = 4500.0,  # Neutral/Warm overhead
    fill_temperature: float = 6500.0, # Cool screen/window fill
    alarm_color: tuple = (1.0, 0.02, 0.0) # RGB for emergency light
) -> str:
    """
    Creates an interior lighting kit utilizing Spot, Area, and Point lights 
    driven by procedural Blackbody temperature nodes for physical accuracy.
    
    Args:
        scene_name: Name of the target scene.
        kit_name: Base name for the generated objects.
        location: (x, y, z) world-space base position for the kit.
        scale: Spacing multiplier for the light arrangement.
        key_temperature: Kelvin temperature for the overhead spotlight.
        fill_temperature: Kelvin temperature for the area light.
        alarm_color: RGB tuple for the local practical point light.
        
    Returns:
        Status string detailing the created lighting setup.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    base_loc = Vector(location)
    
    # Create a collection to keep the scene organized
    kit_collection = bpy.data.collections.new(kit_name)
    scene.collection.children.link(kit_collection)

    # --- Helper Function: Create Light with Node Setup ---
    def add_physical_light(name, l_type, rel_loc, rot_euler, energy, temp=None, color=None):
        # Create Data and Object
        light_data = bpy.data.lights.new(name=name + "_Data", type=l_type)
        light_data.energy = energy
        light_obj = bpy.data.objects.new(name=name, object_data=light_data)
        kit_collection.objects.link(light_obj)
        
        # Transform
        light_obj.location = base_loc + (Vector(rel_loc) * scale)
        light_obj.rotation_euler = rot_euler
        
        # Setup Nodes (Blackbody or RGB)
        light_data.use_nodes = True
        tree = light_data.node_tree
        nodes = tree.nodes
        links = tree.links
        
        # Clear default nodes safely
        for n in nodes:
            nodes.remove(n)
            
        out_node = nodes.new('ShaderNodeOutputLight')
        out_node.location = (300, 0)
        
        em_node = nodes.new('ShaderNodeEmission')
        em_node.location = (100, 0)
        links.new(em_node.outputs['Emission'], out_node.inputs['Surface'])
        
        if temp is not None:
            bb_node = nodes.new('ShaderNodeBlackbody')
            bb_node.location = (-100, 0)
            bb_node.inputs['Temperature'].default_value = temp
            links.new(bb_node.outputs['Color'], em_node.inputs['Color'])
        elif color is not None:
            em_node.inputs['Color'].default_value = (*color, 1.0)
            
        return light_obj, light_data

    # === 1. Overhead Motivated Key (Spotlight) ===
    # Points straight down, high blend for soft edges
    spot_obj, spot_data = add_physical_light(
        name=f"{kit_name}_Overhead_Spot",
        l_type='SPOT',
        rel_loc=(0, 0, 3),
        rot_euler=(0, 0, 0), # Points down -Z
        energy=1500.0 * scale,
        temp=key_temperature
    )
    spot_data.spot_size = math.radians(75)
    spot_data.spot_blend = 1.0 # 100% softened edge
    spot_data.shadow_soft_size = 0.25 # Soft shadows

    # === 2. Screen/Panel Motivated Fill (Area Light) ===
    # Rectangular, points +Y into the room
    area_obj, area_data = add_physical_light(
        name=f"{kit_name}_Screen_Area",
        l_type='AREA',
        rel_loc=(0, -2, 1.5),
        rot_euler=(math.pi/2, 0, 0), 
        energy=800.0 * scale,
        temp=fill_temperature
    )
    area_data.shape = 'RECTANGLE'
    area_data.size = 3.0 * scale
    area_data.size_y = 0.5 * scale

    # === 3. Alarm/Practical (Point Light) ===
    # Small radius for hard shadows, colored RGB
    point_loc = (2.0, 0, 2.0)
    point_obj, point_data = add_physical_light(
        name=f"{kit_name}_Alarm_Point",
        l_type='POINT',
        rel_loc=point_loc,
        rot_euler=(0, 0, 0),
        energy=200.0 * scale,
        color=alarm_color
    )
    point_data.shadow_soft_size = 0.05 * scale # Crisp shadows for small bulb

    # === 4. Motivating Geometry for the Alarm ===
    # A physical object with an emission shader to represent the bulb
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16, 
        radius=0.1 * scale, 
        depth=0.15 * scale,
        location=base_loc + (Vector(point_loc) * scale),
        rotation=(math.pi/2, 0, 0)
    )
    bulb_obj = bpy.context.active_object
    bulb_obj.name = f"{kit_name}_Alarm_Fixture"
    
    # Move from default collection to kit collection
    for coll in bulb_obj.users_collection:
        coll.objects.unlink(bulb_obj)
    kit_collection.objects.link(bulb_obj)

    # Pure Emission Material for the bulb
    mat = bpy.data.materials.new(name=f"{kit_name}_Alarm_Mat")
    mat.use_nodes = True
    mnodes = mat.node_tree.nodes
    for n in mnodes:
        mnodes.remove(n)
    
    m_out = mnodes.new('ShaderNodeOutputMaterial')
    m_em = mnodes.new('ShaderNodeEmission')
    m_em.inputs['Color'].default_value = (*alarm_color, 1.0)
    m_em.inputs['Strength'].default_value = 10.0 # Blown out visually
    mat.node_tree.links.new(m_em.outputs['Emission'], m_out.inputs['Surface'])
    
    bulb_obj.data.materials.append(mat)

    # === 5. Scene Rendering Context ===
    # Set to High Contrast for cinematic falloff as recommended in tutorial
    scene.view_settings.look = 'High Contrast'

    return f"Created '{kit_name}' at {location}. Includes: Soft Spot ({key_temperature}K), Rectangular Area ({fill_temperature}K), and Point light with physical fixture."
```