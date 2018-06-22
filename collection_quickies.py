# GPL blahblah do whatever you want with this
bl_info = {
    "name": "Collectioranth",
    "author": "Pablo Vazquez",
    "version": (0, 1),
    "blender": (2, 80),
    "location": "Header of the 3D View",
    "description": "2.7 Style Collection Browser",
    "category": "Scene"}


import bpy
from bpy.types import Operator
from bpy.props import BoolProperty


def view3d_header_collections(self, context):

    layout = self.layout

    collections = bpy.data.collections
    act_ob = context.active_object

    idx = 1

    split = layout.split()
    col = split.column(align=True)
    row = col.row(align=True)
    row.scale_y = 0.5


    for coll in bpy.data.collections:

        # If there are icons, use LAYER_USED
        icon = 'LAYER_USED' if len(coll.objects) > 0 else 'BLANK1'

        # if the active object is in the current collection
        if act_ob and (coll in act_ob.users_collection):
            icon = 'LAYER_ACTIVE'

        props = row.operator('object.hide_collection', text='', icon=icon)
        props.collection_index = idx

        if idx%5==0:
            row = col.row(align=True)
            row.scale_y = 0.5

        if idx%10==0:
            layout.separator()
            col = layout.column(align=True)
            row = col.row(align=True)
            row.scale_y = 0.5

        idx += 1


def register():
    bpy.types.VIEW3D_HT_header.append(view3d_header_collections)


def unregister():
    bpy.types.VIEW3D_HT_header.remove(view3d_header_collections)


if __name__ == "__main__":
    register()
