import numpy as np 
import cv2

if __name__ == "__main__":    
    #生成元素都是1的3*3的矩陣
    mean_f=np.ones((3,3)).astype(np.float)
    #將矩陣除以9
    mean_f = mean_f/int(mean_f.size)
    #讀取雜訊影像
    img = cv2.imread("gaussian_noise.png",0)
    #獲取雜訊影像的高跟寬
    row,col = img.shape
    #在影像邊緣加上一圈跟邊緣一樣的數值，也就是padding
    pad_img = np.pad(img,1,mode='edge')
    #複製一個跟雜訊圖片一樣大小的矩陣(元素皆為0)
    obj_img = np.zeros((row,col)).astype(np.uint8)
    
    for r in range(1,row+1):
        for c in range(1,col+1):
            #擷取3*3的範圍
            obj = pad_img[r-1:r+2,c-1:c+2]
            #將中心點與濾鏡相乘
            mean_f_value = obj*mean_f
            #將結果加總在一起
            obj_img[r-1][c-1] = int( mean_f_value.sum())

    cv2.imshow("mean filter.png",obj_img)
    cv2.imwrite("mean filter.png",obj_img)
    cv2.waitKey(0)

