"""
This module contains functions for G-code generation.

Author: Your Name
Date: Date Created

Include additional information about the module's purpose and usage here.
"""

import numpy as np
from stl import mesh

# Define the STL file path
stl_file_path = '/workspaces/IMEX-Independent-Multi-Extrusion-3D-printer-/slicer/Stanford_Bunny_sample.stl'

# Load the STL file
mesh_data = mesh.Mesh.from_file(stl_file_path)

# Define slicing parameters
layer_height = 0.2  # Layer height in millimeters

# Calculate the number of layers
max_z = np.max(mesh_data.vectors[:, :, 2])  # Access z-coordinates of all vertices
min_z = np.min(mesh_data.vectors[:, :, 2])
num_layers = int((max_z - min_z) / layer_height)

# Define G-code parameters
extrusion_width = 0.4  # Extrusion width in millimeters
print_speed = 50  # Print speed in millimeters per second

# Create an empty G-code string
gcode = []

# Loop through each layer
for layer in range(num_layers):
    # Calculate the current layer height
    current_z = min_z + layer * layer_height

    # Create a new layer in the G-code
    gcode.append(f"; Layer {layer + 1}, Z = {current_z:.2f} mm")
    gcode.append(f"G1 Z{current_z:.2f} F{print_speed}")

    # Loop through each triangle in the mesh
    for triangle in mesh_data.vectors:
        # Get the z-coordinates of the triangle's vertices
        triangle_z = triangle[:, 2]
        
        # Calculate the min and max z-coordinates of the triangle
        min_z_triangle = min(triangle_z)
        max_z_triangle = max(triangle_z)

        # Check if the triangle intersects with the current layer
        if min_z_triangle <= current_z <= max_z_triangle:
            # Calculate the area of the triangle (cross product method)
            a, b, c = triangle[0], triangle[1], triangle[2]
            ab = b - a
            ac = c - a
            area = 0.5 * np.linalg.norm(np.cross(ab, ac))

            # Calculate the extrusion length based on layer height and triangle area
            extrusion_length = layer_height * area
            # Calculate the extrusion feedrate (speed)
            extrusion_feedrate = print_speed * extrusion_width / extrusion_length

            # Create G-code for moving to the triangle's starting point
            for vertex in triangle:
                gcode.append(f"G1 X{vertex[0]:.2f} Y{vertex[1]:.2f} Z{current_z:.2f} F{print_speed}")

            # Create G-code for extruding along the triangle edges
            for i in range(3):
                next_vertex = (i + 1) % 3
                gcode.append(f"G1 X{triangle[i][0]:.2f} Y{triangle[i][1]:.2f} Z{current_z:.2f} E{extrusion_length:.2f} F{extrusion_feedrate:.2f}")

# Save the G-code to a file
with open('output.gcode', 'w', encoding='utf-8') as gcode_file:
    gcode_file.write('\n'.join(gcode))

print('G-code generation complete. Output saved to "output.gcode".')
