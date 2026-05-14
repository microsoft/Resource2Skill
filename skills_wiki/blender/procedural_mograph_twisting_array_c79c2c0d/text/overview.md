# Procedural MoGraph Twisting Array

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural MoGraph Twisting Array

* **Core Visual Mechanism**: This technique uses a generative array system (built via Geometry Nodes) to stack a base object (a rounded, frosted glass card) and apply a cascading, time-driven mathematical transformation. By multiplying the instance index by a sine wave of the scene time, the array produces an organic, looping "twirl" or "twist" animation that ripples through the stacked objects.
* **Why Use This Skill (Rationale)**: Traditional keyframing of multiple objects is tedious and hard to iterate on. This procedural approach condenses the entire animation into a single parameterized modifier. The addition of `Object Info -> Random` in the shader ensures that each instanced card receives a unique color from a predefined palette, adding instant visual richness without needing multiple materials.
* **Overall Applicability**: Perfect for abstract motion graphics, stylized UI backgrounds, tech/sci-fi visualizations, or dynamic hero props in product rendering. 
* **Value Addition**: Transforms a simple, static primitive into a complex, animated motion graphics assembly that loops perfectly and reacts seamlessly to lighting due to its refractive material properties.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Base Mesh**: A standard cube scaled in Edit Mode to the proportions of a playing card/panel (thick along Z, thin along Y).
  - **Modifiers**: A `Bevel` modifier (clamped, small width) rounds the sharp edges, followed by a `Subdivision Surface` modifier to ensure buttery smooth reflections.
  - **Geometry Nodes**: A custom node tree replaces the standard Array modifier. It uses a `Mesh Line` to generate points, `Instance on Points` to duplicate the card, and a mathematical chain (`Scene Time` $\times$ `Sine` $\times$ `Index`) to drive the Z/Y rotation.

* **Step B: Materials & Shading**
  - **Shader Model**: Principled BSDF optimized for frosted glass.
  - **Transmission**: Set to `0.9` with a Roughness of `0.25` to blur the refractions behind it.
  - **Coloring**: A `ColorRamp` node holds a specific MoGraph palette (Peach `(0.9, 0.4, 0.2)`, Maroon `(0.3, 0.05, 0.1)`, Dark Gray `(0.1, 0.1, 0.12)`, and Red `(0.8, 0.1, 0.1)`). It is driven by an `Object Info -> Random` node, assigning a unique color to every instance.

* **Step C: Lighting & Rendering Context**
  - **Engine**: EEVEE (with Screen Space Reflections & Refraction enabled) or Cycles.
  - **Lighting**: A warm, high-intensity Area light positioned off-camera to cast distinct highlights and drive light through the refractive surfaces.

* **Step D: Animation & Dynamics**
  - Completely driverless and keyframeless. Relies entirely on the `Scene Time` node within Geometry Nodes, ensuring the twisting animation plays automatically and loops endlessly.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Base Mesh & Smoothing | `bmesh` + Modifiers | `bmesh` allows for object-space scaling (keeping Object scale at 1.0), which ensures the Bevel modifier is perfectly uniform. |
| Cascading Twist Animation | Geometry Nodes | GN handles instancing, math-based procedural rotation, and animation (`Scene Time` node) all in a single portable block without needing Python f-curves or drivers. |
| Multi-color Instancing | Shader Nodes (`Object Info`) | Modern Blender renderers assign unique random IDs to GN instances, allowing one material to color an entire array procedurally. |

> **Feasibility Assessment**: 100% reproduction. The code completely rebuilds the geometry, the cascading twist animation, the frosted glass material, and the unique color assignment shown in the MoGraph toolbox demonstration.

#### 3b. Complete Reproduction Code

