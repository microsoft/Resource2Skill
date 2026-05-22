"""
product_hero_shot scene shell
-----------------------------
Studio-style isolated product on a turntable with infinity backdrop and
3-point lighting. The "product" is a parametric placeholder (sphere on
cylindrical base) that custom code can replace via execute_blender_code.

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


def build(*, backdrop_color: list | None = None,
          product_material: str = "ceramic_glossy",
          product_shape: str = "sphere",
          product_color: list | None = None,
          render_resolution=(1280, 720)) -> dict:
    reset_scene()

    backdrop_preset = load_json("material_presets", "plastic_matte").copy()
    backdrop_preset["principled"] = dict(backdrop_preset["principled"])
    backdrop_preset["principled"]["Base Color"] = backdrop_color or [0.85, 0.85, 0.88, 1.0]
    backdrop_preset["principled"]["Roughness"] = 0.95
    backdrop_mat = make_principled_material("Backdrop", backdrop_preset)

    product_preset = load_json("material_presets", product_material).copy()
    if product_color:
        product_preset["principled"] = dict(product_preset["principled"])
        product_preset["principled"]["Base Color"] = product_color
    product_mat = make_principled_material("Product", product_preset)

    base_preset = load_json("material_presets", "metal_brushed").copy()
    base_mat = make_principled_material("ProductBase", base_preset)

    # Infinity-curve backdrop: floor + back wall joined with a curved transition.
    # Approximated by a large floor + slightly sloped back panel.
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
    floor = bpy.context.active_object
    assign_material(floor, backdrop_mat)

    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 4, 4))
    back = bpy.context.active_object
    back.rotation_euler = (1.5708, 0, 0)
    bpy.ops.object.transform_apply(rotation=True)
    assign_material(back, backdrop_mat)

    # Smooth join: a curved cylinder section
    bpy.ops.mesh.primitive_cylinder_add(radius=2.0, depth=10, location=(0, 2, 2))
    curve = bpy.context.active_object
    curve.rotation_euler = (0, 1.5708, 0)
    bpy.ops.object.transform_apply(rotation=True)
    curve.scale = (1.0, 0.5, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    assign_material(curve, backdrop_mat)

    # Product base (low cylinder)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=0.08, location=(0, 0, 0.04))
    base = bpy.context.active_object
    assign_material(base, base_mat)

    # Product hero
    z_top = 0.08
    if product_shape == "sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.35, location=(0, 0, z_top + 0.35))
        bpy.ops.object.shade_smooth()
    elif product_shape == "cube":
        bpy.ops.mesh.primitive_cube_add(size=0.7, location=(0, 0, z_top + 0.35))
    elif product_shape == "torus":
        bpy.ops.mesh.primitive_torus_add(major_radius=0.32, minor_radius=0.10,
                                         location=(0, 0, z_top + 0.20))
        bpy.ops.object.shade_smooth()
    else:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.35, location=(0, 0, z_top + 0.35))
        bpy.ops.object.shade_smooth()
    product = bpy.context.active_object
    product.name = "Product"
    assign_material(product, product_mat)

    # Lighting + camera
    rig = load_json("lighting_rigs", "studio_3point")
    apply_lighting_rig(rig)

    setup_camera(location=(2.5, -3.0, 1.2), target=(0, 0, 0.45),
                 focal_length=70)

    configure_render(engine="BLENDER_EEVEE", samples=128,
                     resolution=render_resolution, bloom=True)

    return {
        "shell": "product_hero_shot",
        "objects": len(bpy.data.objects),
        "product_shape": product_shape,
        "product_material": product_material,
    }
