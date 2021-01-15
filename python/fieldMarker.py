# Field Marker PCell for Klayout
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

class fieldMarker(pya.PCellDeclarationHelper):
  '''
  Generates a pair of field markers to coerce the write field position
    
  Parameters
  ---------
  cellName : from interface
        The name of the cell
  fieldSize : from interface
        The field size for the JBX-5500FS Electron Beam Writer
          
  Description
  ---------
  The write field for the JBX-5500FS Electron Beam Writer (EBW) is a square that is 100 or 1000 microns wide. When a pattern
  is smaller than the write field, the EBW will begin writing the pattern from the top left corner of the write field. The corners
  of the write field should be avoided since it is prone to distortion. This PCell inserts a couple of tiny (100nm) squares to
  ensure that pattern will be written at the center of the write field.
  '''
  def __init__(self):

    super(fieldMarker, self).__init__()
    self.param("layer", self.TypeLayer, "Layer", default = pya.LayerInfo(1,0))
    self.param("cellName", self.TypeString, "Cell Name", default = "pattern")
    self.param("fieldSize", self.TypeInt, "Field Size [um]", default = 1000, choices = [["Mode 4: 100 um", 100],["Mode 2: 1000 um", 1000]])

  def display_text_impl(self):
    return "Field\n" + "Field Size [um] = " + str('%.3f' % self.fieldSize)
  
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
    # Gets the reference to the layout
    layout = cv.layout()
    # Gets the databause unit
    dbu = self.layout.dbu
    
    # Gets a list of all the layers in the layout
    layerList = layout.layer_infos()

    # Creates a temporary cell
    cell = layout.create_cell("tmp_cell")
    # Copy the target cell to the temporary cell
    cell.copy_tree(layout.cell(self.cellName))
    # Flatten the temporary cell
    cell.flatten(True)
    
    # Insert every pattern from every layer into the PCell
    for i in layerList:
      shapes = cell.shapes(self.layout.layer(i))
      self.cell.shapes(self.layout.layer(i)).insert(shapes)
    
    # Create a small box to use as a field marker
    rbox = 100
    box = pya.Box(-rbox,-rbox,rbox,rbox)
    
    # Determine the width of the target cell
    bbox = layout.cell(self.cellName).dbbox()
    w = bbox.right - bbox.left
    # Determine the height of the target cell
    h = bbox.top - bbox.bottom
    # Determine the center of the target cell
    c = bbox.center()
    
    # If the target cell fits into the field, add field markers
    if w < self.fieldSize and h < self.fieldSize:
      # Calculate the field radius
      rf = int(self.fieldSize/dbu/2)
      # Calculate the position of the top left field marker
      tt = pya.Trans(int(c.x/dbu)-rf+rbox,int(c.y/dbu)+rf-rbox)
      # Insert a field marker at the top left of the field
      self.cell.shapes(self.layer_layer).insert(tt.trans(box))
      # Calculate the position of the bottom right field marker
      tt = pya.Trans(int(c.x/dbu)+rf-rbox,int(c.y/dbu)-rf+rbox)
      # Insert the field marker at the bottom left of the field
      self.cell.shapes(self.layer_layer).insert(tt.trans(box))
      '''
      # Creates field markers for each layer/datatype -- Excessive?
      for i in layerList:
        # Calculate the field radius
        rf = int(self.fieldSize/dbu/2)
        # Calculate the position of the top left field marker
        tt = pya.Trans(int(c.x/dbu)-rf+rbox,int(c.y/dbu)+rf-rbox)
        # Insert a field marker at the top left of the field
        self.cell.shapes(self.layout.layer(i)).insert(tt.trans(box))
        # Calculate the position of the bottom right field marker
        tt = pya.Trans(int(c.x/dbu)+rf-rbox,int(c.y/dbu)-rf+rbox)
        # Insert the field marker at the bottom left of the field
        self.cell.shapes(self.layout.layer(i)).insert(tt.trans(box))
      '''
    # If the target cell does not fit into the field, inform the user
    else:
      pya.MessageBox.warning("Field Size too Small","The pattern in the specified cell is larger than the selected field size.",pya.MessageBox.Ok)

    # Deletes the temporary cell
    cell.delete()
    
    # Show newly added layers
    pya.LayoutView.current().add_missing_layers()