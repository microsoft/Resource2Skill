# dramatic_rim

## Description

High-contrast moody — strong rim from behind, deep shadows on subject front. Cinematic portraits, hero villains.

## Parameters

```json
{
  "best_for": [
    "cinematic portraits",
    "hero villains",
    "dramatic close-ups",
    "noir scenes"
  ],
  "lights": [
    {
      "color": [
        1.0,
        0.92,
        0.85,
        1.0
      ],
      "energy": 1500,
      "location": [
        -2.5,
        5.5,
        4.5
      ],
      "name": "Rim",
      "rotation_euler_deg": [
        -65,
        0,
        -160
      ],
      "spot_blend": 0.6,
      "spot_size_deg": 35,
      "type": "SPOT"
    },
    {
      "color": [
        0.85,
        0.92,
        1.0,
        1.0
      ],
      "energy": 120,
      "location": [
        4.0,
        2.0,
        1.5
      ],
      "name": "Kicker",
      "rotation_euler_deg": [
        80,
        0,
        110
      ],
      "size": 1.0,
      "type": "AREA"
    },
    {
      "color": [
        0.55,
        0.6,
        0.78,
        1.0
      ],
      "energy": 30,
      "location": [
        -3.5,
        -3.5,
        1.0
      ],
      "name": "AmbientWash",
      "rotation_euler_deg": [
        70,
        0,
        -45
      ],
      "size": 4.0,
      "type": "AREA"
    }
  ],
  "world_color": [
    0.01,
    0.01,
    0.02,
    1.0
  ],
  "world_strength": 0.02
}
```