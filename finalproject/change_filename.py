import os


# 指定要查詢的路徑
yourPath = r"C:/Users/user/Desktop/w/"


allFileList = os.listdir(yourPath)
# 逐一查詢檔案清單
for file in allFileList:
  counter_folder=0 #用來命名資料夾的計數器
  if file == 'test' or 'train':    #一定要有test/train資料夾
      first_path = os.path.join(yourPath , file)
      for folder in os.listdir(first_path):
          os.rename(first_path + '/' + folder , first_path + '/' + f'{counter_folder}_{folder}')   #重新命名資料夾到規定格式
          second_path = first_path + '/' + f'{counter_folder}_{folder}'  #創建一個新的檔案路徑訪問資料夾下的檔案
          counter_files=1
          for files in os.listdir(second_path):
              os.rename(second_path + '/' + files , second_path + '/' + f'{counter_files}.jpg')    #重新命名資料夾裡的圖片檔到規定格式
              counter_files+=1  #檔案命名計數器
          counter_folder+=1
      print('successfully change',file)
  else:
      print('naming error !!! please rename the folder to train/test only  !!!') #若沒有test/train資料夾就退出程式
      break
