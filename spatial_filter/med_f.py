import numpy as np 
import cv2 

if __name__== "__main__":
    #讀取雜訊影像
    img = cv2.imread("salt&pepper_noise.png",0)
    #獲取雜訊影像的高跟寬
    row,col = img.shape
    #在影像邊緣加上一圈跟邊緣一樣的數值，也就是padling
    pad_img = np.pad(img,1,mode='edge')
    #複製一個跟雜訊圖片一樣大小的矩陣(元素皆為0)
    obj_img = np.zeros((row,col)).astype(np.uint8)
    
    for r in range(1,row+1):
        for c in range(1,col+1):
            #擷取3*3的範圍
            med_f = pad_img[r-1:r+2,c-1:c+2]
            #將3*3的範圍內的元素作排列
            med_f = np.sort(med_f,axis=None)
            #選出中位數
            med_n =int(med_f.size/2)
            #將中位數填入輸出影像
            obj_img[r-1][c-1] = med_f[med_n]
    #展示結果影像
    cv2.imshow("meduim filter.png",obj_img)
    #儲存結果影像
    cv2.imwrite("meduim filter.png",obj_img)
    cv2.waitKey(0)
