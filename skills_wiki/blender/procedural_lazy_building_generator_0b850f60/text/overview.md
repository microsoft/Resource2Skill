# Procedural Lazy Building Generator

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Lazy Building Generator

* **Core Visual Mechanism**: The tutorial demonstrates a "lazy" approach to architectural modeling: starting with basic primitive blocks, applying textures, and using simple extrusions, knife cuts, and insets to quickly build 3D detail that matches the 2D texture. It heavily emphasizes *imperfection*—offsetting edge loops and vertices so the building looks slightly crooked, organic, and derelict rather than mathematically perfect. 
* **Why Use This Skill (Rationale)**: Hand-modeling every window, ledge, and beam of a background city is incredibly time-consuming. This "macro-to-micro" technique (blocking out shapes, adding random protrusions, and pushing in windows) combined with a tiny amount of randomized vertex displacement creates highly believable, lived-in background structures in seconds. 
* **Overall Applicability**: Perfect for cyberpunk cityscapes, dystopian environments, background matte paintings, or any dense urban scene where silhouette and atmospheric lighting matter more than up-close, subdivision-perfect topology.
* **Value Addition**: Transforms a basic cube into a complex architectural asset complete with randomized structural variations, recessed window panes, and multi-material setups (including emissive lights for night scenes).

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A simple `Cube` primitive scaled to building proportions (tall and rectangular).
  - **Topology Generation**: The cube is heavily subdivided using `bmesh.ops.subdivide_edges` to create a dense grid of quad faces.
  - **Macro Extrusions**: Random face groups on the sides are selected and extruded outwards using `bmesh.ops.extrude_discrete_faces` to form balconies, ledges, or chaotic structural blocks.
  - **Micro Insets (Windows)**: A high percentage of the remaining vertical faces are selected, discretely extruded, scaled inwards (inset), and translated backwards to create deep window recesses with frames.
  - **Imperfection Pass**: Every vertex is slightly translated by a random uniform amount to break up perfectly straight edges, giving the "derelict/crooked" look mentioned in the tutorial.

* **Step B: Materials & Shading**
  - **Material 0 (Wall)**: A procedural grungy concrete using a `Noise Texture` driving a `ColorRamp`, plugged into the `Principled BSDF` Base Color. Roughness is high (0.85).
  - **Material 1 (Lit Window)**: A warm, emissive material. Base color is near black, but `Emission` is set to a bright orange/yellow `(1.0, 0.6, 0.1)` with a strength of 5.0. 
  - **Material 2 (Dark Window)**: A glossy, dark material simulating unlit glass. Base color is `(0.01, 0.01, 0.01)` and Roughness is low (0.15).
  - *Note: Since the tutorial relies on an external photo texture which cannot be guaranteed in automated environments, this procedural 3-material setup replicates the visual outcome of the photo-bashed technique.*

