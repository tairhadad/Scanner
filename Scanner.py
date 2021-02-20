# Tair Hadad - 204651897
#Shir Bar - 313253668
import cv2
import imutils
from skimage.filters import threshold_local
from imutils.perspective import four_point_transform
import argparse

'''
    import the image, create a copy so we can restore the original size  
'''
def ImportImage(path):
    image = cv2.imread(path)
    orig = image.copy()
    rows, cols, x = orig.shape
    if (rows>cols and rows > 1600):
        scale_percent = 40  # percent of original size
    elif (rows<cols and cols > 1200):
        scale_percent = 40  # percent of original size
    else:
        scale_percent = 100
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return image,orig

def PreProcessing (image):
    #GussianBlur for make the img more clear without unnesseccery noises
    # (5,5) is the kernel size and 0 is sigma that determines the amount of blur
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (5, 5), 0)

    '''
        canny method detect edgess in an image
        canny(img, trashhold1, trashhold2)
        trashhold1 - it is the high treshold value of intensity gradint
        treshhold2 - it is the low treshold value of intensity gredient
        75 MinThreshold and 200 is the MaxThreshold
    '''
    edged = cv2.Canny(img, 75, 200)
    cv2.imwrite("Images//PreProcessing.png", edged)
    return edged
'''
    cv2.CHAIN_APPROX_none => draw a full frame of borders 
    cv2.RETR_LIST- gives all the contours and doesn't even bother calculating the hierarchy --
    good if you only want the contours and don't care whether one is nested inside another.
'''

def FindingCounter (edgs, image):

    Counters = cv2.findContours(edgs.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # clear th set of counter from noises in order to avoid False positive
    Counters = imutils.grab_contours(Counters)
    Counters = sorted(Counters,key=cv2.contourArea,reverse=True)[:5]

    for counter in Counters:
        #epsilon - calculate te perimeter of the counter using arcLength
        epsilon = cv2.arcLength(counter, True)
        # get approximation of the counter with 4 points
        approx= cv2.approxPolyDP(counter, 0.02 * epsilon, True)


        #We assum that the image presents with 4 points
        if len(approx) == 4:
            pageCnt = approx
            break

    if len(approx) != 4:
        print("No Contours is found")
        exit(0)
    # draw the blue borders on the images
    cv2.drawContours(image, [pageCnt], -1, (0,255,0), 4)
    cv2.imwrite("Images//drawContours.jpg",image)

    return pageCnt

def PerspectiveTransform(img, pageCnt,rows, cols,outputPath):
    # get 4 points of borders image
    warped = four_point_transform(img, pageCnt.reshape(4, 2))

    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    # t = threshold_local(warped, 11,offset=10, method ="gaussian")
    # warped = (warped > t).astype("uint8") * 255

    '''
        resize the img to the original size using resize method 
    '''
    warped_resize = cv2.resize(warped, (cols,rows), interpolation=cv2.INTER_AREA)
    ret, thresh1 = cv2.threshold(warped_resize, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite(outputPath,thresh1)


#-------------------------------------------------------------------------------------#
parser = argparse.ArgumentParser()
parser.add_argument('PathI',metavar='Path',type=str)
parser.add_argument('pathO',metavar='Path',type=str)
args = parser.parse_args()

if args.PathI and args.pathO:
    PathI = args.PathI[0]
    pathO = args.pathO[0]

InputPath = args.PathI
OutputPath = args.pathO

img,orig = ImportImage(InputPath)
rows, cols, ch = orig.shape
edgs = PreProcessing(img)
pageCnt = FindingCounter(edgs,img)
img_transform = PerspectiveTransform(img,pageCnt,rows, cols,OutputPath)
print('Output is done!')