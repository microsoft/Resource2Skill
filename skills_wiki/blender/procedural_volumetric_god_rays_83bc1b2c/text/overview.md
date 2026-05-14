# Procedural Volumetric God Rays

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Volumetric God Rays

* **Core Visual Mechanism**: The defining signature of this technique is the generation of "crepuscular rays" (god rays) using physically accurate volumetric scattering. A highly directional, low-angle light source (Nishita Sky Texture sun) is partially blocked by floating geometric occluders. A bounding box filled with a `Volume Scatter` shader captures these light paths, with a high Anisotropy value (0.9) forcing the light to scatter forward toward the camera, producing intensely visible, cinematic light shafts.

* **Why Use This Skill (Rationale)**: Volumetric lighting adds immense depth, scale, and atmosphere to a 3D environment. Instead of relying on 2D post-processing, this technique uses physical light simulation. By scattering light dynamically around occluding objects, it grounds the composition and instantly establishes mood (e.g., misty mornings, dusty attics, or cinematic sci-fi reveals). 

* **Overall Applicability**: Essential for dramatic environment design, architectural visualization (sun streaming through windows), establishing establishing shots for animations, and creating "hero" lighting for product/character showcases.

* **Value Addition**: Transforms a flat, default scene into a moody, atmospheric environment by introducing physical air density and dynamic shadow casting through 3D space.

---

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Focal Object:** A basic primitive (Cube) sitting on a floor plane.
  - **Occluders:** A cluster of small, randomly rotated and scattered cubes suspended in the air. These act as the "leaves" or "window frames" that break up the light and cast the volumetric shadows.
  - **Volume Domain:** A heavily scaled-up bounding box that completely encapsulates the floor, subjects, and occluders. Set to display as `Bounds` in the viewport to maintain visibility.

* **Step B: Materials & Shading**
  - **Volume Material:** Attached to the large Volume Domain box. The Principled BSDF is completely removed.
  - **Shader:** `Volume Scatter` node plugged directly into the `Volume` socket of the Material Output.
  - **Parameters:** Density is set to `0.1` (thick enough to catch light, thin enough to see through). Anisotropy is pushed to `0.9` (highly forward-scattering, meaning light rays beam strongly in the direction the light is traveling).

* **Step C: Lighting & Rendering Context**
  - **Engine:** Must be **Cycles**. EEVEE handles volumes differently and requires specific shadow settings, whereas Cycles traces the physical light paths required for accurate god rays out of the box.
  - **World Environment:** `Nishita Sky Texture` plugged into the background. `Sun Elevation` is set extremely low (`5.0` degrees) to cast long, raking shadows through the occluders.
  - **Color Management:** Scene Film Exposure is dropped to `0.1` to compensate for the extreme brightness of the physical sky model, maintaining contrast between the dark shadows and the bright rays.

* **Step D: Animation & Dynamics**
  - The volumetric rays will dynamically shift in real-time if the occluders or the sun elevation/rotation are animated.

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Scene Geometry | `bpy.ops.mesh.primitive` + Python `random` | Clean instantiation and procedural clustering of occluders mimics the tutorial's manual "proportional editing" scatter. |
| Volumetric Medium | Shader node tree (Material) | Direct programmatic control over the `Volume Scatter` node's Density and Anisotropy. |
| Lighting setup | Shader node tree (World) | Procedural instantiation of the Nishita Sky Texture allows us to mathematically set the exact sun angle required for the rays. |

