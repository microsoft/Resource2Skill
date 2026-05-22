# Modular Symmetric Character Block-Out

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Modular Symmetric Character Block-Out

* **Core Visual Mechanism**: The technique uses basic geometric primitives (cubes and low-resolution cylinders) to establish the silhouette, proportions, and structural foundation of a character. It relies on a "half-mesh" approach where only one side of the body is modeled, and a Mirror Modifier dynamically generates the opposite side, merging seamlessly at the center axis.
* **Why Use This Skill (Rationale)**: Blocking out is the most critical first step in character modeling. By using separate, simple geometric blocks before creating continuous topology, you can quickly adjust limb lengths, shoulder width, and overall stance without worrying about edge flows or deformation. Keeping cylinder resolutions low (e.g., 8 vertices) ensures that when the limbs are eventually joined to the torso, matching the vertex counts is manageable.
* **Overall Applicability**: Essential for any character creation workflow, from stylized low-poly avatars to complex mecha or realistic creatures. It defines the T-pose (or A-pose) blueprint that will later be rigged and animated.
* **Value Addition**: Replaces chaotic, free-form modeling with a structured, mathematically mirrored foundation. It guarantees perfect symmetry and provides a non-destructive way to tweak proportions before committing to a unified mesh.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Torso**: A subdivided or scaled Cube bisected along the X-axis. The center face (at X=0) is deleted to allow the Mirror modifier to clip and merge the halves without creating interior geometry.
  - **Limbs**: Cylinders reduced to 8 vertices (N-gon caps optional, but usually removed later). 8 vertices provide a clean octagonal profile that is easy to subdivide and attach to the torso's grid topology.
  - **Head & Extremities**: Simple cubes (often with a Subdivision Surface modifier for the head to create a rounded box) scaled to represent the mass of hands and feet.
  - **Symmetry**: A Mirror Modifier applied on the X-axis, with "Clipping" enabled to lock center vertices to the origin.

* **Step B: Materials & Shading**
  - Uses a standard Principled BSDF. During the block-out phase, materials are purely for visual separation or aesthetic placeholder.
  - Base Color: A stylized purple `(0.2, 0.05, 0.4)` to match the tutorial's space-themed character.
  - Roughness: `0.7` to prevent distracting specular highlights while assessing the silhouette.

* **Step C: Lighting & Rendering Context**
  - Designed for real-time viewport evaluation (EEVEE or solid view). 
  - Standard three-point lighting or a basic HDRI is sufficient, as the focus is purely on proportional volumes.

* **Step D: Animation & Dynamics (if applicable)**
  - Characters are blocked out in a standard "T-Pose" or "A-Pose" with limbs straight and aligned to global axes. This is a mandatory prerequisite for clean armature rigging and weight painting later down the pipeline.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Proportional Assembly | `bmesh` scripting | Allows programmatic generation, scaling, and precise positioning of multiple primitive shapes into a single mesh object without relying on fragile `bpy.ops` selection states. |
| Perfect Symmetry | Mirror Modifier | Natively handles X-axis duplication and center-line clipping, identical to the manual workflow shown in the tutorial. |
| Soft Head Shape | Subdivision Surface | Turns a rigid cube into a smooth, rounded box, perfectly matching the stylized spherical-but-squarish head of the reference character. |

