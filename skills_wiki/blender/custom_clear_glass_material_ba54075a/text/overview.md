# Custom Clear Glass Material

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Custom Clear Glass Material

* **Core Visual Mechanism**: The defining characteristic of this technique is separating the optical behavior of glass into two distinct components: pure **Refraction** and pure **Reflection (Glossy)**. Instead of using a monolithic Principled BSDF, this approach blends the two using a **Fresnel node** as a mask. This creates a highly realistic physical effect where the object is transparent when viewed straight on, but highly reflective at grazing angles.

* **Why Use This Skill (Rationale)**: By breaking the glass down into its foundational shader components, you gain absolute control over the look. It forces the render engine to evaluate reflections and refractions exactly as you define them. Placing Refraction in the top socket of the Mix Shader prevents the object from looking like a solid chrome block, ensuring the default facing angle prioritizes transparency.

* **Overall Applicability**: This technique is essential for product visualization (bottles, cups, cosmetics), architectural renders (windows, glass partitions), and jewelry. It is specifically tailored for the **Cycles** render engine, which handles the complex raytracing needed for accurate glass.

* **Value Addition**: Compared to a default Principled BSDF with high transmission, this custom node group often yields cleaner, more predictable reflections and less noise, giving a "crystal clear" aesthetic that feels highly polished.


### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A tapered bmesh cylinder (`create_cone`) is used.
  - **Modifiers**: The top face is deleted to form an open cup. A **Solidify** modifier provides the necessary physical thickness (glass requires thickness to refract light properly). A **Subdivision Surface** modifier rounds out the shape, while an edge crease on the base keeps the bottom flat.

* **Step B: Materials & Shading**
  - **Shader Model**: A custom mix of `ShaderNodeBsdfRefraction` and `ShaderNodeBsdfGlossy`.
  - **Fresnel Mask**: `ShaderNodeFresnel` controls the Mix Shader factor.
  - **Parameters**: 
    - **IOR (Index of Refraction)**: Set to `1.5` on both the Fresnel and Refraction nodes (the physical standard for standard clear glass).
    - **Roughness**: Set to `0.0` on both Glossy and Refraction nodes for perfectly clear, polished glass.
  - **Routing**: Refraction is plugged into the *Top* socket (evaluated at `Fac = 0`), Glossy is plugged into the *Bottom* socket (evaluated at `Fac = 1`).

* **Step C: Lighting & Rendering Context**
  - **Lighting Setup**: Glass is invisible without an environment. It *requires* an HDRI, three-point lighting, or a studio setup to bounce off of.
  - **Render Engine**: **Cycles** is strongly recommended. If using EEVEE, Screen Space Refraction must be enabled in both the render settings and the material properties.

* **Step D: Animation & Dynamics**
  - Static material, though the object can easily be part of a rigid body simulation (e.g., falling cups).


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Geometry (Cup) | `bmesh` + Modifiers | Generates a clean, tapered vessel procedurally so the material has a proper physical volume to refract light through. |
| Clear Glass Material | Custom Shader Node Tree | Reproduces the exact Fresnel/Mix logic shown in the tutorial, bypassing the Principled BSDF. |

> **Feasibility Assessment**: 100% reproduction of the material technique. Since the tutorial used an imported Kitbash asset for the cup, this code goes a step further by fully procedurally generating a matching glass cup to apply the material to.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "ClearGlassCup",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.95, 0.95, 0.95),
    **kwargs,
) -> str:
    """
    Create a Custom Clear Glass Material applied to a procedural cup mesh.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base tint of the glass in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import bpy
    import bmesh
    from mathutils import Vector, Matrix

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # === Step 1: Create Base Geometry (Procedural Cup) ===
    mesh = bpy.data.meshes.new(object_name + "_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)

    bm = bmesh.new()
    # Create tapered cylinder, shift up so base rests at local Z=0
    matrix = Matrix.Translation((0, 0, 1.0))
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=32,
        radius1=0.7,  # Base radius
        radius2=1.0,  # Top radius
        depth=2.0,
        matrix=matrix
    )
    
    # Delete the top face to hollow it out
    top_faces = [f for f in bm.faces if f.calc_center_median().z > 1.9]
    bmesh.ops.delete(bm, geom=top_faces, context='FACES')

    # Add edge crease to the bottom face to keep it flat during subdivision
    bottom_faces = [f for f in bm.faces if f.calc_center_median().z < 0.1]
    if bottom_faces:
        crease_layer = bm.edges.layers.crease.verify()
        for e in bottom_faces[0].edges:
            e[crease_layer] = 1.0

    bm.to_mesh(mesh)
    bm.free()

    # Apply smooth shading to polygons
    for poly in mesh.polygons:
        poly.use_smooth = True

    # Add Modifiers for physical glass thickness and smooth curves
    solidify = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = 0.08
    solidify.offset = 0.0  # Expand evenly

    subsurf = obj.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 3

    # === Step 2: Build Material (Custom Clear Glass Nodes) ===
    mat = bpy.data.materials.new(name="ClearGlassMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes (Removes Principled BSDF)
    for node in nodes:
        nodes.remove(node)

    # Output Node
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    out_node.location = (300, 0)

    # Mix Shader
    mix_node = nodes.new(type='ShaderNodeMixShader')
    mix_node.location = (100, 0)

    # Refraction BSDF (Handles straight-on transparency)
    refraction_node = nodes.new(type='ShaderNodeBsdfRefraction')
    refraction_node.location = (-100, 100)
    refraction_node.inputs['Color'].default_value = (*material_color, 1.0)
    refraction_node.inputs['Roughness'].default_value = 0.0
    refraction_node.inputs['IOR'].default_value = 1.5

    # Glossy BSDF (Handles grazing-angle reflections)
    glossy_node = nodes.new(type='ShaderNodeBsdfGlossy')
    glossy_node.location = (-100, -100)
    glossy_node.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0) # Reflections remain white
    glossy_node.inputs['Roughness'].default_value = 0.0

    # Fresnel Node (Drives the Mix Factor based on view angle)
    fresnel_node = nodes.new(type='ShaderNodeFresnel')
    fresnel_node.location = (-100, 300)
    fresnel_node.inputs['IOR'].default_value = 1.5

    # Connect Nodes
    # NOTE: Refraction goes into Top Socket (1), Glossy into Bottom Socket (2)
    links.new(fresnel_node.outputs['Fac'], mix_node.inputs[0])
    links.new(refraction_node.outputs['BSDF'], mix_node.inputs[1])
    links.new(glossy_node.outputs['BSDF'], mix_node.inputs[2])
    links.new(mix_node.outputs['Shader'], out_node.inputs['Surface'])

    # Enable EEVEE transparency settings (acts as a fallback, though Cycles is intended)
    try:
        mat.use_screen_refraction = True
        mat.blend_method = 'HASHED'
    except AttributeError:
        pass

    obj.data.materials.append(mat)

    # === Step 3: Position & Scale ===
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)

    return f"Created '{object_name}' (Clear Glass Cup) at {location}"
```