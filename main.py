##TODO:

##Completed:
# Basic CGoL implementation
# Create second grid which considers first grid as neighbors
# Graph visualization of living cells
# Create more complex display to show both grids layered
# Create a way to input/output grids as files

import random as r
import turtle as t
import json
import os

t.penup()
t.shape("square")
t.tracer(0, 0)
gridwidth = 25
gridheight = 25
indgrid = [0] * (gridwidth * gridheight)
depgrid = [0] * (gridwidth * gridheight)
## Set initial living cells
#living = [100, 125, 150]

def print_grid(grid, width):
    for i in range(0, len(grid), width):
        print(grid[i:i + width])
    print()

def save_grids_to_file(indgrid, depgrid, width, height, filename="grid_state.json"):
  grid_state = {
    "width": width,
    "height": height,
    "independent_grid": indgrid,
    "dependent_grid": depgrid
  }
  with open(filename, 'w') as f:
    json.dump(grid_state, f, indent=2)
  print(f"Grid states saved to {filename}")

def load_grids_from_file(filename="grid_state.json"):
  if not os.path.exists(filename):
    print(f"File {filename} not found. Using random initialization.")
    return None

  try:
    with open(filename, 'r') as f:
      grid_state = json.load(f)

    width = grid_state.get("width")
    height = grid_state.get("height")
    indgrid = grid_state.get("independent_grid")
    depgrid = grid_state.get("dependent_grid")

    if not all([width, height, indgrid, depgrid]):
      print(f"Error: Missing required fields in {filename}. Using random initialization.")
      return None

    expected_size = width * height
    if len(indgrid) != expected_size or len(depgrid) != expected_size:
      print(f"Error: Grid size mismatch in {filename}. Expected {expected_size} cells, got {len(indgrid)} and {len(depgrid)}. Using random initialization.")
      return None

    if not all(cell in [0, 1] for cell in indgrid + depgrid):
      print(f"Error: Grid cells must be 0 or 1 in {filename}. Using random initialization.")
      return None

    print(f"Grid states loaded from {filename}")
    print(f"Grid dimensions: {width}x{height}")

    return width, height, indgrid, depgrid

  except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON in {filename}: {e}. Using random initialization.")
    return None
  except Exception as e:
    print(f"Error loading {filename}: {e}. Using random initialization.")
    return None

def initialize_grid(grid, width, height, living):
  # to initialize a grid with random alive cells
  for i in range(width * 2 + 1):  # Set a block of alive cells
      index = r.randint(0, width * height - 1)
      grid[index] = 1
  for i in living:
    grid[i] = 1

def count_alive_neighbors(grid, width, height, index):
    row, col = divmod(index, width)
    alive = 0
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),         (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]

    for dr, dc in directions:
        r_, c_ = row + dr, col + dc
        if 0 <= r_ < height and 0 <= c_ < width:
            neighbor_index = r_ * width + c_
            alive += grid[neighbor_index]

    return alive

def count_alive_neighbors2(igrid, dgrid, width, height, index):
    row, col = divmod(index, width)
    alive = 0
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),         (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]
    for dr, dc in directions:
        r_, c_ = row + dr, col + dc
        if 0 <= r_ < height and 0 <= c_ < width:
            neighbor_index = r_ * width + c_
            alive += igrid[neighbor_index]
            alive += dgrid[neighbor_index]
    return alive

def update_life(grid, width, height):
    new_grid = grid[:]
    for i in range(len(grid)):
      alive_neighbors = 0
      if grid == indgrid:
        alive_neighbors = count_alive_neighbors(grid, width, height, i)
      elif grid == depgrid:
        alive_neighbors = count_alive_neighbors2(indgrid, depgrid, width, height, i)
      if grid[i] == 1:
        if alive_neighbors < 2 or alive_neighbors > 3:
          new_grid[i] = 0
      else:
        if alive_neighbors == 3:
          new_grid[i] = 1
    return new_grid

def cell_color(cell, grid1, grid2):
  color = "darkgray"
  if grid1[cell] == 1 and grid2[cell] == 0:
    color = "blue"
  if grid1[cell] == 0 and grid2[cell] == 1:
    color = "red"
  if grid1[cell] == 1 and grid2[cell] == 1:
    color = "purple"
  return color

def draw_grid(width, height, cell_size, xoffset, yoffset):
    for i in range(width * height):
        row, col = divmod(i, width)
        x, y = col * cell_size, row * cell_size
        t.goto(x + xoffset, y + yoffset)
        t.color(cell_color(i, indgrid, depgrid))
        t.stamp()

def run_step(gridwidth, gridheight):
  global indgrid
  global depgrid
  indgrid = update_life(indgrid, gridwidth, gridheight)
  print(f"Independent Step {step}:")
  print_grid(indgrid, gridwidth)
  depgrid = update_life(depgrid, gridwidth, gridheight)
  print(f"Dependent Step {step}:")
  draw_grid(gridwidth, gridheight, 20, -250, -235)
  print_grid(depgrid, gridwidth)
  t.update()

# Run simulation
loaded_state = load_grids_from_file("grid_state.json")

if loaded_state:
  gridwidth, gridheight, indgrid, depgrid = loaded_state
  print("Initial Independent Grid (loaded):")
  print_grid(indgrid, gridwidth)
  print("Initial Dependent Grid (loaded):")
  print_grid(depgrid, gridwidth)
else:
  initialize_grid(indgrid, gridwidth, gridheight, [])
  print("Initial Independent Grid:")
  print_grid(indgrid, gridwidth)

  initialize_grid(depgrid, gridwidth, gridheight, [])
  print("Initial Dependent Grid:")
  print_grid(depgrid, gridwidth)

wn = t.Screen()
wn.bgcolor("black")
for step in range(1, 101):
  t.ontimer(run_step(gridwidth, gridheight), 500 * (step + 1))
wn.mainloop()
