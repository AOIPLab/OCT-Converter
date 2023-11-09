import os

import numpy as np
from tifffile import imwrite

from oct_converter.readers import E2E
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askdirectory()  # ask user for the directory of E2E files

f = []
n = []
slice_as_np_array = []

f = [os.path.join(dirpath, f) for (dirpath, dirnames, filenames) in os.walk(file_path) for f in filenames]  # get the file names

# get the file names without the .E2E extension
for i in range(0, len(f)):
    temp = f[i].split(".")
    n.append(temp[0])

# go through folder and save each as avi and png in the E2E folder
count = 0
for e2e_file in f:
    file = E2E(e2e_file)
    oct_volumes = (file.read_oct_volume())  # returns a list of all OCT volumes with additional metadata if available
    for volume in oct_volumes:
        # volume.peek(show_contours=True)  # plots a montage of the volume
        list_of_slices = volume.volume
        for i in range(0, len(list_of_slices)):
            slice_as_np_array.append(list_of_slices[i])
        # imwrite('multipage.tif', slice_as_np_array)
        imwrite('{}.tif'.format(n[count]), slice_as_np_array)
        slice_as_np_array = []
        # volume.save("{}.avi".format(n[count]))

    fundus_images = (file.read_fundus_image())  # returns a list of all fundus images with additional metadata if available
    for image in fundus_images:
        image.save("{}.png".format(n[count]))

    count = count + 1
