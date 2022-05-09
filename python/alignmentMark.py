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
  cross : from interface
            Specify the cross type as Solid or Dashed       
    
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
    self.param("pos", self.TypeDouble, "Position [mm]", default = 40)
    self.param("layer", self.TypeLayer, "Layer", default = pya.LayerInfo(1,0))
    self.param("type", self.TypeInt, "Type", default = 0, choices = [["Wafer", 0],["Mask", 1]])
    self.param("mask", self.TypeInt, "Mask Type", default = 0, choices = [["Dark Field", 0],["Clear Field", 1]])
    self.param("num", self.TypeString, "Mask Number", default = "01")
    self.param("res", self.TypeDouble, "Resolution [um]", default = 0.2)
    self.param("cross", self.TypeInt, "Cross Type", default = 0, choices = [["Solid", 0],["Dashed", 1]])

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
    mPos = pya.Point(140000,140000)
    
    # Border
    border = 10
    
    # Create references to the active cell
    cv = pya.CellView().active()
    layout = cv.layout()
    dbu = self.layout.dbu
    
    # Position of the Alignment Marks
    posLeftMark = pya.Point(-self.pos*1000/dbu,0)
    posRightMark = pya.Point(self.pos*1000/dbu,0)
    
    s = shape()
    
    #Creates a cross
    if (self.cross == 0): #Solid Cross
      if (self.type == 0): #Wafer Type
        #Creates an inverted cross
        cross = s.cross((cWidth+2*cGap)/dbu, (cLength + 2*cGap)/dbu)
        cross = s.invert(cross, cBorder/dbu)
        cross.transform(pya.Trans(cPos))
      else:
        cross = s.cross(cWidth/dbu, cLength/dbu)
        cross.transform(pya.Trans(cPos))
    else: #Dashed Cross
      if (self.type == 0): #Wafer Type
        cross = s.cross(cWidth/dbu, cLength/dbu,1)
        cross = s.invert(cross, cBorder/dbu)
        cross.transform(pya.Trans(cPos))
      else:
        cross = s.cross(cWidth/dbu, cLength/dbu,2)
        cross.transform(pya.Trans(cPos))
    
    if (self.type == 0): #Wafer Type
      #Create Vernier Patterns
      vLeft = s.vernier(vWidth/dbu, vLength/dbu, vPitch/dbu)
      vLeft.transform(pya.Trans(vPosL))
      vBot = vLeft.dup()
      vBot.transform(pya.Trans(1,0,0,0))
      vRight = vLeft.dup()
      vRight.transform(pya.Trans(2,0,0,0))
      vTop = vLeft.dup()
      vTop.transform(pya.Trans(3,0,0,0))
      
      #Create Mask Number 
      tt = pya.CplxTrans(mLineWidth, 0, False, -mPos.x, mPos.y)
      mNumLeft = s.text(self.num).transform(tt)
      mNumRight = mNumLeft.dup()
      mNumRight.transform(pya.Trans(2,True,0,0))
    else:
      #Create Vernier Left 2
      vLeft = s.vernier(vWidth/dbu, vLength/dbu, vPitch/dbu+self.res/dbu)
      vLeft.transform(pya.Trans(2, False, vPosL.x-vLength/dbu-vGap/dbu, vPosL.y))
      vBot = vLeft.dup()
      vBot.transform(pya.Trans(1,0,0,0))
      vRight = vLeft.dup()
      vRight.transform(pya.Trans(2,0,0,0))
      vTop = vLeft.dup()
      vTop.transform(pya.Trans(3,0,0,0))
    
      #Create Mask Number
      tt = pya.CplxTrans(mLineWidth, 0, False, -mPos.x, -mPos.y)
      mNumLeft = s.text(self.num).transform(tt)
      mNumRight = mNumLeft.dup()
      mNumRight.transform(pya.Trans(2,True,0,0))
    
    #Create Shapes for Left Mark and Right Mark 
    leftMarkCross = cross.dup()
    leftMarkCross.transform(pya.Trans(posLeftMark))
    leftMarkVernierLeft = vLeft.dup()
    leftMarkVernierLeft.transform(pya.Trans(posLeftMark))
    leftMarkVernierBot = vBot.dup()
    leftMarkVernierBot.transform(pya.Trans(posLeftMark))
    leftMarkVernierRight = vRight.dup()
    leftMarkVernierRight.transform(pya.Trans(posLeftMark))
    leftMarkVernierTop = vTop.dup()
    leftMarkVernierTop.transform(pya.Trans(posLeftMark))
    leftMarkMNumLeft = mNumLeft.dup()
    leftMarkMNumLeft.transform(pya.Trans(posLeftMark))
    leftMarkMNumRight = mNumRight.dup()
    leftMarkMNumRight.transform(pya.Trans(posLeftMark))
    
    rightMarkCross = cross.dup()
    rightMarkCross.transform(pya.Trans(posRightMark))
    rightMarkVernierLeft = vLeft.dup()
    rightMarkVernierLeft.transform(pya.Trans(posRightMark))
    rightMarkVernierBot = vBot.dup()
    rightMarkVernierBot.transform(pya.Trans(posRightMark))
    rightMarkVernierRight = vRight.dup()
    rightMarkVernierRight.transform(pya.Trans(posRightMark))
    rightMarkVernierTop = vTop.dup()
    rightMarkVernierTop.transform(pya.Trans(posRightMark))
    rightMarkMNumLeft = mNumLeft.dup()
    rightMarkMNumLeft.transform(pya.Trans(posRightMark))
    rightMarkMNumRight = mNumRight.dup()
    rightMarkMNumRight.transform(pya.Trans(posRightMark))
    
    #Creates the Wafer Alignment MarkCross
    regionLeft = pya.Region()
    regionLeft.insert(leftMarkCross)
    regionLeft.insert(leftMarkVernierLeft)
    regionLeft.insert(leftMarkVernierBot)
    regionLeft.insert(leftMarkVernierRight)
    regionLeft.insert(leftMarkVernierTop)
    regionLeft.insert(leftMarkMNumLeft)
    regionLeft.insert(leftMarkMNumRight)
      
    regionRight = pya.Region()
    regionRight.insert(rightMarkCross)
    regionRight.insert(rightMarkVernierLeft)
    regionRight.insert(rightMarkVernierBot)
    regionRight.insert(rightMarkVernierRight)
    regionRight.insert(rightMarkVernierTop)
    regionRight.insert(rightMarkMNumLeft)
    regionRight.insert(rightMarkMNumRight)
   
    if (self.type == 1) and (self.mask == 0):
      regionLeft = s.invert(regionLeft,border/dbu)
      regionRight = s.invert(regionRight,border/dbu)
        
    self.cell.shapes(self.layer_layer).insert(regionLeft)
    self.cell.shapes(self.layer_layer).insert(regionRight)
    
if __name__ == '__main__':
  #This function will automatically run if Python is running this file
  a = pya.Library()
  # Set the description
  a.description = "Lithography Tool Kit"
  # Create the PCell declarations
  a.layout().register_pcell("Test PCell", alignmentMark())
  a.register("LTK")