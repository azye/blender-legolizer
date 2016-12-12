bl_info = {
    "name": "Legolizer",
    "category": "Mesh",
}

import bpy
import bmesh
from mathutils import Vector

OCTREE_DEPTH = 4
UP_VECTOR = Vector((0.0, 0.0, 1.0));

def calculate_radius(obj):
    v0 = obj.matrix_world * obj.data.vertices[obj.data.edges[0].vertices[0]].co
    v1 = obj.matrix_world * obj.data.vertices[obj.data.edges[0].vertices[1]].co
    return (v1-v0).length / 2.8
    
class Legolizer(bpy.types.Operator):
    """Legolizer"""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "object.legolize"        # unique identifier for buttons and menu items to reference.
    bl_label = "Legolize"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
 
    def execute(self, context):        # execute() is called by blender when running the operator.
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                bpy.ops.object.mode_set(mode='OBJECT')
                context.scene.objects.active = obj
                bpy.ops.object.modifier_add(type='REMESH')
                context.object.modifiers["Remesh"].mode = 'BLOCKS'
                context.object.modifiers["Remesh"].octree_depth = OCTREE_DEPTH
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Remesh")
                
                # context.scene.objects.active = obj
                # bpy.ops.object.mode_set(mode='EDIT')
                # bm = bmesh.from_edit_mesh(obj.data)
                # #ret = bmesh.ops.bevel(bm, geom=bm.edges, offset=0.005, segments=4, profile=0.3)
                # for face in bm.faces[:]:
                #     if (face.normal != UP_VECTOR) and (face.normal != UP_VECTOR * -1):
                #         print(face.edges[:])
                #         for edge in face.edges[:]:
                #             print(dir(edge))
                #             for vert in edge.verts:
                #                 print(dir(vert))
                        #bmesh.ops.bevel(bm, geom=face.edges, offset=0.2, profile=0.3)
                
                #bpy.ops.object.mode_set(mode='OBJECT')
                radius = calculate_radius(obj)
                for polygon in obj.data.polygons:
                    if polygon.normal == UP_VECTOR:
                        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=1.4*radius, location=polygon.center)
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
                
                if bpy.context.mode == 'OBJECT':
                    bpy.ops.object.mode_set(mode='EDIT', toggle=True)
                bpy.ops.mesh.dissolve_degenerate()
      
            return {'FINISHED'}            # this lets blender know the operator finished successfully.
    
def register():
    bpy.utils.register_class(Legolizer)

def unregister():
    bpy.utils.unregister_class(Legolizer)

# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()