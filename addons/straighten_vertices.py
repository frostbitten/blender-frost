bl_info = {
    "name": "Straighten Vertices",
    "author": "Matthew Seremet @frostbitten + Open AI Chat GPT-4",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Mesh Tools",
    "description": "Straightens the selected vertices between the first and last vertex in the selection.",
    "category": "Mesh",
}

import bpy
import bmesh

class MESH_OT_straighten(bpy.types.Operator):
    bl_idname = "mesh.straighten"
    bl_label = "Straighten Vertices"
    bl_options = {'REGISTER', 'UNDO'}

    influence: bpy.props.FloatProperty(
        name="Influence",
        description="Influence of the straightening operation",
        default=1.0,
        min=0.0,
        max=1.0
    )

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != "MESH":
            self.report({"ERROR"}, "Active object must be a mesh")
            return {"CANCELLED"}

        bpy.ops.object.mode_set(mode="EDIT")
        mesh = bmesh.from_edit_mesh(obj.data)

        selected_verts = [v for v in mesh.verts if v.select]

        if len(selected_verts) < 3:
            self.report({"ERROR"}, "At least 3 vertices must be selected")
            return {"CANCELLED"}

        last_vert = mesh.select_history.active
        if last_vert is None or not last_vert.select:
            self.report({"ERROR"}, "No active vertex found or it's not selected")
            return {"CANCELLED"}

        first_vert = None
        for v in selected_verts:
            linked_verts = [e.other_vert(v) for e in v.link_edges if e.other_vert(v).select]
            if len(linked_verts) == 1 and v != last_vert:
                first_vert = v
                break

        if first_vert is None:
            self.report({"ERROR"}, "Couldn't find the first selected vertex")
            return {"CANCELLED"}

        start_vert = first_vert.co
        end_vert = last_vert.co
        line_vector = end_vert - start_vert

        for vert in selected_verts:
            if vert != first_vert and vert != last_vert:
                original_position = vert.co
                projected_position = start_vert + line_vector * line_vector.dot(vert.co - start_vert) / line_vector.length_squared
                vert.co = original_position.lerp(projected_position, self.influence)

        bmesh.update_edit_mesh(obj.data)
        return {"FINISHED"}

class VIEW3D_PT_mesh_straighten(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Mesh Tools"
    bl_label = "Straighten Vertices"

    def draw(self, context):
        layout = self.layout
        layout.operator(MESH_OT_straighten.bl_idname)

def menu_func(self, context):
    self.layout.operator(MESH_OT_straighten.bl_idname)

def register():
    bpy.utils.register_class(MESH_OT_straighten)
    bpy.utils.register_class(VIEW3D_PT_mesh_straighten)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.prepend(menu_func)

def unregister():
    bpy.utils.unregister_class(MESH_OT_straighten)
    bpy.utils.unregister_class(VIEW3D_PT_mesh_straighten)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)

if __name__ == "__main__":
    register()
