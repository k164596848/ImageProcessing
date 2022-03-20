import numpy as np
import cv2 
import random



if __name__ == "__main__":

    #高斯的離散程度
    sigma = 20
    #-100~100，有201個數值
    x = np.arange(-100,101).astype(np.float64)
    #帶入高斯分配 公式
    y= np.exp(-(x**2)/(2*(sigma**2))).astype(np.float64)
    #Normalization
    y = y/y.sum()
    #計算高斯累計的y值
    cum = 0 
    cum_y =[]
    for i in range(0,np.size(x)):
        cum=cum+y[i]
        cum_y.append(cum)
    
    #將高斯累計的y值，與對x(-100~100)相對應，存成list
    cum_y_list =[]
    i =x[0]
    for val in range(0,len(cum_y)):
        cum_y_list.append([cum_y[val],i])
        i=i+1

    #讀取圖片
    img = cv2.imread("ntust_gray.jpg",0)
    #獲取圖片的高、寬
    row,col= img.shape 

    for r in range (row):
        for c in range(col):
            #p:生成0~1的隨機數
            p = random.random()
            
            for gaussian_cum in cum_y_list:
                #gaussian_cum[0]:為累計的y值
                if gaussian_cum[0]>=p:
                    temp = img[r][c]
                    #加入雜訊，gaussian_cum[1]:為對應的x值(noise)
                    temp =temp+ gaussian_cum[1]
                    #因為會有shift的現象，若加入雜訊後<0，則等於0。若加入雜訊後>255，則等於255。
                    if(temp<=0):temp=0
                    elif(temp>=255):temp=255
                    img[r][c] = temp
                    #為省時間跳離迴圈
                    break
    
    cv2.imshow("gaussian_noise",img)
    cv2.imwrite("gaussian_noise.png",img)
    cv2.waitKey(0)
        
        
