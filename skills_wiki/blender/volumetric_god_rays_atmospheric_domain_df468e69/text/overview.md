# Volumetric God Rays & Atmospheric Domain

## Analysis

Here is the skill extraction based on the provided tutorial.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Volumetric God Rays & Atmospheric Domain

* **Core Visual Mechanism**: The defining characteristic of this technique is the creation of distinct, localized "light shafts" or "god rays." This is achieved by enclosing the scene in a bounding geometry with a volumetric material and passing a high-intensity, narrow-angle light source (like a Spot light) through it.

* **Why Use This Skill (Rationale)**: In real life, light shafts occur when photons scatter off particulate matter suspended in the air (dust, fog, smoke). In 3D rendering, adding this atmospheric scattering exponentially increases the realism, scale, and cinematic mood of a scene. It separates the foreground from the background and gives empty space a tangible presence.

* **Overall Applicability**: This technique is essential for cinematic lighting setups, interior renders with windows (sunlight streaming in), moody sci-fi corridors, underwater scenes, or dense environments like forests.

* **Value Addition**: By using a localized cube "domain" instead of applying volumetrics to the entire World shader, you gain artistic control over exactly where the fog exists, drastically improve render times, and prevent the background/skybox from being completely washed out by ambient haze.


### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A simple primitive Cube acting as a volume container (domain).
  - **Scale**: Scaled uniformly to encompass the subjects of the scene.
  - **Viewport Optimization**: The object's Viewport Display mode is set to `Bounds`. This makes the geometry completely wireframe/invisible while working in the 3D viewport so it doesn't obscure the artist's view, while still rendering properly as a volume.

* **Step B: Materials & Shading**
  - **Shader Model**: `Principled Volume` (or `Volume Scatter`) routed directly into the **Volume** socket of the Material Output (leaving the Surface socket empty).
  - **Density**: Set extremely low (e.g., `0.025` to `0.05`). Volumetrics compound over distance, so large objects require tiny density values.
  - **Anisotropy**: Increased significantly (e.g., `0.6`). Positive anisotropy means light scatters forward in the direction the rays are traveling, making the "god rays" much more pronounced when looking towards the light source.

* **Step C: Lighting & Rendering Context**
  - **Light Source**: A single Spot light is used to drive the effect.
  - **Light Settings**: Extremely high power (e.g., `2000W`), a narrow cone angle (e.g., `30-35 degrees`), and a high blend value (`1.0`) for soft ray edges.
  - **Render Engine**: Works best in Cycles for physically accurate scattering, but perfectly compatible with EEVEE (provided Volumetrics are enabled in the render settings).


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Atmospheric Domain** | `bmesh` primitive + `display_type` | Generates a clean cube container and sets it to 'BOUNDS' so it doesn't block viewport interaction. |
| **Volumetric Material** | Shader Node Tree | Procedurally routes a `Principled Volume` node to the Volume output socket, clearing any surface shaders. |
| **Light Source** | `bpy.data.lights` | Generates a custom Spot light parameterized to cast a narrow, high-energy beam and automatically tracks its rotation to the center of the volume. |

> **Feasibility Assessment**: 100% — The provided code fully proceduralizes the volumetric domain, the optimized viewport settings, the shader node logic, and the driving spotlight exactly as demonstrated in the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "VolumetricGodRays",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 10.0,
    material_color: tuple = (1.0, 1.0, 1.0),
    **kwargs,
) -> str:
    """
    Create a localized volumetric fog domain and a driving spotlight for god rays.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position for the center of the fog domain.
        scale: Uniform scale factor for the cubic fog domain.
        material_color: (R, G, B) base color of the fog particles.
        **kwargs: 
            density (float): Density of the volume (default 0.025).
            anisotropy (float): Forward scattering intensity (default 0.6).
            create_spotlight (bool): Whether to create a driving spotlight (default True).
            light_location (tuple): World position of the spotlight (default (0, 0, 8)).
            light_power (float): Energy/power of the spotlight in Watts (default 2000.0).

    Returns:
        Status string describing the generated atmospheric setup.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    # Extract scene and kwargs
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    density = kwargs.get("density", 0.025)
    anisotropy = kwargs.get("anisotropy", 0.6)
    create_spotlight = kwargs.get("create_spotlight", True)
    light_location = kwargs.get("light_location", (0.0, 0.0, 8.0))
    light_power = kwargs.get("light_power", 2000.0)
    light_color = kwargs.get("light_color", (1.0, 0.95, 0.9))  # Slightly warm light

    objects_created = []

    # === Step 1: Create Volumetric Domain Geometry ===
    mesh = bpy.data.meshes.new(name=f"{object_name}_DomainMesh")
    domain_obj = bpy.data.objects.new(name=object_name, object_data=mesh)
    scene.collection.objects.link(domain_obj)
    objects_created.append(domain_obj.name)
    
    # Generate cube geometry (2x2x2 base size)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    bm.to_mesh(mesh)
    bm.free()
    
    # Transform and optimize viewport
    domain_obj.location = Vector(location)
    domain_obj.scale = (scale, scale, scale)
    domain_obj.display_type = 'BOUNDS'  # Keep viewport clear

    # === Step 2: Build Volumetric Shader ===
    mat = bpy.data.materials.new(name=f"{object_name}_VolMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default Surface nodes
    for node in nodes:
        nodes.remove(node)

    # Add Output Node
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (300, 0)

    # Add Principled Volume Node
    vol_node = nodes.new(type='ShaderNodeVolumePrincipled')
    vol_node.location = (0, 0)
    
    # Set Volumetric Properties
    vol_node.inputs['Color'].default_value = (*material_color, 1.0)
    vol_node.inputs['Density'].default_value = density
    vol_node.inputs['Anisotropy'].default_value = anisotropy

    # Link Volume Output to Material Volume Socket
    links.new(vol_node.outputs['Volume'], out_node.inputs['Volume'])
    domain_obj.data.materials.append(mat)

    # === Step 3: Create Driving Spotlight ===
    if create_spotlight:
        light_data = bpy.data.lights.new(name=f"{object_name}_SpotData", type='SPOT')
        light_obj = bpy.data.objects.new(name=f"{object_name}_SpotLight", object_data=light_data)
        scene.collection.objects.link(light_obj)
        objects_created.append(light_obj.name)
        
        # Position light
        light_obj.location = Vector(light_location)
        
        # Track light rotation to point at the center of the volumetric domain
        direction = domain_obj.location - light_obj.location
        if direction.length > 0:
            # -Z is the default forward direction for Spot lights in Blender
            light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
        
        # Configure Light Properties
        light_data.energy = light_power
        light_data.spot_size = math.radians(35)  # Narrow beam
        light_data.spot_blend = 1.0              # Soft edges
        light_data.color = light_color

    # Ensure EEVEE renders volumetrics if it is the active engine
    if scene.render.engine == 'BLENDER_EEVEE':
        try:
            scene.eevee.use_volumetric = True
        except Exception:
            pass

    return f"Created {len(objects_created)} atmospheric objects: {', '.join(objects_created)} at location {location}"
```