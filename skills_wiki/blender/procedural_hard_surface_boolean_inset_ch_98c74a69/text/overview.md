# Procedural Hard-Surface Boolean Inset & Chamfer

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Hard-Surface Boolean Inset & Chamfer

* **Core Visual Mechanism**: Using a non-destructive Boolean modifier combined with an Angle-limited Bevel modifier to create perfectly shaded, chamfered intersections between geometric shapes. The workflow mimics the visual results of specialized hard-surface add-ons (like the "Chamfer" and "Plug" tools in Mesh Machine) but relies entirely on native procedural logic.

* **Why Use This Skill (Rationale)**: The video demonstrates using third-party add-ons to clean up, select, and chamfer edge loops after a boolean operation is applied destructively. Replicating destructive mesh cleanup via code is extremely brittle. Instead, utilizing Blender's procedural modifier stack (Boolean $\rightarrow$ Bevel $\rightarrow$ Weighted Normal) achieves the exact same premium mechanical aesthetic dynamically. It allows Blender to automatically calculate the intersecting angles and apply chamfers without ever destroying the base topology.

* **Overall Applicability**: This is a foundational technique for hard-surface modeling, sci-fi props, mecha armor, weapons, mechanical detailing, architectural cutouts, and product visualization. 

* **Value Addition**: Transforms basic primitive shapes into complex mechanical parts instantly. It adds high-frequency detail (panel lines, vents, inset handles) and realistic "caught-edge" specular highlights that make 3D models look heavy and manufactured.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: High-resolution UV Sphere.
  - **Cutter Mesh**: A Cube heavily modified by a Bevel modifier (limit method: 'NONE', high segments) to act as a "pill" shaped mechanical punch.
  - **Modifier Stack (Base)**: 
    1. `Boolean` (Difference) using the pill cutter.
    2. `Bevel` (Limit Method: 'ANGLE' at 30°). This automatically detects the sharp 90° intersection created by the boolean cut. Set segments to 1 to create a sharp mechanical chamfer, as shown in the tutorial.
    3. `Weighted Normal` to instantly fix any shading artifacts created by the n-gons at the boolean boundary.

* **Step B: Materials & Shading**
  - **Shader Model**: Principled BSDF designed to look like machined metal.
  - **Color**: Dark gunmetal `(0.2, 0.2, 0.25)`.
  - **Properties**: High Metallic (`0.8`) and Low Roughness (`0.25`) to maximize the visibility and specularity of the chamfered intersection edge.

* **Step C: Lighting & Rendering Context**
  - Works beautifully in EEVEE and Cycles. 
  - Requires high-contrast lighting (like a 3-point setup or a studio HDRI) to catch the glint on the narrow chamfered edges.

* **Step D: Animation & Dynamics**
  - Because it is 100% procedural, the mechanical inset can be animated opening/sliding by keyframing the Cutter object's location.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Creating the "Plug" cut | Primitive + Boolean Modifier | Keeps the mesh non-destructive and allows easy parametric placement. |
| Chamfering the intersection | Bevel Modifier (Angle Limit) | Automates the tedious edge-loop selection demonstrated in the tutorial. The angle limit dynamically catches the boolean cut. |
| Fixing shading artifacts | Weighted Normal Modifier | Provides flawless surface normals around n-gons without manual topology cleanup. |

> **Feasibility Assessment**: 100%. While the video demonstrates doing this destructively with a proprietary add-on, this code reproduces the exact premium visual result (a smooth mechanical shape with a pristine chamfered inset cut) purely procedurally.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "SciFi_Panel_Cut",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.2, 0.25),
    **kwargs,
) -> str:
    """
    Create a Procedural Hard-Surface Boolean Inset & Chamfer.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created base object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the metallic material.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (Sphere) ===
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.0, location=location)
    base_obj = bpy.context.active_object
    base_obj.name = object_name
    base_obj.scale = (scale, scale, scale)

    # Apply smooth shading
    bpy.ops.object.shade_smooth()
    
    # Handle auto-smooth for Blender versions < 4.1
    if hasattr(base_obj.data, "use_auto_smooth"):
        base_obj.data.use_auto_smooth = True
        base_obj.data.auto_smooth_angle = math.radians(30)

    # === Step 2: Create "Plug" Cutter Geometry (Rounded Pill) ===
    # Position the cutter slightly offset on the X-axis to cut into the side of the sphere
    cutter_loc = Vector(location) + Vector((0.8 * scale, 0.0, 0.0))
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=cutter_loc)
    cutter_obj = bpy.context.active_object
    cutter_obj.name = f"{object_name}_Cutter"
    cutter_obj.scale = (1.0 * scale, 0.5 * scale, 0.5 * scale)
    
    # Hide the cutter from render and show as bounds/wire in viewport
    cutter_obj.display_type = 'WIRE'
    cutter_obj.hide_render = True
    bpy.ops.object.shade_smooth()

    # Round out the cutter to create a smooth 'pill' shaped inset
    cutter_bevel = cutter_obj.modifiers.new("Cutter_Rounding", 'BEVEL')
    cutter_bevel.width = 0.15 * scale
    cutter_bevel.segments = 16
    cutter_bevel.limit_method = 'NONE'

    # === Step 3: Apply Hard-Surface Procedural Stack to Base ===
    bpy.context.view_layer.objects.active = base_obj

    # 3a. Boolean Cut
    bool_mod = base_obj.modifiers.new("Mechanical_Cut", 'BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = cutter_obj
    bool_mod.solver = 'EXACT'

    # 3b. Automatic Intersection Chamfer
    bevel_mod = base_obj.modifiers.new("Intersection_Chamfer", 'BEVEL')
    bevel_mod.limit_method = 'ANGLE'
    bevel_mod.angle_limit = math.radians(30)
    bevel_mod.width = 0.03 * scale
    bevel_mod.segments = 1  # 1 segment creates a flat mechanical chamfer
    bevel_mod.harden_normals = True

    # 3c. Shading Fixer
    wn_mod = base_obj.modifiers.new("Weighted_Normal", 'WEIGHTED_NORMAL')
    wn_mod.keep_sharp = True

    # === Step 4: Build Machined Metal Material ===
    mat = bpy.data.materials.new(name=f"{object_name}_Metal_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.8
        bsdf.inputs['Roughness'].default_value = 0.25
    
    if not base_obj.data.materials:
        base_obj.data.materials.append(mat)

    # Deselect cutter, select base
    cutter_obj.select_set(False)
    base_obj.select_set(True)

    return f"Created '{object_name}' with procedural inset cut and chamfer at {location}"
```