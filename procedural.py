bl_info = {
    'name': 'Source Procedural Bone',
    'author': 'Β L Λ Ζ Ξ',
    'version': (0, 15),
    'blender': (2, 79, 0),
    'location': 'View3D > Tool Shelf > Β L Λ Ζ Ξ',
    'description': 'Get basepos & rotation values for procedural bones',
    'warning': '',
    'wiki_url': '',
    'category': 'Scene',
    }
    
import bpy
import math

def main(context):
    bone = bpy.context.active_pose_bone
    
    if bone is not None:
        if bone.parent:
        	parent = bone.parent.matrix.inverted_safe()
        	matrix = parent * bone.matrix
        else:
        	matrix = bone.matrix

        vectorRot = matrix.to_euler()
        vectorRot = [math.degrees(n) for n in vectorRot]
        vectorPos = matrix.to_translation().xyz

        stringRot = ' '.join(str(round(n, 6)) for n in vectorRot)
        stringPos = ' '.join(str(round(n, 6)) for n in vectorPos)
        
        try:
            return stringPos, stringRot, bone, bone.name, bone.parent.name
        except:
            return stringPos, stringRot, bone, bone.name, ''

class ProceduralBone(bpy.types.Operator):
    bl_idname = 'blz.procedural'
    bl_label = 'Pose Bone Transforms'
    bl_options = {'REGISTER', 'INTERNAL'}
    
    type = bpy.props.EnumProperty(
        name = 'Transform Type',
        items = [
            ('NAME', 'Name', ''),
            ('NAME + PARENT', 'Name + parent', ''),
            ('TRANSLATION', 'Translation', ''),
            ('ROTATION', 'Rotation', ''),
        ],
    )
	
    @classmethod
    def poll(cls, context):
        return context.mode == 'POSE'

    def execute(self, context):
        result = main(context)
        bone = result[2]

        if bone is None:
            self.report({'INFO'}, 'No active bone')
            return {'CANCELLED'}
            
        if self.type == 'ROTATION':
            context.window_manager.clipboard = result[1]
            self.report({'INFO'}, self.type.capitalize()+': '+result[1])
        elif self.type == 'TRANSLATION':
            context.window_manager.clipboard = result[0]
            self.report({'INFO'}, self.type.capitalize()+': '+result[0])
        elif self.type == 'NAME + PARENT':
            bone_name_parent = result[3].replace('ValveBiped.','') + ' ' + result[4].replace('ValveBiped.','')
            context.window_manager.clipboard = bone_name_parent
            self.report({'INFO'}, self.type.capitalize()+': '+ bone_name_parent)
        else:
            bone_name = result[3].replace('ValveBiped.','')
            context.window_manager.clipboard = bone_name
            self.report({'INFO'}, self.type.capitalize()+': '+ bone_name)
        
        return {'FINISHED'}

class ProceduralBonePanel(bpy.types.Panel):
    bl_label = 'Procedural Bones'
    bl_idname = 'OBJECT_PT_procedural'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Β L Λ Ζ Ξ'

    def draw(self, context):
        result = main(context)     
        layout = self.layout          
        ls = []
        
        for obj in bpy.data.objects:
            ls.append(obj.type)
        
        if 'ARMATURE' not in ls:    
            row = layout.row()        
            row.label(text='Armature not found!', icon='ERROR')
        else:        
            if result is not None:
                row = layout.row()        
                row.label(text='Active Bone: '+result[3])
                
                row = layout.row()   
                row.operator('blz.procedural', text='Copy bone name').type = 'NAME'
                row.operator('blz.procedural', text='Copy bone + parent').type = 'NAME + PARENT'
                
                row = layout.row()        
                row.label(text='Translation: '+result[0])
                
                row = layout.row()        
                row.label(text='Rotation: '+result[1])
                
                row = layout.row()
                row.operator('blz.procedural', text='Copy translation').type = 'TRANSLATION'
                row.operator('blz.procedural', text='Copy rotation').type = 'ROTATION'
            else:
                row = layout.row()        
                row.label(text='Armature must be in pose mode!', icon='INFO')
        
def ProceduralBoneMenu(self, context):
    layout = self.layout
    layout.separator()
    
    layout.operator('blz.procedural', text='Copy bone name').type = 'NAME'
    layout.operator('blz.procedural', text='Copy name + parent').type = 'NAME + PARENT'
    layout.operator('blz.procedural', text='Copy translation').type = 'TRANSLATION'
    layout.operator('blz.procedural', text='Copy rotation').type = 'ROTATION'
    
def register():
    bpy.utils.register_class(ProceduralBone)
    bpy.utils.register_class(ProceduralBonePanel)
    bpy.types.VIEW3D_MT_pose_specials.append(ProceduralBoneMenu)

def unregister():
    bpy.utils.unregister_class(ProceduralBone)
    bpy.utils.unregister_class(ProceduralBonePanel)
    bpy.types.VIEW3D_MT_pose_specials.remove(ProceduralBoneMenu)

if __name__ == '__main__':
    register()