# GPL blahblah do whatever you want with this
bl_info = {
    "name": "Jump to Next/Previous Scene",
    "author": "Pablo Vazquez, Dalai Felinto",
    "version": (0, 2),
    "blender": (2, 72),
    "location": "Scene Properties > Scene, or press Ctrl+Shift+Left/Right",
    "description": "Easily jump to the next or previous scenes",
    "category": "Scene"}


import bpy
from bpy.types import Operator
from bpy.props import BoolProperty


class SCENE_OT_stroll(Operator):
    '''Jump to the next or previous scene'''
    bl_idname = "scene.stroll"
    bl_label = "Jump to Next Scene"
    bl_options = {'REGISTER', 'UNDO'}

    next = BoolProperty(
        default=True,
        name="Next Scene",
        description="Disable to jump to previous scene",
        options={'SKIP_SAVE'},
        )

    def execute(self, context):
        scenes = bpy.data.scenes

        # Only go if we have more than 1 scene
        if scenes[0] != scenes[-1]:

            scene_id = scenes.find(context.scene.name)
            scene_id += 1 if self.next else -1

            if scene_id < 0 or scene_id == len(scenes):
                return self.error()

            bpy.context.screen.scene = scenes[scene_id]
        else:
            return self.error()

        return {'FINISHED'}

    def error(self):
        self.report({"INFO"}, "No more scenes to go to")
        return {'CANCELLED'}


def scene_stroll_ui(self, context):

    layout = self.layout

    split = layout.split(percentage=0.33)

    col = split.column()
    col.label(text="Go to Scene:")

    col = split.column()
    row = col.row(align=True)

    row.operator(
        SCENE_OT_stroll.bl_idname,
        text="Previous",
        icon='BACK').next=False

    row.operator(
        SCENE_OT_stroll.bl_idname,
        text="Next",
        icon='FORWARD')


addon_keymaps = []

def register():
    bpy.utils.register_class(SCENE_OT_stroll)
    bpy.types.SCENE_PT_scene.append(scene_stroll_ui)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.get('Window')
        if not km:
            km = kc.keymaps.new(name='Window')

        kmi = km.keymap_items.new('scene.stroll', 'LEFT_ARROW', 'PRESS', shift=True, ctrl=True)
        kmi.properties.next = False
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('scene.stroll', 'RIGHT_ARROW', 'PRESS', shift=True, ctrl=True)
        kmi.properties.next = True
        addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.types.SCENE_PT_scene.remove(scene_stroll_ui)
    bpy.utils.unregister_class(SCENE_OT_stroll)


if __name__ == "__main__":
    register()

