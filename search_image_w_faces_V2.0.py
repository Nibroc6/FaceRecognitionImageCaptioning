#Master_Settings

batch_size = 20

#-------------------------------------------
batch_size = 20

try:
    from exif import Image as eImage
except:
    raise Exception("missing library 'exif' or one of its dependancies\nrun 'pip install exif' to install")
import json
try:
    import face_recognition
except:
    raise Exception("missing library 'face_recognition' or one of its dependancies\ngo to 'https://pypi.org/project/face-recognition/#Installation' for installation instructions")
try:
    import numpy as np
except:
    raise Exception("missing library 'numpy' or one of its dependancies\nrun 'pip install numpy' to install")
import pickle
import platform
print(platform.system())
try:
    from termcolor import cprint
except:
    raise Exception("missing library 'termcolor' or one of its dependancies\nrun 'pip install termcolor' to install")
try:
    from colorama import just_fix_windows_console
    just_fix_windows_console()
except:
    raise Exception("missing library 'colorama' or one of its dependancies\nrun 'pip install colorama' to install")




cprint("Save with same name? (y/n): ","yellow",end="")
show = input("")
if show.lower() in ["y","yes","true","1","ye","es","t","tr"]:
    same_name = True
else:
    same_name = False
 
#load data
cprint("loading face data...","magenta")
with open('face_data.pkl', 'rb') as f:
   known_face_encodings, known_face_names = pickle.load(f)
cprint("done","green")

#init vars
images = []
l=""
batch = 0
outputs = []
c = 0

#command input
while True:
    cprint("Image (h for all commands): ","yellow",end="")
    l = input("")
    if l == "s":
        break
    elif l == "rff":
        with open('input.txt') as f:
            lines = f.readlines()
        lines[len(lines)-1] = lines[len(lines)-1]+" "
        for d in lines:
            if platform.system() == "Darwin":
                images.append(d[0:len(d)-1])
                images[len(images)-1] = images[len(images)-1].replace("\\","")
            else:
                images.append(d[1:len(d)-2])
            cprint(images[len(images)-1],"blue")
    elif l == "h":
        cprint("""Commands:
s: stop getting file names and run face recognition
h: help
rff: import all files in 'input.txt' in the format \"<full file path here>\" (seperated by newlines)
\"full file path here>\": import file""","light_green")
    else:
        if platform.system() == "Darwin":
            images.append(l)
            images[len(images)-1] = images[len(images)-1].replace("\\","")
        else:
            images.append(l[1:len(l)-1])
        cprint(images[len(images)-1],"blue")
        
        

#little more var init
tot = len(images)

#iterate through all images
for input_image in images:
    c += 1
    cprint(str(c)+" of "+str(tot),"light_magenta")
    try: #make sure we don't end the program if something goes wrong
        #find face locations    
        cprint("loading image to recognise...","magenta")
        unknown_image = face_recognition.load_image_file(input_image)
        cprint("done","green")
        cprint("finding faces","magenta")
        # Find all the faces and face encodings in the unknown image
        face_locations = face_recognition.face_locations(unknown_image)
        cprint("done","green")
        cprint("loading found faces","magenta")
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
        cprint("done","green")


        # Create an exif image
        cprint("initilizing exif","magenta")
        with open(input_image, 'rb') as image_file:
            exif_image = eImage(image_file)
        faces_found = []
        cprint("done","green")
        
        
        cprint("recognising faces","magenta")
        # Loop through each face found in the unknown image
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            cprint("matched "+name,"cyan")
            faces_found.append([[top,right,bottom,left],name])
            
        exif_image.model = json.dumps(faces_found)
        #print(exif_image.model)
        cprint("done","green")
        

        # Display the resulting image
        outputs.append((exif_image,input_image))
        # You can also save a copy of the new image to disk if you want by uncommenting this line
        # pil_image.save("image_with_boxes.jpg")
        
    except Exception as e: #tell the user something went wrong
        cprint("error","red")
        cprint(e,"red")
        
        
    batch += 1#iterate batch item num
    if batch == batch_size:#if the current batch num is the same as the batch size, save images
        cprint("Saving","magenta")
        for o in outputs:
            t = o[1]
            if same_name:
                fname=t
            else:
                fname = t[0:t.rfind(".")]+"_FaceRecExifed"+t[t.rfind("."):]
            cprint(fname,"blue")
            with open(fname, 'wb') as new_image_file:
                new_image_file.write(o[0].get_file())
        outputs = []
        batch = 0
        

cprint("Saving","magenta")
for o in outputs:
    t = o[1]
    if same_name:
        fname=t
    else:
        fname = t[0:t.rfind(".")]+"_FaceRecExifed"+t[t.rfind("."):]
    cprint(fname,"blue")
    with open(fname, 'wb') as new_image_file:
        new_image_file.write(o[0].get_file())
