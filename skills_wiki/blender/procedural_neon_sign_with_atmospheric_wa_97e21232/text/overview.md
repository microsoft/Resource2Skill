# Procedural Neon Sign with Atmospheric Wall

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Neon Sign with Atmospheric Wall

* **Core Visual Mechanism**: The defining visual signature is a glowing, tubular structure achieved by setting text/curve fill to "None" and adding a Bevel depth. This hollow geometry is paired with an intense Emission shader. To sell the effect, the scene relies on a dark, textured background (a procedural brick wall) that catches and diffuses the emitted light, creating a strong contrast and atmospheric glow.
* **Why Use This Skill (Rationale)**: Neon signs are staple elements in cyberpunk, retro-wave, and urban environments. Using actual 3D tubular geometry rather than flat planes with emission creates realistic self-shadowing and depth. Bouncing that light off a rough, normal-mapped surface (like brick) grounds the light source in physical space.
* **Overall Applicability**: Perfect for adding focal points in dark cityscapes, creating retro diner facades, or adding colorful atmospheric bounce light to night-time interior/exterior renders. 
* **Value Addition**: This skill instantly injects stylized lighting and procedural environmental context. Instead of just adding an emitting object, it provides the *canvas* (the wall) that makes the emission look impressive.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: Standard Text object, centered.
  - **Modifiers/Properties**: Text `fill_mode` is set to `NONE` (removing the front/back faces), and `bevel_depth` is increased. This instantly converts flat outlines into 3D glass-like tubes.
* **Step B: Materials & Shading**
  - **Neon Material**: A pure `Emission` shader with an un-clamped strength (e.g., 20.0).
  - **Wall Material**: A `Principled BSDF` driven by a `Brick Texture`. The brick colors are extremely dark (almost black/charcoal) with high roughness to act as a realistic canvas for the bright neon. The brick `Fac` is plugged into a `Bump` node to generate realistic normal mapping, catching the light on the edges of the bricks.
* **Step C: Lighting & Rendering Context**
  - **Bounce Faking**: In the tutorial, an Irradiance Volume is used to bake the bounce light for older versions of EEVEE. To make this fully procedural and real-time without requiring manual baking, an Area light matching the neon color is placed directly behind the text, pointing at the wall. This instantly fakes the radiant bounce.
* **Step D: Animation & Dynamics**
  - No animation is required, though the emission strength can easily be keyframed using `#frame` drivers to simulate a flickering broken neon sign.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Neon Tube Geometry | `bpy.data.curves.new(type='FONT')` properties | Setting `fill_mode='NONE'` and adding `bevel_depth` procedurally converts text to tubes without complex destructive bmesh editing. |
| Neon Glow | `ShaderNodeEmission` | Direct emission of colored light. |
| Background Canvas | `bpy.ops.mesh.primitive_plane_add` + `ShaderNodeTexBrick` | Procedural infinite resolution texture that reacts beautifully to light angles via Bump mapping. |
| Real-time Light Bounce | `bpy.data.lights.new(type='AREA')` | Fakes the light bounce onto the wall instantly without requiring EEVEE indirect light baking (Irradiance Volumes). |

