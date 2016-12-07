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
    "name": "Legolizer",
    "category": "Mesh",
}

import bpy
    
class Legolizer(bpy.types.Operator):
    """Legolizer"""                    # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "object.legolize"      # unique identifier for buttons and menu items to reference.
    bl_label = "Legolize"              # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
 
    def execute(self, context):        # execute() is called by blender when running the operator.

        # The original script
        for obj in bpy.context.selected_objects:
            bpy.context.scene.objects.active = obj
            bpy.ops.object.modifier_add(type='REMESH')
            bpy.context.object.modifiers["Remesh"].mode = 'BLOCKS'
            bpy.context.object.modifiers["Remesh"].octree_depth = 6
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Remesh")

        return {'FINISHED'}            # this lets blender know the operator finished successfully.

def register():
    bpy.utils.register_class(Legolizer)

def unregister():
    bpy.utils.unregister_class(Legolizer)

# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()