> **Feasibility Assessment**: 100%. The code faithfully reproduces the lighting model, the volumetric scattering domain, and the procedural scattering of occluders to generate the god rays exactly as demonstrated.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "VolumetricGodRays",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.8, 0.8),
    **kwargs,
) -> str:
    """
    Create Procedural Volumetric God Rays in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created setup.
        location: (x, y, z) world-space origin position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the volume scatter.
        **kwargs: Overrides for volume_density, volume_anisotropy, sun_elevation.

    Returns:
        Status string.
    """
    import bpy
    import math
    import random
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Force object mode if needed
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # === Engine Setup ===
    # Cycles is required for accurate volumetric light scattering
    scene.render.engine = 'CYCLES'
    scene.view_settings.exposure = 0.1  # Darken global exposure to make rays pop

    # === Step 1: Create Base Geometry ===
    loc = Vector(location)
    
    # Create an empty as the master parent
    root_empty = bpy.data.objects.new(object_name, None)
    root_empty.location = loc
    bpy.context.collection.objects.link(root_empty)

    # Floor plane
    bpy.ops.mesh.primitive_plane_add(size=40*scale, location=loc)
    floor = bpy.context.active_object
    floor.name = f"{object_name}_Floor"
    floor.parent = root_empty

    # Main Subject Cube (Focal point)
    bpy.ops.mesh.primitive_cube_add(size=2*scale, location=loc + Vector((0, 0, 1*scale)))
    main_cube = bpy.context.active_object
    main_cube.name = f"{object_name}_Subject"
    main_cube.parent = root_empty

    # Occluders (Scattered cubes to break up light and cast shadows)
    random.seed(42)  # Fixed seed for reproducible scattering
    for i in range(35):
        # Cluster them higher up in the air
        pos_offset = Vector((
            random.uniform(-6, 6) * scale,
            random.uniform(-6, 6) * scale,
            random.uniform(4, 10) * scale
        ))
        bpy.ops.mesh.primitive_cube_add(
            size=random.uniform(0.2, 0.8) * scale, 
            location=loc + pos_offset
        )
        occ = bpy.context.active_object
        occ.name = f"{object_name}_Occluder_{i}"
        occ.rotation_euler = (
            random.uniform(0, 3.14), 
            random.uniform(0, 3.14), 
            random.uniform(0, 3.14)
        )
        occ.parent = root_empty

    # Volume Domain (Large box enclosing everything)
    bpy.ops.mesh.primitive_cube_add(size=40*scale, location=loc + Vector((0, 0, 15*scale)))
    vol_cube = bpy.context.active_object
    vol_cube.name = f"{object_name}_VolumeDomain"
    vol_cube.parent = root_empty
    vol_cube.display_type = 'BOUNDS'  # Do not block viewport visibility

    # === Step 2: Build Volume Material ===
    vol_mat = bpy.data.materials.new(name=f"{object_name}_VolMat")
    vol_mat.use_nodes = True
    v_nodes = vol_mat.node_tree.nodes
    v_links = vol_mat.node_tree.links

    # Clear default Surface node setup
    for n in v_nodes:
        v_nodes.remove(n)

    # Create Volume Shader
    v_out = v_nodes.new(type='ShaderNodeOutputMaterial')
    v_out.location = (300, 0)
    
    v_scatter = v_nodes.new(type='ShaderNodeVolumeScatter')
    v_scatter.location = (0, 0)
    v_scatter.inputs['Density'].default_value = kwargs.get('volume_density', 0.1)
    v_scatter.inputs['Anisotropy'].default_value = kwargs.get('volume_anisotropy', 0.9)
    v_scatter.inputs['Color'].default_value = (material_color[0], material_color[1], material_color[2], 1.0)

    # Plug into Volume, NOT Surface
    v_links.new(v_scatter.outputs['Volume'], v_out.inputs['Volume'])
    vol_cube.data.materials.append(vol_mat)

    # === Step 3: Setup World Lighting (Sky Texture) ===
    # Create a new world additively so we don't destroy existing user worlds
    new_world = bpy.data.worlds.new(f"{object_name}_SkyWorld")
    scene.world = new_world
    new_world.use_nodes = True
    w_nodes = new_world.node_tree.nodes
    w_links = new_world.node_tree.links

    w_out = w_nodes.get("World Output")
    if not w_out:
        w_out = w_nodes.new(type='ShaderNodeOutputWorld')
    
    w_bg = w_nodes.get("Background")
    if not w_bg:
        w_bg = w_nodes.new(type='ShaderNodeBackground')

    w_sky = w_nodes.new(type='ShaderNodeTexSky')
    w_sky.sky_type = 'NISHITA'
    # Extremely low sun elevation (5 degrees) for long, raking crepuscular rays
    w_sky.sun_elevation = math.radians(kwargs.get('sun_elevation', 5.0))
    w_sky.sun_rotation = math.radians(kwargs.get('sun_rotation', 135.0))

    w_links.new(w_sky.outputs['Color'], w_bg.inputs['Color'])
    w_links.new(w_bg.outputs['Background'], w_out.inputs['Surface'])

    # === Step 4: Finalize ===
    bpy.ops.object.select_all(action='DESELECT')
    root_empty.select_set(True)
    bpy.context.view_layer.objects.active = root_empty

    return f"Created '{object_name}' volumetric setup at {location} with {len(root_empty.children)} objects and custom Sky World."
```