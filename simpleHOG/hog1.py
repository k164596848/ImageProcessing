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
    #創建一個16*16且元素皆為0的array
    alpha = np.zeros((row,col),dtype=np.float32)
    
    for r in range(row):
        for c in range(col):
            #計算梯度方向角，α 超過[0 180]度範圍的，用mod(α, 180)限制其範圍
            alpha[r][c] = math.ceil((math.degrees(math.atan2(Gy[r][c],Gx[r][c]))%180)/45)
    
    #HOG Array
    HOG_A = alpha

    #獲得長度 64(=4×4×4)的向量。
    return HOG_A

def img_grid(img,grid_row,grid_col):
    """將輸入的img 切成指定大小的grids並回傳"""
    #存放切割好的grids
    grids=[]
    h,w=img.shape
    grid_h = int(h/grid_row)
    grid_w = int(w/grid_col)

    for r in range(0,h,grid_h):
        for c in range(0,w,grid_w):
            #裁切成4X4的大小
            crop_img = img[r:r+grid_h,c:c+grid_h]
            grids.append(crop_img)
    
    return grids

def show_hist(alpha):
    """將直方圖秀出來"""
    #切成4X4 Grid
    grid = img_grid(alpha,4,4)

    hist =[]
    for g in grid:
        #將4X4 grid 拉平成 1X16 list
        angle  =g.ravel(order='C')
        hist.append(angle)

    #劃出4X4的直方圖
    figure, axis = plt.subplots(4, 4)
    for i in range(0,4):
        for j in range(0,4):
            #直方圖的垂直尺度(垂直範圍)一致
            axis[i,j].set_ylim([0, 16])
            #繪製每個子區域的方向梯度直方圖
            axis[i,j].hist(hist[i*4+j], bins=np.arange(0,5)+0.5,range=(0,5), ec="k")
    plt.show()



def input(number):
    #2.1生成檔名字串
    img_name  = "ABC"+str(number)+".jpg"
    #讀取灰階字母樣本圖片
    img = cv2.imread(img_name,0)
    #獲得字母樣本 HOG 向量
    hog=HOG(img)
    #展示直方圖
    show_hist(hog)
    

def search(sample,img):
    """找尋與樣本圖片相似的區域並標記出來"""
    #獲取樣本的HOG
    sample = HOG(sample)
    
    #要辨識的影像resize 到 128X128
    img = cv2.resize(img,(128,128),interpolation=cv2.INTER_LINEAR)
    #複製一個辨識影像，要用來把B、G通道染紅
    img2= np.copy(img).astype("uint8")

    #存放計算L2距離的與座標
    candidates = {}
    row,col = img.shape
    #以16X16的windows區域進行辨識
    for r in range(row-16):
        for c in range(col-16):
            ROI = HOG(img[r:r+16,c:c+16])
            #計算L2 distance 
            diff = np.linalg.norm(sample - ROI)
            #將座標(key)與L2的距離(value)加入candidate字典
            candidates.update({(r,c):diff})
    #排序出前六名與樣本最小的L2距離的candidates  
    min_six_candidates =sorted(candidates.items(), key=lambda x:x[1])[0:6]

    for key,val in min_six_candidates:
        #將前六名的區域的B、G通道染紅
        img2[key[0]:key[0]+16,key[1]:key[1]+16]=img2[key[0]:key[0]+16,key[1]:key[1]+16]*0.5
    
    #合併影像
    img = cv2.merge([img2,img2,img])
    #顯示結果
    cv2.imshow("search result",img)
    cv2.waitKey(0)        
 


if __name__ == "__main__":

    # input("01")
    # input("15")

    taget = cv2.imread("t3.jpg",0)
    samp_img = cv2.imread("ABC15.jpg",0)
    search(samp_img,taget)



