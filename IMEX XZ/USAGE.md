# Usage Guide

Welcome to the **Modular Multi-Extrusion 3D Printer**! This guide will walk you through the process of using the printer effectively, from assembling and configuring the hardware to creating stunning multi-color prints.

## Table of Contents

- [Getting Started](#getting-started)
- [Hardware Assembly](#hardware-assembly)
- [Firmware Setup](#firmware-setup)
- [Printing Modes](#printing-modes)
- [Maintenance](#maintenance)
- [Troubleshooting](#troubleshooting)

## Getting Started

Before you begin, make sure you have read the [README](README.md) and are familiar with the project's goals and features. If you're new to 3D printing, consider exploring some introductory resources.

## Hardware Assembly

Follow the detailed assembly instructions provided in the [Hardware Assembly Guide](HARDWARE_ASSEMBLY.md). Properly assemble the frame, attach the extruder modules, and set up the shared Y-axis motion system and print bed.

## Firmware Setup

1. **Download the Firmware:** Obtain the latest version of the printer firmware from the repository's `firmware` folder.

2. **Upload Firmware:** Use a compatible tool (e.g., Arduino IDE) to upload the firmware to your printer's microcontroller. Refer to the [Firmware Installation Guide](FIRMWARE_INSTALLATION.md) for detailed steps.

3. **Calibration:** Once the firmware is uploaded, follow the calibration instructions in the [Calibration Guide](CALIBRATION.md) to ensure accurate extrusion and printing.

## Printing Modes

### Single Extrusion Mode

1. **Load Filament:** Load the desired filament into the active extruder.
2. **Import G-code:** Prepare your 3D model and generate G-code using your preferred slicing software.
3. **Start Printing:** Use the printer's interface to start the printing process. The active extruder will lay down the model layer by layer.

### Multi-Extrusion Mode

1. **Select Extruders:** Choose the extruders you want to use for multi-color or multi-material printing.
2. **Modify G-code:** Use G-code commands for extruder selection during different segments of the print.
3. **Start Printing:** Initiate printing as usual, and the firmware will handle the coordinated extrusion of multiple materials/colors.

### High-Speed Mode

1. **Enable High-Speed Mode:** Activate the high-speed mode through the printer's interface.
2. **Prepare G-code:** Adjust slicing settings for faster printing. Be cautious not to compromise quality.
3. **Start Printing:** Begin printing, and the printer will optimize motion to achieve higher speeds while maintaining acceptable quality.

## Maintenance

- Regularly clean the print bed and nozzles to prevent adhesion issues and blockages.
- Lubricate moving parts of the printer to ensure smooth motion.
- Inspect and tighten screws and connections to prevent loosening during operation.

## Troubleshooting

If you encounter issues during printing, consult the [Troubleshooting Guide](TROUBLESHOOTING.md) for common problems and solutions. If the issue persists, seek help from the [Community Forum](https://forum.modular3Dprinter.com) for assistance.

Remember, practice and experimentation will help you master the printer's capabilities and create amazing 3D prints. Happy printing!
