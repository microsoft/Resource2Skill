# Advanced 4-Point Studio Lighting Environment

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Advanced 4-Point Studio Lighting Environment

* **Core Visual Mechanism**: This pattern builds an entire product visualization studio setup. It centers around an "infinity cove" (a seamless, procedurally generated curved backdrop) that removes the horizon line, creating a clean gradient background. The lighting relies on a 4-point Area Light setup: a soft overhead Key light, two contrasting rim lights (warm and cool) flanking the subject, and an angled front fill light with reduced specularity to prevent blown-out highlights on the camera-facing side.
* **Why Use This Skill (Rationale)**: Lighting is the defining factor in 3D presentation. Default primitives look flat in empty space. This specific setup uses color temperature contrast (warm orange vs. cool blue) on the rim lights to visually separate the subject from the backdrop while the overhead key light provides soft, flattering form definition.
* **Overall Applicability**: Essential for product rendering, portfolio prop presentation, character turnarounds, and look-dev environments. Any time a hero asset needs to be showcased in a professional, distraction-free environment.
* **Value Addition**: Instantly upgrades flat, unlit assets into portfolio-ready renders. It provides a perfectly smoothed procedural backdrop without relying on boolean or bevel modifiers, ensuring perfect shading regardless of scale.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Backdrop**: Instead of relying on boolean or bevel operators which can fail across API versions, the backdrop is generated via `bmesh` by mathematically plotting a 2D profile curve (floor -> arc -> wall) and extruding it along the X-axis. This guarantees perfect topology and 100% smooth shading.
  - **Subject**: A high-resolution UV Sphere sits perfectly on the floor plane as a demonstration object.
* **Step B: Materials & Shading**
  - Both objects use standard Principled BSDFs.
  - **Backdrop**: Roughness 0.5, Base Color (0.8, 0.8, 0.8) to softly catch shadows and light gradients without sharp reflections.
  - **Subject**: Roughness 0.15, Base Color (0.9, 0.9, 0.9) to cleanly reflect the contrasting rim lights and demonstrate the light setup's specularity.
* **Step C: Lighting Setup**
  - **Key Light (Top)**: 600W Area Light shining straight down.
  - **Left Rim (Warm)**: 200W Area Light rotated 90 degrees to shine inwards, colored HSV(0.1, 0.2, 1.0) / RGB(1.0, 0.85, 0.7).
  - **Right Rim (Cool)**: 200W Area Light rotated 90 degrees to shine inwards, colored HSV(0.6, 0.2, 1.0) / RGB(0.7, 0.85, 1.0).
  - **Front Fill**: 300W Area Light angled 65 degrees downwards/forwards. Specular factor is heavily reduced (0.3) so it fills shadows without creating a distracting white dot reflection on the front of the object.
* **Step D: Rendering Context**
  - Configures EEVEE to use Ambient Occlusion, Bloom, and Screen Space Reflections to maximize the visual quality of the studio out-of-the-box.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Infinity Cove Backdrop** | `bmesh` procedural extrusion | Generates perfect curved geometry mathematically, bypassing volatile modifier or `bpy.ops.bevel` API changes. |
