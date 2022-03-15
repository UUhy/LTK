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
import numpy as np

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
    checkerboard
    circle
    cross
    invert
    pieceHolderCassette
    ring
    siWafer
    text
    vernier
 
    Description
    --------
    These function use database unit. 
    By default the drawing units of 1 [um] and the database unit is 1000. 
    For example,  1 [um] is represented as 1000 dbu.
    '''
  def __init__(self):
    layout = pya.Layout()
    self.layout = layout
    self.cell = layout.create_cell("shape")
    self.layer = layout.layer(1,0)
    
  def __repr__(self):
    return ''
  
  def cross(self, width, length, crossType = 0):
    '''
    cross(width, length)
    
    Generates a cross
    
    Parameters
    ---------
    width : integer
          The width of each leg of the cross
    length : integer
          The length of each leg of the cross
    crossType : integer
          The type of cross
          0 : A regular cross
          1 : A dashed cross with center
          2 : A dashed cross without center
    
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
    
    #Create a cross
    if (crossType == 0):
      #Create a rectangle with length along X
      xBox = pya.Box(-wh,-lh,wh,lh)
      #Create a rectangle with length along y
      yBox = pya.Box(-lh,-wh,lh,wh)
      #Combine the two rectangles together
      region = pya.Region(xBox)+pya.Region(yBox)
      #Merge the region
      region.merge()
    #Create a dashed cross with center
    elif (crossType == 1):
      #Define the position of the segments
      pos = [-4, -2, 2, 4]
      #Calculate segment dimension
      s = int((lh-wh)/4)
      sh = int(s/2)
      #Create segments
      xBox = pya.Box(-sh, -wh, sh, wh)
      yBox = pya.Box(-wh, -sh, wh, sh)
      #Define a region with a center cross
      region = pya.Region(pya.Box(-wh,-wh,wh,wh))
      #Calculate an offset due to center
      dw = sh-wh
      for i in pos:
        #Determine translations for negative positions
        if (i < 0):
          tx = pya.ICplxTrans(int(i*s+dw),0)
          ty = pya.ICplxTrans(0,int(i*s+dw))
        else:
        #Determine translations for positive positions
          tx = pya.ICplxTrans(int(i*s-dw),0)
          ty = pya.ICplxTrans(0,int(i*s-dw))
        #Insert the segments into the region
        region.insert(tx.trans(xBox))
        region.insert(ty.trans(yBox))
    #Create a dashed cross without a center
    elif (crossType == 2):
      #Define the position of the segments
      pos = [-3, -1, 1, 3]
      #Calculate the segment dimension
      s = int((lh-wh)/4)
      sh = int(s/2)
      #Create segments
      xBox = pya.Box(-sh, -wh, sh, wh)
      yBox = pya.Box(-wh, -sh, wh, sh)
      #Calculate an offset due to center
      dw = sh-wh
      #Define a region with nothing
      region = pya.Region()
      for i in pos:
        if (i < 0):
          #Determine translations for negative positions
          tx = pya.ICplxTrans(int(i*s+dw),0)
          ty = pya.ICplxTrans(0,int(i*s+dw))
        else:
          #Determine the translations for positive positions
          tx = pya.ICplxTrans(int(i*s-dw),0)
          ty = pya.ICplxTrans(0,int(i*s-dw))
        #Insert the segments into the region
        region.insert(tx.trans(xBox))
        region.insert(ty.trans(yBox))
    
    return region

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
    #tick = pya.Polygon([pya.Point(0,0), pya.Point(length,0), pya.Point(length,width), pya.Point(0,width)])
    tick = pya.Polygon([pya.Point(0,0), pya.Point(0,width), pya.Point(length,width), pya.Point(length,0)])
    tc = pya.ICplxTrans(int(-length/2),int(-width/2))
    polygons.append(tc.trans(tick))
    
    # Create the medium tick mark
    #tickm = pya.Polygon([pya.Point(0,0), pya.Point(length*scaleM,0), pya.Point(length*scaleM,width), pya.Point(0,width)])
    tickm = pya.Polygon([pya.Point(0,0), pya.Point(0,width), pya.Point(length*scaleM,width), pya.Point(length*scaleM,0)])
    pos = [-2, -1, 1, 2]
    for i in pos:
      tt = pya.ICplxTrans(0,int(i*pitch*5))
      polygons.append(tc.trans(tt.trans(tickm)))
    
    # Create the small tick mark
    #ticks = pya.Polygon([pya.Point(0,0), pya.Point(length*scaleS,0), pya.Point(length*scaleS,width), pya.Point(0,width)])
    ticks = pya.Polygon([pya.Point(0,0), pya.Point(0,width), pya.Point(length*scaleS,width), pya.Point(length*scaleS,0)])
    pos = [-9, -8, -7, -6, -4, -3, -2, -1, 1, 2, 3, 4, 6, 7, 8, 9]
    for i in pos:
      tt = pya.ICplxTrans(0,int(i*pitch))
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
  
  def invert(self, region, width, enlarge = True):
    '''
    invert(polygons, length, boxLength)
    
    Generates an invert of the polygons inside a bounding box
    
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
  
  def checkerboard(self, width, num = 5):
    '''
    checkerboard(width, num)
    
    Generates a checkerboard pattern
    
    Parameters
    ---------
    width : integer
          The width of each square
    num : integer (5)
          The number of squares
    
    Returns
    ------
    region : pya.Region
         A region containing the checkerboard
    
    Description
    ---------
    A checkerboard pattern is used to qualitatively evaluate the resolution of the print.
    The corners of the checkboard pattern will degrade as resolution gets worse
    '''    
    # Create a box
    square = pya.Polygon([pya.Point(0,0), pya.Point(0,width), pya.Point(width,width), pya.Point(width,0)])
    polygons = []
    tc = pya.ICplxTrans(-int(num*width/2),-int(num*width/2))
    
    if (num%2 == 1):
      for i in range(num*num):
        if (i%2 == 0):
          tt = pya.ICplxTrans(int(i%num*width),int(i/num*width))
          polygons.append(tc.trans(tt.trans(square)))
    else:
      for i in range(num):
        for j in range(num):
          if ((j+i)%2 == 0):
            tt = pya.ICplxTrans(int(i*width),int(j*width))
            polygons.append(tc.trans(tt.trans(square)))
    
    return pya.Region(polygons)

  def circle(self, diameter, vertices = 128):
      '''
      circle(diameter, vertices)
      
      Generates a circle shape
      
      Parameters
      ---------
      diameter : integer
            The diameter of a circle
      vertices : integer (128)
            Number of vertices in the circle (coerce to multiple of 4)
      
      Returns
      ------
      region : [pya.Region]
           A region containing the circle shape
      
      Description
      ------
      The number of vertices is coerced to even numbers to ensure good fracturing
      '''  
      r = int(diameter/2)
      vertices = int(vertices/4)*4
      
      # Create a circle
      polygon = pya.Polygon([pya.Point(-r,-r), pya.Point(-r,r), pya.Point(r,r), pya.Point(r,-r)])
      polygon = polygon.round_corners(0,r,vertices)

      return pya.Region(polygon)
      
  def ring(self, outerDiameter, innerDiameter, vertices = 128, fracture = True):
      '''
      circle(outerDiameter, innerDiameter, vertices)
      
      Generates a circle shape
      
      Parameters
      ---------
      outerDiameter : integer
            The outer diameter of the ring
      innerDiameter : integer
            The inner diameter of the ring
      vertices : integer (128)
            Number of vertices in the circle (coerce to multiples of 4)
      fracture : boolean (True)
            Create the inner polygon with vertices that is optimal for fracturing horizontally
      
      Returns
      ------
      region : [pya.Region]
           A region containing the circle shape
      '''  
      ro = int(outerDiameter/2)
      ri = int(innerDiameter/2)
      vertices = int(vertices/4)*4
      
      # Create a circle
      polygon = pya.Polygon([pya.Point(-ro,-ro), pya.Point(-ro,ro), pya.Point(ro,ro), pya.Point(ro,-ro)])
      polygonOuter = polygon.round_corners(0,ro,vertices)
      polygon = pya.Polygon([pya.Point(-ri,-ri), pya.Point(-ri,ri), pya.Point(ri,ri), pya.Point(ri,-ri)])
      
      if fracture:
        points =  polygonOuter.each_point_hull()
        polygonInnerPoints = []
        r2 = np.power(ri,2)
        for point in points:
          if (ri > np.absolute(point.y)):
            x = np.sqrt(r2 - np.power(point.y,2))
            polygonInnerPoints.append(pya.Point(np.sign(point.x)*x,point.y))
        polygonInner = pya.Polygon(polygonInnerPoints)
      else:
        polygonInner = polygon.round_corners(0,ri,vertices)

      return pya.Region(polygonOuter) - pya.Region(polygonInner)

  def siWafer(self, diameter, primaryFlat, secondaryFlat, angle, vertices = 128):
      '''
      siWafer(diameter, secondaryFlatAngle)
      
      Generates a Silicon Wafer shape
      
      Parameters
      ---------
      diameter : integer
            The diameter of a standard silicon wafer
      primaryFlat : integer
            The length of the primary flat
      secondaryFlat : integer
            The length of the secondary flat
      angle : double
            The location of the secondary flat relative (counterclockwise) to primary flat in degrees
      vertices : integer (coerce to even number)
            The number of vertices used to generate the circle
      
      Returns
      ------
      region : [pya.Region]
           A region containing the Si Wafer shape
      
      Description
      ---------
      SEMI Wafer Flat M1-0302 Specification
      Wafer Size  = [2", 3", 100mm, 125mm, 150mm, 200mm, 300mm]
      Diameter [mm] = [50.8, 76.2, 100, 125, 150, 200, 300]
      Thickness [um] = [279, 381, 525 or 625, 625, 675 or 625, 725, 775]
      Primary Flat Length = [15.88, 22.22, 32.5, 42.5, 57.5, Notch, Notch]
      Secondary Flat Length = [8, 11.18, 18, 27.5, 37.5, NA, NA]
      '''
      dList = [50800, 76200, 10000, 12500, 15000]
      pFlatLengthList = [15.88, 22.22, 32.5, 42.5, 57.5]
      sFlatLengthList = [8, 11.18, 18, 27.5, 37.5]
      
      r = int(diameter/2)
      
      #Height of arc position (https://mathworld.wolfram.com/CircularSegment.html)
      pH = r- int(np.sqrt(4*np.power(r,2)-np.power(primaryFlat,2))/2)
      sH = r - int(np.sqrt(4*np.power(r,2)-np.power(secondaryFlat,2))/2)
      
      # Create a circle
      polygon = pya.Polygon([pya.Point(-r,-r), pya.Point(-r,r), pya.Point(r,r), pya.Point(r,-r)])
      polygon = polygon.round_corners(0,r,vertices)
      
      #Create a rectangle to produce the primary flat
      pRectangle = pya.Polygon([pya.Point(-r,-r-pH), pya.Point(-r,-r+pH), pya.Point(r,-r+pH), pya.Point(r,-r-pH)])
      
      #Create a rectangle to produce the secondary flat
      sRectangle = pya.Polygon([pya.Point(-r,r-sH), pya.Point(-r,r+sH), pya.Point(r,r+sH), pya.Point(r,r-sH)])
      tt = pya.ICplxTrans(1, angle, False, 0, 0)

      return pya.Region(polygon)-pya.Region(pRectangle)-pya.Region(sRectangle.transform(tt))

  def pieceHolderCassette(self,dbu = 1):
      '''
      pieceHolderCassette()
      
      Generates the shape of the Jeol JBX-5500FS piece holder cassette
      
      Parameters
      ---------
      dbu : double
            The database unit
            
      Returns
      ------
      region : [pya.Region]
           A region containing the piece holder cassette shape
           
      Description
      ------
      The center of this piece holder shape (0,0) is at stage position (62.5mm, 37.5mm)
      
      Jeol Stage Y axis is reverse of KLayout Y axis
      '''
      # Create the quarter circle
      r = 36100/dbu
      rx = 62500/dbu
      ry = -37500/dbu
      polygon = pya.Polygon([pya.Point(-r,-r), pya.Point(-r,r), pya.Point(r,r), pya.Point(r,-r)])
      polygon = polygon.round_corners(0,r,128)
      rectangle = pya.Polygon([pya.Point(-r,0), pya.Point(-r,r), pya.Point(r,r), pya.Point(r,0)])
      tt = pya.ICplxTrans(1, 90, False, 0, 0)
      qCircle = pya.Region(polygon)-pya.Region(rectangle)-pya.Region(rectangle.transform(tt))
      
      
      # Create the trapezoid
      trapezoid = pya.Polygon([pya.Point(49500/dbu,-70500/dbu), pya.Point(40500/dbu,-20500/dbu), pya.Point(60500/dbu,-20500/dbu), pya.Point(51500/dbu,-70500/dbu)])
      tt = pya.ICplxTrans(-rx,-ry)
      
      cassette = qCircle + pya.Region(trapezoid.transform(tt))

      return cassette

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
  region = a.invert(region,10/dbu)
  cell.shapes(layer).insert(region)
  
  #Creates a dashed cross
  tt = pya.ICplxTrans(0,-200000)
  region = a.cross(10/dbu,50/dbu,1)
  cell.shapes(layer).insert(region, tt)
  region = a.cross(10/dbu,50/dbu,2)
  cell.shapes(layer).insert(region, tt)
  tt = pya.ICplxTrans(-100000,-200000)
  region = a.cross(10/dbu,100/dbu,1)
  cell.shapes(layer).insert(region, tt)
  region = a.cross(10/dbu,100/dbu,2)
  cell.shapes(layer).insert(region, tt)
  
  #Creates a vernier pattern and inserts it into the test cell
  tt = pya.ICplxTrans(-100000,0)
  region = a.vernier(4/dbu, 40/dbu, 8.2/dbu)
  region.transform(tt)
  cell.shapes(layer).insert(region)
  
  #Creates an invert vernier pattern and inserts it into the test cell
  tt = pya.Trans(2, False, -160000,0)
  region = a.vernier(4/dbu, 40/dbu, 8/dbu)
  region = a.invert(region, 10/dbu)
  cell.shapes(layer).insert(region,tt)
  
  tt = pya.ICplxTrans(0,80000)
  region = a.text("0123456789 Hello")
  cell.shapes(layer).insert(region,tt)
  
  tt = pya.ICplxTrans(0,100000)
  region = a.text("0123456789")
  region = a.invert(region, 10/dbu)
  cell.shapes(layer).insert(region,tt)
  
  #Create checkboard patterns
  tt = pya.ICplxTrans(-100000,150000)
  region = a.checkerboard(10/dbu,4)
  cell.shapes(layer).insert(region,tt)
  tt = pya.ICplxTrans(0,150000)
  region = a.checkerboard(10/dbu,5)
  cell.shapes(layer).insert(region,tt)
  
  #Create Si Wafer patterns
  tt = pya.ICplxTrans(-100000,200000)
  region = a.siWafer(50.8/dbu,15.88/dbu, 8/dbu, 90,128)
  cell.shapes(layer).insert(region,tt)
  tt = pya.ICplxTrans(0,200000)
  region = a.siWafer(50.8/dbu,15.88/dbu, 8/dbu, 45,128)
  cell.shapes(layer).insert(region,tt)
  
  #Create cassette patterns
  tt = pya.ICplxTrans(100000,0)
  region = a.pieceHolderCassette()
  cell.shapes(layer).insert(region,tt)
  
  #Create circle patterns
  tt = pya.ICplxTrans(-100000,250000)
  region = a.circle(50/dbu, 16)
  cell.shapes(layer).insert(region,tt)
  
  #Create ring patterns
  tt = pya.ICplxTrans(0,250000)
  region = a.ring(50/dbu,25/dbu, 32)
  cell.shapes(layer).insert(region,tt)
  tt = pya.ICplxTrans(100000,250000)
  region = a.ring(50/dbu,25/dbu, 32, False)
  cell.shapes(layer).insert(region,tt)
  
  cv.cell = cell

if __name__ == '__main__':
  #This function will automatically run if Python is running this file
  testKLayout()