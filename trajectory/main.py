import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from scipy import ndimage

def get_number(path):
	return int(path.stem.split("_")[1])

data_folder = Path("out")
npy_files = sorted(list(data_folder.glob("*.npy")), key=get_number)
all_coordinates = []

for file in npy_files:
	image = np.load(file)
	labeled, cnt_circle = ndimage.label(image)

	centre_coordinates = []

	for i in range(1, cnt_circle + 1):
		mask = labeled == i
		y, x = ndimage.center_of_mass(mask)
		centre_coordinates.append((x, y))

	all_coordinates.append(centre_coordinates)

first_frame = all_coordinates[0]
num_obj = len(first_frame)
trajectories = [[pt] for pt in first_frame] # хранит всегда три объекта(списка), куда добавляются корды точек
prev_points = first_frame

for frame_index in range(1, len(all_coordinates)):
	cur_points = all_coordinates[frame_index]
	new_prev_points = [None] * num_obj

	for obj_index, prev_pt in enumerate(prev_points):
		px, py = prev_pt
		best_j = None
		best_dist = float("inf")

		for j, cur_pt in enumerate(cur_points):
			cx, cy = cur_pt
			dist = np.hypot(cx - px, cy - py)
			if dist < best_dist:
				best_dist = dist
				best_j = j

		matched_point = cur_points[best_j]
		trajectories[obj_index].append(matched_point)
		new_prev_points[obj_index] = matched_point

	prev_points = new_prev_points

for i, trej in enumerate(trajectories):
	xs = [p[0] for p in trej]
	ys = [p[1] for p in trej]
	plt.plot(xs, ys)

plt.show()