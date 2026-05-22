### 1. High-level Design Pattern Extraction

**Skill Name**: PBR Textured Displacement Plane

*   **Core Visual Mechanism**: This skill applies Physically Based Rendering (PBR) textures (Albedo, Roughness, Normal, Displacement) to a simple plane mesh, and crucially, uses the displacement map to create *true geometric displacement* of the mesh. This transforms a flat surface into a highly detailed, volumetric one with realistic undulations and surface relief.

*   **Why Use This Skill (Rationale)**: True displacement, driven by PBR height maps, significantly enhances realism compared to bump or normal mapping alone. It physically alters the mesh, allowing for proper self-shadowing and silhouette changes, making surfaces like rocks, bricks, or uneven ground appear genuinely three-dimensional and tactile. This technique leverages physically accurate material properties for realistic light interaction.

*   **Overall Applicability**: This skill is ideal for adding detailed surfaces to environmental elements such as:
    *   Ground textures (rocky terrain, cobblestones, dirt paths)
    *   Architectural details (brick walls, weathered concrete, carved stone facades)
    *   Detailed props (ancient ruins, broken pottery, industrial plating)
    *   Any large, flat surface that requires realistic depth and texture.

*   **Value Addition**: It elevates a basic geometric primitive (a plane) into a complex, visually rich surface. It automates the setup of PBR materials and true displacement, saving significant manual effort and enabling high-fidelity surface representation with minimal modeling.

### 2. Technical Breakdown

*   **Step A: Geometry & Topology**
    *   **Base Mesh**: A simple `Plane` primitive.
    *   **Modifier**: A `Subdivision Surface` modifier (Catmull-Clark type) is added to the plane. This is essential to provide enough geometric detail (vertices and faces) for the displacement map to physically deform the mesh effectively. The number of subdivision levels is controllable.
    *   **Topology Flow**: Starts with a simple quad plane; the subdivision surface modifier creates clean, subdividable topology suitable for high-detail displacement.

*   **Step B: Materials & Shading**
    *   **Shader Model**: `Principled BSDF` is used as the core shader, providing a physically accurate material model.
    *   **Texture Setup**: A node tree is constructed using `Image Texture` nodes connected to the `Principled BSDF` and `Material Output`.
        *   **Albedo (Base Color)**: An image texture for the primary color information is connected to the `Base Color` input.
        *   **Roughness**: An image texture (set to `Non-Color` data) controls how shiny or dull the surface is, connected to the `Roughness` input.
        *   **Normal**: An image texture (set to `Non-Color` data) is fed into a `Normal Map` node, which then connects to the `Normal` input of the `Principled BSDF`, adding fine surface detail.
        *   **Displacement (Height Map)**: An image texture (set to `Non-Color` data) is connected to a `Displacement` node (specifically, its `Height` input), which then links to the `Displacement` input of the `Material Output` node.
    *   **Mapping**: `Texture Coordinate` and `Mapping` nodes are used to control the UV mapping, allowing for scaling of the textures across the surface.
    *   **Displacement Settings**: In the material's Cycles settings, the `Displacement` method is explicitly set to `Displacement Only` (or `Displacement and Bump`) to enable true mesh deformation. The `Scale` of the `Displacement` node can be adjusted to control the intensity of the deformation.

*   **Step C: Lighting & Rendering Context**
    *   **Render Engine**: `Cycles` is mandated for true displacement to function.
    *   **Lighting**: A `Sun` lamp is used to provide directional lighting, casting strong, realistic shadows that interact with the displaced geometry. The strength and direction of the sun are configurable.
    *   **World/Environment**: Default world settings are assumed, but an HDRI could further enhance realism. GPU compute is optionally enabled for faster rendering if available.

*   **Step D: Animation & Dynamics**: Not applicable to this skill.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
| :------------------- | :-------------------------------- | :------------------------------------------------------ |
| Base geometry        | `bpy.ops.mesh.primitive_plane_add` | Direct creation of a simple plane.                      |
| Surface detail       | `Subdivision Surface` modifier    | Procedural and efficient way to add mesh density for displacement. |
| Material setup       | Shader node tree (bpy API)        | Required for PBR textures and true displacement, emulating Node Wrangler. |
| Lighting             | `bpy.ops.object.light_add`        | To provide realistic shadows and highlights for the displaced surface. |

**Feasibility Assessment**: 100% reproducible if valid texture paths are provided. The core mechanism of applying PBR textures with true displacement is fully supported by Blender's Cycles renderer and node system.

#### 3b. Complete Reproduction Code

