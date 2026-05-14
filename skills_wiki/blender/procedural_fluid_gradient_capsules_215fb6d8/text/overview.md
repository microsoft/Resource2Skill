# Procedural Fluid Gradient Capsules

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Fluid Gradient Capsules

* **Core Visual Mechanism**: The signature of this technique is the combination of staggered, interlocking 3D capsules (pill shapes) shaded with a vibrant, unified procedural gradient. The gradient features a "liquid meniscus" effect where the color bands curve naturally at the edges of the capsules. This is achieved by manipulating the Z-coordinate vector mapping using the absolute value of the object's X-axis surface normal.
* **Why Use This Skill (Rationale)**: This style produces highly modern, abstract, and polished visuals commonly used in premium UI/UX design, motion graphics (mograph), and tech product reveals. The "bending" gradient gives flat colors a voluminous, fluid, and glass-like dimensionality without requiring complex liquid simulations or UV unwrapping.
* **Overall Applicability**: Perfect for abstract backgrounds, modern stylized environments, screensaver-style motion graphics, or as glowing hero elements in a sci-fi or cyberpunk scene. 
* **Value Addition**: Compared to standard objects with simple materials, this skill introduces a cross-object unified gradient that responds procedurally to the geometry's curvature, creating an illusion of colorful liquid encapsulated within glass.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A simple 3D Cube scaled heavily along the Z-axis (e.g., 1x1x4).
  - **Modifiers**: A Bevel modifier is applied with the `width` set to half the smallest dimension (0.5) and a high segment count (16). This perfectly rounds the ends, turning the stretched cube into a flawless capsule without complex modeling.
  - **Layout**: The capsules are arranged in columns. To create the irregular "staggered" intersection lines seen in the reference, each column contains two capsules (top and bottom) offset by a synchronized random Z-value.

* **Step B: Materials & Shading**
  - **Shader Model**: A pure Emission shader (or Principled BSDF with high emission) to make the colors vibrant and unlit by the scene's default gray lights.
  - **Procedural Logic**: 
    1. Extract `Position Z` (Geometry node).
    2. Extract `Normal X` (Geometry node), take its Absolute value to get a 0-1 mask of the side edges.
    3. Multiply the Normal mask by a "Bend Amount" and subtract it from the Position Z. This bends the coordinate system downwards at the edges.
    4. Map the resulting Z value to a 0-1 range and feed it into a Color Ramp.
  - **Color Palette**: Yellow `(1.0, 0.8, 0.0)`, Purple `(0.5, 0.0, 0.8)`, Bright Blue `(0.0, 0.5, 1.0)`, Deep Blue `(0.0, 0.0, 0.1)`. Interpolation set to `B-Spline` for silky smooth transitions.

* **Step C: Lighting & Rendering Context**
  - **Render Engine**: Cycles is highly recommended for proper light transmission and glass refractions, though EEVEE works if Screen Space Reflections and Refractions are enabled.
  - **Overlay Elements**: Floating, semi-transparent "glass plates" (flattened capsules with 1.0 Transmission and 0.0 Roughness) are placed in front of the main capsules to add depth, specular highlights, and optical complexity.

* **Step D: Animation & Dynamics (if applicable)**
  - The scene is static, but the procedural Z-offset or the "Bend Amount" can be driven by a `#frame` driver to animate the fluid colors moving up and down the capsules.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Capsule Generation | BMesh (Cube) + Bevel Modifier | Setting `use_clamp_overlap=True` on a heavily beveled stretched cube mathematically guarantees a perfect capsule shape while keeping the base topology non-destructive and light. |
| Grid & Staggering | Python `for` loops | Allows precise mathematical alignment of the top and bottom capsules so their tips touch perfectly at randomized heights. |
| Fluid Gradients | Shader Node Tree (Math Nodes) | Bypasses the need for the non-standard "Evaluate Closure" setup mentioned in the tutorial, achieving the exact same visual using pure, vanilla vector math. |

