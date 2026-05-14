# Volumetric Spot Light Cone (Mesh-Bound)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Volumetric Spot Light Cone (Mesh-Bound)

* **Core Visual Mechanism**: Encapsulating volumetric scattering within a specific boundary (a custom cone mesh) rather than applying it globally to the world environment. This is achieved by generating a procedural BMesh cone that mathematically perfectly matches the spot light's aperture angle and distance, parenting it to the light, and applying a `Principled Volume` material to the mesh with the surface shader removed.
* **Why Use This Skill (Rationale)**: Global volumetric scatter (fog) washes out the entire scene's contrast and severely increases render times because the engine calculates scattering everywhere. Using a mesh-bound volume allows for crisp, defined "god rays" or spotlight beams without filling the ambient shadows with fog. It is highly art-directable and computationally cheaper.
* **Overall Applicability**: Cinematic stage lighting, vehicle headlights, flashlights, UFO tractor beams, or localized atmospheric effects in dark environments (e.g., sci-fi corridors).
* **Value Addition**: Transforms a standard, invisible spot light into a tangible, atmospheric beam with clearly defined physical boundaries, adding cinematic depth to the scene while dodging the performance hit of global fog.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - A procedural mesh is generated using `bmesh`.
  - The tip of the cone is placed at the local origin `(0, 0, 0)`.
  - A base circle (32 vertices) is generated at a fixed $Z$-depth (`-beam_length`).
  - The radius of the base is calculated via trigonometry (`beam_length * tan(spot_angle / 2)`) so the geometry perfectly sleeves the Spot Light's actual light emission.
  - The cone is parented to the Spot Light, allowing them to move and rotate as a single cohesive unit.

* **Step B: Materials & Shading**
  - **Shader Model**: Volume-only material.
  - The `Principled BSDF` is deleted from the `Surface` output socket to make the outer shell completely transparent.
  - A `Principled Volume` node is connected to the `Volume` socket.
  - **Density**: Set low, typically `0.1` to `0.2`, allowing light to travel through the beam.
  - **Color**: Passed dynamically, e.g., `(0.8, 0.9, 1.0)` for a cool bluish sci-fi beam.
  - **Eevee Bounding Box Fix**: A tiny amount of `Emission Strength` (e.g., `0.003`) is applied using the same color to artificially mask blocky artifacting that occurs in Eevee when volume bounds intersect with dark World environment lighting.

* **Step C: Lighting & Rendering Context**
  - Uses a standard `SPOT` light with high energy (e.g., `5000 W`).
  - Best showcased against a dark or near-black World background.
  - **EEVEE Specifics**: `Volumetric Lighting` must be enabled in Render Properties. The `Volumetric Tile Size` should be dropped to `2px` to smooth out the jagged edges of the light cone.

* **Step D: Animation & Dynamics**
  - Simply animating the parent Spot Light's rotation or location will drag the procedural volumetric beam along with it perfectly.
  - An optional `Boolean` modifier (Difference mode) can be applied to the cone targeting the floor, preventing the "beam" from penetrating solid surfaces.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base Cone Geometry | `bmesh` procedural generation | Allows precise trigonometric alignment of the mesh radius with the Spotlight's angle parameter. |
| Volumetric Fog | Shader node tree | Deleting the Surface node and applying `Principled Volume` confines the scatter strictly inside the cone's boundaries. |
| Linking Light & Mesh | Object Parenting | Ensures the physical bounds always aim precisely where the light points without manual synchronization. |

