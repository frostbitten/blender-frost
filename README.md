# Blender Frost

This is a collection of addons, tools, and random bits of info that have helped me achieve a smooth Blender experience.

A large portion of the code was generated with the help of AI tools.

## Addons

### auto_set_output_path.py

Automatically set the output path based on a template. Helpful when quickly iterating on a project to ensure new renders don't overwrite previous ones. The automatic update triggers after each save and whenever the template is updated.

Variables:
  *  `__FILE_NAME__` The blend file name without extension
  * `__BLENDER_VERSION__`

Defaults to `//renders/__FILE_NAME__/__FILE_NAME___`.

Example: A blender file named `my-animation-v021.blend` would output frame 1 to `//renders/my-animation-v021/my-animation-v021_0001.png`

Tested in Blender `v2.93.16`, `v3.5.0`