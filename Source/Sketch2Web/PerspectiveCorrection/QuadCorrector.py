# Filename: QuadCorrector
# Author: Yinan
# Reference: http://opencv-code.com/tutorials/automatic-perspective-correction-for-quadrilateral-objects/

import sys
import urllib2
import cv2
import numpy

class QuadCorrector(object):
    """This class corrects quadrilateral objects' perspective view. 
    Transform from perspective view to over head view."""

    def __init__(self):
        self.mCenter = ( 0, 0 );
        self.mInputImg = None;
        self.mOutputImg = None;
        pass;
    
    def __showImg( self, img ):
        cv2.imshow( "Temp Window", img );
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        pass;

    def showInput(self):
        # Set up a window to display the image, the window is named "Display"
        # cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
        # Show the image in a window named "Display"
        cv2.imshow( "Input", self.mInputImg );
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        pass;

    def showOutput(self):
        if self.mOutputImg is not None:
            cv2.imshow( "Output", self.mOutputImg );
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            pass;
        else:
            print "No output, yet!"

            
    def computeIntersection( self, line1, line2 ):
        """@param line1 and line2 are supposed to be a 4-element vector with (x1, y1, x2, y2)"""
        x1 = line1[0];       y1 = line1[1];
        x2 = line1[2];       y2 = line1[3];
        x3 = line2[0];       y3 = line2[1];
        x4 = line2[2];       y4 = line2[3];

        d = ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4))
        if d != 0:
            x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / d
            y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / d
            return [ x, y ]
        else:
            return [-1, -1]
        pass;


    def getOverViewImg( self, imageFilename ):
        self.mInputImg = cv2.imread( imageFilename )
        grayImg = cv2.cvtColor(self.mInputImg, cv2.COLOR_BGR2GRAY)
        blurImg = cv2.blur(grayImg, (3,3))
        edgesImg = cv2.Canny(blurImg, 100, 100, 3)
        lines = cv2.HoughLines( edgesImg, 1, numpy.pi/180, 70,  30, 10 )
        vec4lines = []
        # Present the lines in a 4-element tuple
        for rho,theta in lines[0]:
            a = numpy.cos(theta)
            b = numpy.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            vec4lines.append( [x1, y1, x2, y2] )
            #cv2.line( self.mInputImg, (x1, y1), (x2,y2), (0, 0, 255), 1 )

        # Get corners of the rectangle shape
        corners = None
        for i in range( 0, len(vec4lines) ):
            for j in range( i+1, len(vec4lines) ):
                intersectPoint = self.computeIntersection( vec4lines[i], vec4lines[j] )
                if( intersectPoint[0] >= 0 and intersectPoint[1] >= 0 ):
                    if( corners is None ):
                        corners = numpy.array([ [ intersectPoint[0], intersectPoint[0]] ])
                    else:
                        corners = numpy.append( corners, [intersectPoint], axis=0 )
                    pass
                pass
            pass

        approx = cv2.approxPolyDP( corners, cv2.arcLength(corners, True ) * 0.025, True )
        if( approx.size() != 4 ):
            print "The object might not be quadrilateral!!\n"
            return




x = numpy.array([[1,2]])
x= numpy.append( x, [[2,3]], axis=0 )
#print x
#print numpy.append([[1, 2, 3]], [[7, 8, 9]], axis=0)

corrector = QuadCorrector()
corrector.getOverViewImg(".\Resources\\Poker.jpg")




