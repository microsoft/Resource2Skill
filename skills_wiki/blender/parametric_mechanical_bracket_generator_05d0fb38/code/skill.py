def create_object(
    scene_name: str = "Scene",
    object_name: str = "MountingBracket",
    location: tuple = (0.0, 0.0, 0.0),
    scale: float = 1.0,
    material_color: tuple = (0.2, 0.2, 0.2),
    length: float = 0.1,        # 100mm
    width: float = 0.012,       # 12mm
    thickness: float = 0.003,   # 3mm
    leg_height: float = 0.01,   # 10mm
    hole_diameter: float = 0.0056, # 5.6mm (Fits 5mm bolt)
    num_holes: int = 3,
    **kwargs,
) -> str:
    """
    Create a Parametric Mechanical Mounting Bracket in the active Blender scene.
    
    Args:
        scene_name: Name of the target scene.
        object_name: Name for the created object.
        location: (x, y, z) world-space position.
        scale: Uniform scale factor.
        material_color: (R, G, B) base color for the plastic/metal.
        length: Total length of the bracket.
        width: Total width of the bracket.
        thickness: Thickness of the structural plates.
        leg_height: Height of the L-bracket leg (0 for flat plate).
        hole_diameter: Diameter of the mounting holes.
        num_holes: Number of evenly spaced mounting holes.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import bpy
    import math
    from mathutils import Vector

    # Ensure scene exists
    scene = bpy.data.scenes.get(scene_name) or bpy.data.scenes[0]
    
    # Helper to deselect all
    def deselect_all():
        if bpy.context.object and bpy.context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

    deselect_all()

    # === Step 1: Create Base Plate ===
    bpy.ops.mesh.primitive_cube_add(size=1)
    plate = bpy.context.active_object
    plate.name = object_name
    plate.scale = (length, width, thickness)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # === Step 2: Create & Boolean Union Leg ===
    if leg_height > 0:
        deselect_all()
        bpy.ops.mesh.primitive_cube_add(size=1)
        leg = bpy.context.active_object
        leg.name = f"{object_name}_Leg"
        leg.scale = (thickness, width, leg_height)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Position leg at the extreme end of the plate
        leg.location = (length/2 - thickness/2, 0, thickness/2 + leg_height/2)
        
        # Boolean Union
        bool_union = plate.modifiers.new(name="Union", type='BOOLEAN')
        bool_union.operation = 'UNION'
        bool_union.object = leg
        bool_union.solver = 'EXACT'
        
        bpy.context.view_layer.objects.active = plate
        bpy.ops.object.modifier_apply(modifier="Union")
        
        # Cleanup temporary leg object
        deselect_all()
        leg.select_set(True)
        bpy.ops.object.delete()

    # === Step 3: Create & Boolean Difference Holes ===
    cutters = []
    cutter_depth = thickness * 4 # Make tall enough to clearly cut through
    
    for i in range(num_holes):
        deselect_all()
        bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=hole_diameter/2, depth=cutter_depth)
        cutter = bpy.context.active_object
        cutter.name = f"{object_name}_HoleCutter_{i}"
        
        if num_holes == 1:
            x_pos = 0
        else:
            # Distribute holes avoiding the edges and the L-leg
            margin = thickness * 3
            start_x = -length/2 + margin
            end_x = length/2 - margin - (thickness if leg_height > 0 else 0)
            fraction = i / (num_holes - 1)
            x_pos = start_x + fraction * (end_x - start_x)
            
        cutter.location = (x_pos, 0, 0)
        cutters.append(cutter)

    if cutters:
        deselect_all()
        for c in cutters:
            c.select_set(True)
        bpy.context.view_layer.objects.active = cutters[0]
        
        if len(cutters) > 1:
            bpy.ops.object.join()
            
        main_cutter = bpy.context.active_object
        
        # Boolean Difference
        bool_diff = plate.modifiers.new(name="Holes", type='BOOLEAN')
        bool_diff.operation = 'DIFFERENCE'
        bool_diff.object = main_cutter
        bool_diff.solver = 'EXACT'
        
        bpy.context.view_layer.objects.active = plate
        bpy.ops.object.modifier_apply(modifier="Holes")
        
        # Cleanup temporary cutter object
        deselect_all()
        main_cutter.select_set(True)
        bpy.ops.object.delete()

    # === Step 4: Mesh Topology Cleanup ===
    deselect_all()
    plate.select_set(True)
    bpy.context.view_layer.objects.active = plate
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=0.0001)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.ops.object.shade_flat() # Mechanical parts look better flat shaded unless highly beveled

    # === Step 5: Bevel for Realism ===
    bevel = plate.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.0005 # 0.5mm bevel
    bevel.segments = 3
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(45)

    # === Step 6: Material & Shading ===
    mat = bpy.data.materials.new(name=f"{object_name}_ManufacturedMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*material_color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.4
        
        # Micro-texture noise to emulate manufacturing lines/grain
        noise = nodes.new('ShaderNodeTexNoise')
        noise.inputs['Scale'].default_value = 1000.0
        
        bump = nodes.new('ShaderNodeBump')
        bump.inputs['Distance'].default_value = 0.001
        bump.inputs['Strength'].default_value = 0.15
        
        links.new(noise.outputs['Fac'], bump.inputs['Height'])
        links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
        
    plate.data.materials.append(mat)

    # === Step 7: Final Placement & Scale ===
    # Set the pivot so Z location represents the bottom of the bracket
    plate.location = Vector(location) + Vector((0, 0, (thickness / 2) * scale))
    plate.scale = (scale, scale, scale)

    return f"Created '{object_name}' (L:{length}m, W:{width}m) at {location} with {num_holes} holes"
