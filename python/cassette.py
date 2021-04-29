# JBX5500FS Cassette PCell for Klayout
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
from shape import shape

class cassette(pya.PCellDeclarationHelper):
  '''
  Generates a Jeol JBX-5500FS cassette pattern
    
  Parameters
  ---------
  layer : from interfance
        The layer and datatype for the patterns
  cassette : from interface
        The type of cassette
  invert : from interface
        Invert the pattern
  border : from interface
        The space between the bounding box and the inverted pattern
          
  Description
  ---------
  The cassette pattern can be positioned to correspond to the stage positions on the JBX5500FS EBW
  The EBW y axis is reverse of the KLayout y axis
  '''
  def __init__(self):

    # Important: initialize the super class
    super(cassette, self).__init__()

    # Parameters
    self.specCassetteName = ["3\"", "4\"", "Piece Holder"]
    self.param("layer", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("cassette", self.TypeInt, "Cassette Type", default = 0, choices = [["3\"", 0],["4\"", 1],["Piece Holder", 2]])
    self.param("real", self.TypeBoolean, "Stage Position", default = True)
    self.param("invert", self.TypeBoolean, "Hole", default = False)
    self.param("border", self.TypeDouble, "   Border Width [um]", default = 10) 

  def display_text_impl(self):
    return "Cassette\n" + "Type = " + self.specCassetteName(self.cassette)
  
  def coerce_parameters_impl(self):   
    pass
  
  def can_create_from_shape_impl(self):
    pass
  
  def parameters_from_shape_impl(self):
    pass
  
  def transformation_from_shape_impl(self):
    return pya.Trans(pya.Point(0,0))
  
  def produce_impl(self):
    # Creates the patterns

    # Convert parameters from [um] to [dbu] or database units
    b = self.border / self.layout.dbu
    
    s = shape()

    # Create the 3" Wafer Cassette
    if (self.cassette == 0):
      region = s.circle(70000/self.layout.dbu, 128)
      tt =  pya.ICplxTrans(66500/self.layout.dbu, -37500/self.layout.dbu)
    if (self.cassette == 1):
      region = s.circle(78000/self.layout.dbu, 128)
      tt =  pya.ICplxTrans(66500/self.layout.dbu, -37500/self.layout.dbu)
    if (self.cassette == 2):
      region = s.pieceHolderCassette(self.layout.dbu)
      tt =  pya.ICplxTrans(62500/self.layout.dbu, -37500/self.layout.dbu)
    
    if (self.real):
      region.transform(tt)
    
    if (self.invert):
      region = s.invert(region,b)
   
    self.cell.shapes(self.layer_layer).insert(region)

if __name__ == '__main__':
  #This function will automatically run if Python is running this file
  a = pya.Library()
  # Set the description
  a.description = "Lithography Tool Kit"
  # Create the PCell declarations
  a.layout().register_pcell("Test PCell", cassette())
  a.register("LTK")