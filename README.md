# LTK
Lithography Took Kit for KLayout GDSII editor. This kit contains PCells and macros to facilitate layout preparations for photolithography and electron beam lithography.

## Macros
* Image to GDS Converter: Converts an image into a binary GDSII layout
* Save to SVG: Save the active cell as an SVG file
* Write Time Calculator: Estimates the write time for electron beam lithography
* Reload LTK


## PCell
* Alignment Mark
* Cross (Solid, Dashed)
* Checkerboard
* Vernier Scale
* Jeol - Dose Series
* Jeol - Field Markers

## Known Problems
The LTK library loads before a layout is loaded. PCells that require layer data such as
Jeol - Dose Series and Jeol - Field Markers will fail to load properly. To fix this,
the user needs to run the Macro called Reload LTK.
