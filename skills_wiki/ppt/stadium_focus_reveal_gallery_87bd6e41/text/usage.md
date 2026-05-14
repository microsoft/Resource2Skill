# Usage

## Signature

`create_slide(output_pptx_path, title_text, active_index, accent_color)`

## Parameters

- `output_pptx_path`: `str`
- `title_text`: `str` = `'Meet our Team'`
- `active_index`: `int` = `1`
- `accent_color`: `tuple` = `(236, 64, 122)`

## Example call

```python
from skill import create_slide
create_slide(
    output_pptx_path='out.pptx',
)
```

---

# Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Stadium mask & photo composite | `PIL/Pillow` | PowerPoint cannot dynamically auto-crop images to custom stadium masks combined with solid color bases cleanly via python-pptx alone. PIL ensures pixel-perfect asset generation. |
| Grayscale filtering | `PIL/Pillow` | Python-pptx lacks native API calls to apply grayscale picture recolor matrices programmatically. |
| Bottom fade gradient | `PIL/Pillow` | Native python-pptx shapes do not support gradient transparency (alpha fading). Generating a PNG alpha gradient mask is the only reliable way to achieve the cinematic bottom fade. |
| Layout & Typography | `python-pptx` | Best for exact placement of text boxes, font styling, and slide assembly. |

> **Feasibility Assessment**: 100% of the single-slide visual state is reproduced. (Note: To achieve the continuous animation seen in the video, a user would run this script multiple times with different `active_index` values and apply the Morph transition between them in PowerPoint).

#### 3b. Complete Reproduction Code

_(code moved to [`../code/skill.py`](../code/skill.py))_
