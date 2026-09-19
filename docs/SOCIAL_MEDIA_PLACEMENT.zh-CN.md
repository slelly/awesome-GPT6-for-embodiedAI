# 社媒原始媒体放置说明（轻量包）

轻量交付包保留 `site/assets/social/` 中的既有小封面和其他媒体，但为降低附件体积，未收入下列 14 个用户上传的原始文件。将原始 ZIP 中的 12 个视频、单独的 Dual-ALOHA 视频和魔方图片**直接复制**到解压后的 `site/assets/social/`；不要改名、不要更改大小写，也不要把空格改成下划线。网页数据已使用 URL 编码引用这些原始文件名。

## 文件清单

| 项目 | 原始文件名 | 来源 |
| --- | --- | --- |
| X01 | `Physical Robot Keyboard Typing.mp4` | 原始社媒视频 ZIP |
| X02 | `Physical Ethernet Insertion.mp4` | 原始社媒视频 ZIP |
| X03 | `Robot Arm Draws the Golden Gate Bridge.mp4` | 原始社媒视频 ZIP |
| X04 | `Cross-Scene Mobile Manipulation ICL.mp4` | 原始社媒视频 ZIP |
| X05 | `G1 Coke-Bottle Grasp.mp4` | 原始社媒视频 ZIP |
| X06 | `G1 Navigation.mp4` | 原始社媒视频 ZIP |
| X08 | `Sharpa Dexterous-Hand Pen Spinning PPO.mp4` | 原始社媒视频 ZIP |
| X09 | `Go1 Paused-Physics Joint Control.mp4` | 原始社媒视频 ZIP |
| X10 | `CARLA Visual Waypoint Driving.mp4` | 原始社媒视频 ZIP |
| X11 | `Two-Robot Ball Toss.mp4` | 原始社媒视频 ZIP |
| X12 | `G1 Bicycle-Control Code.mp4` | 原始社媒视频 ZIP |
| X14 | `Office Scene to Newton  G1.mp4` | 原始社媒视频 ZIP；`Newton` 与 `G1` 间是两个空格 |
| X13 | `Dual-ALOHA Spatial-Constraint Demo.mp4` | 单独上传的 Dual-ALOHA 视频 |
| X07 | `SaveTwitter.Net_HST8HsrawAAkgPu.jpg` | 单独上传的魔方图片 |

## 放回后的检查

1. 上述 14 个文件应全部位于 `site/assets/social/` 的同一层，不要创建额外子目录。
2. 运行 `python3 scripts/validate.py && python3 scripts/build.py`。
3. 以静态服务器访问 `site/`。卡片内视频会按需加载；视频使用保留的小封面，图片和视频控件无需更改。

本说明不改变原帖、项目页或来源台账中的核验结论；尤其 Dual-ALOHA 的具体原帖仍待确认。