```python
def create_pbr_textured_plane(
    scene_name: str = "Scene",
    object_name: str = "PBR_Textured_Plane",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    albedo_path: str = "",
    normal_path: str = "",
    roughness_path: str = "",
    displacement_path: str = "",
    displacement_scale: float = 0.2,
    subdivision_levels: int = 5,
    uv_scale: float = 1.0,
    sun_strength: float = 5.0,
    sun_direction: tuple = (45, 0, 45), # Euler angles in degrees
    **kwargs,
) -> str:
    """
    Create a plane with PBR textures and true displacement in the active Blender scene.

    Args:
        scene_name: Name of the target scene (usually "Scene").
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor (1.0 = default size).
        albedo_path: Absolute path to the albedo/base color texture image (e.g., "C:/Textures/rock_albedo.png").
        normal_path: Absolute path to the normal map texture image (e.g., "C:/Textures/rock_normal.png").
        roughness_path: Absolute path to the roughness texture image (e.g., "C:/Textures/rock_roughness.png").
        displacement_path: Absolute path to the displacement/height map texture image (e.g., "C:/Textures/rock_disp.png").
        displacement_scale: Scale factor for the displacement effect (default 0.2).
        subdivision_levels: Number of subdivision levels for the plane's geometry (default 5).
        uv_scale: Scale factor for the UV mapping of all textures (default 1.0).
        sun_strength: Strength of the added/modified sun lamp (default 5.0).
        sun_direction: (x, y, z) Euler angles in degrees for the sun lamp's rotation (default 45, 0, 45).
        **kwargs: Additional overrides (currently none specific).

    Returns:
        Status string, e.g., "Created 'PBR_Textured_Plane' at (0, 0, 0) with PBR material and displacement."
    """
    import bpy
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]

    # --- 1. Set up Render Engine (Cycles for Displacement) ---
    scene.render.engine = 'CYCLES'
    # Optional: Enable GPU compute if available, as shown in the video context
    try:
        if hasattr(bpy.context.preferences.addons['cycles'].preferences, 'compute_device_type'):
            bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA' # or 'OPTIX'
            bpy.context.preferences.addons['cycles'].preferences.get_devices()
            for d in bpy.context.preferences.addons['cycles'].preferences.devices:
                if d.type == 'CUDA' or d.type == 'OPTIX':
                    d.use = True
                else:
                    d.use = False
    except Exception:
        pass # Fallback to CPU if GPU not available or setup fails

    # --- 2. Create Base Geometry (Plane) ---
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    plane_obj = bpy.context.object
    plane_obj.name = object_name
    plane_obj.location = Vector(location)
    plane_obj.scale = (scale, scale, scale)

    # Add Subdivision Surface modifier for displacement
    subdiv_mod = plane_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv_mod.render_levels = subdivision_levels
    subdiv_mod.levels = subdivision_levels # For viewport
    subdiv_mod.subdivision_type = 'CATMULL_CLARK'

    # --- 3. Build Material with PBR Textures ---
    mat_name = f"{object_name}_Material"
    material = bpy.data.materials.new(name=mat_name)
    material.use_nodes = True
    plane_obj.data.materials.append(material)

    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Clear default nodes for a clean setup (mimics Node Wrangler's fresh setup)
    for node in nodes:
        nodes.remove(node)

    # Create new Principled BSDF and Material Output nodes
    principled_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.location = (0, 0)

    material_output = nodes.new('ShaderNodeOutputMaterial')
    material_output.name = "Material Output"
    material_output.location = (400, 0)

    # Link Principled BSDF to Material Output
    links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])

    # Add Texture Coordinate and Mapping nodes
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 200)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.vector_type = 'TEXTURE'
    mapping.location = (-800, 200)

    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    
    # Set UV scale
    mapping.inputs['Scale'].default_value = (uv_scale, uv_scale, uv_scale)

    # --- Load and connect PBR textures (if paths provided) ---
    # Albedo Texture
    if albedo_path:
        try:
            albedo_image = bpy.data.images.load(albedo_path, check_existing=True)
            albedo_tex = nodes.new('ShaderNodeTexImage')
            albedo_tex.image = albedo_image
            albedo_tex.location = (-400, 300)
            links.new(mapping.outputs['Vector'], albedo_tex.inputs['Vector'])
            links.new(albedo_tex.outputs['Color'], principled_bsdf.inputs['Base Color'])
        except RuntimeError:
            print(f"Warning: Could not load albedo texture from {albedo_path}. Please check the path.")

    # Roughness Texture
    if roughness_path:
        try:
            roughness_image = bpy.data.images.load(roughness_path, check_existing=True)
            roughness_tex = nodes.new('ShaderNodeTexImage')
            roughness_tex.image = roughness_image
            roughness_tex.image.colorspace_settings.name = 'Non-Color' # Important for non-color data
            roughness_tex.location = (-400, 100)
            links.new(mapping.outputs['Vector'], roughness_tex.inputs['Vector'])
            links.new(roughness_tex.outputs['Color'], principled_bsdf.inputs['Roughness'])
        except RuntimeError:
            print(f"Warning: Could not load roughness texture from {roughness_path}. Please check the path.")

    # Normal Map Texture
    if normal_path:
        try:
            normal_image = bpy.data.images.load(normal_path, check_existing=True)
            normal_tex = nodes.new('ShaderNodeTexImage')
            normal_tex.image = normal_image
            normal_tex.image.colorspace_settings.name = 'Non-Color' # Important for non-color data
            normal_tex.location = (-400, -100)
            
            normal_map_node = nodes.new('ShaderNodeNormalMap')
            normal_map_node.location = (-200, -100)
            
            links.new(mapping.outputs['Vector'], normal_tex.inputs['Vector'])
            links.new(normal_tex.outputs['Color'], normal_map_node.inputs['Color'])
            links.new(normal_map_node.outputs['Normal'], principled_bsdf.inputs['Normal'])
        except RuntimeError:
            print(f"Warning: Could not load normal texture from {normal_path}. Please check the path.")

    # Displacement Texture
    if displacement_path:
        try:
            displacement_image = bpy.data.images.load(displacement_path, check_existing=True)
            displacement_tex = nodes.new('ShaderNodeTexImage')
            displacement_tex.image = displacement_image
            displacement_tex.image.colorspace_settings.name = 'Non-Color' # Important for non-color data
            displacement_tex.location = (-400, -300)
            
            displacement_node = nodes.new('ShaderNodeDisplacement')
            displacement_node.location = (200, -300)
            
            displacement_node.inputs['Scale'].default_value = displacement_scale
            # Midlevel default 0.5 is suitable for standard height maps where 50% gray is zero displacement.
            
            links.new(mapping.outputs['Vector'], displacement_tex.inputs['Vector'])
            links.new(displacement_tex.outputs['Color'], displacement_node.inputs['Height'])
            links.new(displacement_node.outputs['Displacement'], material_output.inputs['Displacement'])
            
            # Set material displacement method to 'Displacement Only' as shown in the video
            material.cycles.displacement_method = 'DISPLACEMENT'
        except RuntimeError:
            print(f"Warning: Could not load displacement texture from {displacement_path}. Please check the path.")
    else:
        # If no displacement path is provided, ensure displacement is not active
        material.cycles.displacement_method = 'BUMP' # Default to bump only if no displacement map

    # --- 4. Lighting (Sun Lamp) ---
    # Attempt to find an existing sun light to modify, otherwise create a new one.
    sun_light_obj = None
    for obj in scene.objects:
        if obj.type == 'LIGHT' and obj.data.type == 'SUN':
            sun_light_obj = obj
            break
    
    if sun_light_obj is None:
        # No sun light found, create one
        bpy.ops.object.light_add(type='SUN', location=(0,0,0)) # Position at origin for easier rotation
        sun_light_obj = bpy.context.object
        sun_light_obj.name = f"{object_name}_Sun"
    else:
        print(f"Modifying existing sun light: '{sun_light_obj.name}'")

    sun_light_obj.data.energy = sun_strength
    sun_light_obj.rotation_euler = (math.radians(sun_direction[0]), math.radians(sun_direction[1]), math.radians(sun_direction[2]))

    # Set viewport shading to rendered to immediately see the effect (optional)
    # This part depends on context (e.g., if there's an active 3D view)
    # for area in bpy.context.screen.areas:
    #     if area.type == 'VIEW_3D':
    #         for space in area.spaces:
    #             if space.type == 'VIEW_3D':
    #                 space.shading.type = 'RENDERED'
    #                 break
    #         break

    return f"Created '{object_name}' at {location} with PBR material and displacement."

```

#### 3c. Verification Checklist

- [x] Does the code import all required modules INSIDE the function body?
- [x] Is it purely ADDITIVE (no scene clearing, no deleting existing objects)? (A new plane and material are added. An existing sun light is modified or a new one is added if none exists).
- [x] Does it set `obj.name = object_name` so the object is identifiable?
- [x] Are all color values explicit numeric tuples (not referencing undefined variables)? (No direct material color, but texture paths, sun strength, and direction are explicit).
- [x] Does it respect the `location` and `scale` parameters?
- [x] Does the function return a descriptive status string?
- [x] Would someone looking at the viewport say "yes, that is the technique from the tutorial"? (Yes, provided valid texture maps are supplied).
- [x] Does it avoid hardcoded file paths or external image dependencies? (Yes, by making all texture paths configurable parameters). Warnings are printed if paths are invalid.
- [x] Does it handle the case where an object with the same name already exists (Blender auto-suffixes, but verify no crashes)? (Blender handles duplicate object/material names by appending numbers; image loading uses `check_existing=True`.)