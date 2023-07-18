import fitz
import numpy as np
import matplotlib.pyplot as plt
import json

line_lenght = 7
char_size = 65

with open('Sample\charactor_list.json') as file:
    char_list  = json.load(file)

pdf_file = fitz.open("./Sample/template.pdf")


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
        
        # enter new line
        if((i+1)%line_lenght==0):cursor_y += char_size

