"""
This module contains functions for G-code generation.

Author: Your Name
Date: Date Created

Include additional information about the module's purpose and usage here.
"""

import numpy as np
from stl import mesh

# Define the STL file path as a constant (uppercase naming style)
STL_FILE_PATH = (
    '/workspaces/IMEX-Independent-Multi-Extrusion-3D-printer-/slicer/'
    'Stanford_Bunny_sample.stl'
)

# Load the STL file
MESH_DATA = mesh.Mesh.from_file(STL_FILE_PATH)

# Define slicing parameters
LAYER_HEIGHT = 0.2  # Layer height in millimeters

# Calculate the number of layers
MAX_Z = np.max(MESH_DATA.vectors[:, :, 2])  # Access z-coordinates of all vertices
MIN_Z = np.min(MESH_DATA.vectors[:, :, 2])
NUM_LAYERS = int((MAX_Z - MIN_Z) / LAYER_HEIGHT)

# Define G-code parameters
EXTRUSION_WIDTH = 0.4  # Extrusion width in millimeters
PRINT_SPEED = 50  # Print speed in millimeters per second

# Create an empty G-code string
GCODE = []

# Loop through each layer
for LAYER in range(NUM_LAYERS):
    # Calculate the current layer height
    CURRENT_Z = MIN_Z + LAYER * LAYER_HEIGHT

    # Create a new layer in the G-code
    GCODE.append(
        f"; Layer {LAYER + 1}, Z = {CURRENT_Z:.2f} mm"
    )
    GCODE.append(
        f"G1 Z{CURRENT_Z:.2f} F{PRINT_SPEED}"
    )

    # Loop through each triangle in the mesh
    for TRIANGLE in MESH_DATA.vectors:
        # Get the z-coordinates of the triangle's vertices
        TRIANGLE_Z = TRIANGLE[:, 2]

        # Calculate the min and max z-coordinates of the triangle
        MIN_Z_TRIANGLE = min(TRIANGLE_Z)
        MAX_Z_TRIANGLE = max(TRIANGLE_Z)

        # Check if the triangle intersects with the current layer
        if MIN_Z_TRIANGLE <= CURRENT_Z <= MAX_Z_TRIANGLE:
            # Calculate the area of the triangle (cross product method)
            A, B, C = TRIANGLE[0], TRIANGLE[1], TRIANGLE[2]
            AB = B - A
            AC = C - A
            AREA = 0.5 * np.linalg.norm(np.cross(AB, AC))

            # Calculate the extrusion length based on layer height and triangle area
            EXTRUSION_LENGTH = LAYER_HEIGHT * AREA
            # Calculate the extrusion feedrate (speed)
            EXTRUSION_FEEDRATE = PRINT_SPEED * EXTRUSION_WIDTH / EXTRUSION_LENGTH

            # Create G-code for moving to the triangle's starting point
            for VERTEX in TRIANGLE:
                GCODE.append(
                    f"G1 X{VERTEX[0]:.2f} Y{VERTEX[1]:.2f} Z{CURRENT_Z:.2f} F{PRINT_SPEED}"
                )

            # Create G-code for extruding along the triangle edges
            for I in range(3):
                NEXT_VERTEX = (I + 1) % 3
                GCODE.append(
                    f"G1 X{TRIANGLE[I][0]:.2f} Y{TRIANGLE[I][1]:.2f} Z{CURRENT_Z:.2f} "
                    f"E{EXTRUSION_LENGTH:.2f} F{EXTRUSION_FEEDRATE:.2f}"
                )

# Save the G-code to a file
with open('output.gcode', 'w', encoding='utf-8') as GCODE_FILE:
    GCODE_FILE.write('\n'.join(GCODE))

print('G-code generation complete. Output saved to "output.gcode".')
