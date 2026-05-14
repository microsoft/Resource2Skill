# Procedural Cinematic Environment Rig (Atmosphere, Sky & Gobos)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Cinematic Environment Rig (Atmosphere, Sky & Gobos)

* **Core Visual Mechanism**: This technique relies on three interacting elements to create realistic outdoor lighting: 
  1. A physically based procedural sky (replacing flat HDRI setups) positioned at grazing angles.
  2. A global low-density atmospheric volume (Volume Scatter/Principled Volume) to create aerial perspective, light rays, and mood.
  3. "Gobos" (off-camera shadow casters) to intentionally break up overly bright, uniform foregrounds and guide the viewer's eye.

* **Why Use This Skill (Rationale)**: 
  * **Directionality**: Placing the main light source behind or to the side of the camera (never directly behind the camera) reveals the form, silhouette, and texture of 3D objects through shadows.
  * **Atmosphere**: Default Blender scenes exist in a vacuum. Adding a volume bounding box grounds objects and provides realistic depth cueing (distant objects fade into the atmosphere).
  * **Gobos**: Bright foregrounds draw the eye away from the subject. Adding off-screen objects to cast shadows into the foreground acts as a natural vignette, focusing attention on the hero elements of the scene.

* **Overall Applicability**: Essential for any outdoor environment design, architectural exterior visualization, or natural concept art. It bridges the gap between a "3D viewport" look and a "photographic" look.

* **Value Addition**: Instead of manually hunting for external HDRIs and struggling with flat, uninteresting lighting, this procedural rig provides a highly customizable, mathematically accurate outdoor lighting setup with built-in atmosphere and compositional shadow control.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  * **Volume Box**: A simple primitive Cube scaled massively to encompass the entire scene. The viewport display is set to `BOUNDS` so it doesn't obstruct the user's view while working.
  * **Gobo Caster**: A primitive Plane positioned high and off-camera. Instead of complex geometry, it relies on a procedural Alpha mask to cast complex, leafy/dappled shadows.

* **Step B: Materials & Shading**
  * **World Shader**: Uses Blender's native `Nishita Sky Texture` node. This mathematically simulates atmospheric scattering, sun size, and color based purely on elevation and rotation.
  * **Atmosphere Material**: Uses a `Principled Volume` node plugged into the Volume output. Density is kept very low (e.g., `0.01` to `0.05`), and Anisotropy is pushed up (e.g., `0.6` to `0.8`) so light scatters forward towards the camera, mimicking real-world dust/moisture.
  * **Gobo Material**: A `Principled BSDF` with a `Voronoi Texture` running through a high-contrast `ColorRamp`, plugged directly into the `Alpha` socket to create procedural holes for light to shine through.

* **Step C: Lighting & Rendering Context**
  * This setup thrives in **Cycles**. While EEVEE can handle volumes, Cycles is required for the Nishita Sky Texture and accurate volumetric shadow casting from the procedural gobo.
  * The sun elevation dictates the mood: 5°-15° for Golden Hour/Sunset, 30°-60° for a standard sunny day.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Environment Light | World Node Tree (Nishita Sky) | Fully procedural, infinite resolution, physically accurate alternative to external HDRIs. |
| Atmosphere | Mesh Primitive + Principled Volume | Allows precise control over the bounding area of the fog and keeps the setup contained. |
| Foreground Shadows | Mesh Primitive + Alpha Shader | Procedural "Gobo" avoids the need to model complex off-screen trees just to cast shadows. |

