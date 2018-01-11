# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Amaranth Channel Tools",
    "author": "Pablo Vazquez",
    "version": (1, 0),
    "blender": (2, 76, 0),
    "location": "Sequencer > Channel Tools Panel",
    "description": "Tools for Channels",
    "warning": "",
    "wiki_url": "",
    "category": "Sequencer",
    }


import bpy
from bpy.types import Operator, Panel, UIList, PropertyGroup


def get_strip_rectf(strip):
     # Get x and y in terms of the grid's frames and channels
    x1 = strip.frame_final_start
    x2 = strip.frame_final_end
    y1 = strip.channel + 0.2
    y2 = y1 + 0.25

    return [x1, y1, x2, y2]

def get_channel_rectf(channel, scene, full=False):
     # Get x and y in terms of the grid's frames and channels
    x1 = scene.frame_start
    x2 = scene.frame_end
    y1 = channel
    if full:
        y2 = y1 + 1
    else:
        y2 = y1 + 0.1
    # y2 = y1 + 1

    return [x1, y1, x2, y2]


def draw_channel_color(scroller_width, channel_coords, curx, color):
    from bgl import glColor4f, glRectf, glEnable, glDisable, glBlendFunc, GL_BLEND, GL_ONE, GL_SRC_ALPHA

    context = bpy.context

    # Strip coords
    s_x1, s_y1, s_x2, s_y2 = channel_coords

    # Drawing coords
    x = 0
    d_y1 = s_y1
    d_y2 = s_y2
    d_x1 = s_x1
    d_x2 = s_x2

    # be careful not to override the current frame line
    cf_x = context.scene.frame_current_final
    y = 0

    r, g, b, a = color
    glColor4f(r, g, b, a)
    glEnable(GL_BLEND)
    # glBlendFunc(GL_SRC_ALPHA, GL_ONE);

    if d_x1 < cf_x and cf_x < d_x2:
        # current frame line over strip
        glRectf(d_x1, d_y1, cf_x - curx, d_y2)
        glRectf(cf_x + curx, d_y1, d_x2, d_y2)
    else:
        # Normal, full rectangle draw
        glRectf(d_x1, d_y1, d_x2, d_y2)

    glDisable(GL_BLEND)


def draw_underline_in_strip(scroller_width, strip_coords, curx, color):
    from bgl import glColor4f, glRectf, glEnable, glDisable, GL_BLEND

    context = bpy.context

    # Strip coords
    s_x1, s_y1, s_x2, s_y2 = strip_coords

    # Drawing coords
    x = 0
    d_y1 = s_y1
    d_y2 = s_y2
    d_x1 = s_x1
    d_x2 = s_x2

    # be careful not to override the current frame line
    cf_x = context.scene.frame_current_final
    y = 0

    r, g, b, a = color
    glColor4f(r, g, b, a)
    glEnable(GL_BLEND)

    # // this checks if the strip range overlaps the current f. label range
    # // then it would need a polygon? to draw around it
    # // TODO: check also if label display is ON
    # Check if the current frame label overlaps the strip
    # label_height = scroller_width * 2
    # if d_y1 < label_height:
    #    if cf_x < d_x2 and d_x1 < cf_x + label_height:
    #        print("ALARM!!")

    if d_x1 < cf_x and cf_x < d_x2:
        # Bad luck, the line passes our strip
        glRectf(d_x1, d_y1, cf_x - curx, d_y2)
        glRectf(cf_x + curx, d_y1, d_x2, d_y2)
    else:
        # Normal, full rectangle draw
        glRectf(d_x1, d_y1, d_x2, d_y2)

    glDisable(GL_BLEND)


