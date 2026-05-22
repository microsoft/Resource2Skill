# Procedural Raycast Water Shader (Cycles)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Raycast Water Shader (Cycles)

* **Core Visual Mechanism**: This shader utilizes the `ShaderNodeRaycast` (introduced in recent Blender versions) to cast rays downward from the water surface to calculate dynamic depth. This internal depth measurement drives three key effects: 
  1. **Depth-based color blending** (shallow water is clear/bright, deep water is dark).
  2. **Depth-based refraction blur** (objects deeper underwater appear blurrier, simulating particulate scattering).
  3. **Procedural Meniscus** (the surface tension lip where water meets an object), achieved by blending the water's geometry normal with the raycast `Hit Normal` when the depth is near zero.

* **Why Use This Skill (Rationale)**: Traditional 3D water relies heavily on Volume Absorption (computationally expensive and noisy) or Screen-Space Depth tricks (which break down at certain camera angles or with overlapping transparencies). The raycast approach evaluates locally, meaning it is mathematically precise, requires zero actual volume rendering, and automatically wraps the surface tension (meniscus) around any intersecting geometry without needing high-density meshes or dynamic boolean modifiers.

* **Overall Applicability**: Ideal for pools, rivers, puddles, and coastal environments where objects intersect the water line. It shines in physically based or stylized environments rendered in Cycles where interaction between the water and submerged props is critical to the composition.

* **Value Addition**: Compared to a standard glass/transparent plane, this shader physically anchors the water to the scene. The procedural meniscus and depth-driven blur trick the eye into perceiving physical volume and fluid dynamics on a completely flat, single-polygon plane.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A simple 2D Plane. No subdivision or complex topology is required because all depth and surface tension effects are evaluated per-pixel via the shader.
  - **Environment**: Requires objects placed underneath and intersecting the plane to demonstrate the raycast hits.

* **Step B: Materials & Shading**
  - **Vector Refraction**: The `Incoming` view vector is scaled by -1 and refracted using the surface normal and water IOR (1.333).
  - **Raycasting**: A `Raycast` node shoots this refracted vector from the surface into the scene.
  - **Depth Correction**: To prevent optical artifacts at grazing viewing angles, the `Hit Distance` is multiplied by the absolute dot product of the `Incoming` vector and the surface `Normal`.
  - **Meniscus Generation**: A `Map Range` node isolates depths extremely close to 0 (e.g., `< 0.1m`). This masks a `Mix Vector` node that blends the flat surface normal with the `Hit Normal` of the intersecting object.
  - **Material Layering**: 
    - `Diffuse BSDF` provides the "particulate" watercolor (blended from Shallow to Deep).
    - `Refraction BSDF` provides the transparency, with its `Roughness` driven by the depth (deeper = blurrier).
    - `Glossy BSDF` provides the sharp surface reflections, layered on top using a `Fresnel` mask.

* **Step C: Lighting & Rendering Context**
  - **Render Engine**: **Cycles is strictly required**. The `ShaderNodeRaycast` is a Cycles-exclusive feature and will not evaluate in EEVEE.
  - **Lighting**: An HDRI or a strong Sun/Area light is necessary to highlight the sharp glossy reflections and the bending meniscus edges.

* **Step D: Animation & Dynamics**
  - To animate the water, a driver (`#frame / 250`) can be added to the `W` or `Phase` input of the `Noise Texture` driving the surface bump.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Test Environment | `bpy.ops.mesh.primitive` | Creates a floor and submerged objects so the raycast has geometry to hit. |
| Depth Calculation | `ShaderNodeRaycast` | Shoots rays into the scene to measure true depth and intersecting normals. |
| Meniscus & Blur | Node Math (`Map Range`, `Vector Mix`) | Modulates the surface normal and refraction roughness programmatically based on the raycast outputs. |

> **Feasibility Assessment**: 100% reproduction of the core water shader technique. The video also briefly covers a separate ambient-occlusion-style "foam" generator, but the core raycast logic (color, blur, meniscus) is fully encapsulated here.

#### 3b. Complete Reproduction Code

