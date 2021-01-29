# Cross PCell for Klayout
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

class cross(pya.PCellDeclarationHelper):
  '''
  Generates a cross pattern
    
  Parameters
  ---------
  layer : from interfance
        The layer and datatype for the patterns
  width : from interface
        The width of each tick mark
  length : from interface
        The length of the central tick mark
  inverse : from interface
        Invert the pattern
  border : from interface
        The space between the bounding box and the inverted pattern
          
  Description
  ---------
  A cross is a common pattern used for alignment in photolithography and ebeam lithography.
  '''
  def __init__(self):

    # Important: initialize the super class
    super(cross, self).__init__()

    # Parameters
    self.param("layer", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("type", self.TypeInt, "Type", default = 0, choices = [["Solid", 0],["Dashed", 1],["Dashed Inverted", 2]])
    self.param("width", self.TypeDouble, "Width [um]", default = 10)
    self.param("length", self.TypeDouble, "Length [um]", default = 100)
    self.param("inverse", self.TypeBoolean, "Inverse", default = False)
    self.param("border", self.TypeDouble, "   Border Width [um]", default = 10) 

  def display_text_impl(self):
    return "Cross Pattern\n" + "Leg Width [um] = " + str('%.3f' % self.width) + "\n" + "Leg Length [um] = " + str('%.3f' % self.length)
  
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
    w = self.width / self.layout.dbu
    l = self.length / self.layout.dbu
    b = self.border / self.layout.dbu
    
    # Create the cross
    s = shape()
    region = s.cross(w,l,self.type)
    
    if (self.inverse):
      region = s.inverse(region,b)
   
    self.cell.shapes(self.layer_layer).insert(region)

if __name__ == '__main__':
  #This function will automatically run if Python is running this file
  a = pya.Library()
  # Set the description
  a.description = "Lithography Tool Kit"
  # Create the PCell declarations
  a.layout().register_pcell("Test PCell", cross())
  a.register("LTK")