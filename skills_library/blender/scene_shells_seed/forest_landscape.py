"""
forest_landscape scene shell
----------------------------
Outdoor stylized forest with low-poly trees clustered on a rolling ground
plane, lit by golden_hour rig. Sky background tinted warm.

Tier: scene_shell
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _helpers import (  # noqa: E402
    apply_lighting_rig, assign_material, configure_render, load_json,
    make_principled_material, reset_scene, setup_camera,
)


def build(*, tree_count: int = 14, ground_size: float = 30.0,
          seed: int = 7, render_resolution=(1280, 720)) -> dict:
    reset_scene()
    random.seed(seed)

    foliage_mat = make_principled_material("Foliage", load_json("material_presets", "foliage_green"))
    bark_preset = load_json("material_presets", "concrete_raw").copy()
    bark_preset["principled"] = dict(bark_preset["principled"])
    bark_preset["principled"]["Base Color"] = [0.18, 0.10, 0.06, 1.0]
    bark_preset["principled"]["Roughness"] = 0.85
    bark_mat = make_principled_material("Bark", bark_preset)
    ground_preset = load_json("material_presets", "foliage_green").copy()
    ground_preset["principled"] = dict(ground_preset["principled"])
    ground_preset["principled"]["Base Color"] = [0.14, 0.22, 0.10, 1.0]
    ground_preset["principled"]["Roughness"] = 0.9
    ground_mat = make_principled_material("Ground", ground_preset)
    rock_mat = make_principled_material("Rock", load_json("material_presets", "concrete_raw"))

    # Ground (subdivided plane with light displacement)
    bpy.ops.mesh.primitive_plane_add(size=ground_size, location=(0, 0, 0))
    ground = bpy.context.active_object
    bpy.ops.object.modifier_add(type="SUBSURF")
    ground.modifiers["Subdivision"].levels = 4
    ground.modifiers["Subdivision"].render_levels = 4
    bpy.ops.object.modifier_add(type="DISPLACE")
    disp = ground.modifiers["Displace"]
    tex = bpy.data.textures.new("GroundNoise", type="DISTORTED_NOISE")
    tex.noise_scale = 4.0
    disp.texture = tex
    disp.strength = 0.6
    assign_material(ground, ground_mat)

    # Trees: cone foliage (3 stacked) + cylinder trunk
    for i in range(tree_count):
        x = random.uniform(-ground_size / 2 + 2, ground_size / 2 - 2)
        y = random.uniform(-ground_size / 2 + 2, ground_size / 2 - 2)
        if abs(x) < 2 and abs(y) < 2:  # keep camera area clear
            x += 4 if x >= 0 else -4
        scale = random.uniform(0.85, 1.4)

        # trunk
        bpy.ops.mesh.primitive_cylinder_add(radius=0.18 * scale,
                                            depth=1.5 * scale,
                                            location=(x, y, 0.75 * scale))
        trunk = bpy.context.active_object
        assign_material(trunk, bark_mat)

        # foliage cones (3 stacked, decreasing radius)
        radii = [1.3, 1.0, 0.7]
        offsets = [1.4, 2.0, 2.6]
        for r, off in zip(radii, offsets):
            bpy.ops.mesh.primitive_cone_add(radius1=r * scale, radius2=0.05,
                                            depth=1.0 * scale,
                                            location=(x, y, off * scale))
            cone = bpy.context.active_object
            cone.rotation_euler = (0, 0, random.uniform(0, 6.28))
            assign_material(cone, foliage_mat)

    # A few scattered rocks
    for _ in range(6):
        x = random.uniform(-ground_size / 2 + 1, ground_size / 2 - 1)
        y = random.uniform(-ground_size / 2 + 1, ground_size / 2 - 1)
        s = random.uniform(0.3, 0.8)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=s, location=(x, y, s * 0.4))
        rock = bpy.context.active_object
        rock.scale = (1.0, random.uniform(0.7, 1.2), random.uniform(0.4, 0.7))
        assign_material(rock, rock_mat)

    # Lighting + camera
    rig = load_json("lighting_rigs", "golden_hour")
    apply_lighting_rig(rig)

    setup_camera(location=(0, -ground_size / 2 + 4, 5),
                 target=(0, 0, 1.5), focal_length=35)

    configure_render(engine="BLENDER_EEVEE", samples=128,
                     resolution=render_resolution, bloom=True)

    return {
        "shell": "forest_landscape",
        "objects": len(bpy.data.objects),
        "trees": tree_count,
        "ground_size": ground_size,
    }
