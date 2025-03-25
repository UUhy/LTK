# SVG writer for Klayout
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

class svg(object):
  '''      
    Writes an svg file for KLayout
      
    Parameters
    ---------
    text : string
      Contains the text for an svg file
    
    Functions
    --------
    startGroup
    endGroup
    insertBox
    insertPolygon
    write
    '''
  def __init__(self, width, height):
    '''
    Initializes the class
    
    Parameters
    ---------
    width : float
          The width of the svg document
    height : float
          The height of the svg document
    
    Description
    ---------
    Specifies the size of the svg document
    '''
    self.text = '<svg width="%.12g" height="%.12g" xmlns="http://www.w3.org/2000/svg">\n' % (width,height)
    
  def __repr__(self):
    return ''
  
  def startGroup(self, layerProperty):
    '''
    startGroup(layerProperty)
    
    Starts an svg group element with style
    
    Parameters
    ---------
    layerProperty : pya.LayerProperties
          The layer properties contain fill color and stroke color information that will be used to add style to the shapes
    
    Description
    ---------
    All svg elements inside a group will be formatted the same way
    '''
    fillColor = '%06x' % (layerProperty.fill_color & 0xffffff)
    strokeColor = '%06x' % (layerProperty.frame_color & 0xffffff)
    self.text += '  <g fill="#%s" stroke="#%s">\n' % (fillColor, strokeColor)
  
  def endGroup(self):
    '''
    endGroup()
    
    Ends an svg group element
    '''
    self.text += '  </g>\n'
  
  def insertPolygon(self, poly):
    '''
    insertPolygon(poly)
    
    Inserts a polygon
    
    Parameters
    ---------
    poly : pya.Polygon
          A polygon
    
    Description
    ---------
    Inserts the polygon as an svg path element. The shape of an svg path element is defined by one parameter: d
    The parameter d comprise of the following commands:
      M x y      move to coordinate x y
      L x y       line to coordinate x y
    Other commands can be found here: https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths
    '''
    #Create the path representation of the polygon
    #Begin the path element
    txt = '    <path d="M '
    #Insert the polygon hull
    for i in poly.each_point_hull():
      txt += "%.12g %.12g L " % (i.x, i.y)
    txt = txt[:-2]
    txt += "z "
    #Insert all polygon holes
    for i in range(poly.holes()):
      txt += "M "
      for j in poly.each_point_hole(i):
        txt += "%.12g %.12g L " % (j.x, j.y)  
      txt = txt[:-2]
      txt += "z "
    #Close the path element
    txt += '"/>\n'
    
    self.text += txt
  
  def insertBox(self, box):
    '''
    insertBox(box)
    
    Inserts a box
    
    Parameters
    ---------
    box : pya.Box
          A box
    
    Description
    ---------
    Inserts the box as an svg rect element. The shape of an svg rect element is defined by:
      x             the left edge of the rectangle
      y             the top edge of the rectangle
      width      the width of the rectangle
      height     the height of the rectangle
    '''
    #Create the rect element representation of the box
    self.text += '    <rect x="%.12g" y="%.12g" width="%.12g" height="%.12g" />\n' %(box.left, box.top, box.width(), box.height())
  
  def write(self, filename):
    '''
    write(filename)
    
    Writes the svg file
    
    Parameters
    ---------
    filename : string
          An absolute path to the file
    
    Description
    ---------
    Writes the svg file
    '''
    #Closes the svg tag
    self.text += "</svg>"
    
    #Open a file for writing
    f = open(filename, "w")
    #Write to the file
    f.write(self.text)
    #Close the file
    f.close()

def testKLayout():
  #This performs a simple test of the class and draws the result on the active layout in KLayout
  
  filename = pya.FileDialog.ask_save_file_name("Save As SVG", "", "SVG (*.svg)")
  
  #Gets a reference to the active cell view
  cv = pya.CellView().active()
  lv = cv.view()
  
  #Gets a reference to the active layout
  layout = cv.layout()
  
  #Gets a reference to the active cell
  cell = cv.cell
  
  #Gets the database unit
  dbu = layout.dbu
  
  #Gets the binding box of the active cell
  bbox = cell.bbox()
  #Create a transform for KLayout coordinates to SVG coordinate
  tc = pya.CplxTrans(1.0, 0.0, True,-bbox.left, bbox.top)
  
  #Initialize an SVG object and specify its dimension
  s = svg(bbox.width()*dbu, bbox.height()*dbu)
    
  #Get all the layers in the layer view    
  layerIterator = lv.each_layer()
  #For each layer
  for layer in layerIterator:
    #If the layer is not visible, then skip
    if not layer.visible:
      continue
    #Get all the shapes from this layer
    shapeIterator = cell.begin_shapes_rec(layer.layer_index())
    #If there are no shapes, then skip
    if shapeIterator.at_end():
      continue
    #Start an svg group
    s.startGroup(layer)
    while not shapeIterator.at_end():
      shape = shapeIterator.shape()
      if shape.is_box():
        #Insert a box shape with all the transformations and scaling
        s.insertBox(shape.box.transformed(tc * shapeIterator.trans())*dbu)
      elif shape.is_polygon():
        #Insert a polygon shape with all the transformations and scaling
        s.insertPolygon(shape.polygon.transformed(tc * shapeIterator.trans())*dbu)
      #Go to the next shape in the iterator
      shapeIterator.next()
    #End an svg group
    s.endGroup()
  #Write the file
  s.write(filename)
  
if __name__ == '__main__':
  #This function will automatically run if Python is running this file
  testKLayout()