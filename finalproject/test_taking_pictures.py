import cv2

# 選擇網路攝影機

cap = cv2.VideoCapture(0)
path='C:/Users/user/Desktop/E94086149_finalproject/'

while(True):
    # 從攝影機擷取一張影像
    ret, frame = cap.read()

    # 顯示圖片
    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite(path+'My Image.jpg',frame)
        img=cv2.imread(path+'My Image.jpg')
        cv2.imshow('picture', img)
        print('success')
        print('The picture will be saved to : '+ path)
        cv2.waitKey(10000)
        cv2.destroyWindow('picture')
        

    # 若按下 q 鍵則離開迴圈
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('End taking pictures,bye!')
        break
    


# 釋放攝影機
cap.release()

# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()