# -*- coding: UTF-8 -*-
import tkinter as tk
from tkinter.constants import *
from tkinter import filedialog
from PIL import Image,ImageTk
from test_model import *
from puttext_chinese import *

def open_model():
    global model
    entry_filename.delete(0, "end")
    model_path = filedialog.askopenfilename(title='開啟model', filetypes=[('h5', '*.h5')])
    entry_filename.insert('insert', model_path)
    tk.messagebox.showinfo('Processing','                                       Processing!\nPlease PRESS confirm and wait until messagebox shows successfully !')
    model = load_model(model_path, compile=False)
    print("Model Loaded Successfully.")
    print(model_path)
    tk.messagebox.showinfo('Model','Model load successfully !\n Then,load the label !!')

def open_label():
    global labels
    entry_filename.delete(0, "end")
    label_path = filedialog.askopenfilename(title='開啟label', filetypes=[('txt', '*.txt')])
    entry_filename.insert('insert', label_path)
    labels = load_labels(label_path)
    print('Label load successfully!')
    print(label_path)
    tk.messagebox.showinfo('Label','            Label loaded successfully!\nNow choose to load pictures,or take photos!')

def send():
    global imgtk
    entry_filename.delete(0, "end")
    img_path = filedialog.askopenfilename(title='開啟picture', filetypes=[('jpg', '*.jpg')])
    entry_filename.insert('insert', img_path)
    

    #open uninterface picture
    img=Image.open(img_path)
    img.thumbnail((400, 400))
    imgtk = ImageTk.PhotoImage(image=img)
    img_label=tk.Label(width=img.width,height=img.height,image=imgtk)
    img_label.place(x=0,y=220)
    print(img_path)

    _, height, width, channel = model.layers[0].output_shape[0]

    # load image for inference
    image_show = cv2.imread(img_path)
    image = cv2.cvtColor(image_show, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (width, height))
    image = image / 255.0
    image = np.reshape(image, (1, height, width, channel))

    # run inference on input image
    results = model.predict(image)[0]  # inference 
    label_id = np.argmax(results)
    prob = results[label_id]
    
    #detection and save
    tk.messagebox.showinfo('Detected successfully!!','Detected successfully!!\n')
    # print predict result
    print(50 * "=")
    print("Object in {}.jpg is a/an...".format(img_path))
    print("{}! Confidence={}".format(labels[label_id], prob))
    print(50 * "=")

    #put the result on the photo
    '''
    cv2.putText(image_show, f'{labels[label_id]}', (70, 350), cv2.FONT_HERSHEY_TRIPLEX, 8, (0, 255 , 0), 2, cv2.LINE_AA)    # 把辨識結果印在照片上
    cv2.putText(image_show, f'Confidence = {np.around(prob*100,2)}%', (70, 600), cv2.FONT_HERSHEY_TRIPLEX, 4, (255, 255, 0), 2, cv2.LINE_AA)    # 新增信心
    '''
    image_show = cv2ImgAddText(image_show,  f'{labels[label_id]}', 50, 150, (255, 69, 0), 150)
    image_show = cv2ImgAddText(image_show,  f'Confidence = {np.around(prob*100,2)}%', 50, 300, (255, 250, 250), 100)

    #choose save position
    tk.messagebox.showinfo('Detected successfully!! Choose your save position','Detected successfully!!\n Choose your save position!')
    save_path = filedialog.asksaveasfilename(title='選擇存檔位置', filetypes=[('jpg', '*.jpg')])
    save_path = save_path + '.jpg'
    
    #show
    cv2.namedWindow('picture detected',0)
    cv2.resizeWindow('picture detected', width , height)
    cv2.imshow('picture detected', image_show)
    cv2.waitKey(30000)
    cv2.destroyWindow('picture detected')
    cv2.imwrite(save_path,image_show)
    '''
    image_detected=Image.open(save_path)
    image_detected.thumbnail((400, 400))
    image_detected_tk = ImageTk.PhotoImage(image=image_detected)
    image_detected_label=tk.Label(width=image_detected.width,height=image_detected.height,image=image_detected_tk)
    image_detected_label.place(x=0,y=300)
    '''
    print('Detected successfully!')
    tk.messagebox.showinfo('Detected finished!!!','Detected finished!!!\nKeep detecting or exit!')