```python
def create_object(
    scene_name: str = "Scene",
    object_name: str = "MoGraph_Twist_Array",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.9, 0.4, 0.2),
    **kwargs,
) -> str:
    """
    Create an animated, twisting array of frosted glass cards using Geometry Nodes.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) dominant base color in 0-1 range.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import bmesh
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # Enable EEVEE refraction for the glass look if using EEVEE
    if hasattr(scene, "eevee"):
        scene.eevee.use_ssr = True
        scene.eevee.use_ssr_refraction = True

    # ==========================================
    # HELPER 1: Geometry Nodes Setup
    # ==========================================
    def create_gn_group():
        name = "MoGraph_Array_Twist"
        if name in bpy.data.node_groups:
            return bpy.data.node_groups[name]
        
        group = bpy.data.node_groups.new(name, 'GeometryNodeTree')
        
        # Cross-version compatibility for Inputs/Outputs
        if hasattr(group, "interface"): # Blender 4.0+
            group.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
            group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
        else: # Blender 3.x
            group.inputs.new('NodeSocketGeometry', "Geometry")
            group.outputs.new('NodeSocketGeometry', "Geometry")
        
        nodes = group.nodes
        links = group.links
        
        input_node = nodes.new('NodeGroupInput')
        output_node = nodes.new('NodeGroupOutput')
        
        # Mesh Line (Generates the stack)
        line_node = nodes.new('GeometryNodeMeshLine')
        line_node.inputs['Count'].default_value = 7
        line_node.inputs['Offset'].default_value = (0.0, 0.3, 0.0) # Stack closely along Y
        
        # Instance on Points
        iop_node = nodes.new('GeometryNodeInstanceOnPoints')
        links.new(line_node.outputs['Mesh'], iop_node.inputs['Points'])
        links.new(input_node.outputs['Geometry'], iop_node.inputs['Instance'])
        
        # Animation Logic: Index * (sin(Time * Speed) * Amplitude)
        time_node = nodes.new('GeometryNodeInputSceneTime')
        index_node = nodes.new('GeometryNodeInputIndex')
        
        math_speed = nodes.new('ShaderNodeMath')
        math_speed.operation = 'MULTIPLY'
        math_speed.inputs[1].default_value = 2.0 # Animation speed
        links.new(time_node.outputs['Seconds'], math_speed.inputs[0])
        
        math_sin = nodes.new('ShaderNodeMath')
        math_sin.operation = 'SINE'
        links.new(math_speed.outputs['Value'], math_sin.inputs[0])
        
        math_amp = nodes.new('ShaderNodeMath')
        math_amp.operation = 'MULTIPLY'
        math_amp.inputs[1].default_value = 0.4 # Max twist per card (radians)
        links.new(math_sin.outputs['Value'], math_amp.inputs[0])
        
        math_twist = nodes.new('ShaderNodeMath')
        math_twist.operation = 'MULTIPLY'
        links.new(index_node.outputs['Index'], math_twist.inputs[0])
        links.new(math_amp.outputs['Value'], math_twist.inputs[1])
        
        # Apply to Y axis rotation
        combine_node = nodes.new('ShaderNodeCombineXYZ')
        links.new(math_twist.outputs['Value'], combine_node.inputs['Y'])
        
        links.new(combine_node.outputs['Vector'], iop_node.inputs['Rotation'])
        links.new(iop_node.outputs['Instances'], output_node.inputs['Geometry'])
        
        return group

    # ==========================================
    # HELPER 2: Frosted Glass Material Setup
    # ==========================================
    def create_material():
        mat_name = f"{object_name}_FrostedGlass"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        bsdf = nodes.get("Principled BSDF")
        
        # Cross-version compatibility for Transmission & Specular
        if "Transmission Weight" in bsdf.inputs: bsdf.inputs["Transmission Weight"].default_value = 0.9
        elif "Transmission" in bsdf.inputs: bsdf.inputs["Transmission"].default_value = 0.9
            
        if "Specular IOR Level" in bsdf.inputs: bsdf.inputs["Specular IOR Level"].default_value = 0.8
        elif "Specular" in bsdf.inputs: bsdf.inputs["Specular"].default_value = 0.8
            
        bsdf.inputs["Roughness"].default_value = 0.25
        
        # Color Variation based on Instance ID
        obj_info = nodes.new('ShaderNodeObjectInfo')
        ramp = nodes.new('ShaderNodeValToRGB')
        
        ramp.color_ramp.elements[0].position = 0.0
        ramp.color_ramp.elements[0].color = (*material_color, 1.0)
        
        ramp.color_ramp.elements[1].position = 0.3
        ramp.color_ramp.elements[1].color = (0.3, 0.05, 0.1, 1.0) # Maroon
        
        el3 = ramp.color_ramp.elements.new(0.6)
        el3.color = (0.1, 0.1, 0.12, 1.0) # Dark Gray
        
        el4 = ramp.color_ramp.elements.new(0.9)
        el4.color = (0.8, 0.1, 0.1, 1.0) # Red
        
        links.new(obj_info.outputs['Random'], ramp.inputs['Fac'])
        links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
        
        mat.use_screen_refraction = True
        mat.blend_method = 'HASHED' 
        return mat

    # ==========================================
    # MAIN: Construct Object
    # ==========================================
    
    # 1. Base Mesh Creation (Rounded Card)
    mesh = bpy.data.meshes.new(f"{object_name}_Mesh")
    obj = bpy.data.objects.new(object_name, mesh)
    scene.collection.objects.link(obj)
    
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    # Scale in edit mode so Object scale remains (1,1,1) for uniform beveling
    bmesh.ops.scale(bm, vec=(1.0, 0.1, 1.5), verts=bm.verts)
    bm.to_mesh(mesh)
    bm.free()
    
    for poly in mesh.polygons:
        poly.use_smooth = True
        
    # 2. Add Modifiers
    bevel = obj.modifiers.new("Bevel", 'BEVEL')
    bevel.width = 0.04
    bevel.segments = 6
    
    subsurf = obj.modifiers.new("Subdivision", 'SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2
    
    gn_mod = obj.modifiers.new("MoGraph_Array", 'NODES')
    gn_mod.node_group = create_gn_group()
    
    # 3. Add Material
    mat = create_material()
    obj.data.materials.append(mat)
    
    # 4. Add Complimentary Lighting
    light_data = bpy.data.lights.new(name=f"{object_name}_AreaLight", type='AREA')
    light_data.energy = 1000
    light_data.size = 3.0
    light_data.color = (1.0, 0.95, 0.9)
    light_obj = bpy.data.objects.new(name=f"{object_name}_Light", object_data=light_data)
    scene.collection.objects.link(light_obj)
    
    # 5. Position Elements
    obj.location = Vector(location)
    obj.scale = (scale, scale, scale)
    
    light_obj.location = Vector(location) + Vector((3 * scale, -4 * scale, 3 * scale))
    direction = Vector(location) - light_obj.location
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    return f"Created '{obj.name}' with procedural MoGraph Array animation and lighting at {location}."
```