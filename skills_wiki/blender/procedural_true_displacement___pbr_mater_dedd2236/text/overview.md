### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural True Displacement & PBR Material Setup

* **Core Visual Mechanism**: Using heavily subdivided geometry paired with a Cycles material set to "Displacement Only" to create physical depth from texture height maps. Rather than just relying on surface shading (bump/normal maps) to fake detail, true displacement physically extrudes and depresses the mesh at render time.
* **Why Use This (Rationale)**: Traditional bump and normal maps break down at silhouette edges and cannot cast physical self-shadows. True displacement alters the actual geometry, producing photorealistic occlusion, deep shadows, and irregular silhouettes essential for natural surfaces like rock, cracked earth, or brick walls.
* **Overall Applicability**: Essential for creating highly detailed environmental assets (terrains, brick walls, rocky grounds) and close-up hero props where surface silhouette detail is critical to realism.
* **Value Addition**: Transforms a basic primitive plane into a richly detailed, physically accurate 3D surface without requiring high-poly manual sculpting. It bridges the gap between procedural texture generation and high-fidelity mesh modeling.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Primitive**: A basic Plane.
  - **Modification**: A Subdivision Surface modifier set to 'SIMPLE' is applied with high levels (e.g., 6 for viewport, 8 for render). This creates a dense grid of microscopic faces, providing the vertex density required for the displacement map to physically move the geometry.
* **Step B: Materials & Shading**
  - **Shader Model**: Principled BSDF.
  - **Procedural PBR Setup**: Since external textures cannot be reliably downloaded in a standalone script, a robust procedural equivalent is used:
    - **Height Map**: A Voronoi texture (`DISTANCE_TO_EDGE` to simulate cracks/stone blocks) is mathematically added to a Noise texture (for fine grit/surface detail).
    - **Base Color**: Maps the height map through a ColorRamp, placing deep browns/blacks in the cracks `(0.01, 0.01, 0.01)` and a custom rock color `(0.2, 0.15, 0.1)` on the raised surfaces.
    - **Roughness**: Maps the height map to vary roughness between `0.7` and `1.0`.
    - **Displacement Node**: Plugs the height map into a Displacement node, which connects to the Material Output.
  - **Crucial Setting**: The Material's internal `cycles.displacement_method` MUST be set to `'DISPLACEMENT'` or `'BOTH'` (the default `'BUMP'` will ignore the physical displacement).
* **Step C: Lighting & Rendering Context**
  - **Render Engine**: Cycles is explicitly required. EEVEE (prior to 4.2) only fakes displacement as bump.
  - **Lighting**: A Sun light with high strength (Energy = 5.0) placed at a sharp 45-degree angle. This angled lighting is vital to cast the deep shadows that make true displacement look realistic.
* **Step D: Animation & Dynamics**
  - While static, the mapping coordinates of the procedural textures could be animated to simulate shifting terrain or flowing lava.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Geometry Density | `primitive_plane_add` + Subdivision Modifier | Cleaner, non-destructive, and easier to manage than the manual `bmesh` subdivision shown in the video. |
| Material Textures | Procedural Nodes (Voronoi + Noise) | **Necessity**. The tutorial relies on a `.zip` file from Poly Haven. To make the code strictly self-contained and reproducible without external internet requests, a procedural height map mimicking cracked rock is used. |
| True Displacement | Material Output Displacement + Cycles | This directly replicates the core instructional value of the video: linking a height map and enabling physical mesh displacement. |

> **Feasibility Assessment**: 95% reproducible. The code achieves the exact same *technical mechanism* (Cycles true displacement via nodes on a dense mesh) and similar visual results (rocky, deep-shadow terrain), but replaces the specific downloaded image textures with procedural math textures to guarantee the code runs instantly on any machine.

#### 3b. Complete Reproduction Code

