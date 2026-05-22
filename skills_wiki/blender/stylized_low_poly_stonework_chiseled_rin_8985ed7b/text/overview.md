# Stylized Low-Poly Stonework (Chiseled Ring)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized Low-Poly Stonework (Chiseled Ring)

* **Core Visual Mechanism**: **Procedural Degradation & Faceting**. The defining signature of this technique is turning perfect, uniform primitives into organic, hand-hewn "wonky" stones. This is achieved through a specific pipeline: Primitive Box $\rightarrow$ Add Subdivision Topology $\rightarrow$ Apply Random Vertex Displacement (Jitter) $\rightarrow$ Bevel Edges $\rightarrow$ Decimate (Collapse). The Decimate modifier forces the rounded, jittered geometry into sharp, irregular low-poly triangles, creating a chiseled look.
* **Why Use This Skill (Rationale)**: Hand-modeling individual low-poly stones to look naturally irregular is incredibly time-consuming. This procedural approach guarantees unique variations for every single stone without manual sculpting. The decimation pass creates distinct planar facets that catch light beautifully, a hallmark of modern stylized 3D art.
* **Overall Applicability**: Perfect for fantasy or stylized environments. Use this to generate well bases, castle turrets, ruined walls, cobblestone paths, or campfire rings. 
* **Value Addition**: It injects organic imperfection into geometric scenes. By using programmatic polar coordinate math instead of UI-based modifiers, an entire complex multi-tier architectural structure can be generated as a single, clean mesh object.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Primitive**: Simple 1x1x1 cubes.
  - **Transformation**: Scaled non-uniformly into elongated bricks.
  - **Topology**: Subdivided heavily to provide enough vertices for displacement. Vertices are moved using randomized noise (`random.uniform`).
  - **Polar Deformation**: The linear array of stones is mathematically wrapped around a central axis using sine/cosine functions, mapping the X-axis to the circumference.
  - **Modifiers**: Bevel (for edge rounding) followed by Decimate (Ratio: ~0.35) to collapse the geometry into sharp, stylized facets.
* **Step B: Materials & Shading**
  - **Shader**: Principled BSDF.
  - **Properties**: High roughness (`0.95`), low specular IOR (`0.1`) for a matte, dusty stone look.
  - **Variation**: The code assigns slightly shifted base colors (e.g., varying luminance and slight tint shifts) to different stones to make individual bricks readable.
* **Step C: Lighting & Rendering Context**
  - **Lighting**: Best paired with a soft HDRI or three-point lighting. The sharp planar facets created by the Decimate modifier rely on contrasting light and shadow to read properly. 
  - **Engine**: Fully compatible with both EEVEE and Cycles.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Base Stone Generation** | `bmesh.ops.create_cube` | Fast, lightweight primitive generation. |
| **Organic Wonkiness** | `bmesh` vertex manipulation | Applying programmatic random noise to vertex coordinates perfectly mimics the "Randomize Transform" UI tool. |
| **Circular Ring Wrap** | Polar Math in `bmesh` | While the tutorial uses the *Simple Deform (Bend)* modifier, doing the polar wrap mathematically in python is vastly more robust. It avoids bounding-box edge cases and allows us to merge multiple rings with different radii into a single, clean mesh object. |
| **Chiseled Facets** | Modifiers (Bevel + Decimate) | Appending these modifiers perfectly recreates the tutorial's destructive modeling pipeline in a non-destructive way. |

> **Feasibility Assessment**: 100%. This code fully reproduces the visual technique, the specific 3D shape (a multi-tiered well base), and the procedural low-poly aesthetic from the tutorial. 

#### 3b. Complete Reproduction Code

