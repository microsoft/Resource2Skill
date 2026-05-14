# Procedural Rigid-Body Wrecking Ball & Breakable Wall

## Analysis

Here is a comprehensive breakdown and reproducible script for the rigid-body chain and wrecking ball simulation.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Rigid-Body Wrecking Ball & Breakable Wall

* **Core Visual Mechanism**: This technique relies on interlocking, concave 3D meshes (chain links) driven entirely by Blender's Rigid Body physics engine. By starting the chain at an angle and letting gravity take over, it creates a perfectly natural pendulum swing. The wrecking ball smashes into a perfectly stacked wall of cubes that are configured to remain completely still until the exact moment of impact.
* **Why Use This Skill (Rationale)**: Hand-animating a chain swinging and a wall exploding is tedious and often looks artificial. Using rigid body physics ensures physically accurate momentum transfer, chaotic scatter, and natural settling of debris.
* **Overall Applicability**: This pattern is perfect for satisfying physics simulations, destruction animations, industrial visualizations, and generating organic "rubble" or scattered objects for static environment scenes.
* **Value Addition**: It introduces dynamic interaction to a scene. Instead of static props, it creates a cause-and-effect relationship between objects, adding motion and realism that is difficult to achieve with keyframes alone.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Chain Links**: Built starting from a standard Torus. BMesh is used to move half the vertices along the Y-axis, stretching it into a pill shape. The links are duplicated, translated, and alternatingly rotated 90 degrees to interlock.
  - **Wrecking Ball**: A UV Sphere attached (joined) directly to the final chain link.
  - **Wall**: A 3D grid of cubes instantiated with a microscopic gap between them.
* **Step B: Materials & Shading**
  - **Chain/Ball**: Metallic Principled BSDF (Metallic = 1.0, Roughness = 0.3) for an iron/steel look.
  - **Wall Cubes**: Matte Principled BSDF (Roughness = 0.8) to resemble bricks or painted wood.
* **Step C: Lighting & Rendering Context**
  - Works beautifully in both EEVEE and Cycles. Shadows are highly recommended to accentuate the depth of the falling debris.
* **Step D: Animation & Dynamics**
  - **Anchor**: `Passive` rigid body (keeps the chain attached to the sky).
  - **Chain Links**: `Active` rigid bodies. Crucially, their collision shape is set to `Mesh`. Standard shapes (like Convex Hull) wrap around the holes, preventing the links from interlocking. 
  - **Wall**: `Active` rigid bodies set to `Start Deactivated`. This prevents the stacked cubes from jittering or exploding under their own weight before the ball hits them.
  - **World Settings**: `Substeps Per Frame` is increased to 20 to prevent the fast-moving chain links from clipping through each other and breaking the chain.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Chain link modeling** | `bpy.ops.mesh` + `bmesh` | Allows us to stretch a basic Torus into a clean, closed loop procedurally. |
| **Chain assembly** | Python loops + Matrix Math | Calculates exact 3D positioning and alternating rotation to perfectly interlock the links before simulating. |
| **Physics setup** | `obj.rigid_body` API | Automatically handles the physics assignments without requiring manual scene baking. |

