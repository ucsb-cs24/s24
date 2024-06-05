# VoxHop Map Viewer

You can use this voxel viewer in a web browser to visualize a map file.  Open
`index.html` in the browser of your choice, then use the file input in the top
right corner to load the `.vox` file you want to see.

If you want to visualize a point, you can use the Source, Destination, and Extra
fields to place a colored marker on the map.

To see a path, set the Source coordinate to the source of the path, then enter
the path in the bottom bar. The path will appear on the map, and the viewer will
make sure that the path is valid.  The results of this validation show up in the
bottom left.

If your markers or your path are hard to see - if they're underground, for
example - you can use the Clip fields to hide parts of the map.  Only voxels
with coordinates `min <= coord <= max` are displayed.