```python
def create_stylized_stone_ring(
    scene_name: str = "Scene",
    object_name: str = "WellStoneBase",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.55, 0.52, 0.58),  # Stylized purplish-gray stone
    **kwargs,
) -> str:
    """
    Creates a stylized, low-poly chiseled stone ring (like a well base).
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color.
        
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Create object
    mesh = bpy.data.meshes.new(object_name)
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    # --- Step 1: Material Setup with Variations ---
    materials = []
    # Create 3 slightly varied materials for visual distinction between stones
    for i in range(3):
        mat = bpy.data.materials.new(name=f"{object_name}_Mat_Var_{i}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Shift value and tint slightly
            variation = random.uniform(-0.06, 0.06)
            r = max(0.0, min(1.0, material_color[0] + variation))
            g = max(0.0, min(1.0, material_color[1] + variation))
            b = max(0.0, min(1.0, material_color[2] + variation + random.uniform(-0.02, 0.04)))
            
            bsdf.inputs['Base Color'].default_value = (r, g, b, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.95
            bsdf.inputs['Specular IOR Level'].default_value = 0.1
        materials.append(mat)
        obj.data.materials.append(mat)

    # --- Step 2: Mesh Generation ---
    bm = bmesh.new()
    
    # Configuration for a 3-tier well base
    rings_config = [
        {"radius": 1.40, "count": 12, "z": 0.00, "rot": 0.0, "height": 0.40, "thickness": 0.50},
        {"radius": 1.25, "count": 10, "z": 0.38, "rot": 0.3, "height": 0.35, "thickness": 0.40},
        {"radius": 1.35, "count": 11, "z": 0.72, "rot": 0.1, "height": 0.40, "thickness": 0.45},
    ]
    
    for config in rings_config:
        radius = config["radius"]
        stone_count = config["count"]
        z_offset = config["z"]
        rot_offset = config["rot"]
        height = config["height"]
        thickness = config["thickness"]
        
        circumference = 2 * math.pi * radius
        stone_length = circumference / stone_count
        actual_length = stone_length * 1.06  # Slight overlap to avoid gaps
        start_x = -circumference / 2.0 + stone_length / 2.0
        
        # Track starting index so we only process vertices for this specific ring
        start_vert_idx = len(bm.verts)
        
        # Generate bricks in a straight line along X-axis
        for i in range(stone_count):
            mat_idx = random.randint(0, len(materials) - 1)
            start_face_idx = len(bm.faces)
            
            ret = bmesh.ops.create_cube(bm, size=1.0)
            verts = ret['verts']
            
            # Dimension variations
            var_len = actual_length * random.uniform(0.85, 1.15)
            var_height = height * random.uniform(0.85, 1.15)
            var_thick = thickness * random.uniform(0.8, 1.2)
            
            pos_x = start_x + i * stone_length
            pos_y = random.uniform(-0.03, 0.03)  # Depth jitter
            
            for v in verts:
                v.co.x = (v.co.x * var_len) + pos_x
                v.co.y = (v.co.y * var_thick) + pos_y
                v.co.z = (v.co.z * var_height) + z_offset
                
            # Assign material variation
            bm.faces.ensure_lookup_table()
            for f in bm.faces[start_face_idx:]:
                f.material_index = mat_idx
                
        # Subdivide the geometry to give the displacement/decimation something to work with
        bm.verts.ensure_lookup_table()
        ring_edges = set(e for v in bm.verts[start_vert_idx:] for e in v.link_edges)
        bmesh.ops.subdivide_edges(bm, edges=list(ring_edges), cuts=2, use_grid_fill=True)
        
        # Apply organic noise & polar mapping (Bend into ring)
        bm.verts.ensure_lookup_table()
        for v in bm.verts[start_vert_idx:]:
            # 1. Randomize / Jitter
            v.co.x += random.uniform(-0.02, 0.02)
            v.co.y += random.uniform(-0.02, 0.02)
            v.co.z += random.uniform(-0.02, 0.02)
            
            # 2. Polar Wrap (Mathematically bends around Z axis)
            orig_x = v.co.x
            orig_y = v.co.y
            
            theta = (orig_x / circumference) * (2 * math.pi) + rot_offset
            r = radius + orig_y
            
            v.co.x = r * math.sin(theta)
            v.co.y = r * math.cos(theta)

    # Finalize BMesh
    bm.to_mesh(mesh)
    bm.free()
    
    # --- Step 3: Modifiers for Stylized Low-Poly Aesthetic ---
    # Bevel rounds out the sharp corners before decimation
    bevel_mod = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel_mod.width = 0.04
    bevel_mod.segments = 2
    
    # Decimate collapses the dense/jittered/beveled mesh into chunky triangles
    decimate_mod = obj.modifiers.new(name="Decimate", type='DECIMATE')
    decimate_mod.ratio = 0.35
    
    # Ensure flat shading for faceted look
    for p in mesh.polygons:
        p.use_smooth = False
        
    # --- Step 4: Final Placement ---
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    return f"Created '{object_name}' (Stylized Well Base) at {location} with 3 stone rings."
```