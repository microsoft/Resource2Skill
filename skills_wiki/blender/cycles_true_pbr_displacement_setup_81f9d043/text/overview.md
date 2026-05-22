# Cycles True PBR Displacement Setup

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Cycles True PBR Displacement Setup

* **Core Visual Mechanism**: Converting a 2D height map (or procedural height data) into actual 3D geometric deformation at render time. This is achieved by combining a highly subdivided mesh, the Cycles render engine, a Displacement shader node, and setting the material's surface settings to "Displacement Only".
* **Why Use This Skill (Rationale)**: While Normal and Bump maps fake surface detail by altering how light bounces off a flat plane, True Displacement physically moves the vertices. This creates realistic self-shadowing, accurate occlusion, and broken silhouettes, which are vital for photorealistic close-ups of natural terrain, brick walls, or rocky surfaces.
* **Overall Applicability**: Essential for environment design, architectural visualization, and photorealistic prop rendering where macro-surface texture heavily dictates the lighting.
* **Value Addition**: Transforms a flat, lightweight primitive into a highly detailed, physically accurate surface without the need for destructive, manual high-poly sculpting.


### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A standard Plane primitive.
  - **Modifiers**: A Subdivision Surface modifier (set to 'Simple' to avoid smoothing the square borders) generates enough real vertices for the displacement map to push around. The tutorial uses Edit Mode subdivisions, but a modifier is much cleaner and non-destructive.
* **Step B: Materials & Shading**
  - **Shader Model**: Principled BSDF with base color and roughness.
  - **Displacement**: Height data is routed into a `Displacement` node, scaled down, and then plugged into the `Displacement` socket of the Material Output.
  - **Key Engine Setting**: The material must have its Settings > Surface > Displacement dropdown changed from "Bump Only" to "Displacement Only". 
* **Step C: Lighting & Rendering Context**
  - **Engine**: Cycles is strictly required for this specific material-based true displacement workflow.
  - **Lighting**: A Sun light with an energy of `5.0` and a slightly expanded angle (`11.4°`) is positioned to cast strong, defining shadows across the newly created micro-geometry.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Geometry Density | Mesh Primitive + `SUBSURF` Modifier | Provides a clean, parametric way to generate the dense vertex data required for true displacement without permanently freezing the geometry. |
| PBR Textures | Procedural Shader Nodes (Voronoi + Noise) | The tutorial relies on a 3rd-party downloaded image texture. To ensure this script is **fully self-contained** and avoids brittle hardcoded file paths, I built a procedural "Rock Wall" node setup that mathematically replicates the required base color, roughness, and displacement height maps. |
| True Displacement | Material Settings + Cycles Engine | Automatically switches the engine to Cycles and forces the `displacement_method` to 'DISPLACEMENT', which is the core mechanism of the tutorial. |

> **Feasibility Assessment**: 95%. The core technical workflow (subdivision + Cycles material displacement + lighting) is replicated 100%. The visual result uses a procedural approximation of a rock wall instead of the downloaded image file to ensure the code executes successfully on any machine.

#### 3b. Complete Reproduction Code

