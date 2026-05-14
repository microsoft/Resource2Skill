# Procedural Gradient Strip Box (Studio Lighting)

## Analysis

Here is the extraction of the 3D design pattern and the procedural reproduction code based on the provided video tutorial.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Gradient Strip Box (Studio Lighting)

* **Core Visual Mechanism**: Replacing standard, uniform area lights with emission planes driven by procedural gradient textures. The gradient acts as an alpha/strength mask, creating a light source that is brightest at its center (or edge) and smoothly falls off to black.
* **Why Use This Skill (Rationale)**: In professional studio and product photography, lights are rarely perfectly uniform rectangles. Photographers use diffusers, strip boxes, and honeycomb grids to control light falloff. In 3D rendering, a uniform area light reflecting off a glossy cylindrical object (like a camera lens or a wine bottle) results in a harsh, blocky, and fake-looking white rectangle. A gradient plane reflects as a smooth, contoured highlight that accentuates the 3D curvature and surface finish of the object, instantly elevating the render to photorealism.
* **Overall Applicability**: Essential for product rendering (electronics, bottles, cosmetics), automotive rendering, and macro 3D photography where reflections define the shape of the subject. 
* **Value Addition**: Transforms lighting from a basic "CGI look" into a professional studio environment. It provides highly customizable, infinite-resolution reflections without needing external HDRIs or image textures.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A standard primitive plane (`bpy.ops.mesh.primitive_plane_add`).
  - **Transformations**: Non-uniform scaling is used to turn the square plane into a long rectangle (e.g., scale Y by 4.0, scale X by 1.0) to act as a strip box.
  - **Ray Visibility**: The plane is explicitly hidden from Camera rays so it functions purely as an off-screen light source and reflection source, without blocking the background.

* **Step B: Materials & Shading**
  - **Shader Model**: Emission Shader (`ShaderNodeEmission`).
  - **Procedural Logic**: `Texture Coordinate (Generated)` -> `Separate XYZ` isolates an axis (X or Y). Math nodes (`Absolute`, `Multiply`, `Subtract`) are used to convert the 0-to-1 linear gradient into a 0-to-1-to-0 "double" gradient centered on the plane. A `Power` math node controls the falloff/softness of the edge, which is then multiplied by an Intensity value and fed into the Emission Strength.
  - **Colors**: Usually stark white `(1.0, 1.0, 1.0)`, but can be tinted for stylistic edge/rim lighting (e.g., deep red `(0.8, 0.05, 0.05)`).

* **Step C: Lighting & Rendering Context**
  - **Engine**: Cycles is strongly recommended, as physically accurate raytraced reflections are required to see the gradient perfectly mapped onto curved surfaces.
  - **Environment**: Best used against a black or very dark World background (`Strength = 0.0`) so the gradient lights provide 100% of the scene's illumination and reflections.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Light geometry | `bpy.ops.mesh.primitive_plane_add` | A flat polygon is the standard physical representation of a studio bounce board or softbox. |
| Gradient Falloff | Shader Node Tree (Math operations) | Procedural math nodes allow for infinite resolution and real-time adjustment of falloff sharpness without relying on external image textures or difficult-to-script ColorRamps. |
| Invisible Light Source | `obj.visible_camera = False` | Allows the plane to emit light and be reflected by glossy objects without appearing as a glowing white rectangle in the final render. |

**Feasibility Assessment**: 100% — This script perfectly recreates the "Ultimate Strip Box" node setup demonstrated in the video, providing programmatic control over single/double gradients, axis orientation, and falloff.

#### 3b. Complete Reproduction Code

