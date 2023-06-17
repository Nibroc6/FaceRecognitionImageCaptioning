try:
    import face_recognition
except:
    raise Exception("missing library 'face_recognition' or one of its dependancies\ngo to 'https://pypi.org/project/face-recognition/#Installation' for installation instructions")
try:
    from PIL import Image, ImageDraw
except:
    raise Exception("missing library 'PIL' or one of its dependancies\nrun 'pip install Pillow' to install")
try:
    import numpy as np
except:
    raise Exception("missing library 'numpy' or one of its dependancies\nrun 'pip install numpy' to install")
from os import walk, listdir
import pickle
import platform
try:
    from termcolor import cprint
except:
    raise Exception("missing library 'termcolor' or one of its dependancies\nrun 'pip install termcolor' to install")
try:
    from colorama import just_fix_windows_console
    just_fix_windows_console()
except:
    raise Exception("missing library 'colorama' or one of its dependancies\nrun 'pip install colorama' to install")
    
    
cprint("Root Directory: ","yellow",end="")
l = input()
if platform.system() == "Darwin":
    root_dir = l
    root_dir = root_dir.replace("\\","")
else:
    root_dir = l[1:len(l)-1]
cprint(root_dir,"blue")
if platform.system() == "Windows":
    ss = "\\"
else:
    ss="/"
    
    
data_file = "face_data.pkl"
known_face_encodings = []
known_face_names = []
files = []
folders_raw = listdir(root_dir)
folders=[]

for raw in folders_raw:
    if raw.find(".")==-1:
        folders.append(raw)
cprint("Found the following folders to load from: "+str(folders),"blue")

for folder in folders:
    file_names_list = next(walk(root_dir+ss+folder), (None, None, []))[2]  
    for name in file_names_list:
        files.append(root_dir+ss+folder+ss+name)
        
        
def parse_name(p):
    p = p[p.rfind(ss)+1:p.rfind(".")]
    p = p.split("_")
    o = []
    for i in range(len(p)):
        if not p[i].isnumeric():
            o.append(p[i])
    p = o
    return " ".join(p[len(p)-1:])+" "+" ".join(p[:len(p)-1])
cprint("Reading images and learning to recognise them","magenta")
# Load pictures and learn how to recognize them.
for person in files:
    try:
        loaded_image = face_recognition.load_image_file(person)
        known_face_encodings.append(face_recognition.face_encodings(loaded_image)[0])
        known_face_names.append(parse_name(person))
        cprint("Learned "+parse_name(person),"blue")
    except:
        print("Non-fatal error while parsing "+parse_name(person))
cprint("Done learning","green")
cprint("Saving...","magenta") 
with open(data_file, 'wb') as f:
   pickle.dump([known_face_encodings,known_face_names], f)
cprint("Saved", "green")