* **Step C: Lighting & Rendering Context**
  - **Lighting**: This asset shines in low-key, moody night lighting (like the tutorial's example scene). The emissive windows provide striking contrast. 
  - **Engine**: EEVEE with `Bloom` enabled produces instant, beautiful light scatter around the lit windows. Cycles will accurately cast the window light onto neighboring extrusions.

* **Step D: Animation & Dynamics**
  - This is a static environmental asset. For variation, the agent can call the function multiple times with different locations and scales to generate an entire city block, as the randomness ensures no two buildings are identical.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Architecture Blockout | `bmesh` primitive + `subdivide_edges` | Creates a clean quad grid necessary for grid-aligned windows. |
| Extrusions & Windows | `bmesh.ops.extrude_discrete_faces` | Allows independent scaling and pushing of individual faces, perfectly simulating window insets and frames. |
| "Lazy" Derelict Look | Programmatic Vertex Jitter | Iterating over `bm.verts` and applying random micro-translations easily replicates the hand-offsetting of edge loops. |
| Texturing | Procedural Shader Nodes | Replaces the tutorial's reliance on downloaded images, making the skill 100% self-contained and reproducible. |

> **Feasibility Assessment**: 85% — The code perfectly captures the procedural philosophy, geometry generation, and lighting effect shown in the video. The only missing element is the specific real-world photographic textures used by Ian Hubert, which are replaced here with procedural grunge and glass materials.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "LazyBuilding",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.5, 0.5, 0.45),
    **kwargs,
) -> str:
    """
    Create a procedural, semi-derelict building block based on the "Lazy Tutorials" workflow.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created building object.
        location: (x, y, z) world-space base position.
        scale: Uniform scale factor multiplier.
        material_color: (R, G, B) base color for the building walls.
        **kwargs: width, depth, and height overrides.

    Returns:
        Status string describing the generated building.
    """
    import bpy
    import bmesh
    import random
    from mathutils import Vector

    # Parse dimensions
    b_width = kwargs.get("width", 2.0) * scale
    b_depth = kwargs.get("depth", 2.0) * scale
    b_height = kwargs.get("height", 6.0) * scale
    
    # Initialize mesh and object
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    scene.collection.objects.link(obj)
    
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    
    # Scale cube bounding box
    for v in bm.verts:
        v.co.x *= b_width
        v.co.y *= b_depth
        v.co.z *= b_height
        
    # Translate so the building base sits exactly at Z=0 relative to its origin
    for v in bm.verts:
        v.co.z += b_height / 2.0
        
    # Subdivide heavily to create the "grid" for architectural details
    bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=7, use_grid_fill=True)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=1, use_grid_fill=True)

    # 1. Macro Extrusions (Balconies, structural variation)
    faces = [f for f in bm.faces if abs(f.normal.z) < 0.1]
    num_extrusions = max(1, len(faces) // 20)
    extrude_candidates = random.sample(faces, min(num_extrusions, len(faces)))
    
    if extrude_candidates:
        ret = bmesh.ops.extrude_discrete_faces(bm, faces=extrude_candidates)
        for f in ret['faces']:
            center = f.calc_center_median()
            # Scale slightly to avoid perfectly coplanar overlapping walls
            for v in f.verts:
                v.co = center + (v.co - center) * random.uniform(0.85, 0.95)
            # Push outward
            bmesh.ops.translate(bm, vec=f.normal * random.uniform(0.3, 1.2) * scale, verts=f.verts)

    # 2. Window Insets
    bm.faces.ensure_lookup_table()
    side_faces = [f for f in bm.faces if abs(f.normal.z) < 0.1 and f.calc_area() > (0.02 * scale * scale)]
    
    # Randomly select a portion of the side grid to become windows
    window_faces = [f for f in side_faces if random.random() > 0.35]
    
    if window_faces:
        ret = bmesh.ops.extrude_discrete_faces(bm, faces=window_faces)
        new_window_faces = set(ret['faces'])
        
        for f in new_window_faces:
            center = f.calc_center_median()
            # Inset the face (scales it down to form the window frame)
            inset_factor = random.uniform(0.7, 0.85)
            for v in f.verts:
                v.co = center + (v.co - center) * inset_factor
            # Push inwards to create the recess depth
            recess_depth = random.uniform(0.05, 0.15) * scale
            bmesh.ops.translate(bm, vec=-f.normal * recess_depth, verts=f.verts)
    else:
        new_window_faces = set()

    # Assign materials mapping based on face type
    for f in bm.faces:
        if f in new_window_faces:
            # 1 = Lit Window (30% chance), 2 = Dark Window (70% chance)
            f.material_index = 1 if random.random() > 0.7 else 2
        else:
            # 0 = Wall
            f.material_index = 0

    # 3. Random perturbation for "lazy/crooked" derelict look
    perturb_amount = 0.015 * scale
    for v in bm.verts:
        v.co.x += random.uniform(-perturb_amount, perturb_amount)
        v.co.y += random.uniform(-perturb_amount, perturb_amount)
        v.co.z += random.uniform(-perturb_amount, perturb_amount)

    bm.to_mesh(mesh)
    bm.free()
    
    # --- Materials Setup ---
    # Wall Material (Grungy Concrete)
    mat_wall = bpy.data.materials.new(f"{object_name}_Wall")
    mat_wall.use_nodes = True
    nodes = mat_wall.node_tree.nodes
    links = mat_wall.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    
    noise = nodes.new("ShaderNodeTexNoise")
    noise.inputs['Scale'].default_value = 25.0
    
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.4
    ramp.color_ramp.elements[0].color = (*material_color, 1.0)
    ramp.color_ramp.elements[1].position = 0.6
    dark_color = (max(0, material_color[0]-0.2), max(0, material_color[1]-0.2), max(0, material_color[2]-0.2), 1.0)
    ramp.color_ramp.elements[1].color = dark_color
    
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    if bsdf:
        links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
        bsdf.inputs['Roughness'].default_value = 0.85
        
    # Lit Window Material (Emissive)
    mat_lit = bpy.data.materials.new(f"{object_name}_LitWindow")
    mat_lit.use_nodes = True
    bsdf_lit = mat_lit.node_tree.nodes.get("Principled BSDF")
    if bsdf_lit:
        bsdf_lit.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1.0)
        bsdf_lit.inputs['Roughness'].default_value = 0.2
        emission_color = (1.0, 0.6, 0.1, 1.0) # Warm orange/yellow light
        # Handle Blender 3.x vs 4.x Emission API changes
        if 'Emission Color' in bsdf_lit.inputs:
            bsdf_lit.inputs['Emission Color'].default_value = emission_color
        elif 'Emission' in bsdf_lit.inputs:
            bsdf_lit.inputs['Emission'].default_value = emission_color
        if 'Emission Strength' in bsdf_lit.inputs:
            bsdf_lit.inputs['Emission Strength'].default_value = 5.0
            
    # Dark Window Material (Glossy/Unlit)
    mat_dark = bpy.data.materials.new(f"{object_name}_DarkWindow")
    mat_dark.use_nodes = True
    bsdf_dark = mat_dark.node_tree.nodes.get("Principled BSDF")
    if bsdf_dark:
        bsdf_dark.inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1.0)
        bsdf_dark.inputs['Roughness'].default_value = 0.15
        
    # Append materials in exact order of indices (0, 1, 2)
    obj.data.materials.append(mat_wall)
    obj.data.materials.append(mat_lit)
    obj.data.materials.append(mat_dark)
    
    # Position object in world
    obj.location = Vector(location)
    
    # Apply EdgeSplit to retain hard architectural edges while smoothing the slight jitter
    for poly in mesh.polygons:
        poly.use_smooth = True
    mod = obj.modifiers.new(name="EdgeSplit", type='EDGE_SPLIT')
    mod.split_angle = 0.523599 # ~30 degrees
    
    return f"Created procedural building '{object_name}' with {len(mesh.polygons)} faces at {location}."
```