> **Feasibility Assessment**: 100% of the core block-out technique is reproduced. The code algorithmically constructs the torso, generates the right-side limbs, applies the mirror modifier, and sets up a parented sub-surfaced head, resulting in a perfectly proportioned T-pose base mesh.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "CharacterBlockout",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.05, 0.4),
    **kwargs,
) -> str:
    """
    Create a Modular Symmetric Character Block-Out in the active Blender scene.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the character objects.
        location: (x, y, z) world-space position for the character origin.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the blockout material.
        **kwargs: Overrides for proportions (head_size, torso_width, arm_length, etc.)

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector, Euler

    # --- Parameter Overrides ---
    head_size = kwargs.get("head_size", 0.8)
    torso_width = kwargs.get("torso_width", 1.0)
    torso_height = kwargs.get("torso_height", 1.4)
    torso_depth = kwargs.get("torso_depth", 0.6)
    arm_length = kwargs.get("arm_length", 1.2)
    leg_length = kwargs.get("leg_length", 1.5)
    arm_radius = kwargs.get("arm_radius", 0.15)
    leg_radius = kwargs.get("leg_radius", 0.18)

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # === Step 1: Create Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.7

    # === Step 2: Build the Body (Mirrored Base) ===
    mesh = bpy.data.meshes.new(f"{object_name}_Body")
    body_obj = bpy.data.objects.new(f"{object_name}_Body", mesh)
    scene.collection.objects.link(body_obj)
    body_obj.location = location
    body_obj.scale = (scale, scale, scale)
    body_obj.data.materials.append(mat)

    # Add Mirror Modifier
    mod = body_obj.modifiers.new(name="Mirror", type='MIRROR')
    mod.use_axis[0] = True
    mod.use_clip = True

    bm = bmesh.new()

    # --- 2A: Torso Half ---
    ret = bmesh.ops.create_cube(bm, size=1.0)
    torso_verts = ret['verts']
    for v in torso_verts:
        v.co.x *= torso_width / 2.0
        v.co.x += torso_width / 4.0  # Shift so left boundary is exactly at x=0
        v.co.y *= torso_depth
        v.co.z *= torso_height
        v.co.z += torso_height / 2.0 + leg_length  # Raise to hip level

    # Snap center verts exactly to 0 and delete the internal symmetry face
    for v in torso_verts:
        if v.co.x < 0.01:
            v.co.x = 0.0
            
    center_faces = [f for f in bm.faces if all(v.co.x < 0.001 for v in f.verts)]
    bmesh.ops.delete(bm, geom=center_faces, context='FACES')

    # --- 2B: Arm (T-Pose) ---
    ret = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=8, radius1=arm_radius, radius2=arm_radius, depth=arm_length)
    arm_verts = ret['verts']
    # Rotate to point outward along X-axis
    bmesh.ops.rotate(bm, verts=arm_verts, cent=(0,0,0), matrix=Euler((0, math.pi/2, 0)).to_matrix())
    shoulder_z = leg_length + torso_height - arm_radius * 2
    shoulder_x = torso_width / 2.0
    bmesh.ops.translate(bm, verts=arm_verts, vec=Vector((shoulder_x + arm_length/2.0, 0, shoulder_z)))

    # --- 2C: Hand (Flattened Cube) ---
    ret = bmesh.ops.create_cube(bm, size=1.0)
    hand_verts = ret['verts']
    for v in hand_verts:
        v.co.x *= arm_radius * 2.5
        v.co.y *= arm_radius * 1.5
        v.co.z *= arm_radius * 2.5
    bmesh.ops.translate(bm, verts=hand_verts, vec=Vector((shoulder_x + arm_length + arm_radius*1.25, 0, shoulder_z)))

    # --- 2D: Leg ---
    ret = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=8, radius1=leg_radius, radius2=leg_radius, depth=leg_length)
    leg_verts = ret['verts']
    leg_x = torso_width / 4.0
    bmesh.ops.translate(bm, verts=leg_verts, vec=Vector((leg_x, 0, leg_length / 2.0)))

    # --- 2E: Foot (Elongated Cube) ---
    ret = bmesh.ops.create_cube(bm, size=1.0)
    foot_verts = ret['verts']
    for v in foot_verts:
        v.co.x *= leg_radius * 2.0
        v.co.y *= leg_radius * 3.0  # Elongate forward
        v.co.z *= leg_radius * 1.5  # Flatten
    bmesh.ops.translate(bm, verts=foot_verts, vec=Vector((leg_x, leg_radius * 1.0, leg_radius * 0.75)))

    # Finalize Body Mesh
    bm.to_mesh(mesh)
    bm.free()

    # === Step 3: Build the Head ===
    head_mesh = bpy.data.meshes.new(f"{object_name}_Head")
    head_obj = bpy.data.objects.new(f"{object_name}_Head", head_mesh)
    scene.collection.objects.link(head_obj)
    
    # Parent head to body
    head_obj.parent = body_obj
    
    # Position relative to body root
    head_z_pos = leg_length + torso_height + head_size/2.0 + 0.1
    head_obj.location = (0, 0, head_z_pos)
    head_obj.data.materials.append(mat)

    bm_head = bmesh.new()
    bmesh.ops.create_cube(bm_head, size=head_size)
    bm_head.to_mesh(head_mesh)
    bm_head.free()

    # Add Subsurf to head to make it a rounded stylized block
    subsurf = head_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 3
    subsurf.render_levels = 3

    # Enable smooth shading
    for obj in [body_obj, head_obj]:
        for p in obj.data.polygons:
            p.use_smooth = True

    return f"Created Character Blockout '{object_name}' (Body + Head) at {location} in T-Pose."
```