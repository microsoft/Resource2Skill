"""
sci_fi_exterior scene shell
---------------------------
Outdoor sci-fi platform: hexagonal landing pad on raised plinth, two angular
arches with neon trim, distant terrain backdrop, dramatic rim lighting.

Tier: scene_shell
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _helpers import (  # noqa: E402
    apply_lighting_rig, assign_material, configure_render, load_json,
    make_principled_material, reset_scene, setup_camera,
)


def build(*, neon_color: str = "cyan", render_resolution=(1280, 720)) -> dict:
    reset_scene()

    pad_mat = make_principled_material("Pad", load_json("material_presets", "metal_brushed"))
    plinth_mat = make_principled_material("Plinth", load_json("material_presets", "concrete_raw"))
    arch_mat = make_principled_material("Arch", load_json("material_presets", "metal_brushed"))
    neon_preset = load_json("material_presets", "neon_emissive").copy()
    neon_preset["principled"] = dict(neon_preset["principled"])
    neon_preset["principled"]["Emission Color"] = neon_preset["alt_colors"].get(
        neon_color, neon_preset["principled"]["Emission Color"])
    neon_mat = make_principled_material("Neon", neon_preset)
    terrain_preset = load_json("material_presets", "concrete_raw").copy()
    terrain_preset["principled"] = dict(terrain_preset["principled"])
    terrain_preset["principled"]["Base Color"] = [0.20, 0.18, 0.22, 1.0]
    terrain_mat = make_principled_material("Terrain", terrain_preset)

    # Distant terrain: large displaced plane
    bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 18, -1.0))
    terrain = bpy.context.active_object
    bpy.ops.object.modifier_add(type="SUBSURF")
    terrain.modifiers["Subdivision"].levels = 4
    bpy.ops.object.modifier_add(type="DISPLACE")
    disp = terrain.modifiers["Displace"]
    tex = bpy.data.textures.new("TerrainNoise", type="DISTORTED_NOISE")
    tex.noise_scale = 12.0
    disp.texture = tex
    disp.strength = 4.0
    assign_material(terrain, terrain_mat)

    # Plinth (hexagonal-ish: cylinder w/ 6 sides)
    bpy.ops.mesh.primitive_cylinder_add(radius=4.5, depth=0.8, vertices=6,
                                        location=(0, 0, 0.0))
    plinth = bpy.context.active_object
    assign_material(plinth, plinth_mat)

    # Pad on top
    bpy.ops.mesh.primitive_cylinder_add(radius=4.0, depth=0.18, vertices=6,
                                        location=(0, 0, 0.5))
    pad = bpy.context.active_object
    assign_material(pad, pad_mat)

    # Inner pad neon glow ring
    bpy.ops.mesh.primitive_torus_add(major_radius=3.4, minor_radius=0.06,
                                     location=(0, 0, 0.6))
    ring = bpy.context.active_object
    assign_material(ring, neon_mat)

    # Hex pattern accents on pad
    for i in range(6):
        ang = i * (math.pi / 3)
        x = 2.6 * math.cos(ang)
        y = 2.6 * math.sin(ang)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.35, depth=0.05,
                                            vertices=6, location=(x, y, 0.61))
        h = bpy.context.active_object
        assign_material(h, neon_mat)

    # Two angular arches flanking the pad
    for sign in (-1, 1):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(sign * 4.3, 0, 2.5))
        arch = bpy.context.active_object
        arch.scale = (0.4, 0.6, 5.0)
        bpy.ops.object.transform_apply(scale=True)
        arch.rotation_euler = (0, sign * math.radians(15), 0)
        assign_material(arch, arch_mat)

        # Top crossbar
        bpy.ops.mesh.primitive_cube_add(size=1,
                                        location=(sign * 3.6, 0, 5.0))
        cross = bpy.context.active_object
        cross.scale = (1.6, 0.5, 0.3)
        bpy.ops.object.transform_apply(scale=True)
        cross.rotation_euler = (0, sign * math.radians(15), 0)
        assign_material(cross, arch_mat)

        # Neon trim on inner side of arch
        bpy.ops.mesh.primitive_cube_add(size=1,
                                        location=(sign * 3.95, 0, 2.5))
        trim = bpy.context.active_object
        trim.scale = (0.05, 0.4, 4.6)
        bpy.ops.object.transform_apply(scale=True)
        assign_material(trim, neon_mat)

    rig = load_json("lighting_rigs", "dramatic_rim")
    apply_lighting_rig(rig)

    setup_camera(location=(7.5, -8.5, 3.5), target=(0, 0, 1.5), focal_length=42)

    configure_render(engine="BLENDER_EEVEE", samples=128,
                     resolution=render_resolution, bloom=True)

    return {
        "shell": "sci_fi_exterior",
        "objects": len(bpy.data.objects),
        "neon_color": neon_color,
    }
