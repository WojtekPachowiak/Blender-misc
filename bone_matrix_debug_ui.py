import bpy
import blf
import time

class DrawingClass:
    def __init__(self, context):
     
        self.handle = bpy.types.SpaceView3D.draw_handler_add(
                   self.draw_text_callback,(context,),
                   'WINDOW', 'POST_PIXEL')

    def draw_text_callback(self, context):
        font_id = 0  # XXX, need to find out how best to get this.

        # draw some text
        v_width, v_height = get_viewport_res()
        
        
        blf.size(font_id, 8,100)
        blf.color(font_id,1,1,1,1)
        blf.enable(font_id, blf.WORD_WRAP)
        blf.word_wrap(font_id, 1000)

        text = ""
        
        if bpy.context.active_pose_bone != None:
            s = \
f"""PoseBone.matrix
{mat_to_string(bpy.context.active_pose_bone.matrix)}

PoseBone.matrix_basis
{mat_to_string(bpy.context.active_pose_bone.matrix_basis)}

PoseBone.matrix_channel
{mat_to_string(bpy.context.active_pose_bone.matrix_channel)}

"""
            text += s
        
        if bpy.context.active_bone != None:
            s = \
f"""EditBone.matrix
{mat_to_string(bpy.context.active_bone.matrix)}

"""
            text += s
        
        if text == "":
            text = "No bone selected"
        
        text_width, text_height = blf.dimensions(font_id, text)
        blf.position(font_id, 10, text_height+20, 1)
        
        blf.draw(font_id,text)
        
        
        
        
    def remove_handle(self):
         bpy.types.SpaceView3D.draw_handler_remove(self.handle, 'WINDOW')

def mat_to_string(mat):
    size = len(mat)
    return str(mat).replace(f"<Matrix {size}x{size}","").replace(">","").replace(" ","")

def get_viewport_res():
    for a in bpy.context.screen.areas:
        if a.type == 'VIEW_3D':
            for r in a.regions:
                if r.type == 'WINDOW':
                    return r.width,r.height

bpy.app.driver_namespace["dc"] = DrawingClass(bpy.context)
