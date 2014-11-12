# GPL blahblah do whatever you want with this
bl_info = {
    "name": "Go to Next/Previous Scene",
    "author": "Pablo Vazquez",
    "version": (0, 1),
    "blender": (2, 72),
    "location": "Scene Properties > Scene, or press Ctrl+Shift+Left/Right",
    "description": "Go to the next/previous scene",
    "category": "Scene"}

import bpy
from bpy.types import Operator
from bpy.props import BoolProperty

class SCENE_OT_stroll(Operator):
    '''Go to the next/previous scene'''
    bl_idname = "scene.stroll"
    bl_label = "Scene Next / Previous"

    next = BoolProperty(default=True)

    def execute(self, context):

        # Only go if we have more than 1 scene
        if len(bpy.data.scenes) > 1:
            # This is extremely stupid. Really, a 5 years old would find
            # a better way to do it. We go from 0 to the number of scenes
            # we have, then if N is the same as the current one, save N
            for n in range(0, len(bpy.data.scenes)):
                if bpy.context.scene.name == bpy.data.scenes[n].name:
                    break

            if self.next:
                n += 1
            else:
                n -= 1

            try:
                bpy.context.screen.scene = bpy.data.scenes[n]
            except:
                bpy.context.screen.scene = bpy.data.scenes[0]
        else:
            self.report({"INFO"}, "No other scenes to go to")

        return {'FINISHED'}

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
        icon='FORWARD').next=True

addon_keymaps = []

def register():
    bpy.utils.register_class(SCENE_OT_stroll)
    bpy.types.SCENE_PT_scene.append(scene_stroll_ui)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Window')
        kmi = km.keymap_items.new('scene.stroll', 'LEFT_ARROW', 'PRESS', shift=True, ctrl=True)
        kmi.properties.next = False
        kmi = km.keymap_items.new('scene.stroll', 'RIGHT_ARROW', 'PRESS', shift=True, ctrl=True)
        kmi.properties.next = True

        addon_keymaps.append((km, kmi))

def unregister():
    bpy.utils.unregister_class(SCENE_OT_stroll)
    bpy.types.SCENE_PT_scene.remove(scene_stroll_ui)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()

