# Shape Generator for Klayout
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

class shape(object):
  '''      
    A collection of functions for generating various shapes
      
    Parameters
    ---------
    layout : pya.Layout
              The layout where the cell reside
    cell : pya.Cell
              The cell where the shape reside
    layer : pya.Layout.layer
              The layer/datatype for the shape
    
    Functions
    --------
    cross
    vernier
    text
    inverse
    '''
  def __init__(self):
    layout = pya.Layout()
    self.layout = layout
    self.cell = layout.create_cell("shape")
    self.layer = layout.layer(1,0)
    
  def __repr__(self):
    return ''
  
  def cross(self, width, length):
    '''
    cross(width, length)
    
    Generates a cross
    
    Parameters
    ---------
    width : integer
          The width of each leg of the cross
    length : integer
          The length of each leg of the cross
    
    Returns
    ------
    region : pya.Region
         A region containing the cross
    
    Description
    ---------
    A cross is a common pattern used for alignment.
    
    In photolithography a cross (width = 10, length = 100, unit = micron) can be used for coarse alignment.
    
    In ebeam lithography a cross (width = 3, length = 1000, unit = micron) can be used for global/coarse alignment
    and a cross (width = 3, length = 60, unit = micron) can be used for local/fine alignment. Typically, the cross pattern
    is made of 100 to 200 nm of dense material such Cr(10nm)/Au, Ti(10nm)/W, Ti(10nm)/Pt to provide ebeam
    contrast from the substrate.
    '''
    wh = int(width/2)
    lh = int(length/2)
    
    # Create the cross
    polygon = pya.Polygon([pya.Point(-wh,-lh), pya.Point(-wh,-wh), pya.Point(-lh,-wh), pya.Point(-lh,wh), 
      pya.Point(-wh,wh), pya.Point(-wh,lh), pya.Point(wh,lh), pya.Point(wh,wh),
      pya.Point(lh,wh), pya.Point(lh,-wh), pya.Point(wh,-wh), pya.Point(wh,-lh)])
    
    return pya.Region(polygon)

  def vernier(self, width, length, pitch):
    '''
    vernier(width, length, pitch)
    
    Generates a vernier scale
    
    Parameters
    ---------
    width : integer
          The width of each tick marker
    length : integer
          The length of the central tick mark
          The major tick marks are 3/4 this length
          The minor tick marks are half this length
    pitch : integer
          The distance between each tick mark
    
    Returns
    ------
    region : [pya.Region]
         A region containing the vernier scale
    
    Description
    ---------
    A pair of vernier scale can be used to measure misalignment by eye.
    
    In photolithography the wafer will contain one vernier pattern (width = 4, length = 40, pitch = 8, units = micron)
    and the mask will contain a second vernier pattern (pitch = 8.2) providing an alignment measurement resolution of 0.2 micron.
    '''
    scaleM = 0.75
    scaleS = 0.5
    
    # Create the large tick mark
    polygons = []
    tick = pya.Polygon([pya.Point(0,0), pya.Point(length,0), pya.Point(length,width), pya.Point(0,width)])
    tc = pya.Trans(int(-length/2),int(-width/2))
    polygons.append(tc.trans(tick))
    
    # Create the medium tick mark
    tickm = pya.Polygon([pya.Point(0,0), pya.Point(length*scaleM,0), pya.Point(length*scaleM,width), pya.Point(0,width)])
    pos = [-2, -1, 1, 2]
    for i in pos:
      tt = pya.Trans(0,int(i*pitch*5))
      polygons.append(tc.trans(tt.trans(tickm)))
    
    # Create the small tick mark
    ticks = pya.Polygon([pya.Point(0,0), pya.Point(length*scaleS,0), pya.Point(length*scaleS,width), pya.Point(0,width)])
    pos = [-9, -8, -7, -6, -4, -3, -2, -1, 1, 2, 3, 4, 6, 7, 8, 9]
    for i in pos:
      tt = pya.Trans(0,int(i*pitch))
      polygons.append(tc.trans(tt.trans(ticks)))
      
    return pya.Region(polygons)
  
  def text(self, text, center = True):
    '''
    text(text, center)
    
    Generates a text shape
    
    Parameters
    ---------
    text : string
          The text to be converted to shapes
    center : boolen (default = True)
          Centers the region at (0,0)
    
    Returns
    ------
    region : pya.Region
         A region containing the text
    
    Description
    ---------
    Uses the default text generator to create the text where each character is
    (cell width = 6, cell height = 8, line width = 1, design raster = 0.5, unit = micron)
    '''

    region = pya.TextGenerator.default_generator().text(text, 0.001,10)
    
    if center:
      p = region.bbox().center()
      region.move(-p.x,-p.y)
      
    return region
  
  def inverse(self, region, width, enlarge = True):
    '''
    inverse(polygons, length, boxLength)
    
    Generates a inverse of the polygons inside a bounding box
    
    Parameters
    ---------
    region : pya.Region
          A region containg polygons
    width : integer
          The width of the bounding box
    enlarge : boolean (default = True)
          The width parameter specifies an enlargement of the bounding box instead
    
    Returns
    ------
    iRegion : pya.Region
         The inverted region
    
    Description
    ---------
    An inverted pattern is often useful in photolithography and ebeam lithography
    '''
    regionBox = pya.Region.new(region.bbox().enlarged(width,width))
    iRegion = regionBox-region
    
    return iRegion

def testKLayout():
  #This performs a simple test of the class and draws the result on the active layout in KLayout
  
  #Gets a reference to the active cell view
  cv = pya.CellView().active()
  
  #Gets a reference to the active layout
  layout = cv.layout()
  
  #Gets a reference or creates layer 1/0
  layer = layout.layer(1,0)
  
  #Creates a new cell called TestShape
  if (layout.cell('TestShape') == None):
    cell = layout.create_cell('TestShape')
  #Clears the cell TestShape if it already exists
  else:
    cell = layout.cell('TestShape')
    cell.clear()
  
  #Gets the database units  
  dbu = layout.dbu
  
  #Creates a shape object
  a = shape()
  
  #Creates a cross and insert it into the test cell
  region = a.cross(10/dbu,100/dbu)
  cell.shapes(layer).insert(region)
  
  #Creates an inverted cross and insert it into the test cell
  region = a.cross(14/dbu,104/dbu)
  region = a.inverse(region,10/dbu)
  cell.shapes(layer).insert(region)
  
  #Creates a vernier pattern and inserts it into the test cell
  tt = pya.Trans(-100000,0)
  region = a.vernier(4/dbu, 40/dbu, 8.2/dbu)
  region.transform(tt)
  cell.shapes(layer).insert(region)
  
  #Creates an inverse vernier pattern and inserts it into the test cell
  tt = pya.Trans(2, False, -160000,0)
  region = a.vernier(4/dbu, 40/dbu, 8/dbu)
  region = a.inverse(region, 10/dbu)
  cell.shapes(layer).insert(region,tt)
  
  tt = pya.Trans(0,80000)
  region = a.text("0123456789 Hello")
  cell.shapes(layer).insert(region,tt)
  
  tt = pya.Trans(0,100000)
  region = a.text("0123456789")
  region = a.inverse(region, 10/dbu)
  cell.shapes(layer).insert(region,tt)
  
  cv.cell = cell

if __name__ == '__main__':
  #This function will automatically run if Python is running this file
  testKLayout()