import cv2 
import numpy as np 
import math 
import matplotlib.pyplot as plt

def HOG(img):
    #讀取灰階字母樣本，並將樣本影像縮小至 16×16 像素。
    if(img.shape[0]!=16):
        img = cv2.resize(img,(16,16),interpolation=cv2.INTER_LINEAR)
        img = np.copy(img).astype("float32")

    #Sobel 水平邊緣檢測
    Gx = cv2.Sobel(img,cv2.CV_32F,1,0,ksize=3)
    #Sobel 垂直邊緣檢測
    Gy = cv2.Sobel(img,cv2.CV_32F,0,1,ksize=3)
    #梯度絕對值 M
    M=np.abs(Gx)+np.abs(Gy)

    row,col = img.shape
    #創建一個16*16且元素皆為0的array來存放計算好的方向角數值
    alpha = np.zeros((row,col),dtype=np.float32)
    
    for r in range(row):
        for c in range(col):
            #計算梯度方向角alpha
            alpha[r][c] = math.ceil((math.degrees(math.atan2(Gy[r][c],Gx[r][c]))%180)/45)

    #獲得長度 64(=4×4×4)的向量。
    HOG_A = alpha
    
    return HOG_A

def img2text(img):
    """將圖片轉換成文字"""
    h,w =img.shape
    img = cv2.resize(img,(312,32),interpolation=cv2.INTER_LINEAR)
    #使用Otsu二值化
    otsu_th,otsu_img = cv2.threshold(img,0,1,cv2.THRESH_OTSU)
    #反轉1<>0，以便於connected components辨識
    otsu_img=np.where(otsu_img==0,1,0).astype(np.uint8)
    #利用connected components 將components的中心點、數量、 長寬等資訊取出
    num_labels,labels_img,stats,centrodis =cv2.connectedComponentsWithStats(otsu_img,connectivity=8,ltype=cv2.CV_32S)
    #存放切割出來的字母
    letters =[]
    #components中心點位置，使用四捨五入計算
    center_p = np.round(centrodis, decimals=0)
    print(center_p)
    for k in range(1,num_labels):
        #將原影像中的字母分割出來
        letter = img[int(center_p[k][1]-np.min(center_p)):int(center_p[k][1]+13),int(center_p[k][0]-13):int(center_p[k][0]+13)]
        # cv2.imshow(str(k),letter)
        #將分割出來的字母影像 resize 到16X16
        letter = cv2.resize(letter,(16,16),interpolation=cv2.INTER_LINEAR)
        #存放進letters list
        letters.append(letter)
        
        
    # cv2.waitKey(0)
    
    #建立字母查詢字典
    letters_dict = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    #將字母樣本的HOG取出   
    sample_hogs = SampleHOG()
    
    #存放辨識出的字母
    predict_leeters = ""
    
    for letter in letters:
        #計算切割出字母的HOG
        letter_hog = HOG(letter)
        #存放計算距離後的數值
        distances  = []
        for sample_hog in sample_hogs:
            #計算計算切割出字母的HOG與樣本的HOG L2 距離
            dist = np.linalg.norm(sample_hog - letter_hog)
            distances.append(dist)
        #選出最小值的L2 distance的index
        letter_index = distances.index(min(distances))
        #放入辨識出的字母，letters_dict字典查詢
        predict_leeters=predict_leeters+letters_dict[letter_index]
    #顯示辨識結果
    print(predict_leeters)    
        

def SampleHOG():
    #產生26個字母的編號 ex:ABC01
    numbers  = ["ABC"+"%.2d" % i for i in range(1,27)]
    #存放26個樣本的HOG
    sample_hogs =[]
    for num in numbers:
        #讀取樣本A~Z圖片
        img = cv2.imread(num+".jpg",0)
        #放入樣本的HOG
        sample_hogs.append(HOG(img))
            
    return sample_hogs

if __name__ == "__main__":
    #讀取要辨識的影像
    img = cv2.imread("p2.jpg",0)
    #辨識字母
    img2text(img)