> **Feasibility Assessment**: 85% — The code perfectly reproduces the tubular outline geometry, the intense glow, the procedural brick backdrop, and the light interaction. The manual step in the tutorial of destructively deleting specific curve segments to make the font look like a "broken single-stroke" neon tube cannot be reliably automated for arbitrary text inputs, so the procedural version creates a continuous "outlined" neon effect instead, which still perfectly captures the visual style.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "NeonSign",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 1.0, 0.4),
    **kwargs,
) -> str:
    """
    Create a procedural Neon Sign with glowing tubes and a reactive brick background.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        material_color: (R, G, B) base color of the neon glow in 0-1 range.
        **kwargs:
            text_string (str): The word to display (default: "NEON").
            emission_strength (float): Intensity of the glow (default: 20.0).
            tube_radius (float): Thickness of the neon tube (default: 0.02).
            create_wall (bool): Whether to generate the brick backdrop (default: True).

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Configuration kwargs
    text_string = kwargs.get("text_string", "NEON")
    emission_strength = kwargs.get("emission_strength", 20.0)
    tube_radius = kwargs.get("tube_radius", 0.02)
    create_wall = kwargs.get("create_wall", True)
    
    # === Step 1: Create Neon Text Geometry ===
    text_data = bpy.data.curves.new(name=f"{object_name}_Data", type='FONT')
    text_data.body = text_string
    text_data.align_x = 'CENTER'
    
    # Convert standard flat text into hollow tubes
    text_data.fill_mode = 'NONE'
    text_data.bevel_depth = tube_radius
    text_data.bevel_resolution = 4
    
    text_obj = bpy.data.objects.new(object_name, text_data)
    scene.collection.objects.link(text_obj)
    
    text_obj.location = Vector(location)
    text_obj.scale = (scale, scale, scale)
    # Stand the text up vertically
    text_obj.rotation_euler = (math.radians(90), 0, 0)
    
    # === Step 2: Create Neon Material ===
    neon_mat = bpy.data.materials.new(name=f"{object_name}_Mat")
    neon_mat.use_nodes = True
    nodes = neon_mat.node_tree.nodes
    links = neon_mat.node_tree.links
    nodes.clear()
    
    emission = nodes.new('ShaderNodeEmission')
    emission.inputs['Color'].default_value = (*material_color, 1.0)
    emission.inputs['Strength'].default_value = emission_strength
    
    output = nodes.new('ShaderNodeOutputMaterial')
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    text_data.materials.append(neon_mat)
    
    # === Step 3: Create Background Brick Wall ===
    if create_wall:
        wall_size = max(10 * scale, len(text_string) * 1.5 * scale)
        # Place wall slightly behind the text (+Y direction after text X-rotation)
        wall_loc = (location[0], location[1] + 0.15 * scale, location[2])
        bpy.ops.mesh.primitive_plane_add(size=wall_size, location=wall_loc)
        
        wall_obj = bpy.context.active_object
        wall_obj.name = f"{object_name}_Wall"
        wall_obj.rotation_euler = (math.radians(90), 0, 0)
        
        wall_mat = bpy.data.materials.new(name=f"{object_name}_Wall_Mat")
        wall_mat.use_nodes = True
        wnodes = wall_mat.node_tree.nodes
        wlinks = wall_mat.node_tree.links
        
        bsdf = wnodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Roughness'].default_value = 0.95
            
            # Procedural Brick Texture
            brick = wnodes.new('ShaderNodeTexBrick')
            brick.inputs['Color1'].default_value = (0.05, 0.02, 0.02, 1.0)
            brick.inputs['Color2'].default_value = (0.02, 0.01, 0.01, 1.0)
            brick.inputs['Mortar'].default_value = (0.005, 0.005, 0.005, 1.0)
            brick.inputs['Scale'].default_value = 15.0 / scale
            
            # Bump mapping for realistic light catching
            bump = wnodes.new('ShaderNodeBump')
            bump.inputs['Distance'].default_value = 0.05
            
            wlinks.new(brick.outputs['Color'], bsdf.inputs['Base Color'])
            wlinks.new(brick.outputs['Fac'], bump.inputs['Height'])
            wlinks.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
        
        wall_obj.data.materials.append(wall_mat)
        
        # === Step 4: Fake Bounce Lighting for Real-time EEVEE ===
        # Avoids the need for manual Light Probe baking
        light_data = bpy.data.lights.new(name=f"{object_name}_BounceLight", type='AREA')
        light_data.color = material_color
        light_data.energy = emission_strength * 20 * (scale ** 2)
        light_data.shape = 'RECTANGLE'
        light_data.size = len(text_string) * 0.8 * scale
        light_data.size_y = 1.0 * scale
        
        light_obj = bpy.data.objects.new(name=f"{object_name}_LightObj", object_data=light_data)
        scene.collection.objects.link(light_obj)
        
        light_obj.location = Vector(location)
        # Point the light backwards towards the wall (+Y)
        light_obj.rotation_euler = (math.radians(90), 0, 0)
        
    # Attempt to enable Bloom for older EEVEE versions to enhance the glow
    try:
        if scene.render.engine == 'BLENDER_EEVEE':
            scene.eevee.use_bloom = True
            scene.eevee.bloom_intensity = 0.05
            scene.eevee.bloom_radius = 6.0
    except AttributeError:
        # Blender 4.2+ handles bloom differently (compositor), safe to ignore
        pass

    return f"Created procedural neon sign '{object_name}' displaying '{text_string}' at {location}"
```