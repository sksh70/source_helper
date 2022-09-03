## Info

An addon for [Blender 2.79](https://download.blender.org/release/Blender2.79/) to get the `<helper>` & `<trigger>` for Source's [$proceduralbones](https://developer.valvesoftware.com/wiki/$proceduralbones). Modified from [SourceOps](https://github.com/bonjorno7/SourceOps).

## Usage
<p align="center">
  <img src="https://user-images.githubusercontent.com/22228680/188257011-8fea3ab5-9dd2-4f28-8d46-2f2acb8dd955.png">
</p>

1. Select an armature.
2. Set AoI (default is 90).
3. Set scale (default is 1) if you use [$scale](https://developer.valvesoftware.com/wiki/$scale). This affects `<basepos>` since $scale does not work on $proceduralbones.
3. Pick a controller bone from the list.
4. The active bone in pose mode is the helper bone.
5. Click the buttons to copy the `<helper>` & `<basepos>` or `<trigger>` line and paste into your .vrd file.
