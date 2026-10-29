# Offsets reference

| key                   | description                                   |
| --------------------- | --------------------------------------------- |
| `world_pointer`       | base of world object (rip-relative from scan) |
| `player_count`        | int32 count of entities in world              |
| `player_list`         | pointer to first entity slot                  |
| `player_distance`     | float32 distance per slot                     |
| `player_name`         | fixed UTF-8 string, 32 bytes                  |
| `player_health`       | int32 hp                                      |
| `player_team_flag`    | bool — 1 if teammate                         |
| `player_visible_flag` | bool — 1 if not occluded                     |
| `player_head_screen`  | vec2 screen pos of head bone                  |
| `player_chest_screen` | vec2 screen pos of chest bone                 |

Regenerate with `scripts/update_offsets.py`.