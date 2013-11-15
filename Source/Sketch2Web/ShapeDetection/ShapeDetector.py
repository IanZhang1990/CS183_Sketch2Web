import numpy
import cv2

class ShapeDetector(object):
    """This Shape Detectior class detects basic shapes, including triangle, rectangel and circle in a given image."""

    def __init__(self, image):
        self.mImg = image;
        pass

    def detectShapes( self, image ):
        pass

    def angleCos( self, point0, point1, point2 ):
        """Get the cosin value between tow lines: pt0->pt1 and pt0->pt2.
        Reference: """
        dx1 = point1.x - point0.x;
        dy1 = point1.y - point0.y;
        dx2 = point2.x - point0.x;
        dy2 = point2.y - point0.y;
        cosAngle = (dx*dx2 + dy1*dy2)/sqrt( (dx1*dx1 + dy1*dy1)*(dx2*dx2 + dy2*dy2) + 0.0001 )

        return cosAngle
        pass

    def detectShapes(self):
        src = self.mImg;
        if( src.empty() ):
            return;

        # Convert to gray scale
        gayimg = cv2.cvtColor( src, cv2.COLOR_BGR2GRAY)

        # use Canny instead of threshold to catch squares with gradient shading
        blackWhite = cv2.Canny(grayimg, 0, 50, 5 )

        # find contours
        contours = cv2.findContours( blackWhite.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE);

        for i in range(0, len(contours)):
            # Approximate contour with accuracy aproportional to the contour perimeter
            approx = cv2.approxPolyDP( contours[i], cv2.arcLength(contours[i], True ) * 0.02, True )

            # skip small or non-convex objects
            if( numpy.abs( cv2.contourArea( contours[i] ) ) < 00 or (not cv2.isContourConvex( approx )) ):
                continue
            
            if( approx.size() == 3 ):
                pass
        pass