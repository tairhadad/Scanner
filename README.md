# Scanner
Document scanner


Libraries nedded:
cv2 imutils,numpy, skimage.filters, argsparse

=================================================================================
Code explenation:

to run the code please use the terminal and run the following line:
Scanner.py inputPath outputPath

The code first import the choosen image 
than create changes of the size if needded.

if the size of the high is higher than 1200 or if the weight is higher than 1600.

In the second step , we change the color of img to gray 
nd use GussianBlur for make the img more clear 
Then, we use Canny function for detect the edges of the img

In the next step we find the counter , and draw them over the img

In the last step, we perform binarization for get the scan in black and white 
and changed the size back to the originals sizes. 

To see the output, Go to check the output path you have chossed 
=================================================================================

Enjoy :)
