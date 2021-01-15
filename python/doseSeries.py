# Dose Series PCell for Klayout
# Copyright (C) 2021  Long Chang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pya

class doseSeries(pya.PCellDeclarationHelper):
  '''
  Generates a dose series from the specified cell
    
  Parameters
  ---------
  layer : from interface
        The layer and datatype for the patterns
  cellName : from interface
        The name of the cell
  pitchX : from interface
        The horizontal space between each pattern
  pitchY : from interface
        The vertical space between each pattern
  nX : from interface
        The number of repeats along X
  nY : from interface
        The number of repeats along Y
          
  Description
  ---------
  A dose series is a common experiment performed during ebeam lithography to determine the
  optimum dose for a pattern. The optimum dose produces the desired pattern quickly and is
  always within tolerance.
  '''
  def __init__(self):
    super(doseSeries, self).__init__()
    self.param("cellName", self.TypeString, "Cell Name", default = "pattern")
    self.param("layer", self.TypeLayer, "Layer", default = pya.LayerInfo(1,0))
    self.param("pitchX", self.TypeDouble, "PitchX [um]", default = 200)
    self.param("pitchY", self.TypeDouble, "PitchY [um]", default = 200)
    self.param("nX", self.TypeInt, "nX [um]", default = 3)
    self.param("nY", self.TypeInt, "nY [um]", default = 3)

  def display_text_impl(self):
    return "Dose Series\n" + "Cell Name = " + self.cellName + "\nLayer = " + str(self.layer)
  
  def coerce_parameters_impl(self):   
    pass
  
  def can_create_from_shape_impl(self):
    pass
  
  def parameters_from_shape_impl(self):
    pass
  
  def transformation_from_shape_impl(self):
    return pya.Trans(pya.Point(0,0))
  
  def produce_impl(self):
  
    # Gets the reference to the cell view
    cv = pya.CellView().active()
    #Gets the reference to the layout
    layout = cv.layout()
    #Gets the databause unit
    dbu = self.layout.dbu

    # Create a temporary cell
    cell = layout.create_cell("tmp_cell")
    # Copy the target cell to the temporary cell
    cell.copy_tree(layout.cell(self.cellName))
    # Flatten the temporary cell
    cell.flatten(True)
    # Retrieve all shapes from the temporary cell
    shapes = cell.shapes(layout.layer(self.layer))

    # Convert parameters from [um] to [dbu] or database units
    px = int(self.pitchX / dbu)
    py = int(self.pitchY / dbu)
    
    # Create the dose series
    for i in range(self.nX):
      for j in range(self.nY):
        # Create a new datatype for each dose
        layer = self.layout.layer(int(self.layer.layer),i*self.nY+j)
        # Create a position for each dose
        tt = pya.ICplxTrans(px*j,py*i)
        # Insert the shapes into the PCell with the new layer and position
        self.cell.shapes(layer).insert(shapes,tt)
    
    # Delete the temporary cell
    cell.delete()
    # Make the newly added layers visible
    pya.LayoutView.current().add_missing_layers()