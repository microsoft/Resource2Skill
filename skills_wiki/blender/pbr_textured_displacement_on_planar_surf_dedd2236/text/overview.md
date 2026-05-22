### 1. High-level Design Pattern Extraction

**Skill Name**: PBR Textured Displacement on Planar Surface

*   **Core Visual Mechanism**: This skill generates a detailed, physically-based rendered (PBR) surface with true geometric displacement, using multiple image textures (Albedo, Roughness, Normal, Displacement/Height Map). The defining visual feature is the realistic surface relief and material properties derived from these maps, especially the 3D depth provided by displacement.

*   **Why Use This Skill (Rationale)**: This technique creates highly realistic surfaces by simulating intricate geometric detail (displacement) and detailed light interaction (PBR maps). It is crucial for adding environmental realism to flat surfaces like floors, walls, and ground planes, making them appear rough, bumpy, or uneven without complex manual modeling. The PBR workflow ensures that materials react correctly to light, producing believable reflections and shading.

*   **Overall Applicability**: This skill excels in:
    *   **Architectural Visualization**: Realistic stone walls, brick facades, concrete floors.
    *   **Game Environments**: Detailed terrain, rocky paths, historical building surfaces.
    *   **Product Visualization**: Adding realistic surface imperfections to objects.
    *   **General 3D Scenes**: Any scenario requiring a flat object to have complex, tactile surface detail.

*   **Value Addition**: Compared to a default primitive, this skill transforms a simple flat plane into a complex, visually rich surface with genuine 3D relief. It adds realism and depth that cannot be achieved with basic colors or bump maps alone, significantly enhancing the visual fidelity of the scene.

### 2. Technical Breakdown

*   **Step A: Geometry & Topology**
    *   **Base Mesh**: A simple `Plane` primitive is used as the foundation.
    *   **Modifiers**: A `Subdivision Surface` modifier is applied. This is critical because true displacement requires a high-resolution mesh for the displacement map to deform the geometry. The modifier non-destructively increases the polygon count, allowing for adjustable detail.
    *   **Topology Flow**: The plane's simple quad topology is maintained, ensuring clean subdivision.

*   **Step B: Materials & Shading**
    *   **Shader Model**: `Principled BSDF` (Physically Based Shader) is the core shader, offering a comprehensive set of parameters for realistic material representation.
    *   **Textures**: Four primary image textures are used, typically sourced from PBR texture sets:
        1.  **Base Color (Albedo)**: Provides the surface's color information. Color space should be `sRGB`.
        2.  **Roughness**: Controls the micro-surface detail and how light scatters/reflects. Color space should be `Non-Color`.
        3.  **Normal Map**: Adds fine surface detail and bumps by faking lighting direction. Connected via a `Normal Map` node. Color space should be `Non-Color`.
        4.  **Displacement (Height Map)**: Provides grayscale height information to geometrically displace the mesh. Connected via a `Displacement` node. Color space should be `Non-Color`.
    *   **Specific Values**: Roughness and metallic values will depend on the loaded textures. `Normal Map` node strength defaults to 1. `Displacement` node has adjustable `Scale` (e.g., 0.2) and `Midlevel` (e.g., 0.5) parameters.
    *   **Displacement Method**: Crucially, the material's Cycles settings for Displacement must be set to `Displacement Only` or `Displacement and Bump` to enable actual geometric deformation.

*   **Step C: Lighting & Rendering Context**
    *   **Lighting Setup**: A `Sun` light is often used to demonstrate the displacement effect clearly, creating strong shadows and highlights that emphasize the surface's 3D features. The sun's direction and strength are adjustable.
    *   **Render Engine**: `Cycles` is explicitly required for true geometric displacement. EEVEE can only simulate displacement via bump mapping or shader-based displacement, not actual mesh deformation.
    *   **World Settings**: Default world settings are generally sufficient, but an HDRI could enhance reflections.

*   **Step D: Animation & Dynamics (if applicable)**
    *   Not applicable for this static material setup.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect         | Method                            | Why this method                                                                    |
| :--------------------------- | :-------------------------------- | :--------------------------------------------------------------------------------- |
| Base mesh shape              | `bpy.ops.mesh.primitive_plane_add()` | The tutorial starts with a plane.                                                  |
| Geometric detail (displacement) | `Subdivision Surface` modifier  | Provides controllable mesh resolution for displacement, non-destructive.           |
| PBR material setup           | Shader node tree (`bpy.data.materials`) | Directly recreates the Node Wrangler's automatic PBR setup.                        |
| Lighting                     | `bpy.data.lights.new(type='SUN')` | Replicates the Sun lamp used in the tutorial for clear illumination.               |
| True displacement rendering  | `mat.cycles.displacement_method` | Essential setting to enable geometric displacement in Cycles.                      |
| Render engine                | `scene.render.engine = 'CYCLES'`  | Cycles is required for true displacement.                                          |

