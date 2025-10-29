Very crude simulation of CGoL with 2 grids.

Independent Grid:
Runs CGoL normally with no changes
Displayed in blue

Dependent Grid:
Treats both Independent Grid and itself as neighbors
Displayed in red

If grids overlap, the cell will be displayed in purple.

Display is very crudely done with an array of turtle objects and displays through VNC

As an artifact of planned data collection, all grids are dumped to console as they're generated

grid_state.json can be used to import pre-made grids to test specific interactions.
If it is renamed or deleted the program will instead generate a grid randomly.
