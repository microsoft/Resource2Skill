# Procedural Stylized Head Base

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Stylized Head Base

* **Core Visual Mechanism**: This skill mimics the foundational workflow of 3D sculpting (blocking out primary forms) using procedural spatial fields. Instead of manually using a "Grab Brush" with spherical falloff to pull out the jaw, nose, and ears from a high-density primitive (as shown in the tutorial), the script applies mathematical distance-based falloffs to deform specific anatomical regions. It generates a single cohesive head mesh and supplements it with separated UV-sphere eyeballs.

* **Why Use This Skill (Rationale)**: Hand-sculpting a caricature relies entirely on manual tablet strokes and artistic intuition. By mathematically codifying these "grab" strokes, an AI agent can instantly generate organic, recognizable character bases. The separation of the eyeballs from the skin mesh allows for distinct material properties (glossy vs. sub-surface scattering) and prevents geometry stretching in the eye sockets, a core principle of character modeling.

* **Overall Applicability**: Ideal for generating background characters, gargoyles, statues, or proxy meshes for crowd populations. It serves as an excellent starting point for stylized character design.

* **Value Addition**: Compared to standard primitives, this skill provides a complex, recognizable organic silhouette. It introduces foundational character topology (eye sockets, cranium, jaw, ears) without relying on heavy external assets.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Primitive**: An Icosphere with 4 levels of subdivision provides an evenly distributed, high-density mesh (mimicking the tutorial's `Ctrl+R` Remesh step).
  - **Deformation Logic**: Spatial coordinate filtering (`x, y, z`) acts as the "brush". Vertices within specific spatial radii are displaced to form the chin, nose, cranium, and ears. 
  - **Modifier**: A Subdivision Surface modifier (Level 1 viewport, 2 render) is applied post-deformation to smooth any jagged artifacts caused by the mathematical displacement.

* **Step B: Materials & Shading**
  - **Skin Material**: A Principled BSDF shader utilizing a fleshy base color, moderate roughness (`0.45`), and a slight Subsurface Scattering weight (`0.15`) to simulate skin's light absorption.
  - **Eye Material**: A completely separate glossy material (`Base Color: (0.02, 0.02, 0.02)`) applied to the distinct UV spheres, capturing the stylized "beady-eyed" look from the tutorial.

* **Step C: Lighting & Rendering Context**
  - **Lighting**: Best presented with a strong rim/backlight and a softer key light to highlight the organic contours of the nose and brow ridges.
  - **Engine**: Works flawlessly in both EEVEE and Cycles, though Subsurface Scattering looks significantly more realistic in Cycles.

* **Step D: Animation & Dynamics**
  - Because the eyes are generated as separate objects and explicitly parented to the main head, they can be rotated independently for animation (e.g., looking around).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Base Shape Block-out** | `bmesh` spatial vertex manipulation | Replicates the tutorial's "Grab Brush" by applying procedural distance falloffs to pull out the nose, chin, and ears from the base primitive. |
| **Clean Topology** | Subdivided Icosphere + Subsurf Modifier | Icospheres have evenly distributed triangles, preventing the pole-pinching of UV spheres when stretched. The modifier mimics the tutorial's Voxel Remesh step. |
| **Eyeballs** | `bmesh.ops.create_uvsphere` | Appending separate geometry for the eyes prevents the facial mesh from severely stretching, keeping the materials independent. |

> **Feasibility Assessment**: 75% — The code successfully automates the block-out phase (Grab brush shaping, eye sockets, symmetry, and sub-objects), producing a highly recognizable caricature silhouette. However, procedural math cannot replicate the fine, hand-drawn creases, wrinkles, and lip lines achieved with the tutorial's Draw and Crease brushes. 

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "StylizedHead",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.4, 0.3),
    **kwargs,
) -> str:
    """
    Create a procedural stylized head base in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the created objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base skin color in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector

    # Target scene and collection
    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene
    target_collection = scene.collection
    
    # === Step 1: Create Base Head Mesh ===
    mesh = bpy.data.meshes.new(object_name)
    obj = bpy.data.objects.new(object_name, mesh)
    target_collection.objects.link(obj)
    
    bm = bmesh.new()
    # High-density base to mimic the sculpting remesh workflow
    bmesh.ops.create_icosphere(bm, subdivisions=4, radius=1.0)
    
    # Procedural "Grab Brush" application via spatial falloffs
    for v in bm.verts:
        x, y, z = v.co.x, v.co.y, v.co.z
        
        # 1. Jaw and Chin (Pull down and forward)
        if z < -0.1:
            inf = min(1.0, (-z - 0.1) / 0.9)
            z -= inf * 0.7 
            y -= inf * 0.25 
            x *= (1.0 - inf * 0.35) # Narrow the jaw
            
        # 2. Cranium (Bulbous expansion at top)
        if z > 0.1:
            inf = min(1.0, (z - 0.1) / 0.9)
            x *= (1.0 + inf * 0.15)
            y *= (1.0 + inf * 0.2)
            z += inf * 0.2
            
        # 3. Nose (Pull outwards at front middle)
        dist_nose = Vector((x, y + 0.8, z + 0.1)).length
        if dist_nose < 0.6:
            inf = (1.0 - (dist_nose / 0.6)) ** 2
            y -= inf * 0.6
            z -= inf * 0.15
                
        # 4. Eye Sockets (Push geometry inwards to make room for eyeballs)
        dist_l = Vector((x - 0.35, y + 0.7, z - 0.2)).length
        dist_r = Vector((x + 0.35, y + 0.7, z - 0.2)).length
        if dist_l < 0.35:
            inf = (1.0 - (dist_l / 0.35)) ** 2
            y += inf * 0.3
        if dist_r < 0.35:
            inf = (1.0 - (dist_r / 0.35)) ** 2
            y += inf * 0.3
            
        # 5. Ears (Pull outwards at sides)
        dist_ear_l = Vector((x - 0.8, y - 0.1, z)).length
        dist_ear_r = Vector((x + 0.8, y - 0.1, z)).length
        if dist_ear_l < 0.4:
            inf = (1.0 - (dist_ear_l / 0.4)) ** 2
            x += inf * 0.45
            y -= inf * 0.15
            z += inf * 0.15
        if dist_ear_r < 0.4:
            inf = (1.0 - (dist_ear_r / 0.4)) ** 2
            x -= inf * 0.45
            y -= inf * 0.15
            z += inf * 0.15
            
        # 6. Neck (Pull down bottom back/center)
        if z < -0.6 and abs(x) < 0.4 and y > -0.3:
            inf = min(1.0, (-z - 0.6) / 0.6)
            z -= inf * 0.6
            y += inf * 0.2

        v.co = Vector((x, y, z))

    bm.to_mesh(mesh)
    bm.free()
    
    # Set smooth shading
    for poly in mesh.polygons:
        poly.use_smooth = True
        
    # Add subdivision to mimic the smooth "Remesh" look
    subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.levels = 1
    subdiv.render_levels = 2
    
    # === Step 2: Build Materials ===
    # Skin Material
    skin_mat = bpy.data.materials.new(name=f"{object_name}_Skin")
    skin_mat.use_nodes = True
    bsdf = skin_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.45
        # Attempt to add Subsurface Scattering safely across Blender versions
        if 'Subsurface Weight' in bsdf.inputs:
            bsdf.inputs['Subsurface Weight'].default_value = 0.15
        elif 'Subsurface' in bsdf.inputs:
            bsdf.inputs['Subsurface'].default_value = 0.15
    obj.data.materials.append(skin_mat)
    
    # Eye Material
    eye_mat = bpy.data.materials.new(name=f"{object_name}_Eye")
    eye_mat.use_nodes = True
    eye_bsdf = eye_mat.node_tree.nodes.get("Principled BSDF")
    if eye_bsdf:
        eye_bsdf.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1.0)
        eye_bsdf.inputs['Roughness'].default_value = 0.1
        
    # === Step 3: Create & Parent Eyes ===
    eye_locs = [(0.35, -0.62, 0.2), (-0.35, -0.62, 0.2)]
    created_objects = [obj]
    
    for i, eloc in enumerate(eye_locs):
        eye_name = f"{object_name}_Eye_{'L' if i==0 else 'R'}"
        emesh = bpy.data.meshes.new(eye_name)
        eye_obj = bpy.data.objects.new(eye_name, emesh)
        target_collection.objects.link(eye_obj)
        
        ebm = bmesh.new()
        bmesh.ops.create_uvsphere(ebm, u_segments=32, v_segments=16, radius=0.12)
        ebm.to_mesh(emesh)
        ebm.free()
        
        for poly in emesh.polygons:
            poly.use_smooth = True
            
        eye_obj.data.materials.append(eye_mat)
        eye_obj.parent = obj
        eye_obj.location = eloc
        created_objects.append(eye_obj)
        
    # === Step 4: Finalize Transform ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    return f"Created '{object_name}' at {location} with {len(created_objects)} linked objects (Head + Eyes)."
```