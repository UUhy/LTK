# Silicon Wafer PCell for Klayout
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

class siWafer(pya.PCellDeclarationHelper):
  '''
  Generates a silicon wafer pattern
    
  Parameters
  ---------
  layer : from interfance
        The layer and datatype for the patterns
  diameter : from interface
        The diameter of the Silicon Wafer
  secondaryFlatAngle : from interface
        The location of the secondar flat
  invert : from interface
        Invert the pattern
  border : from interface
        The space between the bounding box and the inverted pattern
  '''
  def __init__(self):

    # Important: initialize the super class
    super(siWafer, self).__init__()

    # Parameters
    self.specDiameter = [50.8,76.2,100,125,150]
    self.specPrimaryFlat = [15.88, 22.22, 32.5, 42.5, 57.5]
    self.specSecondaryFlat = [8, 11.18, 18, 27.5, 37.5]
    self.specSecondaryFlatAngle = [45,90,180]
    self.param("layer", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("diameter", self.TypeInt, "Diameter [mm]", default = 0, choices = [["50.8", 0],["76.2", 1],["100", 2],["125", 2],["150", 2]])
    self.param("secondaryFlatAngle", self.TypeInt, "Secondary Flat Angle [degrees]", default = 1, choices = [["45", 0],["90", 1],["180", 2]])
    self.param("invert", self.TypeBoolean, "Hole", default = False)
    self.param("border", self.TypeDouble, "   Border Width [mm]", default = 10) 

  def display_text_impl(self):
    print self.diameter
    return "Silicon Wafer\n" + "Diameter [mm] = " + str(self.specDiameter[self.diameter])
  
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

    d = self.specDiameter[self.diameter] / self.layout.dbu * 1000
    pFlat = self.specPrimaryFlat[self.diameter] / self.layout.dbu * 1000
    sFlat = self.specSecondaryFlat[self.diameter] / self.layout.dbu * 1000
    aFlat = self.specSecondaryFlatAngle[self.secondaryFlatAngle]
    b = self.border / self.layout.dbu * 1000
    
    # Create the cross
    s = shape()
    region = s.siWafer(d, pFlat, sFlat, aFlat, 128)
    
    if (self.invert):
      region = s.invert(region,b)
   
    self.cell.shapes(self.layer_layer).insert(region)

if __name__ == '__main__':
  #This function will automatically run if Python is running this file
  a = pya.Library()
  # Set the description
  a.description = "Lithography Tool Kit"
  # Create the PCell declarations
  a.layout().register_pcell("Test PCell", siWafer())
  a.register("LTK")