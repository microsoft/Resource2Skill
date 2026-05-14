# Stylized Isometric Environment with Volumetric God-Rays

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Stylized Isometric Environment with Volumetric God-Rays

* **Core Visual Mechanism**: This pattern relies on three distinct visual pillars:
  1. **"N-gons are OK" Geometric Chipping**: Using targeted vertex bevels on a low-poly mesh to procedurally generate flat N-gons at the corners. When combined with flat shading, this creates the signature "chunky, damaged wood/stone" look of stylized games.
  2. **Hierarchical Grouping**: Using an `Empty` as the root object for a localized diorama. This allows an entire micro-scene (floorboards, walls, cutters) to be moved, scaled, and snapped to a floor grid without destroying relative layouts.
  3. **Contained Volumetrics**: Using a dedicated bounding box with a `Volume Scatter` shader, pierced by a high-intensity `Spot Light` filtered through a geometric window. This creates crisp, atmospheric "god-rays" (crepuscular rays) without polluting the global environment.

* **Why Use This Skill (Rationale)**: Low-poly scenes often look flat, plastic, and uninteresting if rendered with default lighting and primitive shapes. Adding macro/micro variations (loop cuts + vertex chipping) breaks up the silhouette. Coupling this with volumetric lighting instantly adds depth, scale, and cinematic mood to an otherwise simple diorama.

* **Overall Applicability**: Perfect for isometric room setups, magical diorama renders, stylized prop showcases, and low-poly environment generation.

* **Value Addition**: Transforms primitive cubes into a complete, atmospheric stylized vignette. It provides a foundational template for how to light and structure low-poly assets so they look professional rather than amateur.

### 2. Technical Breakdown

* **Step A: Geometry & Topology**
  - **Floorboards**: Base cubes scaled into planks. Subdivided (using bmesh) to add internal vertices. A randomized positional offset (noise) is applied to all vertices to subtly warp the shape. Finally, random outer corner vertices are targeted with a Vertex Bevel, carving out flat N-gons that mimic chipped wood.
  - **Architecture**: A simple wall with a boolean cutter window is generated to act as a "gobo" (light blocker) to shape the God-rays.
  - **Topology**: Flat shading is enforced. Topology contains intentional N-gons and Triangles, adhering to the principle that flat-shaded, non-deforming hard surface objects do not require perfect quad flow.

* **Step B: Materials & Shading**
  - **Stylized Wood**: A basic `Principled BSDF` with high roughness (`0.85`), low specular (`0.1`), and a rich brown base color `(0.25, 0.15, 0.08)`.
  - **Volumetric Fog**: A `ShaderNodeVolumeScatter` node with a density of `0.05` and a high anisotropy (`0.7`) to emphasize forward light scattering.

* **Step C: Lighting & Rendering Context**
  - **God-Ray Source**: A `SPOT` light positioned behind the wall, pointed precisely at the origin. It has an extreme energy level (`20,000 W`) and a tight blend to force beams through the boolean window.
  - **World**: The World background is darkened to `(0.01, 0.01, 0.02)` so the volumetric rays pop against the darkness.
  - **Engine**: EEVEE is highly recommended for real-time volumetrics, though Cycles will render it physically accurately. 

* **Step D: Organization**
  - All generated meshes (planks, wall, cutter) are parented to a central `Empty` (Axes). Moving the Empty safely transports the entire lit vignette.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Stylized Chipping | `bmesh.ops.bevel` (Affecting Vertices) | Dynamically creates custom N-gons on corners, perfectly mimicking the "Ctrl+Shift+B" manual modeling trick. |
| Volumetrics | `ShaderNodeVolumeScatter` + Spot Light | Creates isolated atmospheric depth and crisp god-rays compatible with EEVEE's volumetric engine. |
| Organization | `bpy.data.objects.new(..., None)` (Empties) | Encapsulates the multi-object scene into a single transformable unit. |

> **Feasibility Assessment**: 100% of the core techniques (N-gon chipping, hierarchical Empties, lighting references/god-rays) are procedurally reproduced. The code generates a fully lit, chipped-wood isometric floor and wall setup.

#### 3b. Complete Reproduction Code