```python
def create_pbr_displacement_plane(
    scene_name: str = "Scene",
    object_name: str = "PBR_Rock_Plane",
    location: tuple = (0, 0, 0),
    scale: float = 2.0,
    material_color: tuple = (0.2, 0.15, 0.1),
    **kwargs,
) -> str:
    """
    Create a procedural PBR rock material with true displacement on a subdivided plane.
    Recreates the core workflow of applying true displacement in Cycles.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created plane.
        location: (x, y, z) world-space position.
        scale: Size scale of the plane.
        material_color: (R, G, B) base color for the top surface of the rock.
        **kwargs: Additional overrides.

    Returns:
        Status string confirming creation.
    """
    import bpy
    import math

    # Get scene
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Enforce Cycles Engine ===
    # True material displacement relies heavily on Cycles
    scene.render.engine = 'CYCLES'
    
    # === Step 2: Create Dense Base Geometry ===
    # Multiply size by scale directly to avoid needing to apply transforms later
    bpy.ops.mesh.primitive_plane_add(size=2.0 * scale, location=location)
    obj = bpy.context.active_object
    obj.name = object_name
    
    # Add Subdivision Surface modifier for heavy geometry (replacing manual edit-mode sub-D)
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 6        # High density for viewport preview
    subsurf.render_levels = 8 # Extremely dense for final Cycles render
    
    # === Step 3: Create Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    
    # THE MOST CRITICAL STEP: Tell Cycles to actually move the mesh, not just fake bump
    mat.cycles.displacement_method = 'DISPLACEMENT'
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear unnecessary default nodes
    for node in nodes:
        if node.type not in {'BSDF_PRINCIPLED', 'OUTPUT_MATERIAL'}:
            nodes.remove(node)
            
    principled = nodes.get("Principled BSDF")
    if not principled: 
        principled = nodes.new('ShaderNodeBsdfPrincipled')
    output = nodes.get("Material Output")
    
    # --- Procedural PBR Texture Generation ---
    # 1. Voronoi for structural cracks (simulating stone blocks)
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.feature = 'DISTANCE_TO_EDGE'
    voronoi.inputs['Scale'].default_value = 3.0
    
    # 2. Noise for fine surface grit
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 10.0
    noise.inputs['Detail'].default_value = 15.0
    
    # 3. Combine Voronoi and Noise to form the master Height Map
    math_mult = nodes.new('ShaderNodeMath')
    math_mult.operation = 'MULTIPLY'
    math_mult.inputs[1].default_value = 0.3
    links.new(noise.outputs['Fac'], math_mult.inputs[0])
    
    math_add = nodes.new('ShaderNodeMath')
    math_add.operation = 'ADD'
    links.new(voronoi.outputs['Distance'], math_add.inputs[0])
    links.new(math_mult.outputs['Value'], math_add.inputs[1])
    
    # 4. Base Color Ramp (Dark cracks, colored surface)
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.color_ramp.elements[0].color = (0.01, 0.01, 0.01, 1.0) 
    color_ramp.color_ramp.elements[1].color = material_color + (1.0,) 
    links.new(math_add.outputs['Value'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
    
    # 5. Roughness Ramp
    rough_ramp = nodes.new('ShaderNodeValToRGB')
    rough_ramp.color_ramp.elements[0].color = (0.7, 0.7, 0.7, 1.0)
    rough_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    links.new(math_add.outputs['Value'], rough_ramp.inputs['Fac'])
    links.new(rough_ramp.outputs['Color'], principled.inputs['Roughness'])
    
    # 6. Normal (Bump) Map
    bump = nodes.new('ShaderNodeBump')
    bump.inputs['Distance'].default_value = 0.2
    links.new(math_add.outputs['Value'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], principled.inputs['Normal'])
    
    # 7. True Displacement Node
    disp = nodes.new('ShaderNodeDisplacement')
    disp.inputs['Midlevel'].default_value = 0.0
    disp.inputs['Scale'].default_value = 0.5 * scale # Extrusion amount relative to scale
    links.new(math_add.outputs['Value'], disp.inputs['Height'])
    links.new(disp.outputs['Displacement'], output.inputs['Displacement'])
    
    # Assign material to object
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat
    
    # === Step 4: Add Angled Lighting ===
    # True displacement is invisible without sharp shadows. We add a sun if one isn't present.
    sun_exists = False
    for obj_lit in scene.objects:
        if obj_lit.type == 'LIGHT' and obj_lit.data.type == 'SUN':
            sun_exists = True
            break
            
    if not sun_exists:
        sun_data = bpy.data.lights.new(name="Sun_Displacement_Light", type='SUN')
        sun_data.energy = 5.0 # High strength to match tutorial
        sun_data.angle = 0.1  # Sharp shadows
        sun = bpy.data.objects.new(name="Sun_Displacement_Light", object_data=sun_data)
        scene.collection.objects.link(sun)
        
        # Position slightly above and angle to rake across the surface
        sun.location = (location[0], location[1], location[2] + 5)
        sun.rotation_euler = (math.radians(45), math.radians(45), 0)
        
    return f"Created '{object_name}' (PBR True Displaced Plane) with Cycles displacement at {location}"
```