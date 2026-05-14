"""
_helpers.py — shared utilities for blender scene shells.

Each shell module imports these to apply material presets, lighting rigs,
and camera placement consistently.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import bpy
from mathutils import Euler, Vector

_PRESET_CACHE: dict[str, dict] = {}


def _skills_root() -> Path:
    return Path(__file__).resolve().parent


def load_json(kind: str, name: str) -> dict:
    key = f"{kind}/{name}"
    if key in _PRESET_CACHE:
        return _PRESET_CACHE[key]
    p = _skills_root() / kind / f"{name}.json"
    if not p.exists():
        raise FileNotFoundError(f"{kind}/{name}.json not found")
    data = json.loads(p.read_text(encoding="utf-8"))
    _PRESET_CACHE[key] = data
    return data


def reset_scene() -> None:
    """Wipe all mesh / light / camera objects + orphan data."""
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for col in (bpy.data.meshes, bpy.data.materials, bpy.data.lights,
                bpy.data.cameras, bpy.data.worlds):
        for item in list(col):
            if item.users == 0:
                col.remove(item)


def make_principled_material(name: str, preset: dict) -> bpy.types.Material:
    """Create a material whose Principled BSDF inputs are set from preset['principled']."""
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf is None:
        bsdf = nodes.new("ShaderNodeBsdfPrincipled")
        out = nodes.get("Material Output") or nodes.new("ShaderNodeOutputMaterial")
        mat.node_tree.links.new(bsdf.outputs[0], out.inputs[0])
    inputs = bsdf.inputs
    for key, value in preset.get("principled", {}).items():
        if key in inputs:
            try:
                if isinstance(value, list):
                    inputs[key].default_value = value
                else:
                    inputs[key].default_value = value
            except Exception:
                pass
    return mat


def assign_material(obj: bpy.types.Object, mat: bpy.types.Material) -> None:
    if obj.data is None or not hasattr(obj.data, "materials"):
        return
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)


def apply_lighting_rig(rig: dict) -> list[bpy.types.Object]:
    """Add lights from a rig spec, set world strength/color. Returns light objects."""
    world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background") or world.node_tree.nodes.new("ShaderNodeBackground")
    bg.inputs["Strength"].default_value = float(rig.get("world_strength", 0.5))
    bg.inputs["Color"].default_value = list(rig.get("world_color", [0.05, 0.05, 0.05, 1.0]))

    created: list[bpy.types.Object] = []
    for spec in rig.get("lights", []):
        light_type = spec.get("type", "AREA").upper()
        light_data = bpy.data.lights.new(name=spec["name"], type=light_type)
        light_data.energy = float(spec.get("energy", 100))
        if "color" in spec:
            light_data.color = spec["color"][:3]
        if light_type == "AREA" and "size" in spec:
            light_data.size = float(spec["size"])
        if light_type == "SPOT":
            if "spot_size_deg" in spec:
                light_data.spot_size = math.radians(spec["spot_size_deg"])
            if "spot_blend" in spec:
                light_data.spot_blend = float(spec["spot_blend"])
        if light_type == "SUN" and "angle_deg" in spec:
            light_data.angle = math.radians(spec["angle_deg"])

        obj = bpy.data.objects.new(spec["name"], light_data)
        bpy.context.collection.objects.link(obj)
        obj.location = Vector(spec.get("location", [0, 0, 0]))
        rot_deg = spec.get("rotation_euler_deg", [0, 0, 0])
        obj.rotation_euler = Euler([math.radians(a) for a in rot_deg], "XYZ")
        created.append(obj)
    return created


def setup_camera(location, target=(0, 0, 1), focal_length: float = 35.0,
                 name: str = "Camera") -> bpy.types.Object:
    cam_data = bpy.data.cameras.new(name)
    cam_data.lens = float(focal_length)
    cam = bpy.data.objects.new(name, cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = Vector(location)
    direction = Vector(target) - cam.location
    rot_quat = direction.to_track_quat("-Z", "Y")
    cam.rotation_euler = rot_quat.to_euler()
    bpy.context.scene.camera = cam
    return cam


def configure_render(engine: str = "BLENDER_EEVEE", samples: int = 64,
                     resolution=(1280, 720), bloom: bool = True) -> None:
    scene = bpy.context.scene
    scene.render.engine = engine
    scene.render.resolution_x, scene.render.resolution_y = resolution
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    if engine == "CYCLES":
        scene.cycles.samples = samples
        scene.cycles.use_denoising = True
    elif engine in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
        try:
            scene.eevee.taa_render_samples = samples
            if hasattr(scene.eevee, "use_bloom"):
                scene.eevee.use_bloom = bloom
            if hasattr(scene.eevee, "use_ssr"):
                scene.eevee.use_ssr = True
            if hasattr(scene.eevee, "use_gtao"):
                scene.eevee.use_gtao = True
        except Exception:
            pass

    # View transform — Filmic gives much better tonal response than Standard
    try:
        scene.view_settings.view_transform = "Filmic"
        scene.view_settings.look = "Medium High Contrast"
        scene.view_settings.exposure = 0.0
    except Exception:
        pass
