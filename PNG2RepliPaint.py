# PNG2RepliPaint

#########################
FILENAME = "rick.png"
IMAGE_SIZE = 18
#########################

import os
from PIL import Image
import math

COLOR_PALETTE = [
	(0xDF, 0xE9, 0xF5), (0x69, 0x75, 0x94), (0x10, 0x15, 0x17), (0xF7, 0xAA, 0xA8),
	(0xD4, 0x68, 0x9A), (0x78, 0x2C, 0x96), (0xE8, 0x35, 0x62), (0xF2, 0x82, 0x5B),
	(0xFF, 0xC7, 0x6E), (0x88, 0xC4, 0x4D), (0x3F, 0x9E, 0x59), (0x36, 0x34, 0x61),
	(0x48, 0x54, 0xA7), (0x71, 0x99, 0xD9), (0x9E, 0x52, 0x52), (0x4D, 0x25, 0x35)
]

def closest_color(rgb):
	r, g, b = rgb
	min_distance = float('inf')
	closest_index = -1
	for i, (pr, pg, pb) in enumerate(COLOR_PALETTE):
		distance = math.sqrt((r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2)
		if distance < min_distance:
			min_distance = distance
			closest_index = i
	return closest_index + 1

def process_image(file_path, grid_size=16):
	image = Image.open(file_path).convert('RGB')
	image = image.resize((grid_size, grid_size), Image.LANCZOS)
	color_grid = []

	for y in range(grid_size):
		row = []
		for x in range(grid_size):
			rgb = image.getpixel((x, y))
			color_id = closest_color(rgb)
			row.append(color_id)
		color_grid.append(row)

	return color_grid

def find_rects(color_grid):
	grid_size = len(color_grid)
	visited = [[False] * grid_size for _ in range(grid_size)]
	rects = []

	for y in range(grid_size):
		for x in range(grid_size):
			if not visited[y][x]:
				color_id = color_grid[y][x]
				rect_width, rect_height = 1, 1

				while x + rect_width < grid_size and all(color_grid[y][x + w] == color_id for w in range(rect_width)):
					rect_width += 1

				while y + rect_height < grid_size and all(color_grid[y + h][x:x + rect_width] == [color_id] * rect_width for h in range(rect_height)):
					rect_height += 1

				for yy in range(y, y + rect_height):
					for xx in range(x, x + rect_width):
						visited[yy][xx] = True

				rects.append((x, y, rect_width, rect_height, color_id))

	return rects

def save_color_grid(color_grid, output_filename):
	rects = find_rects(color_grid)
	with open(output_filename, "w+") as f:
		f.write("return (")
		first = True
		for rect in rects:
			x, y, width, height, color_id = rect
			f.write(f'{"" if first else " or "}(x>={x} and y>={y} and x<{x+width} and y<{y+height} and {color_id})')
			first = False
		f.write(") or 0")

if __name__ == "__main__":
	input_filename = FILENAME
	output_filename, _ = os.path.splitext(input_filename)

	grid_size = IMAGE_SIZE
	color_grid = process_image(input_filename, grid_size)
	save_color_grid(color_grid, output_filename + ".pnt")