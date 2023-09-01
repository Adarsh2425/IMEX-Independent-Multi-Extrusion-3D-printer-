# 3D Printer Slicer

## Step 1: Anatomy of a Slicer

A 3D printer makes objects with stacks of two-dimensional layers. In general, these layers are made up of two parts: perimeters and infill. The perimeters form the hard shell of the part, while the infill is a pattern full of mostly air to support the part while saving material. Flat top and bottom areas of a part have solid infill patterns, forming the shell when perimeters aren't enough.

To generate these structures, the slicer follows a pretty simple pattern. First, it takes cross-sections of the model at regular intervals aligned with the layers. Next, it offsets the cross-section several times to generate each of the outer walls. Finally, the slicer overlays the infill pattern inside of each layer. (This infill process can get very complex, so we don't cover it in this guide.)

After each layer is generated, the slicer figures out how much plastic the printer needs to use for each step, then generates the instructions as a G-Code file (.gco or .gcode).

## Step 2: Set Up Your Environment

The most important part of any programming project is setting up your development environment. We're using Autodesk Dynamo Studio 2017, which is a visual programming environment with a built-in geometry library and visualizer. Dynamo is free for students or for a 30-day trial, and can be downloaded [here](https://www.autodesk.com/products/dynamo-studio/overview).

Once you have Dynamo downloaded, create a new file and navigate to Packages > Search for a Package in the top bar. You will need to download the MeshToolkit package, which is a fully-featured mesh manipulation library written by the Dynamo Team. You will also need my DynamoClipper package, which handles polygon offsetting, an important part of the slicing process.

If you can't get or would rather not use Dynamo, you can still follow this guide. The geometry commands in Dynamo are fairly general, and most programming languages should have a geometry library that will do the same things. Make sure you have mesh manipulation and polygon offsetting capabilities.

## Step 3: Organize Your Inputs

In general, this tutorial will be pretty organic in the way we build our code, but I like to keep all of my "tweakables" at the far left of the canvas. That way, it's easy for me to adjust the settings of my code without hunting through the entire file. At the absolute simplest, we need four options to plan our paths:

- **Layer Height**: the spacing between our two-dimensional layers
- **Number of Perimeters**: the number of solid shells on the outside of our part
- **Extrusion Width**: how wide to make an individual wall of the part

We also need a few more settings for later parts of the process:

- **Filament Diameter**: the width of the filament we're using
- **Print Speed**: how fast to move while printing, in mm/minute
- **Print Temperature**: how hot the nozzle needs to be, in Celsius
- **Output File Name**: the name of the final file of printing instructions (G-Code)

In Dynamo, the easiest way to do this is to double-click and create a code block with all the settings. However, you can get much fancier with sliders under the Core > Input menu.

We also have to import our file to slice. For this, we make a File Path node and connect it to a Mesh.ImportFile node. If you select an STL file in the File Path node, you should see your design appear in the viewer.

## Step 4: Adjust Your Model

Inside the MeshToolkit > Mesh menu, you can select the Translate, Scale, and Rotate nodes to manipulate the mesh. The bottom of the model should be on the viewer plane, and the "up" direction should be upward on your screen.

At this point, you'll probably want to right-click each of the Mesh nodes except for the last one and deselect Preview. By default, Dynamo shows the result of every node, but usually we don't want to see the intermediate geometries. From now on, we'll leave the Preview decisions to you.

## Step 5: Build the Layer Planes

To build the plane for each layer, we will use the Plane.ByOriginNormal node. For this node, we need an "origin" point for each plane to pass through, as well as a "normal" vector perpendicular to the plane. Since all of our planes are parallel to the build platform, we can just use the Z axis vector for each plane's normal.

We create a Point.ByCoordinates node for the origins of our planes. This node requires XYZ coordinates to construct a point. The X and Y coordinates don't matter, so we can just set both of them to zero. For the Z coordinate, we use Dynamo's built-in "range" feature. This feature has the format "start..end..step," and makes the list of numbers "start, start + step, start + 2*step, ..." which goes up to but not past "end." In this case, we need to start at one layer height above the bed, then go up one layer height at a time, but not past the top of the mesh.

To figure out the top and bottom of the mesh, we first grab the list of triangles in the mesh with Mesh.Triangles, then create a Polysurface container to hold them all, and finally compute the bounding box around the Polysurface (which is exactly around the mesh). By using the MinPoint and MaxPoint of this bounding box, we can find the top and bottom of the mesh, and use those in our code.

**WARNING**: In the last step, you ought to have moved the mesh so that the bottom of the mesh was at Z = 0. If you didn't, the code in this step might leave you printing in midair, or otherwise crash your print nozzle into the bed. Double-check that MinPoint.Z is indeed 0, and adjust if necessary.

## Step 6: Compute Layer Intersections

Next, we need to find the ring around the outside of the part where each layer plane intersects the mesh. In Dynamo, this step is very easy. With the MeshToolkit plugin, there is a Mesh.Intersect node which generates PolyCurve objects for each layer. By grabbing the StartPoint of each curve in the PolyCurves, we can make a series of Polygons for each layer. (We know that the intersection has to be polygons because the mesh is all triangles, so the intersection has to be straight lines.)

## Step 7: Build the Part Walls

Now that we have the outside of the part on each layer, we can work on building the part walls. Since we don't want just one wall centered on the part boundary, we can't just use the Polygons from the last step. We need an outer wall which has one edge on the boundary, and maybe more walls inside of that.

This means we have to implement a process called polygon offsetting. Dynamo doesn't do this by default, and it's a bit too complex to do ourselves in this tutorial. Thankfully, there is a library called Clipper which can be used from a C++ or C# program to do offsetting. Dynamo allows users to use custom C# libraries and use them in Dynamo, so you might think that we could just import Clipper and move on.

In a C#, environment, the translation
. Dynamo allows users to use custom C# libraries and use them in Dynamo, so you might think that we could just import Clipper and move on.

In a C# environment, the translation between the two formats is easy. Earlier, we downloaded the DynamoClipper package that I wrote for just this purpose. This package gives us one node, OffsetPolys, which does exactly what we need: offset a polygon by a certain amount. In this case, the first layer needs to be one half of the extrusion width inward (so that the outer edge is on the original polygon boundary), and every edge after that is one extrusion width inward (just touching the next-outermost one). We use the range syntax again, noting that all of the values are negative so that we offset inward instead of outward.

You'll notice that there is one bit of special Dynamo magic happening in this step. We need to do every layer and every offset, so we need to move through two separate lists. The way to do this in Dynamo is using the List.CartesianProduct node and placing the OffsetPolys node as the input function. This will apply OffsetPolys for every single combination of layer and offset, which is exactly what we want.

(NOTE: If you aren't using Dynamo, you might be able to use Clipper in your own language. You also might be able to find a different library for offsetting in your language; a quick web search for "polygon offsetting " will probably turn something up.)

## Step 8: Calculate Extrusion Values

The 3D printer needs to know exactly how much plastic to put down for each movement. On almost every hobbyist printer, this corresponds to the length of filament to push out. In this step, we calculate those values so we can pass them to the printer.

First, we take all the Points in all the Polygons and put them into one long list with the Flatten node. This keeps the same order of Points inside one Polygon, and keeps the same order of Polygons. Since we built our polygons upward, this is just fine by us. We create a copy of this list, but throw away the first point to get the end points of each move (and the first point doesn't need an extrusion value anyway, since the first move is just the printer going to where the part is).

There are a lot of ways to think about the shape of the plastic for each move, but for simplicity, we choose the easiest: a rectangular box from the first point to the second, as tall as the layer and as wide as the extrusion width. When we multiply the width times the height times the length of the move, we get the volume of plastic. Then we can divide this by the cross-section of the filament to get the length of filament we need.

## Step 9: Create the G-Code File Beginning

We're done with all the fun stuff, so now we have to put it into the right file format. 3D printers use a format called G-Code, which contains all the instructions to print a part. The beginning of the G-Code file has a lot of important settings and instructions that can be hard to get right, and a lot of it depends on your specific printer. At the very least, you need to home the printer, turn on the heaters, and set the proper units at the beginning of a print. In our case, we also need to set the E commands to relative with the command "M83" (most slicers use absolute E values, which is more accurate but harder to code, especially in Dynamo).

One way to get the G-Code settings right for your printer is to take a look at the G-Code file generated by a slicer you already use. Many slicers have a "verbose" option that adds comments to the G-Code file explaining each command, or alternatively, you can use a G-Code reference like [this one](https://reprap.org/wiki/G-code).

The other important thing to do at the beginning of the file is to add in the first move. Moves in G-Code use the "G0" or "G1" command, and 3D printers don't distinguish between the two. Since this particular move just gets us to the part, it has no E value, and we call it a "travel" move. Since this is the first real move in the part, we also use it to set the speed by adding an "F" (for "feedrate," another word for speed), followed by the speed in mm/min. Later moves inherit this speed, so we only need to specify a speed when it changes.

Store every command in its own element in a list; later these will become the lines of the G-Code text file.

## Step 10: Write the Printing and End G-Code

The main body of the G-Code file consists of printing moves, which follow the same pattern as the travel move in the last step. Of course, this time we include the E values and not the F value. Make sure that you take points from the list where we dropped the first element, or the E values won't match up with the moves themselves, and your part will not turn out well.

Your print probably needs some G-Code commands at the end, too. At the very least, these should include turning off the heaters, but there might also be commands to partially home the printer, turn off fans, or other operations. Again, check a G-Code file from another slicer and figure out what's important.

Finally, use a List.Join node to combine the beginning, middle, and end into a single list. A String.Join node will join them with "\n" (the "new line" character), and the File.WriteText function will create your output G-Code file.

## Step 11: Test Your File!

There are two basic ways to test your G-Code file on your 3D printer. The easiest is using a 3D printing host program (Repetier-Host, Cura, MatterControl, etc.) to stream the file to your printer. If your printer has an SD card reader, you can also place the G-Code file on an SD card and have the printer run straight from the card.

Since we don't have infill or top/bottom solid layers, be careful with the model you choose to print. Drastic overhangs and large flat horizontal regions will not turn out well with the slicer we built here. For best results, I recommend using a part designed for "spiral vase" prints, as this is essentially the printing method we built into our slicer.

## Step 12: Explore Further

The slicer we built was very basic, leaving a lot of room for further development. Probably the first changes you might consider would be to add infill and support material to allow more designs to be printed, or heated bed controls to handle higher-temperature filaments like ABS.

If you're in need of more inspiration, you might dive into the source code for the excellent open-source slicers out there. Slic3r, Cura, and MatterSlice are all open-source and widely-used slicers. Maybe you might even have a new idea for a feature or improvement, and contribute to one of the projects!
