try:
    import exif
except:
    raise Exception("missing library 'exif' or one of its dependancies\nrun 'pip install exif' to install")
import json
from tkinter import *  
try:
    from PIL import ImageFont, Image, ImageDraw, ImageTk
except:
    raise Exception("missing library 'PIL' or one of its dependancies\nrun 'pip install Pillow' to install") 
try:
    import clipboard
except:
    raise Exception("missing library 'clipboard' or one of its dependancies\nrun 'pip install clipboard' to install")
import platform


print("Path to image: ", end="")
l = input()
if platform.system() == "Darwin":
    input_image = l
    input_image = input_image.replace("\\","")
else:
    input_image = l[1:len(l)-1]
            
with open(input_image, 'rb') as image_file:
	exif_image = exif.Image(image_file)
face_rec_data = json.loads(exif_image.model)
root = Tk()
root.title("Click to Copy Names")
root.geometry('300x300')
def resize_image(event):
    global nheight, nwidth, img_to_draw, conversion_factor, new_width, new_height
    original_image2 = original_image_root.copy()
    new_width = event.width
    new_height = event.height
    canvas.config(width=new_width, height=new_height)
    canvas.delete("all")
    if new_height/new_width<=original_image2.size[1]/original_image2.size[0]:
        nheight = new_height
        nwidth = new_height*original_image2.size[0]/original_image2.size[1]
    else:
        nheight = new_width*original_image2.size[1]/original_image2.size[0]
        nwidth = new_width
    
    new_img=original_image2.resize((int(nwidth),int(nheight)))
    img_to_draw = ImageTk.PhotoImage(new_img) 
    canvas.create_image(0, 0, anchor=NW, image=img_to_draw)
    conversion_factor = [original_size[0]/nwidth,original_size[1]/nheight]
    for p in face_rec_data:
        canvas.create_rectangle(p[0][3]*(1/conversion_factor[0]),p[0][0]*(1/conversion_factor[1]), p[0][1]*(1/conversion_factor[0]), p[0][2]*(1/conversion_factor[1]), outline = "blue")

def clicked(object_pos,mouse):
    top,right,bottom,left = object_pos
    x,y = mouse
    if top<=y and y<=bottom and left <= x and x <= right:
        return True
    else:
        return False

def clear_rect():
    canvas.delete(info_screen)

def on_click(event):
    global info_screen
    for person in face_rec_data:
        if clicked(person[0],(event.x*conversion_factor[0],event.y*conversion_factor[1])):
            if clipboard.paste() == "":
                clipboard.copy(person[1])
            else:
                clipboard.copy(clipboard.paste()+", "+person[1])
            print(person[1])
            info_screen = canvas.create_rectangle(0,0, new_width, new_height, fill = "white")
            canvas.after(40,clear_rect)
            break

def keydown(event):
    global info_screen
    if str(event.char) == "q":
        print("quitting...")
        quit()
    elif str(event.char) == "r":
        clipboard.copy("")
        info_screen = canvas.create_rectangle(0,0, new_width, new_height, fill = "black")
        canvas.after(40,clear_rect)
        print("clipboard reset")

original_image_root = Image.open(input_image)
original_image = original_image_root.copy()
canvas = Canvas(root, height = 300, width=300, bg="black", highlightthickness=0)

image_to_draw = ImageTk.PhotoImage(original_image.copy())
canvas.pack(fill=BOTH, expand = YES)
canvas_image = canvas.create_image(0, 0, anchor=NW, image=image_to_draw)
original_size = original_image.size
canvas.bind('<Configure>', resize_image)
canvas.bind("<Button-1>", on_click)
root.bind("<KeyPress>", keydown)

root.mainloop()    

