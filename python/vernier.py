# Vernier Pattern PCell for Klayout
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

class vernier(pya.PCellDeclarationHelper):
  '''
  Generates a vernier scale pattern
    
  Parameters
  ---------
  layer : from interface
        The layer and datatype for the patterns
  width : from interface
        The width of each tick mark
  length : from interface
        The length of the central tick mark
  pitch : from interface
        The distance between neighboring tick marks
  invert : from interface
        Invert the pattern?
  border : from interface
        The space between the bounding box and the inverted pattern
          
  Description
  ---------
  A pair of vernier scale can be used to measure misalignment by eye.
    
  In photolithography the wafer will contain one vernier pattern (width = 4, length = 40, pitch = 8, units = micron)
  and the mask will contain a second vernier pattern (pitch = 8.2) providing an alignment measurement resolution of 0.2 micron.
  '''
    
  def __init__(self):
    super(vernier, self).__init__()
    self.param("layer", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("width", self.TypeDouble, "Width [um]", default = 4)
    self.param("length", self.TypeDouble, "Length [um]", default = 40)
    self.param("pitch", self.TypeDouble, "Pitch [um]", default = 8)
    self.param("invert", self.TypeBoolean, "Hole", default = False)
    self.param("border", self.TypeDouble, "   Border Width [um]", default = 10)   

  def display_text_impl(self):
    return "Vernier Pattern\n" + "Pitch [um] = " + str('%.3f' % self.pitch) + "\n" + "Width [um] = " + str('%.3f' % self.width)
  
  def coerce_parameters_impl(self):   
    pass
  
  def can_create_from_shape_impl(self):
    return False
  
  def parameters_from_shape_impl(self):
    pass
  
  def transformation_from_shape_impl(self):
    return pya.Trans(pya.Point(0,0))
  
  def produce_impl(self):
    dbu = self.layout.dbu

    # Convert parameters from [um] to [dbu] or database units
    w = self.width / dbu
    l = self.length / dbu
    p = self.pitch / dbu
    b = self.border / dbu
    
    # Create the vernier pattern
    s = shape()
    region = s.vernier(w,l,p)
    
    if (self.invert):
      region = s.invert(region,b)

    self.cell.shapes(self.layer_layer).insert(region)

if __name__ == '__main__':
  #This function will automatically run if Python is running this file
  a = pya.Library()
  # Set the description
  a.description = "Lithography Tool Kit"
  # Create the PCell declarations
  a.layout().register_pcell("Test PCell", vernier())
  a.register("LTK")