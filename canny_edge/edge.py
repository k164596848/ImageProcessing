import numpy as np
import cv2


base = 10
for x in range(5):
    imgpath = 'img\\'+ str(x+1) +'.jpg'
    image = cv2.imread(imgpath)
    print(type(image))
    gray= cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imwrite('blurred'+ str(x+1) +'.jpg',blurred)
    cv2.imwrite('gray'+ str(x+1) +'.jpg',gray)
    for i in range(24):
        threshold1 =base+i*5
        threshold2 = threshold1*2
        threshold3 = threshold1*3
        canny = cv2.Canny(gray, threshold1, threshold2)
        canny3 = cv2.Canny(gray,threshold1, threshold3)
        if(threshold2<255):
            cv2.imwrite(str(x+1)+"canny_2gray"+ str(threshold1) +".jpg",canny)
        if (threshold3<255):
            cv2.imwrite(str(x+1)+"canny_3gray"+ str(threshold1) +".jpg",canny3)
    for i in range(24):
        threshold1 =base+i*5
        threshold2 = threshold1*2
        threshold3 = threshold1*3
        canny = cv2.Canny(blurred, threshold1, threshold2)
        canny3 = cv2.Canny(blurred,threshold1, threshold3)
        if (threshold2<255):
            cv2.imwrite(str(x+1)+"canny2_blurred"+ str(threshold1) +".jpg",canny)
        if (threshold3<255):
            cv2.imwrite(str(x+1)+"canny3_blurred"+ str(threshold1) +".jpg",canny3)


cv2.waitKey(0)
# cv2.destroyAllWindows()