# Advanced HDRI Lighting & Background Mask Rig

## Analysis

An essential skill in 3D visualization is using High Dynamic Range Images (HDRIs) to light scenes. Default point, sun, and area lights struggle to replicate the complex, multi-directional color variations and realistic reflections found in the real world. 

This document extracts the standard procedural HDRI environment rig, which not only projects realistic lighting and reflections onto your objects but also includes a **Light Path masking technique** to keep the camera background clean (solid color or transparent) while preserving the complex HDRI lighting.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Advanced HDRI Lighting & Background Mask Rig

* **Core Visual Mechanism**: Image-Based Lighting (IBL) via an `Environment Texture` node mapped onto the World shader. A `Light Path` node intercepts rays, distinguishing between "Camera Rays" (what the viewer sees directly in the background) and "Diffuse/Glossy Rays" (the light and reflections cast onto objects).
* **Why Use This Skill (Rationale)**: Physically accurate materials (like chrome, glass, or car paint) look broken or "CGI-like" without a real-world environment to reflect. HDRIs instantly ground objects in reality. Masking out the HDRI from the camera background is critical for product rendering and compositing, as it removes distracting background elements (like random trees or buildings) while keeping their beautiful lighting contributions.
* **Overall Applicability**: Essential for product visualization, automotive rendering, architectural exteriors, and any scene requiring photorealistic materials and lighting.
* **Value Addition**: Transforms a flat, artificially lit scene into a highly realistic one instantly. The rig includes mapping coordinates, allowing you to arbitrarily rotate the HDRI to find the perfect rim light or shadow angle.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Effect Target**: Modifies the global `World` shader space, affecting all objects in the scene. 
  - **Demonstration Object**: A simple UV Sphere with smooth shading is generated to showcase the complex reflections.

* **Step B: Materials & Shading**
  - **World Shader Nodes**:
    - `Texture Coordinate` (Generated) → `Mapping` (Controls rotation) → `Environment Texture` (Loads the EXR/HDR file).
    - `Light Path` → `Mix Shader`. By using the `Is Camera Ray` output as the mixing factor, the rig feeds the HDRI into the scene's lighting/reflections, while feeding a clean, solid color into the actual visible background.
  - **Fallback Mechanism**: If no external HDRI path is provided, the script dynamically searches for Blender's built-in studio `.exr` files (used for Material Preview mode) to guarantee the script executes and produces beautiful reflections without external dependencies. If it fails, it falls back to a procedural `Nishita Sky Texture`.

* **Step C: Lighting & Rendering Context**
  - Replaces default lighting. Works in both EEVEE and Cycles, though Cycles computes the HDRI global illumination and contact shadows with absolute physical accuracy.

* **Step D: Animation & Dynamics (if applicable)**
  - The Z-Rotation value on the `Mapping` node can be keyframed to simulate time-lapses (with sky textures) or dynamically alter lighting setups during an animation.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| HDRI Environment Setup | World Shader Node Tree | Procedural, non-destructive, and affects global illumination. |
| Background Separation | Light Path Node (Is Camera Ray) | Industry-standard technique to decouple lighting data from the visible backdrop. |
| Reproducibility | Built-in Resource Fetcher | Guarantees the script works out-of-the-box by leveraging Blender's hidden built-in EXR studio lights. |
| Demonstration Object | `bpy.ops.mesh` + Material Nodes | Creates a high-metallic sphere to instantly validate that the HDRI reflections are working. |

#### 3b. Complete Reproduction Code