```python
def create_pbr_displaced_plane(
    scene_name: str = "Scene",
    object_name: str = "PBR_Rock_Plane",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 2.0,
    material_color: tuple = (0.35, 0.25, 0.18), # Base rocky brown
    **kwargs
) -> str:
    """
    Create a highly subdivided plane with a procedural PBR rock material utilizing True Cycles Displacement.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created plane.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color of the rock surface.
        **kwargs: Additional overrides (e.g., subdivision_levels).
        
    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    subdivision_levels = kwargs.get("subdivision_levels", 6)

    # === Step 1: Engine Setup ===
    # True displacement requires Cycles
    scene.render.engine = 'CYCLES'
    if hasattr(scene.cycles, 'feature_set'):
        scene.cycles.feature_set = 'SUPPORTED'

    # === Step 2: Create Base Geometry ===
    bpy.ops.mesh.primitive_plane_add(size=2, location=location)
    plane = bpy.context.active_object
    plane.name = object_name
    plane.scale = (scale, scale, scale)
    
    # Add Subdivision Surface modifier for dense geometry
    subsurf = plane.modifiers.new(name="Displacement_Subdiv", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = subdivision_levels
    subsurf.render_levels = subdivision_levels + 1 # Even more detail at render time

    # === Step 3: Build Procedural PBR Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    plane.data.materials.append(mat)
    
    # CRITICAL: Enable True Displacement in material settings
    mat.cycles.displacement_method = 'DISPLACEMENT'
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
        
    # Output & Shader
    mat_out = nodes.new('ShaderNodeOutputMaterial')
    mat_out.location = (1000, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (600, 0)
    links.new(bsdf.outputs['BSDF'], mat_out.inputs['Surface'])
    
    # Texture Coordinates
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-800, 0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    
    # Procedural Shape: Voronoi for rock chunks/cracks
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-500, 200)
    voronoi.feature = 'DISTANCE_TO_EDGE' # Creates a crack network
    voronoi.inputs['Scale'].default_value = 4.0
    links.new(mapping.outputs['Vector'], voronoi.inputs['Vector'])
    
    # Invert Voronoi so chunks bulge outwards and cracks are deep
    invert = nodes.new('ShaderNodeMath')
    invert.operation = 'SUBTRACT'
    invert.inputs[0].default_value = 1.0
    invert.location = (-300, 200)
    links.new(voronoi.outputs['Distance'], invert.inputs[1])
    
    # Procedural Detail: Noise for rock surface grain
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-500, -100)
    noise.inputs['Scale'].default_value = 15.0
    noise.inputs['Detail'].default_value = 15.0
    noise.inputs['Roughness'].default_value = 0.65
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    
    # Scale down noise impact
    mult_noise = nodes.new('ShaderNodeMath')
    mult_noise.operation = 'MULTIPLY'
    mult_noise.inputs[1].default_value = 0.2
    mult_noise.location = (-300, -100)
    links.new(noise.outputs['Fac'], mult_noise.inputs[0])
    
    # Combine Chunks and Grain to create final Height Map
    combine_height = nodes.new('ShaderNodeMath')
    combine_height.operation = 'ADD'
    combine_height.location = (-100, 50)
    links.new(invert.outputs['Value'], combine_height.inputs[0])
    links.new(mult_noise.outputs['Value'], combine_height.inputs[1])
    
    # Displacement Setup
    disp = nodes.new('ShaderNodeDisplacement')
    disp.location = (600, -300)
    disp.inputs['Scale'].default_value = 0.2  # Match tutorial displacement strength
    disp.inputs['Midlevel'].default_value = 0.0
    links.new(combine_height.outputs['Value'], disp.inputs['Height'])
    links.new(disp.outputs['Displacement'], mat_out.inputs['Displacement'])
    
    # Color Map Generation
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (200, 150)
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (0.05, 0.04, 0.03, 1.0) # Dark crevices
    color_ramp.color_ramp.elements[1].position = 0.8
    color_ramp.color_ramp.elements[1].color = (*material_color, 1.0) # Main rock color
    links.new(combine_height.outputs['Value'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
    
    # Roughness Map Generation
    rough_ramp = nodes.new('ShaderNodeValToRGB')
    rough_ramp.location = (200, -100)
    rough_ramp.color_ramp.elements[0].position = 0.0
    rough_ramp.color_ramp.elements[0].color = (0.9, 0.9, 0.9, 1.0) # High roughness
    rough_ramp.color_ramp.elements[1].position = 1.0
    rough_ramp.color_ramp.elements[1].color = (0.6, 0.6, 0.6, 1.0)
    links.new(noise.outputs['Fac'], rough_ramp.inputs['Fac'])
    links.new(rough_ramp.outputs['Color'], bsdf.inputs['Roughness'])
    
    # === Step 4: Lighting Setup ===
    # Add the strong Sun light from the tutorial if one doesn't exist to show off shadows
    if not any(light.type == 'SUN' for light in bpy.data.lights):
        bpy.ops.object.light_add(type='SUN', location=(5, -5, 5))
        sun = bpy.context.active_object
        sun.name = "Displacement_Sun"
        sun.data.energy = 5.0
        sun.data.angle = math.radians(11.4)
        sun.rotation_euler = (math.radians(45), 0, math.radians(45))

    return f"Created '{object_name}' with procedural true Cycles displacement and Subdiv level {subdivision_levels}."
```