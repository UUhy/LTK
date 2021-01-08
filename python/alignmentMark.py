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

class alignmentMark(pya.PCellDeclarationHelper):
  '''
  Alignment Mark PCell
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
    dbu = layout.dbu
    
    s = shape()
    
    #Creates a cross
    t = pya.Trans(cPos)
    cross = t.trans(s.cross(cWidth/dbu, cLength/dbu))
    
    #Creates an inverted cross
    t = pya.Trans(cPos)
    poly = t.trans(s.cross((cWidth+2*cGap)/dbu, (cLength + 2*cGap)/dbu))
    icross = s.inverse(poly, cBorder/dbu)
    
    #Create Vernier Left 1
    vLeft1 = s.vernier(vWidth/dbu, vLength/dbu, vPitch/dbu)
    t = pya.Trans(vPosL)
    for i in range(len(vLeft1)):
      vLeft1[i] = t.trans(vLeft1[i])
    
    #Create Vernier Bottom 1
    vBot1 = s.vernier(vWidth/dbu, vLength/dbu, vPitch/dbu)
    t = pya.Trans(1, False, vPosB.x, vPosB.y)
    for i in range(len(vBot1)):
      vBot1[i] = t.trans(vBot1[i])

    #Create Vernier Left 2
    vLeft2 = s.vernier(vWidth/dbu, vLength/dbu, vPitch/dbu+self.res/dbu)
    t = pya.Trans(2, False, vPosL.x-vLength/dbu-vGap/dbu, vPosL.y)
    for i in range(len(vLeft2)):
      vLeft2[i] = t.trans(vLeft2[i])
    
    #Create Vernier Bottom 2
    vBot2 = s.vernier(vWidth/dbu, vLength/dbu, vPitch/dbu+self.res/dbu)
    t = pya.Trans(3, False, vPosB.x, vPosB.y-vLength/dbu-vGap/dbu)
    for i in range(len(vBot2)):
      vBot2[i] = t.trans(vBot2[i])
    
    #Create Mask Number for Wafer and Mask
    tm = pya.CplxTrans(mLineWidth)
    tl = pya.Trans(mPosL)
    tr = pya.Trans(mPosR)
    mn = s.number(str(self.num))
    mnLeft = []
    mnRight = []
    for i in range(len(mn)):
      mnLeft.append(tl.trans(tm.trans(mn[i])))
      mnRight.append(tr.trans(tm.trans(mn[i])))
    
    #Create sthe Wafer Alignment Mark
    poly = []
    if self.type == 0:
      poly.extend(icross)
      poly.extend(vLeft1)
      poly.extend(vBot1)
      poly.extend(mnLeft)
    else:
      #Creates the Mask Alignment Mark for a Dark Field Mask
      if self.mask == 0:
        poly.append(cross)
        poly.extend(vLeft2)
        poly.extend(vBot2)
        poly.extend(mnRight)
        poly = s.inverse(poly,border/dbu)
      #Creates the Mask Alignment Mark for a Light Field Mask
      else:
        poly.append(cross)
        poly.extend(vLeft2)
        poly.extend(vBot2)
        poly.extend(mnRight)
        
    for i in poly:
      self.cell.shapes(self.layer_layer).insert(i)