```python
def create_raycast_water(
    scene_name: str = "Scene",
    object_name: str = "RaycastWater",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    shallow_color: tuple = (0.05, 0.6, 0.8),
    deep_color: tuple = (0.0, 0.1, 0.3),
    **kwargs
) -> str:
    """
    Creates a flat procedural water plane that uses Cycles Raycasting to generate 
    depth-based color, depth-based refraction blur, and a procedural meniscus.
    
    Args:
        scene_name: Target scene.
        object_name: Name of the water plane.
        location: World-space position of the water surface.
        scale: Size scale of the pool and objects.
        shallow_color: RGB tuple for water color near the surface.
        deep_color: RGB tuple for water color at max depth.
        
    Returns:
        Status string.
    """
    import bpy

    # Ensure valid scene and force Cycles (Raycast node requirement)
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    scene.render.engine = 'CYCLES'

    # === 1. Create Test Environment (So Raycast has something to hit) ===
    # Floor
    bpy.ops.mesh.primitive_plane_add(size=10 * scale, location=(location[0], location[1], location[2] - 2.0 * scale))
    floor = bpy.context.active_object
    floor.name = f"{object_name}_Floor"
    
    # Submerged intersecting objects
    bpy.ops.mesh.primitive_torus_add(location=(location[0] - 1.5 * scale, location[1], location[2] - 0.5 * scale))
    torus = bpy.context.active_object
    torus.name = f"{object_name}_SubmergedTorus"
    torus.scale = (scale, scale, scale)
    
    bpy.ops.mesh.primitive_cube_add(location=(location[0] + 1.5 * scale, location[1] - 0.5 * scale, location[2] - 1.0 * scale))
    cube = bpy.context.active_object
    cube.name = f"{object_name}_SubmergedCube"
    cube.scale = (scale, scale, scale)
    
    # Simple base material for test objects
    obj_mat = bpy.data.materials.new(name=f"{object_name}_PropsMat")
    obj_mat.use_nodes = True
    obj_mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.8, 0.3, 0.1, 1.0)
    floor.data.materials.append(obj_mat)
    torus.data.materials.append(obj_mat)
    cube.data.materials.append(obj_mat)

    # === 2. Create the Water Plane ===
    bpy.ops.mesh.primitive_plane_add(size=10 * scale, location=location)
    water = bpy.context.active_object
    water.name = object_name
    
    # === 3. Build the Procedural Raycast Shader ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    water.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Base Nodes
    geom = nodes.new('ShaderNodeNewGeometry')
    geom.location = (-1200, 0)
    
    # Refraction Ray Setup
    scale_inc = nodes.new('ShaderNodeVectorMath')
    scale_inc.operation = 'SCALE'
    scale_inc.inputs[3].default_value = -1.0 # Scale value
    scale_inc.location = (-1000, 100)
    links.new(geom.outputs['Incoming'], scale_inc.inputs[0])
    
    ior_div = nodes.new('ShaderNodeMath')
    ior_div.operation = 'DIVIDE'
    ior_div.inputs[0].default_value = 1.0
    ior_div.inputs[1].default_value = 1.333 # Water IOR
    ior_div.location = (-1000, -100)
    
    refract = nodes.new('ShaderNodeVectorMath')
    refract.operation = 'REFRACT'
    refract.location = (-800, 100)
    links.new(scale_inc.outputs[0], refract.inputs[0])
    links.new(geom.outputs['Normal'], refract.inputs[1])
    links.new(ior_div.outputs[0], refract.inputs[2])
    
    norm_refract = nodes.new('ShaderNodeVectorMath')
    norm_refract.operation = 'NORMALIZE'
    norm_refract.location = (-600, 100)
    links.new(refract.outputs[0], norm_refract.inputs[0])
    
    # The Raycast Node
    raycast = nodes.new('ShaderNodeRaycast')
    raycast.location = (-400, 100)
    links.new(geom.outputs['Position'], raycast.inputs['Position'])
    links.new(norm_refract.outputs[0], raycast.inputs['Direction'])
    
    # Grazing Angle Depth Correction
    dot_inc_norm = nodes.new('ShaderNodeVectorMath')
    dot_inc_norm.operation = 'DOT_PRODUCT'
    dot_inc_norm.location = (-400, -100)
    links.new(geom.outputs['Incoming'], dot_inc_norm.inputs[0])
    links.new(geom.outputs['Normal'], dot_inc_norm.inputs[1])
    
    abs_dot = nodes.new('ShaderNodeMath')
    abs_dot.operation = 'ABSOLUTE'
    abs_dot.location = (-200, -100)
    links.new(dot_inc_norm.outputs['Value'], abs_dot.inputs[0])
    
    calc_depth = nodes.new('ShaderNodeMath')
    calc_depth.operation = 'MULTIPLY'
    calc_depth.location = (0, 0)
    links.new(raycast.outputs['Hit Distance'], calc_depth.inputs[0])
    links.new(abs_dot.outputs[0], calc_depth.inputs[1])
    
    # Procedural Meniscus (Surface Tension)
    meniscus_map = nodes.new('ShaderNodeMapRange')
    meniscus_map.location = (0, 300)
    meniscus_map.interpolation_type = 'SMOOTHSTEP'
    meniscus_map.inputs[1].default_value = 0.0
    meniscus_map.inputs[2].default_value = 0.1 * scale # Meniscus Distance Falloff
    meniscus_map.inputs[3].default_value = 1.0 # 1.0 means full hit normal
    meniscus_map.inputs[4].default_value = 0.0
    links.new(calc_depth.outputs[0], meniscus_map.inputs[0])
    
    meniscus_mix = nodes.new('ShaderNodeMix')
    meniscus_mix.data_type = 'VECTOR'
    meniscus_mix.location = (200, 300)
    links.new(meniscus_map.outputs[0], meniscus_mix.inputs[0]) 
    links.new(geom.outputs['Normal'], meniscus_mix.inputs[4]) # A (Base Normal)
    links.new(raycast.outputs['Hit Normal'], meniscus_mix.inputs[5]) # B (Hit Normal)
    
    meniscus_norm = nodes.new('ShaderNodeVectorMath')
    meniscus_norm.operation = 'NORMALIZE'
    meniscus_norm.location = (400, 300)
    links.new(meniscus_mix.outputs[1], meniscus_norm.inputs[0])
    
    # Surface Bump Ripples
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 15.0 / scale
    noise.location = (200, 500)
    
    bump = nodes.new('ShaderNodeBump')
    bump.inputs['Distance'].default_value = 0.02 * scale
    bump.location = (400, 500)
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(meniscus_norm.outputs[0], bump.inputs['Normal'])
    
    # Depth Color Blend
    color_map = nodes.new('ShaderNodeMapRange')
    color_map.location = (200, -100)
    color_map.inputs[1].default_value = 0.0
    color_map.inputs[2].default_value = 2.0 * scale # Deep Depth limit
    color_map.inputs[3].default_value = 0.0
    color_map.inputs[4].default_value = 1.0
    links.new(calc_depth.outputs[0], color_map.inputs[0])
    
    color_mix = nodes.new('ShaderNodeMix')
    color_mix.data_type = 'RGBA'
    color_mix.location = (400, -100)
    color_mix.inputs[6].default_value = (*shallow_color, 1.0)
    color_mix.inputs[7].default_value = (*deep_color, 1.0)
    links.new(color_map.outputs[0], color_mix.inputs[0])
    
    # Blur Amount (Drives Refraction Roughness)
    blur_map = nodes.new('ShaderNodeMapRange')
    blur_map.location = (200, -350)
    blur_map.inputs[1].default_value = 0.0
    blur_map.inputs[2].default_value = 3.0 * scale # Blur max depth
    blur_map.inputs[3].default_value = 0.0 # Min Roughness
    blur_map.inputs[4].default_value = 0.4 # Max Roughness
    links.new(calc_depth.outputs[0], blur_map.inputs[0])
    
    # Core Shaders
    diffuse = nodes.new('ShaderNodeBsdfDiffuse')
    diffuse.location = (600, -100)
    links.new(color_mix.outputs[2], diffuse.inputs['Color'])
    links.new(bump.outputs[0], diffuse.inputs['Normal'])
    
    refraction = nodes.new('ShaderNodeBsdfRefraction')
    refraction.location = (600, -300)
    refraction.inputs['IOR'].default_value = 1.333
    links.new(blur_map.outputs[0], refraction.inputs['Roughness'])
    links.new(bump.outputs[0], refraction.inputs['Normal'])
    
    mix_diff_refr = nodes.new('ShaderNodeMixShader')
    mix_diff_refr.location = (800, -200)
    mix_diff_refr.inputs[0].default_value = 0.85 # Mostly Refraction
    links.new(diffuse.outputs[0], mix_diff_refr.inputs[1])
    links.new(refraction.outputs[0], mix_diff_refr.inputs[2])
    
    glossy = nodes.new('ShaderNodeBsdfGlossy')
    glossy.location = (800, 0)
    glossy.inputs['Roughness'].default_value = 0.02
    links.new(bump.outputs[0], glossy.inputs['Normal'])
    
    fresnel = nodes.new('ShaderNodeFresnel')
    fresnel.inputs['IOR'].default_value = 1.333
    fresnel.location = (800, 200)
    links.new(bump.outputs[0], fresnel.inputs['Normal'])
    
    mix_final = nodes.new('ShaderNodeMixShader')
    mix_final.location = (1000, 0)
    links.new(fresnel.outputs[0], mix_final.inputs[0])
    links.new(mix_diff_refr.outputs[0], mix_final.inputs[1])
    links.new(glossy.outputs[0], mix_final.inputs[2])
    
    out = nodes.new('ShaderNodeOutputMaterial')
    out.location = (1200, 0)
    links.new(mix_final.outputs[0], out.inputs['Surface'])

    # === 4. Add Environment Lighting ===
    if not any(light.type == 'SUN' for light in bpy.data.lights):
        bpy.ops.object.light_add(type='SUN', location=(location[0], location[1], location[2] + 5))
        sun = bpy.context.active_object
        sun.name = f"{object_name}_Sun"
        sun.data.energy = 5.0
        sun.rotation_euler = (0.8, 0.5, 0.0)

    return f"Created Raycast Water '{object_name}' with test objects. Ensure viewport is set to CYCLES to view."
```