# Ring PCell for Klayout
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

class ring(pya.PCellDeclarationHelper):
  '''
  Generates a ring pattern
    
  Parameters
  ---------
  layer : from interfance
        The layer and datatype for the patterns
  outerDiameter : from interface
        The outer diameter of the ring
  innerDiameter : from interface
        The inner diameter of the ring
  vertices : from interface
        The number of vertices in the outer diameter and inner diameter
  fracture : from interface
        Make a fracture friendly ring
  invert : from interface
        Invert the pattern
  border : from interface
        The space between the bounding box and the inverted pattern
          
  Description
  ---------
  A fracture friendly lines up the vertices of the inner circle with the outer circle
  '''
  def __init__(self):

    # Important: initialize the super class
    super(ring, self).__init__()

    # Parameters
    self.param("layer", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("outerDiameter", self.TypeDouble, "Outer Diameter [um]", default = 10)
    self.param("innerDiameter", self.TypeDouble, "Inner Diameter [um]", default = 8)
    self.param("vertices", self.TypeDouble, "Vertices", default = 8)
    self.param("fracture", self.TypeBoolean, "Fracture Friendly", default = True)
    self.param("invert", self.TypeBoolean, "Hole", default = False)
    self.param("border", self.TypeDouble, "   Border Width [um]", default = 10) 

  def display_text_impl(self):
    return "Ring\n" + "Outer Diameter [um] = " + str('%.3f' % self.outerDiameter) + "\n" + "Inner Diameter [um] = " + str('%.3f' % self.innerDiameter)
  
  def coerce_parameters_impl(self):   
    #Vertices must be at least 8 and an even number
    if (self.vertices < 8):
      self.vertices = 8
    self.vertices = int(self.vertices/4)*4
  
  def can_create_from_shape_impl(self):
    pass
  
  def parameters_from_shape_impl(self):
    pass
  
  def transformation_from_shape_impl(self):
    return pya.Trans(pya.Point(0,0))
  
  def produce_impl(self):
    # Creates the patterns

    # Convert parameters from [um] to [dbu] or database units
    do = self.outerDiameter / self.layout.dbu
    di = self.innerDiameter / self.layout.dbu
    b = self.border / self.layout.dbu
    
    # Create the cross
    s = shape()
    region = s.ring(do,di,self.vertices,self.fracture)
    
    if (self.invert):
      region = s.invert(region,b)
   
    self.cell.shapes(self.layer_layer).insert(region)

if __name__ == '__main__':
  #This function will automatically run if Python is running this file
  a = pya.Library()
  # Set the description
  a.description = "Lithography Tool Kit"
  # Create the PCell declarations
  a.layout().register_pcell("Test PCell", ring())
  a.register("LTK")