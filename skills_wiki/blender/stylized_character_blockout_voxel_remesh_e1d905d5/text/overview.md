# Stylized Character Blockout & Voxel Remesh Prep

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized Character Blockout & Voxel Remesh Prep

* **Core Visual Mechanism**: Utilizing basic primitives (spheres, cones) modified via non-uniform scaling and tapering to block out a stylized, bulbous character (a fish). This specific arrangement creates a proportional volume that perfectly emulates the initial stages of a digital sculpting workflow, ready to be unified via a Voxel Remesh.
* **Why Use This Skill (Rationale)**: Trying to pull long, thin extrusions (like fins or tails) directly out of a single sphere during sculpting often stretches the topology and destroys the mesh surface. Blocking out the silhouette using separate, intersecting primitive objects ensures accurate initial volume and proportions, drastically reducing the amount of manual sculpting required.
* **Overall Applicability**: Character design, creature modeling, stylized prop creation, and any workflow that relies on Dynamic Topology (Dyntopo) or Voxel Remeshing.
* **Value Addition**: Automates the tedious structural blockout phase. It replaces the default primitives with a complete, logically grouped character base mesh, immediately establishing a stylized silhouette that can be used as-is for low-poly rendering or taken straight into Sculpt Mode.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Body**: Uses a standard UV Sphere. It is procedurally stretched along the X-axis, with programmatic tapering applied to the negative X-axis (tail) and slight expansion on the positive X-axis (head) to create a teardrop fish shape.
  - **Fins**: Created from Cone primitives. They are flattened along the Y-axis and rotated to sweep backwards along the body. 
  - **Symmetry**: Symmetrical elements (pectoral fins, eyes, pupils) are generated on the negative Y-axis (right side) and utilize a `Mirror` modifier across the Y-axis, referencing the main body as the mirror origin.

* **Step B: Materials & Shading**
  - Emulates the vertex painting shown in the tutorial using Principled BSDF shaders.
  - **Body Material**: A vibrant base color (default Red), with Roughness set to `0.3` to mimic the shiny, wet look of a fish or fresh digital clay.
  - **Extremity Material**: A mathematically offset secondary color (Orange/Yellow) applied to the fins and tail.
  - **Eyes**: High-contrast, low-roughness (`0.1`) black and white materials to give the character a lively, glossy gaze.

* **Step C: Lighting & Rendering Context**
  - Best viewed in EEVEE for real-time stylized feedback. 
  - Complemented well by a soft HDRI or a strong three-point lighting setup to catch sharp specular highlights on the low-roughness, bulbous geometry.

* **Step D: Animation & Dynamics**
  - The hierarchical setup (all parts parented to the main body) allows for easy skeletal rigging or simple object-level wiggle animations.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Base shapes & tapering** | `bmesh` vertex math | Allows for precise, smooth tapering of the sphere (teardrop body) and flattening of cones without managing complex modifier stacks. |
| **Symmetry** | `Mirror` Modifier | Keeps the geometry procedural and lightweight, exactly mirroring the digital sculpting symmetry settings. |
| **Colors & Shading** | Shader Node Tree | Procedurally applies the painted visual style using Principled BSDFs, bypassing the manual vertex-painting process. |

> **Feasibility Assessment**: 80% — This code perfectly reproduces the geometric blockout, proportions, and painted shading of the fish. The remaining 20% involves the manual, localized hand-sculpted details (like the carved mouth and individual scale indentations) which are subjective and require human pen-strokes in Sculpt Mode.

#### 3b. Complete Reproduction Code

