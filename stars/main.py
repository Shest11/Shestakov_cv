import numpy as np
from skimage.measure import label
from skimage.morphology import erosion, footprint_rectangle

image = np.load("stars.npy")
general_amt = label(image).max()

erosioned = erosion(image, footprint=footprint_rectangle((2, 2)))
labeled = label(erosioned)

print(general_amt - labeled.max())