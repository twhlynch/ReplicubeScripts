# OBJ2RepliCube

#########################
FILENAME = "dragon.obj"
AREA_SIZE = 16
#########################

import os

def read_vertices(file_path):
	vertices = []
	with open(file_path, 'r') as file:
		for line in file:
			if line.startswith('v '):
				parts = line.split()
				x, y, z = map(float, parts[1:4])
				vertices.append((x, y, z))

	if vertices:
		center_x = sum(v[0] for v in vertices) / len(vertices)
		center_y = sum(v[1] for v in vertices) / len(vertices)
		center_z = sum(v[2] for v in vertices) / len(vertices)

		vertices = [(x - center_x, y - center_y, z - center_z) for x, y, z in vertices]

		max_extent = max(
			max(abs(x) for x, _, _ in vertices),
			max(abs(y) for _, y, _ in vertices),
			max(abs(z) for _, _, z in vertices),
		)

		if max_extent > 0:
			vertices = [(x / max_extent, y / max_extent, z / max_extent) for x, y, z in vertices]
	
	return vertices

def voxelize(vertices, grid_size):

	voxel_grid = [[[False for _ in range(grid_size)] for _ in range(grid_size)] for _ in range(grid_size)]

	for x, y, z in vertices:
		i = int((x + 1) * (grid_size - 1) / 2)
		j = int((y + 1) * (grid_size - 1) / 2)
		k = int((z + 1) * (grid_size - 1) / 2)
		voxel_grid[i][j][k] = True

	def has_all_neighbors(i, j, k):
		neighbors = [
			(i - 1, j, k), (i + 1, j, k),
			(i, j - 1, k), (i, j + 1, k),
			(i, j, k - 1), (i, j, k + 1),
		]
		return all(0 < ni < grid_size - 1 and 0 < nj < grid_size - 1 and 0 < nk < grid_size - 1 and voxel_grid[ni][nj][nk] for ni, nj, nk in neighbors)

	for i in range(grid_size):
		for j in range(grid_size):
			for k in range(grid_size):
				if voxel_grid[i][j][k] and has_all_neighbors(i, j, k):
					voxel_grid[i][j][k] = False

	return voxel_grid

if __name__ == "__main__":
	input_filename = FILENAME
	output_filename, _ = os.path.splitext(input_filename)

	vertices = read_vertices(input_filename)

	area_size = AREA_SIZE
	grid_size = area_size * 2

	voxels = voxelize(vertices, grid_size)
	pixels = [[any(y_list) for y_idx, y_list in enumerate(x_list) if y_idx % 2 == 0] for x_idx, x_list in enumerate(voxels) if x_idx % 2 == 0]

	with open(output_filename + ".vox", "w+") as f:
		f.write("return (")

		first = True
		for i, j, k in [(i, j, k) for i in range(grid_size) for j in range(grid_size) for k in range(grid_size) if voxels[i][j][k]]:
			x, y, z = i - area_size, j - area_size, k - area_size
			f.write(f'{'' if first else ' or '}(x=={x} and y=={y} and z=={z})')
			first = False

		f.write(") and 1")