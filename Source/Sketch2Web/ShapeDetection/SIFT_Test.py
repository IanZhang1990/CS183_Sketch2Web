import numpy as np
import cv2


img1_path = "C:\\Users\\ianzh_000\\Documents\\GitHub\\CS183_Sketch2Web\\Source\\Sketch2Web\\Resources\\outputImg.jpg"
img2_path = "C:\\Users\\ianzh_000\\Documents\\GitHub\\CS183_Sketch2Web\\Source\\Sketch2Web\\Resources\\rect-template.png"

img1 = cv2.imread(img1_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
img2 = cv2.imread(img2_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)

detector = cv2.FeatureDetector_create("SURF")
descriptor = cv2.DescriptorExtractor_create("BRIEF")
matcher = cv2.DescriptorMatcher_create("BruteForce-Hamming")

# detect keypoints
kp1 = detector.detect(img1)
kp2 = detector.detect(img2)

print '#keypoints in image1: %d, image2: %d' % (len(kp1), len(kp2))

# descriptors
k1, d1 = descriptor.compute(img1, kp1)
k2, d2 = descriptor.compute(img2, kp2)

print '#keypoints in image1: %d, image2: %d' % (len(d1), len(d2))

# match the keypoints
matches = matcher.match(d1, d2)

# visualize the matches
print '#matches:', len(matches)
dist = [m.distance for m in matches]

print 'distance: min: %.3f' % min(dist)
print 'distance: mean: %.3f' % (sum(dist) / len(dist)) 
print 'distance: max: %.3f' % max(dist)

# threshold: half the mean
thres_dist = (sum(dist) / len(dist)) * 0.5

# keep only the reasonable matches
sel_matches = [m for m in matches if m.distance < thres_dist]

print '#selected matches:', len(sel_matches)

for m in sel_matches:
    cv2.circle( img1, (int(k1[m.queryIdx].pt[0]), int(k1[m.queryIdx].pt[1]) ), 10, (255,0,0) )
    cv2.circle( img2, (int(k2[m.trainIdx].pt[0]), int(k2[m.trainIdx].pt[0]) ), 10, (255,255,0) )


cv2.imshow( "Input", img1 );
cv2.imshow( "Template", img2 );
cv2.waitKey(0);
cv2.destroyAllWindows();