> **Feasibility Assessment**: This code reproduces **~90%** of the tutorial's visual effect and 100% of the technical setup. The core node configuration for PBR materials with displacement, the necessary geometry, and render settings are all reproduced. The only missing part is the actual loading of the specific texture *image files* from Poly Haven, as the code cannot directly access local user files. Users will need to manually load their downloaded images into the created `Image Texture` nodes in the Shader Editor for the complete visual result.

#### 3b. Complete Reproduction Code

```python
def create_pbr_rock_wall(
    scene_name: str = "Scene",
    object_name: str = "PBR_RockWall_Plane",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    subdivision_levels: int = 4,
    displacement_scale: float = 0.2,
    displacement_midlevel: float = 0.5,
    light_strength: float = 5.0,
    light_rotation_euler: tuple = (0.785, 0.523, 2.356), # ~45, 30, 135 degrees in radians
    **kwargs,
) -> str:
    """
    Create a plane with a PBR rock wall material setup, including displacement,
    emulating the Node Wrangler workflow. User needs to load image textures manually.

    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created plane object.
        location: (x, y, z) world-space position for the plane.
        scale: Uniform scale factor for the plane.
        subdivision_levels: Number of subdivision levels for the Subdivision Surface modifier (for displacement).
        displacement_scale: Scale factor for the Displacement node.
        displacement_midlevel: Midlevel value for the Displacement node.
        light_strength: Strength of the Sun light added to the scene.
        light_rotation_euler: (x, y, z) Euler rotation for the Sun light in radians.
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'PBR_RockWall_Plane' at (0, 0, 0) with PBR material setup."
    """
    import bpy
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.context.scene

    # --- 1. Create Base Geometry (Plane) ---
    # Create the plane
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0,0,0))
    plane_obj = bpy.context.active_object
    plane_obj.name = object_name
    plane_obj.location = Vector(location)
    plane_obj.scale = (scale, scale, scale)

    # Add Subdivision Surface Modifier for displacement
    subdiv_mod = plane_obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv_mod.render_levels = subdivision_levels
    subdiv_mod.levels = subdivision_levels # For viewport preview

    # --- 2. Build Material and Shader Node Tree ---
    mat_name = f"{object_name}_Material"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    if plane_obj.data.materials:
        plane_obj.data.materials[0] = mat
    else:
        plane_obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Access existing default nodes or create if somehow missing
    principled_bsdf = nodes.get("Principled BSDF")
    if not principled_bsdf:
        principled_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled_bsdf.name = "Principled BSDF"
    principled_bsdf.location = (0, 0)

    material_output = nodes.get("Material Output")
    if not material_output:
        material_output = nodes.new(type='ShaderNodeOutputMaterial')
        material_output.name = "Material Output"
    material_output.location = (400, 0)

    # Clean up any other nodes that might have been there
    for node in list(nodes): # Iterate over a copy to allow removal
        if node not in [principled_bsdf, material_output]:
            nodes.remove(node)

    # Connect Principled BSDF to Material Output
    if not principled_bsdf.outputs['BSDF'].is_linked_to(material_output.inputs['Surface']):
        links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])

    # Create Image Texture nodes (placeholders - user must load actual images)
    # 1. Base Color (Albedo)
    node_albedo = nodes.new(type='ShaderNodeTexImage')
    node_albedo.label = "PBR_BaseColor"
    node_albedo.location = (-800, 300)
    links.new(node_albedo.outputs['Color'], principled_bsdf.inputs['Base Color'])

    # 2. Roughness
    node_roughness = nodes.new(type='ShaderNodeTexImage')
    node_roughness.label = "PBR_Roughness"
    node_roughness.location = (-800, 100)
    node_roughness.image_user.colorspace_settings.name = 'Non-Color' # Important for non-color data
    links.new(node_roughness.outputs['Color'], principled_bsdf.inputs['Roughness'])

    # 3. Normal Map
    node_normal_map_img = nodes.new(type='ShaderNodeTexImage')
    node_normal_map_img.label = "PBR_Normal"
    node_normal_map_img.location = (-800, -100)
    node_normal_map_img.image_user.colorspace_settings.name = 'Non-Color' # Important for non-color data

    node_normal_map = nodes.new(type='ShaderNodeNormalMap')
    node_normal_map.location = (-400, -100)
    links.new(node_normal_map_img.outputs['Color'], node_normal_map.inputs['Color'])
    links.new(node_normal_map.outputs['Normal'], principled_bsdf.inputs['Normal'])

    # 4. Displacement (Height Map)
    node_displacement_img = nodes.new(type='ShaderNodeTexImage')
    node_displacement_img.label = "PBR_Displacement"
    node_displacement_img.location = (-800, -300)
    node_displacement_img.image_user.colorspace_settings.name = 'Non-Color' # Important for non-color data

    node_displacement = nodes.new(type='ShaderNodeDisplacement')
    node_displacement.location = (0, -300)
    node_displacement.inputs['Scale'].default_value = displacement_scale
    node_displacement.inputs['Midlevel'].default_value = displacement_midlevel
    links.new(node_displacement_img.outputs['Color'], node_displacement.inputs['Height'])
    links.new(node_displacement.outputs['Displacement'], material_output.inputs['Displacement'])

    # --- 3. Enable True Displacement for Cycles ---
    mat.cycles.displacement_method = 'BOTH'

    # --- 4. Lighting Setup (Sun Lamp) ---
    sun_light_name = f"{object_name}_SunLight"
    
    # Check if a light with the same name already exists
    sun_obj = bpy.data.objects.get(sun_light_name)
    if not sun_obj:
        sun_data = bpy.data.lights.new(name=sun_light_name, type='SUN')
        sun_data.energy = light_strength
        sun_obj = bpy.data.objects.new(name=sun_light_name, object_data=sun_data)
        scene.collection.objects.link(sun_obj)
    else:
        # If it exists, update its data
        if sun_obj.data.type == 'SUN':
            sun_obj.data.energy = light_strength
        else: # If a non-sun light has the same name, rename it to avoid conflict
            sun_obj.name = f"{sun_obj.name}_old"
            sun_light_name = f"{object_name}_SunLight"
            sun_data = bpy.data.lights.new(name=sun_light_name, type='SUN')
            sun_data.energy = light_strength
            sun_obj = bpy.data.objects.new(name=sun_light_name, object_data=sun_data)
            scene.collection.objects.link(sun_obj)


    # Set light position and rotation for directional light
    sun_obj.location = Vector((10.0, 10.0, 10.0)) # Position is not critical for Sun, direction matters
    sun_obj.rotation_euler = light_rotation_euler

    # --- 5. Set Render Engine to Cycles ---
    scene.render.engine = 'CYCLES'
    
    # Optional: Set Cycles compute device to GPU if available and supported
    if 'cycles' in bpy.context.preferences.addons:
        cycles_prefs = bpy.context.preferences.addons['cycles'].preferences
        # Prefer OPTIX, then CUDA, then OpenCL, otherwise CPU
        if cycles_prefs.compute_device_type == 'OPTIX':
            scene.cycles.device = 'GPU'
        elif cycles_prefs.compute_device_type == 'CUDA':
            scene.cycles.device = 'GPU'
        elif cycles_prefs.compute_device_type == 'OPENCL':
            scene.cycles.device = 'GPU'
        else:
            scene.cycles.device = 'CPU'
    else:
        scene.cycles.device = 'CPU' # Fallback if Cycles addon somehow not found

    return f"Created '{object_name}' at {location} with PBR material setup. " \
           f"Please load your PBR texture images into the Image Texture nodes named 'PBR_BaseColor', 'PBR_Roughness', 'PBR_Normal', and 'PBR_Displacement' in the Shader Editor."

```

#### 3c. Verification Checklist

- [x] Does the code import all required modules INSIDE the function body? Yes (`bpy`, `mathutils`, `math`).
- [x] Is it purely ADDITIVE (no scene clearing, no deleting existing objects)? Yes, new objects and materials are added. Existing lights with the same name are updated or new ones created with distinct names.
- [x] Does it set `obj.name = object_name` so the object is identifiable? Yes, for the plane and the sun light.
- [x] Are all color values explicit numeric tuples (not referencing undefined variables)? Yes (material colors are determined by textures, light strength is numeric).
- [x] Does it respect the `location` and `scale` parameters? Yes.
- [x] Does the function return a descriptive status string? Yes.
- [x] Would someone looking at the viewport say "yes, that is the technique from the tutorial"? Yes, the full PBR node setup with displacement is created, and the necessary render engine and light are configured. The only manual step is loading the actual image files, which is clearly communicated.
- [x] Does it avoid hardcoded file paths or external image dependencies? Yes, by creating placeholder `Image Texture` nodes.
- [x] Does it handle the case where an object with the same name already exists? Blender automatically appends `.001`, etc., to object names. For the light, it attempts to modify an existing light of the correct type or creates a new one.