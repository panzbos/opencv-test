import PySimpleGUI as sg
import cv2
import numpy as np
import time


"""
Demo program that displays a webcam using OpenCV
"""

car_classifier = cv2.CascadeClassifier('haarcascade_car.xml')

def main():

    sg.theme('DarkBlue')

    # define the window layout
    layout = [[sg.Text('OpenCV Demo', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image')],
              [sg.Button('Record', size=(10, 1), font='Helvetica 14'),
               sg.Button('Stop', size=(10, 1), font='Any 14'),
               sg.Button('Exit', size=(10, 1), font='Helvetica 14'), ]]

    # create the window and show it without the plot
    window = sg.Window('Demo Application - OpenCV Integration',
                       layout, location=(200, 300))

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    cap = cv2.VideoCapture(0)#'http://192.168.1.11:4747/video'
    recording = False

    while True:
        event, values = window.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            return

        elif event == 'Record':
            recording = True

        elif event == 'Stop':
            recording = False
            img = np.full((480, 640), 255)
            # this is faster, shorter and needs less includes
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['image'].update(data=imgbytes)

        if recording:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cars = car_classifier.detectMultiScale(gray, 1.4, 2)
            for (x,y,w,h) in cars:

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                #cv2.imshow('Cars', frame)

            imgbytes = cv2.imencode('.ppm', frame)[1].tobytes()  # ditto
            window['image'].update(data=imgbytes)
        

main()