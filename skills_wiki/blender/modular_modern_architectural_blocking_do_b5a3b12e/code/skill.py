def create_object(
    scene_name: str = "Scene",
    object_name: str = "ModernHouse",
    location: tuple = (0, 0, 0),
    scale: float = 1.0,
    material_color: tuple = (0.85, 0.85, 0.85), # Base plaster color
    **kwargs,
) -> str:
    """
    Creates a Modular Modern Architectural blockout with procedural wood/plaster 
    materials and architectural downlighting.

    Args:
        scene_name: Name of the target scene.
        object_name: Base name for the generated objects.
        location: (x, y, z) world-space placement.
        scale: Uniform scale factor.
        material_color: RGB tuple for the main structure color.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    from mathutils import Vector
    import math

    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    base_loc = Vector(location)

    # --- Helper: Create Procedural Materials ---
    def create_plaster_material(name, color):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.6
        output = nodes.new(type="ShaderNodeOutputMaterial")
        
        noise = nodes.new(type="ShaderNodeTexNoise")
        noise.inputs["Scale"].default_value = 50.0
        noise.inputs["Detail"].default_value = 15.0
        
        bump = nodes.new(type="ShaderNodeBump")
        bump.inputs["Strength"].default_value = 0.2
        bump.inputs["Distance"].default_value = 0.1
        
        links.new(noise.outputs["Fac"], bump.inputs["Height"])
        links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
        links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
        return mat

    def create_wood_material(name):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
        bsdf.inputs["Roughness"].default_value = 0.4
        output = nodes.new(type="ShaderNodeOutputMaterial")
        
        wave = nodes.new(type="ShaderNodeTexWave")
        wave.bands_direction = 'Z'
        wave.inputs["Scale"].default_value = 10.0
        wave.inputs["Distortion"].default_value = 5.0
        
        cramp = nodes.new(type="ShaderNodeValToRGB")
        cramp.color_ramp.elements[0].position = 0.3
        cramp.color_ramp.elements[0].color = (0.05, 0.02, 0.01, 1.0)
        cramp.color_ramp.elements[1].position = 0.7
        cramp.color_ramp.elements[1].color = (0.25, 0.12, 0.05, 1.0)
        
        links.new(wave.outputs["Color"], cramp.inputs["Fac"])
        links.new(cramp.outputs["Color"], bsdf.inputs["Base Color"])
        links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
        return mat

    def create_glass_material(name):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.01, 0.01, 0.015, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.05
            # Using basic glossy dark setup for robust exterior architectural glass look
        return mat

    mat_plaster = create_plaster_material(f"{object_name}_Plaster", material_color)
    mat_wood = create_wood_material(f"{object_name}_Wood")
    mat_glass = create_glass_material(f"{object_name}_Glass")
    mat_dark = create_plaster_material(f"{object_name}_Dark", (0.1, 0.1, 0.1))

    # --- Helper: Create Block ---
    created_objects = []
    
    def add_block(name, pos, dimensions, material):
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        obj = bpy.context.active_object
        obj.name = f"{object_name}_{name}"
        
        # Apply transforms based on base location and scale
        final_pos = base_loc + (Vector(pos) * scale)
        obj.location = final_pos
        obj.scale = (dimensions[0] * scale, dimensions[1] * scale, dimensions[2] * scale)
        
        if material:
            obj.data.materials.append(material)
            
        created_objects.append(obj)
        return obj

    # --- Step 1: Architectural Composition (Blocking) ---
    # Dimensions format: (X_scale, Y_scale, Z_scale) - Note: standard cube is 1x1x1
    
    # Foundation
    add_block("Base", (0, 0, 0.25), (12, 8, 0.5), mat_dark)
    add_block("Patio", (0, -4.5, 0.25), (6, 3, 0.5), mat_dark)
    
    # Main Structure Walls
    add_block("BackWall", (0, 3.5, 2.5), (10, 0.5, 4), mat_plaster)
    add_block("LeftWall", (-4.75, 0, 2.5), (0.5, 7.5, 4), mat_plaster)
    add_block("RightWall", (4.75, 0, 2.5), (0.5, 7.5, 4), mat_plaster)
    
    # Roof Cantilever
    add_block("MainRoof", (0, -1.0, 4.75), (11, 10, 0.5), mat_plaster)
    
    # Wood Accent Volumes
    add_block("WoodAccent1", (-2.5, -3.0, 2.5), (2, 0.5, 4), mat_wood)
    add_block("WoodAccent2", (3.0, -1.0, 2.5), (2.5, 4.0, 4), mat_wood)
    
    # Glass Facades (filling the gaps)
    add_block("GlassFrontMain", (0.25, -2.5, 2.5), (3.5, 0.1, 4), mat_glass)
    add_block("GlassSide", (-4.4, -1.0, 2.5), (0.1, 3.0, 4), mat_glass)

    # Entry Stairs
    add_block("Stair1", (0, -6.5, 0.08), (2, 1.0, 0.16), mat_plaster)
    add_block("Stair2", (0, -6.0, 0.25), (2, 1.0, 0.16), mat_plaster)

    # --- Step 2: Architectural Spot Lighting ---
    light_positions = [
        ("Spot_WoodAccent", (-2.5, -2.6, 4.4), mat_wood),
        ("Spot_Entry", (0.5, -2.2, 4.4), mat_glass),
        ("Spot_SideWall", (4.5, -3.5, 4.4), mat_plaster)
    ]

    for l_name, l_pos, target in light_positions:
        light_data = bpy.data.lights.new(name=f"{object_name}_{l_name}_Data", type='SPOT')
        light_data.energy = 500.0 * (scale * scale) # Scale intensity with object size
        light_data.color = (1.0, 0.85, 0.6) # Warm incandescent
        light_data.spot_size = math.radians(60)
        light_data.spot_blend = 0.8
        
        light_obj = bpy.data.objects.new(name=f"{object_name}_{l_name}", object_data=light_data)
        scene.collection.objects.link(light_obj)
        
        # Position and point down
        light_obj.location = base_loc + (Vector(l_pos) * scale)
        light_obj.rotation_euler = (0, math.radians(-15), 0) # slight angle
        created_objects.append(light_obj)

    # --- Step 3: Organization ---
    # Create an empty as a parent for easy moving
    parent_empty = bpy.data.objects.new(f"{object_name}_Root", None)
    parent_empty.location = base_loc
    scene.collection.objects.link(parent_empty)
    
    for obj in created_objects:
        obj.parent = parent_empty

    # Adjust world background slightly to make the lights pop
    if scene.world and scene.world.use_nodes:
        bg_node = scene.world.node_tree.nodes.get("Background")
        if bg_node:
            bg_node.inputs[0].default_value = (0.02, 0.03, 0.05, 1.0) # Dark twilight blue
            bg_node.inputs[1].default_value = 0.5

    return f"Created modular architecture '{object_name}' with {len(created_objects)} elements at {location}."