def draw_callback_px():
    context = bpy.context

    if not context.scene.sequence_editor:
        return

    # Calculate scroller width, dpi and pixelsize dependent
    pixel_size = context.user_preferences.system.pixel_size
    dpi = context.user_preferences.system.dpi
    dpi_fac = pixel_size * dpi / 72
    # A normal widget unit is 20, but the scroller is apparently 16
    scroller_width = 16 * dpi_fac

    region = context.region
    xwin1, ywin1 = region.view2d.region_to_view(0, 0)
    xwin2, ywin2 = region.view2d.region_to_view(region.width, region.height)
    curx, cury = region.view2d.region_to_view(1, 0)
    curx = curx - xwin1

    act_channel = context.scene.vse_channels_list_index + 1

    # for strip in context.scene.sequence_editor.sequences:
    #     if strip.channel == act_channel:
    #         pass

    #         # Get corners (x1, y1), (x2, y2) of the strip rectangle in px region coords
    #         strip_coords = get_strip_rectf(strip)

    #         #check if any of the coordinates are out of bounds
    #         if strip_coords[0] > xwin2 or strip_coords[2] < xwin1 or strip_coords[1] > ywin2 or strip_coords[3] < ywin1:
    #             continue

    #         # Draw
    #         color = [1.0, 0, 1.0, 0.1]
    #         draw_underline_in_strip(scroller_width, strip_coords, curx, color)

    for strip in context.scene.sequence_editor.sequences:
        if strip.name.endswith('final'):

            strip_coords = get_strip_rectf(strip)

            if strip_coords[0] > xwin2 or strip_coords[2] < xwin1 or strip_coords[1] > ywin2 or strip_coords[3] < ywin1:
                continue

            color = [0.863, 0.078, 0.235, 0.5]
            draw_underline_in_strip(scroller_width, strip_coords, curx, color)


    channels_list = context.scene.vse_channels_list
    channels_index = context.scene.vse_channels_list_index

    # Get corners (x1, y1), (x2, y2) of the strip rectangle in px region coords
    for c in channels_list:
        channel_coords = get_channel_rectf(c.number, context.scene)

        # Draw colors for each channel
        color = [c.color[0],c.color[1], c.color[2], 0.33]
        draw_channel_color(scroller_width, channel_coords, curx, color)

        # Highlight active channel
        if c == channels_list[channels_index]:
            channel_coords = get_channel_rectf(c.number, context.scene, True)

            # color = [1.0, 0.66, 0.25, 0.1]
            color = [1.0, 1.0, 1.0, 0.1]
            draw_channel_color(scroller_width, channel_coords, curx, color)

def tag_redraw_all_sequencer_editors():
    context = bpy.context

    # Py cant access notifiers
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'SEQUENCE_EDITOR':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        region.tag_redraw()

# This is a list so it can be changed instead of set
# if it is only changed, it does not have to be declared as a global everywhere
cb_handle = []


def callback_enable():
    if cb_handle:
        return

    cb_handle[:] = bpy.types.SpaceSequenceEditor.draw_handler_add(
        draw_callback_px, (), 'WINDOW', 'POST_VIEW'),

    tag_redraw_all_sequencer_editors()


def callback_disable():
    if not cb_handle:
        return

    bpy.types.SpaceSequenceEditor.draw_handler_remove(cb_handle[0], 'WINDOW')

    tag_redraw_all_sequencer_editors()


class SEQUENCER_OT_ChannelsToolsInitialize(Operator):
    """Initialize Channels Tools Addon"""
    bl_idname = "sequencer.channel_tools_initialize"
    bl_label = "Initialize Channels Tools"

    def execute(self, context):
        bpy.context.scene.vse_channels_list.clear()

        for c in range(1, 33):
            channel = bpy.context.scene.vse_channels_list.add()
            channel.name = "Channel #%i" % c
            channel.number = c

        return {'FINISHED'}


class SEQUENCER_OT_ChannelSelectAll(Operator):
    """Select all strips in channel"""
    bl_idname = "sequencer.channel_select_all"
    bl_label = "Select Strips in Channel"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        channel = context.scene.vse_channels_list_index + 1

        for s in context.sequences:
            s.select = True if s.channel == channel else False

        return {'FINISHED'}


class SEQUENCER_OT_ChannelMute(Operator):
    """Mute all strips in channel"""
    bl_idname = "sequencer.channel_mute"
    bl_label = "Mute Strips in Channel"
    bl_options = {'REGISTER', 'UNDO'}

    inverse = bpy.props.BoolProperty(default=False)
    channel = bpy.props.IntProperty(default=1)

    def execute(self, context):
        inverse = self.inverse
        channel = self.channel

        context.scene.vse_channels_list_index = channel - 1

        for s in context.sequences:
            if s.channel == channel:
                s.mute = inverse

        return {'FINISHED'}


class SEQUENCER_OT_SilenceAll(Operator):
    """Silence all sound strips"""
    bl_idname = "sequencer.silence_all"
    bl_label = "Silence All Volume Strips"
    bl_options = {'REGISTER', 'UNDO'}

    selected = bpy.props.BoolProperty(default=False)

    def execute(self, context):

        channel = context.scene.vse_channels_list_index + 1

        if self.selected:
            sequences = context.selected_editable_sequences
        else:
            sequences = context.sequences

        for s in sequences:
            if s.type == 'SOUND':
                s.mute = True

        return {'FINISHED'}


