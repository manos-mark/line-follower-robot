"""
- This module saves images and a log file.
- Images are saved in a folder.
- Folder should be created manually with the name "DataCollected"
- The name of the image and the steering angle is logged
in the log file.
- Call the save_data function to start.
- Call the save_log function to end.
- If runs independent, will save ten images as a demo.
"""

import pandas as pd
import os
import cv2
from datetime import datetime

global image_list, steering_list
count_folder = 0
count = 0
image_list = []
steering_list = []


# GET CURRENT DIRECTORY PATH
my_directory = os.path.join(os.getcwd(), 'DataCollected')
# print(myDirectory)

# CREATE A NEW FOLDER BASED ON THE PREVIOUS FOLDER COUNT
while os.path.exists(os.path.join(my_directory, f'IMG{str(count_folder)}')):
    count_folder += 1
new_path = my_directory + "/IMG" + str(count_folder)
os.makedirs(new_path)


# SAVE IMAGES IN THE FOLDER
def save_data(img, steering):
    global image_list, steering_list
    now = datetime.now()
    timestamp = str(datetime.timestamp(now)).replace('.', '')
    # print("timestamp =", timestamp)
    file_name = os.path.join(new_path, f'Image_{timestamp}.jpg')
    cv2.imwrite(file_name, img)
    image_list.append(file_name)
    steering_list.append(steering)


# SAVE LOG FILE WHEN THE SESSION ENDS
def save_log():
    global image_list, steering_list
    raw_data = {'Image': image_list,
                'Steering': steering_list}
    df = pd.DataFrame(raw_data)
    df.to_csv(os.path.join(my_directory, f'log_{str(count_folder)}.csv'), index=False, header=False)
    print('Log Saved')
    print('Total Images: ', len(image_list))


if __name__ == '__main__':
    cap = cv2.VideoCapture(1)
    for x in range(10):
        _, img = cap.read()
        save_data(img, 0.5)
        cv2.waitKey(1)
        cv2.imshow("Image", img)
    save_log()