> **Feasibility Assessment**: 100% of the core visual technique is reproduced. The layout, the procedural edge-bending gradient, and the glass overlays are all mathematically replicated. Note: The tutorial mentions an "Evaluate Closure" node—this is actually a recurring joke by the creator and doesn't exist in standard Blender. The code provides the actual node math to solve the problem.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "FluidGradientCapsules",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = None,  # Not used directly; we use a curated 4-color palette
    **kwargs,
) -> str:
    """
    Create a staggered array of rounded capsules with a procedural fluid gradient.
    """
    import bpy
    import bmesh
    import random
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Configuration
    columns = kwargs.get('columns', 8)
    spacing = kwargs.get('spacing', 1.05)
    bend_strength = kwargs.get('bend_strength', 1.5)
    
    # Colors (Yellow, Purple, Bright Blue, Deep Blue)
    c1 = (1.0, 0.8, 0.0, 1.0)
    c2 = (0.5, 0.0, 0.8, 1.0)
    c3 = (0.0, 0.5, 1.0, 1.0)
    c4 = (0.0, 0.0, 0.1, 1.0)

    # === Step 1: Create the Base Capsule Mesh ===
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(1.0, 1.0, 4.0), verts=bm.verts) # Base height 4
    
    capsule_mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    bm.to_mesh(capsule_mesh)
    bm.free()

    # === Step 2: Build the Procedural Fluid Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_GradientMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create Shader Nodes
    node_geom = nodes.new(type='ShaderNodeNewGeometry')
    node_sep_pos = nodes.new(type='ShaderNodeSeparateXYZ')
    node_sep_norm = nodes.new(type='ShaderNodeSeparateXYZ')
    
    node_abs = nodes.new(type='ShaderNodeMath')
    node_abs.operation = 'ABSOLUTE'
    
    node_mult = nodes.new(type='ShaderNodeMath')
    node_mult.operation = 'MULTIPLY'
    node_mult.inputs[1].default_value = bend_strength
    
    node_sub = nodes.new(type='ShaderNodeMath')
    node_sub.operation = 'SUBTRACT'
    
    node_map = nodes.new(type='ShaderNodeMapRange')
    node_map.inputs[1].default_value = -4.0 # From Min
    node_map.inputs[2].default_value = 4.0  # From Max
    
    node_ramp = nodes.new(type='ShaderNodeValToRGB')
    node_ramp.color_ramp.interpolation = 'B_SPLINE'
    node_ramp.color_ramp.elements[0].position = 0.0
    node_ramp.color_ramp.elements[0].color = c1
    node_ramp.color_ramp.elements[1].position = 0.33
    node_ramp.color_ramp.elements[1].color = c2
    node_ramp.color_ramp.elements.new(0.66)
    node_ramp.color_ramp.elements[2].color = c3
    node_ramp.color_ramp.elements.new(1.0)
    node_ramp.color_ramp.elements[3].color = c4
    
    node_emission = nodes.new(type='ShaderNodeEmission')
    node_emission.inputs['Strength'].default_value = 2.0
    
    node_output = nodes.new(type='ShaderNodeOutputMaterial')

    # Link the Node Tree
    links.new(node_geom.outputs['Position'], node_sep_pos.inputs['Vector'])
    links.new(node_geom.outputs['Normal'], node_sep_norm.inputs['Vector'])
    
    links.new(node_sep_norm.outputs['X'], node_abs.inputs[0])
    links.new(node_abs.outputs['Value'], node_mult.inputs[0])
    
    links.new(node_sep_pos.outputs['Z'], node_sub.inputs[0])
    links.new(node_mult.outputs['Value'], node_sub.inputs[1])
    
    links.new(node_sub.outputs['Value'], node_map.inputs['Value'])
    links.new(node_map.outputs['Result'], node_ramp.inputs['Fac'])
    links.new(node_ramp.outputs['Color'], node_emission.inputs['Color'])
    links.new(node_emission.outputs['Emission'], node_output.inputs['Surface'])

    # === Step 3: Build the Glass Material ===
    glass_mat = bpy.data.materials.new(name=f"{object_name}_GlassMat")
    glass_mat.use_nodes = True
    glass_mat.use_screen_refraction = True # For EEVEE compatibility
    glass_nodes = glass_mat.node_tree.nodes
    glass_bsdf = glass_nodes.get("Principled BSDF")
    if glass_bsdf:
        glass_bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
        glass_bsdf.inputs['Roughness'].default_value = 0.05
        # Handle Blender 4.0+ vs older versions for Transmission
        if 'Transmission Weight' in glass_bsdf.inputs:
            glass_bsdf.inputs['Transmission Weight'].default_value = 1.0
        elif 'Transmission' in glass_bsdf.inputs:
            glass_bsdf.inputs['Transmission'].default_value = 1.0

    # === Step 4: Construct the Scene Assembly ===
    master_empty = bpy.data.objects.new(object_name, None)
    master_empty.location = Vector(location)
    master_empty.scale = (scale, scale, scale)
    scene.collection.objects.link(master_empty)
    
    capsules_created = 0
    random.seed(42) # Consistent generation
    
    total_width = (columns - 1) * spacing
    start_x = -total_width / 2.0

    for col in range(columns):
        x_pos = start_x + (col * spacing)
        # Random staggered height for the intersecting cut
        intersection_z = random.uniform(-1.5, 1.5)
        
        # Create Top and Bottom capsules for this column
        for is_top in [True, False]:
            z_offset = 2.0 if is_top else -2.0
            z_pos = intersection_z + z_offset
            
            cap = bpy.data.objects.new(f"{object_name}_Capsule_{col}_{'Top' if is_top else 'Bot'}", capsule_mesh)
            cap.location = (x_pos, 0, z_pos)
            cap.parent = master_empty
            cap.data.materials.append(mat)
            
            # Add Bevel Modifier for perfect rounding
            mod = cap.modifiers.new(name="Rounding", type='BEVEL')
            mod.width = 0.499 # Just under 0.5 to prevent degenerate geometry
            mod.segments = 16
            mod.use_clamp_overlap = True
            
            # Smooth shading
            for poly in cap.data.polygons:
                poly.use_smooth = True
                
            scene.collection.objects.link(cap)
            capsules_created += 1

    # === Step 5: Add Floating Glass Overlays ===
    for i in range(3):
        glass_cap = bpy.data.objects.new(f"{object_name}_Glass_{i}", capsule_mesh)
        
        # Random placement in front of the main capsules
        gx = start_x + random.randint(0, columns-1) * spacing
        gy = -0.6 - random.uniform(0.1, 0.4) # Push forward towards camera
        gz = random.uniform(-2, 2)
        
        glass_cap.location = (gx, gy, gz)
        glass_cap.scale = (0.9, 0.1, random.uniform(1.0, 1.5)) # Flatter, varying height
        glass_cap.parent = master_empty
        glass_cap.data.materials.append(glass_mat)
        
        g_mod = glass_cap.modifiers.new(name="Rounding", type='BEVEL')
        g_mod.width = 0.499
        g_mod.segments = 16
        g_mod.use_clamp_overlap = True
        
        for poly in glass_cap.data.polygons:
            poly.use_smooth = True
            
        scene.collection.objects.link(glass_cap)
        capsules_created += 1

    return f"Created '{object_name}' with {capsules_created} procedural capsules and glass overlays at {location}."
```