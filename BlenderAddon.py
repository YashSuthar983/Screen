bl_info = {
    "name": "Cube Distributor & Merger",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import bmesh
from bpy.props import IntProperty
from math import ceil,sqrt

class OBJECT_OT_DistributeCubes(bpy.types.Operator):
    bl_idname = "object.distribute_cubes"
    bl_label = "Distribute Cubes"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        n = context.scene.cube_count
        if n > 20:
            self.report({'ERROR'}, "The number is out of range")
            return {'CANCELLED'}
        
        m = ceil(sqrt(n))
        collection_name = "Distributed Cubes"

        # Create or get the collection
        if collection_name not in bpy.data.collections:
            cube_collection = bpy.data.collections.new(collection_name)
            context.scene.collection.children.link(cube_collection)
        else:
            cube_collection = bpy.data.collections[collection_name]

        # Get existing positions to prevent overlap
        occupied_positions = {(obj.location.x, obj.location.y) for obj in cube_collection.objects}
        
        for i in range(n):
            x, y = i % m, i // m
            while (x, y) in occupied_positions:
                x += 1
                if x >= m:
                    x = 0
                    y += 1
            occupied_positions.add((x, y))
            
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0))
            obj = context.object
            
            # Ensure object is added to the cube collection
            cube_collection.objects.link(obj)
        bpy.ops.object.select_all(action='SELECT')
            
        return {'FINISHED'}

class OBJECT_OT_DeleteCubes(bpy.types.Operator):
    bl_idname = "object.delete_cubes"
    bl_label = "Delete Cubes"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        for obj in context.selected_objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        return {'FINISHED'}

class OBJECT_OT_MergeMeshes(bpy.types.Operator):
    bl_idname = "object.merge_meshes"
    bl_label = "Compose Mesh"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        selected_objs = context.selected_objects
        if len(selected_objs) < 2:
            self.report({'WARNING'}, "Select at least two objects")
            return {'CANCELLED'}
        
        bpy.ops.object.join()
        obj = context.object
        mesh = bmesh.new()
        mesh.from_mesh(obj.data)

        # Find and remove common faces
        faces_to_remove = []
        for face in mesh.faces:
            shared_faces = [f for f in mesh.faces if set(f.verts) == set(face.verts)]
            if len(shared_faces) > 1:
                faces_to_remove.extend(shared_faces)
        
        bmesh.ops.delete(mesh, geom=faces_to_remove, context='FACES')
        
        # Merge common vertices
        bmesh.ops.remove_doubles(mesh, verts=mesh.verts, dist=0.0001)
        mesh.to_mesh(obj.data)
        obj.data.update()
        return {'FINISHED'}

class OBJECT_PT_CubePanel(bpy.types.Panel):
    bl_label = "Cube Tools"
    bl_idname = "OBJECT_PT_cube_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'
    
    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "cube_count")
        layout.operator("object.distribute_cubes")
        layout.operator("object.delete_cubes")
        layout.operator("object.merge_meshes")

classes = [
    OBJECT_OT_DistributeCubes,
    OBJECT_OT_DeleteCubes,
    OBJECT_OT_MergeMeshes,
    OBJECT_PT_CubePanel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.cube_count = IntProperty(
        name="Number of Cubes",
        default=1,
        min=1
    )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.cube_count

if __name__ == "__main__":
    register()

