# golden_hour

## Description

Warm low sun + cool sky bounce, long shadows. Use for outdoor landscapes, exteriors.

## Parameters

```json
{
  "best_for": [
    "outdoor landscapes",
    "exteriors",
    "sunset shots",
    "warm scenes"
  ],
  "lights": [
    {
      "angle_deg": 1.5,
      "color": [
        1.0,
        0.78,
        0.42,
        1.0
      ],
      "energy": 5.5,
      "location": [
        10,
        -8,
        6
      ],
      "name": "Sun",
      "rotation_euler_deg": [
        70,
        0,
        30
      ],
      "type": "SUN"
    },
    {
      "color": [
        0.55,
        0.7,
        1.0,
        1.0
      ],
      "energy": 80,
      "location": [
        0,
        0,
        12
      ],
      "name": "SkyFill",
      "rotation_euler_deg": [
        180,
        0,
        0
      ],
      "size": 20,
      "type": "AREA"
    }
  ],
  "world_color": [
    0.98,
    0.78,
    0.55,
    1.0
  ],
  "world_strength": 0.7
}
```