```python
def create_isometric_godray_scene(
    scene_name: str = "Scene",
    object_name: str = "StylizedDiorama",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    plank_count: int = 6,
    plank_color: tuple = (0.25, 0.12, 0.05),
    light_color: tuple = (1.0, 0.85, 0.6),
    **kwargs
) -> str:
    """
    Create a stylized isometric diorama with chipped floorboards and volumetric god-rays.
    
    Args:
        scene_name: Target scene name.
        object_name: Base name for the generated objects and root Empty.
        location: (x, y, z) world-space placement for the diorama.
        scale: Uniform scale multiplier.
        plank_count: Number of floorboards to generate.
        plank_color: RGB tuple for the wood material.
        light_color: RGB tuple for the God-ray spot light.
        
    Returns:
        Status string detailing the generation.
    """
    import bpy
    import bmesh
    import random
    import math
    from mathutils import Vector
    
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Enable Volumetrics in EEVEE
    if bpy.context.scene.render.engine == 'BLENDER_EEVEE':
        scene.eevee.use_volumetric = True
        scene.eevee.use_volumetric_shadows = True

    # Darken world background to make god-rays visible
    if scene.world and scene.world.use_nodes:
        bg_node = scene.world.node_tree.nodes.get("Background")
        if bg_node:
            bg_node.inputs['Color'].default_value = (0.01, 0.01, 0.02, 1.0)
            bg_node.inputs['Strength'].default_value = 0.2

    # === Step 1: Materials ===
    # Stylized Wood
    mat_wood = bpy.data.materials.new(f"{object_name}_Wood")
    mat_wood.use_nodes = True
    bsdf = mat_wood.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*plank_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.85
        if 'Specular IOR Level' in bsdf.inputs: # Blender 4.0+
            bsdf.inputs['Specular IOR Level'].default_value = 0.1
        elif 'Specular' in bsdf.inputs:         # Blender 3.x
            bsdf.inputs['Specular'].default_value = 0.1

    # Volumetric Fog
    mat_vol = bpy.data.materials.new(f"{object_name}_Fog")
    mat_vol.use_nodes = True
    v_nodes = mat_vol.node_tree.nodes
    v_nodes.clear()
    out_node = v_nodes.new('ShaderNodeOutputMaterial')
    scatter_node = v_nodes.new('ShaderNodeVolumeScatter')
    scatter_node.inputs['Density'].default_value = 0.06
    scatter_node.inputs['Anisotropy'].default_value = 0.7 # Forward scattering
    mat_vol.node_tree.links.new(scatter_node.outputs[0], out_node.inputs['Volume'])

    # === Step 2: Root Empty (Tip 4: Use Empties) ===
    root_empty = bpy.data.objects.new(f"{object_name}_Root", None)
    root_empty.empty_display_type = 'ARROWS'
    root_empty.empty_display_size = 2.0 * scale
    root_empty.location = location
    scene.collection.objects.link(root_empty)

    # === Step 3: Generating Chipped Planks (Tips 1 & 2: Complexity & Ngons) ===
    plank_w = 0.8 * scale
    plank_l = 4.0 * scale
    plank_h = 0.2 * scale
    gap = 0.05 * scale

    for i in range(plank_count):
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(plank_l, plank_w, plank_h), verts=bm.verts)
        
        # Subdivide to get internal geometry
        bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=2, use_grid_fill=True)
        
        # Warp/Noise
        for v in bm.verts:
            v.co.x += random.uniform(-0.02, 0.02) * scale
            v.co.y += random.uniform(-0.02, 0.02) * scale
            v.co.z += random.uniform(-0.01, 0.01) * scale
            
        # Target outer/top vertices for chipping
        chip_candidates = []
        for v in bm.verts:
            if v.co.z > (plank_h * 0.3): # Top half
                if abs(v.co.y) > (plank_w * 0.3) or abs(v.co.x) > (plank_l * 0.4): # Outer edges
                    chip_candidates.append(v)
                    
        random.shuffle(chip_candidates)
        num_chips = random.randint(2, 6)
        chips = chip_candidates[:num_chips]
        
        # Execute Vertex Bevel to create N-gon chips
        if chips:
            bmesh.ops.bevel(bm, geom=chips, offset=random.uniform(0.05, 0.15)*scale, affect='VERTICES')
            
        mesh = bpy.data.meshes.new(f"{object_name}_PlankMesh_{i}")
        bm.to_mesh(mesh)
        bm.free()
        
        # Enforce flat shading for stylized look
        for poly in mesh.polygons:
            poly.use_smooth = False
            
        plank_obj = bpy.data.objects.new(f"{object_name}_Plank_{i}", mesh)
        scene.collection.objects.link(plank_obj)
        plank_obj.data.materials.append(mat_wood)
        
        # Position locally relative to the root empty
        y_offset = (i - plank_count / 2.0 + 0.5) * (plank_w + gap)
        plank_obj.location = (0, y_offset, 0)
        plank_obj.parent = root_empty

    # === Step 4: Wall & Window (Gobo for Light) ===
    bm_wall = bmesh.new()
    bmesh.ops.create_cube(bm_wall, size=1.0)
    bmesh.ops.scale(bm_wall, vec=(0.2 * scale, 5.0 * scale, 4.0 * scale), verts=bm_wall.verts)
    wall_mesh = bpy.data.meshes.new(f"{object_name}_WallMesh")
    bm_wall.to_mesh(wall_mesh)
    bm_wall.free()
    
    wall_obj = bpy.data.objects.new(f"{object_name}_Wall", wall_mesh)
    scene.collection.objects.link(wall_obj)
    wall_obj.location = (-plank_l/2 - 0.5*scale, 0, 2.0*scale)
    wall_obj.parent = root_empty
    wall_obj.data.materials.append(mat_wood)
    
    # Boolean Cutter for Window
    bm_cut = bmesh.new()
    bmesh.ops.create_cube(bm_cut, size=1.0)
    bmesh.ops.scale(bm_cut, vec=(1.0 * scale, 1.5 * scale, 1.5 * scale), verts=bm_cut.verts)
    cut_mesh = bpy.data.meshes.new(f"{object_name}_CutterMesh")
    bm_cut.to_mesh(cut_mesh)
    bm_cut.free()
    
    cut_obj = bpy.data.objects.new(f"{object_name}_WindowCutter", cut_mesh)
    scene.collection.objects.link(cut_obj)
    cut_obj.location = wall_obj.location + Vector((0, 0, 0.5*scale))
    cut_obj.parent = root_empty
    cut_obj.display_type = 'WIRE'
    cut_obj.hide_render = True
    
    bool_mod = wall_obj.modifiers.new(name="WindowCut", type='BOOLEAN')
    bool_mod.object = cut_obj
    bool_mod.operation = 'DIFFERENCE'

    # === Step 5: Volumetric God-Ray Lighting ===
    # Volume Domain
    bm_vol = bmesh.new()
    bmesh.ops.create_cube(bm_vol, size=1.0)
    bmesh.ops.scale(bm_vol, vec=(15.0*scale, 15.0*scale, 10.0*scale), verts=bm_vol.verts)
    vol_mesh = bpy.data.meshes.new(f"{object_name}_VolMesh")
    bm_vol.to_mesh(vol_mesh)
    bm_vol.free()
    
    vol_obj = bpy.data.objects.new(f"{object_name}_VolumeDomain", vol_mesh)
    scene.collection.objects.link(vol_obj)
    vol_obj.location = Vector(location) + Vector((0, 0, 2.0*scale))
    vol_obj.data.materials.append(mat_vol)
    vol_obj.display_type = 'BOUNDS'
    
    # Spot Light
    spot_data = bpy.data.lights.new(name=f"{object_name}_GodRay", type='SPOT')
    spot_data.energy = 25000 * (scale**2) # Scale energy with object size
    spot_data.spot_size = math.radians(45)
    spot_data.spot_blend = 0.5
    spot_data.color = light_color
    
    spot_obj = bpy.data.objects.new(f"{object_name}_SpotLight", spot_data)
    scene.collection.objects.link(spot_obj)
    
    # Position light outside the window, pointing at the center
    spot_loc = Vector(location) + Vector((-5.0 * scale, 0, 5.0 * scale))
    spot_obj.location = spot_loc
    
    # Track to origin
    direction = Vector(location) - spot_loc
    spot_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    # === Step 6: Isometric Camera Override (Optional Viewer Setup) ===
    cam_data = bpy.data.cameras.new(f"{object_name}_IsoCam")
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = 8.0 * scale
    cam_obj = bpy.data.objects.new(f"{object_name}_Camera", cam_data)
    scene.collection.objects.link(cam_obj)
    cam_obj.location = Vector(location) + Vector((10*scale, -10*scale, 10*scale))
    cam_obj.rotation_euler = (math.radians(54.736), 0, math.radians(45)) # True isometric angle
    
    return f"Created '{object_name}' vignette at {location}. Generated {plank_count} procedural planks with N-gon chips, volumetric domain, and god-rays."
```