```python
def create_gradient_light(
    scene_name: str = "Scene",
    object_name: str = "GradientStripBox",
    location: tuple = (0.0, -2.0, 0.0),
    rotation: tuple = (1.5708, 0, 0), # 90 degrees on X
    scale: tuple = (1.0, 4.0, 1.0),
    light_color: tuple = (1.0, 1.0, 1.0),
    intensity: float = 10.0,
    double_gradient: bool = True,
    axis: str = 'X',
    falloff: float = 2.0,
    **kwargs
) -> str:
    """
    Creates a procedural gradient emission plane (Strip Box) for studio lighting.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name of the created light plane.
        location: (x, y, z) position.
        rotation: (x, y, z) rotation in radians.
        scale: Scale factor (non-uniform scale creates strip lights).
        light_color: (R, G, B) color of the emission.
        intensity: Brightness multiplier.
        double_gradient: If True, gradient peaks in the center and fades to both edges. 
                         If False, fades linearly from one edge to the other.
        axis: 'X' or 'Y' - the local axis the gradient flows along.
        falloff: Controls the sharpness of the gradient (higher = sharper, thinner strip).
        
    Returns:
        Status string.
    """
    import bpy
    import math
    
    # 1. Create Base Geometry (Plane)
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = object_name
    obj.scale = scale
    
    # Hide from camera so it acts as an off-screen light/reflection source
    obj.visible_camera = False 
    if hasattr(obj, 'cycles'):
        obj.cycles.is_camera_visible = False
    
    # 2. Build Procedural Gradient Material
    mat = bpy.data.materials.new(name=f"{object_name}_GradientMat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear() # Remove default Principled BSDF setup
    
    # Add Core Nodes
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    
    sep_xyz = nodes.new('ShaderNodeSeparateXYZ')
    sep_xyz.location = (-400, 0)
    
    math_power = nodes.new('ShaderNodeMath')
    math_power.operation = 'POWER'
    math_power.inputs[1].default_value = falloff
    math_power.location = (200, 0)
    
    math_intensity = nodes.new('ShaderNodeMath')
    math_intensity.operation = 'MULTIPLY'
    math_intensity.inputs[1].default_value = intensity
    math_intensity.location = (400, 0)
    
    emission = nodes.new('ShaderNodeEmission')
    emission.inputs['Color'].default_value = (*light_color, 1.0)
    emission.location = (600, 0)
    
    out = nodes.new('ShaderNodeOutputMaterial')
    out.location = (800, 0)
    
    # 3. Connect the basic coordinate flow
    links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], sep_xyz.inputs['Vector'])
    
    # Select target axis
    axis_socket = sep_xyz.outputs[0] if axis.upper() == 'X' else sep_xyz.outputs[1]
    current_output = axis_socket
    
    # 4. Math Logic for Gradient Types
    if double_gradient:
        # Center the generated coordinates (-0.5 to 0.5)
        mapping.inputs['Location'].default_value = (-0.5, -0.5, 0.0)
        
        # Absolute (-0.5 -> 0.5 becomes 0.5 -> 0 -> 0.5)
        math_abs = nodes.new('ShaderNodeMath')
        math_abs.operation = 'ABSOLUTE'
        math_abs.location = (-200, 100)
        
        # Multiply by 2 (0.5 -> 0 -> 0.5 becomes 1.0 -> 0 -> 1.0)
        math_mul = nodes.new('ShaderNodeMath')
        math_mul.operation = 'MULTIPLY'
        math_mul.inputs[1].default_value = 2.0
        math_mul.location = (0, 100)
        
        # Subtract from 1 (1.0 -> 0 -> 1.0 becomes 0.0 -> 1.0 -> 0.0)
        math_sub = nodes.new('ShaderNodeMath')
        math_sub.operation = 'SUBTRACT'
        math_sub.inputs[0].default_value = 1.0
        math_sub.location = (0, -100)
        
        links.new(current_output, math_abs.inputs[0])
        links.new(math_abs.outputs[0], math_mul.inputs[0])
        links.new(math_mul.outputs[0], math_sub.inputs[1])
        
        current_output = math_sub.outputs[0]
        
    # 5. Connect Final Falloff and Emission
    links.new(current_output, math_power.inputs[0])
    links.new(math_power.outputs[0], math_intensity.inputs[0])
    links.new(math_intensity.outputs[0], emission.inputs['Strength'])
    links.new(emission.outputs['Emission'], out.inputs['Surface'])
    
    # Deselect all and select the newly created light plane
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    grad_type = "Double" if double_gradient else "Single"
    return f"Created '{object_name}' (Procedural {grad_type} Gradient Strip Light) at {location} with intensity {intensity}."
```