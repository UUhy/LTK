# LTK
Lithography Took Kit for KLayout GDSII editor. This kit contains PCells and macros to facilitate layout preparations for photolithography and electron beam lithography.

## Macros
* Digitize Graph: Converts the layout of a graph into a CSV file
* Image to GDS Converter: Converts an image into a binary GDSII layout
* Save to SVG: Save the active cell as an SVG file
* Text to GDS: Converts a tab separated value (tsv) file of text to GDS
* Write Time Calculator: Estimates the write time for electron beam lithography
* Reload LTK


## PCell
* Alignment Mark
* Shape: Checkerboard
* Shape: Circle
* Shape: Cross
* Shape: Ring
* Shape: Vernier
* Shape: Wafer
* Jeol: Dose Series
* Jeol: Field Markers
* Jeol: JBX-5500FS Cassette

## Known Problems
Does not work on Windows because KLayout Python cannot load matplotlib due to circular imports.
No idea how to solve this problem.

The LTK library loads before a layout is loaded. PCells that require layer data such as
Jeol - Dose Series and Jeol - Field Markers will fail to load properly. To fix this,
the user needs to run the Macro called Reload LTK.