def taking_pictures():
    
    #import model,label
    global labels , model

    #open camera
    cap = cv2.VideoCapture(0)
    tk.messagebox.showinfo('Camera!!','You have just chosen taking pictures\nPRESS S to save picture , PRESS Q to quit!')

    while(True):
        #grab a photo
        ret, frame = cap.read()
        print('Hi there ! PRESS S to save picture , PRESS Q to quit!')

        # show 
        cv2.imshow('frame', frame)
        
        #press s save photo and detect
        if cv2.waitKey(1) & 0xFF == ord('s'):
            tk.messagebox.showinfo('Photo taken successfully!!!','You have just taken a photo!\n Choose your save position ')
            original_path = filedialog.asksaveasfilename(title='選擇存檔位置', filetypes=[('jpg', '*.jpg')])
            originaljpg_path = original_path + '.jpg'
            cv2.imwrite(originaljpg_path,frame)

            _, height, width, channel = model.layers[0].output_shape[0]

            # load image for inference
            image_show = cv2.imread(originaljpg_path)
            image = cv2.cvtColor(image_show, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (width, height))
            image = image / 255.0
            image = np.reshape(image, (1, height, width, channel))

            # run inference on input image
            results = model.predict(image)[0]  # inference 
            label_id = np.argmax(results)
            prob = results[label_id]
            
            #detection and save
            # print predict result
            print(50 * "=")
            print("Object in {}.jpg is a/an...".format(original_path))
            print("{}! Confidence={}".format(labels[label_id], prob))
            print(50 * "=")

            #put the result on the photo
            '''
            cv2.putText(image_show, f'{labels[label_id]}', (70, 350), cv2.FONT_HERSHEY_TRIPLEX, 8, (0, 255 , 0), 2, cv2.LINE_AA)    # 把辨識結果印在照片上
            cv2.putText(image_show, f'Confidence = {np.around(prob*100,2)}%', (70, 600), cv2.FONT_HERSHEY_TRIPLEX, 4, (255, 255, 0), 2, cv2.LINE_AA)    # 新增信心
            '''
            image_show = cv2ImgAddText(image_show,  f'{labels[label_id]}', 25, 25, (255, 69, 0), 30)
            image_show = cv2ImgAddText(image_show,  f'Confidence = {np.around(prob*100,2)}%', 25, 70, (255, 250, 250), 20)

            #choose save position
            #tk.messagebox.showinfo('Detected successfully!! Choose your save position','Detected successfully!! Choose your save position!')
            #save_path = filedialog.asksaveasfilename(title='選擇存檔位置', filetypes=[('jpg', '*.jpg')],initialdir=r'C:\Users\user\Desktop\E94086149_finalproject\save_pictures')
            #save_path = save_path + '.jpg'
            
            #show
            '''
            cv2.namedWindow('picture detected',0)
            cv2.resizeWindow('picture detected', image_show.shape[0] , image_show.shape[1])
            '''

            tk.messagebox.showinfo('Objected detected!!!','Detected objected!!')
            cv2.imshow('picture detected', image_show)
            cv2.waitKey(30000)
            cv2.destroyWindow('picture detected')
            detected_path = original_path + f'_detected.jpg'
            cv2.imwrite(detected_path,image_show)
            tk.messagebox.showinfo('Detected photo saved!!!',f'Detected photo will be saved to {detected_path}')
            print(f'Detected photo will be saved to {detected_path}')
            '''
            image_detected=Image.open(save_path)
            image_detected.thumbnail((400, 400))
            image_detected_tk = ImageTk.PhotoImage(image=image_detected)
            image_detected_label=tk.Label(width=image_detected.width,height=image_detected.height,image=image_detected_tk)
            image_detected_label.place(x=0,y=300)
            '''
            print('Detected successfully!')
            tk.messagebox.showinfo('Detected finished!!!','Detected finished!!!\nKeep photoing or exit!')

        # press q and leave
        if cv2.waitKey(1) & 0xFF == ord('q'):
            tk.messagebox.showinfo('End photoing!','                        End photoing!\nPlease choose sending pictures or photoing!')
            print('End taking pictures , bye!')
            break
        


    # 釋放攝影機
    cap.release()

    # 關閉所有 OpenCV 視窗
    cv2.destroyAllWindows()
    print('Bye')


#setup
w=tk.Tk()
w.title('辨識GUI')
w.geometry('600x600')


#按鈕
model_button=tk.Button(width='25',height=3,text='Load model',command=open_model,font=("宋體", 10, 'bold'))
model_button.place(x=0,y=0)
label_button=tk.Button(width='25',height=3,text='Load label',command=open_label,font=("宋體", 10, 'bold'))
label_button.place(x=200,y=0)
send_button=tk.Button(width='25',height=3,text='Load pictures',command=send,font=("宋體", 10, 'bold'))
send_button.place(x=0,y=100)
takepicture_button=tk.Button(width='25',height=3,text='Taking pictures',command=taking_pictures,font=("宋體", 10, 'bold'))
takepicture_button.place(x=200,y=100)



# 設定entry
entry_filename = tk.Entry(w, width=80, font=("宋體", 10, 'bold'))
entry_filename.place(x=0,y=200)

#tips

tk.messagebox.showinfo('Welcome!!','            Welcome!\nPlease load your model first!')

#
w.mainloop()