> **Feasibility Assessment**: 95% reproduction. The tutorial uses specific photographic HDRIs and image planes which require external files. By substituting these with Blender's procedural Nishita Sky and procedural Alpha Gobos, we achieve the exact same visual principles (directional light, volumes, foreground shadow breaking) in a 100% self-contained, executable script.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "CinematicEnvRig",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 100.0,
    material_color: tuple = (1.0, 1.0, 1.0),
    **kwargs,
) -> str:
    """
    Create a Cinematic Environment Lighting Rig (Sky, Volume, and Gobo).

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the rig components.
        location: Center of the volume bounding box.
        scale: Size of the atmospheric volume box (should cover the scene).
        material_color: Not strictly used for the volume/sky, provided for signature.
        **kwargs: 
            sun_elevation_deg (float): Altitude of the sun (e.g., 10 for sunset, 45 for day).
            sun_rotation_deg (float): Direction of the light.
            volume_density (float): Thickness of the fog.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # Parse kwargs
    sun_elevation = kwargs.get("sun_elevation_deg", 15.0)  # Default Golden Hour
    sun_rotation = kwargs.get("sun_rotation_deg", 120.0)   # Side lighting
    vol_density = kwargs.get("volume_density", 0.02)       # Subtle atmosphere

    # === Step 1: Create Rig Parent Empty ===
    empty_obj = bpy.data.objects.new(object_name, None)
    empty_obj.empty_display_type = 'ARROWS'
    empty_obj.empty_display_size = 2.0
    empty_obj.location = location
    scene.collection.objects.link(empty_obj)

    # === Step 2: Configure World (Nishita Procedural Sky) ===
    world = scene.world
    if not world:
        world = bpy.data.worlds.new(f"{object_name}_World")
        scene.world = world
    
    world.use_nodes = True
    wnodes = world.node_tree.nodes
    wlinks = world.node_tree.links
    wnodes.clear()

    sky_node = wnodes.new("ShaderNodeTexSky")
    sky_node.sky_type = 'NISHITA'
    sky_node.sun_elevation = math.radians(sun_elevation)
    sky_node.sun_rotation = math.radians(sun_rotation)
    sky_node.sun_size = math.radians(1.5)  # Slightly softer shadows
    sky_node.sun_intensity = 1.0
    sky_node.location = (-300, 0)

    bg_node = wnodes.new("ShaderNodeBackground")
    bg_node.location = (0, 0)

    out_node = wnodes.new("ShaderNodeOutputWorld")
    out_node.location = (300, 0)

    wlinks.new(sky_node.outputs['Color'], bg_node.inputs['Color'])
    wlinks.new(bg_node.outputs['Background'], out_node.inputs['Surface'])

    # === Step 3: Create Atmospheric Volume Box ===
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    vol_box = bpy.context.active_object
    vol_box.name = f"{object_name}_VolumeBox"
    vol_box.location = location
    vol_box.scale = (scale, scale, scale * 0.5) # Flatter box
    vol_box.parent = empty_obj
    
    # Set to display as bounds so it doesn't block the viewport
    vol_box.display_type = 'BOUNDS'

    vol_mat = bpy.data.materials.new(name=f"{object_name}_VolumeMat")
    vol_mat.use_nodes = True
    vnodes = vol_mat.node_tree.nodes
    vlinks = vol_mat.node_tree.links
    vnodes.clear()

    prin_vol = vnodes.new("ShaderNodeVolumePrincipled")
    prin_vol.inputs['Density'].default_value = vol_density
    prin_vol.inputs['Anisotropy'].default_value = 0.65  # Forward scattering
    prin_vol.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
    
    vol_out = vnodes.new("ShaderNodeOutputMaterial")
    
    vlinks.new(prin_vol.outputs['Volume'], vol_out.inputs['Volume'])
    vol_box.data.materials.append(vol_mat)

    # === Step 4: Create Procedural Foreground Gobo ===
    bpy.ops.mesh.primitive_plane_add(size=1.0)
    gobo = bpy.context.active_object
    gobo.name = f"{object_name}_Gobo"
    gobo.scale = (scale * 0.5, scale * 0.5, 1.0)
    gobo.parent = empty_obj
    
    # Position overhead to cast shadows down into the scene
    gobo.location = (location[0], location[1], location[2] + (scale * 0.4))
    
    gobo_mat = bpy.data.materials.new(name=f"{object_name}_GoboMat")
    gobo_mat.use_nodes = True
    gobo_mat.blend_method = 'CLIP' # For EEVEE alpha viewing
    gobo_mat.shadow_method = 'CLIP'
    gnodes = gobo_mat.node_tree.nodes
    glinks = gobo_mat.node_tree.links
    
    g_bsdf = gnodes.get("Principled BSDF")
    g_bsdf.inputs['Base Color'].default_value = (0.0, 0.0, 0.0, 1.0)
    
    g_voronoi = gnodes.new("ShaderNodeTexVoronoi")
    g_voronoi.inputs['Scale'].default_value = 5.0
    g_voronoi.location = (-600, 0)
    
    g_ramp = gnodes.new("ShaderNodeValToRGB")
    g_ramp.color_ramp.elements[0].position = 0.35
    g_ramp.color_ramp.elements[1].position = 0.40
    g_ramp.location = (-300, 0)
    
    glinks.new(g_voronoi.outputs['Distance'], g_ramp.inputs['Fac'])
    glinks.new(g_ramp.outputs['Color'], g_bsdf.inputs['Alpha'])
    
    gobo.data.materials.append(gobo_mat)

    return f"Created '{object_name}' Lighting Rig (Sky, Volume, Gobo) at {location}. Switch to Rendered view (Cycles recommended) to see effect."
```