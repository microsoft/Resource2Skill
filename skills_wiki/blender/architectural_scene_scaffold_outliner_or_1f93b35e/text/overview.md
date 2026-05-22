# Architectural Scene Scaffold & Outliner Organization

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Architectural Scene Scaffold & Outliner Organization

* **Core Visual Mechanism**: Establishing a structured baseline for architectural visualization. Rather than a specific complex shape, the core mechanism here is the **hierarchical and environmental setup**: creating a master controller (Empty), procedurally generating base architectural elements (L-shaped walls and floor), categorizing objects into specific Outliner Collections (Meshes, Lights, Cameras), and configuring physically accurate rendering (Cycles + Area Lights).

* **Why Use This Skill (Rationale)**: Architectural scenes quickly become the most complex scenes in 3D modeling, often containing thousands of objects. Setting up strict collection management, correct real-world scale logic, and baseline physically-based rendering (PBR) lighting is a mandatory prerequisite. Without this scaffold, scenes become unmanageable and lighting behaves unpredictably.

* **Overall Applicability**: Used as the absolute starting point for any interior or exterior architectural visualization, retail store design, or level design block-out. 

* **Value Addition**: Compared to just dropping a default cube, this skill provides a production-ready environment. It guarantees that meshes, lights, and cameras are segregated, that the render engine is optimized for architectural realism (Cycles with denoising), and provides a scaled physical corner to begin placing CAD imports or detailed props.


### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: Procedurally generated using `bmesh`. It creates an L-shaped wall segment with calculated thickness and height, alongside a floor plane. 
  - **Topology**: Extremely low-poly (ngons/quads) to serve purely as a bounding box or structural block-out.
  - **Hierarchy**: All meshes, lights, and cameras are parented to a central `PLAIN_AXES` Empty, allowing the entire room environment to be moved, rotated, or scaled as a single modular unit.

* **Step B: Materials & Shading**
  - **Shader Model**: Principled BSDF.
  - **Color**: Configurable via parameters (defaulting to a neutral off-white/light-grey wall color `(0.8, 0.8, 0.8)`). 
  - **Roughness**: Set to `0.9` to mimic standard matte architectural interior paint/drywall.

* **Step C: Lighting & Rendering Context**
  - **Lighting**: Utilizes an `AREA` light. Area lights are the industry standard for arch-viz because they provide soft, realistic light dispersion mimicking windows or large ceiling panels.
  - **Camera**: A camera is spawned with a wider focal length (24mm) commonly used in interior photography to capture enclosed spaces, automatically tracked to look into the corner of the room.
  - **Render Engine**: Configured to `CYCLES` with `use_denoising` enabled, directly reflecting the tutorial's guidance for achieving realistic architectural renders.

* **Step D: Animation & Dynamics**
  - None required for the static structural scaffold.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Scene Organization | `bpy.data.collections.new()` | Crucial for arch-viz workflows to separate geometry, lights, and cameras for easy visibility toggling. |
| Architectural Shell | `bmesh` scripting | Allows exact parametric control over wall thickness, length, and height rather than guessing with primitive scaling. |
| Rendering Setup | `scene.render` API | Automates the switch to Cycles and Denoising, skipping manual UI configuration. |