class SEQUENCER_OT_DeleteAllStrips(bpy.types.Operator):
    """Delete All Strips"""
    bl_idname = "sequencer.delete_all_strips"
    bl_label = "Delete All Strips"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        # Save which editor are we in when we run the operator
        where = bpy.context.area.type

        # Temporary switch to the Sequencer to get context data
        bpy.context.area.type = 'SEQUENCE_EDITOR'

        # Build the context to override
        override = {
            "window": bpy.context.window,
            "screen": bpy.context.screen,
            "scene": context.scene,
            "area": bpy.context.area,
            "region": bpy.context.area.regions[0],
            "blend_data": context.blend_data}

        # Check if we have sequences at all
        if context.scene.sequence_editor and context.scene.sequence_editor.sequences_all:

            i = 0

            for s in context.scene.sequence_editor.sequences_all:
                s.select = True
                # this is just to count them (for the report message)
                i += 1

            # DIE DIE DIE!
            bpy.ops.sequencer.delete(override)

            if i != 0:
                self.report({"INFO"}, "BAM! {0} Strips Destroyed!".format(i))
            else:
                self.report({"INFO"}, "No strips to murder")
        else:
            self.report({"INFO"}, "No sequences")

        # Go back to the area we were before
        bpy.context.area.type = where

        return {'FINISHED'}


def header_stuff(self, context):
    space = context.space_data

    scene = context.scene
    channels_list = scene.vse_channels_list
    channels_index = scene.vse_channels_list_index
    act_strip = scene.sequence_editor.active_strip
    channels_index_strip = act_strip.channel - 1

    layout = self.layout

    if space.view_type in {'SEQUENCER', 'SEQUENCER_PREVIEW'}:
        if channels_index >= 0 and len(channels_list) > 0:

            row = layout.row(align=True)
            row.label(text="Channel:")

            row = layout.row(align=True)
            row.prop(channels_list[channels_index_strip], "color", text="")
            row.prop(channels_list[channels_index_strip], "name", text="")


class SEQUENCER_PG_channels_item(PropertyGroup):
    """ Group of properties representing an item in the list """

    number = bpy.props.IntProperty(
           name="Number",
           description="Number of the channel",
           default=1)

    name = bpy.props.StringProperty(
           name="Name",
           description="Name for the channel",
           default="Channel")

    color = bpy.props.FloatVectorProperty(
           name="Color",
           subtype='COLOR',
           description="Color for the channel",
           default=[0.2,0.2,0.2],
           size=3,
           precision=2,
           min=0.0,
           max=1.0)


class SEQUENCER_UL_channels(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):

        col = layout.column()
        split = col.split(percentage=0.1)

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # row = split.row(align=False)
            split.prop(item, "color", text="")
            row = split.row(align=True)
            split = row.split(percentage=0.75)
            split.label(text="{0}. {1}".format(item.number, item.name), translate=False)

        elif self.layout_type in {'GRID'}:
            row.alignment = 'CENTER'
            row.label(text="")

        row = split.row(align=True)

        row.operator(
            "sequencer.channel_select_all",
            icon="RESTRICT_SELECT_OFF",
            emboss=False,
            text="")
        props = row.operator(
            "sequencer.channel_mute",
            icon="RESTRICT_VIEW_OFF",
            emboss=False,
            text="")
        props.inverse = False
        props.channel = item.number

        props = row.operator(
            "sequencer.channel_mute",
            icon="RESTRICT_VIEW_ON",
            emboss=False,
            text="")
        props.inverse = True
        props.channel = item.number


class SEQUENCER_PT_ChannelTools(Panel):
    bl_label = "Amaranth VSE Tools"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'


    def draw(self, context):

        scene = context.scene
        layout = self.layout

        layout.operator(
            "sequencer.channel_tools_initialize",
            text="Reset Channel Settings")

        layout.separator()

        if scene.vse_channels_list_index >= 0 and len(scene.vse_channels_list) > 0:
            layout.template_list("SEQUENCER_UL_channels", "", scene, "vse_channels_list", scene, "vse_channels_list_index")

            if scene.vse_channels_list_index >= 0 and len(scene.vse_channels_list) > 0:
                item = scene.vse_channels_list[scene.vse_channels_list_index]

                row = layout.row()
                row.prop(item, "name", text="Channel Name")

            layout.separator()

            layout.label(text="Sequencer Tools:")

            col = layout.column()
            split = col.split(percentage=0.50)
            split.label(text="Silence Volume Strips:", icon="SPEAKER")

            row = split.row(align=True)
            row.operator(
                "sequencer.silence_all",
                text="All").selected = False
            row.operator(
                "sequencer.silence_all",
                text="Selected").selected = True

            layout.separator()

            row = layout.row(align=True)
            row.operator(
                "sequencer.delete_all_strips",
                icon="X")


def register():

    bpy.utils.register_module(__name__)
    bpy.types.Scene.vse_channels_list = bpy.props.CollectionProperty(type = SEQUENCER_PG_channels_item)
    bpy.types.Scene.vse_channels_list_index = bpy.props.IntProperty(name = "Index for Channels List", default = 0)

    bpy.types.SEQUENCER_HT_header.append(header_stuff)

    callback_enable()


def unregister():

    callback_disable()

    del bpy.types.Scene.vse_channels_list
    del bpy.types.Scene.vse_channels_list_index

    bpy.types.SEQUENCER_HT_header.remove(header_stuff)

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()

