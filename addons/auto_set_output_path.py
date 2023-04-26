bl_info = {
    "name": "Auto Set Render Output Path",
    "author": "Matthew Seremet @frostbitten + Open AI Chat GPT-4",
    "version": (1, 0, 0),
    "blender": (2, 93, 16),
    "location": "Render Properties > Output",
    "description": "Automatically sets render output path based on a template",
    "warning": "",
    "doc_url": "https://github.com/frostbitten/blender-frost",
    "category": "Render",
}

import bpy
import os
from bpy.app.handlers import persistent


def replace_variables(template, file_name, file_dir, blender_version):
    output_path = template.replace("__FILE_NAME__", file_name)
    output_path = output_path.replace("__FILE_DIR__", file_dir)
    output_path = output_path.replace("__BLENDER_VERSION__", blender_version)
    return output_path


@persistent
def auto_set_output_path(dummy):
    scene = bpy.context.scene
    if scene.auto_set_output:
        current_file_path = bpy.data.filepath
        current_file_name = os.path.basename(current_file_path)
        file_name_without_extension, _ = os.path.splitext(current_file_name)

        file_dir = os.path.dirname(current_file_path)
        blender_version = f"{bpy.app.version[0]}.{bpy.app.version[1]}.{bpy.app.version[2]}"

        output_path = replace_variables(scene.template_output_path, file_name_without_extension, file_dir, blender_version)
        scene.render.filepath = output_path


def update_auto_set_output(self, context):
    auto_set_output_path(None)
    
def update_template_output_path(self, context):
    auto_set_output_path(None)


class RENDER_PT_auto_set_output(bpy.types.Panel):
    bl_label = "Auto Set Output Path"
    bl_idname = "RENDER_PT_auto_set_output"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"
    bl_parent_id = "RENDER_PT_output"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "auto_set_output")
        layout.prop(scene, "template_output_path")


def register():
    bpy.utils.register_class(RENDER_PT_auto_set_output)
    bpy.types.Scene.auto_set_output = bpy.props.BoolProperty(name="Auto Set Output Path", default=False, update=update_auto_set_output)
    bpy.types.Scene.template_output_path = bpy.props.StringProperty(
        name="Output Path Template",
        default="//renders/__FILE_NAME__/__FILE_NAME___",
        subtype='FILE_PATH',
        update=update_template_output_path
    )
    bpy.app.handlers.save_post.append(auto_set_output_path)


def unregister():
    bpy.utils.unregister_class(RENDER_PT_auto_set_output)
    del bpy.types.Scene.auto_set_output
    del bpy.types.Scene.template_output_path
    bpy.app.handlers.save_post.remove(auto_set_output_path)


if __name__ == "__main__":
    register()
