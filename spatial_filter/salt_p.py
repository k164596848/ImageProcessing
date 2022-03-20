
import numpy as np 
import random
import cv2

def salt_pepper_noise(noise_img,persent):
    """
    將總數 N%的pixel變成胡椒鹽雜訊
    """
    #獲取高、寬
    row,col = noise_img.shape
    #需要變成雜訊的pixel總數
    target_n = int(row*col*persent)

    #隨機抽取高、寬座標，湊到符合需要變成雜訊的pixel總數
    candiate_p = []
    for i in range(noise_img.size):
        r = random.randint(0,row-1)
        c = random.randint(0,col-1)
        p =[r,c]
        if p not in candiate_p: candiate_p.append(p)
        if len(candiate_p)>=target_n:break 
    
    #將目標pixel變成胡椒鹽雜訊
    for p in candiate_p:
        if(random.random()>=0.5):noise_img[p[0]][p[1]]=255
        else: noise_img[p[0]][p[1]]=0
    
    #回傳胡椒鹽雜訊
    return noise_img
        
 
def salt_pn(noise_img,persent):
    """
    歷遍每個pixel,每個pixel有N%的機率被變成為胡椒鹽雜訊。
    """
    #圖片 高row、寬col
    row,col = noise_img.shape
    
    for r in range (row):
        for c in range(col):
            #如果再n%以內就加入雜訊
            if(random.randint(0,100)<persent):
                #決定是白點雜訊還是黑點雜訊，各有50%
                if(random.random()>=0.5):noise_img[r][c]=255
                else: noise_img[r][c]=0

    #回傳胡椒鹽雜訊影像
    return noise_img

if __name__ == "__main__":
    persent = random.random() #設定胡椒鹽濃度，這裡用random[0~1]
    #讀取圖片
    img=cv2.imread("ntust_gray.jpg",0)
    #呼叫胡椒鹽雜訊function
    noise_img=salt_pepper_noise(img,persent)
    #展示雜訊圖片
    cv2.imshow("salt&pepper_noise",noise_img)
    #儲存雜訊圖片
    cv2.imwrite("salt&pepper_noise.png",noise_img)
    cv2.waitKey(0)

    

   

