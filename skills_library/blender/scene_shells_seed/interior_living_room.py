"""
interior_living_room scene shell
--------------------------------
Modern minimalist living room: floor, two walls, sofa, coffee table, rug,
floor lamp, large window letting overcast light in.

Tier: scene_shell
"""
from __future__ import annotations

import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _helpers import (  # noqa: E402
    apply_lighting_rig, assign_material, configure_render, load_json,
    make_principled_material, reset_scene, setup_camera,
)


def build(*, room_size: float = 7.0, render_resolution=(1280, 720)) -> dict:
    reset_scene()

    floor_preset = load_json("material_presets", "plastic_matte").copy()
    floor_preset["principled"] = dict(floor_preset["principled"])
    floor_preset["principled"]["Base Color"] = [0.55, 0.42, 0.30, 1.0]
    floor_preset["principled"]["Roughness"] = 0.7
    floor_mat = make_principled_material("Floor", floor_preset)

    wall_preset = load_json("material_presets", "plastic_matte").copy()
    wall_preset["principled"] = dict(wall_preset["principled"])
    wall_preset["principled"]["Base Color"] = [0.92, 0.90, 0.86, 1.0]
    wall_mat = make_principled_material("Wall", wall_preset)

    sofa_mat = make_principled_material("Sofa", load_json("material_presets", "fabric_velvet"))
    table_preset = load_json("material_presets", "concrete_raw").copy()
    table_preset["principled"] = dict(table_preset["principled"])
    table_preset["principled"]["Base Color"] = [0.18, 0.12, 0.08, 1.0]
    table_mat = make_principled_material("Table", table_preset)
    rug_preset = load_json("material_presets", "fabric_velvet").copy()
    rug_preset["principled"] = dict(rug_preset["principled"])
    rug_preset["principled"]["Base Color"] = [0.78, 0.65, 0.42, 1.0]
    rug_preset["principled"]["Sheen Tint"] = [0.95, 0.85, 0.7, 1.0]
    rug_mat = make_principled_material("Rug", rug_preset)
    lamp_mat = make_principled_material("LampPost", load_json("material_presets", "metal_brushed"))
    shade_preset = load_json("material_presets", "neon_emissive").copy()
    shade_preset["principled"] = dict(shade_preset["principled"])
    shade_preset["principled"]["Emission Color"] = [1.0, 0.85, 0.55, 1.0]
    shade_preset["principled"]["Emission Strength"] = 4.0
    shade_mat = make_principled_material("LampShade", shade_preset)

    # Floor
    bpy.ops.mesh.primitive_plane_add(size=room_size, location=(0, 0, 0))
    assign_material(bpy.context.active_object, floor_mat)

    # Back wall + side wall
    bpy.ops.mesh.primitive_plane_add(size=room_size,
                                     location=(0, room_size / 2, room_size * 0.45))
    back = bpy.context.active_object
    back.rotation_euler = (1.5708, 0, 0)
    bpy.ops.object.transform_apply(rotation=True)
    assign_material(back, wall_mat)

    bpy.ops.mesh.primitive_plane_add(size=room_size,
                                     location=(-room_size / 2, 0, room_size * 0.45))
    side = bpy.context.active_object
    side.rotation_euler = (0, 1.5708, 0)
    bpy.ops.object.transform_apply(rotation=True)
    assign_material(side, wall_mat)

    # Window cutout: emissive panel on back wall
    win_preset = load_json("material_presets", "neon_emissive").copy()
    win_preset["principled"] = dict(win_preset["principled"])
    win_preset["principled"]["Emission Color"] = [0.85, 0.92, 1.0, 1.0]
    win_preset["principled"]["Emission Strength"] = 6.0
    win_mat = make_principled_material("Window", win_preset)
    bpy.ops.mesh.primitive_plane_add(size=2.4,
                                     location=(1.5, room_size / 2 - 0.04, 1.8))
    win = bpy.context.active_object
    win.scale = (1.2, 1.0, 0.85)
    bpy.ops.object.transform_apply(scale=True)
    win.rotation_euler = (1.5708, 0, 0)
    bpy.ops.object.transform_apply(rotation=True)
    assign_material(win, win_mat)

    # Sofa: long cushion + back + arms
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.0, -1.2, 0.45))
    cushion = bpy.context.active_object
    cushion.scale = (2.4, 0.95, 0.45)
    bpy.ops.object.transform_apply(scale=True)
    assign_material(cushion, sofa_mat)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.0, -1.6, 1.0))
    back_rest = bpy.context.active_object
    back_rest.scale = (2.4, 0.18, 0.6)
    bpy.ops.object.transform_apply(scale=True)
    assign_material(back_rest, sofa_mat)

    for x in (-1.25, 1.25):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, -1.2, 0.7))
        arm = bpy.context.active_object
        arm.scale = (0.16, 0.95, 0.55)
        bpy.ops.object.transform_apply(scale=True)
        assign_material(arm, sofa_mat)

    # Coffee table
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.2, 0.32))
    table = bpy.context.active_object
    table.scale = (1.4, 0.7, 0.05)
    bpy.ops.object.transform_apply(scale=True)
    assign_material(table, table_mat)

    for tx, ty in [(-0.6, -0.25), (0.6, -0.25), (-0.6, 0.65), (0.6, 0.65)]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(tx, ty, 0.16))
        leg = bpy.context.active_object
        leg.scale = (0.05, 0.05, 0.32)
        bpy.ops.object.transform_apply(scale=True)
        assign_material(leg, table_mat)

    # Rug
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -0.4, 0.005))
    rug = bpy.context.active_object
    rug.scale = (3.0, 2.4, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    assign_material(rug, rug_mat)

    # Floor lamp (post + emissive shade)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=1.8,
                                        location=(-1.9, -1.5, 0.9))
    post = bpy.context.active_object
    assign_material(post, lamp_mat)

    bpy.ops.mesh.primitive_cone_add(radius1=0.4, radius2=0.18, depth=0.45,
                                    location=(-1.9, -1.5, 1.95))
    shade = bpy.context.active_object
    assign_material(shade, shade_mat)

    rig = load_json("lighting_rigs", "overcast_overhead")
    apply_lighting_rig(rig)

    setup_camera(location=(3.8, -3.4, 1.7), target=(0, -0.5, 0.7),
                 focal_length=35)

    configure_render(engine="BLENDER_EEVEE", samples=128,
                     resolution=render_resolution, bloom=True)

    return {
        "shell": "interior_living_room",
        "objects": len(bpy.data.objects),
        "room_size": room_size,
    }