> **Feasibility Assessment**: 100% reproduction. The procedural bmesh aligns perfectly with the spot light API parameters, and the shader manipulation identically recreates the isolated volumetric beam from the tutorial, including the Eevee-specific artifact mitigation strategies.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "VolumetricSpotBeam",
    location: tuple = (0.0, 0.0, 5.0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.9, 1.0),
    **kwargs,
) -> str:
    """
    Create a mesh-bound Volumetric Spot Light Cone in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the light and cone objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the object grouping.
        material_color: (R, G, B) base color for the light and volume.
        **kwargs: 
            rotation: (x, y, z) Euler angles in radians. Default (0, 0, 0).
            spot_size_degrees: Spotlight aperture angle. Default 45.0.
            beam_length: Physical length of the cone mesh. Default 10.0.
            energy: Light wattage. Default 5000.0.
            volume_density: Density of the fog inside the cone. Default 0.1.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Euler
    
    # Parse kwargs
    rotation = kwargs.get("rotation", (0.0, 0.0, 0.0))
    spot_size_degrees = kwargs.get("spot_size_degrees", 45.0)
    beam_length = kwargs.get("beam_length", 10.0)
    energy = kwargs.get("energy", 5000.0)
    volume_density = kwargs.get("volume_density", 0.1)

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Create the Spot Light ===
    light_data = bpy.data.lights.new(name=f"{object_name}_Light", type='SPOT')
    light_data.energy = energy
    light_data.spot_size = math.radians(spot_size_degrees)
    light_data.spot_blend = 0.5  # Soften the edge of the light slightly
    light_data.color = material_color[:3]
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_LightObj", object_data=light_data)
    scene.collection.objects.link(light_obj)
    
    light_obj.location = location
    light_obj.rotation_euler = Euler(rotation, 'XYZ')

    # === Step 2: Generate the Exact Bounding Cone via BMesh ===
    bm = bmesh.new()
    tip = bm.verts.new((0.0, 0.0, 0.0))
    
    segments = 32
    # Trigonometry to perfectly match the base radius to the spot light angle
    radius = beam_length * math.tan(light_data.spot_size / 2.0)
    
    base_verts = []
    for i in range(segments):
        angle = (i / segments) * 2 * math.pi
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        # Spotlights point down the local -Z axis
        z = -beam_length 
        v = bm.verts.new((x, y, z))
        base_verts.append(v)
        
    # Create the slanted side faces
    for i in range(segments):
        v1 = base_verts[i]
        v2 = base_verts[(i + 1) % segments]
        bm.faces.new((tip, v1, v2))
        
    # Create the flat base cap (essential for proper volume bounds rendering)
    # Reversed to ensure the normal points outward (-Z)
    bm.faces.new(reversed(base_verts))
    
    bm.normal_update()
    
    mesh = bpy.data.meshes.new(name=f"{object_name}_Mesh")
    bm.to_mesh(mesh)
    bm.free()
    
    cone_obj = bpy.data.objects.new(name=object_name, object_data=mesh)
    scene.collection.objects.link(cone_obj)
    
    # Parent the cone directly to the light
    cone_obj.parent = light_obj
    cone_obj.matrix_world = light_obj.matrix_world
    cone_obj.scale = (scale, scale, scale)

    # === Step 3: Build the Volumetric Shader ===
    mat = bpy.data.materials.new(name=f"{object_name}_VolMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default surface nodes
    nodes.clear()
    
    vol_node = nodes.new(type='ShaderNodeVolumePrincipled')
    vol_node.location = (0, 0)
    vol_node.inputs['Density'].default_value = volume_density
    vol_node.inputs['Color'].default_value = (*material_color[:3], 1.0)
    
    # Eevee bounding box artifact fix: add a nearly imperceptible amount of emission
    vol_node.inputs['Emission Strength'].default_value = 0.003
    vol_node.inputs['Emission Color'].default_value = (*material_color[:3], 1.0)
    
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (300, 0)
    
    # Crucial: connect to Volume, not Surface
    links.new(vol_node.outputs['Volume'], out_node.inputs['Volume'])
    
    cone_obj.data.materials.append(mat)

    # === Step 4: Configure Global Eevee Volumetrics ===
    try:
        scene.eevee.use_volumetric_lights = True
        # Using 2px tile size vastly improves beam edge quality in Eevee
        scene.eevee.volumetric_tile_size = '2' 
    except AttributeError:
        # Failsafe for API changes in newer Blender versions (e.g. Eevee Next)
        pass

    return f"Created '{object_name}' (Spot Light + Volumetric Mesh Cone) at {location}. Beam length: {beam_length}."
```