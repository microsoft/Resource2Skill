# neon_corridor

## Description

Cyberpunk corridor lighting — magenta + cyan rim accents + low-key ambient + practical strip lights

## Parameters

```json
{
  "best_for": [
    "cyberpunk",
    "sci-fi corridors",
    "futuristic interiors",
    "neon scenes"
  ],
  "lights": [
    {
      "color": [
        0.95,
        0.18,
        0.62,
        1.0
      ],
      "energy": 350,
      "location": [
        -3.0,
        1.5,
        2.5
      ],
      "name": "MagentaRim",
      "rotation_euler_deg": [
        85,
        0,
        -55
      ],
      "size": 1.5,
      "type": "AREA"
    },
    {
      "color": [
        0.18,
        0.85,
        0.95,
        1.0
      ],
      "energy": 350,
      "location": [
        3.0,
        1.5,
        2.5
      ],
      "name": "CyanRim",
      "rotation_euler_deg": [
        85,
        0,
        55
      ],
      "size": 1.5,
      "type": "AREA"
    },
    {
      "color": [
        0.65,
        0.78,
        1.0,
        1.0
      ],
      "energy": 90,
      "location": [
        0,
        0,
        4.5
      ],
      "name": "OverheadCool",
      "rotation_euler_deg": [
        180,
        0,
        0
      ],
      "size": 2.0,
      "type": "AREA"
    },
    {
      "color": [
        0.98,
        0.65,
        0.12,
        1.0
      ],
      "energy": 250,
      "location": [
        0,
        6,
        2.5
      ],
      "name": "PracticalStrip",
      "rotation_euler_deg": [
        -90,
        0,
        0
      ],
      "size": 1.0,
      "type": "AREA"
    }
  ],
  "world_color": [
    0.02,
    0.02,
    0.04,
    1.0
  ],
  "world_strength": 0.05
}
```