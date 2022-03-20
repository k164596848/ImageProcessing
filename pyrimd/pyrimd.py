import cv2
import numpy as np
from PIL import Image


def pydec(a0):
    #獲取input image(a0) 的高、寬、通道數
    a_row,a_col,a_ch = a0.shape
   
    #對 a0 做高斯模糊
    gauss=cv2.GaussianBlur(a0,(7,7),10)
    
    #將高斯模糊後的a0做 downsampe, a1其尺寸為a0的1/2 
    a1 = cv2.resize(gauss,(int(a_row*0.5),int(a_col*0.5)),interpolation=cv2.INTER_LINEAR)
    
    #將 a1 放大尺寸到與 a0 的大小一致
    enlarge_a1 = cv2.resize(a1,(a_row,a_col),interpolation=cv2.INTER_LINEAR)

    #d0 為殘差
    d0 = (enlarge_a1  - a0)

    return[a1,d0]

def pycon(a1,d0):
    #獲取高、寬
    d_row,d_col,ch  = d0.shape
    
    #將 a1 放大尺寸到與 d0 的大小一致
    enlarge_a1 = cv2.resize(a1,(d_row,d_col),interpolation=cv2.INTER_LINEAR)

    #加入下層殘差
    a0 = (enlarge_a1 + d0)
    
    return a0

def pyrimid(img,current=0,layer=4):
    #利用遞迴的方式產生層數不同的金字塔分解與合成
    if current<=layer:
        a1,d0 = pydec(img)
        a0 = pycon(a1,d0)
        pyrimid(a1,current+1)


        if(d0.shape[0]<512):
            scaled_d0 = cv2.resize(d0,(512,512),interpolation=cv2.INTER_LINEAR)
            scaled_a0 = cv2.resize(a0,(512,512),interpolation=cv2.INTER_LINEAR)
            # cv2.imshow("d0"+str(current),scaled_d0+0.5)
            cv2.imshow("a1"+str(current),scaled_a0)
            cv2.waitKey(0)
        else:
            # cv2.imshow("d0"+str(current),d0+0.5)
            cv2.imshow("a1"+str(current),a0)
            cv2.waitKey(0)
    pass 


def fusion(apple,wood):
    
    #產生蘋果照片的金字塔分解內容與材質
    a10 ,d0 = pydec(apple)
    a11 ,d1 = pydec(a10)
    a12 ,d2 = pydec(a11)
    a13 ,d3 = pydec(a12)
    a14 ,d4 = pydec(a13)

    # 產生木頭照片的金字塔分解內容與材質
    w10,r0 =pydec(wood)
    w11,r1 =pydec(w10)
    w12,r2 =pydec(w11)
    w13,r3 =pydec(w12)
    w14,r4 =pydec(w13)

    # 前兩層內容:材質 = 1:0
    fusion4= cv2.resize(a14,(r4.shape[0],r4.shape[0]),interpolation=cv2.INTER_LINEAR) +0*r4
    fusion3= cv2.resize(a13,(r3.shape[0],r3.shape[0]),interpolation=cv2.INTER_LINEAR) +0*r3
    #逐漸提高材質比例
    fusion2= cv2.resize(a12,(r2.shape[0],r2.shape[0]),interpolation=cv2.INTER_LINEAR) + r2*0.33
    fusion1= cv2.resize(a11,(r1.shape[0],r1.shape[0]),interpolation=cv2.INTER_LINEAR) + r1*0.67
    # 最後一層內容:材質 = 0:1 
    fusion0= cv2.resize(a10,(r0.shape[0],r0.shape[0]),interpolation=cv2.INTER_LINEAR) + r0*1
    #展示結果圖片
    cv2.imshow("fusion4",cv2.resize(fusion4,(512,512),interpolation=cv2.INTER_LINEAR))
    cv2.imshow("fusion3",cv2.resize(fusion3,(512,512),interpolation=cv2.INTER_LINEAR))
    cv2.imshow("fusion2",cv2.resize(fusion2,(512,512),interpolation=cv2.INTER_LINEAR))
    cv2.imshow("fusion1",cv2.resize(fusion1,(512,512),interpolation=cv2.INTER_LINEAR))
    cv2.imshow("fusion0",fusion0)
    cv2.waitKey(0)


    






if __name__ == "__main__":
    #load img from folder
    apple = cv2.imread("a10.jpg")
    wood = cv2.imread("a20.JPG")
    #resize image as 512x512 使用 雙線性內插
    apple = cv2.resize(apple,(512,512),interpolation=cv2.INTER_LINEAR)
    wood = cv2.resize(wood,(512,512),interpolation=cv2.INTER_LINEAR)
    #將圖片 normalize 0~1 其中 max=255;min=0 且是浮點數
    a10 = cv2.normalize(apple,None,0,1, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    a20 = cv2.normalize(wood,None,0,1, cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    # pyrimid(a10)
    # pyrimid(a20)

    # a1,d0 = pydec(a10)
    # a0 = pycon(a1,d0)

    # fusion(a10,a20)

    cv2.imshow("test",0.5*(a10+a20))
    cv2.imshow("a10",a10)
    cv2.imshow("a20",a20)
    cv2.waitKey(0)

    # cv2.imshow("a0",a10)
    # cv2.imshow("a0",a20)
    # cv2.waitKey(0)




    pass