```python
def create_stylized_fish(
    scene_name: str = "Scene",
    object_name: str = "StylizedFish",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.05, 0.05),
    **kwargs,
) -> str:
    """
    Create a Stylized Fish base mesh ready for sculpting or stylized rendering.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated objects.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) primary color of the fish body.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector, Matrix
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Create master collection
    fish_col = bpy.data.collections.new(object_name)
    scene.collection.children.link(fish_col)

    # === Step 1: Material Setup ===
    mat_body = bpy.data.materials.new(name=f"{object_name}_BodyMat")
    mat_body.use_nodes = True
    bsdf_body = mat_body.node_tree.nodes.get("Principled BSDF")
    bsdf_body.inputs["Base Color"].default_value = (*material_color, 1.0)
    bsdf_body.inputs["Roughness"].default_value = 0.3

    # Derive fin color (brighter, slightly shifted hue)
    fin_color = (min(material_color[0] * 1.2, 1.0), min(material_color[1] + 0.25, 1.0), material_color[2])
    mat_fin = bpy.data.materials.new(name=f"{object_name}_FinMat")
    mat_fin.use_nodes = True
    bsdf_fin = mat_fin.node_tree.nodes.get("Principled BSDF")
    bsdf_fin.inputs["Base Color"].default_value = (*fin_color, 1.0)
    bsdf_fin.inputs["Roughness"].default_value = 0.3
    
    mat_eye_w = bpy.data.materials.new(name=f"{object_name}_EyeWhite")
    mat_eye_w.use_nodes = True
    mat_eye_w.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (1, 1, 1, 1)
    mat_eye_w.node_tree.nodes.get("Principled BSDF").inputs["Roughness"].default_value = 0.1

    mat_eye_b = bpy.data.materials.new(name=f"{object_name}_EyeBlack")
    mat_eye_b.use_nodes = True
    mat_eye_b.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (0.02, 0.02, 0.02, 1)
    mat_eye_b.node_tree.nodes.get("Principled BSDF").inputs["Roughness"].default_value = 0.1

    # Helper function for mesh creation
    def make_mesh(name, bmesh_func, mat):
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        fish_col.objects.link(obj)
        bm = bmesh.new()
        bmesh_func(bm)
        bm.to_mesh(mesh)
        bm.free()
        obj.data.materials.append(mat)
        for p in mesh.polygons:
            p.use_smooth = True
        return obj

    # === Step 2: Geometry Generation ===
    
    # Body
    def body_shape(bm):
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1.0)
        for v in bm.verts:
            x, y, z = v.co.x, v.co.y, v.co.z
            x *= 1.2
            y *= 0.5
            z *= 0.7
            # Taper tail (negative X)
            if x < 0:
                t = abs(x) / 1.2
                y *= (1.0 - t * 0.6)
                z *= (1.0 - t * 0.6)
            # Round head (positive X)
            else:
                t = x / 1.2
                y *= (1.0 + t * 0.1)
                z *= (1.0 + t * 0.1)
            v.co = Vector((x, y, z))
            
    body_obj = make_mesh(f"{object_name}_Body", body_shape, mat_body)

    # Tail Fin
    def tail_shape(bm):
        bmesh.ops.create_cone(bm, segments=16, radius1=0.6, radius2=0.0, depth=1.2)
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0,0,0), matrix=Matrix.Rotation(-math.pi/2, 3, 'Y'))
        for v in bm.verts:
            v.co.y *= 0.1 
            v.co.z *= 1.5 
            v.co.x -= 1.1 

    tail_obj = make_mesh(f"{object_name}_Tail", tail_shape, mat_fin)

    # Dorsal Fin (Top)
    def top_fin_shape(bm):
        bmesh.ops.create_cone(bm, segments=16, radius1=0.5, radius2=0.0, depth=0.8)
        for v in bm.verts:
            v.co.y *= 0.1 
            v.co.x *= 1.5 
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0,0,0), matrix=Matrix.Rotation(-math.pi/8, 3, 'Y'))
        for v in bm.verts:
            v.co.z += 0.7 
            v.co.x -= 0.2
            
    top_fin_obj = make_mesh(f"{object_name}_TopFin", top_fin_shape, mat_fin)

    # Pectoral Fin (Side)
    def side_fin_shape(bm):
        bmesh.ops.create_cone(bm, segments=16, radius1=0.4, radius2=0.0, depth=1.0)
        for v in bm.verts:
            v.co.y *= 0.1
        # Sweep backwards and angle outwards
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0,0,0), matrix=Matrix.Rotation(-math.pi/2, 3, 'Y'))
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0,0,0), matrix=Matrix.Rotation(-math.pi/6, 3, 'X'))
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0,0,0), matrix=Matrix.Rotation(-math.pi/6, 3, 'Z'))
        for v in bm.verts:
            v.co.x += 0.2
            v.co.y -= 0.55
            v.co.z -= 0.2

    fin_R = make_mesh(f"{object_name}_Pectoral_R", side_fin_shape, mat_fin)
    
    # Eyes
    def eye_shape(bm):
        bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=16, radius=0.25)
        for v in bm.verts:
            v.co.y *= 0.8
            v.co.x += 0.6 
            v.co.y -= 0.35 
            v.co.z += 0.15 
            
    eye_w_R = make_mesh(f"{object_name}_Eye_R", eye_shape, mat_eye_w)

    def pupil_shape(bm):
        bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=16, radius=0.1)
        for v in bm.verts:
            v.co.y *= 0.5
            v.co.x += 0.7   
            v.co.y -= 0.52  
            v.co.z += 0.15

    eye_b_R = make_mesh(f"{object_name}_Pupil_R", pupil_shape, mat_eye_b)

    # === Step 3: Hierarchy & Symmetry Setup ===
    
    objects_to_parent = [tail_obj, top_fin_obj, fin_R, eye_w_R, eye_b_R]
    objects_to_mirror = [fin_R, eye_w_R, eye_b_R]

    for obj in objects_to_mirror:
        mod = obj.modifiers.new("Mirror", 'MIRROR')
        mod.mirror_object = body_obj
        mod.use_axis[0] = False
        mod.use_axis[1] = True # Mirror across Y-axis
        
    for obj in objects_to_parent:
        obj.parent = body_obj

    # === Step 4: Final Positioning ===
    body_obj.location = Vector(location)
    body_obj.scale = Vector((scale, scale, scale))

    return f"Created Stylized Fish Blockout '{object_name}' at {location} with {len(objects_to_parent) + 1} mesh components."
```