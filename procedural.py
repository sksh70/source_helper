bl_info = {
    'name': 'Source Procedural Bone',
    'author': 'Β L Λ Ζ Ξ',
    'version': (0, 35),
    'blender': (2, 79, 0),
    'location': 'View3D > Tool Shelf > Β L Λ Ζ Ξ',
    'description': 'Get <helper> and <trigger> for $proceduralbones. Modified from SourceOps.',
    'warning': '',
    'wiki_url': '',
    'category': 'Scene',
    }
    
import bpy
from bpy.props import *
import math

def main(context):
    scn = context.scene
    ob = bpy.context.object
    bone = bpy.context.active_pose_bone
    
    if ob is not None:
        if ob.type == 'ARMATURE':
            bone2 = ob.pose.bones.get(scn.Controller)
            
            if bone and bone2 is not None:
                if bone.parent:
                	parent = bone.parent.matrix.inverted_safe()
                	matrix = parent * bone.matrix
                else:
                	matrix = bone.matrix

                vectorRot = matrix.to_euler()
                vectorRot = [math.degrees(n) for n in vectorRot]
                vectorPos = matrix.to_translation().xyz
                vectorPos = [n * round(scn.MyFloat,3) for n in vectorPos]

                stringRot = ' '.join(str(round(n, 6)) for n in vectorRot)
                stringPos = ' '.join(str(round(n, 6)) for n in vectorPos)
                
                if bone2.parent:
                	parent2 = bone2.parent.matrix.inverted_safe()
                	matrix2 = parent2 * bone2.matrix
                else:
                	matrix2 = bone2.matrix

                vectorRot2 = matrix2.to_euler()
                vectorRot2 = [math.degrees(n) for n in vectorRot2]
                vectorPos2 = matrix2.to_translation().xyz
                vectorPos2 = [n * round(scn.MyFloat,3) for n in vectorPos2]

                stringRot2 = ' '.join(str(round(n, 6)) for n in vectorRot2)
                stringPos2 = ' '.join(str(round(n, 6)) for n in vectorPos2)
           
                try:
                    return stringPos, stringRot, bone, bone.name, bone.parent.name, stringRot2
                except:
                    return stringPos, stringRot, bone, bone.name, '', stringRot2

class ProceduralBone(bpy.types.Operator):
    bl_idname = 'blz.procedural'
    bl_label = 'Pose Bone Transforms'
    bl_options = {'REGISTER', 'INTERNAL'}
    
    type = bpy.props.EnumProperty(
        name = 'Transform Type',
        items = [
            ('HELPER', 'Helper', ''),
            ('TRIGGER', 'Trigger', ''),
        ],
    )
	
    @classmethod
    def poll(cls, context):
        return context.mode == 'POSE'

    def execute(self, context):
        result = main(context)
        scn = context.scene
        ob = bpy.context.object
        
        if result is not None:
            bone = result[2]
            
            if ob.type == 'ARMATURE':  
                pb = ob.pose.bones.get(scn.Controller)

                try:
                    parent = pb.parent.name
                except:
                    parent = ''
                
                if bone is None:
                    self.report({'INFO'}, 'No active bone')
                    return {'CANCELLED'}
                else:
                    if self.type == 'HELPER':
                        bone_name_parent = result[3].replace('ValveBiped.','') + ' ' + result[4].replace('ValveBiped.','')
                        bone_controller_parent = parent.replace('ValveBiped.','') + ' ' + scn.Controller.replace('ValveBiped.','')
                        context.window_manager.clipboard = "<helper> " + bone_name_parent + ' ' + bone_controller_parent + '\n<basepos> ' + result[0] + "\n"
                        self.report({'INFO'}, 'Copied <helper> to clipboard!'+ result[0])
                    elif self.type == 'TRIGGER':
                        context.window_manager.clipboard = "<trigger> " + str(scn.MyInt) + "\t" + result[5] + "\t" + result[1] + "\t" + "0 0 0" + "\n"
                        self.report({'INFO'}, 'Copied <trigger> to clipboard!')
                    return {'FINISHED'}
        else:
            return {'FINISHED'}
 
class panel1(bpy.types.Panel):
    bl_idname = "panel.panel1"
    bl_label = "Procedural Bones"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = 'Β L Λ Ζ Ξ'
    
    def draw(self, context):
        result = main(context)   
        layout = self.layout
        scn = context.scene
        ob = bpy.context.object
        
        if ob is None:   
            row = layout.row()   
            row.label(text='Selected Armature: None')    
        else:
            if ob.type == 'ARMATURE':  
                pb = ob.pose.bones.get(scn.Controller)
                armature = ob.data
                                
                try:
                    parent = pb.parent.name
                except:
                    parent = ''
                
                row = layout.row() 
                row.label(text='Selected armature: ' + armature.name)
                
                layout.prop(scn, 'MyInt')
                arma = bpy.data.armatures.get(scn.arma_name)       
                
                layout.prop(scn, 'MyFloat')
                   
                row = layout.row()
                row.prop_search(scn, "Controller", armature, "bones")
                
                
                row = layout.row()
                row.label(text='Controller parent: ' + parent)     
                
                if result is not None:
                    row = layout.row()        
                    row.label(text='Controller rotation: ' + result[5])
                    
                    row = layout.row()        
                    row.label(text='Helper: '+result[3])
                    
                    row = layout.row()        
                    row.label(text='Helper parent: '+result[4])
                    
                    row = layout.row()        
                    row.label(text='Helper rotation: '+result[1])
                    
                    row = layout.row()        
                    row.label(text='Helper translation: '+result[0])
                else:
                    row = layout.row()        
                    row.label(text='Controller rotation: ')
                    
                    row = layout.row()        
                    row.label(text='Helper: ')
                    
                    row = layout.row()        
                    row.label(text='Helper parent: ')
                    
                    row = layout.row()        
                    row.label(text='Helper rotation: ')  
                    
                    row = layout.row()        
                    row.label(text='Helper translation: ')                
                                    
                row = layout.row()
                row.operator('blz.procedural', text='Copy <helper>').type = 'HELPER'
                
                row = layout.row()
                row.operator('blz.procedural', text='Copy <trigger>').type = 'TRIGGER'
            else:
                row = layout.row()   
                row.label(text='Selected Armature: None')                  
                
def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.MyInt = IntProperty(
        name = "AoI", 
        description = "Enter an integer",
        default = 90)
        
    bpy.types.Scene.MyFloat = FloatProperty(
        name = "Scale", 
        description = "Enter scale",
        default = 1.000)

    bpy.types.Scene.arma_name = bpy.props.StringProperty()
    bpy.types.Scene.Controller = bpy.props.StringProperty()    

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == '__main__':
    register()