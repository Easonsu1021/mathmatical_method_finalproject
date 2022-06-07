import time
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import cv2
from puttext_chinese import *


def load_labels(path):
    with open(path, 'r',encoding="utf-8") as f:
        return {i: line.strip() for i, line in enumerate(f.readlines())}


def detect(labels , model , img_name):
    '''labels = load_labels(label_path)
    model = load_model(model_path, compile=False)
    print("Model Loaded Successfully.")'''

    _, height, width, channel = model.layers[0].output_shape[0]
    #print("Required input Shape ({}, {}, {})".format(height, width, channel))

    # load image for inference
    image_show = cv2.imread(img_name)
    #image = cv2.cvtColor(image_show, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image_show, (width, height))
    image = image / 255.0
    image = np.reshape(image, (1, height, width, channel))

    # run inference on input image
    #results = model.predict(image)[0]  # inference first time
    #start_time = time.time()
    results = model.predict(image)[0]  # inference second time
    #stop_time = time.time()
    label_id = np.argmax(results)
    prob = results[label_id]

    # print predict result~
    print(50 * "=")
    print("Object in {} is a/an...".format(img_name))
    print("{}! Confidence={}".format(labels[label_id], prob))
    print(50 * "=")
    #print("Time spend: {:.5f} sec.".format(stop_time - start_time))

    #show result
    '''
    cv2.putText(image_show, f'{labels[label_id]}', (0, 60), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1.5, (255, 192 , 203), 1, cv2.LINE_AA)    # 新增文字
    cv2.putText(image_show, f'Confidence = {np.around(prob*100,2)}%', (0, 100), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (250, 255, 240), 1, cv2.LINE_AA)    # 新增文字
    '''
    image_show = cv2ImgAddText(image_show,  f'{labels[label_id]}', 10, 100, (255, 69, 0), 100)
    image_show = cv2ImgAddText(image_show,  f'Confidence = {np.around(prob*100,2)}%', 10, 250, (255, 250, 250), 50)
    cv2.imshow('picture', image_show)
    cv2.waitKey(10000)
    cv2.destroyWindow('picture')
    cv2.imwrite(img_name, image_show)

if __name__ == "__main__":

    #check if tensorflow is installed and its edition
    print(tf.__version__)
    
    #set label、model
    label_path = 'Vegetable_Images_mobilenetv2.txt'
    model_path = 'Vegetable_Images_mobilenetv2.h5'

    #load model
    labels = load_labels(label_path)
    model = load_model(model_path, compile=False)
    print("Model Loaded Successfully.")

    #open camera
    cap = cv2.VideoCapture(0)
    path='C:/Users/user/Desktop/E94086149_finalproject/save_pictures/'
    picture_counter=0
    
    
    while(True):
        #grab a photo
        ret, frame = cap.read()
        print('Hello , press s to save picture , and press q to quit!')

        # show 
        cv2.imshow('frame', frame)
        
        #press s save photo and detect
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite(path+f'My Image{picture_counter}.jpg',frame)
            img_name = path+f'My Image{picture_counter}.jpg'
            detect(labels , model , img_name)
            print('Save successfully!')
            print('The picture will be saved to : '+ path)
            picture_counter+=1

        # press q and leave
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('End taking pictures , bye!')
            break
        


    # 釋放攝影機
    cap.release()

    # 關閉所有 OpenCV 視窗
    cv2.destroyAllWindows()
    print('Bye')