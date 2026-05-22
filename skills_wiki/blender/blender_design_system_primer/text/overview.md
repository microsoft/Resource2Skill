# Blender Hero-Shot Primer

Foundational reference for building polished hero shots with the bpy-headless MCP runtime. Use this primer to pick the right shell (or skip it), choose a lighting rig, apply materials with discipline, and avoid the common shell-fit footguns that produce dark/washed-out renders.

## Available Catalog

### Scene shells (5)

| Shell | Produces | Fits ONLY when brief mentions |
|---|---|---|
| `cyberpunk_corridor` | sci-fi hallway with neon strips, crates, pipes | corridor / hallway / tunnel / metro |
| `forest_landscape` | stylized low-poly forest, golden hour, trees | forest / outdoor nature / woods |
| `product_hero_shot` | infinity backdrop + 3-point lighting + ONE central object | clean product on plain backdrop (sphere/cube/torus hero) |
| `interior_living_room` | modern living room (sofa/table/rug/lamp) + overcast daylight | living room / loft / architectural interior |
| `sci_fi_exterior` | hexagonal landing pad with arches + dramatic rim | hex landing pad with arches scene |

**Hot footguns:**
- **Don't use `product_hero_shot`** for portraits, busts, jewelry, vehicles, sculpture, or abstract scenes — its studio backdrop + 3-point lighting will fight your custom geometry and produce a near-black or washed-out render.
- **Don't use `sci_fi_exterior`** for moon outposts, alien terrain, supercars, or cityscapes — the hex pad geometry will intrude on the frame.

If the brief doesn't map cleanly to one of these five, **skip the shell entirely** and start from `execute_blender_code` to build geometry. Then layer `apply_lighting_rig` and `apply_material_preset` for polish.

Shell kwargs:
```
cyberpunk_corridor:    neon_color (magenta/cyan/amber/lime), length, width, height, with_props
forest_landscape:      tree_count, ground_size, seed
product_hero_shot:     product_shape (sphere/cube/torus), product_material (any preset name),
                        product_color (RGBA list), backdrop_color
interior_living_room:  (no kwargs)
sci_fi_exterior:       neon_color
```

### Lighting rigs (5)

| Rig | Mood | Use for |
|---|---|---|
| `studio_3point` | Neutral, balanced | Product hero on backdrop |
| `golden_hour` | Warm low sun + cool sky bounce | Exteriors, nature, outdoor |
| `neon_corridor` | Magenta/cyan rim + cool overhead | Cyberpunk, tech-moody |
| `overcast_overhead` | Soft daylight | Architectural, interior daylight |
| `dramatic_rim` | High-contrast moody rim | Sculptural, abstract, cinematic |

### Material presets (9)

`metal_brushed` · `glass_frosted` · `water_ocean` · `foliage_green` · `fabric_velvet` · `ceramic_glossy` · `plastic_matte` · `concrete_raw` · `neon_emissive` (with `alt_colors` for magenta/cyan/amber/lime).

## Decision Flow

### Step 1: Geometry — shell or custom?

If the brief maps to one of the 5 shell themes (per the table above), call `build_scene_from_shell(shell_id=...)`. Otherwise:
```
execute_blender_code("""
import bpy
# delete the default cube + any leftover defaults
for o in list(bpy.data.objects):
    if o.name in ('Cube', 'Light') and o.type != 'CAMERA':
        bpy.data.objects.remove(o, do_unlink=True)
# build your geometry from scratch ...
""")
```

### Step 2: Lighting — wipe + replace

After geometry is in place (whether from a shell or custom), wipe leftover lights and apply ONE rig:
```
execute_blender_code("""
import bpy
for o in list(bpy.data.objects):
    if o.type == 'LIGHT':
        bpy.data.objects.remove(o, do_unlink=True)
""")
apply_lighting_rig(rig_name=<one of the 5>)
```

Rig choice rule of thumb:
- product / single hero on backdrop → `studio_3point`
- exterior / nature / outdoor → `golden_hour`
- cyberpunk / neon / tech moody → `neon_corridor` or `dramatic_rim`
- architectural / interior daylight → `overcast_overhead`
- sculptural / abstract / cinematic → `dramatic_rim`

### Step 3: Materials — every named hero object gets one

Default `Material` (gray plastic) kills realism. Re-skin every visible hero object:
```
apply_material_preset(preset_name="ceramic_glossy", object_name="Product")
apply_material_preset(preset_name="metal_brushed", object_name="Frame")
apply_material_preset(preset_name="glass_frosted", object_name="Cover")
```

Common combos that score well:
- studio product: `ceramic_glossy` + `metal_brushed` + `fabric_velvet` (backdrop)
- cyberpunk: `metal_brushed` + `neon_emissive` (with `alt_colors`) + `concrete_raw`
- exterior/nature: `foliage_green` + `concrete_raw` + `water_ocean`
- abstract/sculptural: pick 2-3 contrasting (`glass_frosted` + `metal_brushed` + `plastic_matte`)
- jewelry/macro: `metal_brushed` (gold-tinted via `alt_colors`) + `glass_frosted` + `fabric_velvet`
- portraits/busts: `ceramic_glossy` (porcelain skin) + `metal_brushed` (chrome plates) + `neon_emissive` (eye glow)

### Step 4: Camera — verify framing before render

```
get_viewport_screenshot(width=512, height=288)
```

Inspect the screenshot. Common failures:
- Camera pointing at empty space → reposition `bpy.data.objects['Camera'].location` and add a `track_to` constraint to your hero object
- Scene too dark / blown-out → adjust `bpy.context.scene.world.light_settings.exposure` or rig strength
- Hero geometry off-screen / clipped → reposition camera or scale geometry
- Default cube / shell leftovers intruding → delete via `bpy.ops.object.delete()`

If the viewport screenshot looks broken, FIX IT FIRST, take another screenshot, then render. A bad final render is far worse than an extra fix iteration.

### Step 5: Render

```
render_scene(output_name="my_scene", width=1920, height=1080, samples=128, engine="EEVEE")
save_scene(output_name="my_scene")
```

Render best practices:
- 1920×1080 for hero shots; 1280×720 minimum (anything smaller looks toy-like)
- 128 samples for EEVEE; 256 for Cycles when used
- Filmic + Medium-High Contrast view transform — shells set this; if you write custom code, do the same:
  ```python
  scene = bpy.context.scene
  scene.view_settings.view_transform = "Filmic"
  scene.view_settings.look = "Medium High Contrast"
  ```
- Bloom on for cyberpunk/neon scenes
- DOF for product/macro shots: `cam.data.dof.use_dof = True`, `focus_distance`, `aperture_fstop = 2.0` for shallow

## Common Pitfalls

- **Skipping the shell when it fits** — corridor/forest/product-backdrop/living-room/hex-pad briefs benefit from the shell. Just don't *force* a shell onto a non-matching brief.
- **Over-inspecting** — don't call `get_scene_info` after every change. Trust the shell's return and call once before render.
- **Distilled skills with hash suffix** — those reference snippets are mixed quality; read with `get_skill_code` first to verify.
