"""
cyberpunk_corridor scene shell
------------------------------
Long sci-fi corridor with neon strip lighting on side walls, tiled floor,
fog/atmosphere, and props (crates, panels). Camera placed at near end
looking down the corridor.

Tier: scene_shell
"""
from __future__ import annotations

import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _helpers import (  # noqa: E402
    apply_lighting_rig, assign_material, configure_render, load_json,
    make_principled_material, reset_scene, setup_camera,
)


def build(*, length: float = 18.0, width: float = 4.5, height: float = 3.5,
          neon_color: str = "magenta", with_props: bool = True,
          render_resolution=(1280, 720)) -> dict:
    reset_scene()

    floor_mat   = make_principled_material("CorridorFloor",   load_json("material_presets", "concrete_raw"))
    wall_mat    = make_principled_material("CorridorWall",    load_json("material_presets", "metal_brushed"))
    ceiling_mat = make_principled_material("CorridorCeiling", load_json("material_presets", "concrete_raw"))
    neon_preset = load_json("material_presets", "neon_emissive").copy()
    color = neon_preset["alt_colors"].get(neon_color, neon_preset["principled"]["Emission Color"])
    neon_preset["principled"]["Emission Color"] = color
    neon_mat = make_principled_material("CorridorNeon", neon_preset)
    crate_mat = make_principled_material("Crate", load_json("material_presets", "plastic_matte"))

    # Floor
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, length / 2, 0))
    floor = bpy.context.active_object
    floor.scale = (width, length, 1)
    bpy.ops.object.transform_apply(scale=True)
    assign_material(floor, floor_mat)

    # Ceiling
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, length / 2, height))
    ceil = bpy.context.active_object
    ceil.scale = (width, length, 1)
    ceil.rotation_euler = (3.14159, 0, 0)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    assign_material(ceil, ceiling_mat)

    # Side walls
    for sign, name in [(-1, "WallL"), (1, "WallR")]:
        bpy.ops.mesh.primitive_plane_add(size=1, location=(sign * width / 2,
                                                           length / 2, height / 2))
        wall = bpy.context.active_object
        wall.scale = (1, length, height)
        wall.rotation_euler = (0, sign * 1.5708, 0)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        assign_material(wall, wall_mat)

    # Neon strips along side walls (segmented)
    seg_count = 6
    seg_len = length / (seg_count + 0.5)
    for sign in (-1, 1):
        for i in range(seg_count):
            y = (i + 0.5) * (length / seg_count)
            bpy.ops.mesh.primitive_cube_add(
                size=1, location=(sign * (width / 2 - 0.05), y, height - 0.4))
            strip = bpy.context.active_object
            strip.scale = (0.06, seg_len * 0.42, 0.08)
            bpy.ops.object.transform_apply(scale=True)
            assign_material(strip, neon_mat)

    # Floor accent line down the middle
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, length / 2, 0.02))
    line = bpy.context.active_object
    line.scale = (0.12, length * 0.96, 0.005)
    bpy.ops.object.transform_apply(scale=True)
    assign_material(line, neon_mat)

    # Props (crates near end)
    if with_props:
        crate_positions = [(-1.4, length * 0.65, 0.4),
                           (-1.4, length * 0.65, 1.0),
                           (1.5, length * 0.7, 0.45),
                           (1.5, length * 0.55, 0.45)]
        for pos in crate_positions:
            bpy.ops.mesh.primitive_cube_add(size=0.8, location=pos)
            c = bpy.context.active_object
            assign_material(c, crate_mat)

        # End door (taller plane, dark with neon outline)
        bpy.ops.mesh.primitive_cube_add(size=1,
                                        location=(0, length - 0.05, height / 2))
        door = bpy.context.active_object
        door.scale = (1.6, 0.05, height * 0.85)
        bpy.ops.object.transform_apply(scale=True)
        assign_material(door, wall_mat)

    # Lighting + camera
    rig = load_json("lighting_rigs", "neon_corridor")
    apply_lighting_rig(rig)

    setup_camera(location=(0, -1.5, 1.6), target=(0, length, 1.6),
                 focal_length=35)

    configure_render(engine="BLENDER_EEVEE", samples=128,
                     resolution=render_resolution, bloom=True)

    return {
        "shell": "cyberpunk_corridor",
        "objects": len(bpy.data.objects),
        "lights": len([o for o in bpy.data.objects if o.type == "LIGHT"]),
        "neon_color": neon_color,
        "dimensions": [width, length, height],
    }