> **Feasibility Assessment**: 100% reproduction of the foundational workflow. The script perfectly encapsulates the tutorial's emphasis on Outliner organization, object types, and render engine setup, automating the tedious setup phase of architectural design.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "ArchScaffold",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.8, 0.8),
    **kwargs,
) -> str:
    """
    Create an Architectural Scene Scaffold in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Base name for the created objects and collections.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color for the walls.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated scene.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Master Controller & Collections ===
    # Create an Empty to control the entire scaffold
    empty_data = bpy.data.objects.new(object_name, None)
    empty_data.empty_display_type = 'PLAIN_AXES'
    empty_data.empty_display_size = 2 * scale
    empty_data.location = Vector(location)
    scene.collection.objects.link(empty_data)

    # Establish architectural collections
    col_names = ["Arch_Meshes", "Arch_Lights", "Arch_Cameras"]
    collections = {}
    for name in col_names:
        prefixed_name = f"{object_name}_{name}"
        if prefixed_name not in bpy.data.collections:
            new_col = bpy.data.collections.new(prefixed_name)
            scene.collection.children.link(new_col)
        collections[name] = bpy.data.collections[prefixed_name]

    # === Step 2: Build Base Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_WallMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.9 # Matte wall paint

    # === Step 3: Procedural Geometry (Walls & Floor) ===
    thickness = 0.5 * scale
    height = 5.0 * scale
    length = 10.0 * scale

    # 3a. L-Shaped Walls
    wall_mesh = bpy.data.meshes.new(f"{object_name}_WallMesh")
    wall_obj = bpy.data.objects.new(f"{object_name}_Walls", wall_mesh)
    collections["Arch_Meshes"].objects.link(wall_obj)
    wall_obj.parent = empty_data
    
    bm_wall = bmesh.new()
    v1 = bm_wall.verts.new((0, 0, 0))
    v2 = bm_wall.verts.new((length, 0, 0))
    v3 = bm_wall.verts.new((length, thickness, 0))
    v4 = bm_wall.verts.new((thickness, thickness, 0))
    v5 = bm_wall.verts.new((thickness, length, 0))
    v6 = bm_wall.verts.new((0, length, 0))
    
    f_bottom = bm_wall.faces.new((v1, v2, v3, v4, v5, v6))
    res = bmesh.ops.extrude_face_region(bm_wall, geom=[f_bottom])
    extruded_verts = [elem for elem in res['geom'] if isinstance(elem, bmesh.types.BMVert)]
    bmesh.ops.translate(bm_wall, vec=Vector((0, 0, height)), verts=extruded_verts)
    
    bmesh.ops.recalc_face_normals(bm_wall, faces=bm_wall.faces)
    bm_wall.to_mesh(wall_mesh)
    bm_wall.free()
    wall_obj.data.materials.append(mat)

    # 3b. Floor
    floor_mesh = bpy.data.meshes.new(f"{object_name}_FloorMesh")
    floor_obj = bpy.data.objects.new(f"{object_name}_Floor", floor_mesh)
    collections["Arch_Meshes"].objects.link(floor_obj)
    floor_obj.parent = empty_data
    floor_obj.location = (length/2, length/2, 0)
    
    bm_floor = bmesh.new()
    s = length / 2
    fv1 = bm_floor.verts.new((-s, -s, 0))
    fv2 = bm_floor.verts.new((s, -s, 0))
    fv3 = bm_floor.verts.new((s, s, 0))
    fv4 = bm_floor.verts.new((-s, s, 0))
    bm_floor.faces.new((fv1, fv2, fv3, fv4))
    
    bm_floor.to_mesh(floor_mesh)
    bm_floor.free()
    floor_obj.data.materials.append(mat)

    # === Step 4: Architectural Lighting ===
    light_data = bpy.data.lights.new(name=f"{object_name}_AreaData", type='AREA')
    light_data.energy = 500.0 * (scale ** 2)
    light_data.size = 5.0 * scale
    light_data.shape = 'SQUARE'
    
    light_obj = bpy.data.objects.new(name=f"{object_name}_AreaLight", object_data=light_data)
    collections["Arch_Lights"].objects.link(light_obj)
    light_obj.parent = empty_data
    light_obj.location = (length/2, length/2, height - (0.5 * scale))

    # === Step 5: Camera Setup ===
    cam_data = bpy.data.cameras.new(name=f"{object_name}_CamData")
    cam_data.lens = 24.0 # Wide angle, standard for interiors
    
    cam_obj = bpy.data.objects.new(name=f"{object_name}_Camera", object_data=cam_data)
    collections["Arch_Cameras"].objects.link(cam_obj)
    cam_obj.parent = empty_data
    cam_obj.location = (length * 0.8, length * 0.8, height * 0.6)
    
    # Point camera at the corner
    target_pos = Vector((thickness, thickness, height * 0.4))
    direction = target_pos - Vector(cam_obj.location)
    cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    # === Step 6: Render Settings ===
    scene.render.engine = 'CYCLES'
    if hasattr(scene.cycles, 'use_denoising'):
        scene.cycles.use_denoising = True
    scene.cycles.samples = 128

    return f"Created '{object_name}' Architectural Scaffold at {location} with organized collections, Area Light, and Wide-Angle Camera."
```