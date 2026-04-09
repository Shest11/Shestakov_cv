import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.io import imread
from pathlib import Path

save_path = Path(__file__).parent

def count_holes(region):
    shape = region.image.shape
    new_image = np.zeros((shape[0] + 2, shape[1] + 2))
    new_image[1:-1, 1:-1] = region.image
    new_image = np.logical_not(new_image)
    labeled = label(new_image)
    return np.max(labeled) - 1

def count_lines(region):
    shape = region.image.shape
    image = region.image
    vlines = (np.sum(image, 0) / shape[0] == 1).sum()
    hlines = (np.sum(image, 1) / shape[1] == 1).sum()
    return vlines, hlines

def symmetry(region):
    image = region.image.astype(int)
    index = image.shape[1] // 2

    part1 = image[:, :index]
    part2 = image[:, index:]

    part2_mirrored = np.fliplr(part2)

    min_index = min(part1.shape[1], part2.shape[1])

    part1 = part1[:, :min_index]
    part2_mirrored = part2_mirrored[:, :min_index]
    diff = np.abs(part1 - part2_mirrored).mean()
    return diff


def extractor(region):
    cy, cx = region.centroid_local
    cy /= region.image.shape[0]
    cx /= region.image.shape[1]

    perimeter = region.perimeter / region.image.size

    holes = count_holes(region)

    v, h = count_lines(region)
    v /= region.image.shape[1]
    h /= region.image.shape[0]

    eccentricity = region.eccentricity

    aspect = region.image.shape[0] / region.image.shape[1]

    vertical_symmetry = symmetry(region)

    return np.array([region.area/region.image.size, cy, cx, perimeter, holes, v, h, eccentricity, aspect, vertical_symmetry])

def classificator(region, templates):
    features = extractor(region)
    result = ""
    min_d = 10 ** 16
    for symbol, t in templates.items():
        d = ((t - features) ** 2).sum() ** 0.5
        if d < min_d:
            result = symbol
            min_d = d
    return result

template = imread("alphabet-small.png")[:, :, :-1]
template = template.sum(2)
binary = template != 765.

labeled = label(binary)
props = regionprops(labeled)

templates = {}

for region, symbol in zip(props, ["8", "0",
                                  "A", "B", "1", "W",
                                  "X", "*", "/", "-"]):
    templates[symbol] = extractor(region)

image = imread("alphabet.png")[:, :, :-1]
abinary = image.mean(2) > 0
alabeled = label(abinary)
aprops = regionprops(alabeled)
result = {}
image_path = save_path / "out"
image_path.mkdir(exist_ok=True)

# plt.ion()
plt.figure(figsize=(5, 7))
for region in aprops:
    symbol = classificator(region, templates)
    if symbol not in result:
        result[symbol] = 0
    result[symbol] += 1
    plt.cla()
    plt.title(f"Class - {symbol}")
    plt.imshow(region.image)
    plt.savefig(image_path / f"image_{region.label}.png")

print(result)
plt.imshow(abinary)
plt.show()


