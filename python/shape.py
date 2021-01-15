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
    textNumber : [pya.Polygon]
              A list of polygons representing numbers
      
    Returns
    ------
    shape [pya.Polygon]
    
    Functions
    --------
    cross
    vernier
    number
    inverse
    
    '''
  def __init__(self):
    layout = pya.Layout()
    self.layout = layout
    self.cell = layout.create_cell("shape")
    self.layer = layout.layer(1,0)
    self.textNumber = []
    #Number 0
    self.textNumber.append(pya.Polygon([pya.Point(1000,0), pya.Point(0,1000), pya.Point(0,6000), pya.Point(1000,7000), 
      pya.Point(4000,7000), pya.Point(5000,6000), pya.Point(1500,6000), pya.Point(1000,5500),
      pya.Point(1000,1500), pya.Point(1500,1000), pya.Point(3500,1000), pya.Point(4000,1500),
      pya.Point(4000,5500), pya.Point(3500,6000), pya.Point(5000,6000), pya.Point(5000,1000),
      pya.Point(4000,0)]))
    #Number 1
    self.textNumber.append(pya.Polygon([pya.Point(0,0), pya.Point(0,1000), pya.Point(2000,1000), pya.Point(2000,5000), 
      pya.Point(1500,5000), pya.Point(500,4000), pya.Point(0,4000), pya.Point(0,5000),
      pya.Point(2000,7000), pya.Point(3000,7000), pya.Point(3000,1000), pya.Point(5000,1000),
      pya.Point(5000,0)]))
    #Number 2
    self.textNumber.append(pya.Polygon([pya.Point(0,0), pya.Point(0,2500), pya.Point(1000,3500), pya.Point(3500,3500), 
      pya.Point(4000,4000), pya.Point(4000,5500), pya.Point(3500,6000), pya.Point(1500,6000),
      pya.Point(1000,5500), pya.Point(1000,5000), pya.Point(0,5000), pya.Point(0,6000),
      pya.Point(1000,7000), pya.Point(4000,7000), pya.Point(5000,6000), pya.Point(5000,3500),
      pya.Point(4000,2500), pya.Point(1500,2500), pya.Point(1000,2000), pya.Point(1000,1000),
      pya.Point(5000,1000), pya.Point(5000,0)]))
    #Number 3
    self.textNumber.append(pya.Polygon([pya.Point(1000,0), pya.Point(0,1000), pya.Point(0,2000), pya.Point(1000,2000), 
      pya.Point(1000,1500), pya.Point(1500,1000), pya.Point(3500,1000), pya.Point(4000,1500),
      pya.Point(4000,2500), pya.Point(3500,3000), pya.Point(2000,3000), pya.Point(2000,4000),
      pya.Point(3500,4000), pya.Point(4000,4500), pya.Point(4000,5500), pya.Point(3500,6000),
      pya.Point(1500,6000), pya.Point(1000,5500), pya.Point(1000,5000), pya.Point(0,5000),
      pya.Point(0,6000), pya.Point(1000,7000), pya.Point(4000,7000), pya.Point(5000,6000),
      pya.Point(5000,4000), pya.Point(4500,3500), pya.Point(5000,3000), pya.Point(5000,1000),
      pya.Point(4000,0)]))
    #Number 4
    self.textNumber.append(pya.Polygon([pya.Point(3000,0), pya.Point(3000,1500), pya.Point(0,1500), pya.Point(0,2500), 
      pya.Point(3000,2500), pya.Point(3000,5000), pya.Point(2500,5000), pya.Point(1000,3500),
      pya.Point(1000,2500), pya.Point(0,2500), pya.Point(0,4000), pya.Point(3000,7000),
      pya.Point(4000,7000), pya.Point(4000,2500), pya.Point(5000,2500), pya.Point(5000,1500),
      pya.Point(4000,1500), pya.Point(4000,0)]))
    #Number 5
    self.textNumber.append(pya.Polygon([pya.Point(1000,0), pya.Point(0,1000), pya.Point(0,2000), pya.Point(1000,2000), 
      pya.Point(1000,1500), pya.Point(1500,1000), pya.Point(3500,1000), pya.Point(4000,1500), pya.Point(4000,3000),
      pya.Point(3500,3500), pya.Point(0,3500), pya.Point(0,7000), pya.Point(5000,7000), pya.Point(5000,6000),
      pya.Point(1000,6000), pya.Point(1000,4500), pya.Point(4000,4500), pya.Point(5000,3500), pya.Point(5000,1000),
      pya.Point(4000,0)]))
    #Number 6
    self.textNumber.append(pya.Polygon([pya.Point(1000,0), pya.Point(0,1000), pya.Point(0,5000), pya.Point(2000,7000), 
      pya.Point(4000,7000), pya.Point(4000,6000), pya.Point(2500,6000), pya.Point(1500,5000),
      pya.Point(1500,4500), pya.Point(4000,4500), pya.Point(5000,3500), pya.Point(1500,3500),
      pya.Point(1000,3000), pya.Point(1000,1500), pya.Point(1500,1000), pya.Point(3500,1000),
      pya.Point(4000,1500), pya.Point(4000,3000), pya.Point(3500,3500), pya.Point(5000,3500),
      pya.Point(5000,1000), pya.Point(4000,0)]))
    #Number 7
    self.textNumber.append(pya.Polygon([pya.Point(2000,0), pya.Point(2000,3500), pya.Point(4000,5500), pya.Point(4000,6000), 
      pya.Point(0,6000), pya.Point(0,7000), pya.Point(5000,7000), pya.Point(5000,5000),
      pya.Point(3000,3000), pya.Point(3000,0)]))
    #Number 8
    self.textNumber.append(pya.Polygon([pya.Point(1000,0), pya.Point(0,1000), pya.Point(0,3000), pya.Point(500,3500), 
      pya.Point(0,4000), pya.Point(0,6000), pya.Point(1000,7000), pya.Point(4000,7000),
      pya.Point(5000,6000), pya.Point(1500,6000), pya.Point(1000,5500), pya.Point(1000,4500),
      pya.Point(1500,4000), pya.Point(3500,4000), pya.Point(4000,4500), pya.Point(4000,5500),
      pya.Point(3500,6000), pya.Point(5000,6000), pya.Point(5000,4000), pya.Point(4500,3500),
      pya.Point(5000,3000), pya.Point(1500,3000), pya.Point(1000,2500), pya.Point(1000,1500),
      pya.Point(1500,1000), pya.Point(3500,1000), pya.Point(4000,1500), pya.Point(4000,2500),
      pya.Point(3500,3000), pya.Point(5000,3000), pya.Point(5000,1000), pya.Point(4000,0)]))
    #Number 9
    self.textNumber.append(pya.Polygon([pya.Point(1000,0), pya.Point(1000,1000), pya.Point(2500,1000), pya.Point(3500,2000), 
      pya.Point(3500,2500), pya.Point(1000,2500), pya.Point(0,3500), pya.Point(3500,3500),
      pya.Point(4000,4000), pya.Point(4000,5500), pya.Point(3500,6000), pya.Point(1500,6000),
      pya.Point(1000,5500), pya.Point(1000,4000), pya.Point(1500,3500), pya.Point(0,3500),
      pya.Point(0,6000), pya.Point(1000,7000), pya.Point(4000,7000), pya.Point(5000,6000),
      pya.Point(5000,2000), pya.Point(3000,0)]))
    
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
    polygon : pya.Polygon
         A KLayout polygon representing the cross
    
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
    
    return polygon

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
    polygons : [pya.Polygon]
         A list of polygons comprising the vernier scale
    
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
      
    return polygons

  def number(self, num, center = True):
    '''
    number(num)
    
    Generates a number
    
    Parameters
    ---------
    number : string
          A string numbers
    center : boolen (default = True)
          Centers the polygon at (0,0)
    
    Returns
    ------
    polygon : [pya.Polygon]
         A KLayout polygon representing the number
    
    Description
    ---------
    The parameters of a single digit is (cell width = 6, cell height = 8, line width = 1, design raster = 0.5, unit = micron)
    
    1/8/2021 Ideally want to insert Basic.TEXT PCell to generate text, but it was supported
    '''
    if isinstance(num, int):
      num = str(num)
    poly = []
    counter = 0
    for i in num:
      tt = pya.Trans(counter*6000,0)
      poly.append(tt.trans(self.textNumber[int(i)]))
      counter += 1
    
    if center:
      tt = pya.Trans(-counter*6000/2+500,-3500)
      for i in range(counter):
        poly[i] = tt.trans(poly[i])
    
    return poly
  
  def inverse(self, polygons, width, enlarge = True):
    '''
    inverse(polygons, length, boxLength)
    
    Generates a inverse of the polygons inside a bounding box
    
    Parameters
    ---------
    cell : [pya.Polygon]
          A list of polygons
    width : integer
          The width of the bounding box
    enlarge : boolean (default = True)
          The width parameter specifies an enlargement of the bounding box instead
    
    Returns
    ------
    iPolygon : [pya.Polygon]
         The inverted polygons
    
    Description
    ---------
    An inverted pattern is often useful in photolithography and ebeam lithography
    '''
    if not isinstance(polygons,list):
      polygons = [polygons]
    
    self.cell.clear()
    for i in polygons:
      self.cell.shapes(self.layer).insert(i)
    region1 = pya.Region.new(self.cell.bbox().enlarged(width,width))
    region2 = pya.Region.new(self.cell.begin_shapes_rec(self.layer))
    region3 = region1-region2
    self.cell.clear()
    self.cell.shapes(self.layer).insert(region3)
    #self.cell.flatten
    iPolygon = []
    for i in self.cell.shapes(self.layer).each():
      iPolygon.append(i)
    
    return iPolygon

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
  poly = a.cross(10/dbu,100/dbu)
  cell.shapes(layer).insert(poly)
  
  #Creates an inverted cross and insert it into the test cell
  poly = a.cross(14/dbu,104/dbu)
  poly = a.inverse(poly,10/dbu)
  for i in poly:
    cell.shapes(layer).insert(i)
  
  #Creates a vernier pattern and inserts it into the test cell
  tt = pya.Trans(-100000,0)
  poly = a.vernier(4/dbu, 40/dbu, 8.2/dbu)
  for i in poly:
    cell.shapes(layer).insert(tt.trans(i))
  
  #Creates an inverse vernier pattern and inserts it into the test cell
  tt = pya.Trans(2, False, -160000,0)
  poly = a.vernier(4/dbu, 40/dbu, 8/dbu)
  for i in range(len(poly)):
    poly[i] = tt.trans(poly[i])
  poly = a.inverse(poly, 10/dbu)
  for i in poly:
    cell.shapes(layer).insert(i)
  
  tt = pya.Trans(0,80000)
  poly = a.number("0123456789")
  for i in range(len(poly)):
    cell.shapes(layer).insert(tt.trans(poly[i]))
  
  tt = pya.Trans(0,100000)
  poly = a.number("0")
  for i in range(len(poly)):
    poly[i] = tt.trans(poly[i])
  poly = a.inverse(poly, 10/dbu)
  for i in poly:
    cell.shapes(layer).insert(i)

if __name__ == '__main__':
  #This function will automatically run if Python is running this file
  testKLayout()