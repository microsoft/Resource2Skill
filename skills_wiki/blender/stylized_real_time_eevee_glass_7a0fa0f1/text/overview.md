# Stylized Real-Time EEVEE Glass

## Analysis

An elegant and highly optimized technique for rendering glass in Blender's EEVEE engine. This method deliberately bypasses expensive raytracing by combining transparency and procedural view-dependent reflections to create a convincing, noise-free glass effect that renders instantly.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized Real-Time EEVEE Glass

* **Core Visual Mechanism**: The core trick relies on blending a purely **Transparent BSDF** with a **Glossy BSDF** using a heavily exaggerated **Fresnel node** (IOR ~15). Because the IOR is so high, the Fresnel effect pushes all reflections strictly to the grazing angles (the edges of the object) while keeping the center perfectly see-through, mimicking refraction without actually computing it.
* **Why Use This Skill (Rationale)**: Real-time raytraced refraction in EEVEE can be computationally heavy, noisy, or produce unwanted artifacts. This shader technique acts as an ultra-fast, stylized alternative. It guarantees a clean, noise-free surface that still communicates volume, curvature, and shininess perfectly. 
* **Overall Applicability**: Ideal for motion graphics, stylized scenes, architectural visualization previews, background props, or any scenario constrained by rendering time or hardware performance. 
* **Value Addition**: Transforms a flat, invisible transparent mesh into a tangible glass object with edge highlights and surface imperfections, all without the performance penalty of screen-space refractions.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: Any hollow object. For demonstration, an open-topped cylinder is used.
  - **Modifiers**: A **Solidify** modifier is absolutely critical. Hollow objects need physical thickness for the grazing angles to catch the light on both the inside and outside edges. A **Bevel** modifier is also added to catch micro-reflections.
  - **Shading**: Smooth shading is required for the Fresnel node to calculate a continuous gradient.

* **Step B: Materials & Shading**
  - **Shader Mix**: `Mix Shader` combining `Transparent BSDF` (Top/Factor 0) and `Glossy BSDF` (Bottom/Factor 1).
  - **Factor**: `Fresnel` node with IOR spammed to **15.2**.
  - **Surface Imperfection**: `Noise Texture` (Scale 30) routed through a `ColorRamp` (Black to Dark Gray `(0.1, 0.1, 0.1)`) plugged into the Glossy Roughness. This adds subtle smudges/waviness to the reflections.
  - **Render Settings**: Material blend mode set to `Alpha Blend` (or "Blended") and shadows set to `None` so the glass doesn't cast a solid black shadow.

* **Step C: Lighting & Rendering Context**
  - **Lighting**: This material **requires** an environment to reflect. An HDRI or a scene with bright emissive lights/windows will make the Glossy BSDF pop on the edges.
  - **Engine**: Specifically designed for EEVEE, with raytracing explicitly turned off for maximum performance.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base Mesh Hollow Cup | `bmesh` + mesh primitive | Deleting the top face programmatically ensures we have an open volume. |
| Object Thickness | `Solidify` & `Bevel` Modifiers | Creates the necessary dual-sided geometry to catch reflections on inner and outer edges. |
| Fake Refraction Material | Shader Node Tree | Procedural nodes recreate the exaggerated Fresnel logic exactly as described in the tutorial. |

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "EEVEE_Glass_Cup",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.95, 0.95, 1.0),
    **kwargs,
) -> str:
    """
    Create a stylized, fast-rendering glass cup optimized for EEVEE.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created glass object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) tint for the transparent glass.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    # Get the target scene
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # === Step 1: Create Base Geometry (Open Cylinder) ===
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32, 
        radius=1.0, 
        depth=2.0, 
        end_fill_type='NGON',
        location=(0, 0, 1) # Shift up so origin is at bottom
    )
    obj = bpy.context.active_object
    obj.name = object_name
    
    # Use bmesh to delete the top face to make it hollow
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    
    # Find the top face (normal pointing straight up)
    top_face = next((f for f in bm.faces if f.normal.z > 0.9), None)
    if top_face:
        bmesh.ops.delete(bm, geom=[top_face], context='FACES')
        
    bm.to_mesh(obj.data)
    bm.free()

    # Apply smooth shading
    for poly in obj.data.polygons:
        poly.use_smooth = True

    # === Step 2: Add Modifiers (Thickness & Bevel) ===
    # Solidify is critical for the glass effect to have inner/outer reflections
    solidify = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = 0.05
    solidify.use_even_offset = True
    
    # Bevel to catch highlights on the rim
    bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel.segments = 4
    bevel.width = 0.015
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = 0.52  # ~30 degrees

    # === Step 3: Build the EEVEE Glass Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    # Handle EEVEE transparency settings (Safeguard for Blender 4.2+ engine changes)
    try:
        mat.blend_method = 'BLEND'
        mat.shadow_method = 'NONE'
        mat.show_transparent_back = True
    except AttributeError:
        pass

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Core Shader Nodes
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)

    mix_shader = nodes.new('ShaderNodeMixShader')
    mix_shader.location = (200, 0)

    # 1. Transparency (Facing)
    transparent = nodes.new('ShaderNodeBsdfTransparent')
    transparent.location = (0, 100)
    transparent.inputs['Color'].default_value = (*material_color, 1.0)

    # 2. Reflection (Edges)
    glossy = nodes.new('ShaderNodeBsdfGlossy')
    glossy.location = (0, -100)
    glossy.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0) # Pure white reflections

    # 3. Fresnel blending with exaggerated IOR
    fresnel = nodes.new('ShaderNodeFresnel')
    fresnel.location = (0, 300)
    fresnel.inputs['IOR'].default_value = 15.2  # The secret sauce from the tutorial

    # 4. Surface Imperfections (Noise -> ColorRamp -> Roughness)
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-400, -100)
    noise.inputs['Scale'].default_value = 30.0
    noise.inputs['Detail'].default_value = 2.0

    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-200, -100)
    # Clamp noise to keep it mostly glossy (black to dark gray)
    color_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[1].color = (0.15, 0.15, 0.15, 1.0)
    color_ramp.color_ramp.elements[1].position = 1.0

    # Wire up the network
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], glossy.inputs['Roughness'])
    
    links.new(fresnel.outputs['Fac'], mix_shader.inputs['Fac'])
    links.new(transparent.outputs['BSDF'], mix_shader.inputs[1]) # Top socket
    links.new(glossy.outputs['BSDF'], mix_shader.inputs[2])      # Bottom socket
    
    links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])

    # Assign material to object
    obj.data.materials.append(mat)

    # === Step 4: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    # Link to scene collection if not already there (primitive_add usually does this)
    if obj.name not in scene.collection.objects:
        scene.collection.objects.link(obj)

    return f"Created '{object_name}' with stylized EEVEE glass at {location}. Requires HDRI/lights to reflect properly."
```