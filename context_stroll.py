# GPL blahblah do whatever you want with this
bl_info = {
    "name": "Stroll to Next/Previous Context",
    "author": "Pablo Vazquez",
    "version": (0, 1),
    "blender": (2, 77),
    "location": "Properties editor: Press Ctrl+Tab for next context, Ctrl+Shift+Tab for previous.",
    "description": "Easily jump to the next or previous context",
    "category": "Scene"}


import bpy
from bpy.types import Operator
from bpy.props import BoolProperty


class SCENE_OT_context_stroll(Operator):
    '''Jump to the next or previous scene'''
    bl_idname = "screen.context_stroll"
    bl_label = "Jump to Next/Previous Context"
    bl_options = {'REGISTER', 'UNDO'}

    next = BoolProperty(
        default=True,
        name="Next Context",
        description="Disable to jump to previous context",
        options={'SKIP_SAVE'},
        )

    def execute(self, context):
        space = bpy.context.space_data

        # There must be a smarter way of getting this        
        contexts = ['RENDER',
                    'RENDER_LAYER',
                    'SCENE',
                    'WORLD',
                    'OBJECT',
                    'CONSTRAINT',
                    'MODIFIER',
                    'DATA',
                    'MATERIAL',
                    'BONE',
                    'BONE_CONSTRAINT',
                    'TEXTURE',
                    'PARTICLES',
                    'PHYSICS']


        # Only if we are in the properties editor
        if space.type == 'PROPERTIES':
            context_current = contexts.index(space.context)
            context_go = (context_current + 1) if self.next else (context_current - 1)

            # First try if the context we want to go to is available
            try:
                space.context = contexts[context_go]
            except:
                # Oops! Not found, lets move to the next or previous
                found = False
                context_go += 1 if self.next else -1

                while found is False:
                    try:
                        # Success!
                        space.context = contexts[context_go]
                        found = True
                    except:
                        # Nope, keep trying. If we reach the end, start again
                        if context_go < len(contexts):
                            context_go += 1 if self.next else -1
                        else:
                            context_go = 0
                        continue

        return {'FINISHED'}


addon_keymaps = []

def register():
    bpy.utils.register_class(SCENE_OT_context_stroll)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.get('Window')
        if not km:
            km = kc.keymaps.new(name='Window')

        kmi = km.keymap_items.new('screen.context_stroll', 'TAB', 'PRESS', shift=True, ctrl=True)
        kmi.properties.next = False
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('screen.context_stroll', 'TAB', 'PRESS', shift=False, ctrl=True)
        kmi.properties.next = True
        addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(SCENE_OT_context_stroll)


if __name__ == "__main__":
    register()

