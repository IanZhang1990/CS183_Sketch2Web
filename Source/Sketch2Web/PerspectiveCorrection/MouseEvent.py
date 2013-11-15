import cv2
import numpy

class MouseSelection:

    def __init__(self, image, corners):
        self.imgSrc = image
        self.corners = corners
        self.ifExit = False;
        self.chosenPoint = None;

    def on_mouse(self,event, x, y, flag, param):
        if(event == cv2.EVENT_LBUTTONDOWN):
            minDist = 1000000000000;
            for point in self.corners:
                dst = (point[0]-x)*(point[0]-x) + (point[1]-y)*(point[1]-y)
                if dst < minDist:
                    minDist = dst; self.chosenPoint = point;
                    pass
            pass
        elif(event == cv2.EVENT_RBUTTONDOWN):
           self.chosenPoint[0] = x;
           self.chosenPoint[1] = y;
           # Draw corner points
           cv2.circle( self.imgSrc, (self.chosenPoint[0], self.chosenPoint[1]), 3, ( 0, 255, 255 ), 3)

    def callback(self):
        while True:
             cv2.setMouseCallback("MouseSelection",self.on_mouse)
             cv2.imshow("MouseSelection", self.imgSrc)
             if cv2.waitKey(20) & 0xFF == 27:
                 break
             pass
        cv2.destroyAllWindows();

