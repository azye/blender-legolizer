bl_info = {
    "name": "Legolizer",
    "category": "Mesh",
}

import bpy
import bmesh
from mathutils import Vector
from bpy.props import *

OCTREE_DEPTH = 4
UP_VECTOR = Vector((0.0, 0.0, 1.0))
DEF_UP_VECTOR = '+z'
 
class DialogOperator(bpy.types.Operator):
    bl_idname = "object.legolize"
    bl_label = "Legolize"
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    
    BUMP_ROTATE = Vector((0.0, 0.0, 0.0))
    
    O_DEPTH = IntProperty(name="Octree Depth", 
        min=0, max=8, default=4)

    U_VECTOR = EnumProperty(name="Lego Bump Direction",
        items = [
            ('-z', '-z', '-z'),
            ('+z', '+z', '+z'),
            ('-y', '-y', '-y'),
            ('+y', '+y', '+y'),
            ('-x', '-x', '-x'),
            ('+x', '+x', '+x')
        ]
    )

    def execute(self, context):        # execute() is called by blender when running the operator.
        message = "%d, %s" % (self.O_DEPTH, self.U_VECTOR)
        vec = self.U_VECTOR
       
        if vec == '+x':
            UP_VECTOR = Vector((1.0, 0.0, 0.0))
            self.BUMP_ROTATE = Vector((0.0, 1.57, 0.0))
        elif vec == '-x':
            UP_VECTOR = Vector((-1.0, 0.0, 0.0))
            self.BUMP_ROTATE = Vector((0.0, 1.57, 0.0))
        elif vec == '+y':
            UP_VECTOR = Vector((0.0, 1.0, 0.0))
            self.BUMP_ROTATE = Vector((1.57, 0.0, 0.0))
        elif vec == '-y':
            UP_VECTOR = Vector((0.0, -1.0, 0.0))
            self.BUMP_ROTATE = Vector((1.57, 0.0, 0.0))
        elif vec == '+z':
            UP_VECTOR = Vector((0.0, 0.0, 1.0))
        elif vec == '-z':
            UP_VECTOR = Vector((0.0, 0.0, -1.0))

        for obj in bpy.context.selected_objects:            
            bpy.ops.object.mode_set(mode='OBJECT')
            context.scene.objects.active = obj
            bpy.ops.object.modifier_add(type='REMESH')
            context.object.modifiers["Remesh"].mode = 'BLOCKS'
            context.object.modifiers["Remesh"].octree_depth = OCTREE_DEPTH
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Remesh")

            radius = calculate_radius(obj)
            for polygon in obj.data.polygons:
                if polygon.normal == UP_VECTOR:
                    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=1.4*radius, location=polygon.center, rotation=self.BUMP_ROTATE)
                    bump = bpy.context.object
                    bump.parent = obj
                
            bpy.ops.object.select_all(action='DESELECT')
            context.scene.objects.active = obj
            bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')
            obj.select = True
            for so in context.selected_objects:
                if so.type != 'MESH':
                    so.select = False
            if len(context.selected_objects):
                context.scene.objects.active = context.selected_objects[0]        
                bpy.ops.object.join()

            bpy.ops.object.modifier_add(type='BEVEL')
            context.object.modifiers["Bevel"].segments = 2
            context.object.modifiers["Bevel"].width = 0.05
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Bevel")
            
            bpy.ops.object.mode_set(mode='EDIT', toggle=True)
            bpy.ops.mesh.dissolve_degenerate()
            
            bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, message)
        print(message)
        return {'FINISHED'}            # this lets blender know the operator finished successfully.
 
    def invoke(self, context, event):
        global OCTREE_DEPTH, DEF_UP_VECTOR
        self.O_DEPTH = OCTREE_DEPTH
        self.U_VECTOR = DEF_UP_VECTOR
        return context.window_manager.invoke_props_dialog(self)

class DialogPanel(bpy.types.Panel):
    bl_label = "Dialog"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
 
    def draw(self, context):
        global OCTREE_DEPTH, DEF_UP_VECTOR
        OCTREE_DEPTH = 4
        DEF_UP_VECTOR = '+z'
        self.layout.operator("object.dialog_operator")

def calculate_radius(obj):
    v0 = obj.matrix_world * obj.data.vertices[obj.data.edges[0].vertices[0]].co
    v1 = obj.matrix_world * obj.data.vertices[obj.data.edges[0].vertices[1]].co
    return (v1-v0).length / 2.8
    
def register():
    bpy.utils.register_class(DialogOperator)

def unregister():
    bpy.utils.unregister_class(DialogOperator)

# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()