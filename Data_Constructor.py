import fitz
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from PIL import Image
import albumentations as Al


Augment = True
extranumber = 3
line_lenght = 7
char_size = 65

transform = Al.Compose([
    Al.Resize(width=char_size, height=char_size),
    Al.Rotate(25,p=0.75)
])

def create_dir(path, copy = 0):
    if(copy != 0):
        path+str(copy)
    if not os.path.exists("./Dataset_result/{}".format(path)):
        os.mkdir("./Dataset_result/{}".format(path))
    else:
        print("directory already created")
        exit(0)

with open('Sample\charactor_list.json') as file:
    char_list  = json.load(file)

pdf_file = fitz.open("./Sample/template.pdf")

directory_name = input("enter your dataset name : ")
# create directory
create_dir(directory_name)

for page_index in range(len(pdf_file)):
    cursor_x, cursor_y = 52,54
    labels = char_list["page"+str(page_index+1)]
    page = pdf_file[page_index]
    pix = page.get_pixmap()
    pix_arr = np.frombuffer(buffer=pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, -1))

    print(pix_arr.shape)
    plt.imshow(pix_arr)
    plt.show()
    #this code crop using manual approximation
    for i in range(len(labels)):
        #determine range of cropping
        factor = (i)%line_lenght
        cropped_pic = pix_arr[cursor_y:cursor_y+char_size,
                              cursor_x+char_size*factor:cursor_x+char_size*(factor+1)]
        # save original image in created directory
        create_dir(directory_name+"/"+labels[i])
        im = Image.fromarray(cropped_pic)
        im.save("./Dataset_result/"+directory_name+"/"+labels[i]+"/{}_0.jpeg".format(labels[i]))

        # Augment images
        if(Augment):
            # use albuments create new array and save it to directory
            for extra in range(extranumber-1):
                # Augment
                trans_pic = transform(image  = cropped_pic)
                # save augment image
                im = Image.fromarray(trans_pic["image"])
                im.save("./Dataset_result/"+directory_name+"/"+labels[i]+"/{}_{}.jpeg".format(labels[i],extra+1))
        # enter new line
        if((i+1)%line_lenght==0):cursor_y += char_size

