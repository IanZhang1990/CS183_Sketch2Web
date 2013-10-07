# Filename: QuadCorrector
# Author: Yinan
# Reference: http://opencv-code.com/tutorials/automatic-perspective-correction-for-quadrilateral-objects/

import sys
import urllib2
import cv2
import numpy
#import copy

class QuadCorrector(object):
    """This class corrects quadrilateral objects' perspective view. 
    Transform from perspective view to over head view."""

    def __init__(self):
        self.mCenter = ( 0, 0 );
        self.mInputImg = None;
        self.mOutputImg = None;
        self.mOutputImgSize = ( 800, 600 )
        pass;
    
    def setOutputSize( self, size ):
        self.mOutputImgSize = size;

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

    ##################################
    ### This is not right!!!!!!
    ##################################
    def classifyCorners(self, cornerPoints, center):
        """Sort each point, and get the calculated topLeft/ topRight/ bottomLeft/ bottomRight point"""
        topLeft = numpy.array([[0,0]]); topRight = numpy.array([[0,0]]);
        bottomLeft = numpy.array([[0,0]]); bottomRight = numpy.array([[0,0]]);
        # sort each point, find if they are topLeft/topRight/bottomLeft/bottomRight
        for point in cornerPoints:
            if point[1] < center[1] and point[0] < center[0]:
                topLeft = numpy.append(topLeft,  [point], axis=0 )
            elif point[1] < center[1] and point[0] > center[0]:
                topRight = numpy.append( topRight, [point], axis=0 )
            elif point[1] > center[1] and point[0] < center[0]:
                bottomLeft = numpy.append( bottomLeft, [point], axis=0 )
            elif point[1] > center[1] and point[0] > center[0]:
                bottomRight = numpy.append( bottomRight, [point], axis=0 )
                pass
            pass

        # for each point in each group, get the average value
        tlAvg = [0,0]; trAvg = [0,0]; blAvg = [0,0]; brAvg = [0,0];
        for point in topLeft:
            tlAvg += point;
        for point in topRight:
            trAvg += point;
        for point in bottomLeft:
            blAvg += point;
        for point in bottomRight:
            brAvg += point;

        if( len(topLeft) > 1 ):
            tlAvg /= (len(topLeft)-1)
        if( len(topRight) > 1 ):
            trAvg /= (len(topRight)-1)
        if( len(bottomLeft) > 1 ):
            blAvg /= (len(bottomLeft)-1)
        if( len(bottomRight) > 1 ):
            brAvg /= (len(bottomRight)-1)

        returnVal = numpy.float32([tlAvg, trAvg, blAvg, brAvg])
        return returnVal
        pass;

    def getOverViewImg( self, imageFilename ):
        self.mInputImg = cv2.imread( imageFilename )
        grayImg = cv2.cvtColor(self.mInputImg, cv2.COLOR_BGR2GRAY)
        blurImg = cv2.blur(grayImg, (3,3))
        edgesImg = cv2.Canny(blurImg, 100, 100, 3)
        #lines = cv2.HoughLines( edgesImg, 1, numpy.pi/180, 130 )
        # I changed cv2.HoughLines to cv2.HoughLinesP, That seems to be better.
        lines = cv2.HoughLinesP( edgesImg, 1, numpy.pi/180, 80, 30, 20 )
        vec4lines = lines[0]         # We need this only when using cv2.HoughLinesP()

        """
        # Present the lines in a 4-element tuple
        for rho,theta in vec4lines:
            a = numpy.cos(theta)
            b = numpy.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            #vec4lines.append( [x1, y1, x2, y2] )
            cv2.line( self.mInputImg, (x1, y1), (x2,y2), (255, 255, 255), 1 )
        # sortedLines = self.sortLinesBySlop( vec4lines );
        """
        
        for line in vec4lines:
            print line
            x1 = line[0];       y1 = line[1];
            x2 = line[2];       y2 = line[3];
            cv2.line( self.mInputImg, (x1, y1), (x2,y2), (255, 255, 255), 2 )


            
        
        # Get corners of the rectangle shape
        corners = None
        for i in range( 0, len(vec4lines) ):
            for j in range( i+1, len(vec4lines) ):
                intersectPoint = self.computeIntersection( vec4lines[i], vec4lines[j] )
                if( intersectPoint[0] >= 0 and intersectPoint[1] >= 0 ):
                    if( corners is None ):
                        corners = numpy.array([ [ intersectPoint[0], intersectPoint[1]] ])
                    else:
                        corners = numpy.append( corners, [intersectPoint], axis=0 )
                    pass
                cv2.circle( self.mInputImg, (intersectPoint[0], intersectPoint[1]), 3, ( 0, 255, 255 ), 3)
                pass
            pass
        self.showInput()



        approx = cv2.approxPolyDP( corners, cv2.arcLength(corners, True ) * 0.02, True )
        #if( len(approx) != 4 ):
        #    print "The object might not be quadrilateral!!\n"
        #    return

        # Get mass center
        center = [0,0]
        for corner in corners:
            center += corner

        center /= len(corners)
        # determin each corner point's position
        quadCornerPoints = self.classifyCorners( corners, center )
        
        imgCopy = self.mInputImg.copy()
        # Draw Lines based on the corner points we got
        for i in range( 0, len( vec4lines ) ):
            line = vec4lines[i]
            cv2.line( imgCopy, (line[0], line[1]), (line[2], line[3]), (0, 255, 0), 1 )
        #self.__showImg( imgCopy )

        # Draw corner points
        cv2.circle( imgCopy, (quadCornerPoints[0][0], quadCornerPoints[0][1]), 3, ( 255, 0, 0 ), 3)
        cv2.circle( imgCopy, (quadCornerPoints[1][0], quadCornerPoints[1][1]), 3, ( 0, 255, 0 ), 3)
        cv2.circle( imgCopy, (quadCornerPoints[2][0], quadCornerPoints[2][1]), 3, ( 0, 0, 255 ), 3)
        cv2.circle( imgCopy, (quadCornerPoints[3][0], quadCornerPoints[3][1]), 3, ( 255, 255, 255 ), 3)

        # Draw mass center 
        cv2.circle( imgCopy, (center[0], center[1]), 3, ( 255, 255, 0 ), 2 )
        self.__showImg( imgCopy )

        imgCols = self.mOutputImgSize[0]
        imgRows = self.mOutputImgSize[1] 
        dstQuadPoints = numpy.float32( [[0,0], [imgCols,0], [0, imgRows], [imgCols, imgRows]] )
        transMtrix = cv2.getPerspectiveTransform( quadCornerPoints, dstQuadPoints )
        self.mOutputImg = cv2.warpPerspective( self.mInputImg, transMtrix, (imgCols,imgRows))
        cv2.imshow( "Input", self.mInputImg );
        cv2.imshow( "Output", self.mOutputImg );
        cv2.waitKey(0)
        cv2.destroyAllWindows()


x = numpy.array([[1,2]])
x = numpy.append( x, [[2,3]], axis=0 )
#print x
#print numpy.append([[1, 2, 3]], [[7, 8, 9]], axis=0)

corrector = QuadCorrector()
corrector.setOutputSize( (600, 800) )
# Use this in Visiual Studio
#corrector.getOverViewImg(".\Resources\\best.jpg")
# If you are using other IDE, you probably want to change the path of the image
corrector.getOverViewImg("C:\\Users\\ianzh_000\\Documents\\GitHub\\CS183_Sketch2Web\\Source\\Sketch2Web\\Resources\\tip3.jpg")