| **Studio Lighting** | `bpy.data.lights` (Area) | Area lights provide the softest, most physically accurate studio illumination with customizable sizing and specular control. |
| **Composition** | Master Empty hierarchy | Ensures the entire studio (backdrop, subject, lights, camera) can be moved or scaled as a single modular unit safely. |

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "Advanced_Studio_Setup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.9, 0.9, 0.9),
    **kwargs,
) -> str:
    """
    Create an Advanced 4-Point Studio Lighting Environment with an infinity cove backdrop.

    Args:
        scene_name: Name of the target scene.
        object_name: Name of the master parent object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor for the entire studio.
        material_color: Base color of the demonstration subject.
        **kwargs: 
            warm_rim_color: (R,G,B) for the left rim light.
            cool_rim_color: (R,G,B) for the right rim light.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    warm_rim = kwargs.get('warm_rim_color', (1.0, 0.85, 0.7))
    cool_rim = kwargs.get('cool_rim_color', (0.7, 0.85, 1.0))

    # --- 1. Create Master Control Object ---
    master = bpy.data.objects.new(name=object_name, object_data=None)
    master.empty_display_type = 'ARROWS'
    master.empty_display_size = 2.0
    master.location = location
    master.scale = (scale, scale, scale)
    scene.collection.objects.link(master)

    # --- 2. Build Procedural Infinity Cove Backdrop ---
    profile = []
    # Floor segment (Y goes from -8 to 4)
    for i in range(10):
        y = -8.0 + (12.0 * i / 9.0)
        profile.append(Vector((0, y, 0)))

    # Arc segment (radius 4, center at Y=4, Z=4)
    for i in range(1, 16):
        angle = -math.pi/2 + (math.pi/2 * i / 15.0)
        y = 4.0 + 4.0 * math.cos(angle)
        z = 4.0 + 4.0 * math.sin(angle)
        profile.append(Vector((0, y, z)))

    # Wall segment (Z goes from 4 to 16)
    for i in range(1, 10):
        z = 4.0 + (12.0 * i / 9.0)
        profile.append(Vector((0, 8, z)))

    # Extrude profile along X axis via bmesh
    bm_bg = bmesh.new()
    verts = []
    for p in profile:
        v_left = bm_bg.verts.new(p + Vector((-8, 0, 0)))
        v_right = bm_bg.verts.new(p + Vector((8, 0, 0)))
        verts.append((v_left, v_right))
        
    bm_bg.verts.ensure_lookup_table()
    
    # Create faces linking the extrusion steps
    for i in range(len(verts) - 1):
        v1_L, v1_R = verts[i]
        v2_L, v2_R = verts[i+1]
        bm_bg.faces.new((v1_L, v1_R, v2_R, v2_L))

    mesh_bg = bpy.data.meshes.new(f"{object_name}_Backdrop")
    bm_bg.to_mesh(mesh_bg)
    bm_bg.free()

    for p in mesh_bg.polygons:
        p.use_smooth = True

    obj_bg = bpy.data.objects.new(name=f"{object_name}_Backdrop", object_data=mesh_bg)
    obj_bg.parent = master
    scene.collection.objects.link(obj_bg)

    # --- 3. Create Demonstration Subject (Sphere) ---
    bm_sph = bmesh.new()
    bmesh.ops.create_uvsphere(bm_sph, u_segments=64, v_segments=32, radius=1.0)
    mesh_sph = bpy.data.meshes.new(f"{object_name}_DemoSubject")
    bm_sph.to_mesh(mesh_sph)
    bm_sph.free()
    
    for p in mesh_sph.polygons:
        p.use_smooth = True
        
    obj_sph = bpy.data.objects.new(name=f"{object_name}_DemoSubject", object_data=mesh_sph)
    obj_sph.location = (0, 0, 1.0) # Rest on the floor
    obj_sph.parent = master
    scene.collection.objects.link(obj_sph)

    # --- 4. Setup Materials ---
    mat_bg = bpy.data.materials.new(name=f"{object_name}_GroundMat")
    mat_bg.use_nodes = True
    if mat_bg.node_tree:
        bsdf = mat_bg.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.5
    obj_bg.data.materials.append(mat_bg)

    mat_obj = bpy.data.materials.new(name=f"{object_name}_SubjectMat")
    mat_obj.use_nodes = True
    if mat_obj.node_tree:
        bsdf = mat_obj.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (*material_color, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.15
    obj_sph.data.materials.append(mat_obj)

    # --- 5. Setup Advanced 4-Point Lighting ---
    def create_area_light(name, loc, rot, power, size, color, specular):
        ld = bpy.data.lights.new(name=name, type='AREA')
        ld.energy = power
        ld.size = size
        ld.color = color
        
        # Suppress heavy front-facing reflections if needed
        if hasattr(ld, "specular_factor"):
            ld.specular_factor = specular
            
        # Custom distance for soft falloff clipping
        if hasattr(ld, "use_custom_distance"):
            ld.use_custom_distance = True
            ld.cutoff_distance = 20.0
            
        lo = bpy.data.objects.new(name=name, object_data=ld)
        lo.location = loc
        lo.rotation_euler = rot
        lo.parent = master
        scene.collection.objects.link(lo)

    # Top Hero Key Light (Soft White)
    create_area_light(f"{object_name}_Key_Top", (0, 0, 12), (0, 0, 0), 600, 8.0, (1.0, 1.0, 1.0), 1.0)
    
    # Left Rim Light (Warm)
    create_area_light(f"{object_name}_Rim_Warm_Left", (-8, 0, 4), (0, math.radians(-90), 0), 200, 8.0, warm_rim, 1.0)
    
    # Right Rim Light (Cool)
    create_area_light(f"{object_name}_Rim_Cool_Right", (8, 0, 4), (0, math.radians(90), 0), 200, 8.0, cool_rim, 1.0)
    
    # Front Camera Fill (Low Specular)
    create_area_light(f"{object_name}_Fill_Front", (0, -8, 5), (math.radians(65), 0, 0), 300, 6.0, (1.0, 1.0, 1.0), 0.3)

    # --- 6. Setup Presentation Camera ---
    cam_data = bpy.data.cameras.new(name=f"{object_name}_Camera")
    cam_obj = bpy.data.objects.new(name=f"{object_name}_Camera", object_data=cam_data)
    cam_obj.location = (0, -12, 2)
    cam_obj.rotation_euler = (math.radians(85), 0, 0) # Angled slightly downwards towards subject
    cam_obj.parent = master
    scene.collection.objects.link(cam_obj)

    # --- 7. Configure EEVEE Render Engine Properties ---
    if scene.render.engine == 'BLENDER_EEVEE':
        try:
            scene.eevee.use_gtao = True
            scene.eevee.use_bloom = True
            scene.eevee.use_ssr = True
        except AttributeError:
            # Silently pass if running on newer Blender versions where EEVEE API changed
            pass

    return f"Created Advanced Studio Lighting Environment '{object_name}' with infinity cove, 4 area lights, and a presentation camera at {location}."
```