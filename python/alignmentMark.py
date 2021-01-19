# Alignment Mark Pattern PCell for Klayout
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

class alignmentMark(pya.PCellDeclarationHelper):
  '''
  alignmentMark()
    
  Generates an alignment mark with a cross and vernier patterns
    
  Parameters
  ---------
  layer : from interface
            The layer/datatype for the pattern
  type : from interface
            Specify the mark type as Wafer or Mask
  mask : from interface
            Specify the mask type as Dark Field or Light Field
  num : from interface
            Specify the mask number
  res : from interface
            Specify the alignment resolution        
    
  Returns
  ------
  pcell : PCell
            A PCell containing the alignment mark
  
  Description
  ---------
  Creates a PCell for alignment mark patterns for photolithography
  There are 2 types of alignment marks:
    Wafer marks are used to print alignment marks on the wafer, but not used for alignment
    Mask marks are used to align to an alignment mark
      Mask marks should facilitate the alignment process so it must contain minimal opaque patterns
      Mask mark patterns differ depending on whether the mask is Dark Field or Light Field
        Dark Field masks means polygons are transparent
        Light Field masks means polygons are opaque
  
  This is our preferred alignment mark. Perhaps we can add other variants in the future.
  '''
  def __init__(self):
    super(alignmentMark, self).__init__()
    self.param("layer", self.TypeLayer, "Layer", default = pya.LayerInfo(1,0))
    self.param("type", self.TypeInt, "Type", default = 0, choices = [["Wafer", 0],["Mask", 1]])
    self.param("mask", self.TypeInt, "Mask Type", default = 0, choices = [["Dark Field", 0],["Light Field", 1]])
    self.param("num", self.TypeString, "Mask Number", default = "01")
    self.param("res", self.TypeDouble, "Resolution [um]", default = 0.2)

  def display_text_impl(self):
    return "Alignment Mark\n" + "Mask Number = " + self.num
  
  def coerce_parameters_impl(self): 
    pass
  
  def can_create_from_shape_impl(self):
    pass
  
  def parameters_from_shape_impl(self):
    pass
  
  def transformation_from_shape_impl(self):
    return pya.Trans(pya.Point(0,0))
  
  def produce_impl(self):
    
    # Cross parameters
    cWidth = 10
    cLength = 100
    cGap = 0
    cBorder = 10
    cPos = pya.Point(0,0)
    
    # Vernier parameters
    vWidth = 4
    vLength = 40
    vPitch = 8
    vGap = 0
    vPosL = pya.Point(-120000,cPos.y)
    vPosB = pya.Point(cPos.x,-120000)
    
    # Mask number parameters
    mLineWidth = 4
    mPosL = pya.Point(-40000,90000)
    mPosR = pya.Point(40000,90000)
    
    # Border
    border = 10
    
    # Create references to the active cell
    cv = pya.CellView().active()
    layout = cv.layout()
    dbu = self.layout.dbu
    
    s = shape()
    
    #Creates a cross
    #t = pya.Trans(cPos)
    cross = s.cross(cWidth/dbu, cLength/dbu)
    cross.transform(pya.Trans(cPos))
    
    #Creates an inverted cross
    icross = s.cross((cWidth+2*cGap)/dbu, (cLength + 2*cGap)/dbu)
    icross = s.inverse(icross, cBorder/dbu)
    icross.transform(pya.Trans(cPos))
    
    #Create Vernier Left 1
    vLeft1 = s.vernier(vWidth/dbu, vLength/dbu, vPitch/dbu)
    vLeft1.transform(pya.Trans(vPosL))
    
    #Create Vernier Bottom 1
    vBot1 = s.vernier(vWidth/dbu, vLength/dbu, vPitch/dbu)
    vBot1.transform(pya.Trans(1, False, vPosB.x, vPosB.y))

    #Create Vernier Left 2
    vLeft2 = s.vernier(vWidth/dbu, vLength/dbu, vPitch/dbu+self.res/dbu)
    vLeft2.transform(pya.Trans(2, False, vPosL.x-vLength/dbu-vGap/dbu, vPosL.y))
    
    #Create Vernier Bottom 2
    vBot2 = s.vernier(vWidth/dbu, vLength/dbu, vPitch/dbu+self.res/dbu)
    vBot2.transform(pya.Trans(3, False, vPosB.x, vPosB.y-vLength/dbu-vGap/dbu))
    
    #Create Mask Number for Wafer and Mask
    tl = pya.CplxTrans(mLineWidth, 0, False, mPosL.x, mPosL.y)
    tr = pya.CplxTrans(mLineWidth, 0, False, mPosR.x, mPosR.y)
    mnLeft = s.text(self.num).transform(tl)
    mnRight = s.text(self.num).transform(tr)
    
    #Creates the Wafer Alignment Mark
    region = pya.Region()
    if self.type == 0:
      region.insert(icross)
      region.insert(vLeft1)
      region.insert(vBot1)
      region.insert(mnLeft)
    else:
      #Creates the Mask Alignment Mark for a Dark Field Mask
      if self.mask == 0:
        region.insert(cross)
        region.insert(vLeft2)
        region.insert(vBot2)
        region.insert(mnRight)
        region = s.inverse(region,border/dbu)
      #Creates the Mask Alignment Mark for a Light Field Mask
      else:
        region.insert(cross)
        region.insert(vLeft2)
        region.insert(vBot2)
        region.insert(mnRight)
        
    self.cell.shapes(self.layer_layer).insert(region)