```python
def create_advanced_hdri_rig(
    scene_name: str = "Scene",
    object_name: str = "HDRI_Demo_Sphere",
    location: tuple = (0, 0, 1),
    scale: float = 1.0,
    hdri_path: str = "",
    rotation_z_degrees: float = 45.0,
    light_strength: float = 1.0,
    separate_background: bool = True,
    visible_background_color: tuple = (0.05, 0.05, 0.05, 1.0),
    **kwargs
) -> str:
    """
    Creates an advanced HDRI World Lighting rig and a reflective demo sphere.
    
    Args:
        scene_name: Name of the active scene.
        object_name: Name of the reflective demonstration sphere.
        location: World-space position for the demo sphere.
        scale: Scale of the demo sphere.
        hdri_path: Absolute path to an .exr or .hdr file. If empty, uses built-in studio lights.
        rotation_z_degrees: Rotates the HDRI environment to change lighting angles.
        light_strength: Overall brightness of the HDRI.
        separate_background: If True, uses the HDRI for lighting but a solid color for the camera backdrop.
        visible_background_color: The RGBA color for the camera backdrop if separated.
        
    Returns:
        Status string.
    """
    import bpy
    import os
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Helper: Find a built-in Blender HDRI for guaranteed reproducibility
    def get_builtin_hdri():
        paths = [
            os.path.join(bpy.utils.resource_path('LOCAL'), 'datafiles', 'studiolights', 'world'),
            os.path.join(bpy.utils.system_resource('DATAFILES'), 'studiolights', 'world')
        ]
        for p in paths:
            if os.path.exists(p):
                for file in os.listdir(p):
                    if file.lower().endswith(('.exr', '.hdr')):
                        return os.path.join(p, file)
        return None

    # === Step 1: Create a New Additive World ===
    new_world = bpy.data.worlds.new(name="Advanced_HDRI_World")
    new_world.use_nodes = True
    scene.world = new_world
    
    nodes = new_world.node_tree.nodes
    links = new_world.node_tree.links
    nodes.clear() # Clear default nodes in the new world

    # === Step 2: Create World Nodes ===
    world_output = nodes.new('ShaderNodeOutputWorld')
    world_output.location = (800, 0)
    
    bg_hdri = nodes.new('ShaderNodeBackground')
    bg_hdri.name = "Background_HDRI"
    bg_hdri.inputs['Strength'].default_value = light_strength
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-400, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-200, 0)
    mapping.inputs['Rotation'].default_value = (0.0, 0.0, math.radians(rotation_z_degrees))
    
    # Try to load HDRI, fallback to procedural Sky Texture
    if not hdri_path:
        hdri_path = get_builtin_hdri()
        
    if hdri_path and os.path.exists(hdri_path):
        env_tex = nodes.new('ShaderNodeTexEnvironment')
        try:
            env_tex.image = bpy.data.images.load(hdri_path)
        except:
            pass
        env_tex.location = (0, 0)
        bg_hdri.location = (200, 0)
        
        links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
        links.new(mapping.outputs['Vector'], env_tex.inputs['Vector'])
        links.new(env_tex.outputs['Color'], bg_hdri.inputs['Color'])
    else:
        # Failsafe procedural fallback
        env_tex = nodes.new('ShaderNodeTexSky')
        env_tex.sky_type = 'NISHITA'
        env_tex.location = (0, 0)
        bg_hdri.location = (200, 0)
        links.new(env_tex.outputs['Color'], bg_hdri.inputs['Color'])

    # === Step 3: Implement Light Path Masking ===
    if separate_background:
        mix_node = nodes.new('ShaderNodeMixShader')
        mix_node.location = (500, 0)
        
        light_path = nodes.new('ShaderNodeLightPath')
        light_path.location = (200, 300)
        
        bg_solid = nodes.new('ShaderNodeBackground')
        bg_solid.name = "Background_Solid_Visible"
        bg_solid.inputs['Color'].default_value = visible_background_color
        bg_solid.inputs['Strength'].default_value = 1.0
        bg_solid.location = (200, -200)
        
        # Connect mixing logic
        links.new(light_path.outputs['Is Camera Ray'], mix_node.inputs[0]) # Fac
        links.new(bg_hdri.outputs['Background'], mix_node.inputs[1])       # Shader 0 (Lighting/Reflections)
        links.new(bg_solid.outputs['Background'], mix_node.inputs[2])      # Shader 1 (Visible Backdrop)
        links.new(mix_node.outputs['Shader'], world_output.inputs['Surface'])
    else:
        links.new(bg_hdri.outputs['Background'], world_output.inputs['Surface'])

    # === Step 4: Create Demonstration Object ===
    # Add a highly reflective sphere to prove the HDRI lighting is working
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=scale, location=location)
    demo_obj = bpy.context.active_object
    demo_obj.name = object_name
    bpy.ops.object.shade_smooth()
    
    # Chrome material
    mat = bpy.data.materials.new(name="Demo_Chrome_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if 'Metallic' in bsdf.inputs:
            bsdf.inputs['Metallic'].default_value = 1.0
        if 'Roughness' in bsdf.inputs:
            bsdf.inputs['Roughness'].default_value = 0.05
        if 'Base Color' in bsdf.inputs:
            bsdf.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)
    demo_obj.data.materials.append(mat)

    hdri_status = f"using external HDRI '{os.path.basename(hdri_path)}'" if hdri_path else "using procedural Sky Texture fallback"
    return f"Created HDRI Lighting Rig ({hdri_status}) and spawned demonstration object '{object_name}' at {location}."
```