> **Feasibility Assessment**: 100% reproduction. The resulting script mathematically generates the chains, sets up the physics properties, and stacks the wall. Simply running the code and pressing `Spacebar` (Play) in Blender will trigger the wrecking ball simulation.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "WreckingBall",
    location: tuple = (0, 0, 10),
    scale: float = 1.0,
    material_color: tuple = (0.8, 0.1, 0.1),
    **kwargs,
) -> str:
    """
    Create a functional Rigid-Body Wrecking Ball and breakable wall.
    Press Spacebar to play the simulation after running.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for created objects.
        location: (x, y, z) location of the highest pivot point (Anchor).
        scale: Uniform scale factor for all sizes.
        material_color: (R, G, B) color of the breakable wall boxes.
        
    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector, Matrix

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    scene.frame_set(1) # Ensure we are at start frame for physics initialization

    # --- Dimensions ---
    link_major = 0.15 * scale
    link_minor = 0.03 * scale
    link_stretch_half = 0.2 * scale
    link_offset = 0.60 * scale
    sphere_radius = 0.6 * scale
    anchor_size = 0.8 * scale
    cube_size = 0.5 * scale

    # --- Helper: Rigid Body Setup ---
    def add_rb(obj, rb_type='ACTIVE', shape='CONVEX_HULL', mass=1.0, deactivated=False, margin=0.0):
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        # Add physics if it doesn't exist
        if obj.rigid_body is None:
            bpy.ops.rigidbody.object_add()
            
        obj.rigid_body.type = rb_type
        obj.rigid_body.collision_shape = shape
        if rb_type == 'ACTIVE':
            obj.rigid_body.mass = mass
        if deactivated:
            obj.rigid_body.use_start_deactivated = True
        if margin > 0:
            obj.rigid_body.use_margin = True
            obj.rigid_body.collision_margin = margin

    # --- Helper: Material Setup ---
    def make_material(name, color, metallic, roughness):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*color, 1.0)
            bsdf.inputs["Metallic"].default_value = metallic
            bsdf.inputs["Roughness"].default_value = roughness
        return mat

    mat_chain = make_material(f"{object_name}_ChainMat", (0.8, 0.8, 0.8), 1.0, 0.3)
    mat_cube = make_material(f"{object_name}_CubeMat", material_color, 0.0, 0.8)
    mat_floor = make_material(f"{object_name}_FloorMat", (0.05, 0.05, 0.05), 0.0, 1.0)

    # --- 1. Base Chain Link Creation ---
    bpy.ops.mesh.primitive_torus_add(major_radius=link_major, minor_radius=link_minor, location=(0,0,0))
    base_link = bpy.context.active_object
    base_link.name = "TempBaseLink"
    
    # Stretch the torus using BMesh
    bm = bmesh.new()
    bm.from_mesh(base_link.data)
    for v in bm.verts:
        if v.co.y > 0: 
            v.co.y += link_stretch_half
        else: 
            v.co.y -= link_stretch_half
    bm.to_mesh(base_link.data)
    bm.free()
    
    # Orient link to hang straight down
    base_link.rotation_euler = (math.pi/2, 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    base_link.data.materials.append(mat_chain)
    
    # --- 2. Build the Chain ---
    num_links = 14
    links = []
    pivot_loc = Vector(location)
    
    # Start the chain at a 45 degree angle so it swings automatically
    rot_mat = Matrix.Rotation(math.radians(45), 4, 'Y')
    
    for i in range(num_links):
        obj = base_link.copy()
        scene.collection.objects.link(obj)
        obj.name = f"{object_name}_Link_{i}"
        
        z_offset = -i * link_offset
        local_rot = Matrix.Rotation(i * math.pi/2, 4, 'Z') # Alternate 90deg rotations
        mat_world = Matrix.Translation(pivot_loc) @ rot_mat @ Matrix.Translation(Vector((0, 0, z_offset))) @ local_rot
        
        obj.matrix_world = mat_world
        links.append(obj)
        
    bpy.data.objects.remove(base_link) # Cleanup temp object

    # --- 3. Anchor (Top Pivot) ---
    bpy.ops.mesh.primitive_cube_add(size=anchor_size, location=location)
    anchor = bpy.context.active_object
    anchor.name = f"{object_name}_Anchor"
    anchor.data.materials.append(mat_chain)
    
    # Join the first link into the anchor
    bpy.ops.object.select_all(action='DESELECT')
    anchor.select_set(True)
    links[0].select_set(True)
    bpy.context.view_layer.objects.active = anchor
    bpy.ops.object.join()
    
    # Make anchor completely static
    add_rb(anchor, rb_type='PASSIVE', shape='MESH', margin=0.01 * scale)

    # --- 4. Wrecking Ball ---
    link_bottom_offset = 0.35 * scale
    z_offset_sphere = -(num_links - 1) * link_offset - link_bottom_offset - sphere_radius
    sphere_mat_world = Matrix.Translation(pivot_loc) @ rot_mat @ Matrix.Translation(Vector((0, 0, z_offset_sphere)))
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=sphere_radius)
    sphere = bpy.context.active_object
    sphere.name = f"{object_name}_Ball"
    sphere.matrix_world = sphere_mat_world
    sphere.data.materials.append(mat_chain)
    
    # Join the last link into the sphere
    bpy.ops.object.select_all(action='DESELECT')
    sphere.select_set(True)
    links[-1].select_set(True)
    bpy.context.view_layer.objects.active = sphere
    bpy.ops.object.join()
    
    # Make the sphere active and extremely heavy
    add_rb(sphere, rb_type='ACTIVE', shape='MESH', mass=50.0, margin=0.01 * scale)

    # --- 5. Middle Links Physics ---
    for i in range(1, num_links - 1):
        add_rb(links[i], rb_type='ACTIVE', shape='MESH', mass=1.0, margin=0.01 * scale)

    # --- 6. Floor ---
    # Calculate exactly where the bottom of the arc is
    L = (num_links - 1) * link_offset + link_bottom_offset + sphere_radius
    floor_z = pivot_loc.z - L - (0.1 * scale) # Floor is just below the lowest swing point
    
    bpy.ops.mesh.primitive_plane_add(size=30 * scale, location=(pivot_loc.x, pivot_loc.y, floor_z))
    floor = bpy.context.active_object
    floor.name = f"{object_name}_Floor"
    floor.data.materials.append(mat_floor)
    add_rb(floor, rb_type='PASSIVE', shape='BOX', margin=0.01 * scale)

    # --- 7. Breakable Cube Wall ---
    spacing = cube_size + (0.01 * scale) # Leave a microscopic gap so physics don't explode
    boxes_created = 0
    
    # Position wall exactly at X=pivot.x, which is the bottom-most point of the swing
    for ix in range(-2, 3):     # 5 boxes wide
        for iy in range(-1, 2): # 3 boxes deep
            for iz in range(6): # 6 boxes high
                bx = pivot_loc.x + ix * spacing
                by = pivot_loc.y + iy * spacing
                bz = floor_z + (cube_size / 2) + iz * spacing
                
                bpy.ops.mesh.primitive_cube_add(size=cube_size, location=(bx, by, bz))
                box = bpy.context.active_object
                box.name = f"{object_name}_WallBox_{ix}_{iy}_{iz}"
                box.data.materials.append(mat_cube)
                
                # 'Start Deactivated' prevents the wall from trembling before impact
                add_rb(box, rb_type='ACTIVE', shape='BOX', mass=0.2, deactivated=True, margin=0.01 * scale)
                boxes_created += 1

    # --- 8. Increase Physics Fidelity ---
    # Because chain links are interlocking complex shapes moving fast, 
    # we need more substeps to prevent them phasing through each other
    if scene.rigidbody_world:
        scene.rigidbody_world.substeps_per_frame = 20
        scene.rigidbody_world.solver_iterations = 10

    return f"Created physics simulation '{object_name}' with a {num_links}-link chain and a {boxes_created}-block wall."
```