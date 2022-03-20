import cv2
import numpy as np 

if __name__ == "__main__":
    #輸入階調調整曲線 x 方向(input)控制點座標
    input=[0,0.3,0.7,1]
    #輸入階調調整曲線 y 方向(output)控制點座標
    output=[0,0.1,0.9,1]
    #獲取階調各的斜率
    tan1 =abs(output[1]-output[0])/abs(input[1]-input[0])  
    tan2 =abs(output[2]-output[1])/abs(input[2]-input[1])
    tan3 = abs(output[3]-output[2])/abs(input[3]-input[2])
    #讀取圖片，以灰階方式讀入
    img = cv2.imread("ntust_gray.jpg",0)
    #獲取影像高寬
    row, col = img.shape
    #複製一個image
    trans_img = np.copy(img).astype(np.uint8)

    for r in range(row):
        for c in range(col):
            #針對各個階調，進行換算
            #0~.03
            if img[r][c]<input[1]*255 and img[r][c]>input[0]*255:
                trans_img[r][c] = int(img[r][c]*tan1)
            #0.3~.07
            elif input[1]*255<=img[r][c] and img[r][c]<=input[2]*255:
                trans_img[r][c] = int(255*output[1])+int((img[r][c]-255*input[1])*tan2)
            #0.7~1
            elif img[r][c]>input[2]*255 and img[r][c]<=input[3]*255:
                trans_img[r][c] = int(255*output[2])+int((img[r][c]-255*input[2])*tan3)

    #展示結果
    cv2.imshow("trans im ",trans_img)
    #儲存結果
    cv2.imwrite("trans.png",trans_img)
    cv2.waitKey(0)